#!/usr/bin/env python3
"""Check that the three artifacts draw the SAME architecture picture.

    python3 shared/tools/check_diagram.py packs/<slug>/pack-spec.md \
            --deck out/deck.pptx --one-pager out/one-pager.html \
            --site <site>/site/data/diagrams.js --slug <slug>

The model (shared/tools/build_diagram.py, built from the spec: `--channel` for the deck
and the one-pager, the site's name variant for the site) is the picture; the deck slide,
the one-pager's strip and the mini-site's figure are three levels of detail on it. This
asserts they still are: every node the artifact should carry appears exactly, letter
for letter, and no artifact draws a box the model has never heard of. A model file from
`build_diagram.py --out` is read as it is, for every artifact.

What each artifact must carry
    deck        every node name (app, engine, every source, every destination) and
                every edge label — the deck is the full picture
    one-pager   the same systems and the same edge labels as the deck — every source,
                every destination, the app and the engine. Only the descriptive lines
                are shorter: a system that only receives has its own box, one that the
                pack also reads is a write-back and keeps the source box
    site        every system the printed artifacts name — the app, the engine, the
                first two sources (the flow figure draws two) and every destination,
                which ride the target box's second line — plus the human gate, which
                is what the target box itself is

Findings print as `artifact: message`, then one summary line.

Exit codes
    0   every artifact draws the model
    1   at least one artifact has drifted from it
    2   usage or dependency error (unreadable spec, model or artifact, no python-pptx)

Rules: shared/references/architecture-diagram.md.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

PROG = "check_diagram"


# ---------------------------------------------------------------------------
# what the model says each artifact must carry
# ---------------------------------------------------------------------------

def model_names(model: dict) -> set:
    names = {model["app"]["name"], model["engine"]["name"]}
    names |= {s["name"] for s in model.get("sources") or []}
    names |= {d["name"] for d in model.get("destinations") or []}
    if model.get("gate"):
        names.add(model["gate"]["name"])
    return {n for n in names if n}


# ---------------------------------------------------------------------------
# reading the artifacts
# ---------------------------------------------------------------------------

def read_deck(path: Path) -> dict:
    """{boxes: [...], texts: [...]} for the architecture slide, found by its title."""
    try:
        from pptx import Presentation
    except ImportError:
        raise Dependency("python-pptx is required to read a deck — "
                         "pip install -r plugins/oracle-packs/requirements.txt")
    prs = Presentation(str(path))
    for index, slide in enumerate(prs.slides, start=1):
        titles = [shape.text_frame.text.strip() for shape in slide.shapes
                  if shape.has_text_frame and shape.text_frame.text.strip()]
        if not any(t.upper().startswith("ARCHITECTURE") for t in titles):
            continue
        boxes, texts = [], []

        def walk(shapes):
            for shape in shapes:
                if shape.shape_type == 6:                     # a group: look inside
                    walk(shape.shapes)
                    continue
                if not shape.has_text_frame:
                    continue
                paragraphs = [p.text.strip() for p in shape.text_frame.paragraphs
                              if p.text.strip()]
                if not paragraphs:
                    continue
                texts.extend(paragraphs)
                if shape.shape_type == 1:                     # AUTO_SHAPE: a drawn box
                    boxes.append(paragraphs[0])

        walk(slide.shapes)
        return {"slide": index, "boxes": boxes, "texts": texts}
    raise Dependency(f"{path.name} has no slide titled ARCHITECTURE")


def read_one_pager(path: Path) -> dict:
    """The `.arch` strip: its box names, its notes and its two pipe labels."""
    page = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r'<div class="arch">(.*?)\n\s*</div>\s*\n\s*\{\{/ data_flow \}\}',
                      page, re.S) or re.search(r'<div class="arch">(.*)', page, re.S)
    if not match:
        raise Dependency(f"{path.name} has no architecture strip (`<div class=\"arch\">`)")
    strip = match.group(1)
    # The strip ends where the pitch column does; cut at the sell card so the scan
    # never reaches the rest of the page.
    strip = re.split(r'<aside class="sell-card"', strip)[0]

    def texts(pattern):
        return [clean_html(m) for m in re.findall(pattern, strip, re.S)]

    return {"boxes": texts(r"<b>(.*?)</b>"),
            "labels": texts(r'<div class="pipe-lbl">(.*?)</div>'),
            "texts": texts(r">([^<>]+)<")}


def read_site(path: Path, slug: str) -> dict:
    """The slug's `SITE_DIAGRAMS` entry: its node titles, subs, label and note."""
    source = path.read_text(encoding="utf-8", errors="replace")
    start = source.find(f'"{slug}"')
    if start < 0:
        start = source.find(f"'{slug}'")
    if start < 0:
        raise Dependency(f"{path.name} has no figure for \"{slug}\"")
    brace = source.find("{", start)
    depth, end = 0, None
    for i in range(brace, len(source)):
        if source[i] == "{":
            depth += 1
        elif source[i] == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    entry = source[brace:end or len(source)]
    titles = [" ".join(json.loads(a)) for a in re.findall(r"title:\s*(\[[^\]]*\])", entry)]
    subs = [" ".join(json.loads(a)) for a in re.findall(r"sub:\s*(\[[^\]]*\])", entry)]
    labels = [" ".join(json.loads(a)) for a in re.findall(r"label:\s*(\[[^\]]*\])", entry)]
    note = re.search(r'(?:note|loop):\s*"((?:[^"\\]|\\.)*)"', entry)
    return {"boxes": titles, "texts": titles + subs + labels +
            ([note.group(1)] if note else [])}


class Dependency(RuntimeError):
    """Something the check needs is missing or unreadable — a usage error, not drift."""


def clean_html(fragment: str) -> str:
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", fragment))).strip()


# ---------------------------------------------------------------------------
# the checks
# ---------------------------------------------------------------------------

def check(artifact: str, found: dict, must_carry, must_label, names: set,
          findings: list) -> None:
    blob = "\n".join(found["texts"])
    for name in sorted(must_carry):
        if name not in blob:
            findings.append(f"{artifact}: the model's \"{name}\" is not on the picture "
                            f"(exactly, as the model spells it)")
    for label in sorted(must_label):
        if label and label not in blob:
            findings.append(f"{artifact}: the arrow label \"{label}\" is missing — "
                            f"an arrow that does not say what it carries")
    for box in found["boxes"]:
        if box not in names:
            findings.append(f"{artifact}: a box says \"{box}\", which is nothing in the "
                            f"model — the picture was edited by hand, or the model is stale")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog=PROG, description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("model", help="packs/<slug>/pack-spec.md (or a model file from build_diagram.py --out)")
    ap.add_argument("--channel", default="partner_print", choices=("partner_print", "internal"),
                    help="the cut the deck and the one-pager were built for (default: partner_print)")
    ap.add_argument("--deck", type=Path, default=None, help="the sales deck (.pptx)")
    ap.add_argument("--one-pager", type=Path, default=None, help="the one-pager (.html)")
    ap.add_argument("--site", type=Path, default=None, help="the site's data/diagrams.js")
    ap.add_argument("--slug", default=None, help="the site's product slug (default: the model's)")
    args = ap.parse_args(argv)

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import build_diagram  # the one model builder, beside this file
    try:
        model = build_diagram.load_model(args.model, channel=args.channel)
        site_model = build_diagram.load_model(args.model, channel="site") if args.site else model
    except build_diagram.DiagramError as err:
        sys.stderr.write(f"{PROG}: the architecture picture cannot be drawn from "
                         f"{args.model}: {err}\n")
        return 2
    except Exception as err:            # unreadable file, or a spec that does not parse
        sys.stderr.write(f"{PROG}: cannot read {args.model}: {err}\n")
        return 2
    if not model.get("app") or not model.get("engine"):
        sys.stderr.write(f"{PROG}: {args.model} is not an architecture model "
                         f"(no app, no engine)\n")
        return 2
    if not (args.deck or args.one_pager or args.site):
        sys.stderr.write(f"{PROG}: name at least one artifact to check "
                         f"(--deck / --one-pager / --site)\n")
        return 2

    names = model_names(model)
    sources = model.get("sources") or []
    dests = model.get("destinations") or []
    findings, checked = [], []

    try:
        if args.deck:
            found = read_deck(args.deck)
            check("deck", found,
                  {model["app"]["name"], model["engine"]["name"]}
                  | {s["name"] for s in sources} | {d["name"] for d in dests},
                  [s["data"] for s in sources] + [d["data"] for d in dests],
                  names, findings)
            checked.append(f"deck (slide {found['slide']})")

        if args.one_pager:
            found = read_one_pager(args.one_pager)
            check("one-pager", found,
                  {model["app"]["name"], model["engine"]["name"]}
                  | {s["name"] for s in sources} | {d["name"] for d in dests},
                  [s["data"] for s in sources] + [d["data"] for d in dests],
                  names, findings)
            checked.append("one-pager")

        if args.site:
            slug = args.slug or site_model.get("slug") or ""
            found = read_site(args.site, slug)
            site_sources = site_model.get("sources") or []
            must = {site_model["app"]["name"], site_model["engine"]["name"]} | \
                   {s["name"] for s in site_sources[:2]} | \
                   {d["name"] for d in site_model.get("destinations") or []}
            if site_model.get("gate"):
                must.add(site_model["gate"]["name"])
            check("site", found, {m for m in must if m}, [], model_names(site_model), findings)
            checked.append(f"site ({slug})")
    except Dependency as err:
        sys.stderr.write(f"{PROG}: {err}\n")
        return 2

    for finding in findings:
        print(finding)
    where = ", ".join(checked)
    if findings:
        print(f"{PROG}: {len(findings)} difference(s) across {where} — the artifacts no "
              f"longer draw one picture. Rebuild from {args.model}.")
        return 1
    print(f"{PROG}: {where} all draw the model in {args.model}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
