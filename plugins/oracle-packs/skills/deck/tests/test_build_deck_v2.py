#!/usr/bin/env python3
"""Checks for the exemplar builder — run it directly:

    python3 tests/test_build_deck_v2.py

Builds both test specs and asserts what "clone, don't redraw" means in the file:
ten slides in the anatomy's order, the running header rewritten to the current
lockup, no tier eyebrow, no inherited hero photo, the exemplar's own type sizes
and rounded corners still in place, and an architecture rebuilt from the spec.
Stdlib + python-pptx only, no pytest required.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
sys.path.insert(0, str(SKILL / "tools"))

from pptx import Presentation                       # noqa: E402
from pptx.oxml.ns import qn                         # noqa: E402

BUILDER = SKILL / "tools" / "build_deck_v2.py"
FIXTURE = HERE / "fixture-pack-spec.yaml"
VARIABILITY = HERE / "fixture-pack-spec_v2-variability.yaml"

failures: list[str] = []
checks = 0


def check(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        failures.append(message)


def build(spec: Path, out: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, str(BUILDER), str(spec), "--out", str(out)],
        capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def all_shapes(container):
    for shp in container.shapes:
        yield shp
        if shp.shape_type == 6:
            yield from all_shapes(shp)


def texts(slide) -> str:
    out = []
    for shp in all_shapes(slide):
        if getattr(shp, "has_text_frame", False) and shp.has_text_frame:
            out.append(shp.text_frame.text)
        if getattr(shp, "has_table", False) and shp.has_table:
            for row in shp.table.rows:
                for cell in row.cells:
                    out.append(cell.text)
    return "\n".join(out)


def rounded(slide) -> int:
    return sum(1 for shp in all_shapes(slide)
               for geom in shp._element.iter(qn("a:prstGeom"))
               if geom.get("prst") == "roundRect")


def run_fixture(tmp: Path) -> None:
    out = tmp / "fixture"
    rc, log = build(FIXTURE, out)
    check(rc == 0, f"fixture build exited {rc}, not 0:\n{log}")
    check("no overflow" in log, f"fixture fit report is not clean:\n{log}")
    check("PoV" not in log.split("pictures")[0].split("architecture")[0],
          "unexpected tier vocabulary in the build banner")
    deck = out / "workforce-optimization-sales-deck.pptx"
    check(deck.is_file(), "fixture deck was not written")
    prs = Presentation(str(deck))
    slides = list(prs.slides)

    check(len(slides) == 10, f"{len(slides)} slides, expected 10")
    check(round(prs.slide_width / 914400, 2) == 13.33,
          "canvas is not the exemplar's 13.33 in")

    # The running header: the retired lockup never ships, and slide 1 has none.
    for i, slide in enumerate(slides[1:], 2):
        body = texts(slide)
        check("Oracle AI & Data Solutions — Workforce optimization" in body,
              f"slide {i} does not carry the current running header")
        check("OCI AI Accelerators" not in body,
              f"slide {i} still carries the retired OCI AI Accelerators lockup")

    cover = texts(slides[0])
    check("PROOF OF VALUE" not in cover.upper() or "ROLL-OUT" not in cover.upper(),
          "the cover still carries the reference's tier ladder line")
    check("Workforce optimization" in cover, "the cover does not name the pack")

    # The hero photo belongs to the reference pack, not to this one.
    hero = [shp for shp in slides[0].slide_layout.shapes
            if shp.shape_type == 13 and "logo" not in (shp.name or "").lower()]
    check(not hero, "the reference pack's cover photo is still on the layout")

    # Fidelity: the exemplar's own rounded cards and type sizes are untouched.
    check(rounded(slides[1]) == 6,
          f"use-case slide has {rounded(slides[1])} rounded shapes, exemplar has 6")
    table = next(shp.table for shp in slides[8].shapes
                 if getattr(shp, "has_table", False) and shp.has_table)
    header = table.cell(0, 1).text_frame.paragraphs[0].runs[0]
    check(header.font.size.pt == 12.5,
          f"package table header is {header.font.size.pt} pt, exemplar is 12.5 pt")
    check("PoV Jumpstart" in table.cell(0, 1).text, "tier names not filled from the spec")
    check(len(table.rows) == 11, f"package table has {len(table.rows)} rows, expected 11")

    # Verticals keep pictures, never numerals.
    icons = [shp for shp in slides[2].shapes if shp.shape_type == 13]
    check(len(icons) == 4, f"{len(icons)} vertical icons, expected 4")

    # Architecture: named app, named engine product, one box per system.
    arch = texts(slides[7])
    check("Workforce optimization by SoftServe" in arch,
          "the architecture app box does not name the pack")
    check("NVIDIA cuOpt" in arch, "the engine box does not name the catalog product")
    check("BI" in arch, "the architecture has no destination box for the BI output")
    arrows = sum(1 for shp in slides[7].shapes if shp.shape_type == 9)
    check(arrows >= 4, f"{arrows} connectors on the architecture slide, expected 4+")


def run_variability(tmp: Path) -> None:
    out = tmp / "variability"
    rc, log = build(VARIABILITY, out)
    check(rc == 0, f"variability build exited {rc}, not 0:\n{log}")
    check("no overflow" in log, f"variability fit report is not clean:\n{log}")
    deck = out / "contract-intelligence-sales-deck.pptx"
    check(deck.is_file(), "variability deck was not written")
    prs = Presentation(str(deck))
    slides = list(prs.slides)
    check(len(slides) == 10, f"{len(slides)} slides, expected 10")

    # 3 verticals -> one greyed empty card, never a gap.
    icons = [shp for shp in slides[2].shapes if shp.shape_type == 13]
    check(len(icons) == 3, f"{len(icons)} vertical icons for 3 verticals")
    cards = [shp for shp in slides[2].shapes
             if shp.shape_type == 1 and round(shp.width / 914400, 2) == 2.25]
    check(len(cards) == 4, f"{len(cards)} vertical panels, expected 4 (the 4th greyed)")

    # 7 capability rows in both tables, cloned from the exemplar's own row.
    t9 = next(shp.table for shp in slides[8].shapes
              if getattr(shp, "has_table", False) and shp.has_table)
    t10 = next(shp.table for shp in slides[9].shapes
               if getattr(shp, "has_table", False) and shp.has_table)
    check(len(t9.rows) == 12, f"packages table has {len(t9.rows)} rows, expected 12")
    check(len(t10.rows) == 9, f"detailed table has {len(t10.rows)} rows, expected 9")

    # A 3-layer stack shortens the ladder; a 3-product engine names all three.
    arch = texts(slides[7])
    for product in ("NVIDIA NeMo Agent Toolkit", "NVIDIA NIM", "NVIDIA NeMo"):
        check(product in arch, f"the engine box does not name {product}")
    check("Obligation dashboard" in arch, "the destination system is missing")
    layers = texts(slides[6])
    check("Extraction engine" in layers and "Infrastructure" in layers,
          "the ladder was not filled from architecture.stack[]")


def main() -> int:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        run_fixture(tmp)
        run_variability(tmp)
    if failures:
        print(f"{len(failures)} of {checks} checks failed:")
        for f in failures:
            print("  - " + f)
        return 1
    print(f"{checks} checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
