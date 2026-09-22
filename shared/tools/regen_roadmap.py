#!/usr/bin/env python3
"""Regenerate the versioned roadmap extract under shared/data/.

Outputs (see shared/data/roadmap.README.md):
  roadmap-items.csv      id,block,item,status,l1_pattern,l2_pattern
  roadmap-l2-patterns.csv  l1,l2,definition
  pack-crosswalk.csv     pack_slug,pack_name_current,roadmap_item_id,site_slug,tracker_name,older_names
  pack-tracker.csv       pack,artifact,status,due_date          (only when --tracker resolves)

Sources are read-only. Nothing outside --out is written.

Hard rules enforced here:
  * Every parenthetical customer tag is stripped from the workflow-pattern
    sheet's card columns, and a clearance sweep fails the run if a tag-shaped
    string survives into any output field. The customer names themselves are
    deliberately NOT in this file (see "Customer-tag clearance" below); an
    exact-name gate can be supplied at run time with --deny-list.
  * Item ids are minted from the item NAME, never from a row number, and the
    script REFUSES to overwrite when an id already published in
    roadmap-items.csv would change. It prints the diff and exits 2.

Dependencies: standard library. openpyxl is used when importable, otherwise
the .xlsx is read directly with zipfile + ElementTree.

Usage:
    python3 shared/tools/regen_roadmap.py                 # defaults below
    python3 shared/tools/regen_roadmap.py --check         # dry run, write nothing
    python3 shared/tools/regen_roadmap.py --accept-id-changes   # re-mint ids on purpose
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import os
import re
import sys
import unicodedata
import zipfile
from xml.etree import ElementTree as ET

# --------------------------------------------------------------------------
# Where the sources live.
#
# No machine path is written into this repo (it is a disclosure of one person's
# drive layout, and it is wrong on every other machine). Point the run at the
# practice's pack folder once:
#
#     export ORACLE_PACKS_DIR="<the shared drive>/Projects/Oracle/Packs"
#
# and the three defaults below resolve under it; or pass --roadmap / --mapping /
# --tracker explicitly. With neither, the tool says which one is missing and
# stops — an unset source is an environment problem, never an empty CSV.
# --------------------------------------------------------------------------
PACKS_DIR = os.path.expanduser(os.environ.get("ORACLE_PACKS_DIR", ""))


def _under_packs(*parts: str) -> str:
    return os.path.join(PACKS_DIR, *parts) if PACKS_DIR else ""


DEFAULT_ROADMAP = _under_packs("Use case maps", "AI use case roadmap 2026-09-22.md")
DEFAULT_MAPPING = _under_packs(
    "Use case maps", "AI workflow patterns - AIDP-NVIDIA-OracleAI mapping.xlsx")
DEFAULT_TRACKER = _under_packs("Oracle packages.xlsx")
DEFAULT_OUT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
)

CARD_SHEET = "Card labels v2"
PATTERN_SHEET_HINT = "Patterns v2"          # real tab: "Patterns v2 (red-team 2026-09)"
TRACKER_SHEET = "Packaging activities"

# --------------------------------------------------------------------------
# Customer-tag clearance.
#
# The customer names themselves are NOT written down here. A deny-list of
# customer names is itself a disclosure of who the pipeline customers are, and
# this repo is shared. Two mechanisms replace it:
#
#   1. STRIP — in `Card labels v2` every parenthetical is a customer tag; the
#      sheet uses no other kind of parenthetical in the Card 1-5 columns. So
#      all of them are stripped, by shape, with no names needed. If the sheet
#      ever gains a legitimate parenthetical in a card cell, that card stops
#      matching its roadmap item and the run reports it as unmatched rather
#      than guessing.
#
#   2. SWEEP — every output cell is checked for a residual parenthetical that
#      is proper-noun shaped (all words Capitalised or ALL-CAPS, no comma,
#      <= 3 words) and is not one of the technical terms below. That is the
#      shape a customer tag has and the shape the pattern vocabulary does not.
#
# An exact-name second gate can be supplied at run time with --deny-list
# FILE (one lowercase name per line, from outside the repo, never committed),
# or via the ORACLE_PACK_DENYLIST environment variable.
# --------------------------------------------------------------------------
ALLOWED_PARENTHETICAL_TERMS = {
    # technical vocabulary that is legitimately Capitalised or ALL-CAPS
    "idp", "rfp", "nl to sql", "sql", "erp", "crm", "kyc", "aml", "cctv",
    "ivr", "rca", "soc", "cve", "mlr", "hitl", "oci", "ar", "it", "hr",
    "sla", "sku", "api", "pov", "s/m/l",
}
PROPER_NOUN_PARENTHETICAL = re.compile(r"\(([^()]*)\)")


# --------------------------------------------------------------------------
# The id rule (documented in roadmap.README.md — keep the two in step)
# --------------------------------------------------------------------------
def mint_id(name: str) -> str:
    """Kebab-case slug minted deterministically from an item name.

    1. Unicode NFKD normalise, drop combining marks, keep ASCII.
    2. Lowercase, trim.
    3. " & " (ampersand fenced by whitespace) becomes " and ".
    4. Any remaining "&" and every apostrophe are deleted with no separator,
       so "Q&A" -> "qa" and "customer's" -> "customers".
    5. Every remaining run of non [a-z0-9] collapses to a single "-".
    6. Leading/trailing "-" stripped.
    """
    s = unicodedata.normalize("NFKD", name)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.encode("ascii", "ignore").decode("ascii")
    s = s.lower().strip()
    s = re.sub(r"\s+&\s+", " and ", s)
    s = re.sub(r"[&'’‘]", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def strip_card_tag(label: str) -> str:
    """Drop every parenthetical from a `Card labels v2` cell.

    Used only on the Card 1-5 columns, where every parenthetical is a customer
    tag. Never applied to the L1/L2 columns or to a definition, whose
    parentheticals are vocabulary ("Ambient scribe (meetings, clinical)").
    """
    out = re.sub(r"\s*\([^()]*\)", "", label)
    return re.sub(r"\s{2,}", " ", out).strip()


def _looks_like_a_customer_tag(inner: str) -> bool:
    inner = inner.strip()
    if not inner or "," in inner:
        return False
    if inner.lower() in ALLOWED_PARENTHETICAL_TERMS:
        return False
    words = inner.split()
    if len(words) > 3:
        return False
    return all(w[:1].isupper() for w in words if w[:1].isalpha())


def load_deny_list(path: str | None) -> list[str]:
    """Optional exact-name second gate, supplied from outside the repo."""
    path = path or os.environ.get("ORACLE_PACK_DENYLIST")
    if not path or not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        return [ln.strip().lower() for ln in fh
                if ln.strip() and not ln.startswith("#")]


def clearance_sweep(rows: list[list[str]], where: str,
                    deny: list[str]) -> list[str]:
    """Every violation found in any cell: tag-shaped parenthetical, or an
    exact hit from an externally supplied deny-list."""
    hits = []
    for r_i, row in enumerate(rows):
        for c_i, cell in enumerate(row):
            cell = str(cell)
            for m in PROPER_NOUN_PARENTHETICAL.finditer(cell):
                if _looks_like_a_customer_tag(m.group(1)):
                    hits.append(
                        f"{where} row {r_i} col {c_i}: tag-shaped "
                        f"parenthetical ({m.group(1)}) in {cell!r}"
                    )
            low = cell.lower()
            for name in deny:
                if re.search(r"\b" + re.escape(name) + r"\b", low):
                    hits.append(f"{where} row {r_i} col {c_i}: deny-list hit in {cell!r}")
    return hits


# --------------------------------------------------------------------------
# xlsx reading — openpyxl when available, otherwise raw OOXML
# --------------------------------------------------------------------------
_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
_RNS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


def _col_index(ref: str) -> int:
    letters = re.match(r"([A-Z]+)", ref).group(1)
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n - 1


def _read_sheet_raw(path: str, sheet_hint: str) -> list[list[str]]:
    with zipfile.ZipFile(path) as z:
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        rid2target = {e.get("Id"): e.get("Target") for e in rels}

        target = None
        for sh in wb.find(_NS + "sheets"):
            if sheet_hint.lower() in (sh.get("name") or "").lower():
                target = rid2target[sh.get(_RNS + "id")].lstrip("/")
                break
        if target is None:
            raise SystemExit(f"sheet matching {sheet_hint!r} not found in {path}")
        if not target.startswith("xl/"):
            target = "xl/" + target

        shared: list[str] = []
        if "xl/sharedStrings.xml" in z.namelist():
            sst = ET.fromstring(z.read("xl/sharedStrings.xml"))
            shared = ["".join(t.text or "" for t in si.iter(_NS + "t")) for si in sst]

        root = ET.fromstring(z.read(target))
        rows: list[list[str]] = []
        for row in root.find(_NS + "sheetData"):
            cells: dict[int, str] = {}
            for c in row:
                ctype = c.get("t")
                if ctype == "inlineStr":
                    node = c.find(_NS + "is")
                    val = "".join(t.text or "" for t in node.iter(_NS + "t")) if node is not None else ""
                else:
                    v = c.find(_NS + "v")
                    val = "" if v is None else (v.text or "")
                    if ctype == "s" and val != "":
                        val = shared[int(val)]
                if val != "":
                    cells[_col_index(c.get("r"))] = val
            width = max(cells) + 1 if cells else 0
            rows.append([cells.get(i, "") for i in range(width)])
        return rows


def read_sheet(path: str, sheet_hint: str) -> list[list[str]]:
    try:
        import openpyxl  # noqa: F401
    except ImportError:
        return _read_sheet_raw(path, sheet_hint)
    import openpyxl

    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    name = next(
        (n for n in wb.sheetnames if sheet_hint.lower() in n.lower()), None
    )
    if name is None:
        raise SystemExit(f"sheet matching {sheet_hint!r} not found in {path}")
    ws = wb[name]
    rows = []
    for row in ws.iter_rows(values_only=True):
        rows.append(["" if v is None else str(v) for v in row])
    return rows


# --------------------------------------------------------------------------
# Source readers
# --------------------------------------------------------------------------
ROADMAP_HEADER = ("block", "item", "status")


def _md_cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def read_roadmap(path: str) -> list[dict]:
    """Parse the one `Block | Item | Status` markdown table in the roadmap.

    Anchored on that exact header and stopped by the first non-table line.
    The roadmap markdown also carries narrative summary tables (block counts,
    the unpackaged remainder); shape-matching alone picked their rows up as use
    cases, so the header is the contract. A file with no such header, or with
    two of them, is a source problem and stops the run.
    """
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    starts = [i for i, ln in enumerate(lines)
              if ln.strip().startswith("|")
              and tuple(c.lower() for c in _md_cells(ln)) == ROADMAP_HEADER]
    if not starts:
        raise SystemExit(
            f"no `| Block | Item | Status |` header found in {path} — the "
            "roadmap markdown must carry exactly one such table")
    if len(starts) > 1:
        raise SystemExit(
            f"{len(starts)} `| Block | Item | Status |` tables in {path} "
            f"(lines {', '.join(str(i + 1) for i in starts)}) — expected one")

    items = []
    for ln in lines[starts[0] + 1:]:
        if not ln.strip().startswith("|"):
            break
        cells = _md_cells(ln)
        if len(cells) != 3:
            raise SystemExit(
                f"{path}: {len(cells)} cells in a roadmap row: {ln.strip()!r}")
        block, item, status = cells
        if set(block) <= set("-: "):      # the header separator
            continue
        items.append({"block": block, "item": item, "status": status})
    if not items:
        raise SystemExit(f"no roadmap rows parsed from {path}")
    return items


def read_card_labels(path: str) -> dict[str, tuple[str, str]]:
    """card label (customer tag stripped) -> (l1, l2)."""
    rows = read_sheet(path, CARD_SHEET)
    out: dict[str, tuple[str, str]] = {}
    for row in rows[1:]:
        if len(row) < 3 or not row[0]:
            continue
        l1, l2 = row[0].strip(), row[1].strip()
        for card in row[2:]:
            card = strip_card_tag(card)
            if card:
                out[card.lower()] = (l1, l2)
    return out


def read_l2_definitions(path: str) -> list[tuple[str, str, str]]:
    rows = read_sheet(path, PATTERN_SHEET_HINT)
    out = []
    for row in rows[1:]:
        if len(row) < 3:
            continue
        l1, l2, definition = row[0].strip(), row[1].strip(), row[2].strip()
        if not (l1 and l2 and definition):
            continue
        out.append((l1, l2, definition))
    return out


def read_tracker(path: str) -> list[tuple[str, str, str, str]]:
    """Packaging activities tab -> (pack, artifact, status, due_date). No people."""
    rows = read_sheet(path, TRACKER_SHEET)
    out, current = [], ""
    for row in rows[1:]:
        cells = [(row[i].strip() if i < len(row) else "") for i in range(4)]
        pack, artifact, status, due = cells
        if pack:
            current = pack
        if not artifact:
            continue
        out.append((current, artifact, status, due))
    return out


# --------------------------------------------------------------------------
# The free-text join. Card label -> roadmap item, where they drifted apart.
# Left = card label in `Card labels v2` (customer tag already stripped).
# Right = Item as it reads in the roadmap markdown.
# Every entry is a real, verified rename — do not guess new ones.
# --------------------------------------------------------------------------
CARD_TO_ITEM_ALIASES = {
    "account insight briefings": "Account insights",
    "technician shift scheduling": "Workforce optimization",
    "contract metadata extraction": "Large document extraction & validation",
    "warehouse pick-path optimisation": "Warehouse pick-path optimization",
}

# --------------------------------------------------------------------------
# Pack crosswalk. Curated, not derivable — the join is free text with no ids.
# roadmap_item is the roadmap ITEM NAME; the script resolves it to the minted
# id and fails if it no longer exists on the map.
# older_names: ";"-separated other strings this use case has gone by across
# the estate (tracker, mini-site, card labels, work-split sheet).
# --------------------------------------------------------------------------
CROSSWALK = [
    dict(
        pack_slug="workforce-optimization",
        pack_name_current="Workforce optimization",
        roadmap_item="Workforce optimization",
        site_slug="workforce-optimization",
        tracker_name="Workforce optimization",
        older_names=["Technician shift scheduling", "Workforce shift scheduling",
                     "Workforce Scheduling Optimizer"],
    ),
    dict(
        pack_slug="large-document-extraction",
        pack_name_current="Large docs processing and review",
        roadmap_item="Large document extraction & validation",
        site_slug="large-document-extraction",
        tracker_name="Large document extraction and validation",
        older_names=["Contract metadata extraction", "Intelligent Document Extraction",
                     "Enterprise document processing workflow",
                     "Large Document Extraction and review package"],
    ),
    dict(
        pack_slug="account-insights",
        pack_name_current="Account insights",
        roadmap_item="Account insights",
        site_slug="account-insights",
        tracker_name="AI Signal-Impact Engine",
        older_names=["Account insight briefings", "AI Signal-Impact Engine"],
    ),
    dict(
        pack_slug="",
        pack_name_current="",
        roadmap_item="Complaint evidence assembly",
        site_slug="case-evidence-collection",
        tracker_name="",
        older_names=["Case evidence collection"],
    ),
    dict(
        pack_slug="",
        pack_name_current="",
        roadmap_item="Plan-vs-actual investigation",
        site_slug="plan-vs-actual-investigation",
        tracker_name="",
        older_names=["Plan vs actual investigation"],
    ),
    dict(
        pack_slug="",
        pack_name_current="",
        roadmap_item="Cross-system ERP Q&A",
        site_slug="cross-system-erp-qa",
        tracker_name="",
        older_names=[],
    ),
    dict(
        pack_slug="",
        pack_name_current="",
        roadmap_item="Business metrics Q&A",
        site_slug="business-metrics-qa",
        tracker_name="",
        older_names=[],
    ),
    dict(
        pack_slug="",
        pack_name_current="",
        roadmap_item="Fleet route optimization",
        site_slug="",
        tracker_name="",
        older_names=[],
    ),
    dict(
        pack_slug="",
        pack_name_current="",
        roadmap_item="Visual inspection & classification",
        site_slug="",
        tracker_name="",
        older_names=[],
    ),
]


# --------------------------------------------------------------------------
# Build
# --------------------------------------------------------------------------
def build_items(roadmap_path: str, mapping_path: str) -> tuple[list[list[str]], dict]:
    raw = read_roadmap(roadmap_path)
    cards = read_card_labels(mapping_path)

    # Fold the alias table into the card lookup, keyed on the ROADMAP item name.
    by_item: dict[str, tuple[str, str]] = {}
    for card_lower, pair in cards.items():
        by_item[card_lower] = pair
    for card_lower, item_name in CARD_TO_ITEM_ALIASES.items():
        if card_lower in cards:
            by_item[item_name.lower()] = cards[card_lower]

    rows, seen, stats = [], {}, {"matched": 0, "unmatched": []}
    for rec in raw:
        item = rec["item"]
        ident = mint_id(item)
        if ident in seen and seen[ident] != item:
            raise SystemExit(
                f"id collision: {ident!r} minted from both {seen[ident]!r} and {item!r}"
            )
        seen[ident] = item
        l1, l2 = by_item.get(item.lower(), ("", ""))
        if l1:
            stats["matched"] += 1
        else:
            stats["unmatched"].append(item)
        rows.append([ident, rec["block"], item, rec["status"], l1, l2])
    return rows, stats


def build_crosswalk(item_rows: list[list[str]]) -> list[list[str]]:
    by_name = {r[2].lower(): r[0] for r in item_rows}
    out = []
    for entry in CROSSWALK:
        key = entry["roadmap_item"].lower()
        if key not in by_name:
            raise SystemExit(
                f"crosswalk references {entry['roadmap_item']!r}, which is not on "
                "the roadmap any more — update CROSSWALK in this script"
            )
        out.append([
            entry["pack_slug"],
            entry["pack_name_current"],
            by_name[key],
            entry["site_slug"],
            entry["tracker_name"],
            "; ".join(entry["older_names"]),
        ])
    return out


# --------------------------------------------------------------------------
# id stability gate
# --------------------------------------------------------------------------
def id_diff(existing_csv: str, new_rows: list[list[str]]) -> list[str]:
    """Report every published (item -> id) pair the new run would change."""
    if not os.path.exists(existing_csv):
        return []
    with open(existing_csv, encoding="utf-8", newline="") as fh:
        old = {r["item"]: r["id"] for r in csv.DictReader(fh)}
    problems, renamed = [], set()
    for ident, _block, item, _status, _l1, _l2 in new_rows:
        if item in old and old[item] != ident:
            problems.append(f"  {item!r}: {old[item]} -> {ident}")
            renamed.add(old[item])
    new_items = {r[2] for r in new_rows}
    new_ids = {r[0] for r in new_rows}
    for item, ident in sorted(old.items()):
        if ident not in new_ids and ident not in renamed:
            problems.append(
                f"  {ident}: gone from the map"
                + ("" if item in new_items else f" (item {item!r} no longer listed)")
            )
    return problems


def write_csv(path: str, header: list[str], rows: list[list[str]]) -> None:
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


# --------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--roadmap", default=DEFAULT_ROADMAP,
                    help="the cleaned roadmap markdown (Block | Item | Status); "
                         "defaults under $ORACLE_PACKS_DIR")
    ap.add_argument("--mapping", default=DEFAULT_MAPPING,
                    help="the AI workflow patterns .xlsx; defaults under $ORACLE_PACKS_DIR")
    ap.add_argument("--tracker", default=DEFAULT_TRACKER,
                    help="the packaging tracker .xlsx; skipped with a warning if missing")
    ap.add_argument("--out", default=DEFAULT_OUT, help="output directory")
    ap.add_argument("--deny-list", default=None,
                    help="optional file of exact customer names (one per line, "
                         "lowercase) for a second clearance gate. Keep it OUTSIDE "
                         "this repo; never commit it. Env: ORACLE_PACK_DENYLIST")
    ap.add_argument("--check", action="store_true",
                    help="parse and validate, write nothing")
    ap.add_argument("--accept-id-changes", action="store_true",
                    help="allow a published id to change (say why in the README)")
    args = ap.parse_args()

    for p in (args.roadmap, args.mapping):
        if not p:
            print("ERROR: no source path. Set ORACLE_PACKS_DIR to the practice's "
                  "Projects/Oracle/Packs folder, or pass --roadmap and --mapping.",
                  file=sys.stderr)
            return 1
        if not os.path.exists(p):
            print(f"ERROR: source not found: {p}", file=sys.stderr)
            return 1

    item_rows, stats = build_items(args.roadmap, args.mapping)
    l2_rows = [list(t) for t in read_l2_definitions(args.mapping)]
    cross_rows = build_crosswalk(item_rows)

    tracker_rows = None
    if os.path.exists(args.tracker):
        tracker_rows = [list(t) for t in read_tracker(args.tracker)]
    else:
        print(f"WARNING: tracker not found, leaving pack-tracker.csv alone: "
              f"{args.tracker}", file=sys.stderr)

    # --- clearance sweep -------------------------------------------------
    deny = load_deny_list(args.deny_list)
    violations = (
        clearance_sweep(item_rows, "roadmap-items.csv", deny)
        + clearance_sweep(l2_rows, "roadmap-l2-patterns.csv", deny)
        + clearance_sweep(cross_rows, "pack-crosswalk.csv", deny)
        + (clearance_sweep(tracker_rows, "pack-tracker.csv", deny)
           if tracker_rows else [])
    )
    if violations:
        print("ERROR: customer name reached an output field:", file=sys.stderr)
        for v in violations:
            print("  " + v, file=sys.stderr)
        return 3

    # --- integrity -------------------------------------------------------
    ids = [r[0] for r in item_rows]
    if len(ids) != len(set(ids)):
        print("ERROR: duplicate ids", file=sys.stderr)
        return 3
    if any(not i for i in ids):
        print("ERROR: empty id minted", file=sys.stderr)
        return 3

    # --- id stability ----------------------------------------------------
    items_csv = os.path.join(args.out, "roadmap-items.csv")
    problems = id_diff(items_csv, item_rows)
    if problems and not args.accept_id_changes:
        print("REFUSING TO WRITE: published ids would change.\n"
              "Downstream artifacts key on these ids. Fix the source name, or "
              "re-run with --accept-id-changes and record the change in "
              "roadmap.README.md.\n", file=sys.stderr)
        for p in problems:
            print(p, file=sys.stderr)
        return 2

    print(f"roadmap items : {len(item_rows)}  "
          f"(L1/L2 matched {stats['matched']}, unmatched {len(stats['unmatched'])})")
    for u in stats["unmatched"]:
        print(f"  no pattern row for item: {u!r}")
    print(f"L2 patterns   : {len(l2_rows)}")
    print(f"crosswalk     : {len(cross_rows)}")
    print(f"tracker       : {len(tracker_rows) if tracker_rows is not None else 'skipped'}")

    if args.check:
        print("--check: nothing written")
        return 0

    os.makedirs(args.out, exist_ok=True)
    write_csv(items_csv, ["id", "block", "item", "status", "l1_pattern", "l2_pattern"],
              item_rows)
    write_csv(os.path.join(args.out, "roadmap-l2-patterns.csv"),
              ["l1", "l2", "definition"], l2_rows)
    write_csv(os.path.join(args.out, "pack-crosswalk.csv"),
              ["pack_slug", "pack_name_current", "roadmap_item_id", "site_slug",
               "tracker_name", "older_names"], cross_rows)
    if tracker_rows is not None:
        write_csv(os.path.join(args.out, "pack-tracker.csv"),
                  ["pack", "artifact", "status", "due_date"], tracker_rows)

    print(f"\nwritten to {args.out}  (generated {_dt.date.today().isoformat()})")
    print("Update the `generated:` date and the source mtimes in "
          "roadmap.README.md to match.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
