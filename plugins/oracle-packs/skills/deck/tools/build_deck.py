#!/usr/bin/env python3
"""Build the 10-slide Oracle accelerator-pack sales deck from a pack spec.

    build_deck.py <pack-spec.yaml> --out <dir> [--channel partner_print|internal]
                  [--fit-report] [--allow-overflow] [--base <pptx>]

One function per slide; geometry from references/deck-anatomy.md. Text is
sized to fit with a headless estimate (Pillow on the brand face the plugin ships,
+2% safety, else on a Helvetica-metric stand-in, +6%) — the deck-kit rule is:
trust geometry, not glyph widths.
A box that would still overflow is printed and the build exits non-zero.

Dependencies: pyyaml, python-pptx, Pillow  (see plugins/oracle-packs/requirements.txt)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
for _cand in (_HERE, _HERE.parents[1] / "deck" / "tools"):
    if (_cand / "deckkit.py").exists():
        sys.path.insert(0, str(_cand))
        break

from pptx.enum.shapes import MSO_SHAPE                       # noqa: E402
from pptx.enum.dml import MSO_LINE_DASH_STYLE                # noqa: E402
from pptx.enum.text import MSO_ANCHOR                        # noqa: E402
from pptx.dml.color import RGBColor                          # noqa: E402
from pptx.util import Emu, Pt                                # noqa: E402

from deckkit import (                                        # noqa: E402
    C, CONTENT_W, DECK_TITLE_BOX, FONT_BODY, FONT_TITLE, FitEntry, FitLog, MARGIN_L,
    Spec, SpecError, autofit_paras, autofit_pt, fmt_duration, fmt_price, inch,
    log_box, new_slide, open_base, panel, pick_layout, product_name, rect,
    stacked_height, textbox, wrap_count,
)

for _up in range(2, 6):                     # the spec stamp: the plugin's synced shared/tools, or the bundle's
    _shared = _HERE.parents[_up] / "shared" / "tools" if len(_HERE.parents) > _up else None
    if _shared is not None and (_shared / "spec_stamp.py").is_file():
        sys.path.insert(0, str(_shared))
        break
import spec_stamp                                            # noqa: E402  (which spec the deck was built from)

BASE_DEFAULT = _HERE.parent / "assets" / "softserve-deck-base.pptx"

# The shared icon library — plugin copy first, then a source checkout, the same
# two places deckkit looks for the product catalog.
ICON_DIRS = [_HERE.parents[up] / "shared" / "data" / "icons" for up in (2, 4)
             if len(_HERE.parents) > up]

# The running header mirrors the mini-site lockup, so a seller who has seen the
# site recognises the deck. `deck.running_header` in the spec still overrides.
DEFAULT_HEADER = "Oracle AI & Data Solutions — {name}"
HEADER_PT = 9.0                 # measured off the reference deck's header

# The reference deck draws structure with square corners: its cards, panels and
# diagram boxes carry a 0.04–0.12 in radius on shapes inches wide, which reads
# square at slide scale. Only chips and badges are real pills (adj 50000). So
# `rounded` is opt-in here, and PILL is the only radius the deck uses.
PILL = 0.5
STAT_TILE_ADJ = 0.10            # the reference's stat tiles, adj 10000

# Neither brand face carries U+25CF / U+25D0 / U+25CB, so a renderer substitutes a
# different face per glyph and they come out at different sizes (the owner,
# 2026-09-22). One symbol face for all three fixes it by construction — the same
# move the feature-list builder makes; `a:sym` names the Windows equivalent,
# which is the closest a .pptx run gets to Word's fontTable altName.
SYMBOL_FONT = "Apple Symbols"
SYMBOL_ALT = "Segoe UI Symbol"

# Type floors on the package tables: the table never shrinks below these, and a
# table that will not fit at the floor is reported so the wording gets shortened.
TABLE_FLOOR = {9: 11.0, 10: 10.5}
DETAILED_CELL_WORDS = 12        # word budget per cell on slide 10

# Vendor → (tint, bar) for the solution-layers ladder, per the R&D monthly deck.
VENDOR_COLORS = [
    ("softserve", (C["orange_tint"], C["orange"])),
    ("oracle + softserve", ("D2E7F6", C["blue"])),
    ("softserve + oracle", ("D2E7F6", C["blue"])),
    ("nvidia", (C["blue_tint"], C["blue_light"])),
    ("oracle", ("EEF1F3", "6B7680")),
]
TIER_HEADER_FILL = [C["orange_light"], C["orange"], C["orange_dark"]]
GLYPH_DEFAULT = {"pov": "◐", "integration": "●", "scaling": "●●"}
GLYPH_NONE = "—"
NO_STYLE = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"  # "No Style, No Grid"


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------

def vendor_colors(vendor: str, i: int) -> tuple[str, str]:
    v = (vendor or "").strip().lower()
    for key, cols in VENDOR_COLORS:
        if key == v:
            return cols
    for key, cols in VENDOR_COLORS:
        if key in v:
            return cols
    return [(C["blue_tint"], C["blue"]), ("EEF1F3", "6B7680"),
            (C["orange_tint"], C["orange"]), (C["blue_tint_2"], C["blue_light"])][i % 4]


def style_header(slide, text: str) -> None:
    """Set the running header explicitly — face, size, colour, alignment.

    The layout would supply all four, but a run that names nothing inherits
    whatever the host master happens to define, and the header is the one string
    on every slide: it is written out.
    """
    from pptx.enum.text import PP_ALIGN
    for ph in slide.placeholders:
        if ph.placeholder_format.idx != 34:
            continue
        tf = ph.text_frame
        tf.word_wrap = True
        tf.text = text
        for p in tf.paragraphs:
            p.alignment = PP_ALIGN.RIGHT
            for r in p.runs:
                r.font.size = Pt(HEADER_PT)
                r.font.bold = False
                r.font.name = FONT_BODY
                r.font.color.rgb = RGBColor.from_string(C["muted"])
        return


def chip(slide, x, y, w, h, text, fill=C["panel_grey"], color=C["blue"], sz=9.5,
         line=None):
    """A pill — the one shape the reference deck really rounds (adj 50000)."""
    rect(slide, x, y, w, h, fill=fill, line=line, rounded=True, adj=PILL)
    textbox(slide, x + 0.08, y, w - 0.16, h,
            [{"t": text, "sz": sz, "b": True, "color": color, "align": "c"}],
            anchor="m")


def badge(slide, x, y, d, label, color=C["orange"]):
    """Outlined numeral badge — slide-design rule 8 (no heavy ink fills)."""
    rect(slide, x, y, d, d, fill=C["white"], line=color, line_pt=1.25,
         rounded=True, adj=PILL)
    textbox(slide, x, y, d, d,
            [{"t": label, "sz": 9.5, "b": True, "color": color, "align": "c"}],
            anchor="m")


# ---------------------------------------------------------------------------
# the shared icon library
# ---------------------------------------------------------------------------

_ICON_MAP: dict | None = None


def icon_library() -> dict:
    """{"dir": Path, "fallback": str, "icons": [...]} — empty when unreachable."""
    global _ICON_MAP
    if _ICON_MAP is None:
        _ICON_MAP = {}
        for d in ICON_DIRS:
            f = d / "map.yaml"
            if not f.is_file():
                continue
            try:
                import yaml
                data = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
            except Exception:           # a broken library is not a crash
                continue
            _ICON_MAP = {"dir": d,
                         "fallback": str(data.get("fallback") or "generic.png"),
                         "icons": list(data.get("icons") or [])}
            break
    return _ICON_MAP


def icon_for(name: str) -> tuple[Path | None, bool]:
    """(file, matched) for a vertical's name. `matched` is False on the fallback."""
    lib = icon_library()
    if not lib:
        return None, False
    hay = str(name or "").lower()
    best, best_len = None, 0
    for row in lib["icons"]:
        for kw in (row.get("keywords") or []):
            k = str(kw).lower().strip()
            if k and k in hay and len(k) > best_len:
                best, best_len = row.get("file"), len(k)
    path = lib["dir"] / str(best or lib["fallback"])
    if not path.is_file():
        return None, False
    return path, bool(best)


def place_image(slide, path, x, y, w, h):
    """Fill the slot with the image, scaled to cover and cropped to the centre."""
    from PIL import Image
    with Image.open(path) as im:
        iw, ih = im.size
    slot = w / h
    src = (iw / ih) if ih else slot
    pic = slide.shapes.add_picture(str(path), inch(x), inch(y), inch(w), inch(h))
    if src > slot:                       # too wide: trim the sides
        keep = slot / src
        pic.crop_left = pic.crop_right = (1 - keep) / 2
    elif src < slot:                     # too tall: trim top and bottom
        keep = src / slot
        pic.crop_top = pic.crop_bottom = (1 - keep) / 2
    return pic


def arrow(slide, x, y, w, h, color=C["blue"], left=False):
    shp = slide.shapes.add_shape(
        MSO_SHAPE.LEFT_ARROW if left else MSO_SHAPE.RIGHT_ARROW,
        inch(x), inch(y), inch(w), inch(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = RGBColor.from_string(color)
    shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def strip(slide, y, text, fit, slide_no, label="anchor strip", fill=C["ink"],
          sz=11.5, h=0.46):
    rect(slide, MARGIN_L, y, CONTENT_W, h, fill=fill)
    textbox(slide, MARGIN_L + 0.18, y, CONTENT_W - 0.36, h,
            [{"t": text, "sz": sz, "b": True, "color": C["white"], "align": "c"}],
            anchor="m")
    fit.add(slide_no, label, text, sz, CONTENT_W - 0.36, h, bold=True, max_lines=1)


def footnote(slide, text, fit, slide_no, y=6.84, sz=8.0):
    if not text:
        return
    textbox(slide, MARGIN_L, y, CONTENT_W, 0.30,
            [{"t": text, "sz": sz, "color": C["muted_light"]}])
    fit.add(slide_no, "footnote", text, sz, CONTENT_W, 0.30, max_lines=2)


def content_title(slide, text, fit, slide_no, sub=None):
    x, y, w, h = DECK_TITLE_BOX
    pt = autofit_pt(text, w, 0.50, 26, 18, bold=True, max_lines=1)
    textbox(slide, x, y, w, 0.50,
            [{"t": text.upper(), "sz": pt, "b": True, "color": C["ink"]}], anchor="t")
    fit.add(slide_no, "title", text.upper(), pt, w, 0.50, bold=True, max_lines=1)
    if sub:
        textbox(slide, MARGIN_L, 2.24, CONTENT_W, 0.30,
                [{"t": sub, "sz": 12, "color": C["muted"]}])
        fit.add(slide_no, "title sub", sub, 12, CONTENT_W, 0.30, max_lines=1)


# ---------------------------------------------------------------------------
# slides
# ---------------------------------------------------------------------------

def step_band(slide, y, steps, fit, slide_no, label="HOW IT RUNS"):
    """A true sequence reads horizontally (slide-design rule 9)."""
    n = max(1, min(len(steps), 6))
    arrow_w, gap = 0.26, 0.16
    bw = (CONTENT_W - (n - 1) * (arrow_w + 2 * gap)) / n
    textbox(slide, MARGIN_L, y, CONTENT_W, 0.24,
            [{"t": label, "sz": 10.5, "b": True, "color": C["blue"]}])
    top = y + 0.32
    bh = 1.05
    for i in range(n):
        st = steps[i]
        x = MARGIN_L + i * (bw + arrow_w + 2 * gap)
        rect(slide, x, top, bw, bh, fill=C["white"], line=C["hairline"], line_pt=0.75)
        badge(slide, x + 0.16, top + 0.14, 0.26, str(st.get("n", i + 1)),
              color=C["blue"])
        name = str(st.get("name", ""))
        pt = autofit_pt(name, bw - 0.32, 0.46, 11, 8, bold=True, max_lines=3)
        textbox(slide, x + 0.16, top + 0.48, bw - 0.32, 0.46,
                [{"t": name, "sz": pt, "b": True, "color": C["ink"]}])
        fit.add(slide_no, f"step {i+1}", name, pt, bw - 0.32, 0.46, bold=True, max_lines=3)
        if st.get("human_in_the_loop"):
            textbox(slide, x + 0.52, top + 0.14, bw - 0.68, 0.26,
                    [{"t": "person in the loop", "sz": 7.5, "color": C["muted"]}],
                    anchor="m")
        if i < n - 1:
            arrow(slide, x + bw + gap, top + bh / 2 - 0.05, arrow_w, 0.10,
                  color=C["hairline_alt"])
    return top + bh


def slide_01_cover(prs, layout, spec: Spec, fit: FitLog):
    """The reference cover, rebuilt on the base.

    The reference sets its cover on a dark photo layout the base does not carry,
    so the ground is drawn; everything above it keeps the reference's own block —
    a 5.70 in text column at x 0.55, the pack name at 44 pt over the one-liner at
    25 pt, and one small line low on the slide. The reference used that low line
    for the three tier names; the owner asked for no tier line on a cover, so it
    carries the pack's subheading and who the pack is for instead.
    """
    s = new_slide(prs, layout, title=None, header=None)
    rect(s, 0, 0, 13.34, 7.5, fill=C["ink"])

    # The reference sets every run on its cover in the theme's title face; the
    # content slides use the body face. Both are kept.
    col_x, col_w = 0.55, 5.70
    name = spec.name()
    pt = autofit_pt(name, col_w, 1.55, 44, 28, bold=False, max_lines=2)
    lines = wrap_count(name, pt, col_w)
    name_h = max(0.60, lines * pt * 1.22 / 72.0)
    textbox(s, col_x, 2.30, col_w, name_h,
            [{"t": name, "sz": pt, "color": C["white"], "font": FONT_TITLE}])
    fit.add(1, "cover title", name, pt, col_w, name_h, max_lines=2)

    one = spec.get("one_liner.full") or spec.get("one_liner.short") or ""
    one_y = 2.30 + name_h + 0.14
    one_h = max(0.40, 5.00 - one_y)
    opt = autofit_pt(one, col_w, one_h, 25, 15, max_lines=5)
    textbox(s, col_x, one_y, col_w, one_h,
            [{"t": one, "sz": opt, "color": "D9E4EC", "font": FONT_TITLE}])
    fit.add(1, "cover one-liner", one, opt, col_w, one_h, max_lines=5)

    sub = spec.subheading()
    if sub:
        spt = autofit_pt(sub, 4.60, 0.30, 14, 10, bold=True, max_lines=1)
        textbox(s, 0.57, 5.20, 4.60, 0.30,
                [{"t": sub, "sz": spt, "b": True, "color": C["white"],
                  "font": FONT_TITLE}])
        fit.add(1, "cover subheading", sub, spt, 4.60, 0.30, bold=True, max_lines=1)

    icp = spec.get("icp.line")
    if icp:
        textbox(s, 0.57, 5.62, col_w, 0.50,
                [{"t": [("WHO IT IS FOR   ", {"color": C["orange"], "b": True, "sz": 9}),
                        (icp, {"color": "AEB6BD", "sz": 10})], "font": FONT_TITLE}])
        fit.add(1, "cover icp", "WHO IT IS FOR   " + icp, 10, col_w, 0.50, max_lines=3)
    return s



def point_text(point) -> str:
    """A `problem_points` entry: a plain string, or `{label, text}` from the schema."""
    if isinstance(point, dict):
        label = str(point.get("label") or "").strip()
        body = str(point.get("text") or point.get("detail") or "").strip()
        if label and body:
            return f"{label}: {body}"
        return label or body
    return str(point)


def slide_02_use_case(prs, layout, spec: Spec, fit: FitLog, header: str):
    s = new_slide(prs, layout, title=None, header=header)
    style_header(s, header)
    content_title(s, "Use case", fit, 2)

    ps = spec.get("problem_solution", {}) or {}
    top, h = 1.92, 3.68
    panel(s, MARGIN_L, top, 6.02, h, fill=C["panel_grey"], accent=C["ink_soft"],
          accent_w=0.10, line=None)
    panel(s, 6.89, top, 6.02, h, fill=C["blue_tint_2"], accent=C["blue"],
          accent_w=0.10, line=None)

    textbox(s, 0.77, top + 0.18, 5.40, 0.30,
            [{"t": "PROBLEM", "sz": 14, "b": True, "color": C["ink"]}])
    textbox(s, 7.24, top + 0.18, 5.40, 0.30,
            [{"t": "SOLUTION", "sz": 14, "b": True, "color": C["blue"]}])

    problem = str(ps.get("problem", ""))
    bullets = [point_text(b) for b in (ps.get("problem_points") or [])]
    p_paras = [{"t": problem, "sz": 11.5, "b": True, "color": C["ink"],
                "space_after": 8}]
    for b in bullets:
        lead, _, rest = b.partition(":")
        p_paras.append({"t": [(lead + (":" if rest else "") + " ",
                               {"b": True, "color": C["ink"]}),
                              (rest.strip(), {"color": C["muted"]})],
                        "sz": 11, "space_after": 5})
    p_paras = autofit_paras(p_paras, 5.40, h - 0.76, default_sz=11.5,
                            max_scale=1.35)
    textbox(s, 0.76, top + 0.58, 5.40, h - 0.76, p_paras)
    log_box(fit, 2, "problem card", 0.76, top + 0.58, 5.40, h - 0.76, p_paras, 11.5)

    solution = str(ps.get("solution", ""))
    reframe = ps.get("reframe")
    s_paras = []
    if reframe:
        s_paras.append({"t": str(reframe).upper(), "sz": 13, "b": True,
                        "color": C["blue"], "space_after": 7})
    s_paras.append({"t": solution, "sz": 11.5, "color": C["ink"]})
    s_paras = autofit_paras(s_paras, 5.40, 2.30, default_sz=11.5,
                            max_scale=1.35)
    textbox(s, 7.25, top + 0.58, 5.40, 2.30, s_paras)
    log_box(fit, 2, "solution card", 7.25, top + 0.58, 5.40, 2.30, s_paras, 11.5)

    chips = [str(k.get("chip") or k.get("name", "")) for k in spec.kpis()][:3]
    cw, gap = 1.78, 0.06
    for i, label in enumerate(chips):
        x = 7.25 + i * (cw + gap)
        pt = autofit_pt(label, cw - 0.16, 0.34, 9.5, 7.5, bold=True, max_lines=2)
        chip(s, x, 5.05, cw, 0.40, label, fill=C["white"], sz=pt)
        fit.add(2, f"kpi chip {i+1}", label, pt, cw - 0.16, 0.34, bold=True, max_lines=2)

    anchor = spec.get("deck.anchor_line") or spec.get("packages.anchor_line")
    if not anchor:
        req = [p for p in (spec.get("oracle_products") or [])
               if p.get("role") == "required"]
        anchor = ("Anchored to " + ", ".join(
            product_name(p) for p in req[:2]) +
            " — one offer a partner account exec can carry into an account they already own.") if req else ""
    strip(s, 5.82, anchor, fit, 2, "anchor strip", h=0.62)
    return s


def slide_03_verticals(prs, layout, spec: Spec, fit: FitLog, header: str):
    s = new_slide(prs, layout, title=None, header=header)
    style_header(s, header)
    content_title(s, "Vertical applications", fit, 3)

    verticals = (spec.get("verticals") or [])[:4]
    if not verticals:
        fit.note("s3: no verticals in the spec — slide built as empty instances")
    cw, ch = 6.00, 2.00
    icon_d = 1.06                       # the reference's icon, 1.06 x 1.06 in
    xs, ys = [MARGIN_L, 6.72], [2.48, 4.76]
    for i in range(4):
        x, y = xs[i % 2], ys[i // 2]
        v = verticals[i] if i < len(verticals) else None
        rect(s, x, y, cw, ch, fill=C["white"], line=C["hairline_alt"], line_pt=1.0)
        rect(s, x, y, 2.25, ch, fill=C["blue"] if v else C["panel_grey"])
        name = str((v or {}).get("name", ""))
        # An industry gets a picture, never a number: the reference puts one icon
        # in the middle of each card's panel, and the library always resolves —
        # to the neutral mark when nothing matches, and then we say so.
        path, matched = icon_for(name) if v else (None, False)
        if path:
            place_image(s, path, x + (2.25 - icon_d) / 2, y + (ch - icon_d) / 2,
                        icon_d, icon_d)
            if not matched:
                fit.note(f"s3: no icon matches the industry \"{name}\" — the neutral "
                         f"mark is in its card; pick one from the icon library or "
                         f"ask which picture it should carry")
        elif v:
            fit.note(f"s3: the icon library is not reachable — \"{name}\" has an "
                     f"empty panel")
        rect(s, x + 2.25, y, 0.06, ch, fill=C["ink_soft"] if v else C["hairline"])
        if not v:
            continue
        name = str(v.get("name", ""))
        pt = autofit_pt(name, 3.21, 0.70, 14.5, 10, bold=True, max_lines=3)
        textbox(s, x + 2.54, y + 0.24, 3.21, 0.70,
                [{"t": name, "sz": pt, "b": True, "color": C["ink"]}])
        fit.add(3, f"vertical {i+1} name", name, pt, 3.21, 0.70, bold=True, max_lines=3)
        rect(s, x + 2.54, y + 0.99, 0.55, 0.04, fill=C["ink_soft"])
        body = (v.get("what_matters_here")
                or (v.get("framing") or {}).get("solution") or "")
        pt = autofit_pt(str(body), 3.21, 0.85, 11, 8, max_lines=5)
        textbox(s, x + 2.54, y + 1.10, 3.21, 0.85,
                [{"t": str(body), "sz": pt, "color": C["muted"]}])
        fit.add(3, f"vertical {i+1} body", str(body), pt, 3.21, 0.85, max_lines=5)
    return s


def slide_04_today_tomorrow(prs, layout, spec: Spec, fit: FitLog, header: str):
    s = new_slide(prs, layout, title=None, header=header)
    style_header(s, header)
    ps = spec.get("problem_solution", {}) or {}
    images = spec.get("deck.images") or {}
    head = str(ps.get("reframe_question")
               or f"What if the work changed: {ps.get('reframe', 'review, not build')}?")
    pt = autofit_pt(head, 12.00, 0.45, 24, 17, bold=True, max_lines=1)
    textbox(s, 0.43, 1.37, 12.00, 0.45, [{"t": head, "sz": pt, "b": True, "color": C["ink"]}])
    fit.add(4, "reframe headline", head, pt, 12.00, 0.45, bold=True, max_lines=1)

    sub = spec.get("one_liner.short") or spec.get("one_liner.full") or ""
    textbox(s, 0.43, 1.96, 12.00, 0.28, [{"t": sub, "sz": 13, "color": C["muted"]}])
    fit.add(4, "reframe sub", sub, 13, 12.00, 0.28, max_lines=1)

    vcase = spec.get("deck.vertical_case")
    if not vcase and spec.get("verticals"):
        vcase = f"Vertical case: {spec.get('verticals')[0].get('name','')}"
    if vcase:
        textbox(s, 0.43, 2.36, 8.00, 0.26, [{"t": vcase, "sz": 11, "color": C["muted"]}])

    pairs = [("TODAY", C["ink"], str(ps.get("today") or ps.get("problem", "")),
              MARGIN_L, "today"),
             ("TOMORROW", C["blue"], str(ps.get("tomorrow") or ps.get("solution", "")),
              6.88, "tomorrow")]
    missing = []
    for label, fill, body, x, key in pairs:
        rect(s, x, 2.82, 6.02, 0.46, fill=fill)
        textbox(s, x, 2.82, 6.02, 0.46,
                [{"t": label, "sz": 12.5, "b": True, "color": C["white"], "align": "c"}],
                anchor="m")
        pt = autofit_pt(body, 6.02, 0.92, 11, 8.5, max_lines=6)
        textbox(s, x, 3.38, 6.02, 0.92, [{"t": body, "sz": pt, "color": C["muted"]}])
        fit.add(4, f"{label.lower()} body", body, pt, 6.02, 0.92, max_lines=6)
        # The two picture slots. When the spec names a file, it fills the slot,
        # scaled to cover and cropped to the centre. Otherwise the slot stays an
        # empty instance of the same container (rule 3), never a bare gap, and
        # the skill asks for the picture before the deck is shown.
        src = images.get(key)
        path = Path(str(src)).expanduser() if src else None
        if path and not path.is_absolute():   # relative to the pack brief's folder
            path = (getattr(spec, "spec_dir", Path(".")) / path).resolve()
        if path and path.is_file():
            place_image(s, path, x, 4.45, 6.02, 2.15)
            continue
        if src:
            fit.note(f"s4: the {key} picture is set to \"{src}\", which is not a "
                     f"file here — the slot is empty")
        missing.append(key)
        slot = rect(s, x, 4.45, 6.02, 2.15, fill=C["panel_grey"], line=C["hairline_alt"])
        slot.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        textbox(s, x + 0.20, 4.45, 5.62, 2.15,
                [{"t": "image to be chosen", "sz": 9.5,
                  "color": C["muted_light"], "align": "c"}], anchor="m")
    if missing:
        fit.note("s4: " + (" and ".join(missing)) + " — the picture slot(s) are "
                 "still empty; the slide wants the bad current experience on the "
                 "left and the good future with the solution on the right")
    return s


def slide_05_proof(prs, layout, spec: Spec, fit: FitLog, header: str):
    s = new_slide(prs, layout, title=None, header=header)
    style_header(s, header)
    kpis = spec.kpis()
    headline = spec.get("deck.proof_headline") or (
        f"{spec.proof_word()} on real data at {spec.customer_label()}")
    pt = autofit_pt(headline, 12.49, 0.55, 23, 16, bold=True, max_lines=1)
    textbox(s, MARGIN_L, 1.30, 12.49, 0.55,
            [{"t": headline, "sz": pt, "b": True, "color": C["ink"]}], anchor="m")
    fit.add(5, "proof headline", headline, pt, 12.49, 0.55, bold=True, max_lines=1)

    # Peer claims: all or none (slide-design rule 11). If any KPI in the set is
    # not clearable for this channel, the whole strip goes.
    usable = spec.figured_kpis()
    blocked = [k for k in kpis
               if k.get("channels") and spec.channel not in k["channels"]]
    show_stats = usable and not blocked
    if kpis and not show_stats:
        fit.note("s5: KPI strip dropped — not every metric in the set is cleared "
                 "for this channel (peer claims are all-or-none)")

    cw, gap = 3.96, 0.30
    if show_stats:
        for i, k in enumerate(usable[:3]):
            x = MARGIN_L + i * (cw + gap)
            rect(s, x, 2.10, cw, 0.80, fill=C["panel_grey"], rounded=True,
                 adj=STAT_TILE_ADJ)
            fig = str(k.get("figure", ""))
            base = k.get("baseline")
            shown = f"{base} → {fig}" if base and k.get("show_baseline") else fig
            fpt = autofit_pt(shown, cw - 0.36, 0.34, 19, 12, bold=True, max_lines=1)
            textbox(s, x + 0.18, 2.22, cw - 0.36, 0.34,
                    [{"t": shown, "sz": fpt, "b": True, "color": C["blue"]}])
            fit.add(5, f"stat {i+1} value", shown, fpt, cw - 0.36, 0.34,
                    bold=True, max_lines=1)
            # a formula is a definition, not a stat label: name before formula
            lab = str(k.get("label") or k.get("name") or k.get("formula", ""))
            lpt = autofit_pt(lab, cw - 0.36, 0.28, 8.5, 6.5, max_lines=2)
            textbox(s, x + 0.18, 2.58, cw - 0.36, 0.28,
                    [{"t": lab, "sz": lpt, "color": C["muted"]}])
            fit.add(5, f"stat {i+1} label", lab, lpt, cw - 0.36, 0.28, max_lines=2)

    band_y = 3.10 if show_stats else 2.30
    se = spec.get("meta.source_engagement", {}) or {}
    blocks = [
        ("CONTEXT", f"{spec.customer_label().capitalize()}. {se.get('delivered', '')}".strip()),
        ("WHAT THE PACK DOES", str((spec.get("problem_solution") or {}).get("solution", ""))),
    ]
    need = max(stacked_height([{"t": b, "sz": 10.5}], 5.68)[0] for _, b in blocks)
    band_h = min(6.05 - band_y, max(1.25, need + 0.56))
    for i, (label, body) in enumerate(blocks):
        x = MARGIN_L + i * (6.02 + 0.45)
        rect(s, x, band_y, 6.02, 0.36, fill=C["blue"])
        textbox(s, x + 0.16, band_y, 5.72, 0.36,
                [{"t": label, "sz": 11, "b": True, "color": C["white"]}], anchor="m")
        rect(s, x, band_y + 0.36, 6.02, band_h - 0.36, fill=C["white"],
             line="DDE2E6", line_pt=0.75)
        pt = autofit_pt(body, 5.68, band_h - 0.56, 10.5, 8, max_lines=14)
        textbox(s, x + 0.17, band_y + 0.46, 5.68, band_h - 0.56,
                [{"t": body, "sz": pt, "color": C["ink"]}])
        fit.add(5, f"proof block {i+1}", body, pt, 5.68, band_h - 0.56, max_lines=14)

    caveat = spec.kpi_caveat()
    attribution = spec.kpi_attribution()
    # `divergence_line` is the print-ready sentence; `divergence_from_pack` is the
    # internal statement and overflows a two-line footnote by design.
    div = se.get("divergence_line")   # the one print-ready sentence; the internal note never prints
    tail = " ".join(x for x in [f"Source: {attribution}.", caveat,
                                (f"Pack scope differs from the delivered engagement: {div}"
                                 if div else "")] if x)
    steps = spec.get("workflow.steps") or []
    bottom = band_y + band_h
    if steps and bottom + 1.60 < 6.55:
        bottom = step_band(s, bottom + 0.34, steps, fit, 5,
                           label="HOW THE PLAN GETS MADE")
    footnote(s, tail, fit, 5, y=min(6.62, bottom + 0.20), sz=8.5)
    return s


def slide_06_why_it_sells(prs, layout, spec: Spec, fit: FitLog, header: str):
    s = new_slide(prs, layout, title=None, header=header)
    style_header(s, header)
    content_title(s, "Why it sells for your account team", fit, 6,
                  sub=spec.get("deck.seller_lead"))
    claims = [str(c) for c in (spec.get("packages.why_it_sells_for_the_partner") or [])]
    if not claims:
        claims = ["(no seller claims in the spec — confirm them with /oracle-packs:spec)"]
        fit.note("s6: packages.why_it_sells_for_the_partner is empty")
    n = max(1, min(len(claims), 4))
    gap = 0.26
    cw = (CONTENT_W - gap * (n - 1)) / n
    heads, details = [], []
    for i in range(n):
        head, _, rest = claims[i].partition(" \u2014 ")
        heads.append(head)
        details.append(rest)
    cwi = (CONTENT_W - gap * (n - 1)) / n - 0.52
    y, max_ch = 2.72, 3.10
    head_sz, det_sz, scale = 14.0, 10.0, 1.0
    while True:
        head_sz, det_sz = round(14 * scale, 2), round(10 * scale, 2)
        head_h = max(stacked_height([{"t": h, "sz": head_sz, "b": True}], cwi)[0]
                     for h in heads)
        det_h = max([stacked_height([{"t": d, "sz": det_sz}], cwi)[0]
                     for d in details if d] or [0])
        ch = 0.72 + head_h + (det_h + 0.18 if det_h else 0) + 0.28
        if ch <= max_ch or scale <= 0.70:
            break
        scale = round(scale - 0.04, 3)
    ch = min(max_ch, ch)
    for i in range(n):
        x = MARGIN_L + i * (cw + gap)
        rect(s, x, y, cw, ch, fill=C["white"], line=C["hairline"], line_pt=0.75)
        badge(s, x + 0.26, y + 0.26, 0.30, str(i + 1))
        head, rest = heads[i], details[i]
        # Every card hangs its claim and its detail from ONE shared baseline
        # grid computed over all cards, so no card jumps (slide-design rule 2).
        textbox(s, x + 0.26, y + 0.72, cwi, head_h,
                [{"t": head, "sz": head_sz, "b": True, "color": C["ink"]}])
        fit.add(6, f"seller claim {i+1}", head, head_sz, cwi, head_h, bold=True)
        if rest:
            textbox(s, x + 0.26, y + 0.72 + head_h + 0.18, cwi, det_h,
                    [{"t": rest, "sz": det_sz, "color": C["muted"]}])
            fit.add(6, f"seller detail {i+1}", rest, det_sz, cwi, det_h)

    oci = spec.get("packages.target_oci_consumption")
    oci_y = max(y + ch + 0.30, 5.35)
    if not Spec.has_text(oci):
        # `-` is the spec's "deliberately empty"; a CONSUMPTION strip with a dash
        # in it is an empty container reading as content (slide-design rule 3).
        if oci:
            fit.note("s6: no target OCI consumption in the spec — strip omitted")
        oci = None
    if oci:
        panel(s, MARGIN_L, oci_y, CONTENT_W, 0.48, fill=C["blue_tint"],
              accent=C["blue"], line=C["hairline"])
        textbox(s, MARGIN_L + 0.26, oci_y, CONTENT_W - 0.52, 0.48,
                [{"t": [("CONSUMPTION  ", {"b": True, "color": C["blue"], "sz": 9}),
                        (str(oci), {"color": C["ink"], "sz": 10.5})]}], anchor="m")
        fit.add(6, "consumption strip", "CONSUMPTION  " + str(oci), 10.5,
                CONTENT_W - 0.52, 0.48, max_lines=1)

    ct = spec.contact()
    cta = spec.get("deck.cta") or "Ready to test the fit in one of your accounts?"
    who = " · ".join(x for x in [ct.get("name"), ct.get("title"), ct.get("email")] if x)
    rect(s, MARGIN_L, 6.16, CONTENT_W, 0.52, fill=C["ink"])
    textbox(s, MARGIN_L + 0.22, 6.16, 6.20, 0.52,
            [{"t": cta, "sz": 11.5, "b": True, "color": C["white"]}], anchor="m")
    textbox(s, 6.80, 6.16, 6.11 - 0.22, 0.52,
            [{"t": who, "sz": 10, "color": "AEB6BD", "align": "r"}], anchor="m")
    fit.add(6, "cta", cta, 11.5, 6.20, 0.52, bold=True, max_lines=1)
    fit.add(6, "contact", who, 10, 5.89, 0.52, max_lines=1)
    return s


def slide_07_solution_layers(prs, layout, spec: Spec, fit: FitLog, header: str):
    s = new_slide(prs, layout, title=None, header=header)
    style_header(s, header)
    content_title(s, "Solution layers", fit, 7,
                  sub=spec.get("deck.layers_sub")
                  or "How the pack is layered — from the infrastructure up to the customer's own configuration.")
    stack = spec.get("architecture.stack") or []
    if not stack:
        raise SpecError("pack spec has no `architecture.stack` — the "
                        "high-level architecture component is not signed off")
    y0, y1, gap = 2.78, 6.28, 0.14
    n = len(stack)
    rh = (y1 - y0 - gap * (n - 1)) / n
    rect(s, 0.57, y0, 0.02, y1 - y0, fill=C["hairline_alt"])
    textbox(s, 0.95, y0 - 0.28, 7.60, 0.24,
            [{"t": "▲ business value", "sz": 10.5, "b": True, "color": C["blue_dark"]}])
    for i, layer in enumerate(stack):
        y = y0 + i * (rh + gap)
        tint, bar = vendor_colors(str(layer.get("vendor", "")), i)
        panel(s, 0.95, y, 11.45, rh, fill=tint, accent=bar, accent_w=0.06,
              line=C["hairline"])
        name = str(layer.get("layer", ""))
        npt = autofit_pt(name, 3.10, rh - 0.20, 14, 10, bold=True, max_lines=2)
        textbox(s, 1.30, y, 3.10, rh, [{"t": name, "sz": npt, "b": True, "color": C["ink"]}],
                anchor="m")
        fit.add(7, f"layer {i+1} name", name, npt, 3.10, rh - 0.20, bold=True, max_lines=2)
        rect(s, 4.55, y + 0.14, 0.01, rh - 0.28, fill=C["hairline_alt"])
        items = layer.get("items") or []
        body = str(layer.get("summary") or ", ".join(str(i) for i in items))
        bpt = autofit_pt(body, 5.05, rh - 0.20, 11, 8, max_lines=4)
        textbox(s, 4.80, y, 5.05, rh, [{"t": body, "sz": bpt, "color": C["ink"]}], anchor="m")
        fit.add(7, f"layer {i+1} body", body, bpt, 5.05, rh - 0.20, max_lines=4)
        vend = str(layer.get("vendor", ""))
        if vend:
            vpt = autofit_pt(vend, 1.85, 0.30, 10.5, 7, bold=True, max_lines=1)
            chip(s, 10.15, y + (rh - 0.38) / 2, 2.05, 0.38, vend,
                 fill=C["white"], color=C["ink_soft"], sz=vpt)
            fit.add(7, f"layer {i+1} vendor", vend, vpt, 1.85, 0.30, bold=True, max_lines=1)
    return s


def arch_node(entry) -> dict:
    """architecture.inputs/outputs carry `{system, data}` or a plain label.

    A plain string is the older shape and still reads correctly: everything up
    to the first em-dash is the system, the rest is the data it carries.
    """
    if isinstance(entry, dict):
        return entry
    text = str(entry or "").strip()
    if not text:
        return {}
    head, _, tail = text.partition(" — ")
    return {"system": head.strip(), "data": tail.strip()}


def arch_label(entry, fallback: str) -> str:
    node = arch_node(entry)
    return str(node.get("data") or node.get("system") or fallback)


def layer_catalog_names(layer: dict) -> list[str]:
    """The products a stack layer names, by their catalog names.

    `catalog_id` may be one id or a list, and `catalog_ids` is accepted too; the
    catalog supplies the display name so the slide never shows an id.
    """
    raw = layer.get("catalog_ids") or layer.get("catalog_id") or []
    if isinstance(raw, (str, bytes)):
        raw = [raw]
    names = []
    for cid in raw:
        nm = product_name(str(cid)).strip()
        if nm and nm not in names:
            names.append(nm)
    return names


def arch_model(spec: Spec) -> dict:
    """The diagram, derived from the pack brief — boxes and arrows, no drawing.

    Naming rules: the app box is the pack's own name "by SoftServe"; the engine
    box names the products it runs, never the layer's own label; the
    infrastructure layer keeps its line. Flow rules: one labelled arrow per
    input; one labelled arrow out to a destination box holding the outputs; and
    an arrow back to a source only where that same system is also an output.
    """
    stack = spec.get("architecture.stack") or []
    inputs = [arch_node(e) for e in (spec.get("architecture.inputs") or [])]
    inputs = [n for n in inputs if n.get("system") or n.get("name")]
    outputs = [arch_node(e) for e in (spec.get("architecture.outputs") or [])]
    outputs = [n for n in outputs if n.get("system") or n.get("name")]

    app = next((l for l in stack if "app" in str(l.get("layer", "")).lower()), None)
    eng = next((l for l in stack if "engine" in str(l.get("layer", "")).lower()), None)
    infra = next((l for l in stack if "infra" in str(l.get("layer", "")).lower()),
                 stack[-1] if stack else {})

    app_title = f"{spec.name()} by SoftServe"
    app_sub = ""
    if app:
        items = ", ".join(str(i) for i in (app.get("items") or []))
        app_sub = items or str(app.get("summary") or "")

    eng_names = layer_catalog_names(eng or {})
    if not eng_names and eng:
        eng_names = [str(i) for i in (eng.get("items") or []) if str(i).strip()]
    eng_title = " · ".join(eng_names)
    eng_sub = str((eng or {}).get("summary") or (eng or {}).get("layer") or "")

    out_systems = []
    for n in outputs:
        sysname = str(n.get("system") or n.get("name") or "").strip()
        if sysname and sysname not in out_systems:
            out_systems.append(sysname)
    out_data = []
    for n in outputs:
        d = str(n.get("data") or "").strip()
        if d and d not in out_data:
            out_data.append(d)

    # Write-back: a source system that is also a destination gets its own arrow
    # home. Nothing else does — an arrow from the app back to a feed it never
    # writes to is a claim the pack does not make.
    writebacks = []
    for i, n in enumerate(inputs):
        sysname = str(n.get("system") or n.get("name") or "").strip()
        match = next((o for o in outputs
                      if str(o.get("system") or o.get("name") or "").strip().lower()
                      == sysname.lower()), None)
        if match:
            writebacks.append((i, sysname, str(match.get("data") or "the result")))

    return {
        "sources": [{"system": str(n.get("system") or n.get("name") or ""),
                     "data": str(n.get("data") or "")} for n in inputs],
        "app": {"title": app_title, "sub": app_sub},
        "engine": {"title": eng_title, "sub": eng_sub,
                   "layer": str((eng or {}).get("layer") or "")},
        "infrastructure": {
            "title": str(infra.get("layer", "Infrastructure")),
            "sub": ", ".join(str(i) for i in (infra.get("items") or []))
                   or str(infra.get("summary") or "")},
        "destination": {"systems": out_systems, "data": out_data},
        "writebacks": writebacks,
    }


def arch_summary(model: dict) -> list[str]:
    """The diagram in plain words, for the person who has to approve it."""
    out = ["The architecture picture, in words:"]
    if model["sources"]:
        for srcbox in model["sources"]:
            out.append(f"  - a box on the left for {srcbox['system']}")
    else:
        out.append("  - no data sources are named in the pack brief, so the left is empty")
    out.append(f"  - the middle holds {model['app']['title']}"
               + (f" — {model['app']['sub']}" if model["app"]["sub"] else ""))
    if model["engine"]["title"]:
        out.append(f"  - under it, the engine it runs on: {model['engine']['title']}")
    if model["infrastructure"]["title"]:
        out.append(f"  - and the line underneath: {model['infrastructure']['title']}"
                   + (f" — {model['infrastructure']['sub']}"
                      if model["infrastructure"]["sub"] else ""))
    if model["destination"]["systems"]:
        out.append("  - a box on the right for where the result goes: "
                   + " · ".join(model["destination"]["systems"]))
    else:
        out.append("  - nothing is named as the destination for the result, so there "
                   "is no box on the right — say where the result should go")
    out.append("  Arrows:")
    for srcbox in model["sources"]:
        out.append(f"    {srcbox['system']} -> the app"
                   + (f": {srcbox['data']}" if srcbox["data"] else ""))
    if model["destination"]["systems"]:
        out.append("    the app -> " + " · ".join(model["destination"]["systems"])
                   + (": " + " · ".join(model["destination"]["data"])
                      if model["destination"]["data"] else ""))
    for _, sysname, data in model["writebacks"]:
        out.append(f"    the app -> {sysname}: {data}  (written back into the "
                   f"system it came from)")
    return out


def slide_08_architecture(prs, layout, spec: Spec, fit: FitLog, header: str,
                          model: dict | None = None):
    s = new_slide(prs, layout, title=None, header=header)
    style_header(s, header)
    content_title(s, "Architecture", fit, 8,
                  sub=spec.get("deck.architecture_sub")
                  or "Reference architecture for the pack implementation.")
    m = model or arch_model(spec)

    # Three columns across the content band, reading left to right: where the
    # data comes from, what runs, where the result goes. The two gaps are the
    # arrow lanes.
    band_top, band_bot = 2.62, 6.28
    src_x, src_w = MARGIN_L, 2.55
    lane1_x, lane1_w = 3.06, 1.12
    con_x, con_w = 4.18, 5.02
    lane2_x, lane2_w = 9.29, 1.12
    dst_x, dst_w = 10.41, 2.50

    # --- the container: the app, the engine under it, the infrastructure line
    cy, chh = band_top, band_bot - band_top
    rect(s, con_x, cy, con_w, chh, fill=C["white"], line=C["hairline_alt"], line_pt=1.5)
    box_x, box_w = con_x + 0.30, con_w - 0.60
    app_y, eng_y, box_h = cy + 0.40, cy + 1.62, 0.98
    for label, spec_box, fill, fg, y in [
            ("app", m["app"], C["blue"], C["white"], app_y),
            ("engine", m["engine"], C["panel_grey"], C["ink_soft"], eng_y)]:
        if not spec_box["title"]:
            continue
        rect(s, box_x, y, box_w, box_h, fill=fill)
        tpt = autofit_pt(spec_box["title"], box_w - 0.36, 0.42, 14.5, 10.5,
                         bold=True, max_lines=2)
        paras = [{"t": spec_box["title"], "sz": tpt, "b": True, "color": fg,
                  "align": "c"}]
        if spec_box["sub"]:
            paras.append({"t": spec_box["sub"], "sz": 10, "color": fg, "align": "c",
                          "space_before": 2})
        paras = autofit_paras(paras, box_w - 0.36, box_h - 0.14, default_sz=tpt)
        textbox(s, box_x + 0.18, y, box_w - 0.36, box_h, paras, anchor="m")
        log_box(fit, 8, f"{label} box", box_x + 0.18, y, box_w - 0.36,
                box_h - 0.14, paras, tpt)
    infra_paras = [{"t": m["infrastructure"]["title"], "sz": 14, "b": True,
                    "color": C["ink"]}]
    if m["infrastructure"]["sub"]:
        infra_paras.append({"t": m["infrastructure"]["sub"], "sz": 10.5,
                            "color": C["muted"], "space_before": 2})
    infra_paras = autofit_paras(infra_paras, box_w, 0.80, default_sz=14)
    textbox(s, box_x, cy + 2.78, box_w, 0.80, infra_paras)
    log_box(fit, 8, "infrastructure line", box_x, cy + 2.78, box_w, 0.80,
            infra_paras, 14)

    # --- the source boxes, one per input, and their arrows in
    sources = m["sources"][:3]
    n = max(1, len(sources))
    gap = 0.30
    bh = (chh - gap * (n - 1)) / n
    lanes = []                                  # (y of this source's centre)
    for i in range(n):
        srcbox = sources[i] if i < len(sources) else {"system": "", "data": ""}
        y = band_top + i * (bh + gap)
        rect(s, src_x, y, src_w, bh, fill=C["blue"] if srcbox["system"] else C["panel_grey"])
        if not srcbox["system"]:
            textbox(s, src_x + 0.16, y, src_w - 0.32, bh,
                    [{"t": "data source to be named", "sz": 10,
                      "color": C["muted_light"], "align": "c"}], anchor="m")
            lanes.append(y + bh / 2)
            continue
        tpt = autofit_pt(srcbox["system"], src_w - 0.32, bh - 0.20, 13.5, 9.5,
                         bold=True, max_lines=4)
        paras = [{"t": srcbox["system"], "sz": tpt, "b": True, "color": C["white"],
                  "align": "c"}]
        textbox(s, src_x + 0.16, y, src_w - 0.32, bh, paras, anchor="m")
        log_box(fit, 8, f"source box {i+1}", src_x + 0.16, y, src_w - 0.32,
                bh - 0.20, paras, tpt)
        lanes.append(y + bh / 2)

    def arrow_label(x, y, w, text, key, below=False, h=0.44, max_lines=4):
        ly = y + 0.10 if below else y - h - 0.06
        textbox(s, x, ly, w, h,
                [{"t": text, "sz": 8.5, "color": C["muted"], "align": "c"}],
                anchor="t" if below else "b")
        fit.add(8, key, text, 8.5, w, h, max_lines=max_lines)

    wb_index = {i: (sysname, data) for i, sysname, data in m["writebacks"]}
    for i, srcbox in enumerate(sources):
        if not srcbox["system"]:
            continue
        cy_lane = lanes[i]
        # Every input gets its own labelled arrow into the app.
        ay = cy_lane - 0.05 if i in wb_index else cy_lane - 0.055
        arrow(s, lane1_x, ay, lane1_w, 0.11, color=C["blue"])
        arrow_label(lane1_x, ay, lane1_w,
                    srcbox["data"] or "data in", f"arrow in {i+1}",
                    h=max(0.44, min(0.78, bh / 2 - 0.06)), max_lines=6)
        if i in wb_index:
            # ...and one back, only because this system is also a destination.
            _, data = wb_index[i]
            by = cy_lane + 0.42
            arrow(s, lane1_x, by, lane1_w, 0.11, color=C["blue_light"], left=True)
            arrow_label(lane1_x, by + 0.11, lane1_w, data,
                        f"write-back arrow {i+1}", below=True)

    # --- the destination box and the arrow out
    dst = m["destination"]
    dh = 1.70
    dy = max(band_top, app_y + box_h / 2 - dh / 2)   # level with the app box
    if dst["systems"]:
        # Same style as the source boxes: the systems around the pack are one
        # kind of thing, whichever direction the data runs.
        rect(s, dst_x, dy, dst_w, dh, fill=C["blue"])
        text = " · ".join(dst["systems"])
        tpt = autofit_pt(text, dst_w - 0.32, dh - 0.20, 13.5, 9.5, bold=True,
                         max_lines=6)
        paras = [{"t": text, "sz": tpt, "b": True, "color": C["white"], "align": "c"}]
        textbox(s, dst_x + 0.16, dy, dst_w - 0.32, dh, paras, anchor="m")
        log_box(fit, 8, "destination box", dst_x + 0.16, dy, dst_w - 0.32,
                dh - 0.20, paras, tpt)
        ay = app_y + box_h / 2 - 0.055
        arrow(s, lane2_x, ay, lane2_w, 0.11, color=C["blue"])
        arrow_label(lane2_x, ay, lane2_w,
                    " · ".join(dst["data"]) or "the result", "arrow out",
                    h=max(0.44, ay - band_top - 0.08), max_lines=6)
    else:
        slot = rect(s, dst_x, dy, dst_w, dh, fill=C["panel_grey"],
                    line=C["hairline_alt"])
        slot.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        textbox(s, dst_x + 0.16, dy, dst_w - 0.32, dh,
                [{"t": "destination to be named", "sz": 10,
                  "color": C["muted_light"], "align": "c"}], anchor="m")
        fit.note("s8: the pack brief names nothing the result is written to, so the "
                 "box on the right is empty — say which systems receive it")

    tiers = {t.get("id"): t.get("name", "") for t in spec.tiers()}
    notes = []
    for p in (spec.get("oracle_products") or []):
        integ = p.get("integration") or {}
        if integ:
            bits = [f"{tiers.get(k, k)}: {v}" for k, v in integ.items() if v]
            notes.append(f"{product_name(p)} — " + " · ".join(bits))
    if notes:
        footnote(s, "Integration by tier — " + "   |   ".join(notes), fit, 8,
                 y=6.48, sz=8.5)
    return s


# ---------------------------------------------------------------------------
# package tables
# ---------------------------------------------------------------------------

def _glyph(entry: dict, tier_id: str) -> str:
    glyphs = entry.get("glyphs") or {}
    if tier_id in glyphs:
        return str(glyphs[tier_id])
    prose = str(entry.get(tier_id, "") or "").strip()
    if not prose or prose in ("-", "—", "none", "not included"):
        return GLYPH_NONE
    return GLYPH_DEFAULT.get(tier_id, "●")


def _style_table(shape) -> None:
    from pptx.oxml.ns import qn
    tbl = shape.table
    tbl.first_row = False
    tbl.horz_banding = False
    tblPr = shape._element.graphic.graphicData.tbl.find(qn("a:tblPr"))
    if tblPr is not None:
        for child in list(tblPr):
            if child.tag == qn("a:tableStyleId"):
                tblPr.remove(child)
        el = tblPr.makeelement(qn("a:tableStyleId"), {})
        el.text = NO_STYLE
        tblPr.append(el)


def _set_sym(run, typeface: str) -> None:
    """Name the symbol face on the run, the .pptx counterpart of Word's altName.

    `a:latin` carries Apple Symbols; `a:sym` names the face a Windows renderer
    should reach for, so the three status glyphs still come from ONE face there.
    """
    from pptx.oxml.ns import qn
    rPr = run._r.get_or_add_rPr()
    for tag in (qn("a:sym"),):
        for el in rPr.findall(tag):
            rPr.remove(el)
    el = rPr.makeelement(qn("a:sym"), {"typeface": typeface})
    rPr.append(el)


def cell_text(value) -> str:
    """A cell is a string, or a (glyph, prose) pair set in two faces."""
    if isinstance(value, tuple):
        return "  ".join(x for x in value if x)
    return str(value or "")


def _cell(cell, text, sz, bold=False, color=C["ink"], fill=C["white"],
          align="l", font=FONT_BODY, sym=None):
    from pptx.enum.text import PP_ALIGN
    cell.fill.solid()
    cell.fill.fore_color.rgb = RGBColor.from_string(fill)
    cell.margin_left = cell.margin_right = Emu(109728)
    cell.margin_top = cell.margin_bottom = Emu(45720)
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf = cell.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER,
                   "r": PP_ALIGN.RIGHT}[align]
    # (glyph, prose) → two runs, the glyph in the symbol face; everything else is
    # one run. Either way every run names its face and its size explicitly.
    parts = ([(text[0], font, sym)] + ([(text[1], FONT_BODY, None)] if text[1] else [])
             if isinstance(text, tuple)
             else [(str(text), font, sym)])
    first = True
    for body, face, symface in parts:
        r = p.add_run()
        r.text = ("" if first else "  ") + str(body)
        first = False
        r.font.size = Pt(sz)
        r.font.bold = bold
        r.font.name = face
        r.font.color.rgb = RGBColor.from_string(color)
        if symface:
            _set_sym(r, symface)


def _package_rows(spec: Spec, detailed: bool, with_infra: bool):
    tiers = spec.tiers()
    rows: list[tuple[str, list[str], dict]] = []
    rows.append(("", [spec.tier_label(t) for t in tiers], {"header": True}))
    rows.append(("Package scope",
                 [str(t.get("scope_line") or (t.get("what_you_get") or [""])[0] or "")
                  for t in tiers],
                 {"sz": 10.5 if detailed else 11.0, "bold": True}))
    if not detailed:
        svc, foot_s = [], False
        for t in tiers:
            v, f = fmt_price(t.get("services_price"))
            svc.append(v + ("*" if f else ""))
            foot_s = foot_s or f
        rows.append(("Services price (one-time)", svc, {"sz": 11.5, "bold": True,
                                                        "align": "l"}))
        if with_infra:
            infra = []
            for t in tiers:
                v, f = fmt_price(t.get("infra_price_monthly"))
                infra.append(v + ("*" if f else ""))
            rows.append(("Infrastructure (monthly, consumption-based)", infra,
                         {"sz": 11.5, "bold": True}))
        rows.append(("Timeline", [fmt_duration(t.get("duration_weeks")) for t in tiers],
                     {"sz": 11.0, "bold": True}))
    handling = spec.get("packages.capability_handling") or []
    for entry in handling:
        area = str(entry.get("area", ""))
        if detailed:
            cells = []
            for t in tiers:
                tid = t.get("id")
                prose = str(entry.get(tid, "") or "").strip()
                g = _glyph(entry, tid)
                # (glyph, prose): the glyph is set in the symbol face, the prose
                # in the body face, so the three status marks stay one size.
                cells.append((g, "" if g == GLYPH_NONE else prose))
            rows.append((area, cells, {"sz": 10.5, "bold": False, "align": "l",
                                       "glyph_prose": True}))
        else:
            rows.append((area, [_glyph(entry, t.get("id")) for t in tiers],
                         {"sz": 18.0, "bold": True, "align": "c", "glyph": True,
                          "label_sz": 11.0}))
    return rows


def _build_table(s, spec: Spec, fit: FitLog, slide_no: int, detailed: bool,
                 with_infra: bool, top: float, bottom: float):
    rows = _package_rows(spec, detailed, with_infra)
    ncol = 1 + len(spec.tiers())
    colw = [2.55] + [(CONTENT_W - 2.55) / (ncol - 1)] * (ncol - 1) if detailed \
        else [2.92] + [(12.36 - 2.92) / (ncol - 1)] * (ncol - 1)
    total_w = sum(colw)
    band = bottom - top

    floor = TABLE_FLOOR.get(slide_no, 10.0)

    def row_size(opt: dict, scale: float, label_col: bool = False) -> float:
        """Point size for a cell, never below the slide's floor.

        The glyphs are the exception: they are a pictogram at 18 pt, and shrinking
        them is not a legibility problem. Everything the reader has to read stops
        at the floor, and the table reports rather than going smaller.
        """
        if opt.get("header"):
            base = 12.5
        elif label_col:
            base = opt.get("label_sz", opt.get("sz", 10.0))
        else:
            base = opt.get("sz", 10.0)
        scaled = base * scale
        if opt.get("glyph") and not label_col:
            return max(scaled, floor)
        return max(scaled, floor)

    def measure(scale: float) -> list[float]:
        heights = []
        for label, cells, opt in rows:
            need = 0.26
            for ci, txt in enumerate([label] + list(cells)):
                body = cell_text(txt)
                if not body:
                    continue
                w = colw[ci] - 0.26
                csz = row_size(opt, scale, label_col=(ci == 0))
                lines = wrap_count(body, csz, w, bool(opt.get("bold")))
                need = max(need, lines * csz * 1.22 / 72.0 + 0.13)
            heights.append(max(0.33, need))
        return heights

    # Shrink only until the floor bites; below that the wording is what gives.
    scale = 1.0
    heights = measure(scale)
    while sum(heights) > band and scale > 0.70:
        nxt = round(scale - 0.04, 2)
        if measure(nxt) == heights:          # every size is already on the floor
            break
        scale = nxt
        heights = measure(scale)
    if sum(heights) > band:
        fit.note(f"s{slide_no}: the packages table needs {sum(heights):.2f} in of the "
                 f"{band:.2f} in it has, with the type already at its smallest "
                 f"readable size — shorten the wording or drop a row")
        fit.entries.append(FitEntry(
            slide_no, "packages table", "(whole table)", floor, False,
            total_w, band, need_h=sum(heights), lines=len(rows)))
    elif sum(heights) < band - 0.02:
        # Rule 1: a table half the height of its band is a half-empty slide. The
        # type stays at or above the floor and the rows grow into the band.
        grow = band / sum(heights)
        heights = [h * min(grow, 1.9) for h in heights]

    # Word budget on the detailed table: a cell a seller reads out loud, not a
    # paragraph. Over budget is an overflow the wording fixes, never the type.
    if detailed:
        for ri, (label, cells, opt) in enumerate(rows):
            if opt.get("header"):
                continue
            for ci, txt in enumerate(cells):
                # the status mark is not a word the reader reads
                body = (txt[1] if isinstance(txt, tuple) else cell_text(txt)).strip()
                words = len(body.split())
                if words > DETAILED_CELL_WORDS:
                    fit.entries.append(FitEntry(
                        slide_no, f"cell «{label[:24]}», column {ci + 1}",
                        f"{words} words, more than the {DETAILED_CELL_WORDS} a cell "
                        f"on this table carries: {body}",
                        row_size(opt, scale), False, colw[ci + 1] - 0.26,
                        heights[ri], need_h=heights[ri] * 2, lines=words))

    shape = s.shapes.add_table(len(rows), ncol, inch(MARGIN_L), inch(top),
                               inch(total_w), inch(sum(heights)))
    _style_table(shape)
    tbl = shape.table
    for ci, w in enumerate(colw):
        tbl.columns[ci].width = Emu(inch(w))
    for ri, ((label, cells, opt), h) in enumerate(zip(rows, heights)):
        tbl.rows[ri].height = Emu(inch(h))
        sz = row_size(opt, scale)
        if opt.get("header"):
            _cell(tbl.cell(ri, 0), "", sz, fill=C["ink"])
            for ci, txt in enumerate(cells):
                _cell(tbl.cell(ri, ci + 1), txt, sz, bold=True, color=C["white"],
                      fill=TIER_HEADER_FILL[min(ci, len(TIER_HEADER_FILL) - 1)],
                      align="c")
            continue
        _cell(tbl.cell(ri, 0), label, row_size(opt, scale, label_col=True),
              bold=True, color=C["ink"], fill=C["white"])
        symbolic = bool(opt.get("glyph") or opt.get("glyph_prose"))
        for ci, txt in enumerate(cells):
            _cell(tbl.cell(ri, ci + 1), txt, sz,
                  bold=bool(opt.get("bold")),
                  color=C["ink"] if cell_text(txt) != GLYPH_NONE else C["muted_light"],
                  fill=C["white"], align=opt.get("align", "l"),
                  font=SYMBOL_FONT if symbolic else FONT_BODY,
                  sym=SYMBOL_ALT if symbolic else None)
    return sum(heights), scale


def glyph_legend(slide, y, fit, slide_no, tail: str = "", sz: float = 8.5):
    """The status key. The three marks come from the symbol face, like the cells."""
    g = {"font": SYMBOL_FONT, "color": C["muted_light"], "sz": sz}
    parts = [("◐", g), (" partial   ", {}), ("●", g), (" included   ", {}),
             ("●●", g), (" multi-region / advanced   ", {}),
             (GLYPH_NONE, g), (" not in this tier", {})]
    if tail:
        parts.append(("   " + tail, {}))
    textbox(slide, MARGIN_L, y, CONTENT_W, 0.30,
            [{"t": parts, "sz": sz, "color": C["muted_light"]}])
    fit.add(slide_no, "status key", "".join(t for t, _ in parts), sz,
            CONTENT_W, 0.30, max_lines=2)


def slide_09_packages(prs, layout, spec: Spec, fit: FitLog, header: str):
    s = new_slide(prs, layout, title=None, header=header)
    style_header(s, header)
    content_title(s, "Service packages", fit, 9)
    used, scale = _build_table(s, spec, fit, 9, detailed=False, with_infra=True,
                               top=1.98, bottom=6.58)
    star = any(fmt_price(t.get("services_price"))[1]
               or fmt_price(t.get("infra_price_monthly"))[1] for t in spec.tiers())
    note = "* Indicative; depends on usage and rule-set complexity." if star else ""
    glyph_legend(s, 6.66, fit, 9, tail=note)
    return s


def slide_10_packages_detailed(prs, layout, spec: Spec, fit: FitLog, header: str):
    s = new_slide(prs, layout, title=None, header=header)
    style_header(s, header)
    content_title(s, "Service packages (detailed)", fit, 10)
    used, scale = _build_table(s, spec, fit, 10, detailed=True, with_infra=False,
                               top=2.05, bottom=6.62)
    glyph_legend(s, 6.70, fit, 10)
    return s


# ---------------------------------------------------------------------------

BUILDERS = [
    ("cover", slide_01_cover),
    ("use case", slide_02_use_case),
    ("verticals", slide_03_verticals),
    ("today / tomorrow", slide_04_today_tomorrow),
    ("proof", slide_05_proof),
    ("why it sells", slide_06_why_it_sells),
    ("solution layers", slide_07_solution_layers),
    ("architecture", slide_08_architecture),
    ("service packages", slide_09_packages),
    ("service packages (detailed)", slide_10_packages_detailed),
]


def build(spec: Spec, base: Path, out_dir: Path, fit: FitLog,
          stamp: str | None = None) -> tuple[Path, dict, str]:
    prs = open_base(base)
    layout = pick_layout(prs, "ShortTitle-Empty", "Title-1Column")
    header_tpl = spec.get("deck.running_header") or DEFAULT_HEADER
    header = header_tpl.format(name=spec.name())
    model = arch_model(spec)
    for i, (label, fn) in enumerate(BUILDERS, 1):
        try:
            if i == 1:
                fn(prs, layout, spec, fit)
            elif i == 8:
                fn(prs, layout, spec, fit, header, model)
            else:
                fn(prs, layout, spec, fit, header)
        except SpecError:
            raise
        except Exception as exc:  # keep a partial deck rather than nothing
            fit.note(f"s{i} ({label}) failed: {exc.__class__.__name__}: {exc}")
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = spec.get("meta.slug", "pack")
    out = out_dir / f"{slug}-sales-deck.pptx"
    if stamp:
        prs.core_properties.identifier = stamp      # which spec this file reflects (CON006 / CON007)
    prs.save(str(out))
    return out, model, header


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Build the 10-slide accelerator-pack sales deck from a pack spec.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Done means: fit report clean, contact sheet reviewed (see "
               "tools/render_probe.sh), linter clean.")
    ap.add_argument("spec", help="path to pack-spec.yaml")
    ap.add_argument("--out", required=True, help="output directory")
    ap.add_argument("--channel", default="partner_print",
                    choices=["partner_print", "internal"],
                    help="who the deck is for; drives naming, clearance and contact")
    ap.add_argument("--base", default=str(BASE_DEFAULT),
                    help="SoftServe deck base .pptx (default: the skill's asset)")
    ap.add_argument("--fit-report", action="store_true",
                    help="print the per-box text-fit estimate for every box")
    ap.add_argument("--allow-overflow", action="store_true",
                    help="exit 0 even when boxes overflow (review builds only)")
    args = ap.parse_args(argv)

    try:
        spec = Spec.load(args.spec, channel=args.channel)
    except SpecError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    spec.spec_dir = Path(args.spec).resolve().parent   # picture paths hang off it
    fit = FitLog()
    built_from = spec_stamp.stamp(args.spec)
    try:
        out, model, header = build(spec, Path(args.base), Path(args.out), fit, stamp=built_from)
    except SpecError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(f"built {out}  ({len(BUILDERS)} slides, channel={args.channel})")
    print(f"spec stamp: {built_from}")
    print(f"running header on slides 2-10: {header}")
    print(fit.report(verbose=args.fit_report))
    print("")
    for line in arch_summary(model):
        print(line)
    bad = fit.problems()
    if bad and not args.allow_overflow:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
