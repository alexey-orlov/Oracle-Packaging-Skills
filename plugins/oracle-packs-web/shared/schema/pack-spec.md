# Pack spec — schema and template

One YAML file per pack, at `packs/<slug>/pack-spec.yaml` in the working folder the user chooses. It is the single source of truth: every artifact skill reads its values from here and never re-derives them. Values are confirmed by the user through `/oracle-packs:spec`; a build skill that finds a required key missing stops and sends the user back to the spec skill instead of filling the gap itself.

Conventions: every fact carries a `source` (file, call, URL, or `user:<date>` for something the user typed) so the linter can trace it. The four first-order components carry theirs on a fixed key — `problem_solution.source`, `one_liner.source`, `icp.source` and, because the name lives inside `meta`, `meta.name_source` — and the linter reads exactly those. Money in EUR as written on the source artifact. Durations in weeks. `status` values are the ones listed; free text goes in `note`.

```yaml
meta:
  slug: workforce-optimization            # stable id; used for folder, listing slug, file names
  name: Workforce Optimization            # component 4 — one plain name
  name_source: user:2026-09-18            # component 4's source lives here, not inside a `name:` mapping
  name_variants:                          # derived by the spec skill; rule from Alex 2026-09-18
    site: Workforce Optimization
    internal_slide: Workforce Optimization App
    external: Workforce optimization      # one-pager, deck; optional subheading below
    external_subheading: Accelerator App by SoftServe
  roadmap_item_id: workforce-optimization # from shared/data/roadmap-items.csv; never the row number
  roadmap_block: Data analysis & optimization   # label only; blocks are renamed often
  source_engagement:
    customer: "<the delivery customer's name>"   # internal-only unless clearance.customer_name_allowed says otherwise
    delivered: PoC, Jun 2026, cuOpt-based zone/technician allocation on Oracle Fusion Field Service data
    divergence_from_pack: "The pack generalizes the allocation rules; the delivered PoC hard-codes the customer's."
    divergence_line: "The pack generalizes the rules the proof of value hard-coded."   # ONE print-ready sentence
    context: "{Customer}'s dispatchers plan the field force by hand …"   # optional; the proof slide's CONTEXT block
    # `context`, `delivered`, `deck.proof_headline` and `deck.vertical_case` may carry `{customer}` /
    # `{Customer}`: the deck fills it with what the channel may call the customer (the name where
    # clearance.customer_name_allowed is true, clearance.anonymized_descriptor elsewhere).
    # divergence_from_pack is the internal statement and may run to a paragraph; `divergence_line` is what
    # a deck or executive-summary footnote prints. Without the short line the builders fall back to the long
    # one and the fit report reports the overflow, which is the honest failure, not a silent truncation.
  status: draft | research | options | signing-off | confirmed | built
  spec_version: 1
  generated_with: { roadmap_version: 2026-09-17, catalog_version: 2026-09-18 }

clearance:
  customer_name_allowed:                  # per channel; default false
    internal: true
    partner_print: false                  # one-pager, deck for Oracle sellers
    customer_site: false
    demo: false
  anonymized_descriptor: a global home-appliance manufacturer
  internal_only_facts: [contract value, named customer accounts, headcount, POD counts]
  approvals: []                           # who approved what, when

problem_solution:                         # component 1
  problem: "Dispatchers plan technician work zones by hand ..."
  solution: "The app re-optimizes zones and daily plans on the customer's own data ..."
  reframe: "Review the plan, don't build it"   # the job reframe used as a headline
  source: user:2026-09-18

one_liner:                                # component 2
  full: "..."                             # states the job and the outcome; never packaging vocabulary
  short: "..."                            # rep-sayable in one breath
  banned_words_checked: true
  source: user:2026-09-18

icp:                                      # component 3
  line: "Field-service operations leaders at companies running Oracle Fusion Field Service with 200+ technicians"
  buyer_roles: [VP Field Service, COO]
  qualifying_signals: [...]
  disqualifiers: [...]
  source: user:2026-09-18

verticals:                                # component 5
  # `icon:` is written by /oracle-packs:visuals when the user picks one — { file, file_white, name, source, licence }, paths relative to the pack folder; absent means the deck draws an empty container
  - name: Industrial equipment service
    framing: { problem: "...", solution: "..." }
    what_matters_here: "..."
    worked_example: "..."
    status: proven | plausible | roadmap

capabilities:                             # component 6 — Area > Category > Feature
  - area: Allocation rules
    categories:
      - name: Availability
        features:
          - name: Technician availability & skills constraints
            status: available | partial | roadmap        # ● ◐ ○
            customization_scope: "Rule weights and constraint set per customer"
            specificity: [customer, engine, use_case, industry]   # four-axis tag; empty = generic
            tier_first_available: pov | integration | scaling
            note: "file export / import at PoV; API write-back is Integration"  # → a footnote on the feature list
            source: ...
    customization_scope_area: "..."       # per-capability handling summary used in the packages table

workflow:                                 # component 7 — 5-7 steps (hard cap 7, min 3), grouped at the buyer's checkpoints; mechanics live inside a step's description, never as steps
  inputs: [ { system: Oracle Fusion Field Service, data: work orders, technicians, zones } ]
  steps:
    - n: 1
      name: Ingest and validate demand
      actor: system | human | ai
      human_in_the_loop: false
      failure_path: "Missing fields → row flagged, not dropped; dispatcher resolves"
      vertical_differences: { "Industrial equipment service": "...", "Medical devices": "..." }
  outputs: [ { system: Oracle Fusion Field Service, data: optimized plan written back } ]

architecture:                             # component 8
  inputs:                                 # same shape as workflow.inputs: a system and what it carries
    - { system: Oracle Fusion Field Service, data: "technicians, availability, bookings" }
  stack:
    - layer: Custom configuration        # vendor ladder, top to bottom
      vendor: SoftServe
      items: [...]
    - layer: Accelerator business app
      vendor: Oracle + SoftServe
    - layer: Optimization engine
      vendor: NVIDIA
      items: [NVIDIA cuOpt]
      catalog_id: nvidia-cuopt            # every NVIDIA component of the stack is named here, by catalog id
    - layer: Infrastructure
      vendor: Oracle
      items: [OCI Compute, OCI Object Storage]
      catalog_id: [oci-dedicated-ai-cluster, oci-object-storage]  # one id or a list; the platform's services are named here, the platform itself once in oracle_products (`oci`)
  outputs:
    - { system: Oracle Fusion Field Service, data: "the approved plan, written back" }

# `oracle_products[]` holds ORACLE-VENDOR entries only — the products an Oracle seller can put on a
# deal. NVIDIA components (cuOpt, NeMo, NIM, AI-Q, VSS, NVIDIA AI Enterprise) are in the catalog too,
# but they belong in `architecture.stack[].catalog_id`, never in this list: a required/optional
# roll-up across packs is an Oracle-consumption question. Both places take catalog ids only, and the
# linter resolves both against shared/data/oracle-products.yaml.
oracle_products:                          # components 9 and 10 — ids from shared/data/oracle-products.yaml only; required = only what the pack cannot run without (typically 1-3: the platform as one entry + what the core executes on); optional = only what a buyer would plausibly connect (2-4); never a catalog sweep
  - id: oci-dedicated-ai-cluster
    role: required                        # required = built on it or fully relies on it
    why: "Runs the optimization engine"
  - id: oracle-fusion-field-service       # the catalog's canonical name; "Oracle Field Service" is a `not_this`
    role: required
    why: "Source of work orders and destination of the plan"
    integration: { pov: "file export / import", integration: "API write-back", scaling: "API + telemetry" }
  - id: oci-object-storage
    role: optional                        # optional = could logically be a source or destination
    why: "Landing zone for demand forecasts"

# A metric that is defined and measured per engagement but carries no cleared headline number is
# written `figure: "-"`, and then carries no figure_status, caveat or attribution — there is nothing
# to qualify. Artifacts print "results to follow" for it.
kpis:                                     # component 11 — ONE metric set per pack
  - name: Planning cycle time
    formula: "Time from demand freeze to approved plan"
    baseline: "~2 days manual"
    figure: "~30 min"
    figure_status: pov_result | delivered_result | target | modeled
    attribution: { named_when_allowed: "Proof of value · <the customer>", otherwise: "proof of value at a global home-appliance manufacturer" }
    caveat: "Illustrative PoV result, not contractual"
    source: ...

packages:                                 # component 12 — PoV Jumpstart / Integration / Scaling
  tiers:
    - id: pov
      name: PoV Jumpstart
      size_tag: S
      duration_weeks: { target: 6, min: 4, max: 8, hard_cap: 10 }   # skill pushes back above 10 with reasons
      services_price: { value: 90000, currency: EUR, status: confirmed | indicative | tbd, footnote: "..." }
      infra_price_monthly: { value: 2000, currency: EUR, status: indicative }
      what_you_get: [...]
      scope_in: [...]
      scope_out: [...]
    - id: integration
      name: Integration
      size_tag: M
      duration_weeks: { min: 12, max: 20 }
      services_price: { range: [300000, 500000], currency: EUR, status: indicative }
    - id: scaling
      name: Scaling
      size_tag: L
      duration_weeks: { min: 12, max: 52 }
      services_price: { status: tbd }
  capability_handling:                    # per capability area × tier, the ◐ ● ●● cells
    - area: Allocation rules
      pov: "Standard rule set on customer data"
      integration: "Customer rules and weights"
      scaling: "Per-market rules, custom KPIs"
  why_it_sells_for_the_partner:           # the seller block on partner-facing artifacts
    - "A natural Oracle Field Service cross-sell"
    - "Net-new OCI GPU consumption on top of the SaaS seat"
    - "Repeatable across similar accounts"
  target_oci_consumption: "..."           # optional; per tier when known
  value_for_partner: "..."                # optional; the proof slide's VALUE FOR ORACLE + NVIDIA block (falls back to anchor_line)
  value_for_client: "..."                 # optional; the proof slide's VALUE FOR CLIENT block (falls back to problem_solution.solution)

deck:
  images:                                 # written by /oracle-packs:visuals; each is { file, source, creator, licence, source_url }, file relative to the pack folder. A slot absent = the deck draws an empty container, never a stand-in
    today: { file: visuals/today-A-....jpg, source: Pexels, creator: <photographer>, licence: Pexels License, source_url: <the page> }
    tomorrow: { file: visuals/tomorrow-B-....jpg, source: Openverse / rawpixel, creator: <creator>, licence: CC0 1.0, source_url: <the page> }

contacts:                                 # the three addresses: naming-and-clearance.md §3, "Contacts by channel"
  partner_print: { name: <alliances contact>, title: <their title>, email: <the alliances address> }
  site: { mailbox: <the practice mailbox>, named: <alliances contact> }
  internal: { name: <the person doing the packaging>, email: <the R&D request mailbox> }

provenance:
  inputs: [ { path: ..., kind: sow | deck | video | transcript | feature-list | call-note, read: 2026-09-18 } ]
  research_brief: packs/<slug>/research-brief.md

open_questions:
  - "..."                                 # anything the user deferred; artifacts print nothing that depends on an open question
```

## Rules the schema enforces (checked by `shared/tools/lint_spec.py`)

- Every component key present and confirmed before `status: confirmed`; the four first-order components carry a `user:<date>` source on `problem_solution.source`, `one_liner.source`, `icp.source` and `meta.name_source`.
- `oracle_products[].id` and every `architecture.stack[].catalog_id` must exist in the catalog; a product missing from the catalog is a catalog change request, not a free-text entry.
- `oracle_products[]` is Oracle-vendor only. A catalog entry whose `vendor` is NVIDIA belongs in `architecture.stack[].catalog_id`.
- `packages.tiers[pov].duration_weeks.max` ≤ 8 by default; anything above 8 needs a `justification`; above 10 is rejected.
- `kpis` is one set; the same metric may not appear twice with different figures. A figure of `-` means "measured per engagement, no cleared number" and is read as absent.
- `clearance.customer_name_allowed` decides attribution per channel; the builders never read the customer name unless the channel allows it.
- No customer name inside `one_liner`, `problem_solution`, `verticals`, or `name`.
```
