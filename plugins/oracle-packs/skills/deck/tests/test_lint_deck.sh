#!/usr/bin/env bash
# Tests for the deck builder and lint_deck.py.
#
#   plugins/oracle-packs/skills/deck/tests/test_lint_deck.sh
#   PY=.venv/bin/python plugins/oracle-packs/skills/deck/tests/test_lint_deck.sh
#   KEEP=1 ...                                   # leave the work dir in place
#
# It builds the fixture deck, asserts the linter is clean on it, then breaks a
# copy in the two ways the owner's review caught — the old running header and a
# tier line on the cover — and asserts the linter catches both. A linter that
# only ever passes is not a check.
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
DECK="$WORK/workforce-optimization-sales-deck.pptx"

say ""
say "build_deck.py"
run_case "the fixture builds with no box overflowing" 0 \
  "$PY" "$SKILL/tools/build_deck.py" "$SPEC" --out "$WORK" --channel partner_print
expect "the build" "Oracle AI & Data Solutions" "The architecture picture, in words"

say ""
say "lint_deck.py"
run_case "the built deck is clean" 0 \
  "$PY" "$SKILL/tools/lint_deck.py" "$DECK" --spec "$SPEC" --channel partner_print

# --- break it the two ways the owner's review caught ------------------------
"$PY" - "$DECK" "$WORK/broken.pptx" <<'PYBREAK'
import sys
from pptx import Presentation
from pptx.util import Emu, Pt

src, dst = sys.argv[1], sys.argv[2]
prs = Presentation(src)
slides = list(prs.slides)

# 1. the tier eyebrow back on the cover
tb = slides[0].shapes.add_textbox(Emu(502920), Emu(1325880), Emu(7315200), Emu(256032))
run = tb.text_frame.paragraphs[0].add_run()
run.text = "PoV Jumpstart · Integration · Scaling"
run.font.size = Pt(11.5)
run.font.name = "Replica LL TT"

# 2. the old running header on slide 2
for ph in slides[1].placeholders:
    if ph.placeholder_format.idx == 34:
        ph.text_frame.text = "OCI AI Accelerators — Workforce optimization"
        break

prs.save(dst)
print("broke the cover and slide 2")
PYBREAK
[ $? -eq 0 ] || { say "test_lint_deck: could not build the broken copy"; exit 2; }

run_case "the broken copy is caught" 1 \
  "$PY" "$SKILL/tools/lint_deck.py" "$WORK/broken.pptx" --spec "$SPEC" \
  --channel partner_print
expect "the broken copy" "a cover has no tier line" \
  "slide 2: the running header should read"

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
