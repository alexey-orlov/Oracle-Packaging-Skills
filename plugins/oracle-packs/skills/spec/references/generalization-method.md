# Generalization method

How `/oracle-packs:spec` turns **one delivered engagement** into a **generalized pack**: the
workflow research, the vendor study, the vertical differentiation, and the adjudication that
stands between them and the candidate options.

This runs as **stage 2 of the spec skill** — after the first questions, before the pack's story.
Its output is the research brief (`research-brief-format.md`), and then
`workflow.steps[]`, `verticals[]`, `capabilities[]` and `meta.source_engagement` in
`pack-spec.md`.

**This file is read by the research agents, in their own context — never loaded into the
conversation with the owner** (the spec's `SKILL.md` names it on that step's `Agents read:` line). Its
vocabulary is internal: no test or prompt id here, and no word from it, ever appears in anything
the owner reads. What the owner is asked after the research is on `cards/research-review.md`; the
candidate pack stories are on `cards/story.md`.

Rewrite this file in place when the method changes. Never stack dated "UPDATE" sections.

---

## 1. Why this step exists, and the one rule that governs it

The pack is not the delivered project. The delivered project is one instance of it, and the
distance between them is the product work. Alex, reviewing how a delivered case had been
folded into the use-case map (2026-09-13):

> "I think that's too narrowly framed. Can we generalize it to be not that industry-specific?"

And, coaching the same method on the document-processing pack (2026-07-24, RU):

> "there will be a lot of water and Claude trying to satisfy you and find differences; you then
> need to figure out which of these are real differences — but then you'll be more confident
> that you really considered all these different scenarios and generalized enough."

**The governing rule: generation is for coverage, human judgment is for truth.** Never ship the
model's differentiation, gap or vertical list unfiltered. The deliverable is the *adjudicated*
subset **plus** the justified confidence that the space was swept. Every step below therefore
splits into what the agent produces and what the user decides.

Second rule, from the same session: **draft before you research.** Alex tells Vlad to sketch the
maximally generalized step list themselves first, then use research to validate and challenge it —
not to ask a model for a workflow from a blank page:

> "I'd advise you, to get this workflow question sorted — which steps, which features are
> universal — to sketch yourself a draft of these steps. It seems to me the import → analysis →
> review pipeline consists of these steps, at maximum generality."

---

## 2. The test — "general enough, but not too general"

Run all eight checks before proposing options. A failed check is either fixed or written into
the brief's open questions with the decision it blocks. Do not average them away.

| # | Check | Catches | How to run it | Source |
|---|---|---|---|---|
| T1 | **Three-vertical hold** | over-fitting to the delivered case | The step list holds for ≥ 3 **named** verticals with the same steps in the same order. Differences live in the "what matters here" cell, never in the spine. If a vertical needs a different step order, it is a different pack — say so. | R3 (2026-07-24); row-writer self-check "examples from ≥ 3 different industries" |
| T2 | **Entity test** | fake verticals (industry labels over an identical object model) | Each scenario must differ in the *entities* it processes, not only in the industry name. Alex: "a scenario where, in your view, the entities are different. Not different industries that are identical under the hood." | Alex, 2026-07-24 |
| T3 | **Label test** | the customer's own vocabulary surviving into the pack | Would a buyer in three unrelated industries search for this name? "Work-package variance analysis" failed ("work package" is construction/EPC vocabulary) and became "Plan-vs-actual investigation". | row-writer prompt §3.1, 2026-09-13 |
| T4 | **Honest-boundary test** | generalizing into vagueness | When you widen, state the boundary that keeps the claim true and differentiated — e.g. fragmented-source evidence assembly, *not* commentary over a clean ledger that a native product already ships. A widened scope with no boundary is a slogan. | row-writer prompt §3.1 |
| T5 | **No-quirk test** | one customer's oddity presented as a product step | No step or rule exists only because the delivered customer works that way. The workforce case's year-ahead rigid work-zone stability is one customer's habit, atypical for the industry, and it was baked into the algorithm: it becomes a configurable slider, a labelled customer-specific rule, or it leaves the spine. | 2026-07-07 call note |
| T6 | **Failure-path test** | silent gaps | Every step names what happens when the expected thing is not there. No handling = an explicit "not covered" row **and** an OUT OF SCOPE line, never silence. | R2 (2026-07-24) |
| T7 | **Ingress / egress test** | a pack that is an island | The workflow names a real input system and a real output system. Alex: "any client needs this not as a standalone thing — it has to be integrated with something on the way in and on the way out." State the tier at which each integration is real (PoV = file import/export is a legitimate answer). | Alex, 2026-07-24; decisions 2026-09-18 ("state the tier next to every integration claim") |
| T8 | **Instance test** | pretending the pack is what was delivered | The delivered case is stated as one instance, with its divergence named in one line (`meta.source_engagement.divergence_from_pack`). Also: the delivered project's out-of-scope list is **not** the pack's — adjudicate each item. Alex: "that looks out of scope in the [delivered] project, not in our pack." | pack-spec schema; Alex, 2026-07-24 |
| T9 | **Empty-circle test** | a capability list that never left the delivered scope | A generalized matrix with **no ○ rows** is evidence the table is incomplete, not that the product is complete. Alex, twice, on the same table: "we are still at the point where almost all rows are done — some half, some fully — and there are none that are not done. That question still bothers me, same as last time. **There must be some row that is definitely not done.**" If the pass produced no roadmap row, it has not generalized past what was built — go back to steps 4–7. | Alex, 2026-07-24 |

Two standing counterweights to T1–T4, so the pack does not generalize itself into nothing:

- **The workflow generalizes; the go-to-market does not.** Name the partner's specific system in the
  integration and ICP lines even when nothing is technically bound to it. Alex on the workforce
  pack: "we don't even write 'integration with some workforce management system of yours' — we
  write Oracle Field Service specifically, so it is all clear … even though right now nothing is
  hard-wired to OFS, zero. It simplifies perception and positions it for a concrete story."
- **Never bind a feature to a model or an engine.** Alex, on a feature row naming a specific LLM:
  "I wouldn't write in the features that it's Llama … it isn't a property of the feature, and why
  lock yourself into it." Engine dependence belongs on the specificity axis (T/step 9), not in the
  feature name.

---

## 3. The procedure

Thirteen steps. Steps 5–7 are Alex's explicit **three-move process** (their "трёхходовка"), step 4
is the up-front task they append to it. Each step states what the agent does, what the user
adjudicates, the output shape, and when to stop and ask.

### Step 0 — Gate: is this a pack at all?

- **Agent:** state (a) the real partner/market pull for this pack — named opportunities, not
  enthusiasm; (b) whether the underlying systems and the KPI promise are stable enough across
  customers to package. Some cases stay opportunistic by design.
- **User adjudicates:** go / no-go, and if a case was previously parked as unpackageable, what
  changed.
- **Output:** three lines — pull, packageability, verdict.
- **Stop and ask when:** the only evidence of pull is the delivered project itself. Alex, 2026-07-14:
  "just hammering something out in a vacuum is pointless."

### Step 1 — Inventory the delivered case (three lenses)

- **Agent:** from the engagement's own materials (SoW, user guide, requirements, PoC deck, demo
  recording, feature sheets, call notes) reconstruct: actors, systems, data in/out, every screen
  and step, the HITL points, the KPI definitions **as the delivery actually computed them**, and
  what was explicitly out of scope. Then classify every capability on **three lenses**: what the
  vendor accelerator pack gave · what we implemented · what stays custom per engagement.
- **User adjudicates:** the custom-work column's semantics before it is filled (see anti-pattern
  A7), and anything the materials contradict.
- **Output table:** `Area · Category · Feature · In the vendor pack · Our status (● / ◐ / ○) ·
  Custom work per engagement · Evidence`.
- **Stop and ask when:** a capability appears in a document but was never tested in the engagement
  — untested capability does not enter the inventory as delivered (R12).

### Step 2 — Draft the generalized workflow first

- **Agent:** write the job's workflow at maximum generality as **5–7 numbered steps** (§4 below: the research returns the finer list, the pack groups it at the buyer's checkpoints — and the pack's differentiating step gets its own place in the group rather than being folded into a neighbour), using
  step names a buyer would recognize, not the delivered product's screen names. Also draft the
  **scenario set**: the 3–5 *fundamentally different* cases you believe this job splits into,
  with the entity difference stated for each (T2).
- **User adjudicates:** the draft is their — they may rewrite step names and the scenario set outright.
- **Output:** the step list + the scenario list, both one line each.
- **Stop and ask when:** the delivered case supports fewer than 3 distinct scenarios.

### Step 3 — Domain workflow research across industries

- **Agent (research subagent, Opus):** how is this job done generally, across industries, today —
  including without any AI? Canonical step names and the vocabulary practitioners actually use;
  which steps are universal and which appear only in some industries; where the human decision
  sits; the industry-standard term for each step (industry-standard names beat invented blends).
- **User adjudicates:** which canonical names replace ours.
- **Output table:** `Our step · Canonical name(s) · Universal? · Where it differs · Source + tier`.
- **Stop and ask when:** the research finds no canonical vocabulary at all — that usually means the
  step is our own composite and should be split or merged.

### Step 4 — Vendor / competitor taxonomy study and the gap check

Run this as **its own task, up front**, before the differentiation pass. Alex's phrasing:

> "give it a separate task up front: 'I see it as these steps; look at such-and-such vendors and,
> based on how they structure their set of capabilities, highlight which steps I'm missing or
> where there are clearly other tasks.' Most likely it won't do it well unstructured, but it will
> highlight a gap in what we may have missed."

- **Agent:** 3–5 named vendors in three classes — **direct** (sells this job), **indirect
  substitute** (solves the pain another way, including "a team of analysts"), **same-vendor
  overlap** (an Oracle/NVIDIA product that already ships part of this). For each: how they *group*
  their capabilities, their step names, and the steps they carry that we do not. Then the reverse:
  steps we carry that nobody groups that way — over-splitting, usually.
  Judge competition at the **use-case** level, not the product-category label
  (`research-standards.md`), and admit only real, shipped capabilities — no "theoretically can
  also do this" rows.
- **User adjudicates:** each gap → **adopt now · roadmap (○) · reject**, with a reason. Expect low
  precision; the output is a gap list, not a structure.
- **Output table:** `Gap · Which vendors treat it as a step · Why we lack it · Adopt / roadmap /
  reject · Reason`. Adopted gaps that the delivered case never had are marked as **cross-vertical
  extensions** so they are never mistaken for delivered scope.
- **Stop and ask when:** a same-vendor overlap ships the widened scope natively (T4) — that is a
  positioning decision, not a research finding.

### Step 5 — Validate the scenario set (move 1)

- **Agent:** challenge the scenario set, not the steps. Am I missing a fundamentally different
  case? Alex's example of what a good answer looks like: "you didn't account for the fact that in
  all your cases everything goes through validation — but there may be a scenario where no
  validation is possible at all. Example: insurance."
- **User adjudicates:** which candidate scenarios are real and which are re-labels of ones we have.
- **Output table:** `Scenario · Entities that differ · Why it is not a re-label · Keep / drop`.
- **Stop and ask when:** a proposed scenario would change the step order (T1) — it is a different
  pack, and that is a scoping decision.

### Step 6 — Challenge the steps against the scenario set (move 2)

- **Agent:** "here are my N steps and the 5–7 patterns we found — do exactly these steps hold in
  each? Or am I missing one?" Return per scenario: steps that do not occur, steps that occur in a
  different form, steps missing entirely.
- **User adjudicates:** whether a divergence widens the spine or becomes a "what matters here" cell.
- **Output table:** `Step × Scenario` with `holds / differs / absent`, plus a one-line note per
  non-`holds` cell.
- **Stop and ask when:** a step is absent in more than one scenario — it is probably not a spine
  step.

### Step 7 — Vertical differentiation, widened then adjudicated (move 3)

- **Agent:** for each of the N steps, generate the specific differences across the scenarios, with
  a **"what matters here"** cell per intersection. Seed the prompt with two or three real examples
  of your own and ask it to develop the theme — Alex: "here are the 10 steps; I see examples of
  differences like this — in vendor contracts this matters, here it doesn't — develop the theme and
  think where else there may be differences." Define the correspondence (what a "difference" means)
  *in advance*.
- **User adjudicates:** real difference vs filler, cell by cell. This is the core quality gate.
- **Output:** the grid — rows = steps, columns = verticals, each cell = **what matters here** in
  ≤ 15 words. Plus, per vertical, a one-line problem ↔ solution framing in the fixed register
  **"Persona — what the system does; what the persona gets"**, 15–30 words, business language,
  no product names.
- **The grid's real yield is new rows on the left, not filled cells.** Model the workflow against
  two or three fundamentally different examples and ask, at each step, whether it can be trusted
  the same way there. Where it cannot, the answer is usually a **new feature row or a new
  configuration-setting row** — Alex, deriving one live: the client must be able to state the rules
  and approaches for what happens when mismatched values are found; "that is a separate block of
  functionality, which either exists or doesn't. If it doesn't — that's a row in your table with an
  empty circle." Configuration settings are first-class rows alongside features.
- **Stop and ask when:** a vertical's column is more than half filler after adjudication — drop the
  vertical rather than keep a thin one. Populate only cells the evidence supports and mark the rest
  "—"; a fully-populated grid is template-completion bias, not a win (`research-standards.md`).

### Step 8 — Failure path per step; absence is a finding

- **Agent:** interrogate every step: what happens when the expected thing is not there? Alex's
  original probe: "what do we do with a document if it's such that we expected to see 5 parameters
  and didn't find them? We don't foresee that case." Where the market has a name for the handling,
  use it — "isn't that what they call human-in-the-loop exception handling?"
- **User adjudicates:** which failure paths are in scope for which tier, and which become
  OUT OF SCOPE lines.
- **Output:** one `failure_path` string per `workflow.steps[]` entry, plus an explicit **not
  covered** list that feeds the artifacts' OUT OF SCOPE block.
- **Stop and ask when:** a failure path is unhandled *and* unavoidable in production — that is a
  roadmap item with a commercial consequence, not a footnote.

### Step 9 — Four-axis specificity classification

- **Agent:** test every feature on four independent axes and label it; do not delete.
  **customer-specific** (can not be used elsewhere) · **engine / vendor-specific** (irrelevant if
  another engine is used) · **use-case-specific** (only this job) · **industry-specific** (only the
  vertical the delivered customer sits in). Then the derived verdict: **reusable · configurable ·
  custom per engagement**. Rule of thumb recovered from the delivered workforce case: business
  logic (allocation rules, constraints, KPI *formulas*, forecasting) is per-client custom; the UI
  and the approval workflow are the most reusable; KPI *titles* are universal while their formulas
  are custom.
- **User adjudicates:** every `custom` verdict, because each one is priced scope.
- **Output table:** `Feature · customer? · engine? · use-case? · industry? · Verdict · Note`
  (`capabilities[].specificity` in the spec; empty list = generic).
- **Stop and ask when:** a feature fails three or more axes — it is delivery work, not a pack
  feature, and the user decides whether it leaves the list entirely. **Also stop when the list has
  no ○ rows at all** (T9): report that the generalization has not left the delivered scope and name
  which of steps 4–7 you are going back to.

### Step 10 — Candidate options: name · one-liner · problem ↔ solution

- **Agent:** propose **one to three triads**. Each: a plain **name** (passes T3), a **one-liner**
  that leads with the specific business value (time, money, risk or capacity) for a named role
  and object of work, in the buyer's words (card `one-liner`), and a **problem ↔ solution** pair
  written as the change in what the person does — the reframe form, "review the plan, not build
  it"; "review the data, not type it". Give each triad its grounding (which workflow steps and
  which verticals it covers), what it deliberately excludes (T4), and its risk.
- **User adjudicates:** picks one, blends, or sends the research back for another pass.
- **Output:** the triads block of the research brief; ≤ 120 words each; a recommendation with the
  reason.
- **Stop and ask when:** every candidate name is either the delivered customer's vocabulary or a
  category label ("AI document platform") — that means step 7 has not produced a boundary yet.

**Three hard constraints on this step.** The packaging promise is not a one-liner — Alex rejected
their own: "'packaged from proof of value to enterprise scale' and alike things don't fit as a good
product one-liner." No counts, taxonomy or packaging vocabulary in the name or the one-liner.
And the implementation is not a one-liner either — Alex, 2026-09-29: "focus not on the aspects of
the tech implementation, but on the very specific business value": no platform, vendor, engine,
model or data-architecture word (Oracle, OCI, NVIDIA, cuOpt, Lakehouse, GPU, LLM, "gold layer");
any how is what changes in the buyer's work, in plain words. `lint_spec.py` fails those words
(SPEC031).

### Step 11 — Red-team the result

Alex's own red-team, run on the Lakehouse packaging options and then standardized on the demos:

> "Challenge each one in terms: is [the platform] really the right answer to that challenge? is it
> feasible to build that in 1 month? … check if they are not the AI slop and real stuff, red team
> thoroughly, and update / remove or defend for me."

- **Agent:** for each candidate and for the generalized workflow as a whole —
  1. **Is this product really the answer** to that pain, or is a cheaper/native tool the honest
     answer?
  2. **Is it feasible inside the PoV window** (4–8 weeks, 10-week hard cap)? If not, what drops?
  3. **AI-slop check**: every step and feature must be a real, essential use of the product — no
     "theoretically can also do this" items; every row evidence-linked.
  4. **Narrowness check, the other direction**: is the generalized workflow narrower than what the
     pack's own documents already claim? This is the check Alex asked for by name on the demos:
     "doesn't [it] look too narrow compared to what's generalized in package docs we have? If yes —
     think how you can generalize more while sticking to the flow / interface / info architecture
     from the real solution (to not create a major gap between demo and what people will see in the
     real product)."
  5. **Risks column**: your own unresolved issues and risks, named.
- **User adjudicates:** remove or defend, item by item.
- **Output:** a short table — `Item · Challenge · Verdict (kept / cut / defended) · Risk`.
- **Stop and ask when:** the red team cuts a step that a candidate triad depends on.

### Step 12 — Compress to the TLDR

- **Agent:** write the research brief to `research-brief-format.md` — answer first, word budgets
  held, labels and source tiers per `research-standards.md`, every unsupported cell "—". Alex's
  standing instruction on this compression: "Too much text; less is more; condense to the essence
  of meaning, TLDR."
- **User adjudicates:** reads it and picks an option, or sends it back.
- **Output:** `<work>/research-brief.md` — the pack's local work folder, never the repo —
  referenced from `provenance.research_brief`.
- **Stop and ask when:** the brief cannot be read in 10 minutes — cut the least load-bearing
  section rather than shrinking every section evenly.

---

## 4. Prompts to hand to research subagents

Short, second person, one job each. Run on the mechanical model (Opus) unless noted; the
adjudication that follows each is never delegated. Ask each to return the stated table **plus** a
`sources` list with tiers and an `unverified` list.

**P1 · Domain workflow across industries**
> You are researching how the job "<job in the buyer's words>" is done across industries today,
> including without AI. Return the canonical workflow as numbered steps with the names
> practitioners and vendors actually use, as fine-grained as the job really is (often 8–12; the
> pack groups them to 5–7 afterwards). For each step: is it universal or industry-specific,
> where the human decision sits, and the industry-standard term. Name sources with tiers; prefer
> primary docs and case studies over marketing pages. Mark anything you cannot verify "—". Do not
> describe our product; we are not in this research.

**The pack's workflow is 5–7 steps.** The research returns the fine-grained list; the pack groups
it at the buyer's checkpoints — where a human decides, where an output appears, where data changes
hands — into five to seven steps (hard cap 7; fewer than 3 hides the work). Mechanics such as
normalization, dedup, entity resolution, routing or outcome capture are what happens *inside* a
step and are named in its description, never steps of their own (the owner, 2026-09-22, on a
12-step workflow: "too detailed — group to 5–7 max"). `lint_spec.py` enforces the cap (SPEC019).

**P2 · Vendor taxonomy gap check** (Alex's own framing — keep it)
> I see this job as these steps: <steps>. Look at these vendors: <3–5 named>. Find how each
> structures its own set of capabilities — their grouping and their step names — and highlight
> which steps I am missing, or where there are clearly other tasks I have not accounted for.
> Also name steps I carry that no vendor treats as separate. Return a gap list, not a structure;
> low precision is expected. Every claim gets a source and a tier; no "theoretically can also do
> this" capabilities — only real, shipped ones.

**P3 · Competitor classes**
> For the job "<job>", list competitors in three classes: direct (sells this job), indirect
> substitute (solves the pain another way, including doing it manually), same-vendor overlap (an
> Oracle or NVIDIA product that already ships part of it). Judge competition at the use-case
> level, not the product-category label: decompose the job into sub-jobs and say who wins each and
> on what dimension. Verify each product's *current* capability surface; never assert "can't
> compete" from memory.

**P4 · Scenario-set validation (move 1)**
> Here are the fundamentally different scenarios I think this job splits into: <scenarios>, and
> here are my <N> steps: <steps>. First, validate the scenario set: am I missing a fundamentally
> different case? A scenario counts as different only if the *entities* it processes differ — not
> if it is the same object model under a different industry label. For each candidate you add, name
> the entity difference and one concrete example.

**P5 · Step-set challenge (move 2)**
> Now take my <N> steps and challenge them against these <k> scenarios: do exactly these steps hold
> in each one? Or am I missing a step? Return a Step × Scenario grid with holds / differs / absent
> and a one-line note for every non-"holds" cell.

**P6 · Per-step differences (move 3, seeded)**
> For each of my <N> steps, generate the specific differences across each of these <k> scenarios.
> A "difference" means <definition, set in advance>. Examples of the kind of difference I mean:
> <2–3 real examples of your own — Alex's own worked example on the extraction step: in one
> scenario a broad trust level in the model is what matters, in another it is exact correspondence
> to a pre-agreed set of fields>. Develop the theme and think where else there may be differences.
> Fill a "what matters here" cell per step × scenario in ≤ 15 words; write "—" where there is no
> real difference — do not fill the grid for the sake of filling it. Where a scenario cannot be
> trusted at a step the way the delivered case is, propose the **new feature row or configuration
> setting** that would close it, and mark it not-implemented.

**P7 · Failure paths**
> For each step of this workflow, name the failure path: what happens when the expected thing is
> not there (missing field, unclassifiable input, no data for the period, a rule with no answer)?
> Where the market has a standard name for the handling, use it. Where we have no handling at all,
> say so explicitly — "not covered" is a valid and required answer, silence is not.

**P8 · Four-axis specificity**
> Classify each feature on four independent axes, yes/no each, with a one-line reason:
> customer-specific (unusable elsewhere) · engine-specific (irrelevant on another engine) ·
> use-case-specific (only this job) · industry-specific (only this vertical). Then give a verdict:
> reusable / configurable / custom per engagement. Label, never delete. Never name a model or an
> engine inside a feature name.

**P9 · Red team**
> Red-team this candidate pack. (1) Is this product really the right answer to that pain, or does a
> cheaper or native tool answer it? (2) Is it feasible within a 4–8 week proof of value? (3) Is any
> of it AI slop rather than real, shipped capability — check thoroughly and update, remove, or
> defend each item to me. (4) The other direction: is it *narrower* than what the pack's own
> documents already claim? (5) List your own unresolved issues and risks.

---

## 5. What the owner rules on after the research

The questions the research raises for the owner live on one card, `cards/research-review.md`,
and are asked there: at most four, in one widget call, under the heading the owner sees,
**"Your call on what the research found"**. This file does not restate them — the card is their
only home. Everything a research agent produces that needs the owner's ruling (which industries
are really different, which differences are real, which failures are in which package, how broad
the pack should be, which vendor gaps we adopt, what the engagement left out that the pack should
not) is written into the research summary so that card can pose it.

## 6. Anti-patterns

Each was actually rejected. Fix the class, not the instance.

| # | Anti-pattern | Where it came from | The fix |
|---|---|---|---|
| A1 | **Counts, taxonomy or packaging vocabulary in the name or one-liner** — "packaged from proof of value to enterprise scale" | Alex rejected their own one-liner, 2026-09-14 | The one-liner states the job and the outcome in the buyer's words; the packaging promise is sales scaffolding and lives in the packages block |
| A2 | **"Theoretically can also do this" features** | Lakehouse product research, 2026-08 — "Only items that are true essential uses / features of the product should be included" | Every feature evidence-linked to something delivered or shipped; speculative ones are ○ roadmap or absent |
| A3 | **Widening that drifts from the real product** | Demo red-team, 2026-09-16 — generalize more "while sticking to the flow / interface / info architecture from real solution" | Widen the *content* (types, rules, verticals, validators); never change the step order, the screens or the information model |
| A4 | **Generalizing into vagueness** | "Work-package variance analysis" → "Plan-vs-actual investigation", with the boundary kept | Every widening names the boundary that keeps the claim honest and differentiated (T4) |
| A5 | **Keeping a customer-specific rule as if it were generic** | Rigid year-ahead work zones, atypical, baked into the algorithm (2026-07-07) | Make it configurable, label it customer-specific, or drop it from the spine (T5) |
| A6 | **Technically-derived groupings a business buyer cannot place** | Alex on the use-case map, 2026-09-17: "they are broken down too much by the very technical detail … boundary unclear. I need better categorization" | Group where a cluster of business tasks in the stakeholder's mental model overlaps a technology pattern — their own stated reason for liking the groups they kept |
| A7 | **A column or list filled against a different definition than it was read with** | 2026-07-24: the "custom work" column read back as "even when this feature is perfect, we will still come and use a better model" — a false sentence. 2026-09-22, the same failure on a list: `oracle_products` was filled from the delivered engagement's *technology stack* instead of against the schema's own definitions, producing 5 required and 7 optional where 1 and 3 were true — "the pack is built on OCI API Gateway" does not survive the read-back. Alex: "I doubt that we need that much… we only need essential products in required" | Define the column's or list's semantics in one sentence **before** filling it — for `oracle_products` the schema already states them (*required = built on it or fully relying on it · optional = a plausible additional source or destination*) — then read each filled item back as a sentence and keep it only if it is true. **Completeness is not the goal: an enumerated component is a short list of what earns its place, and infrastructure a deployment merely implies never does.** The pull is strongest when a source document hands you a ready-made list, which is exactly when to re-read the definition instead |
| A8 | **Binding a feature to a model or engine** | 2026-07-24: "I wouldn't write in the features that it's Llama" | Engine dependence is a specificity axis, never part of the feature name |
| A9 | **Untested capability presented as delivered** | 2026-09-08: "Remove analytics block as it was not tested / was out of scope" | Status glyph backed by evidence; untested = ○ or absent |
| A10 | **Over-precision you cannot vouch for** | 2026-09-08: state "Filled / Partially filled / Not filled" plus a verification flag instead of itemizing | Graded status + verification flag; figures carry their status and caveat |
| A11 | **Inheriting the delivered project's out-of-scope list as the pack's** | 2026-07-24 | Adjudicate every exclusion separately (T8) |
| A12 | **Changing the structure for the sake of change** | Use-case map red-team brief, 2026-09-06: "don't get biased towards changing for the sake of change" | Prefer hosting a finding in an existing step over inventing a new one; renaming needs a reason stated in one line |
| A13 | **Formatting before the contents are complete** | R6, 2026-07-24: "finish this table … so that we have the table with the contents" | The table is the spine; layout is a later, separate pass — and the other artifacts derive from it |
| A14 | **A capability matrix with nothing marked not-done** | 2026-07-24, raised twice on the same table: "there must be some row that is definitely not done" | Treat it as an incompleteness signal, not a completeness one — T9; go back to the vendor gap check and the differentiation grid for the missing rows |
| A15 | **The implementation in the one-liner** — "re-planned on NVIDIA cuOpt", "from one governed gold layer" | Alex, 2026-09-29: "focus not on the aspects of the tech implementation, but on the very specific business value". The one-liner's old third question, "how, in one clause, generalized", had let the engine stand in for the how | The one-liner leads with the business value (time, money, risk or capacity) for a named role and object of work; any how is what changes in that person's work. The platform, engine, model and data architecture live in the architecture, and on the site's chips and Technology tab |

---

## 7. Self-check before handing the brief to the user

- Does the workflow hold for ≥ 3 named verticals with the same steps in the same order (T1)?
- Does each scenario differ in its entities, not just its industry label (T2)?
- Would a buyer in three unrelated industries search for the pack's name (T3)?
- Is the widened boundary stated, and does it exclude what a native product already ships (T4)?
- Does every step name its failure path, and is every "not covered" written down (T6)?
- Are the input and output systems named, each with the tier at which it is real (T7)?
- Is the delivered case stated as one instance with its divergence in one line (T8)?
- Is every vertical framing in the "Persona — action; outcome" register, business language, no
  product names, 15–30 words?
- Is every feature labelled on four axes, with no model or engine name inside a feature name?
- Does every one-liner lead with the business value (time, money, risk or capacity) for a named
  role and object of work, with no platform, vendor, engine, model or data-architecture word?
- Does the capability list contain at least one ○ row — something the generalization found that we
  have not built (T9)?
- Is every generated difference adjudicated, and is every unsupported cell "—" rather than filled?
- Does every claim carry a label ([Fact / source], [Practitioner consensus], [Inference],
  [Speculation]) and a source tier?
- Did the red team run, and is every cut or defence recorded with its risk?
- Does the brief lead with the answer and read in ≤ 10 minutes?

---

## 8. Provenance

Method sources, most load-bearing first. Items marked *(internal)* are not in this repo.

- **2026-07-24, "Oracle Productization & BA JumpStart Sync"** (Alex ↔ Vlad, RU) — the primary
  source for this file, and the only direct record of Alex coaching this method. Every quote above
  attributed to 2026-07-24 is from the **full** speaker-labelled transcript of the meeting
  recording (`Oracle Productization and BA JumpStart Sync-20260724_133119-Meeting Recording`,
  RU, EN glosses mine), *(internal; held by the call pipeline, not committed)* — not from the
  partial paste in the prep corpus, which is missing 26 of the 31 minutes and therefore misses
  the draft-first rule, the entity test, the empty-circle rule, the integration-naming rule, the
  feature/engine rule and the column-semantics read-back.
- **Prep corpus, 2026-09-17** *(internal wiki)* — `C-vlad-feedback.md` §2 (R1–R29) and §3 (the
  13-step process); `A1-sessions-decks-onepagers.md` §1 S4 (the Lakehouse packaging sequence:
  candidate table → self-challenge → red team → TLDR of differences → risks column → compress) and
  §2 (the 2026-07-07 feature-classification method).
- **2026-07-07 feature-classification working session** *(internal call note)* — customer-specific /
  reusable / engine-specific; business logic custom, UI and approval workflow reusable, KPI titles
  universal and formulas custom; zone stability atypical; zoneless planning a different product.
- **2026-09-13 / 2026-09-17 use-case-map sessions** *(internal)* — "too narrowly framed … can we
  generalize it to be not that industry-specific?"; the objection to technically-derived groupings;
  the card-label breadth test and the honest-boundary rule (also written into the map's own
  row-writer prompt, 2026-09-13).
- **2026-09-15/16 walkthrough sessions** *(internal)* — brand- and industry-agnostic requirement;
  the mandatory red-team against the pack specs; widen without changing flow, screens or
  information model.
- **`research-standards.md`** — labels, source tiers, named specifics, explicit gaps, no
  force-filled frameworks, use-case-level competitive judgment.
- **`shared/schema/pack-spec.md`** — the keys this method writes: `workflow.steps[]`,
  `verticals[]`, `capabilities[].specificity`, `meta.source_engagement.divergence_from_pack`,
  `open_questions`.
- **Structural borrowings** from the use-case map's row-writer prompt *(internal)*: check whether an
  existing step can host a finding before adding one; "the existing cells are the spec"; the
  "Persona — action; outcome" example register; a self-check list before returning; a structured
  return format per subagent. Its content is deal-specific and is not reused.
