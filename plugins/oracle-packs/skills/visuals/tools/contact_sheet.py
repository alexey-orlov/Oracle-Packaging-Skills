#!/usr/bin/env python3
"""Lay the candidates out as one labelled sheet the owner can look at.

    contact_sheet.py <dir> --out <sheet.png> [--label-from json] [--title "..."]
                     [--max-width 2400] [--slots today,tomorrow]

One row per slot, the candidates lettered A / B / C across it, each with one caption line naming the
creator, the source and the licence. Icons are drawn twice per cell — white on the deck's dark panel
and ink on a light ground — because that is how they will actually appear, and an icon that reads in
one and not the other is a bad choice that a single preview would hide.

The sheet is what the owner looks at while answering; open it beside the conversation before the
question, never after. Exit codes: 0 written · 1 nothing to lay out, or a usage error.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from visuals_common import EXIT_OK, EXIT_USAGE, eprint, read_sidecar  # noqa: E402

from PIL import Image, ImageDraw, ImageFont

IMG_EXT = (".png", ".jpg", ".jpeg", ".webp")
INK = (0x26, 0x28, 0x2B)
PAPER = (0xF7, 0xF7, 0xF5)
PANEL = (0x1F, 0x2A, 0x44)      # a stand-in for the deck's dark blue panel
MUTED = (0x6B, 0x70, 0x76)
RULE = (0xD8, 0xD8, 0xD4)

FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
BOLD_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


def font(size: int, bold: bool = False):
    for p in (BOLD_CANDIDATES if bold else FONT_CANDIDATES):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                continue
    return ImageFont.load_default()


def clip(draw, text: str, f, width: int) -> str:
    text = (text or "-").replace("\n", " ")
    if draw.textlength(text, font=f) <= width:
        return text
    while text and draw.textlength(text + "…", font=f) > width:
        text = text[:-1]
    return text + "…"


def collect(directory: str, label_from: str, only: list[str] | None) -> dict[str, list[dict]]:
    rows: dict[str, list[dict]] = {}
    for path in sorted(glob.glob(os.path.join(directory, "*"))):
        if not path.lower().endswith(IMG_EXT):
            continue
        rec = None
        if label_from == "json":
            try:
                rec = read_sidecar(path)
            except (FileNotFoundError, ValueError):
                rec = None
        if rec is None:
            rec = {"slot": os.path.basename(os.path.dirname(path)) or "candidates",
                   "title": os.path.basename(path), "creator": "-", "source": "-",
                   "licence_name": "licence not recorded", "kind": "photo"}
        slot = rec.get("slot", "candidates")
        if only and slot not in only:
            continue
        rec["_path"] = path
        # Keep the letter the search tool gave the file, so the sheet the owner looks at and the
        # search output the agent read use the same names for the same picture.
        m = re.search(r"-([A-H])-", os.path.basename(path))
        rec["_letter"] = m.group(1) if m else None
        rows.setdefault(slot, []).append(rec)
    # An icon fetched in two colours is ONE candidate: keep the ink render and remember the pair.
    for slot, items in rows.items():
        if not items or items[0].get("kind") != "icon":
            continue
        merged: dict[str, dict] = {}
        for rec in items:
            key = rec.get("title") or rec["_path"]
            base = merged.setdefault(key, dict(rec, _white=None, _ink=None))
            if rec["_path"].endswith("-white.png"):
                base["_white"] = rec["_path"]
            elif rec["_path"].endswith("-ink.png"):
                base["_ink"] = rec["_path"]
            else:
                base["_ink"] = base["_ink"] or rec["_path"]
        rows[slot] = list(merged.values())
    return rows


def paste_fit(sheet, img, box):
    x, y, w, h = box
    im = img.copy()
    im.thumbnail((w, h), Image.LANCZOS)
    sheet.paste(im, (x + (w - im.width) // 2, y + (h - im.height) // 2),
                im if im.mode == "RGBA" else None)


CAPTION_H = 96          # title + two meta lines under every cell


def draw_cell(sheet, draw, rec, x, y, cw, ch, letter, fonts):
    f_badge, f_title, f_meta = fonts
    img_h = ch - CAPTION_H
    draw.rectangle([x, y, x + cw, y + img_h], fill=(0xEE, 0xEE, 0xEA), outline=RULE)

    if rec.get("kind") == "icon":
        half = cw // 2
        draw.rectangle([x, y, x + half, y + img_h], fill=PANEL)
        draw.rectangle([x + half, y, x + cw, y + img_h], fill=(0xFF, 0xFF, 0xFF), outline=RULE)
        pad = int(img_h * 0.16)
        if rec.get("_white") and os.path.exists(rec["_white"]):
            paste_fit(sheet, Image.open(rec["_white"]).convert("RGBA"),
                      (x + pad, y + pad, half - 2 * pad, img_h - 2 * pad))
        if rec.get("_ink") and os.path.exists(rec["_ink"]):
            paste_fit(sheet, Image.open(rec["_ink"]).convert("RGBA"),
                      (x + half + pad, y + pad, half - 2 * pad, img_h - 2 * pad))
        draw.line([x + half, y, x + half, y + img_h], fill=RULE)
    else:
        paste_fit(sheet, Image.open(rec["_path"]).convert("RGB"), (x, y, cw, img_h))

    # The letter badge — outlined, ink numeral (slide-design rule 8: no heavy black chips).
    b = 46
    draw.rectangle([x + 10, y + 10, x + 10 + b, y + 10 + b], fill=PAPER, outline=INK, width=3)
    draw.text((x + 10 + b // 2, y + 10 + b // 2), letter, font=f_badge, fill=INK, anchor="mm")

    ty = y + img_h + 12
    draw.text((x, ty), clip(draw, rec.get("title") or "-", f_title, cw), font=f_title, fill=INK)
    ty += 26
    # An icon's creator IS its set, so the two would read "Tabler Icons · Tabler Icons".
    parts, meta = [], []
    for v in [rec.get("creator") or "-", rec.get("source") or "-",
              rec.get("licence_name") or rec.get("licence") or "licence not recorded"]:
        if str(v) not in parts:
            parts.append(str(v))
            meta.append(str(v))
    meta = " · ".join(meta)
    draw.text((x, ty), clip(draw, meta, f_meta, cw), font=f_meta, fill=MUTED)
    ty += 22
    dims = f"{rec.get('width', 0)}×{rec.get('height', 0)}" if rec.get("width") else ""
    tail = " · ".join(v for v in [os.path.basename(rec["_path"]), dims] if v)
    draw.text((x, ty), clip(draw, tail, f_meta, cw), font=f_meta, fill=MUTED)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("directory")
    ap.add_argument("--out", required=True)
    ap.add_argument("--label-from", default="json", choices=["json", "filename"])
    ap.add_argument("--title", default="")
    ap.add_argument("--max-width", type=int, default=2400)
    ap.add_argument("--slots", default="", help="comma-separated slots to include (default: all)")
    args = ap.parse_args(argv)

    only = [s.strip() for s in args.slots.split(",") if s.strip()] or None
    rows = collect(args.directory, args.label_from, only)
    if not rows:
        eprint(f"nothing to lay out in {args.directory}")
        return EXIT_USAGE

    per_row = max(len(v) for v in rows.values())
    margin, gap, head_h = 40, 28, 46
    width = min(args.max_width, 2400)
    cw = (width - 2 * margin - gap * (per_row - 1)) // per_row
    # Icons are square; photographs are laid out 3:2, which is the shape the deck's picture frames
    # use. Peer cells keep one geometry per sheet (slide-design rule 2).
    all_icons = all(r.get("kind") == "icon" for items in rows.values() for r in items)
    ch = int(cw * (0.62 if all_icons else 0.67)) + CAPTION_H
    row_h = head_h + ch + 34
    title_h = 64 if args.title else 24
    height = title_h + len(rows) * row_h + margin

    sheet = Image.new("RGB", (width, height), PAPER)
    draw = ImageDraw.Draw(sheet)
    fonts = (font(28, True), font(20, True), font(17))
    f_title, f_row = font(30, True), font(22, True)

    if args.title:
        draw.text((margin, 26), args.title, font=f_title, fill=INK)

    y = title_h
    for slot, items in rows.items():
        draw.text((margin, y + 8), slot, font=f_row, fill=INK)
        draw.line([margin, y + head_h - 10, width - margin, y + head_h - 10], fill=RULE, width=2)
        for i, rec in enumerate(items[:per_row]):
            x = margin + i * (cw + gap)
            draw_cell(sheet, draw, rec, x, y + head_h, cw, ch,
                      rec.get("_letter") or "ABCDEFGH"[i], fonts)
        y += row_h

    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    sheet.save(args.out)
    print(f"{args.out}  ({sheet.width}×{sheet.height}, {len(rows)} slot(s), "
          f"{sum(len(v) for v in rows.values())} candidate(s))")
    for slot, items in rows.items():
        print(f"  {slot}: " + ", ".join(
            f"{r.get('_letter') or 'ABCDEFGH'[i]}={os.path.basename(r['_path'])}"
            for i, r in enumerate(items)))
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
