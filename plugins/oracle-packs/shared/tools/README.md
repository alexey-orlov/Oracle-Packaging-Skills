# shared/tools — the linters every pack skill runs

The command-line tools every pack skill runs, and their shared library. They are
the executable form of `shared/schema/pack-spec.md` and
`shared/references/naming-and-clearance.md`: when a rule moves, those files are
rewritten first and the tools follow in the same pass. A skill that produces an artifact is not done until the relevant tool here
is green on it.

Python 3, standard library only, plus **PyYAML** — the spec's front matter, the
catalog, anything else that reads YAML. Call every tool through `py`, the
interpreter resolver beside them: it finds a Python that has the packages in
`requirements.txt`, or provisions one in `~/.oracle-packs/venv` on first use —
never in system Python — and runs the tool with it (`py --check` shows which). A
tool run without the packages exits 2 and prints the install line. The linters
read and report and never write; `packspec.py set` and `convert` write the spec, and
`pack_paths.py --create` makes the pack's folders. The architecture model is built from
the spec by every renderer and never stored.

```
py                    the interpreter resolver every tool runs through (--which, --check)
requirements.txt      the Python packages; a copy of plugins/oracle-packs/requirements.txt
packspec.py           the spec: the one loader and writer of pack-spec.md; get / set / check / convert
pack_paths.py         where a pack's files go: the spec in the repo, the work on this machine
spec_stamp.py         the spec stamp every builder writes into its file, and reads back
lint_spec.py          validates a pack spec against the schema
lint_artifact.py      clearance, naming, vocabulary, prices and figures per channel
check_consistency.py  every artifact of a pack against its spec, and the spec it was built from
build_diagram.py      the pack's ONE architecture model, for all three pictures
check_diagram.py      the deck, the one-pager and the site figure against that model
denylist.txt          the customer names and marks that must never ship (internal)
packlint.py           shared library — the spec through packspec.py, the catalog with line numbers, text extraction, reporting
context_budget.py     a skill's per-step reading budget and per-card word caps, against its cards manifest
regen_roadmap.py      regenerates shared/data/roadmap-*.csv (owned separately)
tests/run_tests.sh    the suite; fixtures in tests/fixtures/
```

## Exit codes, output shape

Every tool behaves the same way, so a skill can branch on the code alone:

| code | meaning |
|---|---|
| **0** | clean — nothing to fix |
| **1** | findings — the artifact or spec needs work |
| **2** | usage or dependency error — bad arguments, an unreadable file, or PyYAML missing (it prints the install line) |

Findings print one per line as `file:line: CODE message`, warnings first, then a
tool-specific table (the spec's completeness table, the consistency matrix), then
one summary line. For `.docx`, `.pptx` and `.pdf` the line number is the extracted
paragraph and the message names the part it came from (`[slide 3 notes]`).
Repeats of one finding in one file collapse into a single line with an occurrence
count. Anything a tool **could not** evaluate — a missing catalog, a `.pdf` with
no `pdftotext` installed, a check that needs `--spec` — is listed as
`not evaluated:` and counted in the summary, because a check that could not run is
not a check that passed.

## packspec.py

```
shared/tools/py shared/tools/packspec.py get <spec> <key.path>                    the value, as JSON
shared/tools/py shared/tools/packspec.py set <spec> <key.path> <value> [--source <src>]
shared/tools/py shared/tools/packspec.py check <spec>
```

The spec is one Markdown file per pack, `packs/<slug>/pack-spec.md`, in the fixed layout
`shared/schema/pack-spec.md` sets out. Every tool reads it through
`packspec.load(path) -> (data, linemap)`: `data` is the spec as a mapping, and `linemap` gives
each key's line for findings. The contract is
tested on every spec in the repo: **lossless** (`load(dump(d)) == d`), **canonical**
(`dump(load(md)) == md`), **strict** (a slip — a row with a cell too many or too few, an unknown
section or label, an unescaped `|` in a cell, a price that does not read — is a finding on its
line, never a guess) and **kept** (a key the layout does not know becomes a table column or an
entry in the fenced YAML under `## Other fields`, and is named).

`set` takes JSON when the value parses as JSON, else text; a typed key also takes its own syntax
(`€95K · indicative`, `6–8 weeks (target 8, hard cap 10)`, `yes`); `--source` sets the key's
sibling `source`; the first `set` on a path with no spec creates it. Every write re-renders the
whole file and is refused unless its round trip is exact. `check` names each line that does not
parse or is not in the canonical form, and each key the layout does not know. Exit 0 done ·
1 a finding · 2 usage.

## pack_paths.py

```
shared/tools/py shared/tools/pack_paths.py <slug> [--repo <dir>] [--create] [--json]
```

Where a pack's files go (the owner's layout, 2026-09-24). The spec and the pictures it
names live in this repo's `packs/<slug>/`, committed and shared; everything else — the artifacts, the intake, the inventory and its extracts of
customer documents, sources, research, the decisions log — goes to the work folder,
`$ORACLE_PACKS_OUT/<slug>/`, else `~/oracle-packs/<slug>/`, and never enters the repo.
The repo is `--repo`, else `$ORACLE_PACKS_ROOT`, else the working directory or its
nearest ancestor holding `.claude-plugin/marketplace.json` named
`oracle-packaging-skills`; none found exits 2 with one line saying to clone it and set
`ORACLE_PACKS_ROOT` or pass `--repo`. It prints `slug`, `repo`, `spec_dir`, `spec`,
`work`, `artifacts` and `spec_exists` as `key=value` lines (or one JSON object), plus
`spec_sha`, `spec_commit` and `spec_dirty` when the spec exists — and `spec_error`, with
`spec_sha=none`, when it does not parse. `spec` is `pack-spec.md`. `--create` makes `spec_dir`, `work` and
`artifacts`, nothing else.

## spec_stamp.py

```
shared/tools/py shared/tools/spec_stamp.py <artifact>...     each file's stamp, or "no stamp"
shared/tools/py shared/tools/spec_stamp.py --spec <spec>      the stamp a build writes now
```

Every builder writes `pack-spec sha256:<12 hex> commit:<short hash|uncommitted|none>`
into its file — `dc:identifier` in a `.docx` or `.pptx`, `<meta name="pack-spec">` in the
one-pager's HTML, `/PackSpec` in its PDF — so a file built on one machine still says
which spec it reflects. The sha is of the spec's canonical data — the sorted JSON of its
values (`packspec.data_sha`) — not of the file's bytes, so a re-render, a whitespace edit or
the conversion from YAML never marks a built file stale; a changed value does.
`uncommitted` is a spec git reports modified or untracked; `none` is a spec outside a git
checkout. `check_consistency.py` reads it back (CON006, CON007), and `/oracle-packs:build`
logs it with each approval.

## lint_spec.py

```
shared/tools/py shared/tools/lint_spec.py packs/<slug>/pack-spec.md [--strict] [--signoff] \
        [--catalog shared/data/oracle-products.yaml] \
        [--roadmap shared/data/roadmap-items.csv] [--denylist shared/tools/denylist.txt]
```

Validates the spine: every component key present, the required keys inside each,
the four first-order components (problem ↔ solution, one-liner, ICP, name)
carrying a `user:<date>` source on `problem_solution.source`, `one_liner.source`,
`icp.source` and `meta.name_source` once `meta.status` is `confirmed`, product ids
that resolve to the catalog (in `oracle_products[]`, which is Oracle-vendor only,
and in `architecture.stack[].catalog_id`, which is where the NVIDIA components of
the stack are named), a roadmap id that resolves to the extract, the PoV
duration inside 4–8 weeks (above 8 needs a `justification`, above 10 is rejected),
one metric set, the three tier names exactly, no deny-listed customer name in
customer-facing copy, a one-liner that names no platform, vendor, engine, model
or data architecture, a `figure_status` and a `caveat` on every figure, all four
clearance channels recorded, and `open_questions` present (it may be empty). It
closes with a per-component completeness table — the thing to paste into a
sign-off message.

Two flags, two different questions. **`--strict` asks "is this spec complete?"** —
it promotes the warnings (missing catalog or roadmap file, unfilled recommended
keys, a name variant that does not follow the channel rule) to findings, and it is
the gate a `draft` is expected to pass: the worked example in
`examples/workforce-optimization/` is clean under it. **`--signoff` asks "would
this pass as confirmed?"** — it applies the four first-order `user:<date>` source
rules whatever `meta.status` says. That rule is on by itself once the status is
`confirmed` or `built`, so `--signoff` only asks the question early. On the worked
example it prints exactly the four SPEC003 lines saying the pack owner has not
walked the file through `/oracle-packs:spec` yet, which is true and is the point.

A figure written `-` is the spec's way of saying **defined and measured per
engagement, no cleared headline number**. The linter reads it as absent: no
`figure_status`, `caveat` or `attribution` is demanded for it, and a real
`figure_status` next to a `-` figure is itself a finding.

| code | rule |
|---|---|
| SPEC001 / SPEC002 | a component, or a required key inside one, is missing or empty |
| SPEC003 | a first-order component has no `user:<date>` source on a confirmed spec |
| SPEC004 / SPEC005 | a product id (`oracle_products[].id` or `architecture.stack[].catalog_id`) / the roadmap item id does not resolve |
| SPEC006 / SPEC007 | PoV above 8 weeks without justification / above the 10-week cap |
| SPEC008 | two metric sets — one KPI name, two figures |
| SPEC009 | the tier set or a tier name is not PoV Jumpstart / Integration / Scaling |
| SPEC010 | a deny-listed customer name in name, one-liner, problem ↔ solution, ICP, verticals or a KPI's `attribution.otherwise` |
| SPEC011 / SPEC012 | a figure with no `figure_status`, or a `figure_status` on a `-` figure / a figure with no `caveat` |
| SPEC013 | `clearance.customer_name_allowed` is missing a channel or is not boolean |
| SPEC014 | `open_questions` absent |
| SPEC015 / SPEC016 | an unknown `meta.status` / an unknown product `role` |
| SPEC017 | a `meta.name_variants` entry does not follow the channel rule (warning) |
| SPEC018 | `oracle_products[]` carries a non-Oracle catalog entry — NVIDIA components belong in `architecture.stack[].catalog_id` |
| SPEC019 / SPEC020 | `workflow.steps` has more than 7 steps — the pack's workflow is 5–7, grouped at the buyer's checkpoints, mechanics inside a step / fewer than 3 steps (warning) |
| SPEC021 / SPEC022 | more than 3 required Oracle products / more than 4 optional (warnings) — required is only what the pack cannot run without, optional only what a buyer would plausibly connect |
| SPEC023 | the capability tree is too fine for a one-page feature list (warning) — above 6 areas, 14 categories or 40 features, group at the capabilities sign-off |
| SPEC024 | a record in any list the layout knows (inputs, outputs, steps, the stack, industries, capability areas, categories and features, products, metrics, tiers, capability handling, open questions, provenance inputs) carries a key the layout does not define, or a feature has no status (warning) — usually a value YAML split at its commas, which silently drops everything after the comma |
| SPEC025 | no business metric in `kpis[]`, or a `kind` that is not `business` / `leading` / `technical` (warning) — sales artifacts print business metrics, so a set of proof criteria leaves every tile empty |
| SPEC026 | a metric whose name reads as a proof criterion or a vanity count is not marked `kind: technical` (warning) — agreement, precision, recall, accuracy, latency, coverage, confidence, F1, throughput, "processed", "ingested", "onboarded", "surfaced", signals, documents, tokens, uptime |
| SPEC027 | a `business` metric carries no `owner_role` (warning) — the buyer-side role who would sign the number off |
| SPEC028 | a retired family name ("OCI AI Accelerators", "OCI accelerator") in `meta.eyebrow`, `deck.running_header`, `exec_summary.running_header` or `one_pager.eyebrow` — the family name is **Oracle AI & Data Solutions** |
| SPEC029 | the spec does not parse — one finding on the line of the slip (packspec.py's message), and nothing else is checked |
| SPEC030 | `build.artifacts` or `build.audience` holds a value the build does not know |
| SPEC031 | `one_liner.full` or `.short` names the implementation — a platform, vendor, engine, model or data-architecture word (Oracle, OCI, NVIDIA, cuOpt, NeMo, AI-Q, Lakehouse, GPU, LLM, "gold layer", "semantic layer", "confidence score", "structured data" and the rest of `IMPLEMENTATION_TERMS`, the mini-site checker's own list; word-bounded, any case, plural allowed). A one-liner leads with the business value for a named role and object of work |
| SPEC900–902 | catalog absent / roadmap absent / a recommended key unfilled (warnings) |

## lint_artifact.py

```
shared/tools/py shared/tools/lint_artifact.py <file-or-dir> \
        --channel internal|partner_print|customer_site|demo \
        [--spec packs/<slug>/pack-spec.md] [--denylist ...] [--catalog ...]
```

The clearance gate. It extracts text from `.docx` (document, headers, footers,
notes), `.pptx` (slides **and** speaker notes), `.html`, `.js`, `.md`, `.txt`,
`.yaml` and `.pdf` (through `pdftotext`; skipped with a warning when poppler is
not installed), then applies naming-and-clearance §1–§4 for the channel given.
`internal` is the only channel where the deny-list stands down; the vocabulary
rules apply to the three customer-facing channels, except the one-liner rule
(ART206), which applies everywhere because the one-liner is inherited verbatim by
every artifact; naming, partner-standing, price-disclaimer and tier rules apply
everywhere. With `--spec` it also reads the
clearance switch (`clearance.customer_name_allowed[channel]`), the price set, the
channel's name variant and `figure_status`, so the price, name and "proven" checks
become real instead of skipped.

| code | rule |
|---|---|
| ART001 / ART002 / ART003 | a deny-listed customer name / a mark in an asset path or embedded media / an Oracle partner-standing claim |
| ART101 / ART102 / ART103 / ART104 | a catalog `not_this` spelling, unless it sits inside an accepted longer name (the bare `cuOpt` inside `NVIDIA cuOpt`) / "AIDP" outside internal / a near-miss vendor spelling / the wrong pack-name variant for the channel |
| ART105 | the retired family name ("OCI AI Accelerators", "OCI accelerator") anywhere in an artifact's text, on every channel — the family name is **Oracle AI & Data Solutions**; Oracle's own catalog product `OCI AI Accelerator Packs` is exempt |
| ART201 / ART202 | a count, total or ceiling / a negation or gap ("so far", "yet") |
| ART203 / ART204 / ART205 | packaging vocabulary / operating-model vocabulary / internal taxonomy |
| ART206 | packaging vocabulary inside the pack's one-liner — **every** channel, internal included (needs `--spec`) |
| ART301 / ART302 / ART303 | a EUR figure with no disclaimer within 200 characters / a non-PoV price on the customer site / any price inside a demo |
| ART401 / ART402 / ART403 | "proven" with no `delivered_result` figure beside it / a non-canonical tier name / an S/M/L size tag on a customer-facing channel |
| ART900 / ART901 | a file was skipped / a check needs `--spec` or the catalog (warnings) |

## check_consistency.py

```
shared/tools/py shared/tools/check_consistency.py packs/<slug>/pack-spec.md <artifact>...
```

Asks whether the artifacts say the **same** thing, which the per-artifact linter
cannot see. For each artifact it checks the one-liner (full or short), the tier
names, the PoV duration wording, the prices and the KPI figures that actually
appear, against the spec. **An absent component is information, not a finding** —
artifacts omit by design — so the output is a matrix of artifact × component with
✓ identical, ✗ differs, – absent, and only ✗ sets the exit code.

It also asks **which spec each artifact was built from**. Every builder writes a
stamp into its file — `pack-spec sha256:<12 hex> commit:<short hash|uncommitted|none>`
(`spec_stamp.py`) — and the stamp's sha is compared with the sha of the spec given
here. The matrix's last column, `spec`, shows it: ✓ built from this spec · ✗ from an
earlier version · – no stamp. Both stamp rules are warnings: they never change the
exit code, and the fix is a rebuild from the current spec.

| code | rule |
|---|---|
| CON001 | the one-liner differs from `one_liner.full` / `.short` |
| CON002 | a tier is named something the spec does not |
| CON003 | a duration in weeks matches no tier's `duration_weeks` — except a figure inside one of the spec's own `exec_summary.next_steps`, or the engagement's own length (stated in `meta.source_engagement`) in a sentence about the engagement; never when that sentence names a tier |
| CON004 | a EUR figure matches no price in the spec |
| CON005 | a KPI is printed with a figure the spec does not carry |
| CON006 | the artifact's stamp names another version of the spec: "built from an earlier version of the spec — rebuild before sending" (warning) |
| CON007 | a `.docx`, `.pptx`, `.html` or `.pdf` with no stamp: "no spec stamp: built before 2026-09-24 or by hand; which spec it reflects is unknown" (warning). Other formats — a listing entry, a markdown file — carry no stamp by design and are not reported |

## build_diagram.py

```
shared/tools/py shared/tools/build_diagram.py <spec>                  # the model in sentences, writes nothing
shared/tools/py shared/tools/build_diagram.py <spec> --out model.json  # and a copy of it, e.g. for a test
```

The pack's architecture picture, derived once and rendered three times. It reads
`architecture.inputs[]`, `.stack[]`, `.outputs[]`, `oracle_products[]`, the catalog,
`meta.name` in the channel's variant and the workflow's human step, and writes a model
of sources, platform, app, engine, destinations, gate and the one invariant. **Levels of
detail are the contract**: `name` prints everywhere, `line` on the deck and the one-pager,
`detail` only on the mini-site. It is also a library — `build_model(spec) -> dict` — which
is how the deck and the one-pager builders consume it.

Exit 1, with a plain message, when the picture cannot be drawn as the brief stands: a
source with no edge, an output with no destination, an engine that would be unnamed, an
app box without the pack's name. Rules: `shared/references/architecture-diagram.md`.

## check_diagram.py

```
shared/tools/py shared/tools/check_diagram.py <spec> \
        --deck <pptx> --one-pager <html> --site <diagrams.js> --slug <slug>
```

Reads the picture back out of each artifact — the deck's architecture slide (found by its
title), the one-pager's `.arch` strip, the site's `SITE_DIAGRAMS[slug]` — and asserts that
every node name the artifact should carry is there **exactly**, that the arrow labels are on
the deck and the one-pager, and that no artifact draws a box the model has never heard of.
Exit 1 is drift: rebuild the artifact from the model, never edit the picture in the file.

## denylist.txt

One entry per line, `#` comments allowed; plain entries match case-sensitively on
word boundaries, `~entry` matches case-insensitively, an entry containing `/`
matches as a path fragment, and every entry is also matched against the slugs
inside file names and asset paths (so a `<customer>-logo.svg` or `<customer>_air.png`
is caught). The header says how to add a line. **It is internal to SoftServe** — the
file exists so that names which sit in the source SoWs, decks and transcripts a
pack is generalized from cannot survive a copy-paste into something external. It
is extended, never trimmed, and clearance to name a customer is granted per pack
in the spec, never by deleting a line here.

## Wiring this into a skill's definition of done

In the skill that produces the artifact, after the file is written and before the
review hand-off:

1. `lint_spec.py <spec>` — run it at the top of every build skill too, and stop
   with the completeness table if it exits 1 rather than filling a gap yourself.
2. `lint_artifact.py <the file just written> --channel <the artifact's channel> --spec <spec>` —
   feature list and internal exec slide are `internal`, one-pager and sales deck
   are `partner_print`, the listing is `customer_site`, the walkthrough is `demo`.
3. `check_consistency.py <spec> <every artifact built so far>` — after the second
   artifact exists, and again at the end of `/oracle-packs:build`.
4. `check_diagram.py <spec> --deck/--one-pager/--site <this artifact>` —
   wherever the artifact carries the architecture picture.
5. Exit 1 is not a pass. Fix the artifact, or change the spec and rebuild from it —
   never edit an artifact away from the spec to silence a finding.
6. Hand the owner the `not evaluated:` lines together with the artifact.

Run the suite after touching any rule: `tests/run_tests.sh` (it
runs every tool through `py`; `PY=<interpreter>` points it at another one). It builds
its broken fixtures from the good one and reads the deny-listed name it needs out
of `denylist.txt`, so no customer name is committed to this repo.

## Known limits

- **Proximity, not layout.** "Within 200 characters" is measured in the extracted
  text. In a structured data file (`content.js`) a disclaimer that renders in the
  same visual block can sit far away in the source, so lint the rendered output as
  well when a price check looks wrong.
- **ART103 is a heuristic**: a vendor phrase is flagged when it shares two or more
  significant words with a catalog name without matching it. It finds
  "Oracle AI Lakehouse" and "Oracle Fusion Field Services"; it cannot find a
  wholly invented product.
- **Asset matching is deliberately eager.** A file named `hero-sky-line.jpg`
  trips the deny-list entry `Sky`. Rename the asset rather than trimming the list.
- **`--spec` is not optional in practice.** Without it, four checks cannot run and
  say so; a skill should always pass it.
