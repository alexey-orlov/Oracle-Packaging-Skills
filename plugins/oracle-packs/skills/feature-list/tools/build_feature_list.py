#!/usr/bin/env python3
"""Build the Oracle accelerator-pack feature list (.docx) from a pack spec.

The document follows the practice mini-site: the SoftServe wordmark lockup with
"Oracle AI & Data Solutions", the site's faces (Azurio for the title, Replica LL TT for
everything else), its hairlines and greys, the approved one-liner and one sentence saying
who the pack is for, then one fixed-layout table of Area > Category > Feature with the
current status and the standard customization scope. Area and Category cells merge down
across their rows.

**The feature list is one A4 page.** That is a requirement (the owner, 2026-09-22), so the
build estimates the document's height before writing it and walks a fit ladder until the
estimate fits: one row per feature at 7.5pt, the same at 7pt, then compact mode (one row
per category, features listed inline, the status and tier columns dropped) at 7.5 and 7pt.
If nothing fits, it writes nothing and exits 3 with a report of what has to be grouped —
the capability tree is too fine, and the fix belongs in the spec, not in the type size.

Statuses use three distinct glyphs -- (*) available / (-) partial / (o) roadmap, drawn as
U+25CF / U+25D0 / U+25CB (the owner, 2026-09-18) -- because colour alone cannot be read in
greyscale print or by a screen reader. All three are set in one symbol face, so they come out
the same size instead of one substituted face per glyph. An optional `Tier first available`
column reports `tier_first_available` per feature.

There is no page footer (the owner, 2026-09-22): the spec version and the build date go into
the file's own properties, and the spec stamp (shared/tools/spec_stamp.py: the spec's sha and
commit) into its identifier, so the file says which spec it was built from. Footnotes carry
the caveat alone, and the build says so when there are more than three of them or one runs long.

The feature list carries NO pricing; the build refuses to write a document in which a tier
price has leaked in.

Usage
    build_feature_list.py <pack-spec.md> --out <dir>
        [--tier-column | --no-tier-column] [--fit one-page|none]
        [--check-pages | --no-check-pages]

Exit codes
    0  written
    1  usage / spec error
    2  a pricing figure reached the page, which the feature list must never carry
    3  the capability tree does not fit one A4 page even in compact mode at 7pt

The real page count is verified by exporting the written file to PDF -- Pages.app on macOS,
else LibreOffice headless (`soffice`) -- and the report names the renderer that did it. With
neither installed the report carries a `WARNING: page count NOT verified` line; the exit code
does not change.

Dependencies: pyyaml, python-docx (see plugins/oracle-packs/requirements.txt); pypdf to count
LibreOffice's pages. Pillow is optional and only makes the height estimate exact; without it the
build falls back to an average glyph width and says so on stderr. The brand faces are read from
the plugin's own `fonts/` folder first, then from the installed font folders.
"""

from __future__ import annotations

import argparse
import datetime as dt
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
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
    from docx.shared import Inches, Mm, Pt, RGBColor, Twips
except ImportError:  # pragma: no cover
    sys.exit("build_feature_list: python-docx is required -- pip install -r plugins/oracle-packs/requirements.txt")

HERE = Path(__file__).resolve().parent
for _up in range(2, 6):                     # the spec stamp: the plugin's shared/tools
    _shared = HERE.parents[_up] / "shared" / "tools" if len(HERE.parents) > _up else None
    if _shared is not None and (_shared / "spec_stamp.py").is_file():
        sys.path.insert(0, str(_shared))
        break
import spec_stamp  # noqa: E402  (which spec the file was built from, written into its properties)
for _up in range(2, 6):                     # the spec loader: the plugin's shared/tools
    _shared = HERE.parents[_up] / "shared" / "tools" if len(HERE.parents) > _up else None
    if _shared is not None and (_shared / "packspec.py").is_file():
        sys.path.insert(0, str(_shared))
        break
import packspec  # noqa: E402  (the one spec loader: every tool reads the spec through it)

# --- brand, from the mini-site's stylesheet (site/assets/site.css) ----------
DISPLAY_FONT = "Azurio"          # the title only, regular weight, sentence case
DISPLAY_ALT = "Georgia"          # what Word substitutes where Azurio is not installed
BODY_FONT = "Replica LL TT"      # everything else: lockup name, intro, table, legend, footnotes
BODY_ALT = "Arial"

TEXT = "000000"          # --text: the title and the lockup name
BODY = "26292B"          # --text-body: the one-liner and the table
MUTED = "4C5156"         # --text-muted: the ICP line, the legend, the footnotes
HAIRLINE = "D1DAE2"      # --border-hairline: the title rule and every table border
RULE_DECOR = "BDCBD7"    # --decor-dim: the lockup's vertical rule
CATEGORY_FILL = "EDF0F2" # --bg-raised: the Category cells
ACCENT = "1485C3"        # --action, the practice's blue: Area cells, available/partial glyph
INK = "26282B"           # the table's header row
WHITE = "FFFFFF"
ROADMAP = "AEB4BA"       # the roadmap glyph: legible at 8pt, unlike --decor-dim

GLYPHS = {                       # status -> (glyph, colour, legend wording)
    "available": ("●", ACCENT, "available — provided out of the box, configuration may be required"),
    "partial": ("◐", ACCENT, "partial — partially implemented, major improvements on the roadmap"),
    "roadmap": ("○", ROADMAP, "roadmap — planned, not implemented today"),
}
# Neither brand face carries U+25CF / U+25D0 / U+25CB, so the renderer substitutes one face per
# glyph and they come out at different sizes (the owner, 2026-09-22: ● and ○ visibly smaller than
# ◐). One symbol face for all three fixes it by construction -- Apple Symbols draws them within
# 4% of each other -- with a fontTable altName so Word on Windows lands on a face that also has
# all three.
SYMBOL_FONT = "Apple Symbols"
SYMBOL_ALT = "Segoe UI Symbol"
SYMBOL_FILE = "/System/Library/Fonts/Apple Symbols.ttf"
# The faces the estimator may measure the glyphs with, in order. Where Apple Symbols is absent, a
# face that draws all three at one size stands in -- Segoe UI Symbol on Windows (the altName Word
# substitutes there), DejaVu Sans on Linux. The document still names Apple Symbols with its
# altName; only the measuring changes.
SYMBOL_FACES = (
    (SYMBOL_FONT, SYMBOL_FILE),
    (SYMBOL_ALT, "C:/Windows/Fonts/seguisym.ttf"),
    ("DejaVu Sans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ("DejaVu Sans", "/usr/share/fonts/dejavu/DejaVuSans.ttf"),
)
# Only used when no symbol face can be found: per-glyph sizes that look equal once the renderer
# has substituted a different face for each one.
GLYPH_SCALE = {"available": 1.15, "partial": 1.0, "roadmap": 1.15}
STATUS_ALIASES = {"ootb": "available", "yes": "available", "ga": "available",
                  "in_progress": "partial", "partially_available": "partial",
                  "planned": "roadmap", "no": "roadmap"}

# --- page and table geometry ------------------------------------------------
PAGE_W_MM, PAGE_H_MM = 210.0, 297.0
MARGIN_SIDE_MM = 13.1
MARGIN_TOP_MM = 10.0
MARGIN_BOTTOM_MM = 7.4
SAFETY = 0.04                    # 4% of the usable page height is held back

MM_PT = 72.0 / 25.4
TEXT_W_PT = (PAGE_W_MM - 2 * MARGIN_SIDE_MM) * MM_PT       # 520.98pt
USABLE_H_PT = (PAGE_H_MM - MARGIN_TOP_MM - MARGIN_BOTTOM_MM) * MM_PT

# column widths in dxa (twips); every layout totals 10250 dxa (7.12in), as the reference does
WIDTHS_5 = [1077, 1978, 3420, 1350, 2425]
WIDTHS_6 = [1000, 1800, 3000, 1150, 1150, 2150]
WIDTHS_COMPACT = [1000, 1500, 5400, 2350]
HEADERS_5 = ["Area", "Category", "Features", "Current status", "Standard customization scope"]
HEADERS_6 = ["Area", "Category", "Features", "Current status", "Tier first available",
             "Standard customization scope"]
HEADERS_COMPACT = ["Area", "Category", "Features", "Standard customization scope"]
# The Area column is narrow and its names are single long words ("normalization", "Optimization"),
# which Word breaks mid-word rather than overflow. The build widens it to the longest word it has
# to hold, within these bounds, and takes the difference from the Features column.
AREA_W_MIN, AREA_W_MAX = 1000, 1500

CELL_MAR = {"top": 16, "left": 80, "bottom": 16, "right": 65}   # dxa
MIN_ROW_DXA = 300
BULLET_INDENT_DXA = 159
# Single line spacing is the face's own ascent + descent, which both brand faces put at 1.20 em
# (read off the installed files). Every paragraph is left at single spacing, so this is the
# estimator's line height for text set in Azurio or Replica LL TT.
LINE_FACTOR = 1.20
# What a line carrying status glyphs costs. With the symbol face named explicitly its line is
# shorter than the brand face's, so the glyphs add nothing; left to the renderer's own
# substitution it measured 1.36 em against a Pages export, and in compact mode every line of the
# Features cell carries glyphs. `Symbols` picks the right one at run time.
GLYPH_LINE_FACTOR = 1.36
# A table cell is one line of the body size taller than the text it holds -- the half-leading the
# renderer puts above and below the cell's text. Measured across 1/3/5-line cells at both type
# sizes: every row came out at exactly its wrapped lines plus one more. Ignoring it under-read a
# 13-row table by a quarter of a page, which is how a "75% of one page" estimate printed two pages.
CELL_TRAIL_LINES = 1.0
# The horizontal border each row carries, on top of its content.
BORDER_PT = 0.85
# The status cell sets its line to 1.05 -- the renderer applies the multiplier to the body size,
# not to the 10pt glyph, so the cell is barely taller than a line of table text.
STATUS_LINE_FACTOR = 1.05
# the standalone glyph in the Current status column, as the reference document sets it
STATUS_GLYPH_PT = 10.0

# the header block and the trailing blocks, in points -- build() and estimate() share these
TITLE_PT = 20.0
TITLE_SPACE_BEFORE = 7.0
TITLE_SPACE_AFTER = 3.0
TITLE_RULE_SPACE = 5.0           # the hairline's own space below the text
INTRO_PT = 9.0
INTRO_SPACE_BEFORE = 5.0
INTRO_SPACE_AFTER = 1.5
ICP_PT = 8.0
ICP_SPACE_AFTER = 4.0
TABLE_SPACE_BEFORE = 2.0
LEGEND_PT = 7.0
LEGEND_GLYPH_PT = 8.0
LEGEND_SPACE_BEFORE = 4.5
NOTE_PT = 7.0
NOTE_SPACE_AFTER = 0.8
# a footnote is a tier caveat and nothing else (the owner, 2026-09-22); past these the build says so
MAX_NOTES = 3
MAX_NOTE_WORDS = 20
LOCKUP_NAME_PT = 12.0
LOCKUP_MARK_IN = 1.0
LOCKUP_GAP_IN = 0.125
LOCKUP_RULE_DXA = 20            # 1pt: the site's 1px rule between mark and name
LOCKUP_NAME = "Oracle AI & Data Solutions"

TIER_LABELS = {"pov": "PoV Jumpstart", "integration": "Integration", "scaling": "Scaling"}

TABLE_SIZES = (7.5, 7.0)         # the ladder's two type sizes; 7pt is the floor
VENDOR_PROPER = {"Oracle", "NVIDIA", "SoftServe", "OCI", "Fusion", "AI", "IT", "US", "EU"}


class SpecError(Exception):
    """A required value is missing or unusable -- send the user back to /oracle-packs:spec."""


# --- text measurement -------------------------------------------------------
# The brand faces ship privately in the plugin's own fonts/ folder (<plugin>/fonts, three levels
# above this tools/ folder), so the estimate is exact on any practice member's machine; the
# installed font folders are searched after it. A fonts/ folder that is there but empty is simply
# passed over.
PLUGIN_FONTS = Path(__file__).resolve().parents[3] / "fonts"
FONT_DIRS = (str(PLUGIN_FONTS), "/Library/Fonts/Managed", str(Path.home() / "Library/Fonts"),
             "/Library/Fonts", "/System/Library/Fonts", "/usr/share/fonts")
FONT_FILES = {  # family -> filename stem as installed (the Managed copies carry a hash suffix)
    ("Replica LL TT", False): "ReplicaLLTT-Regular*",
    ("Replica LL TT", True): "ReplicaLLTT-Bold*",
    (DISPLAY_FONT, False): "Azurio-Regular*",
    (DISPLAY_FONT, True): "Azurio-Semibold*",
}
AVERAGE_EM = 0.52                # fallback glyph width when no font file can be read


class Symbols:
    """Which face draws the three status glyphs, at what size, and what a glyph line costs.

    One face for all three is the whole point: the brand faces carry none of the code points, so
    letting the renderer choose gives a different face -- and a different size -- per glyph.
    """

    def __init__(self):
        self.family = SYMBOL_FONT               # what the document names, whichever face is measured
        self.uniform = True
        self.reason = ""
        self.measured = None
        found = next(((face, Path(p)) for face, p in SYMBOL_FACES if Path(p).exists()), None)
        if found is None:
            self._degrade(f"no symbol face was found ({SYMBOL_FONT}, {SYMBOL_ALT} or DejaVu Sans)")
            return
        face, path = found
        self.measured = face
        try:
            from PIL import ImageFont
        except ImportError:
            return                              # the file is there; without Pillow, trust it
        try:
            font = ImageFont.truetype(str(path), 200)
            boxes = {}
            for key, (glyph, _c, _w) in GLYPHS.items():
                box = font.getbbox(glyph)
                boxes[key] = (box[2] - box[0], box[3] - box[1])
            missing = font.getbbox("")     # a private-use code point draws .notdef
            control = (missing[2] - missing[0], missing[3] - missing[1])
            if control in boxes.values():
                self._degrade(f"{face} is missing one of the status glyphs")
                return
            widths = [w for w, _h in boxes.values()]
            heights = [h for _w, h in boxes.values()]
            for values, what in ((widths, "width"), (heights, "height")):
                if max(values) - min(values) > 0.10 * max(values):
                    self._degrade(f"{face} draws the status glyphs at uneven {what}s")
                    return
        except Exception as err:                # pragma: no cover -- unreadable face
            self._degrade(f"{face} could not be read ({err})")
            return
        if face != SYMBOL_FONT:
            print(f"build_feature_list: {SYMBOL_FONT} is not installed here; the status glyphs are "
                  f"measured with {face}, and the document still names {SYMBOL_FONT} "
                  f"({SYMBOL_ALT} where Word substitutes it).", file=sys.stderr)

    def _degrade(self, reason):
        self.family = BODY_FONT
        self.uniform = False
        self.reason = reason
        print(f"build_feature_list: {reason}; the status glyphs fall back to per-glyph point "
              f"sizes so the three still look the same size on the page.", file=sys.stderr)

    def size(self, status, base):
        """The point size to set one glyph at, given the size its neighbours are set at."""
        return base if self.uniform else base * GLYPH_SCALE[status]

    @property
    def line_factor(self):
        return LINE_FACTOR if self.uniform else GLYPH_LINE_FACTOR


_SYMBOLS = None


def symbols() -> "Symbols":
    """The symbol face, probed once per run."""
    global _SYMBOLS
    if _SYMBOLS is None:
        _SYMBOLS = Symbols()
    return _SYMBOLS


class Measurer:
    """Text width in points. Exact when the brand face is found (shipped or installed) and Pillow
    is present."""

    def __init__(self):
        self._cache = {}
        self.sources = {}                        # (family, bold) -> the font file measured
        self.exact = True
        self.reason = ""
        try:
            from PIL import ImageFont            # noqa: F401  (probe only)
        except ImportError:
            self.exact = False
            self.reason = "Pillow is not installed"

    def _font(self, family, bold):
        key = (family, bool(bold))
        if key in self._cache:
            return self._cache[key]
        font = None
        pattern = FONT_FILES.get(key)
        if pattern and self.exact:
            for directory in FONT_DIRS:
                for match in sorted(glob.glob(os.path.join(directory, pattern))):
                    try:
                        from PIL import ImageFont
                        font = ImageFont.truetype(match, 100)
                    except Exception:            # pragma: no cover -- unreadable face
                        continue
                    self.sources[key] = match
                    break
                if font is not None:
                    break
        if font is None and self.exact:
            self.exact = False
            self.reason = f"{family} is in neither the plugin's fonts/ folder nor the installed fonts"
        self._cache[key] = font
        return font

    def source_line(self):
        """Where the estimate's glyph widths came from, for the report."""
        if not self.exact:
            return f"fit measured with an average glyph width ({self.reason}); the estimate is approximate"
        path = self.sources.get((BODY_FONT, False))
        if not path:
            return None
        folder = Path(path).parent
        where = "the plugin's fonts/ folder" if folder == PLUGIN_FONTS else str(folder)
        return f"fit measured with {BODY_FONT} from {where}"

    def length(self, text, size, family=BODY_FONT, bold=False):
        font = self._font(family, bold)
        if font is None:
            return len(text) * AVERAGE_EM * size
        return font.getlength(text) * size / 100.0

    def lines(self, text, width_pt, size, family=BODY_FONT, bold=False):
        """How many lines `text` takes when wrapped at `width_pt`."""
        text = " ".join(str(text).split())
        if not text:
            return 1
        if self.length(text, size, family, bold) <= width_pt:
            return 1
        count, current = 0, ""
        for word in text.split(" "):
            trial = f"{current} {word}" if current else word
            if not current or self.length(trial, size, family, bold) <= width_pt:
                current = trial
            else:
                count += 1
                current = word
        return count + (1 if current else 0)


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


def cell_margins(cell, top=CELL_MAR["top"], left=CELL_MAR["left"],
                 bottom=CELL_MAR["bottom"], right=CELL_MAR["right"]):
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


def row_properties(row, height=MIN_ROW_DXA, keep_together=True):
    tr_pr = row._tr.get_or_add_trPr()
    if keep_together:
        _el(tr_pr, "w:cantSplit")
    _el(tr_pr, "w:trHeight", val=height)


def repeat_header(row):
    _el(row._tr.get_or_add_trPr(), "w:tblHeader")


def table_borders(table, colour=HAIRLINE, size=4):
    borders = _el(table._tbl.tblPr, "w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        _el(borders, "w:" + edge, val="single", sz=size, space=0, color=colour)


def no_borders(table):
    borders = _el(table._tbl.tblPr, "w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        _el(borders, "w:" + edge, val="none", sz=0, space=0, color="auto")


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


def set_face(run, family=BODY_FONT):
    """rFonts on the run itself: Word must not fall back to the style's face mid-paragraph."""
    r_fonts = run._element.get_or_add_rPr().get_or_add_rFonts()
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        r_fonts.set(qn(attr), family)


def add_run(paragraph, text, *, size, bold=False, colour=None, family=BODY_FONT):
    run = paragraph.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)
    if colour:
        run.font.color.rgb = RGBColor.from_string(colour)
    set_face(run, family)
    return run


def write(cell, runs, *, align=None, size=7.5, line=None):
    """Replace a cell's content with one paragraph built from (text, bold, colour, size) runs."""
    paragraph = cell.paragraphs[0]
    for existing in list(paragraph.runs):
        existing._r.getparent().remove(existing._r)
    if align is not None:
        paragraph.alignment = align
    paragraph.paragraph_format.space_before = Pt(0)
    paragraph.paragraph_format.space_after = Pt(0)
    if line is not None:
        paragraph.paragraph_format.line_spacing = line
    for run in runs:
        text, bold, colour, run_size = run[:4]
        family = run[4] if len(run) > 4 else BODY_FONT
        add_run(paragraph, text, size=run_size or size, bold=bool(bold), colour=colour,
                family=family)
    return paragraph


def bullets(cell, items, size=7.5):
    """A cell holding a short bulleted list, like the reference's customization-scope cells."""
    cell.text = ""
    first = True
    for item in items:
        paragraph = cell.paragraphs[0] if first else cell.add_paragraph()
        first = False
        paragraph.style = cell.part.document.styles["List Bullet"]
        paragraph.paragraph_format.left_indent = Twips(BULLET_INDENT_DXA)
        paragraph.paragraph_format.space_before = Pt(0)
        paragraph.paragraph_format.space_after = Pt(0)
        add_run(paragraph, str(item), size=size)


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


def sentence_tail(text, spec):
    """Lower-case the first character of the ICP line so it reads on from "For ..."."""
    text = " ".join(str(text).split())
    if not text:
        return text
    first_word = re.split(r"[\s,.;:]", text, maxsplit=1)[0].strip("(\"'")
    proper = set(VENDOR_PROPER) | {w for w in str(dig(spec, "meta.name", "")).split() if w[:1].isupper()}
    if (len(text) > 1 and text[1].isupper()) or first_word in proper:
        return text
    return text[0].lower() + text[1:]


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


def footnote_marks(rows):
    """Feature -> marker, plus the footnote lines, in document order."""
    notes, marks = [], {}
    for entry in rows:
        if entry["note"] and entry["feature"] not in marks:
            marks[entry["feature"]] = "*" * (len(notes) + 1)
            notes.append((marks[entry["feature"]], entry["feature"], entry["note"]))
    return marks, notes


def compact_rows(rows):
    """One row per category, features listed inline -- the ladder's last two rungs."""
    grouped = []
    for (area, category), start, length in runs_of([(r["area"], r["category"]) for r in rows]):
        members = rows[start:start + length]
        grouped.append({
            "area": area,
            "category": category,
            "features": members,
            "scope": members[0]["scope"],
        })
    return grouped


def compact_text(group, marks):
    """The plain text of a compact Features cell, for measurement and for the lint's eyes."""
    parts = [f"{m['feature']}{marks.get(m['feature'], '')} {GLYPHS[m['status']][0]}"
             for m in group["features"]]
    return "  ·  ".join(parts)


# --- height estimate --------------------------------------------------------
def header_block_height(spec, measurer, one_liner, icp_line):
    """The lockup, the title and the two intro lines, in points."""
    mark_h = LOCKUP_MARK_IN * 72.0 * mark_aspect()[1] / mark_aspect()[0]
    # the lockup is a table row, so it carries the same trailing line every cell does
    lockup = max(mark_h, LOCKUP_NAME_PT * LINE_FACTOR) + CELL_TRAIL_LINES * INTRO_PT + BORDER_PT
    title_text = dig(spec, "feature_list.title") or f"{dig(spec, 'meta.name', 'Pack')} — Feature list"
    title_lines = measurer.lines(title_text, TEXT_W_PT, TITLE_PT, DISPLAY_FONT)
    height = lockup
    height += TITLE_SPACE_BEFORE + title_lines * TITLE_PT * LINE_FACTOR + TITLE_RULE_SPACE + TITLE_SPACE_AFTER
    height += INTRO_SPACE_BEFORE
    height += measurer.lines(one_liner, TEXT_W_PT, INTRO_PT) * INTRO_PT * LINE_FACTOR + INTRO_SPACE_AFTER
    if icp_line:
        height += measurer.lines("For " + icp_line, TEXT_W_PT, ICP_PT) * ICP_PT * LINE_FACTOR
        height += ICP_SPACE_AFTER
    return height + TABLE_SPACE_BEFORE


def tail_block_height(measurer, notes):
    """The one-line legend and the footnotes, in points."""
    legend = legend_text()
    # every legend line carries a glyph, and the glyph's substituted face sets the line's height
    height = (LEGEND_SPACE_BEFORE
              + measurer.lines(legend, TEXT_W_PT, LEGEND_PT) * LEGEND_GLYPH_PT
              * symbols().line_factor)
    for mark, _feature, text in notes:
        line = f"{mark}  {text}"
        height += measurer.lines(line, TEXT_W_PT, NOTE_PT) * NOTE_PT * LINE_FACTOR + NOTE_SPACE_AFTER
    return height


def legend_text():
    return " · ".join(f"{glyph} {wording}" for glyph, _, wording in
                      (GLYPHS[k] for k in ("available", "partial", "roadmap")))


def mark_aspect():
    """(width, height) of the wordmark PNG, so the lockup's height is the real one."""
    path = Path(__file__).resolve().parent.parent / "assets" / "softserve-wordmark-ink.png"
    try:
        from PIL import Image
        with Image.open(path) as image:
            return image.size
    except Exception:
        return (2400, 410)           # the shipped asset's own proportions


def layout(mode, tier_column, rows, measurer, size):
    """(headers, widths) for one rung, with the Area column sized to its longest word."""
    if mode == "compact":
        headers, widths, area_col, feature_col = HEADERS_COMPACT, list(WIDTHS_COMPACT), 0, 2
    elif tier_column:
        headers, widths, area_col, feature_col = HEADERS_6, list(WIDTHS_6), 0, 2
    else:
        headers, widths, area_col, feature_col = HEADERS_5, list(WIDTHS_5), 0, 2
    words = [word for entry in rows for word in str(entry["area"]).split()]
    if words:
        widest = max(measurer.length(word, size, BODY_FONT, True) for word in words)
        needed = int(widest * 20) + CELL_MAR["left"] + CELL_MAR["right"] + 20   # +1pt of air
        wanted = max(AREA_W_MIN, min(AREA_W_MAX, needed))
        shift = wanted - widths[area_col]
        if shift > 0:                          # never starve the Features column to do it
            shift = min(shift, widths[feature_col] - 1800)
        if shift:
            widths[area_col] += shift
            widths[feature_col] -= shift
    return headers, widths


def cell_lines(measurer, text, width_dxa, size, *, bold=False, indent_dxa=0):
    usable = (width_dxa - CELL_MAR["left"] - CELL_MAR["right"] - indent_dxa) / 20.0
    return measurer.lines(text, max(usable, 10.0), size, BODY_FONT, bold)


def estimate_table(measurer, rows, widths, headers, size, *, compact=False, tier_column=False):
    """Total table height in points, modelling Word's merged-cell behaviour."""
    flat = [member for group in rows for member in group["features"]] if compact else rows
    marks, _ = footnote_marks(flat)
    line_h = size * LINE_FACTOR
    glyph_h = size * symbols().line_factor
    trail = CELL_TRAIL_LINES * line_h + BORDER_PT      # what a row carries beyond its own text
    min_row = MIN_ROW_DXA / 20.0 + BORDER_PT

    def block(text, width_dxa, *, bold=False, indent=0, glyph=False):
        lines = cell_lines(measurer, text, width_dxa, size, bold=bold, indent_dxa=indent)
        return lines * (glyph_h if glyph else line_h) + trail

    def stack(items, width_dxa, indent=0):
        """A cell holding several paragraphs -- the bulleted customization-scope cells."""
        lines = sum(cell_lines(measurer, item, width_dxa, size, indent_dxa=indent) for item in items)
        return max(lines, 1) * line_h + trail

    header_h = max([min_row] + [block(text, width, bold=True)
                                for text, width in zip(headers, widths)])

    if compact:
        # every line of a compact Features cell carries status glyphs, so every line is a glyph line
        heights = [max(min_row, block(compact_text(group, marks), widths[2], glyph=True))
                   for group in rows]
    else:
        heights = []
        for entry in rows:
            mark = marks.get(entry["feature"], "")
            cells = [block(entry["feature"] + mark, widths[2]),
                     STATUS_LINE_FACTOR * line_h + trail]
            if tier_column:
                cells.append(block(TIER_LABELS.get(str(entry["tier"]), str(entry["tier"] or "–")),
                                   widths[4]))
            heights.append(max([min_row] + cells))

    def absorb(keys, content_of):
        """A merged cell taller than its span pushes the span's last row down, as Word does."""
        for _value, start, length in runs_of(keys):
            content = content_of(start)
            span = sum(heights[start:start + length])
            if content > span:
                heights[start + length - 1] += content - span

    if compact:
        absorb([g["area"] for g in rows],
               lambda i: block(rows[i]["area"], widths[0], bold=True))
        absorb([(g["area"], g["category"]) for g in rows],
               lambda i: block(rows[i]["category"], widths[1]))
        absorb([(g["area"], tuple(g["scope"])) for g in rows],
               lambda i: stack(rows[i]["scope"], widths[3], BULLET_INDENT_DXA))
        return header_h + sum(heights)

    scope_col = 5 if tier_column else 4
    absorb([r["area"] for r in rows],
           lambda i: block(rows[i]["area"], widths[0], bold=True))
    absorb([(r["area"], r["category"]) for r in rows],
           lambda i: block(rows[i]["category"], widths[1]))
    absorb([(r["area"], tuple(r["scope"])) for r in rows],
           lambda i: stack(rows[i]["scope"], widths[scope_col], BULLET_INDENT_DXA))
    return header_h + sum(heights)


def fit_report(rows, estimate, budget, mode):
    """The plain report the skill puts to the owner when nothing fits one page."""
    areas, categories = {}, {}
    for entry in rows:
        areas[entry["area"]] = areas.get(entry["area"], 0) + 1
        key = f"{entry['area']} › {entry['category']}"
        categories[key] = categories.get(key, 0) + 1
    biggest_areas = sorted(areas.items(), key=lambda kv: -kv[1])[:3]
    biggest_categories = sorted(categories.items(), key=lambda kv: -kv[1])[:5]
    lines = [
        "build_feature_list: the feature list does not fit one A4 page.",
        f"  estimated height {estimate:.0f}pt against a budget of {budget:.0f}pt "
        f"({estimate / budget * 100:.0f}% of one page) at the tightest setting tried ({mode}).",
        f"  {len(areas)} areas / {len(categories)} categories / {len(rows)} features.",
        "  largest areas: " + ", ".join(f"{name} ({count})" for name, count in biggest_areas),
        "  largest categories: " + ", ".join(f"{name} ({count})" for name, count in biggest_categories),
        "  group or generalize the capabilities so the list fits one page: merge sibling "
        "features into one, fold small categories into their neighbour, shorten names.",
    ]
    return "\n".join(lines)


# --- document assembly ------------------------------------------------------
def page_setup(document):
    section = document.sections[0]
    section.orientation = WD_ORIENT.PORTRAIT
    section.page_width, section.page_height = Mm(PAGE_W_MM), Mm(PAGE_H_MM)
    section.left_margin = section.right_margin = Mm(MARGIN_SIDE_MM)
    section.top_margin, section.bottom_margin = Mm(MARGIN_TOP_MM), Mm(MARGIN_BOTTOM_MM)
    return section


def base_styles(document, size):
    normal = document.styles["Normal"]
    normal.font.name = BODY_FONT
    normal.font.size = Pt(size)
    # python-docx starts from Word's default template, whose Normal style carries 8pt space-after
    # and 1.08 line spacing. Left in place it doubles every table row's height.
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(0)
    normal.paragraph_format.line_spacing = 1.0
    r_fonts = normal.element.rPr.rFonts
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        r_fonts.set(qn(attr), BODY_FONT)


def lockup(document):
    """The mini-site's header: the SoftServe wordmark, a hairline rule, the practice's name.

    Three borderless cells. The rule is the middle cell, 1pt wide and filled: a shaded cell is
    drawn by every renderer that draws the table at all, which a cell or paragraph border on a
    borderless table is not. Its height is the row's, which the wordmark sets to ~0.17in.
    """
    mark = Path(__file__).resolve().parent.parent / "assets" / "softserve-wordmark-ink.png"
    gap = int(LOCKUP_GAP_IN * 1440)
    widths = [int(LOCKUP_MARK_IN * 1440) + gap, LOCKUP_RULE_DXA, 6000 + gap]
    table = document.add_table(rows=1, cols=3)
    no_borders(table)
    cells = table.rows[0].cells
    for cell, width, left, right in zip(cells, widths, (0, 0, gap), (gap, 0, 0)):
        valign(cell)
        cell_margins(cell, top=0, left=left, bottom=0, right=right)
        cell.width = Twips(width)
        paragraph = cell.paragraphs[0]
        paragraph.paragraph_format.space_before = Pt(0)
        paragraph.paragraph_format.space_after = Pt(0)

    if mark.exists():
        cells[0].paragraphs[0].add_run().add_picture(str(mark), width=Inches(LOCKUP_MARK_IN))
    else:                                       # never silently drop the brand mark
        add_run(cells[0].paragraphs[0], "SoftServe", size=LOCKUP_NAME_PT, bold=True, colour=TEXT)
        print("build_feature_list: the wordmark asset is missing; the lockup fell back to text.",
              file=sys.stderr)
    shade(cells[1], RULE_DECOR)
    add_run(cells[2].paragraphs[0], LOCKUP_NAME, size=LOCKUP_NAME_PT, colour=TEXT)

    _el(table._tbl.tblPr, "w:tblLayout", type="fixed")
    _el(table._tbl.tblPr, "w:tblW", w=sum(widths), type="dxa")
    margins = _el(table._tbl.tblPr, "w:tblCellMar")
    _el(margins, "w:left", w=0, type="dxa")
    _el(margins, "w:right", w=0, type="dxa")
    grid = table._tbl.find(qn("w:tblGrid"))
    for column, width in zip(grid, widths):
        column.set(qn("w:w"), str(width))
    row_properties(table.rows[0], height=1, keep_together=True)
    return table


def header_block(document, spec, one_liner, icp_line):
    lockup(document)

    title_text = dig(spec, "feature_list.title") or f"{need(spec, 'meta.name')} — Feature list"
    title = document.add_paragraph()
    title.paragraph_format.space_before = Pt(TITLE_SPACE_BEFORE)
    title.paragraph_format.space_after = Pt(TITLE_SPACE_AFTER)
    rule = _el(title._p.get_or_add_pPr(), "w:pBdr")
    _el(rule, "w:bottom", val="single", sz=6, space=4, color=HAIRLINE)
    add_run(title, title_text, size=TITLE_PT, colour=TEXT, family=DISPLAY_FONT)

    intro = document.add_paragraph()
    intro.paragraph_format.space_before = Pt(INTRO_SPACE_BEFORE)
    intro.paragraph_format.space_after = Pt(INTRO_SPACE_AFTER)
    add_run(intro, one_liner, size=INTRO_PT, colour=BODY)

    if icp_line:
        who = document.add_paragraph()
        who.paragraph_format.space_before = Pt(0)
        who.paragraph_format.space_after = Pt(ICP_SPACE_AFTER)
        add_run(who, "For " + icp_line, size=ICP_PT, colour=MUTED)
    return title_text


def tail_block(document, notes, size=LEGEND_PT):
    legend = document.add_paragraph()
    legend.paragraph_format.space_before = Pt(LEGEND_SPACE_BEFORE)
    legend.paragraph_format.space_after = Pt(0)
    for index, key in enumerate(("available", "partial", "roadmap")):
        glyph, colour, wording = GLYPHS[key]
        if index:
            add_run(legend, " · ", size=size, colour=MUTED)
        add_run(legend, glyph, size=symbols().size(key, LEGEND_GLYPH_PT), colour=colour,
                family=symbols().family)
        add_run(legend, " " + wording, size=size, colour=MUTED)

    for mark, _feature, text in notes:
        line = document.add_paragraph()
        line.paragraph_format.space_before = Pt(0)
        line.paragraph_format.space_after = Pt(NOTE_SPACE_AFTER)
        # the marker already sits on the feature name -- a footnote repeats neither the name nor
        # the category, only the caveat (the owner, 2026-09-22)
        add_run(line, f"{mark}  {text}", size=NOTE_PT, colour=MUTED)


def stamp(document, spec, title_text):
    """Traceability without a page footer: the spec version and the build date as file properties.

    The owner's decision of 2026-09-22 -- nothing in the page footer. The document still has to say
    which spec version it came from, so it says it where a reader can ask for it (File > Properties)
    instead of printing it on a page that goes to a customer.
    """
    props = document.core_properties
    props.title = title_text
    props.subject = (f"{dig(spec, 'meta.name', 'Pack')} · feature list · "
                     f"spec v{dig(spec, 'meta.spec_version', '?')}")
    props.comments = (f"Generated {dt.date.today().isoformat()} from "
                      f"{dig(spec, 'meta.slug', 'pack')}/pack-spec.md "
                      f"(spec v{dig(spec, 'meta.spec_version', '?')}) by build_feature_list.py. "
                      f"Internal / partner material: no pricing.")
    props.category = "Accelerator pack · feature list"


def check_notes(notes):
    """A footnote is a tier caveat, not a description -- say so when the list drifts."""
    if len(notes) > MAX_NOTES:
        print(f"build_feature_list: {len(notes)} footnotes ({MAX_NOTES} is the working limit) -- "
              f"a note earns its place only when a tier caveat changes what the buyer gets. Fold "
              f"the rest into the area's customization scope or drop them: "
              + " / ".join(f"{mark} {feature}" for mark, feature, _t in notes), file=sys.stderr)
    long_notes = [(mark, feature, len(str(text).split())) for mark, feature, text in notes
                  if len(str(text).split()) > MAX_NOTE_WORDS]
    if long_notes:
        print(f"build_feature_list: {len(long_notes)} footnote(s) run past {MAX_NOTE_WORDS} words "
              f"-- trim each to the caveat itself: "
              + " / ".join(f"{mark} {feature} ({n} words)" for mark, feature, n in long_notes),
              file=sys.stderr)


def full_table(document, rows, widths, headers, size, tier_column, repeat):
    table = document.add_table(rows=1, cols=len(headers))
    table_borders(table)
    _el(table._tbl.tblPr, "w:tblLook", val="04A0", firstRow=1, lastRow=0,
        firstColumn=1, lastColumn=0, noHBand=0, noVBand=1)
    header_row = table.rows[0]
    row_properties(header_row)
    if repeat:
        repeat_header(header_row)
    for cell, text in zip(header_row.cells, headers):
        shade(cell, INK)
        valign(cell)
        cell_margins(cell)
        write(cell, [(text, True, WHITE, None)], size=size)

    marks, _ = footnote_marks(rows)
    body_rows = []
    for entry in rows:
        row = table.add_row()
        row_properties(row)
        body_rows.append(row)
        for cell in row.cells:
            valign(cell)
            cell_margins(cell)
            shade(cell, WHITE)
        cells = row.cells
        write(cells[2], [(entry["feature"] + marks.get(entry["feature"], ""), False, BODY, None)],
              size=size)
        glyph, colour, _ = GLYPHS[entry["status"]]
        write(cells[3],
              [(glyph, False, colour, symbols().size(entry["status"], STATUS_GLYPH_PT),
                symbols().family)],
              align=WD_ALIGN_PARAGRAPH.CENTER, size=size, line=1.05)
        if tier_column:
            label = TIER_LABELS.get(str(entry["tier"]), str(entry["tier"] or "–"))
            write(cells[4], [(label, False, MUTED, None)], align=WD_ALIGN_PARAGRAPH.CENTER, size=size)

    scope_col = 5 if tier_column else 4
    merge_plan = [
        (0, [r["area"] for r in rows], ACCENT),
        (1, [(r["area"], r["category"]) for r in rows], CATEGORY_FILL),
        (3, [(r["area"], r["category"], r["status"]) for r in rows], WHITE),
    ]
    if tier_column:
        merge_plan.append((4, [(r["area"], r["category"], r["tier"]) for r in rows], WHITE))
    merge_plan.append((scope_col, [(r["area"], tuple(r["scope"])) for r in rows], WHITE))

    for column, keys, fill in merge_plan:
        for _value, start, length in runs_of(keys):
            first = body_rows[start].cells[column]
            shade(first, fill)
            if column == 0:
                write(first, [(rows[start]["area"], True, WHITE, None)],
                      align=WD_ALIGN_PARAGRAPH.CENTER, size=size)
            elif column == 1:
                write(first, [(rows[start]["category"], False, BODY, None)], size=size)
            elif column == scope_col:
                bullets(first, rows[start]["scope"], size=size)
            merge_down(body_rows, column, start, length, fill)
    fixed_layout(table, widths)
    return table


def compact_table(document, groups, rows, widths, size, repeat):
    headers = HEADERS_COMPACT
    marks, _ = footnote_marks(rows)
    table = document.add_table(rows=1, cols=len(headers))
    table_borders(table)
    _el(table._tbl.tblPr, "w:tblLook", val="04A0", firstRow=1, lastRow=0,
        firstColumn=1, lastColumn=0, noHBand=0, noVBand=1)
    header_row = table.rows[0]
    row_properties(header_row)
    if repeat:
        repeat_header(header_row)
    for cell, text in zip(header_row.cells, headers):
        shade(cell, INK)
        valign(cell)
        cell_margins(cell)
        write(cell, [(text, True, WHITE, None)], size=size)

    body_rows = []
    for group in groups:
        row = table.add_row()
        row_properties(row)
        body_rows.append(row)
        for cell in row.cells:
            valign(cell)
            cell_margins(cell)
            shade(cell, WHITE)
        runs = []
        for index, member in enumerate(group["features"]):
            if index:
                runs.append(("  ·  ", False, MUTED, None))
            runs.append((member["feature"] + marks.get(member["feature"], "") + " ", False, BODY, None))
            glyph, colour, _ = GLYPHS[member["status"]]
            runs.append((glyph, False, colour, symbols().size(member["status"], size),
                         symbols().family))
        write(row.cells[2], runs, size=size)

    for column, keys, fill in (
            (0, [g["area"] for g in groups], ACCENT),
            (1, [(g["area"], g["category"]) for g in groups], CATEGORY_FILL),
            (3, [(g["area"], tuple(g["scope"])) for g in groups], WHITE)):
        for _value, start, length in runs_of(keys):
            first = body_rows[start].cells[column]
            shade(first, fill)
            if column == 0:
                write(first, [(groups[start]["area"], True, WHITE, None)],
                      align=WD_ALIGN_PARAGRAPH.CENTER, size=size)
            elif column == 1:
                write(first, [(groups[start]["category"], False, BODY, None)], size=size)
            else:
                bullets(first, groups[start]["scope"], size=size)
            merge_down(body_rows, column, start, length, fill)
    fixed_layout(table, widths)
    return table


def merge_down(body_rows, column, start, length, fill):
    if length <= 1:
        return
    vmerge(body_rows[start].cells[column], restart=True)
    for offset in range(1, length):
        following = body_rows[start + offset].cells[column]
        following.text = ""
        # continuation cells carry the group's fill too: Word paints the merged span from the
        # restart cell, but lighter renderers (QuickLook, some viewers) do not, and an
        # unshaded continuation breaks the column visually.
        shade(following, fill)
        vmerge(following, restart=False)


def build(spec, rows, *, mode, size, tier_column, repeat_header_row):
    """Assemble the document at one rung of the ladder. `mode` is 'full' or 'compact'."""
    one_liner = dig(spec, "feature_list.intro") or need(spec, "one_liner.full")
    one_liner = " ".join(str(one_liner).split())
    icp_raw = dig(spec, "icp.line")
    icp_line = sentence_tail(icp_raw, spec) if icp_raw else ""

    document = Document()
    base_styles(document, size)
    page_setup(document)
    title_text = header_block(document, spec, one_liner, icp_line)

    _marks, notes = footnote_marks(rows)
    headers, widths = layout(mode, tier_column, rows, Measurer(), size)
    if mode == "compact":
        compact_table(document, compact_rows(rows), rows, widths, size, repeat_header_row)
    else:
        full_table(document, rows, widths, headers, size, tier_column, repeat_header_row)
    tail_block(document, notes)
    stamp(document, spec, title_text)
    return document, title_text, headers, widths


def estimate(spec, rows, measurer, *, mode, size, tier_column):
    """(estimated height, budget) in points for one rung of the ladder."""
    one_liner = " ".join(str(dig(spec, "feature_list.intro") or need(spec, "one_liner.full")).split())
    icp_raw = dig(spec, "icp.line")
    icp_line = sentence_tail(icp_raw, spec) if icp_raw else ""
    _marks, notes = footnote_marks(rows)

    head = header_block_height(spec, measurer, one_liner, icp_line)
    tail = tail_block_height(measurer, notes)
    budget = USABLE_H_PT * (1 - SAFETY) - head - tail
    headers, widths = layout(mode, tier_column, rows, measurer, size)
    if mode == "compact":
        table = estimate_table(measurer, compact_rows(rows), widths, headers, size, compact=True)
    else:
        table = estimate_table(measurer, rows, widths, headers, size, tier_column=tier_column)
    return table, budget


# the fit ladder, tried in order: one row per feature at 7.5 then 7pt, then compact mode
# (one row per category) at the same two sizes. 7pt is the floor -- below it the table stops
# being readable, and the answer is a coarser capability tree, not smaller type.
LADDER = [("full", 7.5), ("full", 7.0), ("compact", 7.5), ("compact", 7.0)]


# --- post-processing --------------------------------------------------------
FONT_ENTRY = (
    '<w:font w:name="{name}"><w:altName w:val="{alt}"/><w:charset w:val="00"/>'
    '<w:family w:val="{family}"/><w:pitch w:val="variable"/></w:font>')


def add_font_table_entries(path: Path):
    """Name the brand faces in word/fontTable.xml with a sane altName.

    Word substitutes an unknown face by guessing from the name; an explicit altName makes
    the substitution predictable on a machine without Azurio and Replica LL TT installed.
    """
    entries = (FONT_ENTRY.format(name=DISPLAY_FONT, alt=DISPLAY_ALT, family="roman")
               + FONT_ENTRY.format(name=BODY_FONT, alt=BODY_ALT, family="swiss")
               + FONT_ENTRY.format(name=SYMBOL_FONT, alt=SYMBOL_ALT, family="auto"))
    with zipfile.ZipFile(path) as archive:
        items = {item.filename: archive.read(item.filename) for item in archive.infolist()}
        order = [item.filename for item in archive.infolist()]
    table = items.get("word/fontTable.xml")
    if table is None:
        return False
    text = table.decode("utf-8")
    if f'w:name="{BODY_FONT}"' in text:
        return True
    if "</w:fonts>" not in text:
        return False
    items["word/fontTable.xml"] = text.replace("</w:fonts>", entries + "</w:fonts>").encode("utf-8")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for name in order:
            archive.writestr(name, items[name])
    return True


def pdf_page_count(pdf: Path):
    """Pages via Spotlight, falling back to the PDF's own page objects."""
    try:
        out = subprocess.run(["mdls", "-raw", "-name", "kMDItemNumberOfPages", str(pdf)],
                             capture_output=True, text=True, timeout=20).stdout.strip()
        if out.isdigit():
            return int(out)
    except Exception:
        pass
    try:
        blob = pdf.read_bytes()
        counts = [int(m) for m in re.findall(rb"/Count\s+(\d+)", blob)]
        if counts:
            return max(counts)
        pages = len(re.findall(rb"/Type\s*/Page[^s]", blob))
        if pages:
            return pages
    except Exception:
        pass
    return None


def pages_page_count(docx: Path):
    """Export the docx to PDF with Pages.app and read the page count. (count, note)."""
    if sys.platform != "darwin":
        return None, "not macOS"
    if not Path("/Applications/Pages.app").exists():
        return None, "Pages.app is not installed"
    workdir = Path(tempfile.mkdtemp(prefix="fl-pages-"))
    pdf = workdir / "check.pdf"
    script = (f'tell application "Pages"\n'
              f'  set d to open POSIX file "{docx.resolve()}"\n'
              f'  export d to POSIX file "{pdf}" as PDF\n'
              f'  close d saving no\n'
              f'end tell\n')
    try:
        result = subprocess.run(["perl", "-e", "alarm 90; exec @ARGV", "osascript", "-e", script],
                                capture_output=True, text=True, timeout=95)
        if not pdf.exists():
            reason = (result.stderr or "").strip().splitlines()
            return None, (reason[-1] if reason else "Pages produced no PDF")
        count = pdf_page_count(pdf)
        if count is None:
            return None, "the exported PDF gave no page count"
        return count, ""
    except subprocess.TimeoutExpired:
        return None, "Pages did not answer in 90s (it may be waiting for automation permission)"
    except Exception as err:                    # pragma: no cover -- environment failure
        return None, str(err)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


# LibreOffice's command-line binary where the installers put it; PATH is tried first.
SOFFICE_PATHS = ("/Applications/LibreOffice.app/Contents/MacOS/soffice", "/usr/bin/soffice",
                 "/usr/lib/libreoffice/program/soffice",
                 "C:/Program Files/LibreOffice/program/soffice.exe")
SOFFICE_TIMEOUT = 120                           # seconds; a hung converter is a note, not a hang


def find_soffice():
    """The LibreOffice binary to convert with, or None."""
    for name in ("soffice", "libreoffice"):
        found = shutil.which(name)
        if found:
            return found
    for candidate in SOFFICE_PATHS:
        if Path(candidate).is_file():
            return candidate
    return None


def pypdf_page_count(pdf: Path):
    """The PDF's page count through pypdf, else through the PDF's own page objects."""
    try:
        from pypdf import PdfReader
        return len(PdfReader(str(pdf)).pages)
    except Exception:                           # no pypdf, or a PDF it cannot parse
        return pdf_page_count(pdf)


def soffice_page_count(docx: Path):
    """Export the docx to PDF with LibreOffice headless and count its pages. (count, note)."""
    soffice = find_soffice()
    if not soffice:
        return None, "LibreOffice is not installed"
    workdir = Path(tempfile.mkdtemp(prefix="fl-soffice-"))
    # A private profile, so a LibreOffice already open on this machine cannot swallow the run.
    profile = (workdir / "profile").as_uri()
    try:
        result = subprocess.run(
            [soffice, f"-env:UserInstallation={profile}", "--headless", "--convert-to", "pdf",
             "--outdir", str(workdir), str(docx.resolve())],
            capture_output=True, text=True, timeout=SOFFICE_TIMEOUT)
        pdf = workdir / (docx.stem + ".pdf")
        if not pdf.exists():
            reason = ((result.stderr or "") + (result.stdout or "")).strip().splitlines()
            return None, (reason[-1] if reason else "LibreOffice produced no PDF")
        count = pypdf_page_count(pdf)
        if count is None:
            return None, "the exported PDF gave no page count"
        return count, ""
    except subprocess.TimeoutExpired:
        return None, f"LibreOffice did not finish in {SOFFICE_TIMEOUT}s"
    except Exception as err:                    # pragma: no cover -- environment failure
        return None, str(err)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


def pages_available():
    return sys.platform == "darwin" and Path("/Applications/Pages.app").exists()


# The renderers that can verify the page count, in the order they are tried.
RENDERERS = (("Pages", pages_available, pages_page_count),
             ("LibreOffice", lambda: find_soffice() is not None, soffice_page_count))

NOT_VERIFIED = "WARNING: page count NOT verified — install LibreOffice (or run on a Mac with Pages)"


def page_renderers():
    """The renderers installed here, as (name, count function)."""
    return [(name, count) for name, present, count in RENDERERS if present()]


def verify_page_count(docx: Path, renderers):
    """(count, renderer, notes): the first renderer that answers, and why the ones before it
    did not."""
    notes = []
    for name, count_fn in renderers:
        count, note = count_fn(docx)
        if count is not None:
            return count, name, notes
        notes.append(f"{name}: {note}")
    return None, None, notes


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
        description="Build the feature list (.docx) from a pack spec: Area > Category > Feature, "
                    "on one A4 page.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Exit codes: 0 written | 1 spec error | 2 pricing leaked | "
               "3 the capability tree does not fit one page.",
    )
    parser.add_argument("spec", type=Path, help="path to packs/<slug>/pack-spec.md")
    parser.add_argument("--out", type=Path, required=True, help="output directory (created if missing)")
    tier = parser.add_mutually_exclusive_group()
    tier.add_argument("--tier-column", dest="tier_column", action="store_true", default=None,
                      help="add the 'Tier first available' column (default: on when every feature has one)")
    tier.add_argument("--no-tier-column", dest="tier_column", action="store_false",
                      help="force the 5-column reference layout")
    parser.add_argument("--fit", choices=("one-page", "none"), default="one-page",
                        help="one-page (default): walk the fit ladder and guarantee one A4 page; "
                             "none: one row per feature at 7.5pt over as many pages as it takes")
    check = parser.add_mutually_exclusive_group()
    check.add_argument("--check-pages", dest="check_pages", action="store_true", default=None,
                       help="verify the real page count by exporting to PDF with Pages.app, "
                            "else LibreOffice (default: on wherever either is installed)")
    check.add_argument("--no-check-pages", dest="check_pages", action="store_false",
                       help="skip the PDF export; the estimate is the contract")
    args = parser.parse_args(argv)

    if not args.spec.exists():
        print(f"build_feature_list: no such spec: {args.spec}", file=sys.stderr)
        return 1
    try:
        spec, _lines = packspec.load(args.spec)
    except packspec.SpecError as err:
        print(f"build_feature_list: the spec does not parse: {err}", file=sys.stderr)
        return 1

    measurer = Measurer()
    try:
        rows = flatten(spec)
        _marks, all_notes = footnote_marks(rows)
        check_notes(all_notes)
        tier_column = args.tier_column
        if tier_column is None:
            tier_column = all(r["tier"] for r in rows)
        if not dig(spec, "icp.line"):
            print("build_feature_list: `icp.line` is missing from the spec — the feature list "
                  "prints the one-liner alone, without the sentence saying who the pack is for.",
                  file=sys.stderr)
        if not measurer.exact:
            print(f"build_feature_list: measuring with an average glyph width ({measurer.reason}); "
                  f"the one-page estimate is approximate.", file=sys.stderr)

        rungs = LADDER if args.fit == "one-page" else [("full", TABLE_SIZES[0])]
    except SpecError as err:
        print(f"build_feature_list: {err}", file=sys.stderr)
        return 1

    renderers = page_renderers()
    check_pages = args.check_pages
    if check_pages is None:
        check_pages = bool(renderers)           # default: verify wherever any renderer is here

    args.out.mkdir(parents=True, exist_ok=True)
    path = args.out / f"{dig(spec, 'meta.slug', 'pack')}-feature-list.docx"
    built_from = spec_stamp.stamp(args.spec)    # which spec this file reflects (CON006 / CON007)
    last = None

    for mode, size in rungs:
        rung_tier = tier_column and mode == "full"
        table_h, budget = estimate(spec, rows, measurer, mode=mode, size=size,
                                   tier_column=rung_tier)
        last = (mode, size, table_h, budget)
        if args.fit == "one-page" and table_h > budget:
            continue                            # the estimate already says no; do not write it

        document, title, headers, _widths = build(
            spec, rows, mode=mode, size=size, tier_column=rung_tier,
            repeat_header_row=(args.fit == "none"))

        leaks = pricing_leak(document, spec)
        if leaks:
            print(f"build_feature_list: PRICING -- {', '.join(leaks)} reached the feature list. "
                  f"Pricing belongs on the one-pager and the deck, never here.", file=sys.stderr)
            return 2

        document.core_properties.identifier = built_from
        document.save(str(path))
        if not add_font_table_entries(path):
            print("build_feature_list: could not name the brand faces in word/fontTable.xml; "
                  "Word will guess a substitute where Azurio or Replica LL TT is absent.",
                  file=sys.stderr)
        try:
            Document(str(path))                 # the post-processed zip must still open
        except Exception as err:
            print(f"build_feature_list: the written file no longer opens ({err}).", file=sys.stderr)
            return 1

        verified, warning = None, None
        if check_pages:
            count, renderer, notes = verify_page_count(path, renderers)
            if count is None:
                warning = ("WARNING: page count NOT verified — " + "; ".join(notes)
                           if notes else NOT_VERIFIED)
            elif count > 1 and args.fit == "one-page":
                print(f"build_feature_list: {mode} at {size:g}pt rendered {count} pages in "
                      f"{renderer}; trying the next setting.", file=sys.stderr)
                path.unlink(missing_ok=True)
                last = (mode, size, table_h, budget)
                continue                        # the real count beats the estimate
            else:
                verified = f"page count verified with {renderer}: {count}"
        elif args.check_pages is None:
            warning = NOT_VERIFIED              # nothing here can render a .docx
        else:
            verified = "page count not verified (--no-check-pages): the estimate is the contract"

        report(path, spec, rows, title, headers, mode, size, table_h, budget,
               args.fit, verified, warning, measurer.source_line(), built_from)
        return 0

    print(fit_report(rows, last[2], last[3], f"{last[0]} at {last[1]:g}pt"), file=sys.stderr)
    return 3


def report(path, spec, rows, title, headers, mode, size, table_h, budget, fit, verified,
           warning=None, measured=None, built_from=None):
    areas = len({r["area"] for r in rows})
    categories = len({(r["area"], r["category"]) for r in rows})
    counts = {k: sum(1 for r in rows if r["status"] == k) for k in GLYPHS}
    layout = ("one row per category, features listed inline (compact)" if mode == "compact"
              else "one row per feature")
    print(f"DOCX  {path}")
    print(f"      {title}")
    if built_from:
        print(f"      spec stamp: {built_from}")
    print(f"      {areas} areas / {categories} categories / {len(rows)} features, "
          f"{len(headers)} columns")
    print(f"      status: {counts['available']} available, {counts['partial']} partial, "
          f"{counts['roadmap']} roadmap")
    if fit == "none":
        print(f"      layout: {layout} at {size:g}pt, several pages allowed (--fit none); "
              f"estimated {table_h / budget * 100:.0f}% of one page")
    else:
        print(f"      estimated {table_h / budget * 100:.0f}% of one page, {layout} at {size:g}pt")
    if mode == "compact":
        print("      compact mode dropped the Current status and Tier first available columns; "
              "each feature carries its glyph inline.")
    if measured:
        print(f"      {measured}")
    if verified:
        print(f"      {verified}")
    if warning:
        print(warning)


if __name__ == "__main__":
    sys.exit(main())
