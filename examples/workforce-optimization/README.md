# Worked example — Workforce Optimization

`pack-spec.yaml` in this folder is the reference fill of `shared/schema/pack-spec.md`: the Workforce Optimization (WfO) pack, reconstructed from its **delivered** artifacts with the 2026-09-18 decisions applied on top.

It exists for three jobs:

1. **A reading model for `/oracle-packs:spec`** — what a complete, evidence-bound spec looks like, including how absences and disagreements are recorded rather than smoothed over.
2. **The acceptance fixture for the builder skills** — regenerating the five delivered WfO artifacts from this file, and matching them, is the end-to-end test in `docs/PLAN.md` §7 step 4.
3. **A worked example of `shared/references/pack-anatomy.md`** — every component in that reference has its filled counterpart here.

## Status

`meta.status: draft`, and it stays draft. The example **reproduces the delivered artifacts; it has not been signed off by the pack owner.** The schema requires a `user:<date>` source on the four first-order components (`problem_solution.source`, `one_liner.source`, `icp.source`, `meta.name_source`) before `status: confirmed`; here they carry artifact sources instead. Sign-off happens by walking the file through `/oracle-packs:spec`, not by editing the field.

That is what the two linter flags separate. `lint_spec.py <this file> --strict` is **clean**: every component the spec carries is complete. `lint_spec.py <this file> --strict --signoff` prints exactly four SPEC003 lines — the four first-order sources that are not `user:<date>` — which is the accurate statement of what is missing before this becomes a confirmed spec.

Sixteen items are listed in `open_questions`. The ones that block a confirmed status:

- **Customer name on partner-print artifacts.** `clearance.customer_name_allowed.partner_print` is `false`, but the delivered one-pager, deck, executive summary and section deck all print the customer's name and logo. Approval is pending with Alex. Until it lands, builders emit the anonymized descriptor ("a global home-appliance manufacturer") and the delivered artifacts are out of compliance with their own spec.
- **Two figure sets for one pack.** The print artifacts carry `~30 min` / `up to +26%` / `€190K per month`; the mini-site carries a different, anonymized, modeled set (`+4.5%` median jobs per technician per day, `~5x` three-year return, 83% of 12 simulations positive). The 2026-09-18 decision is one metric set per pack, so one of the two goes. This file carries the one-pager set, as decided.
- **Scaling-tier pricing** is `tbd` on every source artifact, services and infrastructure both.

## Decisions applied on top of the delivered artifacts

| Delivered artifacts say | This spec says | Why |
|---|---|---|
| `PoV · S` / `Roll-out · M` / `Scaling · L` on print; `Jumpstart Proof-of-Value` / `Integration` / `Scale` on the site | **`PoV Jumpstart` / `Integration` / `Scaling`**, `S / M / L` as size tags only | One tier vocabulary everywhere (2026-09-18) |
| PoV timeline "2 months" on print, "4–8 weeks" on the site | **6–8 weeks target, max 8, hard cap 10** | One duration, asserted by the linter |
| PoV infrastructure price: five different values across the estate | **`~€2K / month`, indicative** | The Jul-17 one-pager is canonical |
| Feature status as two colours of the same `●` | **`● available` / `◐ partial` / `○ roadmap`** | Three distinct glyphs; colour is not a data channel |
| "Oracle Field Service" on the deck, feature list and site; "Oracle **Fusion** Field Service" on the Jul-17 one-pager | **`oracle-fusion-field-service`** | The catalog's canonical vendor name |
| Integration claims with no tier attached (the one-pager makes Field Service the native centre; the feature list marks the same integration `○ roadmap`) | **Every integration claim states its tier** — PoV file export/import, Integration API write-back, Scaling API plus telemetry | Both were true at different tiers and neither said so |

## Oracle product ids — reconciled against `shared/data/oracle-products.yaml` (version 2026-09-18)

Every id in this spec now resolves to the catalog, and `shared/tools/lint_spec.py` asserts it (SPEC004). Four of the ids this example first coined had no catalog entry; each was replaced by the closest catalogued product and filed under *Catalog change requests* in `shared/data/oracle-products.README.md`. **The catalog is authoritative: if it later gains or renames an entry, this file changes, not the catalog.**

| id in the spec | Product it stands for | Role | Grounding | Reconciliation |
|---|---|---|---|---|
| `oracle-fusion-field-service` | Oracle Fusion Field Service | required | Named on the Jul-17 one-pager | as coined |
| `oci-dedicated-ai-cluster` | OCI dedicated AI cluster (4–8 NVIDIA A100) | required | One-pager architecture, deck slide 7 | was `oci-compute-gpu`; `oci-gpu-instances` is the alternative when a pack sizes raw shapes |
| `oci-object-storage` | OCI Object Storage | required | Mini-site `technology.stack` | as coined |
| `oci-vcn` | OCI Virtual Cloud Network | required | Mini-site `technology.stack` ("Object storage, networking and IAM") | was `oci-networking` |
| `oci-iam` | OCI Identity and Access Management | required | Same line as above | as coined |
| `oci-kubernetes-engine` | OKE / containers | required | Delivered PoC technical scope only; on no published diagram | as coined |
| `oracle-autonomous-ai-database` | Oracle Database 26ai (persistence) | required | Delivered PoC technical scope only; on no published diagram | as coined |
| `oracle-fusion-cloud-hcm` | HR/WFM source for people availability | optional | **Inferred** from the pack's "up to five integrations" list | was `oracle-fusion-hcm` |
| `oracle-fusion-cloud-scm` | Spare-parts inventory **and** demand-forecast source | optional | **Inferred**, same list | was two ids, `oracle-fusion-inventory-management` and `oracle-fusion-demand-management`; both are Fusion SCM modules, so the entries merged |
| `oracle-analytics-cloud` | BI destination for KPIs per plan version | optional | **Inferred**, same list | as coined; the catalog carries it `verified: false` (Oracle's page leads with "Oracle Analytics") |

One more id sits outside `oracle_products`, in `architecture.stack[].catalog_id`:

| id | Product | Note |
|---|---|---|
| `nvidia-cuopt` | NVIDIA cuOpt, the GPU-accelerated solver | **Not an Oracle product**, and that is now a schema rule: `oracle_products[]` is Oracle-vendor only and the catalog's NVIDIA entries belong in the architecture ladder. The linter enforces both halves — SPEC018 when an NVIDIA id appears in `oracle_products[]`, SPEC004 when a `catalog_id` does not resolve. |

Two notes for the catalog owner:

- The `optional` entries have **no reference anywhere in the delivered estate** — no WfO artifact and no sibling pack's artifact lists optional Oracle products as such. They are inferred from the pack's own named integration list (booking, inventory, HR/WFM, demand forecasting, BI) mapped onto the Oracle products that would serve each. The booking system has no Oracle counterpart and stays customer-specific.
- `oci-kubernetes-engine` and `oracle-autonomous-ai-database` come from the delivered PoC's technical scope and appear on **no published architecture diagram**. They are recorded as required with that caveat in their `note`, not quietly promoted.

## Where the schema did not fit the source

Recorded in `open_questions`, flagged here because they are schema questions, not pack questions. The second one is now settled:

1. **Feature-level `status` and `customization_scope` have no source at that granularity.** The delivered feature list merges `Current status` down per **category** and `Standard customization scope` down per **area**. So `status` on each feature inherits its category's cell (with a `note` on the category saying so), and feature-level `customization_scope` is left unset — only `customization_scope_area` is filled.
2. **Settled: a KPI with no cleared headline figure writes `figure: "-"`.** The enum (`pov_result | delivered_result | target | modeled`) did not need a fifth value — `-` already means "deliberately empty" everywhere in a spec, and `shared/tools/lint_spec.py` now reads a `-` figure as absent: no `figure_status`, `caveat` or `attribution` is demanded for it, and a real `figure_status` beside a `-` figure is itself a finding. Four of the seven WfO KPIs sit in that state, keeping their formula, baseline and caveat.

Separately: `figure_status` for the `€190K / month` figure is set to `modeled`, not `pov_result`, because the one-pager itself types it as "estimated savings at full launch" rather than a measured proof-of-value outcome. The other two headline figures are `pov_result`.

## Sources

`provenance.inputs` carries the full list with paths, read dates and which components each one supplies. The short version:

- **Read directly in this pass**: the Jul-17 sales one-pager PDF (on the practice's shared drive), the Sep-10 feature-list `.docx` (glyph colours read out of `word/document.xml`), the mini-site listing entry in `content.js`, and the 2026-09-16 WfO pack-spec distillation.
- **Read second-hand** through `B-artifact-component-map.md` and `A1-sessions-decks-onepagers.md`: the sales deck, the executive summary, the September section deck, the demo `data.js`, and the June/July call notes.

`provenance.research_brief` points at a brief that was never written — this example was reconstructed from delivered artifacts rather than produced by the spec skill's research pass.
