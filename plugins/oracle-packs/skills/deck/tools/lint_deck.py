#!/usr/bin/env python3
"""Check a built sales deck against the reference deck's shape.

    lint_deck.py <deck.pptx> [--spec <pack-spec.yaml>] [--channel partner_print]
                 [--header "<running header>"] [--geometry <reference-geometry.json>]

Mechanical checks only — the things that drift silently between builds and that
nobody catches by looking at one slide:

  1  ten slides
  2  the running header on slides 2-10
  3  no tier line on the cover
  4  only the brand faces
  5  corners no rounder than the reference's, slide by slide
  6  an icon, not a number, on every industry card
  7  the architecture slide names the pack, the engine's products and a
     destination, and draws one arrow per data source
  8  package-table type at or above the floor

Exit 0 clean · 1 something failed · 2 the deck or the arguments cannot be read.
It never opens the reference deck: the measurements live in
references/reference-geometry.json.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
for _cand in (_HERE, _HERE.parents[1] / "deck" / "tools"):
    if (_cand / "deckkit.py").exists():
        sys.path.insert(0, str(_cand))
        break

GEOMETRY_DEFAULT = _HERE.parent / "references" / "reference-geometry.json"

BRAND_FACES = {"azurio", "replica ll tt", "apple symbols", "segoe ui symbol"}
ROUND_PRSTS = {"roundRect", "round1Rect", "round2SameRect", "round2DiagRect",
               "snipRoundRect"}
ARROW_PRSTS = {"rightArrow", "leftArrow", "upArrow", "downArrow",
               "leftRightArrow", "bentArrow", "straightConnector1",
               "bentConnector3", "curvedConnector3"}

COVER, VERTICALS, ARCHITECTURE = 1, 3, 8
TABLE_FLOOR = {9: 11.0, 10: 10.5}


# ---------------------------------------------------------------------------
# reading the deck
# ---------------------------------------------------------------------------

def walk(shapes):
    for sp in shapes:
        yield sp
        if sp.__class__.__name__ == "GroupShape":
            yield from walk(sp.shapes)


def prst_of(shape):
    from pptx.oxml.ns import qn
    for pg in shape._element.iter(qn("a:prstGeom")):
        return pg.get("prst")
    return None


def shape_text(shape) -> str:
    if not shape.has_text_frame:
        return ""
    return shape.text_frame.text or ""


def header_placeholder_text(slide) -> str:
    """Whatever the running-header placeholder (idx 34) holds on this slide."""
    for ph in slide.placeholders:
        if ph.placeholder_format.idx == 34:
            return (ph.text_frame.text or "").strip()
    return ""


def typefaces(shape):
    """Every explicitly named face under this shape (a run naming none is fine)."""
    from pptx.oxml.ns import qn
    out = set()
    for tag in ("a:latin", "a:ea", "a:cs", "a:sym"):
        for el in shape._element.iter(qn(tag)):
            face = (el.get("typeface") or "").strip()
            if face:
                out.add(face)
    return out


def table_sizes(shape):
    """[(text, pt)] for every run in a table that names its size."""
    out = []
    for row in shape.table.rows:
        for cell in row.cells:
            for p in cell.text_frame.paragraphs:
                for r in p.runs:
                    if r.font.size is not None:
                        out.append((cell.text.strip(), r.font.size.pt))
    return out


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip().lower()


# ---------------------------------------------------------------------------
# what the deck is supposed to say, from the pack brief
# ---------------------------------------------------------------------------

def expectations(spec_path, channel, header_arg):
    """Everything the checks compare against. Missing spec -> only what is known."""
    exp = {"header": header_arg, "name": None, "tier_line": None, "verticals": 0,
           "inputs": 0, "outputs": [], "engine_products": [], "have_spec": False}
    if not spec_path:
        return exp
    from deckkit import Spec, product_name
    spec = Spec.load(spec_path, channel=channel)
    exp["have_spec"] = True
    exp["name"] = spec.name()
    tiers = [str(t.get("name", "")) for t in (spec.get("packages.tiers") or [])]
    exp["tier_line"] = " · ".join(t for t in tiers if t)
    if not exp["header"]:
        tpl = spec.get("deck.running_header") or "Oracle AI & Data Solutions — {name}"
        exp["header"] = tpl.format(name=spec.name())
    exp["verticals"] = min(len(spec.get("verticals") or []), 4)
    exp["inputs"] = min(len(spec.get("architecture.inputs") or []), 3)
    for entry in (spec.get("architecture.outputs") or []):
        if isinstance(entry, dict):
            sysname = str(entry.get("system") or entry.get("name") or "").strip()
        else:
            sysname = str(entry or "").split(" — ")[0].strip()
        if sysname and sysname not in exp["outputs"]:
            exp["outputs"].append(sysname)
    for layer in (spec.get("architecture.stack") or []):
        if "engine" not in str(layer.get("layer", "")).lower():
            continue
        raw = layer.get("catalog_ids") or layer.get("catalog_id") or []
        if isinstance(raw, (str, bytes)):
            raw = [raw]
        for cid in raw:
            nm = product_name(str(cid)).strip()
            if nm:
                exp["engine_products"].append(nm)
    return exp


# ---------------------------------------------------------------------------
# the checks
# ---------------------------------------------------------------------------

def run_checks(deck_path, exp, geometry):
    from pptx import Presentation
    prs = Presentation(str(deck_path))
    slides = list(prs.slides)
    fail, note = [], []

    # 1 — ten slides
    if len(slides) != 10:
        fail.append(f"the deck has {len(slides)} slides; the anatomy is ten")

    shapes = {i: list(walk(s.shapes)) for i, s in enumerate(slides, 1)}

    # 2 — the running header on every slide but the cover
    if exp["header"]:
        want = norm(exp["header"])
        for i in range(2, len(slides) + 1):
            texts = {norm(shape_text(sp)) for sp in shapes[i]}
            if want in texts:
                continue
            got = header_placeholder_text(slides[i - 1])
            fail.append(f"slide {i}: the running header should read "
                        f"\"{exp['header']}\"; it reads "
                        + (f"\"{got}\"" if got else "nothing"))
    else:
        note.append("no running header to compare against — pass --header or --spec")

    # 3 — no tier line on the cover
    if exp["tier_line"]:
        want = norm(exp["tier_line"])
        for sp in shapes.get(COVER, []):
            if norm(shape_text(sp)) == want:
                fail.append(f"the cover carries the three package names as a line "
                            f"(\"{exp['tier_line']}\"); a cover has no tier line")
                break

    # 4 — brand faces only
    seen = {}
    for i, sps in shapes.items():
        for sp in sps:
            for face in typefaces(sp):
                if face.startswith("+"):        # a theme reference, always fine
                    continue
                if face.lower() not in BRAND_FACES:
                    seen.setdefault(face, set()).add(i)
    for face, on in sorted(seen.items()):
        fail.append(f"the face \"{face}\" is used on slide(s) "
                    f"{', '.join(str(n) for n in sorted(on))}; the deck uses "
                    f"Azurio, Replica LL TT and the symbol face only")

    # 5 — corners no rounder than the reference
    allow = {int(k): v for k, v in (geometry.get("deck_slides") or {}).items()
             if k.isdigit()}
    for i, sps in shapes.items():
        rounded = sum(1 for sp in sps if prst_of(sp) in ROUND_PRSTS)
        cap = allow.get(i, {}).get("max_rounded")
        if cap is None:
            continue
        if rounded > cap:
            role = allow[i].get("role", "")
            fail.append(f"slide {i} ({role}): {rounded} rounded shapes, more than the "
                        f"{cap} the reference deck has there — cards, panels and "
                        f"diagram boxes are square")

    # 6 — an icon, not a number, on every industry card
    verticals = shapes.get(VERTICALS, [])
    pics = sum(1 for sp in verticals
               if sp.shape_type is not None and "PICTURE" in str(sp.shape_type))
    if exp["have_spec"]:
        if pics < exp["verticals"]:
            fail.append(f"slide {VERTICALS}: {pics} icons for {exp['verticals']} "
                        f"industries — every card carries a picture")
    elif pics == 0:
        fail.append(f"slide {VERTICALS}: no icons at all on the industries slide")
    for sp in verticals:
        text = shape_text(sp).strip()
        if text and re.fullmatch(r"\d{1,2}", text):
            fail.append(f"slide {VERTICALS}: a card shows the number \"{text}\" "
                        f"where its industry's icon belongs")

    # 7 — the architecture slide names things and draws the flows
    arch = shapes.get(ARCHITECTURE, [])
    texts = [shape_text(sp) for sp in arch]
    blob = norm(" || ".join(texts))
    if exp["name"] and norm(exp["name"]) not in blob:
        fail.append(f"slide {ARCHITECTURE}: no box names the pack "
                    f"(\"{exp['name']}\")")
    if exp["engine_products"]:
        if not any(norm(p) in blob for p in exp["engine_products"]):
            fail.append(f"slide {ARCHITECTURE}: the engine box names no product — "
                        f"it should name "
                        f"{' or '.join(exp['engine_products'])}")
    elif exp["have_spec"]:
        note.append(f"slide {ARCHITECTURE}: the pack brief names no product for the "
                    f"engine layer, so there is nothing to check it against")
    if exp["outputs"]:
        joined = norm(" · ".join(exp["outputs"]))
        if not any(norm(t) == joined for t in texts):
            fail.append(f"slide {ARCHITECTURE}: no box says where the result goes "
                        f"(\"{' · '.join(exp['outputs'])}\")")
    elif exp["have_spec"]:
        note.append(f"slide {ARCHITECTURE}: the pack brief names no destination "
                    f"system, so the box on the right cannot be checked")
    arrows = sum(1 for sp in arch if prst_of(sp) in ARROW_PRSTS)
    if exp["have_spec"] and arrows < exp["inputs"]:
        fail.append(f"slide {ARCHITECTURE}: {arrows} arrows for {exp['inputs']} data "
                    f"sources — every source has its own labelled arrow in")

    # 8 — package-table type at or above the floor
    for i, floor in TABLE_FLOOR.items():
        for sp in shapes.get(i, []):
            if not getattr(sp, "has_table", False):
                continue
            for text, pt in table_sizes(sp):
                if pt < floor - 1e-6:
                    fail.append(f"slide {i}: a cell is set at {pt:g} pt, below the "
                                f"{floor:g} pt floor for this table "
                                f"(\"{text[:48]}\") — shorten the wording instead")
                    break
    return fail, note


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Check a built sales deck against the reference deck's shape.")
    ap.add_argument("deck", help="the built .pptx")
    ap.add_argument("--spec", help="the pack spec the deck was built from")
    ap.add_argument("--channel", default="partner_print",
                    choices=["partner_print", "internal"])
    ap.add_argument("--header", help="the running header to expect on slides 2-10")
    ap.add_argument("--geometry", default=str(GEOMETRY_DEFAULT),
                    help="the measured reference geometry (JSON)")
    args = ap.parse_args(argv)

    deck = Path(args.deck)
    if not deck.is_file():
        print(f"lint_deck: no such deck: {deck}", file=sys.stderr)
        return 2
    try:
        geometry = json.loads(Path(args.geometry).read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"lint_deck: cannot read the reference geometry "
              f"({args.geometry}): {exc}", file=sys.stderr)
        return 2
    try:
        exp = expectations(args.spec, args.channel, args.header)
    except Exception as exc:
        print(f"lint_deck: cannot read the pack spec ({args.spec}): {exc}",
              file=sys.stderr)
        return 2
    try:
        fail, note = run_checks(deck, exp, geometry)
    except Exception as exc:
        print(f"lint_deck: cannot read the deck: {exc}", file=sys.stderr)
        return 2

    for n in note:
        print(f"  note: {n}")
    if fail:
        print(f"{len(fail)} problem(s) in {deck.name}:")
        for f in fail:
            print(f"  - {f}")
        return 1
    print(f"{deck.name}: clean — ten slides, the running header, brand faces, "
          f"square corners, industry icons, the architecture names and flows, "
          f"table type at or above the floor.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
