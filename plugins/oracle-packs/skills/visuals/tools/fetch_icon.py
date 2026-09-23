#!/usr/bin/env python3
"""Fetch one openly licensed icon and render it for the deck.

    fetch_icon.py <icon-name> --out <dir> [--color white|ink|both] [--set tabler|lucide]
                  [--size 512] [--slot vertical:0]

Tabler Icons (MIT) is the primary set, Lucide (ISC) the fallback. Two routes, in this order:

  1. the PNG package on jsDelivr (`@tabler/icons-png`) — already black on transparent, 240 px;
  2. the SVG from the set's repository, rasterized with QuickLook (`qlmanage -t`), which returns a
     square PNG on white — the alpha channel is then rebuilt as 255 minus luminance.

Route 1 is preferred where it answers and the wanted size is 240 px or less; above that the SVG
route is taken instead, because upscaling a 240 px bitmap softens the strokes. Each render is
written as a PNG with a transparent background, in white (for the blue panels) or in ink #26282B
(for light grounds), with a `.json` sidecar carrying the set, the licence and the icon's page.

Exit codes: 0 written · 1 no such icon in the set, or a usage error · 3 the set could not be
reached (deferred, never "not found").
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from visuals_common import (  # noqa: E402
    EXIT_DEFERRED, EXIT_OK, EXIT_USAGE, Deferred, ICON_LICENCES, ICON_SETS,
    eprint, http_get, provenance_record, write_sidecar,
)

INK = (0x26, 0x28, 0x2B)
WHITE = (0xFF, 0xFF, 0xFF)
COLORS = {"ink": INK, "white": WHITE}


def upsize_svg(svg_bytes: bytes, size: int) -> bytes:
    """Tabler and Lucide SVGs declare `width="24" height="24"`. QuickLook honours that literally and
    draws a 24-unit glyph into the corner of the canvas it was asked for, leaving a 512 px render
    whose icon is 35 px across. Rewriting width/height to the target (the viewBox is untouched, so
    stroke weights scale with it) is what makes the render fill its canvas."""
    text = svg_bytes.decode("utf-8", "replace")
    text = re.sub(r'(<svg\b[^>]*?)\bwidth="[^"]*"', rf'\1width="{size}"', text, count=1)
    text = re.sub(r'(<svg\b[^>]*?)\bheight="[^"]*"', rf'\1height="{size}"', text, count=1)
    return text.encode("utf-8")


def rasterize_svg(svg_bytes: bytes, size: int, work: str) -> "Image.Image":
    """QuickLook is the only SVG rasterizer on this Mac (no cairosvg, no rsvg-convert). It renders
    into a square canvas on an opaque white ground, so the alpha channel has to be rebuilt."""
    from PIL import Image

    if not shutil.which("qlmanage"):
        raise Deferred("no SVG rasterizer here: qlmanage is not on PATH, and no cairosvg/rsvg is "
                       "installed. The PNG route is the only one left.")
    svg_path = os.path.join(work, "icon.svg")
    with open(svg_path, "wb") as fh:
        fh.write(upsize_svg(svg_bytes, max(size, 512)))
    try:
        subprocess.run(["qlmanage", "-t", "-s", str(max(size, 512)), "-o", work, svg_path],
                       capture_output=True, timeout=60, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        raise Deferred(f"qlmanage could not render the icon: {exc}")
    png = svg_path + ".png"
    if not os.path.exists(png):
        raise Deferred("qlmanage produced no thumbnail for this SVG.")
    im = Image.open(png).convert("RGB")
    # White ground, dark strokes -> alpha is the ink coverage.
    alpha = im.convert("L").point(lambda v: 255 - v)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.putalpha(alpha)
    return square_on_canvas(out)


def square_on_canvas(im: "Image.Image", fill_floor: float = 0.5) -> "Image.Image":
    """A guard, not a trim. Both sets draw on a 24-unit box with about a 2-unit inset, so a correct
    render fills roughly 85% of its canvas. When a renderer ignores the size it was asked for, the
    glyph lands small in a corner instead; this reconstructs the icon's own 24-unit box around the
    drawn content and re-frames it. Icons that render correctly are returned untouched, so peers
    keep their relative weights (a narrow bolt stays narrower than a square factory)."""
    from PIL import Image

    bbox = im.getchannel("A").getbbox()
    if not bbox:
        return im
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    if max(w, h) >= fill_floor * min(im.size):
        return im
    eprint(f"  the renderer drew the icon at {max(w, h)}px on a {min(im.size)}px canvas; "
           f"re-framing it to its own box")
    side = int(max(w, h) * 24 / 20)
    cx, cy = (bbox[0] + bbox[2]) // 2, (bbox[1] + bbox[3]) // 2
    box = (cx - side // 2, cy - side // 2, cx + side // 2, cy + side // 2)
    out = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    out.paste(im.crop(box), (0, 0))
    return out.resize(im.size, Image.LANCZOS)


def load_png(blob: bytes) -> "Image.Image":
    from PIL import Image
    import io
    im = Image.open(io.BytesIO(blob)).convert("RGBA")
    if im.getextrema()[3][0] == 255:          # fully opaque: treat it like the QuickLook render
        alpha = im.convert("L").point(lambda v: 255 - v)
        im = Image.new("RGBA", im.size, (0, 0, 0, 0))
        im.putalpha(alpha)
    return im


def colorize(im: "Image.Image", rgb: tuple[int, int, int], size: int) -> "Image.Image":
    from PIL import Image
    if im.size != (size, size):
        im = im.resize((size, size), Image.LANCZOS)
    solid = Image.new("RGBA", im.size, rgb + (255,))
    solid.putalpha(im.getchannel("A"))
    return solid


def fetch(name: str, icon_set: str, size: int) -> tuple["Image.Image", dict, str]:
    meta = ICON_SETS[icon_set]
    route = None
    im = None
    # Route 1 — the PNG package, where the set has one and the size fits it.
    if meta["png"] and size <= 240:
        try:
            im = load_png(http_get(meta["png"].format(name=name)))
            route = "png package"
        except FileNotFoundError:
            pass                                   # not in the PNG package; try the SVG
        except Deferred as exc:
            eprint(f"  PNG package deferred ({exc}); trying the SVG")
    if im is None:
        svg = http_get(meta["svg"].format(name=name))   # FileNotFoundError -> no such icon
        with tempfile.TemporaryDirectory() as work:
            im = rasterize_svg(svg, size, work)
        route = "SVG + QuickLook"
    lic = ICON_LICENCES[meta["licence"]]
    rec = provenance_record(
        kind="icon", title=name, creator=meta["credit"],
        creator_url=meta["page"].format(name=name),
        source=meta["credit"], source_url=meta["page"].format(name=name),
        download_url=(meta["png"] or meta["svg"]).format(name=name),
        licence=meta["licence"], licence_name=lic["name"], licence_url=lic["url"],
        attribution_required=False, width=size, height=size,
        terms=name, note=f"rendered via {route}",
    )
    return im, rec, route


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("name", help="the icon's name in the set, e.g. building-factory")
    ap.add_argument("--out", required=True)
    ap.add_argument("--color", default="both", choices=["white", "ink", "both"])
    ap.add_argument("--set", dest="icon_set", default="tabler", choices=sorted(ICON_SETS))
    ap.add_argument("--size", type=int, default=512)
    ap.add_argument("--slot", default="icon", help="the slot this is a candidate for, e.g. vertical:0")
    args = ap.parse_args(argv)

    os.makedirs(args.out, exist_ok=True)
    try:
        im, rec, route = fetch(args.name, args.icon_set, args.size)
    except FileNotFoundError:
        eprint(f"{args.icon_set} has no icon called {args.name!r}. Check the name at "
               f"{ICON_SETS[args.icon_set]['page'].format(name='')} — or run suggest_icons.py "
               f"for candidates that do exist.")
        return EXIT_USAGE
    except Deferred as exc:
        eprint(f"deferred — {exc}\nThis is a network failure, not a missing icon. Retry; do not "
               f"record the icon as unavailable.")
        return EXIT_DEFERRED

    wanted = ["white", "ink"] if args.color == "both" else [args.color]
    written = []
    for c in wanted:
        img = colorize(im, COLORS[c], args.size)
        stem = f"{args.slot.replace(':', '-')}-{args.name}-{c}.png"
        path = os.path.join(args.out, stem)
        img.save(path)
        r = dict(rec, file=path, slot=args.slot, note=rec["note"] + f"; {c} on transparent")
        write_sidecar(path, r)
        written.append(path)

    print(f"{args.icon_set}/{args.name}  ({route}, {args.size}px, transparent)")
    for p in written:
        print("  " + p)
    print(f"  licence: {rec['licence_name']} · {rec['source_url']}")
    return EXIT_OK


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        sys.exit(130)
