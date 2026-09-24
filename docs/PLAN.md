# Oracle Packaging Skills — build plan

_Written 2026-09-18 from the preparation research in `AO-Personal-OS/context/areas/softserve/docs/2026-09-17_packaging-skills-prep/` and Alex's decisions of 2026-09-18. Rewrite this page when the plan changes; never stack dated updates._

## 1. What the skills do

Turn one delivered Oracle + NVIDIA AI engagement into a repeatable **accelerator pack** and produce its standard artifact set from **one signed-off pack spec**:

| Order | Artifact | Skill | Plugin | Output |
|---|---|---|---|---|
| 0 | Pack spec (the spine) | `/oracle-packs:spec` | oracle-packs | `packs/<slug>/pack-spec.md` + research brief |
| 1 | Feature list | `/oracle-packs:feature-list` | oracle-packs | `.docx` (Area > Category > Feature, ● ◐ ○, customization scope) |
| 2 | Sales deck | `/oracle-packs:deck` | oracle-packs | `.pptx` on the SoftServe brand base, 10-slide anatomy |
| 3 | Sales one-pager | `/oracle-packs:one-pager` | oracle-packs | HTML → one A4 PDF, the WfO anatomy |
| 4 | Executive summary | `/oracle-packs:exec-summary` | oracle-packs | one slide in the host deck's style |
| 5 | Mini-site listing | `/oracle-packs-web:listing` | oracle-packs-web | a `products[]` entry for the practice site, checker-clean |
| 6 | Interactive demo | `/oracle-packs-web:demo` | oracle-packs-web | a guided walkthrough built from sources the user supplies |
| all | Build in order | `/oracle-packs:build` | oracle-packs | runs 1–4 (and hands off to 5–6) sequentially, pausing for review after each |

Demo video and Marketplace package/listing are part of a pack's end state but are **not built by the skills** (Alex, 2026-09-18).

## 2. The 12 shared components

Every artifact reads the same values from the spec. Order of sign-off in the spec skill is fixed by Alex: **problem ↔ solution → one-liner → target ICP → name**, then the rest in the order below.

| # | Component | Spec key | Notes |
|---|---|---|---|
| 1 | Problem ↔ solution | `problem_solution` | First thing confirmed; the reader's job, not our packaging |
| 2 | One-liner | `one_liner` | States the job and the outcome; never packaging vocabulary; full + rep-sayable short form |
| 3 | Target ICP | `icp` | One line: who, at what kind of company, with what pain |
| 4 | Name | `name` | One plain name; channel variants derived (site / internal "App" / external + subheading) |
| 5 | Verticals + vertical framings | `verticals[]` | Each vertical carries its own one-line problem ↔ solution and "what matters here" |
| 6 | Capabilities → features → customization | `capabilities[]` | Area > Category > Feature, status ● ◐ ○, customization scope per capability; four-axis specificity tag |
| 7 | Workflow architecture | `workflow.steps[]` | Inputs → processing steps with human-in-the-loop → outputs; failure path per step |
| 8 | High-level architecture | `architecture` | Data inputs → stack (infra / platform / app layers) → outputs; vendor ladder |
| 9 | Required Oracle products | `oracle_products[]` with `role: required` | From the shared catalog only |
| 10 | Optional Oracle products | `oracle_products[]` with `role: optional` | Same catalog; optional = could logically be a source or destination |
| 11 | Key performance metrics | `kpis[]` | Formula, baseline, cleared figure, attribution rule; **one metric set per pack** |
| 12 | Service packages table | `packages` | PoV Jumpstart / Integration / Scaling: per-capability handling, timeframe, cost; PoV 4–8 weeks, 10-week hard cap |

Cross-cutting keys: `meta` (slug, roadmap item id, source engagement, status), `clearance` (customer name/logo approval per channel, internal-only facts), `contacts` (per channel), `figures` (the single metric set and its attribution), `provenance` (source per fact), `open_questions`.

## 3. How `/oracle-packs:spec` runs (Alex's six requirements, 2026-09-18)

1. **Intake, interactive.** Ask the user to locate the raw inputs (folder or files: SoW, PoC deck, demo video, feature lists, transcripts, existing decks) and answer a predefined question list — each question is skipped when the context or the user already answered it. Questions go through the question widget.
2. **Generalization research** (the crucial step). Fan out: the domain's general workflow for this job across industries and how the delivered case differs; vendor / competitor capability taxonomies and the gap check; vertical differentiation with a "what matters here" cell per step; failure path per step; feature specificity on four axes (customer / engine / use case / industry); Oracle products from the catalog; roadmap placement; KPI candidates. Result: a very structured research TLDR with labeled claims and source tiers. General enough to sell across verticals, specific enough to be true.
3. **Options.** Propose one to three candidate triads (name · one-liner · problem ↔ solution) with a brief business-level TLDR and grounding; the user picks one or asks for further research.
4. **Component sign-off, one at a time**, in the fixed order: problem ↔ solution, one-liner, target ICP, name; then verticals, capabilities, workflow, architecture, Oracle products, KPIs, packages. Every proposal = short exec TLDR + grounding + widget. When something essential is missing, the skill asks instead of inventing.
5. **Brief confirmation.** Show the whole spec as a one-screen brief; the user makes last-minute changes; the skill states it is about to build, and which artifacts, in which order (sequential, review after each).
6. **Demo sources.** Before an interactive demo, the demo skill asks for sources: video, screenshots, written overview or a detailed brief.

## 4. Model split (roles, not model names in the shipped text)

- **Strongest model (Fable in Alex's setup):** research synthesis and the TLDRs, option generation, every component proposal, messaging decisions, the final editorial / fact-check pass on each artifact, red-team of a demo against the spec.
- **Mechanical model (Opus):** source extraction, research fan-out, catalog and roadmap lookups, file builds from the spec, render QA, checker and lint runs, captures, docs.

## 5. What ships in the bundle (from the shipping inventory)

`shared/` is the single source; `tools/sync-shared.sh` copies it into both plugins at release.

- **references/**: engagement context (≤ 2 pages) · naming and clearance · pack anatomy (the 12 components and the per-artifact map) · slide-design rules · client-document rules · research standards · review loop (how the owner reviews) · PoV rules.
- **data/**: `oracle-products.yaml` (the shared catalog with canonical names) · `roadmap-items.csv` with stable ids + pack crosswalk + regeneration script · pack tracker snapshot.
- **schema/**: `pack-spec.md` (the schema and template) · a worked example (`examples/workforce-optimization/`).
- **tools/**: artifact clearance linter (customer names, banned vocabulary, pricing rules, naming) · cross-artifact consistency check (every artifact against the spec) · render and fit probes.
- **plugin assets**: the 41 KB SoftServe deck base + brand tokens; the one-pager HTML template and PDF build; the listing schema slice, exemplar entry and relaxed checker; one reference demo, the extracted tour engine and the capture script.

Stays behind: machine-local rendering notes, personal skills and automations, credentials, pipeline and customer files, the personal wiki.

## 6. Rules the skills carry (overview; full text in `shared/references/`)

| Area | Rules |
|---|---|
| Messaging | Persona first; no counts, taxonomy or packaging vocabulary; one-liner states the job; a "why it sells for the partner's seller" block on sales artifacts; verticals as one concrete line each; generalize past the origin customer and say where the pack differs from the delivered scope |
| Truth and clearance | Never invent a tier, price or proof; "proven" only for delivered results; peer claims all-or-none; one metric set per pack, attribution by approval and channel; unconfirmed numbers footnoted; vendor names re-verified; no customer names, no "AIDP", no partner-tier claims externally; the linter runs on every artifact |
| Method | Sources inventoried first; table before layout; vendor-taxonomy gap check, vertical differentiation, then human adjudication; failure path per step; four-axis specificity test; contents before formatting; gaps are an approval gate; one structure for every pack; one-pager is the deck condensed |
| Design and QA | The slide rules; decks on the brand base; render-based per-slide QA; site heading budgets and visual grammar; demos lead with the value band, drill down to the rule behind each number, allow manual override, show the AI reasoning |
| Working with the owner | Options with a recommendation; corrections arrive as a screenshot plus a few words; renders not descriptions; expect a rebuild round; explicit open-items list; a fast path for one-block rebuilds |

## 7. Build sequence (this repo)

1. Scaffold, schema, plan — done 2026-09-18.
2. Shared data and references: Oracle product catalog · roadmap extract · engagement context · naming and clearance · generalization method (from the sessions and the Vlad coaching) · review loop.
3. Spec skill (the spine) with its question list, research fan-out spec, options format, sign-off flow, brief.
4. Document skills: feature list, deck, one-pager, exec summary, build orchestrator; builders from the spec; WfO worked example regenerated end to end as the acceptance test.
5. Web skills: listing (schema slice, exemplar, checker) and demo (playbook, tour engine, sources intake).
6. Linter and consistency checker wired into every skill's definition of done.
7. Plugin validation, the 30-minute plugin spike, README and install guide, pilot copy for Vlad.
