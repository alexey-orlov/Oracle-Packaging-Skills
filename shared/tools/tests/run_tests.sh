#!/usr/bin/env bash
# Tests for shared/tools: lint_spec.py, lint_artifact.py, check_consistency.py.
#
#   shared/tools/tests/run_tests.sh              # uses python3
#   PY=.venv/bin/python shared/tools/tests/run_tests.sh
#   KEEP=1 shared/tools/tests/run_tests.sh       # leave the work dir in place
#
# It runs the three tools on fixtures/pack-spec.valid.yaml, on two deliberately
# broken variants generated from it, and on the artifact fixtures, and asserts
# the exit code and the rule codes of every run.
#
# Exit 0 all assertions pass · 1 an assertion failed · 2 PyYAML is missing (the
# suite cannot run; a skipped check is not a check that passed).
#
# The broken variants are GENERATED from the valid fixture rather than committed,
# so they cannot drift from it, and the deny-listed customer name the clearance
# tests need is read from denylist.txt instead of being committed to this repo.

set -u

cd "$(dirname "$0")" || exit 2
TESTS="$PWD"
TOOLS="$(cd .. && pwd)"
FIX="$TESTS/fixtures"
PY="${PY:-python3}"
PASS=0
FAIL=0
LAST=""

say()  { printf '%s\n' "$*"; }
ok()   { PASS=$((PASS + 1)); printf '  ok   %s\n' "$1"; }
bad()  { FAIL=$((FAIL + 1)); printf '  FAIL %s\n' "$1"; printf '%s\n' "$LAST" | sed 's/^/       | /'; }

# run_case <label> <expected exit> <command...>
run_case() {
  label="$1"; want="$2"; shift 2
  LAST="$("$@" 2>&1)"; got=$?
  if [ "$got" = "$want" ]; then ok "$label (exit $got)"; else
    bad "$label — expected exit $want, got $got"; fi
}

# expect <label> <CODE>... — every code must appear in the last run's output
expect() {
  label="$1"; shift
  for code in "$@"; do
    case "$LAST" in
      *"$code"*) ok "$label prints $code" ;;
      *) bad "$label — $code missing from the output" ;;
    esac
  done
}

# expect_absent <label> <CODE>...
expect_absent() {
  label="$1"; shift
  for code in "$@"; do
    case "$LAST" in
      *"$code"*) bad "$label — $code should not fire here" ;;
      *) ok "$label is silent on $code" ;;
    esac
  done
}

# ---------------------------------------------------------------- dependencies
if ! "$PY" -c "import yaml" >/dev/null 2>&1; then
  say "run_tests: PyYAML is not installed for $PY, so the suite cannot run."
  say "  python3 -m venv .venv \\"
  say "    && .venv/bin/pip install -r plugins/oracle-packs/requirements.txt"
  say "  then: PY=.venv/bin/python shared/tools/tests/run_tests.sh"
  say ""
  say "Checking the dependency guard itself instead:"
  LAST="$("$PY" "$TOOLS/lint_spec.py" "$FIX/pack-spec.valid.yaml" 2>&1)"; got=$?
  [ "$got" = 2 ] && say "  ok   lint_spec exits 2 without PyYAML" \
                 || say "  FAIL lint_spec exited $got without PyYAML, expected 2"
  exit 2
fi

WORK="$(mktemp -d "${TMPDIR:-/tmp}/packlint-tests.XXXXXX")" || exit 2
trap '[ -n "${KEEP:-}" ] || rm -rf "$WORK"' EXIT
say "run_tests: work dir $WORK"

# The first deny-list entry, used wherever a test needs a name that must not ship.
DENY_NAME="$(sed -e 's/#.*//' -e 's/^~//' -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' \
             "$TOOLS/denylist.txt" | grep -v '/' | grep -v '^$' | head -1)"
[ -n "$DENY_NAME" ] || { say "run_tests: denylist.txt has no usable entry"; exit 2; }

sed "s|__DENY__|$DENY_NAME|g" "$FIX/artifact-broken.md" > "$WORK/artifact-broken.md"
cp "$FIX/artifact-clean.md" "$FIX/artifact-inconsistent.md" "$WORK/"

# --------------------------------------------- the two broken spec variants
"$PY" - "$FIX/pack-spec.valid.yaml" "$WORK" "$DENY_NAME" <<'PYGEN'
import sys
src, work, deny = sys.argv[1], sys.argv[2], sys.argv[3]
text = open(src, encoding="utf-8").read()

# Variant A — clearance and sourcing: a deny-listed name in customer-facing copy,
# a clearance channel missing, and first-order sources that are not `user:`.
a = text.replace("source: user:2026-09-18", "source: call-note 2026-09-18")
a = a.replace("    demo: false\n", "")
a = a.replace("Re-plan technician zones",
              "Re-plan %s technician zones" % deny)
a = a.replace("otherwise: \"proof of value at a global home-appliance manufacturer\"",
              "otherwise: \"proof of value at %s\"" % deny)
open(work + "/pack-spec.broken-clearance.yaml", "w", encoding="utf-8").write(a)

# Variant B — packages and metrics: a PoV over the hard cap, a renamed tier, a
# second metric set, an off-catalog product, an unknown roadmap id, no open_questions.
b = text.replace("{ target: 6, min: 4, max: 8, hard_cap: 10 }",
                 "{ target: 6, min: 4, max: 12, hard_cap: 10 }")
b = b.replace("      name: Scaling\n", "      name: Scale\n")
b = b.replace("  roadmap_item_id: workforce-optimization",
              "  roadmap_item_id: technician-shift-scheduling")
b = b.replace("  - id: oci-object-storage", "  - id: oci-object-store")
# the engine pushed into oracle_products, where only Oracle products belong (SPEC018)
b = b.replace("  - id: oracle-fusion-field-service",
              "  - id: nvidia-cuopt\n    role: required\n    why: \"the solver\"\n"
              "  - id: oracle-fusion-field-service")
# an off-catalog id on the stack layer, the other half of SPEC004
b = b.replace("catalog_id: nvidia-cuopt }", "catalog_id: nvidia-cu-opt }")
b = b.replace("    source: pov-report 2026-06-30\n",
              "    source: pov-report 2026-06-30\n"
              "  - name: Planning cycle time\n"
              "    formula: \"Time from demand freeze to approved plan\"\n"
              "    baseline: \"~2 days manual\"\n"
              "    figure: \"~2 h\"\n"
              "    attribution: { otherwise: \"modeled\" }\n")
b = b.replace("open_questions: []\n", "")
open(work + "/pack-spec.broken-packages.yaml", "w", encoding="utf-8").write(b)
print("generated two broken spec variants")
PYGEN
[ $? -eq 0 ] || { say "run_tests: could not generate the broken variants"; exit 2; }

# Variant C — a workflow of 8 steps: mechanics promoted to steps (SPEC019).
"$PY" - "$FIX/pack-spec.valid.yaml" "$WORK" <<'PYSTEPS'
import sys, copy, yaml
src, work = sys.argv[1], sys.argv[2]
spec = yaml.safe_load(open(src, encoding="utf-8"))
steps = spec["workflow"]["steps"]
while len(steps) < 8:
    s = copy.deepcopy(steps[-1]); s["n"] = len(steps) + 1
    s["name"] = "Mechanics promoted to a step %d" % s["n"]; steps.append(s)
yaml.safe_dump(spec, open(work + "/pack-spec.broken-workflow.yaml", "w", encoding="utf-8"),
               sort_keys=False, allow_unicode=True)
print("generated the 8-step workflow variant")
PYSTEPS
[ $? -eq 0 ] || { say "run_tests: could not generate the workflow variant"; exit 2; }

# ------------------------------------------- generated .docx / .pptx artifacts
"$PY" - "$WORK" <<'PYOFFICE'
import sys, zipfile
out = sys.argv[1]
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
pw = lambda t: "<w:p><w:r><w:t>%s</w:t></w:r></w:p>" % t
pa = lambda t: "<a:p><a:r><a:t>%s</a:t></a:r></a:p>" % t
with zipfile.ZipFile(out + "/feature-list.docx", "w") as z:
    z.writestr("word/document.xml",
               '<w:document xmlns:w="%s"><w:body>%s</w:body></w:document>'
               % (W, "".join(pw(t) for t in [
                   "Workforce Optimization App",
                   "PoV Jumpstart runs 4-8 weeks on your own data.",
                   "Services from EUR 90K, indicative."])))
with zipfile.ZipFile(out + "/deck.pptx", "w") as z:
    z.writestr("ppt/slides/slide1.xml",
               '<p:sld xmlns:p="%s" xmlns:a="%s"><a:txBody>%s</a:txBody></p:sld>'
               % (P, A, "".join(pa(t) for t in ["Workforce optimization", "Quick Start tier"])))
    z.writestr("ppt/notesSlides/notesSlide1.xml",
               '<p:notes xmlns:p="%s" xmlns:a="%s"><a:txBody>%s</a:txBody></p:notes>'
               % (P, A, pa("Speaker note: the PoV runs 12 weeks.")))
print("generated feature-list.docx and deck.pptx")
PYOFFICE

CAT="$FIX/catalog.yaml"
ROAD="$FIX/roadmap.csv"
VALID="$FIX/pack-spec.valid.yaml"

# ------------------------------------------------------------------ lint_spec
say ""
say "lint_spec.py"
run_case "valid fixture is clean" 0 \
  "$PY" "$TOOLS/lint_spec.py" "$VALID" --catalog "$CAT" --roadmap "$ROAD"
expect "valid fixture" "17 of 17 components complete"
expect_absent "valid fixture" SPEC019 SPEC020

run_case "valid fixture is clean under --strict" 0 \
  "$PY" "$TOOLS/lint_spec.py" "$VALID" --catalog "$CAT" --roadmap "$ROAD" --strict

run_case "broken variant A (clearance and sourcing)" 1 \
  "$PY" "$TOOLS/lint_spec.py" "$WORK/pack-spec.broken-clearance.yaml" \
  --catalog "$CAT" --roadmap "$ROAD"
expect "variant A" SPEC003 SPEC010 SPEC013

run_case "broken variant B (packages and metrics)" 1 \
  "$PY" "$TOOLS/lint_spec.py" "$WORK/pack-spec.broken-packages.yaml" \
  --catalog "$CAT" --roadmap "$ROAD"
expect "variant B" SPEC004 SPEC005 SPEC007 SPEC008 SPEC009 SPEC011 SPEC012 SPEC014 SPEC018
expect "variant B" "architecture.stack[2].catalog_id"

run_case "broken variant C (workflow of 8 steps)" 1 \
  "$PY" "$TOOLS/lint_spec.py" "$WORK/pack-spec.broken-workflow.yaml" \
  --catalog "$CAT" --roadmap "$ROAD"
expect "variant C" SPEC019

run_case "a missing spec is a usage error" 2 \
  "$PY" "$TOOLS/lint_spec.py" "$WORK/not-here.yaml"

# -------------------------------------------------------------- lint_artifact
say ""
say "lint_artifact.py"
run_case "clean listing on customer_site" 0 \
  "$PY" "$TOOLS/lint_artifact.py" "$WORK/artifact-clean.md" --channel customer_site \
  --spec "$VALID" --catalog "$CAT"

run_case "broken artifact on customer_site" 1 \
  "$PY" "$TOOLS/lint_artifact.py" "$WORK/artifact-broken.md" --channel customer_site \
  --spec "$VALID" --catalog "$CAT"
expect "broken artifact" ART001 ART002 ART003 ART101 ART102 ART103 ART104 \
  ART201 ART202 ART203 ART204 ART205 ART301 ART302 ART401 ART402 ART403

run_case "same artifact on the internal channel" 1 \
  "$PY" "$TOOLS/lint_artifact.py" "$WORK/artifact-broken.md" --channel internal \
  --spec "$VALID" --catalog "$CAT"
expect_absent "internal channel" ART001 ART002 ART102 ART201 ART203
expect "internal channel" ART101 ART301

run_case ".docx extraction (internal deck copy)" 0 \
  "$PY" "$TOOLS/lint_artifact.py" "$WORK/feature-list.docx" --channel internal \
  --spec "$VALID" --catalog "$CAT"

run_case ".pptx extraction, slides and notes" 1 \
  "$PY" "$TOOLS/lint_artifact.py" "$WORK/deck.pptx" --channel partner_print \
  --spec "$VALID" --catalog "$CAT"
expect ".pptx" ART402 "slide 1"

"$PY" - "$WORK/one-pager.pdf" <<'PYPDF'
import sys
text = "PoV Jumpstart, services from EUR 450K per engagement"
stream = "BT /F1 14 Tf 72 720 Td (%s) Tj ET" % text
objs = ["<</Type/Catalog/Pages 2 0 R>>", "<</Type/Pages/Kids[3 0 R]/Count 1>>",
        "<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R"
        "/Resources<</Font<</F1 5 0 R>>>>>>",
        "<</Length %d>>stream\n%s\nendstream" % (len(stream), stream),
        "<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>"]
out, offsets = b"%PDF-1.4\n", []
for i, body in enumerate(objs, 1):
    offsets.append(len(out))
    out += ("%d 0 obj\n%s\nendobj\n" % (i, body)).encode()
xref = len(out)
out += ("xref\n0 %d\n" % (len(objs) + 1)).encode() + b"0000000000 65535 f \n"
for off in offsets:
    out += ("%010d 00000 n \n" % off).encode()
out += ("trailer\n<</Size %d/Root 1 0 R>>\nstartxref\n%d\n%%%%EOF\n"
        % (len(objs) + 1, xref)).encode()
open(sys.argv[1], "wb").write(out)
print("generated one-pager.pdf")
PYPDF

if command -v pdftotext >/dev/null 2>&1; then
  run_case ".pdf extraction through pdftotext" 1 \
    "$PY" "$TOOLS/lint_artifact.py" "$WORK/one-pager.pdf" --channel partner_print \
    --spec "$VALID" --catalog "$CAT"
  expect ".pdf" ART301
  expect_absent ".pdf" ART402   # "PoV Jumpstart" is the correct tier name
else
  run_case ".pdf is skipped when pdftotext is absent" 0 \
    "$PY" "$TOOLS/lint_artifact.py" "$WORK/one-pager.pdf" --channel partner_print \
    --spec "$VALID" --catalog "$CAT"
  expect ".pdf" ART900 "not evaluated"
fi

# A `not_this` spelling that differs from the catalog's own only in case
# ("NVIDIA Nemo" against "NVIDIA NeMo", "Nvidia NIM" against "NVIDIA NIM") used to
# fire ART101 on the correct spellings, so an artifact naming the products right
# came back red. The right spellings are clean; the wrong ones are still caught.
cat > "$WORK/vendor-spelling-right.md" <<'EOF'
The extraction engine runs NVIDIA NeMo Agent Toolkit and NVIDIA NIM on OCI,
with NVIDIA NeMo behind them. NeMo is the framework; NIM serves the models,
and NVIDIA cuOpt does the optimization.
EOF
cat > "$WORK/vendor-spelling-wrong.md" <<'EOF'
The engine runs NVIDIA Nemo and Nvidia NIM; Nemo is the framework and the
NIMs serve the models.
EOF

run_case "the catalog's own vendor spellings are clean" 0 \
  "$PY" "$TOOLS/lint_artifact.py" "$WORK/vendor-spelling-right.md" \
  --channel partner_print --spec "$VALID" --catalog "$CAT"
expect_absent "right spellings" ART101 ART103

run_case "the case-only misspellings are still caught" 1 \
  "$PY" "$TOOLS/lint_artifact.py" "$WORK/vendor-spelling-wrong.md" \
  --channel partner_print --spec "$VALID" --catalog "$CAT"
expect "wrong spellings" "ART101" "NVIDIA Nemo" "Nvidia NIM" "NIMs"

run_case "a directory of artifacts" 1 \
  "$PY" "$TOOLS/lint_artifact.py" "$WORK" --channel customer_site \
  --spec "$VALID" --catalog "$CAT"

run_case "an unknown channel is a usage error" 2 \
  "$PY" "$TOOLS/lint_artifact.py" "$WORK/artifact-clean.md" --channel sales_deck

# ----------------------------------------------------------- check_consistency
say ""
say "check_consistency.py"
run_case "clean artifact matches the spec" 0 \
  "$PY" "$TOOLS/check_consistency.py" "$VALID" "$WORK/artifact-clean.md"

run_case "contradicting artifact" 1 \
  "$PY" "$TOOLS/check_consistency.py" "$VALID" "$WORK/artifact-inconsistent.md"
expect "contradicting artifact" CON001 CON002 CON003 CON004 CON005

run_case "an absent component is not a finding" 0 \
  "$PY" "$TOOLS/check_consistency.py" "$VALID" "$WORK/feature-list.docx"
expect "absent components" "–"

run_case "a missing spec is a usage error" 2 \
  "$PY" "$TOOLS/check_consistency.py" "$WORK/not-here.yaml" "$WORK/artifact-clean.md"

# --------------------------------------------------------------- context_budget
# The spec skill's own manifest must stay inside its per-step reading budget;
# a card that grows past its share fails here, not in a live run.
say ""
say "context_budget.py"
SPEC_MANIFEST="$TESTS/../../../plugins/oracle-packs/skills/spec/references/cards/manifest.yaml"
if [ -f "$SPEC_MANIFEST" ]; then
  run_case "the spec manifest is within budget" 0 \
    "$PY" "$TOOLS/context_budget.py" "$SPEC_MANIFEST" --quiet
  run_case "a missing manifest is a usage error" 2 \
    "$PY" "$TOOLS/context_budget.py" "$WORK/no-manifest.yaml"
else
  bad "the spec manifest is missing: $SPEC_MANIFEST"
fi

# ----------------------------------------------------- the deck builder + linter
# Lives with its skill (it needs python-pptx and the deck base), so it runs as a
# sub-suite: its own assertions are printed, and it counts here as one result.
DECK_TESTS="$TESTS/../../../plugins/oracle-packs/skills/deck/tests/test_lint_deck.sh"
if [ -x "$DECK_TESTS" ]; then
  say ""
  say "deck builder and lint_deck.py"
  LAST="$(PY="$PY" "$DECK_TESTS" 2>&1)"; got=$?
  printf '%s\n' "$LAST" | sed 's/^/  /'
  case "$got" in
    0) ok "the deck sub-suite" ;;
    2) say "  (skipped: $PY has no python-pptx / Pillow)" ;;
    *) bad "the deck sub-suite failed" ;;
  esac
fi

# --------------------------------------------------------------------- report
say ""
if [ "$FAIL" -eq 0 ]; then
  say "run_tests: $PASS passed, 0 failed"
  exit 0
fi
say "run_tests: $PASS passed, $FAIL FAILED (work dir kept: $WORK)"
KEEP=1
exit 1
