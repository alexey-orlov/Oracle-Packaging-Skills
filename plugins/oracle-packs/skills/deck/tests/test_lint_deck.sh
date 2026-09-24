#!/usr/bin/env bash
# Tests for lint_deck.py and the two deck builders.
#
#   plugins/oracle-packs/skills/deck/tests/test_lint_deck.sh
#   PY=.venv/bin/python plugins/oracle-packs/skills/deck/tests/test_lint_deck.sh
#   KEEP=1 ...                                   # leave the work dir in place
#
# The linter's budgets are measured from the exemplar deck, so the suite holds it
# to these verdicts: clean on the exemplar itself (--reference), clean on the
# exemplar builder's fixture deck, RED on the legacy builder's fixture deck (its
# cover is ink only — the stripped base has no photo layout) and clean on that
# same deck under --legacy-cover-ok, and red on a copy broken the five ways the
# owner's review caught — the tier eyebrow back on the cover, the retired running
# header, a numeral where an industry icon belongs, a card with rounded corners,
# and a card pushed out of its ladder row. The proof slide gets its own pass: a
# variant brief that clears the customer's name and names a logo file builds with
# the logo on slide 5 and lints clean; the same brief with no file warns instead
# of failing; and a copy with a relabelled quadrant or an emptied stat tile comes
# back red. A linter that only ever passes is not a check.
#
# Exit 0 all assertions pass · 1 an assertion failed · 2 the suite cannot run
# (no python-pptx / PyYAML — a skipped check is not a check that passed).

set -u

cd "$(dirname "$0")" || exit 2
TESTS="$PWD"
SKILL="$(cd .. && pwd)"
PY="${PY:-python3}"
PASS=0
FAIL=0
LAST=""

say()  { printf '%s\n' "$*"; }
ok()   { PASS=$((PASS + 1)); printf '  ok   %s\n' "$1"; }
bad()  { FAIL=$((FAIL + 1)); printf '  FAIL %s\n' "$1"; printf '%s\n' "$LAST" | sed 's/^/       | /'; }

run_case() {
  label="$1"; want="$2"; shift 2
  LAST="$("$@" 2>&1)"; got=$?
  if [ "$got" = "$want" ]; then ok "$label (exit $got)"; else
    bad "$label — expected exit $want, got $got"; fi
}

expect() {
  label="$1"; shift
  for text in "$@"; do
    case "$LAST" in
      *"$text"*) ok "$label mentions \"$text\"" ;;
      *) bad "$label — \"$text\" missing from the output" ;;
    esac
  done
}

if ! "$PY" -c "import yaml, pptx, PIL" >/dev/null 2>&1; then
  say "test_lint_deck: $PY has no pyyaml / python-pptx / Pillow, so the suite"
  say "  cannot run.  python3 -m venv .venv \\"
  say "    && .venv/bin/pip install -r plugins/oracle-packs/requirements.txt"
  say "  then: PY=.venv/bin/python $0"
  exit 2
fi

WORK="$(mktemp -d "${TMPDIR:-/tmp}/deck-tests.XXXXXX")" || exit 2
trap '[ -n "${KEEP:-}" ] || rm -rf "$WORK"' EXIT
say "test_lint_deck: work dir $WORK"

SPEC="$TESTS/fixture-pack-spec.md"
EXEMPLAR="$SKILL/assets/exemplar/wfo-sales-deck.pptx"

# The one spec loader (shared/tools/packspec.py): the plugin's synced copy, or the bundle's.
SHARED_TOOLS=""
for d in "$SKILL/../../shared/tools" "$SKILL/../../../../shared/tools"; do
  if [ -f "$d/packspec.py" ]; then SHARED_TOOLS="$(cd "$d" && pwd)"; break; fi
done
[ -n "$SHARED_TOOLS" ] || { say "test_lint_deck: shared/tools/packspec.py not found"; exit 2; }
DECK="$WORK/v2/workforce-optimization-sales-deck.pptx"
LEGACY="$WORK/v1/workforce-optimization-sales-deck.pptx"

say ""
say "the reference the budgets are measured from"
run_case "the exemplar deck passes its own checks" 0 \
  "$PY" "$SKILL/tools/lint_deck.py" "$EXEMPLAR" --reference
expect "reference mode" "the running header is not checked"

say ""
say "build_deck_v2.py (the builder the skill uses)"
run_case "the fixture builds with no box overflowing" 0 \
  "$PY" "$SKILL/tools/build_deck_v2.py" "$SPEC" --out "$WORK/v2" --channel partner_print
expect "the build" "10 slides from the exemplar" "architecture diagram"
run_case "the built deck is clean" 0 \
  "$PY" "$SKILL/tools/lint_deck.py" "$DECK" --spec "$SPEC" --channel partner_print
expect "the built deck" "the cover's hero"

say ""
say "build_deck.py (the legacy redrawing builder, for a machine without the exemplar)"
run_case "the legacy fixture builds" 0 \
  "$PY" "$SKILL/tools/build_deck.py" "$SPEC" --out "$WORK/v1" --channel partner_print
# The stripped base carries no photo layout, so the legacy cover is ink only —
# exactly the black cover the owner rejected. It must come back red on its own,
# and pass only under the documented legacy flag.
run_case "the legacy deck fails on the cover" 1 \
  "$PY" "$SKILL/tools/lint_deck.py" "$LEGACY" --spec "$SPEC" --channel partner_print
expect "the legacy deck" "the cover has no hero picture" \
  "not the reference's \"Title-AI\" photo layout" \
  "build with the exemplar builder"
run_case "the legacy deck passes under --legacy-cover-ok" 0 \
  "$PY" "$SKILL/tools/lint_deck.py" "$LEGACY" --spec "$SPEC" --channel partner_print \
  --legacy-cover-ok
expect "the legacy flag" "WARNING: the cover has no hero picture" \
  "not deliverable as final"

# --- break it the four ways the owner's review caught ------------------------
"$PY" - "$DECK" "$WORK/broken.pptx" <<'PYBREAK'
import sys
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

src, dst = sys.argv[1], sys.argv[2]
prs = Presentation(src)
slides = list(prs.slides)

# 1. the tier eyebrow back on the cover
tb = slides[0].shapes.add_textbox(Emu(502920), Emu(1325880), Emu(7315200), Emu(256032))
run = tb.text_frame.paragraphs[0].add_run()
run.text = "PoV Jumpstart · Integration · Scaling"
run.font.size = Pt(11.5)
run.font.name = "Replica LL TT"

# 2. the retired running header on slide 2
for ph in slides[1].placeholders:
    if ph.placeholder_format.idx == 34:
        ph.text_frame.text = "OCI AI Accelerators — Workforce optimization"
        break

# 3. a numeral where an industry icon belongs
tb = slides[2].shapes.add_textbox(Emu(457200), Emu(2286000), Emu(457200), Emu(457200))
tb.text_frame.text = "3"

# 4. a card with rounded corners, on the use-case slide the review flagged
card = slides[1].shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Emu(457200),
                                  Emu(4572000), Emu(2743200), Emu(1143000))
geom = card._element.find(".//" + qn("a:prstGeom"))
avLst = geom.find(qn("a:avLst"))
gd = avLst.makeelement(qn("a:gd"), {"name": "adj", "fmla": "val 50000"})
avLst.append(gd)

# 5. a card pushed out of its row on the technology-stack slide
s7 = slides[6]
rows = [sp for sp in s7.shapes if sp.shape_type == 1 and sp.width / 914400 >= 9.0
        and sp.height / 914400 >= 0.5]
top_row = min(rows, key=lambda r: r.top)
cards = [sp for sp in s7.shapes if sp.shape_type == 1 and 3.0 <= sp.width / 914400 <= 4.5
         and top_row.top <= sp.top + sp.height / 2 <= top_row.top + top_row.height]
cards[0].top = Emu(cards[0].top - 182880)   # 0.2 in up: over the band's edge

prs.save(dst)
print("broke the cover, the header, an industry card, a use-case card and a ladder card")
PYBREAK
[ $? -eq 0 ] || { say "test_lint_deck: could not build the broken copy"; exit 2; }

say ""
say "the five defects come back red"
run_case "the broken copy is caught" 1 \
  "$PY" "$SKILL/tools/lint_deck.py" "$WORK/broken.pptx" --spec "$SPEC" \
  --channel partner_print
expect "the broken copy" "a cover has no tier line" \
  "slide 2: the running header should read" \
  "where its industry's icon belongs" \
  "rounded corners" \
  "sticks out of its row"

# --- the proof slide: the delivered case, in the reference's composition ------
# The default fixture clears nothing, so its proof slide carries no logo and the
# linter has just passed that half of the rule. This variant is the other half:
# the customer's name cleared for the printed channel, a logo file, and the
# delivered case written with {Customer} where the name goes. The logo here is
# the SoftServe wordmark standing in for a customer's mark — this repo carries no
# real customer logo, and the point under test is that a picture reaches slide 5.
say ""
say "the proof slide — the delivered case, the logo, the four labels, three tiles"

VSPEC="$WORK/variant/pack-spec.md"
LOGO="$SKILL/../feature-list/assets/softserve-wordmark-ink.png"
mkdir -p "$WORK/variant" "$WORK/variant-nologo"
"$PY" - "$SPEC" "$VSPEC" "$LOGO" "$SHARED_TOOLS" <<'PYVARIANT'
import sys

src, dst, logo = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, sys.argv[4])
import packspec
spec = packspec.load(src)[0]

spec["clearance"]["customer_name_allowed"]["partner_print"] = True
se = spec["meta"]["source_engagement"]
se["customer"] = "Northwind Appliances"          # fictional: no real customer is named in this repo
se["context"] = (
    "{Customer} dispatch about 900 engineers across three markets from a dozen planning "
    "desks. Zones, skills, working days and absences were maintained by hand in "
    "spreadsheets, and a region's four-week plan took two senior planners about two days "
    "to rebuild.")
se["delivered"] = (
    "A proof of value at {Customer}, on their own field-service data: zone and technician "
    "allocation computed by a GPU solver, reviewed on a live map by their own dispatchers, "
    "and exported to their field-service system. Three markets, one rule set, file-based "
    "import.")
spec["packages"]["value_for_partner"] = (
    "Recurring OCI GPU consumption under every optimization run, and an NVIDIA cuOpt "
    "attach on an Oracle field-service account. The same shape resells to any operator "
    "planning a mobile workforce.")
spec["packages"]["value_for_client"] = (
    "Planners review a plan instead of building one, and a new region opens without a "
    "senior planner's year of local knowledge. Capacity that was lost to uneven "
    "allocation goes back into the working day.")
spec["problem_solution"]["reframe_question"] = "What if dispatchers reviewed the plan?"
spec.setdefault("deck", {}).setdefault("images", {})["customer_logo"] = logo
spec["kpis"][0]["attribution"]["named_when_allowed"] = \
    "the proof of value at Northwind Appliances"

problems = packspec.roundtrip_problems(spec, dst)
if problems:
    sys.exit(problems[0])
with open(dst, "w", encoding="utf-8") as fh:
    fh.write(packspec.dump(spec))
print("wrote the variant brief: the name cleared, a logo file, the delivered case")
PYVARIANT
[ $? -eq 0 ] || { say "test_lint_deck: could not write the variant brief"; exit 2; }

cat > "$WORK/proof_pictures.py" <<'PYPICS'
import sys
from pptx import Presentation


def walk(shapes):
    for sp in shapes:
        yield sp
        if sp.__class__.__name__ == "GroupShape":
            yield from walk(sp.shapes)


slide = list(Presentation(sys.argv[1]).slides)[4]
pics = [sp for sp in walk(slide.shapes)
        if sp.shape_type is not None and "PICTURE" in str(sp.shape_type)]
print("pictures on the proof slide: %d" % len(pics))
PYPICS

VDECK="$WORK/v2-logo/workforce-optimization-sales-deck.pptx"
run_case "the variant builds" 0 \
  "$PY" "$SKILL/tools/build_deck_v2.py" "$VSPEC" --out "$WORK/v2-logo" --channel partner_print
run_case "the logo reached the proof slide" 0 "$PY" "$WORK/proof_pictures.py" "$VDECK"
expect "the variant build" "pictures on the proof slide: 1"
run_case "the variant deck is clean" 0 \
  "$PY" "$SKILL/tools/lint_deck.py" "$VDECK" --spec "$VSPEC" --channel partner_print

# Cleared, but no file given: a warning naming what is missing, not a failure.
NSPEC="$WORK/variant-nologo/pack-spec.md"
"$PY" - "$VSPEC" "$NSPEC" "$SHARED_TOOLS" <<'PYNOLOGO'
import sys
sys.path.insert(0, sys.argv[3])
import packspec
spec = packspec.load(sys.argv[1])[0]
spec["deck"]["images"].pop("customer_logo", None)
problems = packspec.roundtrip_problems(spec, sys.argv[2])
if problems:
    sys.exit(problems[0])
with open(sys.argv[2], "w", encoding="utf-8") as fh:
    fh.write(packspec.dump(spec))
print("wrote the same brief with no logo file")
PYNOLOGO
NDECK="$WORK/v2-nologo/workforce-optimization-sales-deck.pptx"
run_case "the same brief with no logo file builds" 0 \
  "$PY" "$SKILL/tools/build_deck_v2.py" "$NSPEC" --out "$WORK/v2-nologo" --channel partner_print
run_case "a cleared name with no logo file is a warning, not a failure" 0 \
  "$PY" "$SKILL/tools/lint_deck.py" "$NDECK" --spec "$NSPEC" --channel partner_print
expect "the missing logo" \
  "the customer's name is cleared for this audience but no logo file was given"

# Relabel a quadrant and empty a stat tile — the two defects the owner's review
# caught on the delivered-case build, next to the missing logo.
"$PY" - "$VDECK" "$WORK/broken-proof.pptx" <<'PYBREAKPROOF'
import sys
from pptx import Presentation

src, dst = sys.argv[1], sys.argv[2]
prs = Presentation(src)
slide = list(prs.slides)[4]
E = 914400.0


def at(x, y, tol=0.25):
    near = [sp for sp in slide.shapes
            if abs(sp.left / E - x) <= tol and abs(sp.top / E - y) <= tol]
    if not near:
        raise SystemExit("no shape at %.3f, %.3f on the proof slide" % (x, y))
    return min(near, key=lambda sp: abs(sp.left / E - x) + abs(sp.top / E - y))


at(7.050, 4.750).text_frame.text = "WHY IT MATTERS"   # the reference says VALUE FOR CLIENT
at(4.778, 2.527).text_frame.text = ""                 # the middle tile's figure, emptied
prs.save(dst)
print("relabelled a quadrant and emptied a stat tile")
PYBREAKPROOF
[ $? -eq 0 ] || { say "test_lint_deck: could not break the proof slide"; exit 2; }

run_case "a relabelled quadrant and an emptied tile come back red" 1 \
  "$PY" "$SKILL/tools/lint_deck.py" "$WORK/broken-proof.pptx" --spec "$VSPEC" \
  --channel partner_print
expect "the broken proof slide" \
  "block is labelled \"WHY IT MATTERS\"" \
  "the reference labels it \"VALUE FOR CLIENT\"" \
  "stat tile 2 of 3 has no figure"

run_case "a deck that is not there is a usage error" 2 \
  "$PY" "$SKILL/tools/lint_deck.py" "$WORK/not-here.pptx" --spec "$SPEC"

say ""
if [ "$FAIL" -eq 0 ]; then
  say "test_lint_deck: $PASS passed, 0 failed"
  exit 0
fi
say "test_lint_deck: $PASS passed, $FAIL FAILED (work dir kept: $WORK)"
KEEP=1
exit 1
