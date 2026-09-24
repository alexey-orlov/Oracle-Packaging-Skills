#!/usr/bin/env python3
"""Check a built sales deck against the reference deck's shape.

    lint_deck.py <deck.pptx> [--spec <pack-spec.md>] [--channel partner_print]
                 [--header "<running header>"] [--geometry <reference-geometry.json>]
    lint_deck.py <deck.pptx> --reference

Mechanical checks only — the things that drift silently between builds and that
nobody catches by looking at one slide:

  1  ten slides
  2  the running header on slides 2-10
  3  no tier line on the cover
  4  the cover carries the family's hero: the reference's own title layout, and a
     picture on it or on the slide
  5  only the faces the reference uses
  6  corners: no rounded card, and no more pills than the slide type allows
  7  an icon, not a number, on every industry card, and no more pictures than the
     reference's own slide has
  8  the proof slide is the delivered case in the reference's composition: its
     four quadrant labels, three stat tiles that are never empty, and the
     customer's logo exactly where clearance and a logo file both say so
  9  the architecture slide names the pack, the engine's products and where every
     result goes, and draws one arrow per data source
 10  package-table type at or above the reference's own floor
 11  the technology-stack ladder: rows of one width, nothing sticking out of a
     row or flush with its edge

Every budget is measured from the exemplar deck itself and lives in
references/reference-geometry.json; this tool never opens the exemplar.

`--reference` lints the exemplar deck itself: it skips the checks that compare a
deck against a pack brief and would fail the reference by construction — the
running header (the reference carries the old "OCI AI Accelerators" lockup) and
the cover's tier line (the reference has one; the owner asked for none) — plus
the architecture's naming and flow rules and the proof slide's logo clearance,
which are about a pack brief, not about geometry. The proof slide's labels and
stat tiles are checked in reference mode too; the exemplar passes them by
construction, as does the cover-hero check. It is the regression test that the
budgets are still the reference's own.

Exit 0 clean (warnings do not change the exit code) · 1 something failed · 2 the
deck or the arguments cannot be read.
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

ROUND_PRSTS = {"roundRect", "round1Rect", "round2SameRect", "round2DiagRect",
               "snipRoundRect"}
ROUNDRECT_DEFAULT_ADJ = 16667          # what PowerPoint uses when no a:gd is given
ARROW_PRSTS = {"rightArrow", "leftArrow", "upArrow", "downArrow",
               "leftRightArrow", "bentArrow", "straightConnector1",
               "bentConnector3", "curvedConnector3"}

COVER, VERTICALS, PROOF, ARCHITECTURE = 1, 3, 5, 8
_WEIGHTS = ("thin", "extralight", "ultralight", "light", "book", "regular", "roman",
            "medium", "semibold", "demibold", "bold", "extrabold", "black", "heavy",
            "italic", "oblique")


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


def corner_adj(shape) -> int | None:
    """The shape's corner adjustment, or None when it has no rounded preset."""
    from pptx.oxml.ns import qn
    for pg in shape._element.iter(qn("a:prstGeom")):
        if pg.get("prst") not in ROUND_PRSTS:
            return None
        vals = []
        for gd in pg.iter(qn("a:gd")):
            fmla = gd.get("fmla") or ""
            if fmla.startswith("val "):
                try:
                    vals.append(int(fmla[4:]))
                except ValueError:
                    pass
        return max(vals) if vals else ROUNDRECT_DEFAULT_ADJ
    return None


def height_in(shape) -> float:
    return (shape.height or 0) / 914400.0


def at_in(shape) -> tuple[float, float]:
    """The shape's top-left corner, in inches."""
    return (shape.left or 0) / 914400.0, (shape.top or 0) / 914400.0


def shape_at(shapes, spot, tol: float):
    """The shape whose top-left corner is nearest `spot` (a {x, y} in inches), or None when
    nothing sits within `tol` of it. The builder fills the reference's own shapes and never
    moves them, so a slot is found by where the reference put it."""
    want_x, want_y = float(spot.get("x", 0)), float(spot.get("y", 0))
    best, best_d = None, None
    for sp in shapes:
        x, y = at_in(sp)
        if abs(x - want_x) > tol or abs(y - want_y) > tol:
            continue
        d = abs(x - want_x) + abs(y - want_y)
        if best_d is None or d < best_d:
            best, best_d = sp, d
    return best


def is_picture(shape) -> bool:
    return shape.shape_type is not None and "PICTURE" in str(shape.shape_type)


def width_in(shape) -> float:
    return (shape.width or 0) / 914400.0


def top_in(shape) -> float:
    return (shape.top or 0) / 914400.0


def left_in(shape) -> float:
    return (shape.left or 0) / 914400.0


def ladder_rows(slide_shapes) -> list:
    """The technology-stack slide's row bands: three or more wide, plain rectangles."""
    rows = [sp for sp in slide_shapes
            if getattr(sp, "shape_type", None) == 1 and not getattr(sp, "has_table", False)
            and width_in(sp) >= 9.0 and height_in(sp) >= 0.5]
    return rows if len(rows) >= 3 else []


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


def face_key(face: str) -> str:
    """'ReplicaLLTT-Regular', 'Replica LL TT' and 'replica ll tt' are one face."""
    key = re.sub(r"[^a-z0-9]", "", (face or "").lower())
    for weight in _WEIGHTS:
        if key.endswith(weight) and len(key) > len(weight):
            key = key[: -len(weight)]
            break
    return key


def mentions(text: str, name: str) -> bool:
    """Does `text` name this system? Whole words, so 'BI' is not found in 'ambient'."""
    if not name:
        return False
    return re.search(r"(?<![a-z0-9])" + re.escape(norm(name)) + r"(?![a-z0-9])",
                     norm(text)) is not None


# ---------------------------------------------------------------------------
# what the deck is supposed to say, from the pack brief
# ---------------------------------------------------------------------------

def expectations(spec_path, channel, header_arg):
    """Everything the checks compare against. Missing spec -> only what is known."""
    exp = {"header": header_arg, "name": None, "tier_line": None, "verticals": 0,
           "inputs": 0, "outputs": [], "engine_products": [], "have_spec": False,
           "channel": channel, "name_allowed": False, "customer_logo": ""}
    if not spec_path:
        return exp
    from deckkit import Spec, product_name
    spec = Spec.load(spec_path, channel=channel)
    exp["have_spec"] = True
    exp["name"] = spec.name()
    exp["name_allowed"] = bool(spec.customer_name_allowed())
    logo = (spec.get("deck.images") or {}).get("customer_logo")
    if isinstance(logo, dict):
        logo = logo.get("file")
    exp["customer_logo"] = str(logo or "").strip()
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

def run_checks(deck_path, exp, geometry, reference: bool = False):
    from pptx import Presentation
    prs = Presentation(str(deck_path))
    slides = list(prs.slides)
    fail, note, warn = [], [], []

    budgets = {int(k): v for k, v in (geometry.get("deck_slides") or {}).items()
               if k.isdigit()}
    if reference:
        # The exemplar's own slide order is not the anatomy's (its slide 8 is the
        # duplicate table the anatomy drops), so hold it to its own measurements.
        budgets = {int(k): {"role": v.get("role", ""), "exemplar_slide": int(k),
                            "ref_rounded": v.get("rounded", 0),
                            "max_rounded": v.get("rounded", 0),
                            "ref_pictures": v.get("pictures", 0),
                            "max_pictures": v.get("pictures", 0),
                            "table_floor_pt": v.get("table_min_pt")}
                   for k, v in (geometry.get("reference_slides") or {}).items()
                   if k.isdigit()}
    corners = geometry.get("corner_radius") or {}
    pill_min = int(corners.get("pill_adj_min", 20000))
    pill_max_h = float(corners.get("pill_max_h_in", 0.55))
    allowed_faces = {face_key(f) for f in
                     ((geometry.get("fonts") or {}).get("allowed") or [])}
    face_names = ", ".join((geometry.get("fonts") or {}).get("allowed") or [])

    # 1 — ten slides
    if len(slides) != 10:
        fail.append(f"the deck has {len(slides)} slides; the anatomy is ten")

    shapes = {i: list(walk(s.shapes)) for i, s in enumerate(slides, 1)}

    # 2 — the running header on every slide but the cover
    if reference:
        note.append("reference mode: the running header is not checked — the "
                    "exemplar carries the old lockup the rewrite replaced")
    elif exp["header"]:
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
    if reference:
        note.append("reference mode: the cover's tier line is not checked — the "
                    "exemplar has one, and the rewrite drops it")
    elif exp["tier_line"]:
        want = norm(exp["tier_line"])
        for sp in shapes.get(COVER, []):
            if norm(shape_text(sp)) == want:
                fail.append(f"the cover carries the three package names as a line "
                            f"(\"{exp['tier_line']}\"); a cover has no tier line")
                break

    # 4 — the cover carries the family's hero
    #
    # The owner's rule (2026-09-23): a cover is the family's photo cover, not a
    # black rectangle with type on it. The hero lives on the reference's own title
    # layout, so a deck that keeps that layout inherits it; a deck that sets
    # `deck.images.cover` swaps it in place on the same layout. Either way a
    # picture reaches the cover — and an ink-only cover means the deck was redrawn
    # on a base with no photo layout, which is an unfinished state, never a build
    # anyone delivers. Checked in reference mode too; the exemplar passes it by
    # construction.
    cover_cfg = geometry.get("cover") or {}
    want_layout = str(cover_cfg.get("layout") or "").strip()
    remedy = ("an ink-only cover is an unfinished state; build with the exemplar "
              "builder (tools/build_deck_v2.py) or set deck.images.cover")
    cover_fail = []
    if not slides:
        cover_fail.append(f"the deck has no cover slide — {remedy}")
    else:
        cover_slide = slides[0]
        layout = cover_slide.slide_layout
        got_layout = (layout.name or "").strip()
        if not want_layout:
            note.append("the reference geometry records no cover layout name "
                        "(cover.layout), so only the picture half of the cover "
                        "check runs")
        elif norm(got_layout) != norm(want_layout):
            cover_fail.append(
                f"the cover sits on the \"{got_layout or 'unnamed'}\" layout, not the "
                f"reference's \"{want_layout}\" photo layout that carries the family's "
                f"hero — {remedy}")
        pics = sum(1 for sp in list(walk(layout.shapes)) + shapes.get(COVER, [])
                   if sp.shape_type is not None and "PICTURE" in str(sp.shape_type))
        if pics == 0:
            cover_fail.append(f"the cover has no hero picture — {remedy}")
    fail.extend(cover_fail)

    # 5 — the reference's own faces only
    seen = {}
    for i, sps in shapes.items():
        for sp in sps:
            for face in typefaces(sp):
                if face.startswith("+"):        # a theme reference, always fine
                    continue
                if face_key(face) not in allowed_faces:
                    seen.setdefault(face, set()).add(i)
    for face, on in sorted(seen.items()):
        fail.append(f"the face \"{face}\" is used on slide(s) "
                    f"{', '.join(str(n) for n in sorted(on))}; the reference deck "
                    f"uses {face_names}")

    # 6 — corners: the reference rounds chips and badges, nothing else
    for i, sps in shapes.items():
        budget = budgets.get(i)
        if budget is None:
            continue
        role = budget.get("role", "")
        pills = 0
        for sp in sps:
            adj = corner_adj(sp)
            if adj is None or adj <= pill_min:
                continue
            if height_in(sp) > pill_max_h:
                label = norm(shape_text(sp))[:40] or "no text"
                fail.append(f"slide {i} ({role}): a {height_in(sp):.2f} in shape has "
                            f"rounded corners (\"{label}\") — cards, panels and "
                            f"diagram boxes are square; only chips and badges are "
                            f"pills, and none is over {pill_max_h:g} in tall")
            else:
                pills += 1
        cap = budget.get("max_rounded")
        if cap is not None and pills > cap:
            ref_n = budget.get("ref_rounded", 0)
            fail.append(f"slide {i} ({role}): {pills} pills, more than the {cap} this "
                        f"slide allows (the reference has {ref_n})")

    # 7 — an icon, not a number, on every industry card; and no extra pictures
    for i, sps in shapes.items():
        budget = budgets.get(i)
        if budget is None or budget.get("max_pictures") is None:
            continue
        pics = sum(1 for sp in sps
                   if sp.shape_type is not None and "PICTURE" in str(sp.shape_type))
        if pics > budget["max_pictures"]:
            fail.append(f"slide {i} ({budget.get('role', '')}): {pics} pictures, more "
                        f"than the {budget['max_pictures']} the reference's own slide "
                        f"{budget.get('exemplar_slide', '?')} carries")
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

    # 8 — the proof slide: the delivered case, in the reference's composition
    #
    # The owner's rule (2026-09-23): the proof slide is the delivered engagement told
    # in the reference's own shape — the customer's logo top-left, a headline, three
    # stat tiles, and four quadrants labelled as the reference labels them. The build
    # this was set on had no logo, an empty stat band and relabelled quadrants; every
    # one of those comes back red here.
    proof_cfg = geometry.get("proof") or {}
    proof = shapes.get(PROOF, [])
    tol = float(proof_cfg.get("match_tol_in", 0.25))
    # The labels and the tiles are found where the reference put them: the deck is
    # built from the exemplar, so they are where the reference has them.
    proof_shape = fail

    for i, quad in enumerate(proof_cfg.get("quadrants") or [], start=1):
        want = str(quad.get("label", ""))
        sp = shape_at(proof, quad.get("at") or {}, tol)
        got = shape_text(sp).strip() if sp is not None else ""
        if not got:
            proof_shape.append(f"slide {PROOF}: the {i} of 4 block has no label — the "
                               f"four are "
                               f"{', '.join(str(q.get('label')) for q in proof_cfg['quadrants'])}"
                               f", in that order")
        elif norm(got) != norm(want):
            proof_shape.append(f"slide {PROOF}: the {i} of 4 block is labelled "
                               f"\"{got[:60]}\"; the reference labels it \"{want}\" — the "
                               f"four labels and their order are the reference's, not "
                               f"the pack's")

    for i, tile in enumerate(proof_cfg.get("stat_tiles") or [], start=1):
        value = shape_at(proof, tile.get("value") or {}, tol)
        label = shape_at(proof, tile.get("label") or {}, tol)
        missing = [what for what, sp in (("figure", value), ("caption", label))
                   if sp is None or not shape_text(sp).strip()]
        if missing:
            proof_shape.append(f"slide {PROOF}: stat tile {i} of 3 has no "
                               f"{' and no '.join(missing)} — the three tiles are never "
                               f"empty: the cleared figures, or the metrics being "
                               f"measured with their baselines")

    if reference:
        note.append("reference mode: the customer's logo is not checked against a "
                    "clearance — that is about a pack brief, not geometry")
    elif not exp["have_spec"]:
        note.append(f"slide {PROOF}: no pack brief, so whether the customer's logo "
                    f"belongs on this slide cannot be checked — pass --spec")
    else:
        pics = [sp for sp in proof if is_picture(sp)]
        if exp["name_allowed"] and exp["customer_logo"]:
            if not pics:
                fail.append(f"slide {PROOF}: the pack brief clears the customer's name "
                            f"for {exp['channel']} and names a logo file "
                            f"(\"{exp['customer_logo']}\"), and the slide carries no "
                            f"picture — the proof slide shows the customer's logo")
        elif exp["name_allowed"]:
            warn.append(f"slide {PROOF}: the customer's name is cleared for this "
                        f"audience but no logo file was given — the proof slide shows "
                        f"no logo (set deck.images.customer_logo)")
        elif pics:
            fail.append(f"slide {PROOF}: the pack brief does not clear the customer's "
                        f"name for {exp['channel']}, and the slide carries "
                        f"{len(pics)} picture(s) — with no clearance the proof slide "
                        f"carries no logo")

    # 9 — the architecture slide names things and draws the flows
    arch = shapes.get(ARCHITECTURE, [])
    texts = [shape_text(sp) for sp in arch]
    blob = norm(" || ".join(texts))
    if reference:
        note.append("reference mode: the architecture slide's naming and flow rules "
                    "are not checked — they are about a pack brief, not geometry")
    else:
        if exp["name"] and norm(exp["name"]) not in blob:
            fail.append(f"slide {ARCHITECTURE}: no box names the pack "
                        f"(\"{exp['name']}\")")
        if exp["engine_products"]:
            if not any(norm(p) in blob for p in exp["engine_products"]):
                fail.append(f"slide {ARCHITECTURE}: the engine box names no product — "
                            f"it should name "
                            f"{' or '.join(exp['engine_products'])}")
        elif exp["have_spec"]:
            note.append(f"slide {ARCHITECTURE}: the pack brief names no product for "
                        f"the engine layer, so there is nothing to check it against")
        # One box per system the result goes to. A system the pack also reads is a
        # write-back: its own source box is that box, and the second arrow is the
        # write-back — so the check is the same either way, the name is on a box.
        for system in exp["outputs"]:
            plain = re.sub(r"\s+[—–-]\s+", " ", system)   # "Any CRM — Oracle CX included" prints as name + second line
            if not any(mentions(t, system) or mentions(t, plain) for t in texts):
                fail.append(f"slide {ARCHITECTURE}: no box says where the result goes "
                            f"— \"{system}\" is in the pack brief's outputs and on no "
                            f"box on the slide")
        if not exp["outputs"] and exp["have_spec"]:
            note.append(f"slide {ARCHITECTURE}: the pack brief names no destination "
                        f"system, so there is no destination box to check")
        arrows = sum(1 for sp in arch if prst_of(sp) in ARROW_PRSTS)
        if exp["have_spec"] and arrows < exp["inputs"]:
            fail.append(f"slide {ARCHITECTURE}: {arrows} arrows for {exp['inputs']} "
                        f"data sources — every source has its own labelled arrow in")

    # 10 — package-table type at or above the reference's own floor
    for i, budget in budgets.items():
        floor = budget.get("table_floor_pt")
        if floor is None:
            continue
        for sp in shapes.get(i, []):
            if not getattr(sp, "has_table", False):
                continue
            for text, pt in table_sizes(sp):
                if pt < floor - 1e-6:
                    fail.append(f"slide {i}: a cell is set at {pt:g} pt, below the "
                                f"{floor:g} pt floor the reference's own table holds "
                                f"(\"{text[:48]}\") — shorten the wording instead")
                    break
    # 11 — the technology-stack ladder: rows are one width, and what a row holds
    # stays inside it with the reference's inset. A card flush with, or over, its
    # band's edge is the defect the owner's review caught (2026-09-23) after a
    # four-layer stack shortened the rows and left the cards at their old height.
    for i in sorted(shapes):
        rows = ladder_rows(shapes[i])
        if not rows:
            continue
        widths = {round(width_in(r), 2) for r in rows}
        lefts = {round(left_in(r), 2) for r in rows}
        if len(widths) > 1 or len(lefts) > 1:
            fail.append(f"slide {i}: the ladder's rows are not one width on one left edge "
                        f"({', '.join(f'{w:g}' for w in sorted(widths))} in wide)")
        for sp in shapes[i]:
            if sp in rows or getattr(sp, "has_table", False):
                continue
            t, h, l, w = top_in(sp), height_in(sp), left_in(sp), width_in(sp)
            if h <= 0 or w <= 0:
                continue
            cy, cx = t + h / 2, l + w / 2
            row = next((r for r in rows
                        if top_in(r) <= cy <= top_in(r) + height_in(r)
                        and left_in(r) <= cx <= left_in(r) + width_in(r)), None)
            if row is None:
                continue
            rt, rb = top_in(row), top_in(row) + height_in(row)
            over = max(rt - t, (t + h) - rb)
            label = shape_text(sp).strip().splitlines()[0][:40] if shape_text(sp).strip() \
                else (getattr(sp, "name", "") or "a shape")
            if over > 0.02:
                fail.append(f"slide {i}: \"{label}\" sticks out of its row by {over:.2f} in "
                            f"— the row was resized and what it holds was not")
            elif (getattr(sp, "shape_type", None) == 1 and w >= 1.0   # a card, not an accent bar or a divider
                  and h >= 0.6 * height_in(row) and min(t - rt, rb - (t + h)) < 0.05):
                fail.append(f"slide {i}: a card sits flush with its row's edge — the "
                            f"reference insets its cards by 0.13 in")
        break   # one ladder per deck
    return fail, note, warn


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
    ap.add_argument("--reference", action="store_true",
                    help="the deck IS the exemplar: skip the checks that compare it "
                         "against a pack brief (header, cover tier line, the "
                         "architecture's naming and flows)")
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
        exp = expectations(None if args.reference else args.spec,
                           args.channel, None if args.reference else args.header)
    except Exception as exc:
        print(f"lint_deck: cannot read the pack spec ({args.spec}): {exc}",
              file=sys.stderr)
        return 2
    try:
        fail, note, warn = run_checks(deck, exp, geometry, reference=args.reference)
    except Exception as exc:
        print(f"lint_deck: cannot read the deck: {exc}", file=sys.stderr)
        return 2

    for n in note:
        print(f"  note: {n}")
    for w in warn:
        print(f"  WARNING: {w}")
    if fail:
        print(f"{len(fail)} problem(s) in {deck.name}:")
        for f in fail:
            print(f"  - {f}")
        return 1
    if warn:
        print(f"{deck.name}: clean apart from the cover warning above — "
              f"not a deliverable deck.")
        return 0
    print(f"{deck.name}: clean — ten slides, the running header, the cover's hero, "
          f"the reference's faces, square corners, industry icons, the proof slide's "
          f"four labels and three tiles, the architecture names and flows, table type "
          f"at or above the floor.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
