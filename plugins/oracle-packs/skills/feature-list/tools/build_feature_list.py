#!/usr/bin/env python3
"""Build the Oracle accelerator-pack feature list (.docx) from a pack spec.

Rebuilds the anatomy of the Workforce Optimization feature list (2026-09-10): a kicker, an H1
with a rule under it, a one-line application definition, a glyph legend, and one fixed-layout
table of Area > Category > Feature with the current status and the standard customization scope.
Area and Category cells are merged down across their feature rows, as in the reference.

Two deliberate departures from the reference document, both from Alex's decisions of 2026-09-18:
  * status uses three distinct glyphs -- (*) available / (-) partial / (o) roadmap, drawn as
    U+25CF / U+25D0 / U+25CB -- instead of the reference's two same-glyph-different-colour
    statuses, which cannot be told apart in print or by a screen reader;
  * an optional `Tier first available` column reports `tier_first_available` per feature, so the
    tier a capability arrives in is stated next to the capability instead of only in the deck.

The feature list carries NO pricing (confirmed on both of Vlad's feature lists); the build
refuses to write a document in which a tier price has leaked in.

Usage
    build_feature_list.py <pack-spec.yaml> --out <dir> [--tier-column] [--no-tier-column]

Exit codes
    0  written
    1  usage / spec error
    2  a pricing figure reached the page, which the feature list must never carry

Dependencies: pyyaml, python-docx (see plugins/oracle-packs/requirements.txt).
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("build_feature_list: pyyaml is required -- pip install -r plugins/oracle-packs/requirements.txt")
try:
    from docx import Document
    from docx.enum.section import WD_ORIENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.shared import Mm, Pt, RGBColor, Twips
except ImportError:  # pragma: no cover
    sys.exit("build_feature_list: python-docx is required -- pip install -r plugins/oracle-packs/requirements.txt")

# --- brand tokens, read off the reference document -------------------------
ACCENT = "1485C3"        # SoftServe blue: kicker, H1 rule, Area fill, available glyph
INK = "26282B"           # header row fill
CATEGORY_FILL = "EDF0F2"
WHITE = "FFFFFF"
MUTED = "6B7076"         # kicker separator, footer
ROADMAP = "AEB4BA"       # roadmap glyph
BORDER = "D9D9D9"

GLYPHS = {                       # status -> (glyph, colour, legend wording)
    "available": ("●", ACCENT, "available: provided out of the box, configuration may be required"),
    "partial": ("◐", ACCENT, "partial: partially implemented, major improvements on the roadmap"),
    "roadmap": ("○", ROADMAP, "roadmap: planned, not implemented today"),
}
STATUS_ALIASES = {"ootb": "available", "yes": "available", "ga": "available",
                  "in_progress": "partial", "partially_available": "partial",
                  "planned": "roadmap", "no": "roadmap"}

# column widths in dxa (twips). The reference is 5 columns totalling 10250 dxa (7.12in) on A4
# with 0.51in side margins; the 6-column variant keeps the same total.
WIDTHS_5 = [1077, 1978, 3420, 1350, 2425]
WIDTHS_6 = [1000, 1800, 3000, 1150, 1150, 2150]
HEADERS_5 = ["Area", "Category", "Features", "Current status", "Standard customization scope"]
HEADERS_6 = ["Area", "Category", "Features", "Current status", "Tier first available",
             "Standard customization scope"]

TIER_LABELS = {"pov": "PoV Jumpstart", "integration": "Integration", "scaling": "Scaling"}


class SpecError(Exception):
    """A required value is missing or unusable -- send the user back to /oracle-packs:spec."""


# --- low-level docx helpers -------------------------------------------------
def _el(parent, tag, **attrs):
    """Get or create a child element, setting w: attributes."""
    found = parent.find(qn(tag))
    if found is None:
        found = parent.makeelement(qn(tag), {})
        parent.append(found)
    for key, value in attrs.items():
        found.set(qn("w:" + key), str(value))
    return found


def shade(cell, fill):
    _el(cell._tc.get_or_add_tcPr(), "w:shd", val="clear", color="auto", fill=fill)


def valign(cell, value="center"):
    _el(cell._tc.get_or_add_tcPr(), "w:vAlign", val=value)


def cell_margins(cell, top=16, left=80, bottom=16, right=65):
    mar = _el(cell._tc.get_or_add_tcPr(), "w:tcMar")
    for tag, width in (("w:top", top), ("w:left", left), ("w:bottom", bottom), ("w:right", right)):
        _el(mar, tag, w=width, type="dxa")


def vmerge(cell, restart: bool):
    tc_pr = cell._tc.get_or_add_tcPr()
    if restart:
        _el(tc_pr, "w:vMerge", val="restart")
    else:
        merge = tc_pr.find(qn("w:vMerge"))
        if merge is None:
            merge = tc_pr.makeelement(qn("w:vMerge"), {})
            tc_pr.append(merge)


def row_properties(row, height=300, keep_together=True):
    tr_pr = row._tr.get_or_add_trPr()
    if keep_together:
        _el(tr_pr, "w:cantSplit")
    _el(tr_pr, "w:trHeight", val=height)


def repeat_header(row):
    _el(row._tr.get_or_add_trPr(), "w:tblHeader")


def table_borders(table, colour=BORDER, size=4):
    borders = _el(table._tbl.tblPr, "w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        _el(borders, "w:" + edge, val="single", sz=size, space=0, color=colour)


def fixed_layout(table, widths):
    _el(table._tbl.tblPr, "w:tblLayout", type="fixed")
    _el(table._tbl.tblPr, "w:tblW", w=sum(widths), type="dxa")
    margins = _el(table._tbl.tblPr, "w:tblCellMar")
    _el(margins, "w:left", w=10, type="dxa")
    _el(margins, "w:right", w=10, type="dxa")
    grid = table._tbl.find(qn("w:tblGrid"))
    for column, width in zip(grid, widths):
        column.set(qn("w:w"), str(width))
    for row in table.rows:                     # Word honours tcW, not only the grid
        for cell, width in zip(row.cells, widths):
            cell.width = Twips(width)


def write(cell, runs, *, align=None, size=Pt(7.5), space_before=0, space_after=0, line=None):
    """Replace a cell's content with one paragraph built from (text, bold, colour, size) runs."""
    paragraph = cell.paragraphs[0]
    for existing in list(paragraph.runs):
        existing._r.getparent().remove(existing._r)
    if align is not None:
        paragraph.alignment = align
    paragraph.paragraph_format.space_before = space_before
    paragraph.paragraph_format.space_after = space_after
    if line is not None:
        paragraph.paragraph_format.line_spacing = line
    for text, bold, colour, run_size in runs:
        run = paragraph.add_run(text)
        run.bold = bold
        run.font.size = run_size or size
        if colour:
            run.font.color.rgb = RGBColor.from_string(colour)
    return paragraph


def bullets(cell, items, size=Pt(7.5)):
    """A cell holding a short bulleted list, like the reference's customization-scope cells."""
    cell.text = ""
    first = True
    for item in items:
        paragraph = cell.paragraphs[0] if first else cell.add_paragraph()
        first = False
        paragraph.style = cell.part.document.styles["List Bullet"]
        paragraph.paragraph_format.left_indent = Twips(159)
        paragraph.paragraph_format.space_before = 0
        paragraph.paragraph_format.space_after = 0
        run = paragraph.add_run(str(item))
        run.font.size = size


# --- spec helpers -----------------------------------------------------------
def dig(spec, path, default=None):
    node = spec
    for part in path.split("."):
        if not isinstance(node, dict) or part not in node:
            return default
        node = node[part]
    return node if node is not None else default


def need(spec, path):
    value = dig(spec, path)
    if value in (None, "", [], {}):
        raise SpecError(f"pack spec is missing `{path}` -- confirm it in /oracle-packs:spec before building")
    return value


def status_of(feature):
    raw = str(feature.get("status", "")).strip().lower().replace("-", "_").replace(" ", "_")
    key = STATUS_ALIASES.get(raw, raw)
    if key not in GLYPHS:
        raise SpecError(
            f"capability {feature.get('name', '?')!r} has status {feature.get('status')!r}; "
            f"use one of: {', '.join(GLYPHS)}")
    return key


def scope_items(value):
    if value in (None, "", [], {}):
        return []
    return [str(v) for v in value] if isinstance(value, list) else [str(value)]


def runs_of(rows):
    """Group consecutive equal values: [(value, start, length), ...] -- how cells get merged."""
    groups = []
    for index, value in enumerate(rows):
        if groups and groups[-1][0] == value:
            groups[-1][2] += 1
        else:
            groups.append([value, index, 1])
    return groups


# --- document assembly ------------------------------------------------------
def flatten(spec):
    """capabilities[] -> a flat row list plus the per-row grouping keys."""
    rows = []
    for area in need(spec, "capabilities"):
        area_name = area.get("area", "")
        area_scope = scope_items(area.get("customization_scope_area"))
        for category in area.get("categories") or []:
            category_name = category.get("name", "")
            for feature in category.get("features") or []:
                rows.append({
                    "area": area_name,
                    "area_scope": area_scope,
                    "category": category_name,
                    "feature": feature.get("name", ""),
                    "note": feature.get("note"),
                    "status": status_of(feature),
                    "tier": feature.get("tier_first_available"),
                    "scope": scope_items(feature.get("customization_scope")) or area_scope,
                })
    if not rows:
        raise SpecError("pack spec has no capabilities[].categories[].features[] to list")
    return rows


def build(spec, tier_column: bool) -> tuple[Document, str]:
    rows = flatten(spec)
    headers = HEADERS_6 if tier_column else HEADERS_5
    widths = WIDTHS_6 if tier_column else WIDTHS_5

    document = Document()
    normal = document.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(7.5)
    # python-docx starts from Word's default template, whose Normal style carries 8pt space-after
    # and 1.08 line spacing. Left in place it doubles every table row's height.
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(0)
    normal.paragraph_format.line_spacing = 1.0
    r_fonts = normal.element.rPr.rFonts
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        r_fonts.set(qn(attr), "Arial")

    section = document.sections[0]
    section.orientation = WD_ORIENT.PORTRAIT
    section.page_width, section.page_height = Mm(210), Mm(297)
    section.left_margin = section.right_margin = Mm(13.1)     # 0.514in, as measured
    section.top_margin, section.bottom_margin = Mm(10.0), Mm(7.4)

    # --- kicker
    kicker = document.add_paragraph()
    kicker.paragraph_format.space_after = Pt(1)
    kicker.paragraph_format.line_spacing = 1.15
    left = kicker.add_run(dig(spec, "feature_list.kicker", "SOFTSERVE × ORACLE"))
    left.bold, left.font.size = True, Pt(8)
    left.font.color.rgb = RGBColor.from_string(ACCENT)
    tail = kicker.add_run("   ·   " + dig(spec, "meta.eyebrow", "OCI AI ACCELERATORS").upper())
    tail.font.size = Pt(8)
    tail.font.color.rgb = RGBColor.from_string(MUTED)

    # --- H1 + the blue rule under it
    title_text = dig(spec, "feature_list.title") or f"{need(spec, 'meta.name')} — Feature list"
    title = document.add_paragraph()
    title.paragraph_format.space_after = Pt(3.1)
    title.paragraph_format.line_spacing = 1.15
    rule = _el(title._p.get_or_add_pPr(), "w:pBdr")
    _el(rule, "w:bottom", val="single", sz=12, space=4, color=ACCENT)
    run = title.add_run(title_text)
    run.bold, run.font.size = True, Pt(16)

    # --- the one-line application definition
    intro = document.add_paragraph()
    intro.paragraph_format.space_before = Pt(3)
    intro.paragraph_format.space_after = Pt(2.1)
    intro.paragraph_format.line_spacing = 1.15
    label = intro.add_run(dig(spec, "feature_list.intro_label", "App.") + "  ")
    label.bold, label.font.size = True, Pt(8)
    label.font.color.rgb = RGBColor.from_string(ACCENT)
    body = intro.add_run(dig(spec, "feature_list.intro") or need(spec, "one_liner.full"))
    body.font.size = Pt(8)

    # --- the table
    table = document.add_table(rows=1, cols=len(headers))
    table_borders(table)
    _el(table._tbl.tblPr, "w:tblLook", val="04A0", firstRow=1, lastRow=0,
        firstColumn=1, lastColumn=0, noHBand=0, noVBand=1)
    header_row = table.rows[0]
    row_properties(header_row)
    repeat_header(header_row)
    for cell, text in zip(header_row.cells, headers):
        shade(cell, INK)
        valign(cell)
        cell_margins(cell)
        write(cell, [(text, True, WHITE, None)])

    notes, note_marks = [], {}
    for entry in rows:
        if entry["note"]:
            note_marks[entry["feature"]] = "*" * (len(notes) + 1)
            notes.append((note_marks[entry["feature"]], entry["feature"], entry["note"]))

    body_rows = []
    for entry in rows:
        row = table.add_row()
        row_properties(row)
        body_rows.append(row)
        cells = row.cells
        for cell in cells:
            valign(cell)
            cell_margins(cell)
            shade(cell, WHITE)
        mark = note_marks.get(entry["feature"], "")
        write(cells[2], [(entry["feature"] + mark, False, None, None)])
        glyph, colour, _ = GLYPHS[entry["status"]]
        write(cells[3], [(glyph, False, colour, Pt(10))], align=WD_ALIGN_PARAGRAPH.CENTER, line=1.05)
        if tier_column:
            label_text = TIER_LABELS.get(str(entry["tier"]), str(entry["tier"] or "–"))
            write(cells[4], [(label_text, False, MUTED, None)], align=WD_ALIGN_PARAGRAPH.CENTER)

    # --- merge the grouping columns down, exactly as the reference does
    scope_col = 5 if tier_column else 4
    merge_plan = [
        (0, [r["area"] for r in rows], ACCENT, WHITE, True),
        (1, [(r["area"], r["category"]) for r in rows], CATEGORY_FILL, None, False),
        (3, [(r["area"], r["category"], r["status"]) for r in rows], WHITE, None, None),
    ]
    if tier_column:
        merge_plan.append((4, [(r["area"], r["category"], r["tier"]) for r in rows], WHITE, None, None))
    merge_plan.append((scope_col, [(r["area"], tuple(r["scope"])) for r in rows], WHITE, None, None))

    for column, keys, fill, colour, bold in merge_plan:
        for value, start, length in runs_of(keys):
            first = body_rows[start].cells[column]
            shade(first, fill)
            if column == 0:
                write(first, [(rows[start]["area"], True, WHITE, None)], align=WD_ALIGN_PARAGRAPH.CENTER)
            elif column == 1:
                write(first, [(rows[start]["category"], bold, colour, None)])
            elif column == scope_col:
                bullets(first, rows[start]["scope"])
            if length > 1:
                vmerge(first, restart=True)
                for offset in range(1, length):
                    following = body_rows[start + offset].cells[column]
                    following.text = ""
                    # continuation cells carry the group's fill too: Word paints the merged span
                    # from the restart cell, but lighter renderers (QuickLook, some viewers) do
                    # not, and an unshaded continuation breaks the column visually.
                    shade(following, fill)
                    vmerge(following, restart=False)
    fixed_layout(table, widths)

    # --- legend, then any feature footnotes
    legend_head = document.add_paragraph()
    legend_head.paragraph_format.space_before = Pt(4.2)
    legend_head.paragraph_format.space_after = Pt(0.8)
    head_run = legend_head.add_run("Current status")
    head_run.bold, head_run.font.size = True, Pt(7)
    head_run.font.color.rgb = RGBColor.from_string(MUTED)
    for key in ("available", "partial", "roadmap"):
        glyph, colour, wording = GLYPHS[key]
        line = document.add_paragraph()
        line.paragraph_format.space_before = Pt(0)
        line.paragraph_format.space_after = Pt(0.8)
        line.paragraph_format.line_spacing = 1.0
        mark = line.add_run(glyph)
        mark.font.size = Pt(9)
        mark.font.color.rgb = RGBColor.from_string(colour)
        rest = line.add_run("  –  " + wording)
        rest.font.size = Pt(7)
    for mark, feature, text in notes:
        line = document.add_paragraph()
        line.paragraph_format.space_before = Pt(0)
        line.paragraph_format.space_after = Pt(0.8)
        run = line.add_run(f"{mark}  {feature}: {text}")
        run.font.size = Pt(7)
        run.font.color.rgb = RGBColor.from_string(MUTED)

    # --- footer: generated date and spec version, so a printed copy is traceable
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    stamp = footer.add_run(
        f"{dig(spec, 'meta.name', 'Pack')} · feature list · "
        f"spec v{dig(spec, 'meta.spec_version', '?')} · "
        f"generated {dt.date.today().isoformat()}")
    stamp.font.size = Pt(6.5)
    stamp.font.color.rgb = RGBColor.from_string(MUTED)

    return document, title_text


def pricing_leak(document, spec):
    """The feature list never carries pricing. Return the offending strings, if any."""
    text = "\n".join(p.text for p in document.paragraphs)
    for table in document.tables:
        for row in table.rows:
            text += "\n" + "\n".join(cell.text for cell in row.cells)
    hits = set(re.findall(r"[€$£]\s?\d[\d.,]*\s?[KkMm]?", text))
    for tier in dig(spec, "packages.tiers") or []:
        for key in ("services_price", "infra_price_monthly"):
            block = tier.get(key)
            if isinstance(block, dict):
                for value in ([block.get("value")] + list(block.get("range") or [])):
                    if value and re.search(rf"\b{re.escape(str(value))}\b", text):
                        hits.add(str(value))
    return sorted(hits)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="build_feature_list.py",
        description="Build the feature list (.docx) from a pack spec: Area > Category > Feature.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Exit codes: 0 written | 1 spec error | 2 pricing leaked into the feature list.",
    )
    parser.add_argument("spec", type=Path, help="path to packs/<slug>/pack-spec.yaml")
    parser.add_argument("--out", type=Path, required=True, help="output directory (created if missing)")
    tier = parser.add_mutually_exclusive_group()
    tier.add_argument("--tier-column", dest="tier_column", action="store_true", default=None,
                      help="add the 'Tier first available' column (default: on when every feature has one)")
    tier.add_argument("--no-tier-column", dest="tier_column", action="store_false",
                      help="force the 5-column reference layout")
    args = parser.parse_args(argv)

    if not args.spec.exists():
        print(f"build_feature_list: no such spec: {args.spec}", file=sys.stderr)
        return 1
    spec = yaml.safe_load(args.spec.read_text(encoding="utf-8")) or {}

    try:
        rows = flatten(spec)
        tier_column = args.tier_column
        if tier_column is None:
            tier_column = all(r["tier"] for r in rows)
        document, title = build(spec, tier_column)
    except SpecError as err:
        print(f"build_feature_list: {err}", file=sys.stderr)
        return 1

    leaks = pricing_leak(document, spec)
    if leaks:
        print(f"build_feature_list: PRICING -- {', '.join(leaks)} reached the feature list. "
              f"Pricing belongs on the one-pager and the deck, never here.", file=sys.stderr)
        return 2

    args.out.mkdir(parents=True, exist_ok=True)
    path = args.out / f"{dig(spec, 'meta.slug', 'pack')}-feature-list.docx"
    document.save(str(path))
    areas = len({r["area"] for r in rows})
    categories = len({(r["area"], r["category"]) for r in rows})
    counts = {k: sum(1 for r in rows if r["status"] == k) for k in GLYPHS}
    print(f"DOCX  {path}")
    print(f"      {title}")
    print(f"      {areas} areas / {categories} categories / {len(rows)} features, "
          f"{len(HEADERS_6 if tier_column else HEADERS_5)} columns")
    print(f"      status: {counts['available']} available, {counts['partial']} partial, "
          f"{counts['roadmap']} roadmap")
    return 0


if __name__ == "__main__":
    sys.exit(main())
