#!/usr/bin/env bash
# Tests for lint_deck.py and the two deck builders.
#
#   plugins/oracle-packs/skills/deck/tests/test_lint_deck.sh
#   PY=.venv/bin/python plugins/oracle-packs/skills/deck/tests/test_lint_deck.sh
#   KEEP=1 ...                                   # leave the work dir in place
#
# The linter's budgets are measured from the exemplar deck, so the suite holds it
# to four verdicts: clean on the exemplar itself (--reference), clean on the
# exemplar builder's fixture deck, clean on the legacy builder's fixture deck, and
# red on a copy broken the four ways the owner's review caught — the tier eyebrow
# back on the cover, the retired running header, a numeral where an industry icon
# belongs, and a card with rounded corners. A linter that only ever passes is not
# a check.
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

SPEC="$TESTS/fixture-pack-spec.yaml"
EXEMPLAR="$SKILL/assets/exemplar/wfo-sales-deck.pptx"
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

say ""
say "build_deck.py (the legacy redrawing builder, for a machine without the exemplar)"
run_case "the legacy fixture builds" 0 \
  "$PY" "$SKILL/tools/build_deck.py" "$SPEC" --out "$WORK/v1" --channel partner_print
run_case "the legacy deck is clean too" 0 \
  "$PY" "$SKILL/tools/lint_deck.py" "$LEGACY" --spec "$SPEC" --channel partner_print

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

prs.save(dst)
print("broke the cover, the header, an industry card and a use-case card")
PYBREAK
[ $? -eq 0 ] || { say "test_lint_deck: could not build the broken copy"; exit 2; }

say ""
say "the four defects come back red"
run_case "the broken copy is caught" 1 \
  "$PY" "$SKILL/tools/lint_deck.py" "$WORK/broken.pptx" --spec "$SPEC" \
  --channel partner_print
expect "the broken copy" "a cover has no tier line" \
  "slide 2: the running header should read" \
  "where its industry's icon belongs" \
  "rounded corners"

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
