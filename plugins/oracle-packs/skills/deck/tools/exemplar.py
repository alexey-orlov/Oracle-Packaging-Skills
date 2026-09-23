"""Exemplar deck surgery — fill the reference deck's own slides instead of drawing new ones.

The rule this module exists to enforce: **geometry, fonts, corners, colours and
icons come from the exemplar file, never from code**. Every helper here either
edits the *text* inside a shape that already exists, swaps a picture inside a
frame that already exists, or clones an existing shape/row/slide as a prototype.
Nothing creates a styled shape from constants.

Used by `build_deck_v2.py`. Depends on python-pptx only; the brand tokens, the
spec accessor and the fit estimator live in `deckkit.py`.

Vocabulary
----------
*slot*      a semantic name (``use_case.problem.points``) mapped to a shape id
            on one exemplar slide by ``assets/exemplar/slots.json``.
*prototype* an existing shape / paragraph / table row whose XML is deep-copied
            to make a peer. A deck that needs five source boxes clones the one
            the exemplar has; it never builds a sixth style.
"""

from __future__ import annotations

import copy
import io
from pathlib import Path
from typing import Iterable, Sequence

from pptx import Presentation
from pptx.oxml.ns import qn
from pptx.util import Emu

EMU_IN = 914400
RELS_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


def inch(v: float) -> int:
    return int(round(v * EMU_IN))


def to_in(v: int | None) -> float:
    return 0.0 if v is None else v / EMU_IN


# --------------------------------------------------------------------------
# Opening and slide-level surgery
# --------------------------------------------------------------------------

def open_exemplar(path: str | Path) -> Presentation:
    """Open a **copy in memory**. The exemplar file on disk is never touched."""
    return Presentation(io.BytesIO(Path(path).read_bytes()))


def slide_count(prs: Presentation) -> int:
    return len(prs.slides._sldIdLst)


def arrange(prs: Presentation, order: Sequence[int]) -> None:
    """Keep only the slides in `order` (0-based, current indices), in that order.

    Slides left out are dropped together with their part relationship, so their
    media leaves the package with them.
    """
    lst = prs.slides._sldIdLst
    items = list(lst)
    keep = [items[i] for i in order]
    for el in items:
        lst.remove(el)
    for el in keep:
        lst.append(el)
    kept = set(order)
    for i, el in enumerate(items):
        if i in kept:
            continue
        rId = el.get(RELS_NS + "id")
        try:
            prs.part.drop_rel(rId)
        except KeyError:
            pass


def duplicate_slide(prs: Presentation, index: int):
    """Append a copy of slide `index` (0-based) and return it.

    The shape tree is deep-copied and every non-layout relationship of the
    source part is re-added under **the same rId**, so pictures, media and
    hyperlinks inside the copied XML still resolve.
    """
    src = prs.slides[index]
    dest = prs.slides.add_slide(src.slide_layout)
    for shp in list(dest.shapes):
        shp._element.getparent().remove(shp._element)
    for shp in src.shapes:
        dest.shapes._spTree.append(copy.deepcopy(shp._element))
    from pptx.opc.constants import RELATIONSHIP_TARGET_MODE as RTM
    from pptx.opc.package import _Relationship

    rels = dest.part.rels
    for rId, rel in src.part.rels.items():
        if rel.reltype.endswith("slideLayout") or rId in rels:
            continue
        rels._rels[rId] = _Relationship(
            rels._base_uri, rId, rel.reltype,
            target_mode=RTM.EXTERNAL if rel.is_external else RTM.INTERNAL,
            target=rel.target_ref if rel.is_external else rel._target)
    return dest


def clear_notes(slide) -> None:
    if slide.has_notes_slide:
        slide.notes_slide.notes_text_frame.text = ""


# --------------------------------------------------------------------------
# Finding shapes
# --------------------------------------------------------------------------

def iter_shapes(container, recurse: bool = True):
    for shp in container.shapes:
        yield shp
        if recurse and shp.shape_type == 6:          # GROUP
            yield from iter_shapes(shp, recurse)


def by_id(slide, shape_id: int):
    for shp in iter_shapes(slide):
        if shp.shape_id == shape_id:
            return shp
    raise KeyError(f"shape id {shape_id} not on this slide")


def find_id(slide, shape_id: int):
    try:
        return by_id(slide, shape_id)
    except KeyError:
        return None


def delete_shape(shp) -> None:
    shp._element.getparent().remove(shp._element)


def delete_ids(slide, ids: Iterable[int]) -> None:
    for sid in ids:
        shp = find_id(slide, sid)
        if shp is not None:
            delete_shape(shp)


def set_frame(shp, x=None, y=None, w=None, h=None) -> None:
    """Move/resize in inches. Used only where the anatomy calls for it."""
    if x is not None:
        shp.left = inch(x)
    if y is not None:
        shp.top = inch(y)
    if w is not None:
        shp.width = inch(w)
    if h is not None:
        shp.height = inch(h)


def frame_in(shp) -> tuple[float, float, float, float]:
    return to_in(shp.left), to_in(shp.top), to_in(shp.width), to_in(shp.height)


def group_scale_x(group) -> float:
    """How much a group squeezes its children horizontally (ext / chExt).

    A shape inside a group carries its coordinates in the group's own child space,
    so `frame_in` on a child reports a width that is not what renders. Multiply by
    this to get slide inches.
    """
    if group is None:
        return 1.0
    xfrm = group._element.find(qn("p:grpSpPr"))
    xfrm = xfrm.find(qn("a:xfrm")) if xfrm is not None else None
    if xfrm is None:
        return 1.0
    ext, ch_ext = xfrm.find(qn("a:ext")), xfrm.find(qn("a:chExt"))
    if ext is None or ch_ext is None or not int(ch_ext.get("cx", 0)):
        return 1.0
    return int(ext.get("cx")) / int(ch_ext.get("cx"))


def inner_box_in(shp) -> tuple[float, float]:
    """Usable (width, height) in inches — the frame minus the text insets."""
    w, h = to_in(shp.width), to_in(shp.height)
    try:
        tf = shp.text_frame
        w -= to_in(tf.margin_left) + to_in(tf.margin_right)
        h -= to_in(tf.margin_top) + to_in(tf.margin_bottom)
    except Exception:
        pass
    return max(w, 0.1), max(h, 0.1)


def _next_shape_id(slide) -> int:
    used = {shp.shape_id for shp in iter_shapes(slide)}
    return max(used) + 1 if used else 2


def clone_shape(slide, proto, x=None, y=None, w=None, h=None):
    """Deep-copy `proto` onto `slide` (it may live on another slide) and return it."""
    el = copy.deepcopy(proto._element)
    new_id = _next_shape_id(slide)
    for cNvPr in el.iter(qn("p:cNvPr")):
        cNvPr.set("id", str(new_id))
        new_id += 1
    slide.shapes._spTree.append(el)
    shp = slide.shapes[-1]
    set_frame(shp, x, y, w, h)
    return shp


# --------------------------------------------------------------------------
# Text: fill a shape without touching its formatting
# --------------------------------------------------------------------------

_RUNLIKE = (qn("a:r"), qn("a:br"), qn("a:fld"))


def paragraph_prototypes(shp) -> list:
    """Deep copies of the shape's paragraphs, taken before any edit."""
    return [copy.deepcopy(p._p) for p in shp.text_frame.paragraphs]


def _strip_runs(p_el) -> None:
    for child in list(p_el):
        if child.tag in _RUNLIKE:
            p_el.remove(child)


def _runs_of(p_el) -> list:
    return [c for c in p_el if c.tag == qn("a:r")]


def _run_signature(r_el) -> tuple:
    """(bold, size, colour, font) — what makes a run look different from its neighbour."""
    rPr = r_el.find(qn("a:rPr"))
    if rPr is None:
        return (None, None, None, None)
    colour = None
    fill = rPr.find(qn("a:solidFill"))
    if fill is not None:
        srgb = fill.find(qn("a:srgbClr"))
        scheme = fill.find(qn("a:schemeClr"))
        colour = srgb.get("val") if srgb is not None else (
            scheme.get("val") if scheme is not None else None)
    latin = rPr.find(qn("a:latin"))
    return (rPr.get("b"), rPr.get("sz"), colour,
            latin.get("typeface") if latin is not None else None)


def _set_run_text(r_el, text: str) -> None:
    t = r_el.find(qn("a:t"))
    if t is None:
        t = r_el.makeelement(qn("a:t"), {})
        r_el.append(t)
    t.text = text
    # Keep leading/trailing spaces the caller asked for.
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")


def _fill_paragraph(p_el, texts: Sequence[str]):
    """Set the paragraph's run texts, reusing the paragraph's own run formatting.

    Text *i* goes into the *i*-th **formatting-distinct** run of the prototype —
    so "bold lead + regular tail" lands on the bold run and the first regular
    run even when the exemplar split its lead across four bold runs. Runs that
    are not needed are removed; more texts than distinct runs clone the last.
    """
    texts = [t for t in texts]
    runs = _runs_of(p_el)
    if not runs:
        r = p_el.makeelement(qn("a:r"), {})
        _set_run_text(r, "")
        end = p_el.find(qn("a:endParaRPr"))
        if end is not None:
            end.addprevious(r)
        else:
            p_el.append(r)
        runs = [r]
    chosen: list = []
    seen: set = set()
    for r in runs:
        sig = _run_signature(r)
        if sig not in seen:
            seen.add(sig)
            chosen.append(r)
    while len(chosen) < len(texts):
        clone = copy.deepcopy(chosen[-1])
        chosen[-1].addnext(clone)
        chosen.append(clone)
    keep = chosen[:len(texts)]
    for r in runs:
        if r not in keep and r.getparent() is p_el:
            p_el.remove(r)
    for r in chosen[len(texts):]:
        if r.getparent() is p_el:
            p_el.remove(r)
    for r, text in zip(keep, texts):
        _set_run_text(r, text)
    return p_el


def set_paragraphs(shp, specs: Sequence[tuple[int, Sequence[str]]],
                   protos: Sequence | None = None) -> None:
    """Rebuild the shape's text from prototype paragraphs.

    `specs` is a list of ``(prototype_index, [run_text, ...])``. Each entry
    clones the prototype paragraph (its indent, bullet, line spacing and run
    formatting) and fills its runs. An out-of-range prototype index falls back
    to the last available paragraph.
    """
    tf = shp.text_frame
    body = tf._txBody
    if protos is None:
        protos = paragraph_prototypes(shp)
    if not protos:
        protos = [copy.deepcopy(tf.paragraphs[0]._p)]
    for p in list(tf.paragraphs):
        body.remove(p._p)
    if not specs:
        specs = [(0, [""])]
    for proto_ix, texts in specs:
        proto = protos[min(max(proto_ix, 0), len(protos) - 1)]
        p_el = copy.deepcopy(proto)
        _strip_runs(p_el)
        for child in list(p_el):
            if child.tag == qn("a:endParaRPr"):
                p_el.remove(child)
        proto_runs = _runs_of(copy.deepcopy(proto))
        for r in proto_runs:
            p_el.append(r)
        _fill_paragraph(p_el, texts or [""])
        body.append(p_el)


def fill_text(shp, text: str) -> None:
    """One paragraph, one run — the first run's formatting kept."""
    set_paragraphs(shp, [(0, [str(text)])])


def fill_lines(shp, lines: Sequence[str]) -> None:
    """Line i into paragraph i (e.g. a box whose bold name sits above a sub-line)."""
    set_paragraphs(shp, [(i, [str(t)]) for i, t in enumerate(lines)])


def fill_lead(shp, lead: str, rest: str = "") -> None:
    """A bold lead clause followed by regular text, in one paragraph."""
    texts = [lead] if not rest else [lead, rest]
    set_paragraphs(shp, [(0, texts)])


def fill_points(shp, points: Sequence[str], proto: int = 0,
                split: str | None = None,
                head: Sequence[tuple[int, Sequence[str]]] = ()) -> None:
    """Bulleted body: one cloned prototype paragraph per point.

    `split` (e.g. ``":"``) puts the text before the separator in the first run
    (bold in every card the exemplar has) and the remainder in the second.
    `head` prepends paragraphs built from other prototypes (a lead sentence).
    """
    specs = list(head)
    for pt in points:
        text = str(pt).strip()
        if split and split in text:
            a, b = text.split(split, 1)
            specs.append((proto, [a, split + b]))
        else:
            specs.append((proto, [text]))
    set_paragraphs(shp, specs)


def distinct_runs(p_el) -> int:
    """How many formatting-distinct runs a prototype paragraph offers."""
    seen: set = set()
    for r in _runs_of(p_el):
        seen.add(_run_signature(r))
    return max(len(seen), 1)


def last_run_pt(p_el) -> float | None:
    """Point size of the last formatting-distinct run (the prose run in a glyph cell)."""
    runs, seen, chosen = _runs_of(p_el), set(), []
    for r in runs:
        sig = _run_signature(r)
        if sig not in seen:
            seen.add(sig)
            chosen.append(r)
    if not chosen:
        return None
    sz = _run_signature(chosen[-1])[1]
    return float(sz) / 100.0 if sz else None


def shape_text(shp) -> str:
    try:
        return shp.text_frame.text
    except Exception:
        return ""


def run_pt(shp, para: int = 0, run: int = 0) -> float | None:
    """Point size of one run — the exemplar's own size, for the fit estimate."""
    try:
        p = shp.text_frame.paragraphs[para]
        r = p.runs[run]
        if r.font.size is not None:
            return r.font.size.pt
    except Exception:
        pass
    return None


def run_bold(shp, para: int = 0, run: int = 0) -> bool:
    try:
        return bool(shp.text_frame.paragraphs[para].runs[run].font.bold)
    except Exception:
        return False


# --------------------------------------------------------------------------
# Pictures
# --------------------------------------------------------------------------

def _image_aspect(path: str | Path) -> float | None:
    try:
        from PIL import Image
        with Image.open(path) as im:
            w, h = im.size
        return (w / h) if h else None
    except Exception:
        return None


def replace_picture(pic, image_path: str | Path, cover: bool = True) -> None:
    """Swap the image inside an existing picture frame, keeping the frame.

    With `cover`, the new image is centre-cropped (via ``a:srcRect``) to the
    frame's aspect ratio, so it fills the slot the way the exemplar's photo did
    instead of stretching.
    """
    image_path = str(image_path)
    slide_part = pic.part
    image_part, rId = slide_part.get_or_add_image_part(image_path)
    blip = pic._element.find(".//" + qn("a:blip"))
    if blip is None:
        raise ValueError("shape has no a:blip — not a picture")
    blip.set(RELS_NS + "embed", rId)
    blipFill = pic._element.find(".//" + qn("p:blipFill"))
    if blipFill is None:
        return
    for old in blipFill.findall(qn("a:srcRect")):
        blipFill.remove(old)
    if not cover:
        return
    src_aspect = _image_aspect(image_path)
    frame_aspect = (pic.width / pic.height) if pic.height else None
    if not src_aspect or not frame_aspect:
        return
    srcRect = blipFill.makeelement(qn("a:srcRect"), {})
    if src_aspect > frame_aspect:                     # too wide → crop sides
        keep = frame_aspect / src_aspect
        off = int(round((1 - keep) / 2 * 100000))
        srcRect.set("l", str(off))
        srcRect.set("r", str(off))
    elif src_aspect < frame_aspect:                   # too tall → crop top/bottom
        keep = src_aspect / frame_aspect
        off = int(round((1 - keep) / 2 * 100000))
        srcRect.set("t", str(off))
        srcRect.set("b", str(off))
    blip.addnext(srcRect)


def empty_picture_frame(slide, pic, caption: str, caption_proto=None,
                        fill: str = "F4F6F7", line: str = "B6BEC4"):
    """Replace a picture with an explicit empty container carrying a caption.

    Rule 3 (slide-design): an absent asset is an empty *container*, not a gap.
    The caption's type comes from `caption_proto` — a text shape on the same
    slide — so the placeholder is still in the deck's own voice.
    """
    x, y, w, h = frame_in(pic)
    delete_shape(pic)
    box = slide.shapes.add_shape(1, inch(x), inch(y), inch(w), inch(h))   # rect
    box.name = "Image slot"
    from pptx.dml.color import RGBColor
    box.fill.solid()
    box.fill.fore_color.rgb = RGBColor.from_string(fill)
    box.line.color.rgb = RGBColor.from_string(line)
    box.line.width = Emu(9525)
    ln = box._element.find(".//" + qn("a:ln"))
    if ln is not None:
        dash = ln.makeelement(qn("a:prstDash"), {"val": "dash"})
        ln.append(dash)
    tf = box.text_frame
    tf.word_wrap = True
    if caption_proto is not None:
        protos = paragraph_prototypes(caption_proto)
        body = tf._txBody
        for p in list(tf.paragraphs):
            body.remove(p._p)
        p_el = copy.deepcopy(protos[0])
        _strip_runs(p_el)
        for child in list(p_el):
            if child.tag == qn("a:endParaRPr"):
                p_el.remove(child)
        for r in _runs_of(copy.deepcopy(protos[0])):
            p_el.append(r)
        _fill_paragraph(p_el, [caption])
        body.append(p_el)
    else:
        tf.text = caption
    from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    for p in tf.paragraphs:
        p.alignment = PP_ALIGN.CENTER
    return box


# --------------------------------------------------------------------------
# Tables
# --------------------------------------------------------------------------

def clone_table_row(table, src_index: int, at: int | None = None):
    """Duplicate row `src_index`; insert at `at` (default: right after it)."""
    tbl = table._tbl
    rows = tbl.findall(qn("a:tr"))
    proto = rows[src_index]
    new = copy.deepcopy(proto)
    if at is None or at >= len(rows):
        rows[-1].addnext(new)
    else:
        rows[at].addprevious(new)
    return new


def delete_table_row(table, index: int) -> None:
    tbl = table._tbl
    rows = tbl.findall(qn("a:tr"))
    tbl.remove(rows[index])


def match_row_count(table, want: int, proto_index: int, first_index: int) -> None:
    """Grow/shrink the block of rows starting at `first_index` to `want` rows."""
    have = len(table._tbl.findall(qn("a:tr"))) - first_index
    while have < want:
        clone_table_row(table, proto_index, at=first_index + have)
        have += 1
    while have > want:
        delete_table_row(table, first_index + have - 1)
        have -= 1


def cell_paragraph_prototypes(cell) -> list:
    return [copy.deepcopy(p._p) for p in cell.text_frame.paragraphs]


def set_cell(cell, specs: Sequence[tuple[int, Sequence[str]]],
             protos: Sequence | None = None) -> None:
    """`set_paragraphs` for a table cell — the cell's own run formatting kept."""
    tf = cell.text_frame
    body = tf._txBody
    if protos is None:
        protos = cell_paragraph_prototypes(cell)
    if not protos:
        protos = [copy.deepcopy(tf.paragraphs[0]._p)]
    for p in list(tf.paragraphs):
        body.remove(p._p)
    for proto_ix, texts in (specs or [(0, [""])]):
        proto = protos[min(max(proto_ix, 0), len(protos) - 1)]
        p_el = copy.deepcopy(proto)
        _strip_runs(p_el)
        for child in list(p_el):
            if child.tag == qn("a:endParaRPr"):
                p_el.remove(child)
        for r in _runs_of(copy.deepcopy(proto)):
            p_el.append(r)
        _fill_paragraph(p_el, texts or [""])
        body.append(p_el)


def fill_cell(cell, text: str) -> None:
    set_cell(cell, [(0, [str(text)])])


def copy_cell_runs(dst_cell, src_cell) -> None:
    """Give `dst_cell` the run formatting of `src_cell` (same text kept)."""
    texts = [[r.text for r in p.runs] or [""] for p in dst_cell.text_frame.paragraphs]
    protos = cell_paragraph_prototypes(src_cell)
    set_cell(dst_cell, [(min(i, len(protos) - 1), t) for i, t in enumerate(texts)], protos)


def cell_run_pt(cell, para: int = 0, run: int = 0) -> float | None:
    try:
        r = cell.text_frame.paragraphs[para].runs[run]
        if r.font.size is not None:
            return r.font.size.pt
    except Exception:
        pass
    return None


def table_frame(shape):
    return frame_in(shape)


# --------------------------------------------------------------------------
# Connectors (architecture diagram)
# --------------------------------------------------------------------------

def place_connector(cxn, x1: float, y1: float, x2: float, y2: float) -> None:
    """Point a cloned connector from (x1,y1) to (x2,y2), inches, via flipH/flipV."""
    el = cxn._element
    spPr = el.find(qn("p:spPr"))
    xfrm = spPr.find(qn("a:xfrm"))
    if xfrm is None:
        xfrm = spPr.makeelement(qn("a:xfrm"), {})
        spPr.insert(0, xfrm)
    off = xfrm.find(qn("a:off"))
    ext = xfrm.find(qn("a:ext"))
    if off is None:
        off = xfrm.makeelement(qn("a:off"), {})
        xfrm.append(off)
    if ext is None:
        ext = xfrm.makeelement(qn("a:ext"), {})
        xfrm.append(ext)
    off.set("x", str(inch(min(x1, x2))))
    off.set("y", str(inch(min(y1, y2))))
    ext.set("cx", str(max(inch(abs(x2 - x1)), 1)))
    ext.set("cy", str(max(inch(abs(y2 - y1)), 0)))
    for attr, cond in (("flipH", x2 < x1), ("flipV", y2 < y1)):
        if cond:
            xfrm.set(attr, "1")
        elif attr in xfrm.attrib:
            del xfrm.attrib[attr]


def set_connector_geom(cxn, prst: str, adj: int | None = None) -> None:
    """Swap the connector's preset geometry (``straightConnector1`` / ``bentConnector3``).

    `adj` (0-100000) moves an elbow's vertical segment along the gap, so several
    elbows in the same corridor do not lie on top of each other.
    """
    geom = cxn._element.find(".//" + qn("a:prstGeom"))
    if geom is None:
        return
    geom.set("prst", prst)
    for av in geom.findall(qn("a:avLst")):
        geom.remove(av)
    avLst = geom.makeelement(qn("a:avLst"), {})
    if adj is not None:
        gd = avLst.makeelement(qn("a:gd"), {"name": "adj1", "fmla": f"val {int(adj)}"})
        avLst.append(gd)
    geom.append(avLst)
