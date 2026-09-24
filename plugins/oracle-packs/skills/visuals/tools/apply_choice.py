#!/usr/bin/env python3
"""Record the owner's choice for one picture slot.

    apply_choice.py <pack-spec.yaml> --slot <slot> --file <chosen file>
                    [--provenance <sidecar.json>] [--note "<why>"]
                    [--add-to-library] [--library <dir>] [--dry-run]

Four things happen, in this order, and either all of them or none:

  1. the chosen file (and, for an icon, its other colour render) is copied into
     `packs/<slug>/visuals/` beside the spec, in the packaging-skills repo;
  2. the spec key for the slot is written — `verticals[i].icon`, `deck.images.today`,
     `deck.images.tomorrow`, `one_pager.images.hero` (the list is in visuals_common.SLOT_KINDS);
  3. a row is appended to `packs/<slug>/visuals/credits.md`;
  4. a line is appended to the pack's decisions log, `<work>/decisions.md` — the local work
     folder `shared/tools/pack_paths.py` names ($ORACLE_PACKS_OUT/<slug>, else
     ~/oracle-packs/<slug>), never the repo.

The spec is edited **in place as text**, not re-serialized: comments, block scalars and key order in
a hand-written spec survive. The edit is verified by re-parsing and comparing everything except the
key being written; if anything else moved, nothing is saved.

`--add-to-library` additionally copies a chosen icon into the shared icon library and adds its row
to the library's map. It is off by default and never overwrites: a name already in the library is
reported, not replaced.

A `supplied` slot — today only `customer_logo` — is the one exception to the licence gate. That
file comes from the owner's own engagement materials rather than from a picture library, so there
is no sidecar to read and no licence to check: the record says where it came from and that it is
used under the customer's clearance recorded in the pack brief, and the sidecar is written beside
the copy.

Exit codes: 0 applied · 1 usage or input error (unknown slot, missing file, no provenance) ·
2 the file's recorded licence is not one this bundle may use · 3 not used here.
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import os
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from visuals_common import (  # noqa: E402
    CREDITS_HEADER, EXIT_LICENCE, EXIT_OK, EXIT_USAGE, ICON_LICENCES, PHOTO_LICENCES,
    SUPPLIED_SOURCE, SUPPLIED_TERMS, credits_line, eprint, load_spec, pack_dir, parse_slot,
    provenance_record, read_sidecar, slot_kind, slot_spec_path, slugify, write_sidecar,
)

_HERE = Path(__file__).resolve().parent
for _up in range(2, 6):                     # pack_paths: the plugin's synced shared/tools, or the bundle's
    _shared = _HERE.parents[_up] / "shared" / "tools" if len(_HERE.parents) > _up else None
    if _shared is not None and (_shared / "pack_paths.py").is_file():
        sys.path.insert(0, str(_shared))
        break
import pack_paths  # noqa: E402  (the decisions log lives in the local work folder, not the repo)

DEFAULT_LIBRARY = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
    "shared", "data", "icons")

DECISIONS_HEADER = (
    "# Decisions\n"
    "\n"
    "One line per decision the owner made on this pack, newest at the bottom.\n"
    "\n"
)


# --------------------------------------------------------------------- the spec, edited as text

def _block_bounds(lines: list[str], start: int, indent: int) -> int:
    """Index one past the last line belonging to a block that starts at `start` with children more
    indented than `indent`. Blank lines and comments inside the block are kept."""
    i = start + 1
    last = start + 1
    while i < len(lines):
        ln = lines[i]
        if ln.strip() == "" or ln.lstrip().startswith("#"):
            i += 1
            continue
        if len(ln) - len(ln.lstrip(" ")) <= indent:
            break
        i += 1
        last = i
    return last


def _find_top_key(lines: list[str], key: str) -> int | None:
    for i, ln in enumerate(lines):
        if re.match(rf"^{re.escape(key)}\s*:", ln):
            return i
    return None


def _render(value: dict, indent: int) -> list[str]:
    pad = " " * indent
    out = []
    for k, v in value.items():
        s = str(v)
        quote = '"' if re.search(r"[:#\"']|^\s|\s$", s) else ""
        out.append(f"{pad}{k}: {quote}{s}{quote}\n")
    return out


def _set_list_item_child(lines: list[str], list_key: str, index: int, child: str,
                         value: dict) -> list[str]:
    """verticals[i].icon — replace or insert `child:` inside the i-th item of a top-level list."""
    top = _find_top_key(lines, list_key)
    if top is None:
        raise ValueError(f"the spec has no `{list_key}:` block")
    end = _block_bounds(lines, top, 0)
    items = [i for i in range(top + 1, end)
             if re.match(r"^(\s*)-\s", lines[i]) and
             (len(lines[i]) - len(lines[i].lstrip(" "))) == (len(lines[top + 1]) - len(lines[top + 1].lstrip(" ")))]
    if index >= len(items):
        raise ValueError(f"the spec has {len(items)} item(s) under `{list_key}:`; "
                         f"there is no number {index}")
    start = items[index]
    stop = items[index + 1] if index + 1 < len(items) else end
    item_indent = len(lines[start]) - len(lines[start].lstrip(" "))
    child_indent = item_indent + 2
    block = [" " * child_indent + f"{child}:\n"] + _render(value, child_indent + 2)

    for i in range(start, stop):
        if re.match(rf"^ {{{child_indent}}}{re.escape(child)}\s*:", lines[i]):
            j = _block_bounds(lines, i, child_indent)
            return lines[:i] + block + lines[j:]
    # not present: insert at the end of the item, after its last non-blank line
    j = stop
    while j > start and lines[j - 1].strip() == "":
        j -= 1
    return lines[:j] + block + lines[j:]


def _set_nested(lines: list[str], path: list[str], value: dict) -> list[str]:
    """deck.images.today — replace or insert a mapping at a nested path, creating what is missing."""
    top = _find_top_key(lines, path[0])
    if top is None:
        block = [f"\n{path[0]}:\n"]
        for depth, key in enumerate(path[1:], start=1):
            block.append("  " * depth + f"{key}:\n")
        block += _render(value, 2 * len(path))
        out = lines[:]
        while out and out[-1].strip() == "":
            out.pop()
        return out + block

    start, end, indent = top, _block_bounds(lines, top, 0), 0
    for depth, key in enumerate(path[1:], start=1):
        want = indent + 2
        hit = None
        for i in range(start + 1, end):
            if re.match(rf"^ {{{want}}}{re.escape(key)}\s*:", lines[i]):
                hit = i
                break
        if hit is None:
            block = []
            for d, k in enumerate(path[depth:], start=depth):
                block.append("  " * d + f"{k}:\n")
            block += _render(value, 2 * len(path))
            j = end
            while j > start and lines[j - 1].strip() == "":
                j -= 1
            return lines[:j] + block + lines[j:]
        start, indent = hit, want
        end = _block_bounds(lines, hit, want)
    return lines[:start] + ["  " * (len(path) - 1) + f"{path[-1]}:\n"] + \
        _render(value, 2 * len(path)) + lines[end:]


def _path_tokens(slot: str) -> list:
    base, idx = parse_slot(slot)
    spec_path = slot_spec_path(slot)
    if base == "vertical":
        return ["verticals", idx, "icon"]
    return spec_path.split(".")


def _with_value(obj, tokens, value):
    """A deep copy of the parsed spec with exactly this one path set — what the file must parse to
    after the edit. Comparing against it proves both that the value landed and that nothing else
    did; creating the intermediate mappings here is what makes a brand-new `deck:` block legal."""
    out = copy.deepcopy(obj)
    cur = out
    for t in tokens[:-1]:
        if isinstance(t, int):
            cur = cur[t]                       # a list index: the item must already be there
        else:
            nxt = cur.get(t)
            if nxt is None:                    # a missing mapping is created; a list is descended
                nxt = {}
                cur[t] = nxt
            cur = nxt
    cur[tokens[-1]] = value
    return out


def write_spec(spec_path: str, slot: str, value: dict, dry_run: bool) -> str:
    import yaml
    with open(spec_path, encoding="utf-8") as fh:
        lines = fh.readlines()
    before = yaml.safe_load("".join(lines)) or {}
    tokens = _path_tokens(slot)

    if isinstance(tokens[1] if len(tokens) > 1 else None, int):
        new = _set_list_item_child(lines, tokens[0], tokens[1], tokens[2], value)
    else:
        new = _set_nested(lines, tokens, value)

    text = "".join(new)
    after = yaml.safe_load(text) or {}
    expected = _with_value(before, tokens, value)
    if after != expected:
        raise RuntimeError("the edited file does not parse to the spec plus this one picture; "
                           "nothing written")
    if not dry_run:
        with open(spec_path, "w", encoding="utf-8") as fh:
            fh.write(text)
    return ".".join(str(t) for t in tokens)


# ------------------------------------------------------------------------------------ the files

def copy_in(chosen: str, visuals: str, slot: str, rec: dict) -> list[str]:
    os.makedirs(visuals, exist_ok=True)
    base = os.path.splitext(os.path.basename(chosen))[0]
    prefix = slugify(slot)
    stem = base if slugify(base).startswith(prefix) else slugify(f"{slot}-{base}")
    copied = []
    sources = [chosen]
    if rec.get("kind") == "icon":
        for sibling in (chosen.replace("-ink.png", "-white.png"),
                        chosen.replace("-white.png", "-ink.png")):
            if sibling != chosen and os.path.exists(sibling) and sibling not in sources:
                sources.append(sibling)
    for src in sources:
        ext = os.path.splitext(src)[1]
        suffix = "-white" if src.endswith("-white.png") else ("-ink" if src.endswith("-ink.png") else "")
        dst = os.path.join(visuals, f"{stem.removesuffix('-ink').removesuffix('-white')}{suffix}{ext}")
        shutil.copy2(src, dst)
        side = os.path.splitext(src)[0] + ".json"
        if os.path.exists(side):
            shutil.copy2(side, os.path.splitext(dst)[0] + ".json")
        copied.append(dst)
    return copied


def append_credits(visuals: str, rec: dict) -> str:
    path = os.path.join(visuals, "credits.md")
    fresh = not os.path.exists(path)
    with open(path, "a", encoding="utf-8") as fh:
        if fresh:
            fh.write(CREDITS_HEADER)
        fh.write(credits_line(rec) + "\n")
    return path


def work_folder(spec_path: str, spec: dict) -> str:
    """The pack's local work folder (pack_paths.py): the decisions log never enters the repo.

    The slug is the spec's folder name (`packs/<slug>/`), else `meta.slug`. A spec kept in a
    folder with neither a valid slug keeps its log beside it, as before 2026-09-24.
    """
    meta_slug = str(((spec or {}).get("meta") or {}).get("slug") or "")
    for candidate in (os.path.basename(pack_dir(spec_path)), meta_slug):
        if pack_paths.SLUG_RE.match(candidate):
            return pack_paths.work_dir(candidate)
    return pack_dir(spec_path)


def append_decision(work: str, slot: str, rec: dict, note: str) -> str:
    os.makedirs(work, exist_ok=True)
    path = os.path.join(work, "decisions.md")
    fresh = not os.path.exists(path)
    with open(path, "a", encoding="utf-8") as fh:
        if fresh:
            fh.write(DECISIONS_HEADER)
        bits = [dt.date.today().isoformat(), f"picture for **{slot}**",
                f"{os.path.basename(rec.get('file', '-'))}",
                f"{rec.get('source', '-')} · {rec.get('licence_name', '-')}"]
        if note:
            bits.append(note)
        fh.write("- " + " — ".join(bits) + "\n")
    return path


STOPWORDS = {"and", "the", "for", "with", "our", "its", "per", "all", "any"}


def add_to_library(rec: dict, library: str, vertical_name: str, depicts: str = "") -> str | None:
    """Add a chosen icon to the shared icon library.

    The library's own file (`shared/data/icons/map.yaml`) is the format: a top-level `fallback:` and
    an `icons:` LIST of `{file, depicts, source, license, keywords}` rows, under a long comment
    header that explains the house style. So the row is appended as text at the end of that list
    rather than re-serialized — a `yaml.safe_dump` round-trip would silently delete the header.

    New names only. A file or a row that is already there is reported and left exactly as it is: the
    library is added to, never rewritten, because the deck, the one-pager and the site all read it.
    """
    import yaml
    os.makedirs(library, exist_ok=True)
    name = slugify(rec.get("title") or os.path.splitext(os.path.basename(rec["file"]))[0])
    # The library's house style is white line art on a transparent ground.
    src = rec["file"]
    white = src.replace("-ink.png", "-white.png")
    if src.endswith("-ink.png") and os.path.exists(white):
        src = white
    dst = os.path.join(library, f"{name}.png")
    map_path = os.path.join(library, "map.yaml")

    existing = {}
    if os.path.exists(map_path):
        with open(map_path, encoding="utf-8") as fh:
            existing = yaml.safe_load(fh) or {}
    rows = existing.get("icons") or []
    if not isinstance(rows, list):
        eprint("  the icon library's map is not in the shape this tool writes "
               "(`icons:` should be a list of rows); left untouched.")
        return None
    if os.path.exists(dst) or any((r or {}).get("file") == f"{name}.png" for r in rows):
        eprint(f"  the library already has {name!r}; left as it is (the library is added to, "
               f"never overwritten)")
        return None

    keywords = sorted({w for w in re.split(r"[^a-z0-9]+", (vertical_name or "").lower())
                       if len(w) > 2 and w not in STOPWORDS})
    row = [
        f"  - file: {name}.png\n",
        f"    depicts: {depicts or name.replace('-', ' ')}\n",
        f"    source: {rec.get('source', '-')} — {rec.get('source_url', '-')}\n",
        f"    license: {rec.get('licence_name', '-')}\n",
        f"    keywords: [{', '.join(keywords)}]\n",
    ]

    if os.path.exists(map_path):
        with open(map_path, encoding="utf-8") as fh:
            lines = fh.readlines()
        at = _find_top_key(lines, "icons")
        if at is None:
            lines += ["\nicons:\n"] + row
        else:
            end = _block_bounds(lines, at, 0)
            lines = lines[:end] + row + lines[end:]
    else:
        lines = ["# The shared icon library — which picture stands for which kind of business.\n",
                 "\nfallback: generic.png\n\nicons:\n"] + row

    text = "".join(lines)
    after = yaml.safe_load(text) or {}
    if len(after.get("icons") or []) != len(rows) + 1:
        eprint("  the library's map would not have parsed back correctly; left untouched.")
        return None
    shutil.copy2(src, dst)
    with open(map_path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return dst


# ----------------------------------------------------------------------------------------- run

def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec")
    ap.add_argument("--slot", required=True)
    ap.add_argument("--file", required=True, help="the file the owner chose")
    ap.add_argument("--provenance", default="", help="its .json sidecar (default: beside the file)")
    ap.add_argument("--note", default="", help="one plain line on why this one, for the decisions log")
    ap.add_argument("--add-to-library", action="store_true",
                    help="also add a chosen icon to the shared icon library")
    ap.add_argument("--depicts", default="",
                    help="one short phrase for the library row: what the icon shows")
    ap.add_argument("--library", default=DEFAULT_LIBRARY)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    try:
        kind = slot_kind(args.slot)
    except ValueError as exc:
        eprint(str(exc))
        return EXIT_USAGE
    if not os.path.exists(args.spec):
        eprint(f"no spec at {args.spec}")
        return EXIT_USAGE
    if not os.path.exists(args.file):
        eprint(f"no file at {args.file}")
        return EXIT_USAGE
    if kind == "supplied":
        # No search, no sidecar, no licence lookup. The owner handed us this file from the
        # engagement materials, and what permits the use is the customer's clearance recorded in
        # the pack brief — so that is what goes in the record, in those words.
        rec = provenance_record(
            slot=args.slot, kind=kind, file=args.file,
            title=os.path.splitext(os.path.basename(args.file))[0],
            source=SUPPLIED_SOURCE, licence_name=SUPPLIED_TERMS, terms=SUPPLIED_TERMS,
            note=args.note,
        )
    else:
        try:
            rec = read_sidecar(args.provenance or args.file)
        except FileNotFoundError as exc:
            eprint(str(exc))
            return EXIT_USAGE

        lic = (rec.get("licence") or "").lower()
        allowed = ICON_LICENCES if kind == "icon" else PHOTO_LICENCES
        if lic not in allowed:
            eprint(f"the recorded licence for this file is {lic!r}, which is not one this bundle "
                   f"may use for a {kind}. Allowed: {', '.join(sorted(allowed))}. Nothing was "
                   f"written.")
            return EXIT_LICENCE

    pack = pack_dir(args.spec)
    visuals = os.path.join(pack, "visuals")
    spec = load_spec(args.spec)

    copied = [] if args.dry_run else copy_in(args.file, visuals, args.slot, rec)
    chosen = copied[0] if copied else args.file
    if kind == "supplied" and copied:
        # The owner's file arrives with no sidecar; write one beside the copy so the record
        # travels with the picture like every other file in the pack. It is removed with the copy
        # if the spec edit is then refused.
        write_sidecar(chosen, dict(rec, file=chosen, slot=args.slot))
    if kind == "icon":
        ink = next((p for p in copied if p.endswith("-ink.png")), chosen)
        white = next((p for p in copied if p.endswith("-white.png")), None)
        value = {"file": os.path.relpath(ink, pack), "name": rec.get("title", "-"),
                 "source": rec.get("source", "-"), "licence": rec.get("licence_name", "-")}
        if white:
            value["file_white"] = os.path.relpath(white, pack)
    elif kind == "supplied":
        value = {"file": os.path.relpath(chosen, pack),
                 "source": SUPPLIED_SOURCE,
                 "licence": SUPPLIED_TERMS}
    else:
        value = {"file": os.path.relpath(chosen, pack),
                 "source": rec.get("source", "-"),
                 "creator": rec.get("creator", "-"),
                 "licence": rec.get("licence_name", "-"),
                 "source_url": rec.get("source_url", "-")}

    try:
        key = write_spec(args.spec, args.slot, value, args.dry_run)
    except (ValueError, RuntimeError, KeyError, IndexError, TypeError) as exc:
        # Either all four things happen or none: the copies go back out again.
        eprint(f"the spec was not changed: {exc}")
        for p in copied:
            for f in (p, os.path.splitext(p)[0] + ".json"):
                if os.path.exists(f):
                    os.remove(f)
        return EXIT_USAGE

    rec_for_credits = dict(rec, file=chosen, slot=args.slot)
    credits = decisions = lib = None
    if not args.dry_run:
        credits = append_credits(visuals, rec_for_credits)
        decisions = append_decision(work_folder(args.spec, spec), args.slot, rec_for_credits,
                                    args.note)
        if args.add_to_library and kind == "icon":
            vname = ""
            base, idx = parse_slot(args.slot)
            if base == "vertical":
                try:
                    vname = (spec.get("verticals") or [])[idx].get("name", "")
                except (IndexError, AttributeError):
                    vname = ""
            lib = add_to_library(dict(rec, file=chosen), args.library, vname, args.depicts)

    print(("dry run — nothing written\n" if args.dry_run else "") + f"slot {args.slot} ({kind})")
    for p in copied:
        print(f"  copied  {os.path.relpath(p, pack)}")
    print(f"  spec    {key} ← {value['file']}")
    if credits:
        print(f"  credits {os.path.relpath(credits, pack)}")
    if decisions:
        print(f"  logged  {decisions}")
    if lib:
        print(f"  library {lib}")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
