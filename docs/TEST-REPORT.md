# Integration test report

_The integration pass over the ten builders' output, 2026-09-18: what ran, what passed, what was fixed (file: change), and what is still rough. Rewritten to current truth — never appended with dated sections._

**Environment.** macOS (Darwin 24.6) · Python 3.14.6 in a throwaway venv outside the repo · PyYAML 6.0.3, python-docx 1.2.0, python-pptx 1.0.2, Pillow 12.3.0, pypdf 6.19.0 · Node v26.0.0 · Google Chrome (system) · `pdftotext` and `qlmanage` present, `soffice` present but not used (its `--convert-to` is dead on this machine).

**Headline.** Everything in steps 1–9 runs green. `lint_spec.py --strict`, the four document builders, `lint_artifact.py` on every output, `check_consistency.py` across all five files, `shared/tools/tests/run_tests.sh` (65 assertions), both plugin manifests and the marketplace all pass. Nothing was silenced to get there: every finding was fixed in the tool, the reference, the example or the fixture, and what is still rough is listed in §10.

---

## 1. Cross-reference audit

Every backticked path and every tool invocation in all eight `SKILL.md` files, plus every path in every `.md` under the repo, was resolved against the filesystem, and every CLI flag mentioned in a skill was checked against the tool's own `--help`.

**Result: every repo-internal path now resolves.** What remains unresolved is external by design — `<site>/site/data/content.js` and `<site-root>/tools/deny-list.json` live in the mini-site repository, not here.

`deck/tools/render_probe.sh` was already present and correct: it detects `qlmanage`, `soffice`, `pdftoppm`, `pdftotext`, `node`, `python3`, Pillow, ImageMagick and `timeout`, and prints the contact-sheet recipe for what it found, including the `perl -e 'alarm N; exec @ARGV'` substitute for the missing `timeout`. No new file was needed.

| Fix | Change |
|---|---|
| `shared/schema/pack-spec.md` | "checked by `shared/tools/lint-spec.py`" → `lint_spec.py` (the file has always been underscored) |
| `plugins/oracle-packs/skills/exec-summary/references/exec-summary-anatomy.md` | two references to `references/brand-tokens.md`, which does not exist in this skill → `../deck/references/brand-tokens.md` |
| `plugins/oracle-packs/skills/deck/SKILL.md` | removed the invented `--only <n>` fast path — `build_deck.py` has no such flag and writes the whole deck from the spec every time; the fast path is now stated as it works (one line in the spec, one rebuild) |
| `plugins/oracle-packs/skills/deck/SKILL.md` | removed `--host-deck` from the deck skill (the flag belongs to `build_exec_summary.py`, which is where a paste-in section is built) |
| `plugins/oracle-packs/skills/exec-summary/tools/build_exec_summary.py` | **added** the `--channel {internal,partner_print}` flag the SKILL.md already promised; the channel was hard-coded to `internal`, so a partner cut was impossible. It now flows into `Spec.load` (name variant, clearance, contact) and into the per-KPI `channels` gate, which was also hard-coded to `internal` |
| `plugins/oracle-packs/skills/exec-summary/SKILL.md` | the build line now names `--fit-report` and the real flag set |
| `plugins/oracle-packs/requirements.txt` | **python-pptx and Pillow were missing** — the deck and exec-summary builders import both, so a fresh venv built from this file could not build a deck. Added with verified versions; re-verified by installing into a second, empty venv and rebuilding |
| `tools/sync-shared.sh` | `--check` reported permanent DRIFT: `sync` excludes `tests/`, `--check`'s `diff -rq` did not. Same exclusion on both sides |

## 2. Schema ↔ linter ↔ example ↔ fixtures

`source` now sits where the linter reads it, in all four places, and the schema states the rule in its Conventions line: `problem_solution.source`, `one_liner.source`, `icp.source`, and `meta.name_source` (the name lives inside `meta`, so its source cannot be a `name.source`).

| File | Change |
|---|---|
| `shared/schema/pack-spec.md` | `meta.name_source`, `one_liner.source`, `icp.source` added to the template; the Conventions paragraph names the four keys; the rules list restated |
| `examples/workforce-optimization/pack-spec.yaml` | `meta.name_source` added (artifact-sourced, not `user:` — see §10) |
| `plugins/oracle-packs/skills/one-pager/tests/fixture-pack-spec.yaml` | `meta.name_source`, `one_liner.source`, `icp.source` added |
| `plugins/oracle-packs/skills/deck/tests/fixture-pack-spec.yaml` | same three, plus `meta.name` corrected to Title Case so the channel variants derive from it (SPEC017) and caveats added to two figures (SPEC012) |
| `shared/tools/tests/fixtures/pack-spec.valid.yaml` | already carried all four |

**Oracle-only `oracle_products[]`, NVIDIA in the stack.** Stated in `shared/schema/pack-spec.md` as a comment above `oracle_products` and as a rule in its rules list, and asserted in `shared/tools/lint_spec.py`:

- `SPEC004` now also resolves `architecture.stack[].catalog_id` (single value or list) against the catalog;
- `SPEC018` (new) fails an `oracle_products[]` entry whose catalog `vendor` is not Oracle, naming the stack as its home;
- both are documented in `shared/tools/README.md`, and both are exercised by `run_tests.sh` (the test catalog gained an `nvidia-cuopt` entry; broken variant B now moves the engine into `oracle_products` and breaks a stack id).

**Two more linter corrections found while aligning:**

- `--strict` was doing two unrelated jobs, so a `draft` could never be clean under it. It is now the completeness check, and the new **`--signoff`** carries the "would this pass as confirmed?" rule (the four `user:<date>` sources). The rule still applies by itself once `meta.status` is `confirmed`/`built`, so nothing is weaker — `run_tests.sh` still proves SPEC003 fires on a confirmed spec without any flag.
- A KPI figure written `-` (the repo's written convention for "deliberately empty") was being treated as a real figure, demanding a `figure_status`, a `caveat` and an `attribution` for a metric that has no number. `-` is now read as absent, and a real `figure_status` beside a `-` figure is itself a finding. This answers an open question the worked example had filed against the schema; the enum did not need a fifth value.

## 3. Catalog reconciliation

Every invented id is gone; every id in the example and both fixtures resolves to `shared/data/oracle-products.yaml` (version 2026-09-18), and the linter proves it.

| Invented | Used instead | Where |
|---|---|---|
| `oci-compute-gpu` | `oci-dedicated-ai-cluster` | example, both fixtures |
| `oci-networking` | `oci-vcn` | example |
| `oracle-fusion-hcm` | `oracle-fusion-cloud-hcm` | example |
| `oracle-fusion-inventory-management` + `oracle-fusion-demand-management` | one `oracle-fusion-cloud-scm` entry (both are Fusion SCM modules) | example |
| `oci-analytics` | `oracle-analytics-cloud` | deck fixture |

No catalog entry was invented. Three change requests are filed in `shared/data/oracle-products.README.md` under a new **Catalog change requests** section, each naming the id the pack wanted, the substitution, and the question for the catalog owner (dedicated cluster vs GPU shapes; networking as a product vs a landing-zone bundle; whether the SCM modules should be split out). Each substitution also carries a `catalog_note` in the example spec, and `examples/workforce-optimization/README.md` now documents the reconciliation instead of the invented list.

## 4. Banned wording

The owner-rejected one-liner — "…packaged from proof of value to enterprise scale" — is gone from the example and from both fixtures, replaced by the site's own job-stating line (source: `plugins/oracle-packs-web/skills/listing/assets/exemplar-product-entry.js`, `oneLiner` / `shortLine`), with the catalog's vendor spelling and trimmed to the one-pager hero's 20-word budget:

> **full** — "Optimizes field-service work zones and schedules with NVIDIA cuOpt: a region's four-week plan, built in minutes and approved by dispatchers."
> **short** — "A region's four-week field plan, optimized in minutes and approved by dispatchers."

Three more "packaged" strings were found and removed on the way: two in the deck fixture's own copy (`anchor_line`, `exec_summary.goal`) and one hard-coded in `build_deck.py` ("infrastructure up to packaged service" on the solution-layers slide).

**The rule is now asserted on every channel.** `shared/references/naming-and-clearance.md` §4 states that packaging vocabulary inside the pack's one-liner is banned everywhere, internal included, because the one-liner is the one string every artifact inherits verbatim. `lint_artifact.py` implements it as **ART206**: it recognizes the spec's one-liner in an artifact (allowing for a wrap across up to three extracted lines), applies the ART203 packaging patterns to it whatever the channel, and says to fix it in the spec rather than in the artifact. Re-run after the change: clean on all five outputs. And proved the other way round — a scratch copy of the spec carrying the rejected line, with an artifact quoting it, reports exactly one ART206 on `internal`, `partner_print`, `customer_site` and `demo`.

## 5. Shared sync

`tools/sync-shared.sh` then `tools/sync-shared.sh --check` — **OK on both plugins**, after the `--check` exclusion fix in §1. Re-run at the end of the pass; both plugins carry the current `shared/`.

## 6. End to end on the worked example

Commands are in the final section. Every stage is green; this is what had to be fixed to get there.

**`lint_spec.py --strict`** — before: 12 findings (4 × SPEC003, 4 × SPEC002 missing `attribution`, 4 × SPEC011 on `figure_status: "-"`); after: **0 findings, 17 of 17 components complete**, with `meta.status: draft` untouched. Fixes: §2 (sources, the `-` convention), §3 (catalog ids).

**`build_feature_list.py`** — clean first time: 4 areas / 13 categories / 38 features, 20 ● / 2 ◐ / 16 ○.

**`build_deck.py --fit-report --channel partner_print`**

| Before | Fix |
|---|---|
| slide 8 failed outright: `AttributeError: 'str' object has no attribute 'get'` | `architecture.inputs/outputs` may be a mapping or a plain label; `build_deck.py` gained `arch_node()`/`arch_label()`, and the schema pins the `{system, data}` shape the fixtures already used. The example was rewritten to it |
| slide 5 footnote overflowed 2 lines → 4 | the footnote was printing the whole internal `divergence_from_pack` paragraph. Schema gained `meta.source_engagement.divergence_line` (one print-ready sentence); deck and exec-summary prefer it and fall back to the long form (where the fit report then reports the overflow honestly) |
| slide 5 headline read "**Proven** on real data at …" with no delivered result | `Spec.proof_word()` returns "Proven" only when a `delivered_result` figure exists, else "Proof of value" (naming-and-clearance §3). ART401 had caught this |
| slide 5 printed four `-` stat tiles | `Spec.figured_kpis()` — a `-` figure is not a figure. Same fix in the one-pager and the exec summary |
| slide 5 stat labels printed the KPI **formula** | label order is now `label` → `name` → `formula`; the example gained three short `label:` lines |
| slide 2 anchor strip printed raw ids: "Anchored to oracle-fusion-field-service, oci-dedicated-ai-cluster — packaged so any partner account exec can sell it." | `deckkit.product_name()` resolves an id through the catalog (naming-and-clearance §1: artifacts render the canonical name); the sentence lost its packaging vocabulary |
| slide 2 problem bullets rendered as Python dict reprs — `{'label': 'Suboptimal efficiency', 'text': '…'}` | `point_text()` renders a `{label, text}` entry as "Label: text"; the example's key was also renamed `sub_problems` → `problem_points`, the name the builders and both fixtures use |
| slide 6 drew a CONSUMPTION strip containing a dash | an empty container reading as content; the strip is omitted when the value is `-`, with a fit-log note |

After: **10 slides, 72 boxes, no overflow**, two notes (§10).

**`build_one_pager.py --channel partner_print`** (Chrome at the macOS default path) — before: **2 pages**, three blocks over budget; after: **1 page, 428 words against a 470 budget**. Fixes: the one-liner trimmed to the 20-word hero budget; `scope_sentence` → `scope_line` (the builder's key — the example's tier one-liners were being ignored and the first `what_you_get` bullet was rendering instead, a 99-px row); a short `one_pager.proof_story_anonymized` instead of the full `delivered` paragraph; display `name`/`summary`/`label` on the architecture layers so the data-flow block stops wrapping. Worth knowing: the page is **not** word-count-bound — the fixture fits 448 words on one page while the example overflowed at 393 (§10).

**`build_exec_summary.py --fit-report`** — clean: 41 boxes, no overflow, one note that the spec has no `exec_summary.next_steps` so the empty instance is drawn. Its "No next steps confirmed yet." placeholder tripped ART202 (a negation) and is now "To be confirmed with the pack owner."; the feature-list legend's "planned, not implemented yet" became "…not implemented today" (and `feature-list-anatomy.md` with it).

**`lint_artifact.py` on each output** — before: 12 findings across the five files; after: **0**, each on its own channel (feature list and executive summary are `internal`; deck and one-pager are `partner_print`). Four were linter defects, fixed in the tool:

- **ART104** demanded the "<name> App" form in every internal sentence. The App suffix is the executive-slide convention, not a second product name; internal now accepts the plain name, customer-facing channels are unchanged. Written into naming-and-clearance §2.
- **ART101** flagged the bare `cuOpt` inside the correct "NVIDIA cuOpt", because the catalog marks the bare form `not_this`. A `not_this` match that sits inside an accepted longer name is no longer a finding.
- **ART103** invented "Oracle Fusion Field **Planning**" in the PDF: `pdftotext -layout` puts two columns on one line, and the vendor-phrase regex crossed the line break into the next column. Cross-line joining is now text-format only; and in an extracted document a phrase that is a **prefix** of the canonical name is a rendered line break, not a misspelling.
- Prices written as HTML entities (`&euro;90K`) were invisible to every text check. `packlint.py` now unescapes entities in `.html/.htm/.js/.json/.md` (per line, so line numbers stay valid) and in `norm_loose`, which is what made the one-pager's price column checkable at all.

Two findings were real and fixed in the example: `Oracle Field Service` in a feature name (the catalog's `not_this`), and the architecture app layer labelled "Workforce Optimization app". Two more were real in the one-pager template and fixture (the template's comment named the pack; the fixture used the short vendor name seven times).

**`check_consistency.py <spec> <all five>`** — before: 6 findings; after: **0**, matrix all ✓ or – (absent). Three defects, all in the checker:

- a money-shaped **KPI figure** (`€190K / month`) was read as a tier price the spec had lost — CON005 owns figures, so CON004 now skips them;
- `~€300–500K` arrives from the extractor as `€300` because the regex stops at the dash — the range's `K` is now applied to the low end before comparing;
- the HTML one-liner compared unequal because of `&#x27;` — fixed by the entity unescaping above.

**Render QA.** `render_probe.sh --deck … --out …` reported the renderers, and its QuickLook recipe (one `<p:sldId/>` per temp copy, `docProps/thumbnail.*` deleted, ZIP_STORED) rendered all 10 slides; a Pillow contact sheet was assembled and read. Three things were visible only in the render and are fixed above: the dict-repr bullets on slide 2, the raw product ids on slide 2, and the dash-only CONSUMPTION strip on slide 6. Everything else reads correctly — tier names are `PoV Jumpstart / Integration / Scaling` with S/M/L only as size tags on the internal-style table, the proof strip says "Proof of value", geometry and colour semantics hold. What the render shows and the fit report cannot: **slide 4's two dashed screenshot slots** and the large empty band on slide 6 where the consumption strip used to be (§10).

## 7. Listing tools

- **`derive-stage-view.py`** on the example: the four areas needed a `stage`, so the example now carries the site's four stage names (`Load the period's data` · `Set the rules` · `Solve the plan` · `Review, approve, measure`, the same four `workflow.steps[]` walks). Result: **38 capabilities across 4 stages**, exit 0. The tool emitted them in spec order, which breaks its own documented invariant, so it now sorts groups into workflow order when a stage matches a step and says so in a note.
- **`check-grammar.js --help`**: prints its options, exit 0 (Node v26).
- **`denylist-to-json.py`** (new, `plugins/oracle-packs-web/skills/listing/tools/`): converts `shared/tools/denylist.txt` to the checker's JSON — plain and `~` entries become `customerNames`, `/` entries become `bannedStrings` with a reason. Run here: **21 names, 2 path fragments**, resolved from the plugin's synced `shared/` copy. It exists because the checker's customer-name gate **fails open**: with no deny-list configured it warns and still exits 0. Wired into `listing/SKILL.md` gate 4, `listing/assets/README.md`, and `references/preview-and-publish.md` (including its publish checklist).

## 8. Leak scan

A case-insensitive `grep -rniE` over the whole repo, alternating every customer name and mark in `shared/tools/denylist.txt` with the home-directory prefix and the cloud-drive name, now returns hits in **`shared/tools/denylist.txt` only** (and its two synced copies) — the pattern is deliberately not written out here, for the same reason the deny-list is the only file that carries those names. Fixed:

| File | Was | Now |
|---|---|---|
| `examples/…/pack-spec.yaml` | the customer named in `meta.source_engagement.customer` and in three KPI `attribution.named_when_allowed` lines | a placeholder plus the anonymized descriptor, with a comment saying a real spec carries the name and this repo does not |
| `examples/…/pack-spec.yaml` | 14 absolute machine paths in `provenance.inputs[].path` | three documented roots — `<practice-drive>`, `<owner-repo>`, `<owner-local>` |
| `shared/tools/regen_roadmap.py` | a hard-coded absolute path into one person's synced cloud-drive folder as the default source | `$ORACLE_PACKS_DIR`, with an explicit "no source path" error instead of a silent empty run |
| `shared/data/roadmap.README.md` | the same drive named twice | the practice's shared drive plus the variable |
| `shared/references/naming-and-clearance.md` | §3 enumerated thirteen customer names | one sentence pointing at the deny-list, which is the one place those names live |
| `shared/tools/packlint.py`, `shared/tools/README.md`, `denylist.txt` header | two engagements used as worked examples in docstrings | neutral placeholders |
| `plugins/oracle-packs/skills/spec/references/generalization-method.md` | the customer named twice (test T5, sources list) | "the workforce case" / "customer-specific" |
| `build/SKILL.md`, `one-pager/assets/README.md` | the drive named as the delivery convention | "the practice's shared drive" |

`claude.ai/artifact` — no hits. `ktram@` / `oracle@softserveinc.com` — now only in `naming-and-clearance.md` (which gained the **Contacts by channel** block, its documented home per DECISIONS), the example spec, the three fixtures, and one functional constant: `check-grammar.js` asserts that the site's shared contact **is** the practice mailbox. That assertion is the gate that keeps a personal mailbox off the site; it is kept deliberately. The schema template and `pack-anatomy.md` now point at the reference instead of repeating the addresses.

## 9. Plugin validation

| Target | Result |
|---|---|
| `claude plugin validate plugins/oracle-packs --strict` | ✔ passed |
| `claude plugin validate plugins/oracle-packs-web --strict` | ✔ passed |
| `claude plugin validate . --strict` (the marketplace) | ✔ passed |
| `claude plugin validate plugins/*/skills --strict` | ✔ passed (skills, agents, commands) |

Both manifests were missing `version`, which `--strict` treats as an error; both now carry `"version": "0.1.0"`. Every skill folder name equals its frontmatter `name` — `spec`, `build`, `feature-list`, `deck`, `one-pager`, `exec-summary`, `listing`, `demo`.

## 10. Still rough

From the builders' own notes, confirmed here, plus what this pass surfaced:

1. **Deck slide 4's two screenshot slots** are dashed empty containers labelled "Before: the manual artefact" / "After: the product screen". The fit report says so on every build. They are correct as empty instances, but a deck does not go to a seller with them — real before/after screens have to be dropped in.
2. **The packages table type-scales.** Slide 9 reports "table type scaled to 84% to fit the band" (80% on the fixture). It is inside the anatomy's allowance, but it is type shrinking to fit content, which the design rules otherwise forbid; a wider tier column or fewer capability rows is the real fix.
3. **`deckkit.py` is duplicated** in `skills/deck/tools/` and `skills/exec-summary/tools/`. Both copies are byte-identical today (this pass applied every edit to both and re-checked with `diff`), and the exec-summary loader already falls back to the deck skill's copy. The next edit that forgets one of them is a silent divergence: delete the duplicate, or add a `diff` assertion to `run_tests.sh`.
4. **The one-pager layout has no slack.** The page is height-bound, not word-bound: the fixture fits 448 words on one A4 and the example overflowed at 393. The word budgets are a good proxy but not the constraint, so "cut words" can fail to fix an overflow while a shorter architecture label fixes it. The builder is honest about it (it fails, names the longest blocks and writes the HTML anyway), but the guidance in `one-pager/SKILL.md` step 3 is about word budgets only.
5. **Chrome is spawned per run.** `build_one_pager.py` starts a headless Chrome for every build; the builders flagged that it can outlive the build. It did not linger in this pass — `pgrep -f "Google Chrome.*headless"` was empty after a dozen builds — but the risk is real on a killed or timed-out run, so check after a batch.
6. **Slide 6 has a large empty band** now that the CONSUMPTION strip is omitted when the spec has no target consumption. Correct — an absent container, not a dash — but the seller cards could grow into the space.
7. **The example stays `draft` and says why.** `lint_spec.py … --strict --signoff` prints exactly four SPEC003 lines: the four first-order components carry artifact sources, not `user:<date>`, because the pack owner has not walked the file through `/oracle-packs:spec`. That is the true state, not a defect.
8. **Two `not_this` vendor spellings remain in the example**, both inside `note:` fields that exist to explain the relabelling decision (`"…the site still writes 'Oracle Field Service'"`). Notes are never rendered into an artifact and every built artifact lints clean; if a builder ever prints a note, these become findings.

## 11. The two checks a human still has to do

1. **The 30-minute plugin spike** (`docs/PLAN.md` §7 step 7). Copy `plugins/oracle-packs/` into a test repository's `.claude/skills/oracle-packs/`, start a session at that repository's root, and confirm that (a) `/oracle-packs:spec` appears in the command list, and (b) `${CLAUDE_PLUGIN_ROOT}` resolves — the quickest proof is that the skill can read `${CLAUDE_PLUGIN_ROOT}/shared/data/oracle-products.yaml` and run `${CLAUDE_PLUGIN_ROOT}/shared/tools/lint_spec.py`. Everything in this report was run from the repo root with explicit paths, so the plugin-root indirection itself is **unproven**. Run `tools/sync-shared.sh` before copying.
2. **An interactive walk of `/oracle-packs:spec` on a real case.** The spec skill is the one skill with no executable surface: its intake questions, its research fan-out, its option triads and its component-by-component sign-off were read for consistency but never exercised. Only a real run shows whether the question list is answerable, whether the widget flow is bearable at twelve components, and whether the brief at the end is what the owner actually wants to confirm.

---

## Reproducing the end-to-end run

From the repo root, with `$W` any scratch directory:

```bash
python3 -m venv .venv && .venv/bin/pip install -r plugins/oracle-packs/requirements.txt
S=examples/workforce-optimization/pack-spec.yaml

.venv/bin/python shared/tools/lint_spec.py $S --strict                  # 0 findings, 17/17
.venv/bin/python shared/tools/lint_spec.py $S --strict --signoff        # the 4 sign-off gaps

.venv/bin/python plugins/oracle-packs/skills/feature-list/tools/build_feature_list.py $S --out $W
.venv/bin/python plugins/oracle-packs/skills/deck/tools/build_deck.py $S --out $W \
    --channel partner_print --fit-report
.venv/bin/python plugins/oracle-packs/skills/one-pager/tools/build_one_pager.py $S --out $W \
    --channel partner_print                                             # needs Chrome
.venv/bin/python plugins/oracle-packs/skills/exec-summary/tools/build_exec_summary.py $S \
    --out $W --fit-report

# each artifact on its own channel
.venv/bin/python shared/tools/lint_artifact.py $W/workforce-optimization-feature-list.docx \
    --channel internal --spec $S
.venv/bin/python shared/tools/lint_artifact.py $W/workforce-optimization-exec-summary.pptx \
    --channel internal --spec $S
.venv/bin/python shared/tools/lint_artifact.py $W/workforce-optimization-sales-deck.pptx \
    --channel partner_print --spec $S
.venv/bin/python shared/tools/lint_artifact.py $W/workforce-optimization-one-pager-partner_print.html \
    --channel partner_print --spec $S
.venv/bin/python shared/tools/lint_artifact.py $W/workforce-optimization-one-pager-partner_print.pdf \
    --channel partner_print --spec $S

.venv/bin/python shared/tools/check_consistency.py $S $W/*
PY=.venv/bin/python shared/tools/tests/run_tests.sh                     # 65 assertions

# listing tools
.venv/bin/python plugins/oracle-packs-web/skills/listing/tools/derive-stage-view.py $S \
    --no-prompt --out $W/stage-view.js
.venv/bin/python plugins/oracle-packs-web/skills/listing/tools/denylist-to-json.py --out $W/deny-list.json
node plugins/oracle-packs-web/skills/listing/tools/check-grammar.js --help

# release step, then the manifests
tools/sync-shared.sh && tools/sync-shared.sh --check
claude plugin validate plugins/oracle-packs --strict
claude plugin validate plugins/oracle-packs-web --strict
claude plugin validate . --strict
```

Slide QA: `bash plugins/oracle-packs/skills/deck/tools/render_probe.sh --deck $W/workforce-optimization-sales-deck.pptx --out $W/renders` and follow the recipe it prints for this machine.
