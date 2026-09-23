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
# warn <line> — not a failure, but repeated just above the final report so it is seen
WARNINGS=""
warn() { WARNINGS="${WARNINGS}$1
"; printf '  %s\n' "$1"; }

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

# Variant D — the metric set is proof criteria only: technical names, no `kind`, no
# `owner_role`. SPEC025/026/027 must all fire, or a pack ships acceptance criteria as
# its sales tiles (the DHL one-pager, 2026-09-23). The retired family name rides along
# in the eyebrow, where SPEC028 has to refuse it.
"$PY" - "$FIX/pack-spec.valid.yaml" "$WORK" <<'PYMETRICS'
import sys, yaml
src, work = sys.argv[1], sys.argv[2]
spec = yaml.safe_load(open(src, encoding="utf-8"))
spec["meta"]["eyebrow"] = "OCI AI Accelerators"
spec["kpis"] = [
    {"name": "Reviewer agreement", "formula": "Share of decisions two reviewers agree on",
     "baseline": "not measured", "figure": "> 85%", "figure_status": "pov_result",
     "attribution": {"otherwise": "proof of value"}, "caveat": "Illustrative, not contractual"},
    {"name": "Documents processed", "formula": "Documents run through the pipeline",
     "baseline": "-", "figure": "12,000", "figure_status": "pov_result",
     "attribution": {"otherwise": "proof of value"}, "caveat": "Illustrative, not contractual"},
]
yaml.safe_dump(spec, open(work + "/pack-spec.technical-metrics.yaml", "w", encoding="utf-8"),
               sort_keys=False, allow_unicode=True)
print("generated the technical-metrics variant")
PYMETRICS
[ $? -eq 0 ] || { say "run_tests: could not generate the technical-metrics variant"; exit 2; }

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
# the business-metric rule is silent on a set that already passes it
expect_absent "valid fixture" SPEC025 SPEC026 SPEC027 SPEC028

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

run_case "broken variant D (proof criteria as the metric set)" 1 \
  "$PY" "$TOOLS/lint_spec.py" "$WORK/pack-spec.technical-metrics.yaml" \
  --catalog "$CAT" --roadmap "$ROAD"
expect "variant D" SPEC025 SPEC026 SPEC027 SPEC028
expect "variant D" "no business metric in the set" "Oracle AI & Data Solutions"

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
expect "broken artifact" ART001 ART002 ART003 ART101 ART102 ART103 ART104 ART105 \
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

# The retired family name is refused on EVERY channel, and Oracle's own catalog
# product `OCI AI Accelerator Packs` is not it.
cat > "$WORK/retired-header.md" <<'EOF'
OCI AI Accelerators — Workforce optimization

The pack aligns to Oracle's OCI AI Accelerator Packs pattern.
EOF
run_case "the retired family name is a finding on internal too" 1 \
  "$PY" "$TOOLS/lint_artifact.py" "$WORK/retired-header.md" --channel internal \
  --spec "$VALID" --catalog "$CAT"
expect "retired header" ART105 "Oracle AI & Data Solutions"

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

# CON003 reads a week figure as a tier duration. A planned next step and the source
# engagement's own length are not tier claims: the DHL executive summary's next step
# "Run the contracted 12 weeks … engagement" failed it although no tier said 12
# (2026-09-23). They pass; a wrong tier duration still fails, and so does the
# engagement's length printed against a tier — the drift the check exists for.
"$PY" - "$VALID" "$WORK" <<'PYWEEKS'
import sys, yaml
src, work = sys.argv[1], sys.argv[2]
spec = yaml.safe_load(open(src, encoding="utf-8"))
spec["meta"]["source_engagement"]["delivered"] = (
    "PoC over 10 weeks, Jun 2026, zone and technician allocation on field-service data")
spec["exec_summary"] = {"next_steps": [
    {"title": "Repeat the proof of value in a second region",
     "detail": "the same 10 weeks, on that region's own data"},
    "Hold the partner readout within 2 weeks of the go / no-go"]}
yaml.safe_dump(spec, open(work + "/pack-spec.engagement-weeks.yaml", "w", encoding="utf-8"),
               sort_keys=False, allow_unicode=True)
print("generated the engagement-weeks variant")
PYWEEKS
cat > "$WORK/weeks-engagement.md" <<'EOF'
Planned next steps

Repeat the proof of value in a second region
the same 10 weeks, on that region's own data

Hold the partner readout within 2 weeks of the go / no-go

The first engagement ran 10 weeks on live field-service data.
EOF
cat > "$WORK/weeks-wrong-tier.md" <<'EOF'
PoV Jumpstart runs 14 weeks on the customer's own data.
EOF
cat > "$WORK/weeks-engagement-on-a-tier.md" <<'EOF'
PoV Jumpstart runs 10 weeks, as the first engagement did.
EOF
WEEKS_SPEC="$WORK/pack-spec.engagement-weeks.yaml"
run_case "the engagement's weeks in a next step and an engagement line pass" 0 \
  "$PY" "$TOOLS/check_consistency.py" "$WEEKS_SPEC" "$WORK/weeks-engagement.md"
expect_absent "next-step and engagement weeks" CON003
run_case "a wrong tier duration still fails" 1 \
  "$PY" "$TOOLS/check_consistency.py" "$WEEKS_SPEC" "$WORK/weeks-wrong-tier.md"
expect "a wrong tier duration" CON003 "14 weeks"
run_case "the engagement's length printed against a tier still fails" 1 \
  "$PY" "$TOOLS/check_consistency.py" "$WEEKS_SPEC" "$WORK/weeks-engagement-on-a-tier.md"
expect "the engagement's length on a tier" CON003 "10 weeks"

# ------------------------------------------------- the architecture model and its three renderers
# One model, three pictures. The fixture's model must build clean; the deck slide, the
# one-pager's strip and the generated site figure must all draw it; and a model with one
# node renamed must fail against those same three artifacts — that failure is the whole
# point of the check, so it is asserted, not assumed.
say ""
say "build_diagram.py / diagram_to_site.py / check_diagram.py"
REPO="$(cd "$TESTS/../../.." && pwd)"
DECK_FIX="$REPO/plugins/oracle-packs/skills/deck/tests/fixture-pack-spec.yaml"
if [ ! -f "$DECK_FIX" ]; then
  bad "the deck fixture is missing: $DECK_FIX"
else
  mkdir -p "$WORK/pack"
  # The one-pager's capability matrix needs an explicit level per row; the deck fixture
  # carries prose, so the shared copy these renderers build from gets the levels added.
  "$PY" - "$DECK_FIX" "$WORK/pack/pack-spec.yaml" <<'EOF'
import re, sys
out = []
for line in open(sys.argv[1], encoding="utf-8"):
    out.append(line)
    m = re.match(r"^(\s*)- area: ", line)
    if m:
        out.append(m.group(1) + "  levels: {pov: partial, integration: included, scaling: advanced}\n")
open(sys.argv[2], "w", encoding="utf-8").writelines(out)
EOF

  run_case "the fixture's architecture model is valid" 0 \
    "$PY" "$TOOLS/build_diagram.py" "$WORK/pack/pack-spec.yaml" --check
  expect "the model" "Workforce optimization by SoftServe" "NVIDIA cuOpt" "Reviewer approves"

  "$PY" "$TOOLS/build_diagram.py" "$WORK/pack/pack-spec.yaml" \
        --out "$WORK/pack/architecture.json" >/dev/null 2>&1
  MODEL="$WORK/pack/architecture.json"

  # a source whose arrow says nothing is not a diagram the model will hand over
  sed 's|^      data: technicians, availability, bookings, default allocations|      data: ""|' \
      "$WORK/pack/pack-spec.yaml" > "$WORK/pack-spec.no-edge.yaml"
  run_case "a source with no edge fails the model" 1 \
    "$PY" "$TOOLS/build_diagram.py" "$WORK/pack-spec.no-edge.yaml" --check
  expect "a source with no edge" "has no edge"

  # the site figure, generated from the model and wrapped as diagrams.js is
  SITE_TOOL="$REPO/plugins/oracle-packs-web/skills/listing/tools/diagram_to_site.py"
  printf 'window.SITE_DIAGRAMS = {\n' > "$WORK/diagrams.js"
  "$PY" "$SITE_TOOL" "$MODEL" --slug workforce-optimization 2>/dev/null >> "$WORK/diagrams.js"
  printf '};\n' >> "$WORK/diagrams.js"
  run_case "the generated site figure draws the model" 0 \
    "$PY" "$TOOLS/check_diagram.py" "$MODEL" --site "$WORK/diagrams.js" --slug workforce-optimization

  # the one-pager's strip (HTML only: the PDF step needs Chrome, the picture does not)
  "$PY" "$REPO/plugins/oracle-packs/skills/one-pager/tools/build_one_pager.py" \
        "$WORK/pack/pack-spec.yaml" --out "$WORK/op" --no-pdf >/dev/null 2>&1
  OP="$WORK/op/workforce-optimization-one-pager-partner_print.html"
  if [ -f "$OP" ]; then
    run_case "the one-pager's strip draws the model" 0 \
      "$PY" "$TOOLS/check_diagram.py" "$MODEL" --one-pager "$OP"
  else
    bad "the one-pager did not build from the fixture"
  fi

  # the deck's architecture slide (needs python-pptx, like the deck sub-suite)
  DECK=""
  if "$PY" -c "import pptx" >/dev/null 2>&1; then
    "$PY" "$REPO/plugins/oracle-packs/skills/deck/tools/build_deck_v2.py" \
          "$WORK/pack/pack-spec.yaml" --out "$WORK/deck" >/dev/null 2>&1
    DECK="$WORK/deck/workforce-optimization-sales-deck.pptx"
    if [ -f "$DECK" ]; then
      run_case "the deck's architecture slide draws the model" 0 \
        "$PY" "$TOOLS/check_diagram.py" "$MODEL" --deck "$DECK"
    else
      bad "the deck did not build from the fixture"
      DECK=""
    fi
  else
    say "  (deck slide skipped: $PY has no python-pptx)"
  fi

  # one node renamed: every artifact that still says the old name is drift
  "$PY" - "$MODEL" "$WORK/architecture-renamed.json" <<'EOF'
import json, sys
model = json.load(open(sys.argv[1], encoding="utf-8"))
model["sources"][0]["name"] = "Dispatch system of record"
json.dump(model, open(sys.argv[2], "w", encoding="utf-8"), indent=2, ensure_ascii=False)
EOF
  set -- "$TOOLS/check_diagram.py" "$WORK/architecture-renamed.json" \
         --site "$WORK/diagrams.js" --slug workforce-optimization
  [ -f "$OP" ] && set -- "$@" --one-pager "$OP"
  [ -n "$DECK" ] && set -- "$@" --deck "$DECK"
  run_case "a renamed node fails the check" 1 "$PY" "$@"
  expect "a renamed node" "Dispatch system of record"

  # a renamed DESTINATION: the one-pager draws every destination the deck does, so it
  # catches this too — the strip used to drop destination-only systems and the check
  # used to allow it, which is exactly the drift the one-model rule exists to stop.
  "$PY" - "$MODEL" "$WORK/architecture-renamed-dest.json" <<'EOF'
import json, sys
model = json.load(open(sys.argv[1], encoding="utf-8"))
only = [d for d in model["destinations"] if not d["writeback"]]
only[0]["name"] = "Analytics warehouse"
json.dump(model, open(sys.argv[2], "w", encoding="utf-8"), indent=2, ensure_ascii=False)
EOF
  if [ -f "$OP" ]; then
    run_case "a renamed destination fails on the one-pager" 1 \
      "$PY" "$TOOLS/check_diagram.py" "$WORK/architecture-renamed-dest.json" --one-pager "$OP"
    expect "a renamed destination" "Analytics warehouse" "BI"
  fi
  if [ -n "$DECK" ]; then
    run_case "a renamed destination fails on the deck" 1 \
      "$PY" "$TOOLS/check_diagram.py" "$WORK/architecture-renamed-dest.json" --deck "$DECK"
  fi
  run_case "a renamed destination fails on the site figure" 1 \
    "$PY" "$TOOLS/check_diagram.py" "$WORK/architecture-renamed-dest.json" \
    --site "$WORK/diagrams.js" --slug workforce-optimization

  run_case "a missing model is a usage error" 2 \
    "$PY" "$TOOLS/check_diagram.py" "$WORK/not-a-model.json" --site "$WORK/diagrams.js"
fi

# ------------------------------------------ the figure-less metric caveat, one wording
# Where no cleared figure stands, the deck's proof tiles, the one-pager's strip and the
# executive summary all say "to be measured in the proof of value"; the one-pager and
# the executive summary add "results to follow." One wording in three builders, so the
# artifacts of one pack cannot disagree on tense (2026-09-23).
say ""
say "the figure-less metric caveat"
for f in deck/tools/build_deck_v2.py one-pager/tools/build_one_pager.py \
         exec-summary/tools/build_exec_summary.py; do
  run_case "$(basename "$f") says 'to be measured in the proof of value'" 0 \
    grep -q -i "to be measured in the proof of value" "$TESTS/../../../plugins/oracle-packs/skills/$f"
done
for f in one-pager/tools/build_one_pager.py exec-summary/tools/build_exec_summary.py; do
  run_case "$(basename "$f") adds 'results to follow.'" 0 \
    grep -q "in the proof of value; results to follow." "$TESTS/../../../plugins/oracle-packs/skills/$f"
done

# ------------------------------------ the listing inserter writes the kit-links entry
# Site round 12 moved every kit link into links.json at the site's root, and the
# site's checker fails a product with no entry there, so the inserter writes one in
# the same run as the catalog entry: six keys in the site's order, all "" except
# the walkthrough's path. A dry run writes nothing, and a slug the file already
# carries is refused before anything is written (2026-09-23).
say ""
say "insert-product.mjs --links"
if ! command -v node >/dev/null 2>&1; then
  say "  (skipped: no node)"
else
  INSERTER="$(cd "$TESTS/../../.." && pwd)/plugins/oracle-packs-web/skills/listing/tools/insert-product.mjs"
  LK="$WORK/links-site"
  mkdir -p "$LK"
  cat > "$LK/content.js" <<'EOF'
window.SITE_CONTENT = {
  products: [
    { slug: "existing-pack", name: "Existing pack" }
  ]
};
EOF
  cp "$LK/content.js" "$LK/content.pristine.js"
  cat > "$LK/entry.js" <<'EOF'
/* one product object literal, as the listing skill writes it */
{
  slug: "new-pack",
  name: "New pack"
}
EOF
  cat > "$LK/links.json" <<'EOF'
{
  "siteUrl": "",
  "products": {
    "existing-pack": {
      "onePager": "",
      "salesDeck": "",
      "featureList": "",
      "interactiveDemo": "",
      "interactiveDemoArtifact": "",
      "video": ""
    }
  }
}
EOF
  cp "$LK/links.json" "$LK/links.before.json"

  run_case "a dry run with --links" 0 \
    node "$INSERTER" --content "$LK/content.js" --entry "$LK/entry.js" \
    --links "$LK/links.json" --demo-path demo/new-pack/index.html --dry-run
  expect "the dry run" "links.json kit-links entry added" "nothing written"
  run_case "the dry run left links.json as it was" 0 cmp -s "$LK/links.before.json" "$LK/links.json"

  run_case "--demo-path without --links is a usage error" 2 \
    node "$INSERTER" --content "$LK/content.js" --entry "$LK/entry.js" \
    --demo-path demo/new-pack/index.html --dry-run

  run_case "a real run with --links" 0 \
    node "$INSERTER" --content "$LK/content.js" --entry "$LK/entry.js" \
    --links "$LK/links.json" --demo-path demo/new-pack/index.html
  run_case "links.json carries the new entry, the other five keys empty" 0 \
    "$PY" -c 'import json, sys
e = json.load(open(sys.argv[1], encoding="utf-8"))["products"]["new-pack"]
print(",".join(e)); print(e["interactiveDemo"])
sys.exit(0 if all(v == "" for k, v in e.items() if k != "interactiveDemo") else 1)' "$LK/links.json"
  expect "the new entry" "onePager,salesDeck,featureList,interactiveDemo,interactiveDemoArtifact,video" \
    "demo/new-pack/index.html"

  # Against the untouched catalog, so the links check (not the catalog's own
  # duplicate check) is the one that has to refuse.
  run_case "a slug links.json already carries is refused" 1 \
    node "$INSERTER" --content "$LK/content.pristine.js" --entry "$LK/entry.js" \
    --links "$LK/links.json"
  expect "the refusal" "already carries" "nothing written"
  run_case "the refused run left its catalog as it was" 0 cmp -s "$LK/content.js.bak" "$LK/content.pristine.js"

  # Under a site.manifest.json the backups leave the site's tree for its git-ignored
  # .work/insert-product/<timestamp>/: the site repo autosyncs, so a .bak beside
  # content.js would be committed (2026-09-23). The runs above have no manifest
  # above them and keep the old place, beside the file.
  say ""
  say "insert-product.mjs backups under a site manifest"
  MSITE="$WORK/manifest-site"
  mkdir -p "$MSITE/site/data"
  printf '{ "paths": { "content": "site/data/content.js" } }\n' > "$MSITE/site.manifest.json"
  cp "$LK/content.pristine.js" "$MSITE/site/data/content.js"
  run_case "a real run under a site manifest" 0 \
    node "$INSERTER" --content "$MSITE/site/data/content.js" --entry "$LK/entry.js"
  expect "the run under a manifest" ".work/insert-product/"
  BAK="$(find "$MSITE/.work/insert-product" -type f -name content.js 2>/dev/null | head -1)"
  run_case "the backup landed under .work/insert-product/" 0 test -f "$BAK"
  run_case "the backup is the catalog as it was" 0 cmp -s "$BAK" "$LK/content.pristine.js"
  run_case "no backup beside the file" 1 test -e "$MSITE/site/data/content.js.bak"
fi

# ------------------------------------------------ the exemplar and the site
# The listing exemplar is GENERATED from the site manifest's exemplarProduct by
# refresh-exemplar.mjs, never edited by hand: the hand copy drifted (a retired key,
# "Scale" for "Scaling", old category ids) and would have failed the site's own
# checker (2026-09-23). Against the live site, drift is a WARNING, not a failure: the
# site moves on its own schedule and must not block an unrelated release. Against a
# scratch site the tool must blank the account-bound URLs, write what the inserter
# reads, pass --check on its own output, fail it once the site's entry changes, and
# refuse a deny-listed name without printing it.
say ""
say "refresh-exemplar.mjs (the exemplar and the site)"
if ! command -v node >/dev/null 2>&1; then
  say "  (skipped: no node)"
else
  LISTING_TOOLS="$(cd "$TESTS/../../.." && pwd)/plugins/oracle-packs-web/skills/listing/tools"
  REFRESH="$LISTING_TOOLS/refresh-exemplar.mjs"
  SITE_ROOT="${ORACLE_SITE_ROOT:-$HOME/Documents/GitHub/Oracle-Solutions-Site}"
  if [ ! -f "$SITE_ROOT/site.manifest.json" ]; then
    say "  (skipped: no site root)"
  else
    LAST="$(node "$REFRESH" --site "$SITE_ROOT" --check 2>&1)"; got=$?
    case "$got" in
      0) ok "the exemplar matches the site's exemplar product" ;;
      1) printf '%s\n' "$LAST" | sed 's/^/       | /'
         warn "WARNING: the exemplar drifts from the site's exemplar product — run node plugins/oracle-packs-web/skills/listing/tools/refresh-exemplar.mjs --site $SITE_ROOT" ;;
      *) printf '%s\n' "$LAST" | sed 's/^/       | /'
         warn "WARNING: the exemplar could not be checked against the site (exit $got) — see the line above" ;;
    esac
  fi

  MS="$WORK/mini-site"
  mkdir -p "$MS/site/assets" "$MS/site/data"
  cat > "$MS/site.manifest.json" <<'EOF'
{
  "contract": { "round": 99 },
  "exemplarProduct": "demo-pack",
  "paths": {
    "publishRoot": "site",
    "content": "site/data/content.js",
    "config": "site/data/config.js",
    "diagrams": "site/data/diagrams.js",
    "links": "links.json"
  }
}
EOF
  printf 'window.SITE_BRAND = {};\n' > "$MS/site/assets/brand.js"
  cat > "$MS/site/data/content.js" <<'EOF'
window.SITE_CONTENT = {
  products: [
    { slug: "other-pack", name: "Other pack" },
    {
      slug: "demo-pack",
      name: "Demo pack",
      oneLiner: "Plans the field week in minutes, and a dispatcher approves it.",
      jumpstart: { next: [{ tier: "Integration" }, { tier: "Scaling" }] }
    }
  ]
};
EOF
  cat > "$MS/site/data/config.js" <<'EOF'
window.SITE_CONFIG = {
  productOrder: ["other-pack", "demo-pack"],
  products: {
    "other-pack": { marketplace: false, marketplaceUrl: "", video: false, videoPoster: "", successStoryUrl: "" },
    "demo-pack": { marketplace: true, marketplaceUrl: "", video: true, videoPoster: "", successStoryUrl: "" }
  }
};
EOF
  cat > "$MS/site/data/diagrams.js" <<'EOF'
window.SITE_DIAGRAMS = {
  "demo-pack": {
    layout: "flow",
    sources: [{ title: ["Source"], sub: ["Records"] }],
    target: { title: ["Reviewer", "approves"], sub: ["Nothing ships unreviewed"], accent: true },
    note: "A person approves every plan"
  }
};
EOF
  cat > "$MS/links.json" <<'EOF'
{
  "siteUrl": "https://example.com/site",
  "products": {
    "other-pack": { "onePager": "", "salesDeck": "", "featureList": "", "interactiveDemo": "", "interactiveDemoArtifact": "", "video": "" },
    "demo-pack": {
      "onePager": "",
      "salesDeck": "",
      "featureList": "",
      "interactiveDemo": "demo/demo-pack/index.html",
      "interactiveDemoArtifact": "https://claude.ai/code/artifact/test-only-artifact",
      "video": "https://video.example.com/test-only-recording"
    }
  }
}
EOF
  EX="$WORK/exemplar.js"
  run_case "the tool writes the exemplar from a scratch site" 0 \
    node "$REFRESH" --site "$MS" --out "$EX"
  run_case "the artifact URL and the recording are not in it" 1 grep -q "test-only" "$EX"
  run_case "block 4 carries interactiveDemoArtifact as \"\"" 0 \
    grep -q '"interactiveDemoArtifact": ""' "$EX"
  run_case "block 4 keeps the walkthrough path" 0 \
    grep -q '"interactiveDemo": "demo/demo-pack/index.html"' "$EX"
  run_case "--check is clean on what the tool wrote" 0 \
    node "$REFRESH" --site "$MS" --out "$EX" --check
  run_case "a second run writes nothing" 0 node "$REFRESH" --site "$MS" --out "$EX"
  expect "the second run" "nothing written"

  # The inserter reads the generated file: the entry by its JSON-quoted "slug" key,
  # the switch block by its "<slug>": { key.
  IT="$WORK/insert-target"
  mkdir -p "$IT"
  printf 'window.SITE_CONTENT = {\n  products: [\n    { slug: "existing-pack", name: "Existing pack" }\n  ]\n};\n' \
    > "$IT/content.js"
  printf 'window.SITE_CONFIG = {\n  productOrder: ["existing-pack"],\n  products: {\n    "existing-pack": { marketplace: false }\n  }\n};\n' \
    > "$IT/config.js"
  run_case "the inserter takes the generated exemplar (dry run)" 0 \
    node "$LISTING_TOOLS/insert-product.mjs" --entry "$EX" --content "$IT/content.js" \
    --config "$IT/config.js" --config-entry "$EX" --dry-run
  expect "the dry run" '"demo-pack"' "1 → 2 products" "config.js switch block added"

  sed 's/in minutes, and/in an afternoon, and/' "$MS/site/data/content.js" > "$MS/content.edited"
  mv "$MS/content.edited" "$MS/site/data/content.js"
  run_case "--check fails once the site's entry changes" 1 \
    node "$REFRESH" --site "$MS" --out "$EX" --check
  expect "the drift" "drift" "block 1"

  # A deny-listed name in the site's copy: refused, named by its line, never printed.
  sed "s|Plans the field week|Plans the $DENY_NAME field week|" "$MS/site/data/content.js" > "$MS/content.edited"
  mv "$MS/content.edited" "$MS/site/data/content.js"
  cp "$EX" "$WORK/exemplar.before.js"
  run_case "a deny-listed name in the site's entry is refused" 1 \
    node "$REFRESH" --site "$MS" --out "$EX"
  expect "the refusal" "deny-list entry on line" "block 1" "oneLiner" "Nothing written"
  expect_absent "the refusal" "$DENY_NAME"
  run_case "the refused run left the exemplar as it was" 0 cmp -s "$WORK/exemplar.before.js" "$EX"

  run_case "no site root is a usage error" 2 \
    env -u ORACLE_SITE_ROOT node "$REFRESH" --out "$WORK/unused.js"
fi

# --------------------------------------------------------------- context_budget
# EVERY skill's manifest must stay inside its per-step reading budget; a card that
# grows past its share fails here, not in a live run. The loop finds the manifests
# rather than listing them, so a new skill is covered the day it gets one.
say ""
say "context_budget.py"
REPO="$(cd "$TESTS/../../.." && pwd)"
MANIFESTS="$(find "$REPO/plugins" -path '*/skills/*/references/cards/manifest.yaml' \
             -not -path '*/plugins/*/shared/*' | sort)"
if [ -z "$MANIFESTS" ]; then
  bad "no skill manifests found under $REPO/plugins"
else
  # Every skill named in the marketplace's plugins must have one — a skill that
  # silently loses its manifest would otherwise just drop out of this loop.
  SKILLS="$(find "$REPO/plugins" -path '*/skills/*/SKILL.md' \
            -not -path '*/plugins/*/shared/*' | wc -l | tr -d ' ')"
  FOUND="$(printf '%s\n' "$MANIFESTS" | wc -l | tr -d ' ')"
  if [ "$SKILLS" = "$FOUND" ]; then
    ok "every skill has a cards manifest ($FOUND of $SKILLS)"
  else
    LAST="$MANIFESTS"
    bad "$FOUND manifests for $SKILLS skills — a skill is missing references/cards/manifest.yaml"
  fi
  for m in $MANIFESTS; do
    label="$(basename "$(dirname "$(dirname "$(dirname "$m")")")")"
    run_case "$label is within budget" 0 \
      "$PY" "$TOOLS/context_budget.py" "$m" --quiet
  done
fi
run_case "a missing manifest is a usage error" 2 \
  "$PY" "$TOOLS/context_budget.py" "$WORK/no-manifest.yaml"

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
[ -n "$WARNINGS" ] && printf '%s' "$WARNINGS"
if [ "$FAIL" -eq 0 ]; then
  say "run_tests: $PASS passed, 0 failed"
  exit 0
fi
say "run_tests: $PASS passed, $FAIL FAILED (work dir kept: $WORK)"
KEEP=1
exit 1
