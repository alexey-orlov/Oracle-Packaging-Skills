#!/usr/bin/env python3
"""pair_sheet.py — the built deck beside the reference, slide by slide.

    pair_sheet.py <reference renders dir> <built renders dir> <out.png> [--scale 0.5]

Both directories hold `slide-NN.png` renders (tools/render_probe.sh says how to
make them on this machine). Each row of the sheet is one slide: the reference on
the left, the build on the right, so a band that changed height, a card that left
its band, a relabelled card or an added row shows as a difference between two
pictures instead of as something a reader has to remember. Built decks and the
reference may order slides differently (the reference's architecture is slide 7,
the build's is slide 8): pass `--map 7=6,8=7` to pair built slide 7 with reference
slide 6, and so on. Exit 2 when either folder has no renders.
"""
import argparse
import re
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:  # pragma: no cover
    print("pair_sheet: Pillow is not installed (pip install Pillow)", file=sys.stderr)
    sys.exit(2)


def renders(folder: Path) -> dict[int, Path]:
    out = {}
    for p in sorted(folder.glob("slide-*.png")):
        m = re.search(r"slide-(\d+)", p.name)
        if m:
            out[int(m.group(1))] = p
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("reference")
    ap.add_argument("built")
    ap.add_argument("out")
    ap.add_argument("--scale", type=float, default=0.5)
    ap.add_argument("--map", default="", help="built=reference pairs, e.g. 7=6,8=7")
    a = ap.parse_args(argv)
    ref, built = renders(Path(a.reference)), renders(Path(a.built))
    if not ref or not built:
        print("pair_sheet: no slide-NN.png renders in one of the folders", file=sys.stderr)
        return 2
    pairs = {int(k): int(v) for k, v in (x.split("=") for x in a.map.split(",") if x)}
    sample = Image.open(next(iter(built.values())))
    w, h = int(sample.width * a.scale), int(sample.height * a.scale)
    gap, label_h = 24, 28
    rows = sorted(built)
    sheet = Image.new("RGB", (2 * w + 3 * gap, len(rows) * (h + label_h + gap) + gap), "#e9ecef")
    draw = ImageDraw.Draw(sheet)
    y = gap
    for n in rows:
        r = ref.get(pairs.get(n, n))
        draw.text((gap, y), f"reference {pairs.get(n, n)}" if r else "reference — none", fill="#333")
        draw.text((2 * gap + w, y), f"built {n}", fill="#333")
        y += label_h
        if r:
            sheet.paste(Image.open(r).convert("RGB").resize((w, h)), (gap, y))
        sheet.paste(Image.open(built[n]).convert("RGB").resize((w, h)), (2 * gap + w, y))
        y += h + gap
    sheet.save(a.out)
    print(f"{a.out} ({sheet.width}x{sheet.height}) — {len(rows)} slide pair(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
