# Pack anatomy — the 12 components and where each one appears

_The reference every artifact skill reads before it builds. The 12 components live in `packs/<slug>/pack-spec.yaml` (schema: `shared/schema/pack-spec.md`); this page says what each component is, what "good" looks like, and the **form** it takes in each of the six artifacts. Rewrite this page when the anatomy changes; never stack dated updates._

_Worked reference: the Workforce Optimization (WfO) pack, whose delivered estate is mapped artifact by artifact in the preparation research. The WfO pack's delivered case is a global home-appliance manufacturer's PoC; the customer's name is an internal-only fact and appears in no artifact unless `clearance.customer_name_allowed` says so for that channel. Every canonical wording quoted below is from a delivered WfO artifact._

---

## 0. How to read this page

Three rules bind every skill that builds from a spec:

1. **The spec is the only source.** A builder that finds a required component missing stops and sends the user back to `/oracle-packs:spec`. It never re-derives a value from the source engagement, and never invents one to fill a slot.
2. **A component's *content* is one decision; its *form* is per-artifact.** The same problem statement is three dashed bullets on the one-pager, two cards on deck slide 2, and a `problemSolution` object on the listing. The words are the same words.
3. **"Not shown by design" is a legitimate cell.** An absent component is an absence the anatomy already decided, not a gap to be filled. §2's matrix says which is which.

---

## 1. The twelve components

**Sign-off order is fixed** (Alex, 2026-09-18). The four first-order components settle what the pack *is*, in this order, before anything else is proposed:

> **problem ↔ solution → one-liner → target ICP → name**

then the eight that describe it:

> **verticals → capabilities → workflow → architecture → Oracle products → KPIs → packages**

The order is load-bearing. The name is chosen *last of the four* because a name proposed before the job is settled gets defended instead of tested; the packages table is settled *last of all* because price and promise are one decision, and the promise is the capability set.

---

### 1 · Problem ↔ solution

**Definition.** The reader's job, stated as the pain they already have, paired with the reframe that removes it. Two blocks, one sentence each at the top altitude, plus two to four named sub-problems. The solution block leads with a **reframe of the job**, not with the technology.

**Good.** The WfO problem: *"Field-service operators plan their mobile workforce by hand: work zones, technician assignments, dozens of rules and constraints."* Then three named sub-problems, each a label plus one clause: *"Suboptimal efficiency: uneven workloads and under-used capacity" · "Lower customer satisfaction: longer wait times from suboptimal allocations" · "Poor scalability: planning hinges on scarce senior dispatchers; new zones launch slowly."* The solution heading is the reframe — *"THE SOLUTION: REVIEW THE PLAN, NOT BUILD IT"* — followed by the mechanism in two sentences and three outcome chips (`Productivity ↑` · `Capacity utilization ↑` · `Customer wait time ↓`). Note what the good version does: the problem is the reader's daily routine, not a market trend, and the solution names who does what afterwards (dispatchers review) rather than what the software contains.

**Anti-patterns.** Opening on the vendor or the engine ("cuOpt is a GPU-accelerated solver that…"). A problem no named role owns ("data silos", "lack of visibility"). Sub-problems that restate the headline in different words. A solution block that is a feature list with verbs. Stating the problem in the packaging's vocabulary ("customers lack a packaged accelerator").

---

### 2 · One-liner

**Definition.** One sentence that states the job and the outcome, in the reader's words, carried in two lengths: a **full** form for print and hero copy, and a **short** form a partner rep can say in one breath on a call.

**Good.** Full (WfO one-pager hero): *"Intelligent field-service planning with NVIDIA cuOpt on Oracle OCI: packaged from proof of value to enterprise scale."* Short (listing `shortLine`): *"A region's four-week field plan, optimized in minutes and approved by dispatchers."* The short form is the better model of the rule: it names the unit of work (a region's four-week plan), the outcome (minutes), and who stays in charge (dispatchers).

**Anti-patterns.** Packaging vocabulary in the one-liner — "accelerator pack", "ready-to-run", "packaged", "pods", "evaluation-first" are internal words and never reach a reader. Counts and taxonomy ("seven capabilities across four areas"). A one-liner scoped to the *artifact* instead of the *product* (the WfO deck's cover line, "AI accelerator service packages on Oracle OCI + NVIDIA cuOpt", describes the deck). Three different one-liners at three lengths that are not derivations of each other.

---

### 3 · Target ICP

**Definition.** One line naming who buys, at what kind of company, with what pain — written from the **customer's** side, not the seller's. Supported by buyer roles, qualifying signals and disqualifiers, which stay in the spec and reach only internal artifacts.

**Good.** *"Any mobile field force planned against skills, availability and geography."* (WfO listing `industriesNote`.) The best template in the estate comes from a sibling pack: *"Where it applies. Any business that needs to turn market and customer developments into pursuable opportunities across its account base, quickly."* Both name a **shape of operation**, not an industry list and not a product prerequisite.

**Anti-patterns.** Confusing customer ICP with **seller** ICP. The WfO one-pager files its nearest ICP line under "Why it sells" as *"Repeatable: fits any OFS customer with a heavy, centralized dispatch and scheduling routine"* — true, useful, and the wrong component: it gates the ICP on owning a specific Oracle product, which is a partner-value statement. Also: an ICP that is four industry nouns (that is component 5), and an ICP stated as a headcount threshold with no source.

---

### 4 · Name

**Definition.** One plain name, owner-set, from which the channel variants are derived by rule — never re-invented per artifact.

**Good.** The rule (Alex, 2026-09-18): mini-site `Workforce Optimization` · internal exec slide `Workforce Optimization App` · external one-pager and sales deck `Workforce optimization`, with a small `Accelerator App by SoftServe` subheading where one is needed. The spec carries all four in `meta.name_variants`; a builder reads its channel's variant and nothing else.

**Anti-patterns.** A name that drifts between artifacts ("Workforce Optimization Accelerator Pack" on one feature list, "Workforce Optimization App by SoftServe" on its successor). A name built on a vendor trademark without a usage-guidelines check. Casing decided per artifact. Internal acronyms in anything a partner reads.

---

### 5 · Verticals + vertical framings

**Definition.** Three to five verticals, each carrying its **own** one-line problem ↔ solution pair and a "what matters here" sentence — what the work actually looks like in that industry. A chip row of industry nouns is the degenerate form, acceptable only where the page has no room.

**Good.** The WfO listing is the only artifact in the estate that does this properly, with a full pair per vertical. Telecom, for example: problem *"Install-and-repair technicians have to be routed to tight appointment windows across regions, matched to line skills. Missed windows cost customer satisfaction directly…"*; solution *"Appointment windows and line skills are modeled as commitment and skill rules, and the solver routes against them while minimizing travel. Launching a new zone comes down to a configuration change."* Deck slide 3 gives the compressed form, one concrete line per vertical: *"Utilities — water · gas · electric. Schedule field crews across service territories against SLAs, outage spikes and crew certifications, balancing planned and emergency work."*

**Anti-patterns.** A vertical row that is the same sentence with the industry noun swapped. Vertical *labels* that differ between artifacts (see §5). Claiming a vertical as proven when only one has a delivered case — each vertical carries `status: proven | plausible | roadmap`, and only the delivered one is proven.

---

### 6 · Capabilities → features → customization

**Definition.** The master capability tree, **Area > Category > Feature**, with a status glyph per row (`●` available · `◐` partial · `○` roadmap) and a **standard customization scope** per area. This is the pack's single feature truth; every other capability rendering in every other artifact is derived from it.

**Good.** The WfO feature list: 4 areas (Allocation rules · Review and approval workflow · KPIs and analytics · Integrations) → 13 categories → 38 features, with status merged down per category and customization scope merged down per area. The customization text is what makes the table sellable rather than a spec dump — *"Balancing optimization function with penalty / rewards, allocation rules weights tuning to achieve optimal allocation per customer"* tells a buyer exactly what the engagement configures for them.

**Derivation rule.** The mini-site's stage view (`technology.capabilities[]{stage, items[]}`) is **derived from this tree per pack** by mapping every feature to a workflow stage (component 7). The mapping is owned by the spec, not re-invented by the listing skill, and the derived view may drop features but may never add one.

**Anti-patterns.** Two glyph systems in one estate (the delivered WfO feature list distinguishes "available" from "partial" by the **colour** of the same `●`, which is invisible in plain text, in print and to anyone reading a converted copy — the pack standard is `● ◐ ○`, three distinct glyphs). Features that are "theoretically also possible". A feature list with pricing on it. A status claimed at feature granularity when the source only supports it per category.

---

### 7 · Workflow architecture

**Definition.** Inputs → processing steps → outputs, with **human-in-the-loop marked per step** and a **failure path per step**. This is the product's behaviour, and it is the axis the mini-site and the interactive demo are both organized around.

**Good.** WfO: `Load the period's data` → `Set the rules` → `Solve the plan` → `Review, approve, measure`, four steps, each carrying the subset of features it exercises. The HITL detail is the point: the dispatcher compares the current and the optimized plan on a live map, approves or rejects **per zone** with an optional comment, re-runs, and nothing is exported until approval. The demo realizes the same four steps as five processing stages with a validation gate in front.

**Anti-patterns.** A happy-path-only flow — every step needs its failure path ("missing fields → the row is flagged, not dropped; the dispatcher resolves it"), because the failure path is what a buyer's operations lead actually asks about. Steps named after system components rather than the work. Heavy AI work hidden behind a progress bar, which reads as ETL.

---

### 8 · High-level architecture

**Definition.** Data inputs → the stack → outputs, with the **vendor ladder** explicit: which layer is the partner's, which is the engine vendor's, which is ours. Distinct from component 7: this is what it is built on, not what it does.

**Good.** WfO, compact form (one-pager): a three-column diagram, source system on the left, the OCI box on the right containing the app and the solver, two labelled pipes between them — *"technicians data, default allocations"* outbound, *"optimized allocations: zones, visits"* inbound. Detailed form (deck slide 7): the same, plus an "Additional datasources" box and the named GPU cluster. The ladder, top to bottom: **Custom configuration** (SoftServe) → **Accelerator business app** (Oracle + SoftServe) → **Optimization engine** (NVIDIA) → **Infrastructure** (Oracle).

**Anti-patterns.** A new diagram invented for each artifact when one already exists — reuse the deck's. Layers that differ by tint alone on a partner-facing stack (they must differ in weight and shape, with the partner layer on top and real logo images, not text). Conflating the ladder with the architecture: the ladder is an attribution device, the architecture is a data flow.

---

### 9 · Required Oracle products

**Definition.** The Oracle products the pack is **built on or fully relies on**, by `id` from `shared/data/oracle-products.yaml` only, each with a one-line `why`. Where a product is an integration point, the entry states **what happens at each tier** — this is the rule that stops the estate contradicting itself.

**Good.** WfO: Oracle Fusion Field Service as source *and* destination · OCI Object Storage for the period's data · an OCI dedicated AI cluster (4–8 NVIDIA A100 GPUs) · OCI networking and IAM. The listing is the only delivered artifact carrying an explicit required flag per item, and it is the model. The tier statement for Field Service: **PoV Jumpstart = file export / import; Integration = API write-back; Scaling = API plus telemetry.**

**Anti-patterns.** A free-text product name that is not in the catalog (that is a catalog change request, not an entry). A product name taken from an internal deck rather than the vendor's own current label. An integration claim with no tier attached — the WfO estate carries exactly this contradiction, where the one-pager's architecture makes Field Service the native centre while the feature list marks the same integration `○ roadmap`; both are true at different tiers, and neither says so.

---

### 10 · Optional Oracle products

**Definition.** Oracle products that could logically be an **additional data source or destination** for this pack, same catalog, same `why`, flagged `role: optional`. "Optional" is about the product's place in the solution, not about a tier deferral.

**Good.** The shape is new: **no delivered artifact in the WfO estate, and none in the sibling packs, lists optional Oracle products as such.** The nearest things are a listing flag that actually means "deferred to the next tier" and a vendor-neutral "Additional datasources" box on a deck slide. So the spec is the source, and a builder must not go looking for a precedent it will misread. WfO's optional set follows from its own integration list — people availability, spare-parts availability, demand forecasting, KPI/analytics export — each mapped to the Oracle product that would serve it.

**Anti-patterns.** Reusing the listing's `required: false` flag as the definition (it encodes tier deferral, which is component 12's business). Padding the list with every Oracle product that exists. Naming an optional product with no stated reason it would be a source or a destination.

---

### 11 · Key performance metrics

**Definition.** **One metric set per pack** (Alex, 2026-09-18). Each metric carries a formula, a baseline, a cleared figure, a `figure_status`, a caveat and an **attribution rule that varies by channel**. Two contradicting or overlapping sets for one pack are unacceptable.

**Good.** WfO's set, as printed: *"~30 min* to optimize and approve a region's 4-week plan: down from ~2 days"* · *"up to **+26%** productivity gain on proof-of-value data across the US, UK and Netherlands"* · *"**€190K / month** estimated savings at full launch, valued as the cost of additional staffing avoided"*, under the caveat *"KPIs measured before/after on proof-of-value data; figures are illustrative, not contractual."* The formulas sit behind them and are computed identically on the current and the optimized plan for the same window: productivity = total jobs ÷ days with at least one job, averaged across technicians; capacity utilization = round(jobs ÷ (working days × 7) × 100), capped 0–100; average wait = booking date to appointment date in whole calendar days.

**Attribution by channel.** The figure does not change; the name attached to it does. Under the customer's name where `clearance.customer_name_allowed` is true for that channel (*"Proof of value · \<customer\>"*), and under the anonymized descriptor otherwise (*"proof of value at a global home-appliance manufacturer"*). Clearance is revocable and re-checked every round.

**Anti-patterns.** Two figure sets in one estate — the WfO print artifacts and the WfO listing ship different numbers for the same pack, which is precisely the failure this component now forbids. "Proven" on anything but a delivered result (PoV figures get "proof of value", and a PoC *target* is never typeset as an outcome). A number without its footnote. The engine figure instead of the end-to-end figure (30 minutes including review, not 15 minutes of solve). A small percentage shipped without the sentence explaining why it is large at scale.

---

### 12 · Service packages table

**Definition.** Three tiers — **PoV Jumpstart / Integration / Scaling** — with `S / M / L` as size tags in internal tables only. Per tier: duration, services price, infrastructure price, what the customer gets, scope in and scope out; plus a **per-capability-area handling row** across the three tiers. Tiers map to **integration depth, not feature count**.

**Good.** The WfO one-pager's compact form is canonical: tier headers carrying name, size letter and a one-sentence scope (*"PoV · S — Manual data import, limited rule set: prove the KPI gains on the customer's data"*), then three commercial rows (infrastructure price, services price, timeline) and six capability rows rendered as `◐ partial · ● included · ●● multi-region / advanced`, with `—` where a capability is not in the tier, and a single footnote for the indicative prices. Deck slide 10 is canonical for the detailed form: the same rows with prose per cell. Tier semantics, from the partner co-design session: S proves the value with zero integration in a test environment; M delivers a live, fully-integrated deployment at one location; L scales it across markets with per-region rules and telemetry. **PoV duration target 4–8 weeks, hard cap 10** — the skill pushes back above 8 with reasons and rejects above 10.

**Anti-patterns.** Inventing a tier, a price or a scope line that does not exist — where a pack has no S/M/L, the block is reframed honestly ("What the PoC buys": scope in / not in, real duration, real contract value). Labelling the L tier "hardening" (it invites "what was wrong before?" — frame it as telemetry and local tailoring). Publishing prices beyond the PoV externally. A price that contradicts the artifact thumbnail on the same slide. Two tier vocabularies in one estate.

---

## 2. The artifact matrix

Rows are the components; columns are the six artifacts. Each cell is the **form** the component takes there. `—` means the component is genuinely absent by design.

| # | Component | Feature list (.docx) | Sales deck (.pptx) | Sales one-pager (1× A4) | Executive summary (1 slide) | Mini-site listing | Interactive demo |
|---|---|---|---|---|---|---|---|
| 1 | Name | H1 `<Name> App by SoftServe` under the `SOFTSERVE × ORACLE ·` kicker | Cover title + running header on every content slide | `<h1>` in the hero; external variant, optional `Accelerator App by SoftServe` subheading | Slide title `<name> — executive summary` | `name` + `slug` + `headline{accent, rest}` (two-part split for the hero) | App chrome only; no vendor or customer marks |
| 2 | One-liner | — (an `App.` scope paragraph instead, different register) | Cover subtitle, product-scoped | `p.sub` under the H1 — **canonical full form** | — by design (the slide opens on the use case) | `oneLiner` (full) + `shortLine` (rep-sayable) + `heroCaption` | — by design |
| 3 | Problem ↔ solution | One clause inside `App.` | Slide 2: two cards + 3 KPI chips; slide 4: Today \| Tomorrow narrative | `h2.sec` "The problem" + 3 dashed bullets; `h2.sec` reframe heading + 3 outcome chips + body — **canonical** | One `USE CASE` card, solution first, problem as one trailing sentence | `overview.problemSolution{problem,solution}{title,text,icon}` + `moreDetail` Today/Tomorrow + one entry per sub-problem | Live exceptions via `flagsFor(applied)`; dramatized, never stated as copy |
| 4 | Target ICP | — | — (the anchor strip carries *seller* ICP; not this component) | "Where it applies" chips; the `Repeatable:` bullet is seller-framed | — | `overview.industriesNote` — **canonical** | — by design |
| 5 | Verticals | Named inline in the `App.` paragraph | Slide 3: four equal cards, one concrete line each | `.chips` under "Where it applies" — names only | One `VERTICALS` line — names only | `overview.industryCases[]{industry,label,image,problem,solution}`, tabbed — **canonical, the only full pair per vertical** | — by design (industry-neutral) |
| 6 | Capabilities | The matrix: `Area / Category / Feature / Current status / Standard customization scope` + legend — **canonical master** | Slide 10: capability × tier with prose per cell | The 6 capability rows of the packages table, glyphs only | A feature-list thumbnail, no content | `technology.capabilities[]{stage, items[]{name, state}}` — **site view, derived from the master by stage**; plus `overview.features[]` / `featuresDetail[]` at marketing altitude | `settings.rules[]{name,type,desc}` + `settings.objectives[]{name,desc,weight}` panels |
| 7 | Workflow architecture | Partial — the "Review and approval workflow" area only | Slide 4, prose | One sentence in the solution body | — | `overview.steps[]{n,title,text,image,features[]}` — **canonical**, one captured demo frame per step | `inputSheets` → `stages[]` → dashboard → `flagsFor()` → `reoptStages[]` → `exportColumns` — **canonical for the HITL loop** |
| 8 | High-level architecture | — | Slide 7 — **canonical detailed form** | `.arch` three-column diagram with labelled pipes — **canonical compact form** | The 4-rung solution-layers ladder (a stack, not a flow) | `technology.narrative` + `technology.stack[]{key,label,summary,vendors[],items[]}` + the `diagrams.js` flow entry — richest, the only machine-readable I/O direction | `settings.connectors[]{name, state, dir}` |
| 9 | Required Oracle products | Integration rows, each with its own status glyph | Slide 6 stack badges; slide 7 infrastructure label | The `.arch` boxes (no required/optional split) | Ladder rungs | `technology.stack[].items[].required: true` — **canonical, the only explicit flag** | De-branded connector names, by design |
| 10 | Optional Oracle products | Integration rows carrying a roadmap glyph | Slide 7 "Additional datasources" box (vendor-neutral) | — by design (no room on one A4) | — | `technology.stack[].items[].required: false` with a `note` naming the tier | Connectors shown in a not-configured state |
| 11 | KPIs | KPI **names only**, no values, as an area of the matrix | Slide 5: 3 stat chips + footnote | `.stats` ×3 + `p.caveat` — **canonical for the sales set** | `PROOF OF VALUE · <customer>` — 3 stats | `overview.metrics[]{value,label,qualifier,icon}` + `metricsNote` + `roi` + `tile.outcomes[3]` + `caseStudy.metrics[2]`; anonymized attribution | Computed in the page, never quoted; the **before → after band leads**, each number drilling down to the change that produced it |
| 12 | Service packages | — by design (no pricing on a feature list) | Slides 8 / 9 / 10: glyph table without infra row, with infra row, and the detailed prose form | `section.packages` → `table.pk`: 3 tier headers + 3 commercial rows + 6 capability rows + legend + footnote — **canonical compact form** | A three-row tier strip (name · scope · price · duration) | **Jumpstart narrative, PoV price only**; Integration and Scaling read "Scoped per engagement" | Implied as surfaces (available regions, connector count), never stated |

**Standing rules the matrix encodes** (Alex, 2026-09-18):

- **Tier names are `PoV Jumpstart / Integration / Scaling` in every artifact.** `S / M / L` survive only as size tags in internal tables. Print artifacts get relabelled at their next rebuild.
- **Features are `Area > Category > Feature` with `● ◐ ○` everywhere.** The site's stage view is derived per pack from that master, never authored separately.
- **One metric set per pack**, with attribution varying by channel and approval, never the figures.
- **Every integration claim states its tier** in the sentence that makes it.
- **The sales one-pager is one A4 page, always.** When the content does not fit, the skill proposes cuts and does not add a page.

---

## 3. Per-artifact anatomy

Each artifact has a fixed section order. Packs differ in content, never in anatomy.

### 3.1 Sales one-pager — HTML → print → one A4 PDF

Section order, fixed:

1. **Hero** — eyebrow (`OCI AI ACCELERATORS`), H1 (the external name), `p.sub` (the full one-liner), hero photograph faded left-to-right behind the right 46%.
2. **Pitch**, two columns (≈57.5% / 39.5%):
   - Left: `The problem` heading + one lead sentence + three dashed sub-problem bullets; `The solution: <reframe>` heading + three outcome chips + the mechanism in two sentences; then the **`.arch` data-flow line** — a three-column diagram (`25mm 1fr 54mm`) with the source system on the left, the platform box on the right, and two labelled pipes between them.
   - Right: the **"Why it sells: for \<partner\> account teams"** card, three bullets, plus a **`Where it applies`** chip row of verticals.
3. **Proof strip** — customer logo (real image where cleared, anonymized descriptor otherwise), the three-sentence story, three `.stat` figures, and the caveat line directly beneath them.
4. **Packages** — the tier table: three tier headers carrying name + size tag + scope sentence; infrastructure price, services price, timeline; the capability rows as glyphs; the glyph legend bottom-left and the price footnote bottom-right.
5. **CTA footer** — the question, the offer answer, and the named contact block (name, title, email) right-aligned.

Format constraints: one `.page` div at `210mm × 297mm`, `overflow: hidden`, `@page { size: A4; margin: 0 }`, print colour adjust exact. No web fonts and no external assets — logos inline as SVG, photographs as base64 `data:` URIs. Section order is not negotiable; content is cut to fit, and the skill says which cuts it proposes.

### 3.2 Sales deck — .pptx, 16:9, on the brand base

Ten slides, in order:

1. **Cover** — name, one-liner, the brand cover layout.
2. **`USE CASE`** — problem card | solution card, three KPI chips, an anchor strip.
3. **`VERTICAL APPLICATIONS`** — four equal cards, one concrete line per vertical.
4. **Today | Tomorrow** — the narrative form of the reframe, plus one named vertical case.
5. **Proof / commercial case** — three stat chips with the footnote, then `CONTEXT` / `SOLUTION` / `VALUE FOR <partner> + <engine vendor>` / `VALUE FOR CLIENT`.
6. **`TECHNOLOGY STACK`** — the vendor ladder, with the pack-versus-tailored split.
7. **`Architecture`** — the detailed data flow: source systems plus additional datasources → the app → the engine on the named infrastructure, with labelled arrows.
8. **`TAILORED SOLUTION: PACKAGES`** — the glyph table **without** the infrastructure row.
9. **The same table with the infrastructure row.**
10. **`… PACKAGES (DETAILED)`** — the same rows with prose in every cell.

Slides 8, 9 and 10 are three alternates of one table; the deck ships all three and the seller picks. Standing geometry, layouts and the package-table dimensions are in the brand deck kit. Speaker notes in the source decks carry live review comments and are never reproduced.

### 3.3 Feature list — .docx

1. All-caps kicker line: `SOFTSERVE × ORACLE ·`.
2. **H1**: the internal name variant.
3. **`App.`** — a single run-in bold paragraph: what the product does in one sentence, then the verticals it spans, numbered inline.
4. **The capability matrix** — five columns: `Area | Category | Features | Current status | Standard customization scope`. `Area`, `Category`, `Current status` and `Standard customization scope` are merged down across their rows, so only the first row of a group carries text. Footnote markers (`*`, `**`, `***`) append inline to the status glyph.
5. **Legend** — one line per glyph: `●` available out of the box, configuration may be required · `◐` partially implemented out of the box, major improvements on the roadmap · `○` roadmap.

No pricing, ever. No tier columns. The matrix is the master that every other capability rendering derives from.

### 3.4 Executive summary — one slide, in the host deck's style

Built to paste into someone else's deck, on that deck's own master, so it renumbers itself. Latest style reference: `Oracle AI Packages - section slides.pptx` (2026-09-11), whose per-pack slide is the current model.

Six blocks on one slide, in a two-row, three-column arrangement:

| | | |
|---|---|---|
| **`USE CASE`** — the name, the one-liner as a subtitle, problem → solution compressed into one card | **`SOLUTION LAYERS`** — the 4-rung vendor ladder | **`PROOF OF VALUE · <customer>`** — the three stats with their caveat footnote |
| **`VERTICALS`** — four icon tiles, names only | **`SERVICE PACKAGES`** — three compact tier rows: name · scope · price · duration | **`PLANNED NEXT STEPS`** — three numbered items |

A footnote line runs along the bottom. Variants exist with a capability-matrix thumbnail and with an `ARTIFACTS` block of material thumbnails in place of one of the right-hand cells; the skill offers both and defaults to the version without the thumbnail. Contact block is the internal one.

### 3.5 Mini-site listing — a `products[]` entry

The listing is a data object, checked by the site's own checker. Keys, in file order:

```
slug · name · headline{accent,rest} · category · categoryChip · facet · oneLiner · shortLine · heroCaption
tags[] · hero{image{file,alt,focal}} · tile{outcomes[3]}
overview{
  problemSolution{problem{title,text,icon}, solution{title,text,icon}}
  metrics[]{value,label,qualifier,icon} · metricsNote · roi{icon,text}
  features[] · featuresNote · featuresDetail[]{title,body}
  industriesNote · steps[]{n,title,text,image,features[]}
  industryCases[]{industry,label,image,problem,solution}
  scope{in[], out[]} · moreDetail[]{title,body}
  caseStudy{descriptor,area,industry,status,metrics[]{value,label},story,scope[]{label,value},ndaLine,downloadLabel} | null
}
technology{ narrative · stack[]{key,label,summary,vendors[],items[]{name,required,direction,note}} · capabilities[]{stage,items[]{name,state}} }
jumpstart{ title, promise, durationShort, pillars[3]{key,title,text}, outcomes[], timeline[]{label,text},
           needs[], investment{price,duration,includes[],footnote}, next[]{tier,text,duration,price}, cta{label,route} }
sellers{ materials[]{key,title,description,state} }
```

Separately, `diagrams.js` carries the architecture flow: `{layout, sources[], group{label,nodes[]}, target{title,sub,accent}, loop}`, with titles and subtitles as pre-broken line arrays.

Listing-specific rules: a number never renders without its footnote; an absent optional key means the block does not render; absence renders as an empty instance or nothing, never as a "missing" sentence; only the PoV price is published; no customer names or logos anywhere under the deployable root.

### 3.6 Interactive demo — `site/demo/<slug>/`, four files, no build

The demo is not a slide deck in HTML. Its anatomy is a **data model**, and the shape is the same for every pack:

- **Current state** — the world the product operates on (entities, the period, the plan as it stands).
- **Named changes** — each change carrying `{id, rule, kind, title, what, why, <scope>, overrides, effects}`: the rule that produced it, what it does, why, and its **additive effect on each KPI**.
- **`flagsFor(applied)`** — exceptions computed as a function of which changes are applied, so nothing is hard-coded.
- **Additive KPI effects** — every number computed in the page from raw means, so an undo recomputes everything and every figure reconciles.
- Around them: `inputSheets` / `pickerFiles` (mocked upload), `stages[]` and `reoptStages[]` (the processing run), `settings{mode, objectives[], rules[], regions[], connectors[]}` (the capability and architecture surfaces), `exportColumns` and `priorHistory` (the audit trail), plus the shared tour engine's `STEPS[]` of `{id, major, side, title, body, target(), anchor(), auto(), passive?}` and the URL switches `?tour=off`, `?ui=clean`.

Standing demo requirements: keep the real product's flow, screens and information model and generalize the **content** to what the pack sells; synthetic data only, with no customer geography, ids or uncleared figures; **lead with the value** — a before → after band on the product's own KPIs immediately after the run, then drill down from each number to the rule and effect behind it, then let the viewer override a change by hand and watch the numbers follow. Red-team the first cut against the pack spec before delivering.

---

## 4. Standard extras on every sales artifact

These are not among the 12, and they are not optional decoration. Each one appears on every sales artifact that has room for it.

1. **"Why it sells: for the partner's seller."** A dedicated block of partner value, distinct from customer value: the cross-sell path into a product the account already owns, the **net-new consumption** the pack creates on top of the existing seat, and the repeatability across similar accounts. Present on every partner-facing artifact; correctly absent from the listing and the demo, which are customer-facing. Where known, target consumption levels per tier belong beside the packages table.
2. **Proof block.** Logo (real image where cleared) or anonymized descriptor + industry medallion, a three-sentence story, the three stats, and the caveat immediately beneath them. Status is said once, in one plain word — proven, measured, modeled, forecast, estimated, in preparation — and the footnote spends its line on evidence.
3. **Solution-layers ladder.** The four-rung vendor attribution: custom configuration (ours) → accelerator business app (partner + ours) → engine (engine vendor) → infrastructure (partner). Distinct from the architecture diagram, which is a data flow. Partner layer on top, real logos, layers differing in weight and shape rather than tint.
4. **CTA + contact, per channel.** The question, the offer, and the contact the channel dictates: a named partner-facing person on print artifacts, a practice mailbox plus a named person on the site, the packaging owner plus the internal request mailbox on internal decks. Never a personal mailbox on a public page. The spec's `contacts` block carries all three so nobody picks.
5. **Disclaimer / caveat line.** Universal. A figure never ships without one; an indicative price never ships without one. On the listing these are named keys (`metricsNote`, `featuresNote`, `investment.footnote`, top-level `disclaimers`) so the checker can assert them.
6. **Glyph legend.** Wherever a glyph appears, its key appears on the same page or slide. One system across the estate: `● ◐ ○` for feature status, `◐ ● ●● —` for tier coverage.
7. **In-scope / out-of-scope boundary.** A one-sentence boundary statement, then a numbered IN SCOPE list and a numbered OUT OF SCOPE list. Present on the listing as `overview.scope{in, out}`; the sibling packs' one-pagers carry it as a `USE-CASE BOUNDARIES` block. It belongs on any artifact a buyer uses to decide.
8. **Roadmap rows.** What is deliberately not in the pack today, stated positively and only where cleared. The feature list carries it as `○` rows; the listing carries it as a `moreDetail` entry and `state: "roadmap"` items. A roadmap ceiling is never published externally as a count or a negation.

---

## 5. Divergences the WfO estate still carries

The delivered WfO artifacts are the best reference for **anatomy** and the worst reference for **consistency**. A builder copying a value out of one of them will copy one of these. Every one is already resolved in the spec; read the spec, not the artifact.

| Divergence | What the estate carries | The resolved value |
|---|---|---|
| **Five PoV infrastructure prices** | Deck slide 8 has no infra row; deck slide 9 and the executive summary say `€0`; the Jul-13 one-pager says `€4K`; the Jul-17 one-pager says `~€2K *`; the listing says `€4K/mo` | **`~€2K / month`, status `indicative`**, with the footnote "Indicative; depends on the usage and optimization rules complexity". The spec's `packages.tiers[pov].infra_price_monthly` is the only source. |
| **Two tier vocabularies** | Print artifacts: `PoV · S` / `Roll-out · M` / `Scaling · L`. Mini-site: `Jumpstart Proof-of-Value` / `Integration` / `Scale` | **`PoV Jumpstart` / `Integration` / `Scaling`** everywhere, with `S / M / L` as size tags in internal tables only. Existing print artifacts get relabelled at their next rebuild. |
| **Three contacts** | the alliances contact on the one-pagers; the practice mailbox on the site; the R&D request mailbox plus a different named person on the internal section deck (the addresses themselves: `naming-and-clearance.md` §3) | **Not a choice — a per-channel mapping.** `contacts.partner_print` / `contacts.site` / `contacts.internal` in the spec; the builder reads its own channel. |
| **Two one-pager versions** | Jul-13 (shared drive, `€4K`, "Oracle Field Service") and Jul-17 (local HTML build source, `~€2K`, "Oracle Fusion Field Service") | **Jul-17 is canonical** (Alex, 2026-09-18). The shared-drive PDF was overwritten in place with it under the same name so the share link survives; the Jul-13 file is archived locally as superseded. |
| **Two product names for the same product** | "Oracle Field Service" on the deck, the feature list and the listing; "Oracle **Fusion** Field Service" on the Jul-17 one-pager | **The catalog's canonical name**, from `shared/data/oracle-products.yaml`, re-verified against the vendor's own current label at each build. Never the name as it appears on an internal deck. |

Four more the spec resolves, listed so nobody re-introduces them:

- **Two glyph systems.** The delivered feature list distinguishes "available" from "partial" with two colours of the same `●` (`#1485C3` and `#C1E4F5`) — a distinction that vanishes in plain text, in print and in any converted copy. The standard is three distinct glyphs, `● ◐ ○`.
- **Two figure sets.** The print artifacts ship one set of headline numbers; the listing ships a different, anonymized, modeled set for the same pack. One metric set per pack, attribution varying by channel, figures never.
- **Two PoV durations.** Every print artifact says "2 months"; the listing says "4–8 weeks" with a week-by-week timeline. One duration, asserted by the linter: **4–8 weeks, 10-week hard cap**.
- **Two capability grouping axes and inconsistent casing.** `Area > Category > Feature` on the feature list versus workflow `Stage > Item` on the listing — the second is **derived** from the first, per pack, by the spec. Title Case on print artifacts versus sentence case on digital ones is settled by `meta.name_variants`, not per artifact.
