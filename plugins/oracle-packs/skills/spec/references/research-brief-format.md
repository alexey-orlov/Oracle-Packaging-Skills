# Research brief format

The structured TLDR the user reads **after** the generalization research and **before** they pick a
candidate option. Written by `/oracle-packs:spec` step 2 to `packs/<slug>/research-brief.md`, and
referenced from `provenance.research_brief` in `pack-spec.yaml`.

The method that fills it is `generalization-method.md`. The epistemic rules are
`research-standards.md` — this file does not restate them, it says where they land.

Rewrite this file in place when the format changes. Never stack dated "UPDATE" sections.

---

## 1. What this document is for

One decision: **which generalized pack we are building.** Everything in the brief either supports
that choice or is cut. It is an internal working document, not a client artifact — internal
framings, counts and open risks belong here and are stripped later by the artifact skills.

**Its reader is the owner**, who knows the delivered engagement and the pack and nothing about how
this research was run. So the brief carries no step ids, no test ids, no file or key names and no
packaging vocabulary: every heading and every line reads as `shared/references/talking-to-the-owner.md`
requires. Findings are named by what they are — "the research on what the vendors already ship",
"how this workflow runs in other industries" — never by the prompt that produced them.

**Hard budget: a 10-minute read.** ~1,600 words of prose and table content, ten sections, no
section longer than one screen. Alex's standing instruction on this compression: *"Too much text;
less is more; condense to the essence of meaning, TLDR."* When it runs long, cut the least
load-bearing section entirely rather than shaving every section — their own rule when a page budget
bit: *"cut last page with 'sources analyzed' so that it's minus 1 page."*

---

## 2. The sections, in order

Fixed order. A section with nothing in it prints its heading and a single "—" line saying what is
missing and why; it is never silently dropped (absence is a finding).

The `§ n` numbers below are this file's own ordering, so that you and the sign-off cards can refer
to a section. **The brief prints plain titles and no numbers**, in this order:

| This file | The heading the brief prints |
|---|---|
| § 1 | The answer |
| § 2 | The workflow, generalized |
| § 3 | Where the pack differs from what we built |
| § 4 | The industries |
| § 5 | What the other vendors ship |
| § 6 | What happens when things go wrong |
| § 7 | What is specific to the customer |
| § 8 | The options |
| § 9 | Still open |
| § 10 | Sources |

Anything that points at a section — inside the brief, in a card, in a message — names it by that
title ("the research summary, section 'What is specific to the customer'"), never by its number.

### § Header — 6 lines, no prose

`Pack (working title)` · `Delivered engagement + date` (internal name; clearance decides what may
leave this file) · `Researched on` · `Status: research done | choosing the option` ·
`Read: N sources` · `Still open: N`.

### § 1 The answer — ≤ 120 words

Lead with it. Three things, in this order:

1. The generalized job in one sentence — what workflow this pack automates, for whom.
2. The recommended option (name + one-liner) and why it wins over the others in one clause.
3. The single finding that could sink it, named.

No "Overview", no restating the request, no closing pleasantry. If the honest answer is *this is
not a pack*, that is the answer — say it here with the reason (variability of the underlying
systems, a KPI promise that differs per case, no market pull), and stop the brief after §9.

### § 2 The generalized workflow — table, ≤ 12 rows

The steps every industry shares, in order, at the breadth that passed the
"general enough, but not too general" test in §2 of `generalization-method.md`.

| # | Step | Actor | Input → output | HITL | Failure path |
|---|---|---|---|---|---|

- `Actor`: system · human · ai. `HITL`: yes/no, and what the human decides.
- `Failure path`: what happens when the expected thing is not there, ≤ 12 words. **"Not covered"
  is a permitted and required value** — it flows to §6 and to the artifacts' OUT OF SCOPE block.
- ≤ 15 words per cell. Step names are the canonical ones from the domain research, not our
  product's screen names.
- Below the table, one line each: **Inputs** (named source systems) and **Outputs** (named
  destination systems), each with the tier at which the integration is real — "PoV: file export /
  import; Integration: API write-back" is a complete answer.
- Budget: ~200 words including the table.

### § 3 How the delivered case differs — ≤ 150 words + one table

One line first: the divergence, in the form that goes into
`meta.source_engagement.divergence_from_pack` — *"the pack generalizes X; the delivered PoC
hard-codes Y."*

Then the three lenses, by capability area, not by feature (the feature-level version is the
feature list's job):

| Area | In the vendor accelerator pack | We built | Stays custom per engagement |
|---|---|---|---|

Close with two lines: **what we built for the customer that the pack will not do** (the quirks
that belong to that customer alone) and **what was out of scope in the project but is in scope for
the pack**.

### § 4 Verticals — table, 3–5 rows

| Vertical | Entities that differ | Framing: "Persona — what the system does; what they get" | What matters here | Status |
|---|---|---|---|---|

- `Entities that differ` is the evidence that this really is a different business — one phrase. An
  industry that cannot fill it is the same thing under another name and does not belong in the
  table.
- `Framing`: 15–30 words, business language, one concrete artefact, no product or vendor names.
- `What matters here`: the two or three step-level differences that actually matter for this
  vertical, ≤ 20 words. The full step × vertical grid is an appendix, not this section.
- `Status`: **proven** (delivered) · **plausible** (evidence, not delivered) · **roadmap**.
- Budget: ~250 words. Fewer than three rows means the pack has not widened beyond the one customer
  it came from; say so, in those words, in the answer section.

### § 5 Vendor landscape and gaps — two tables, ≤ 250 words

| Vendor | Class | How they group this job | Steps they have that we don't | Steps we split that they don't |
|---|---|---|---|---|

`Class`: **direct** · **indirect substitute** (including "a team of analysts doing it by hand") ·
**same-vendor overlap** (an Oracle/NVIDIA product already shipping part of it). 3–5 rows.

| Gap | Who treats it as a step | Recommendation | Reason |
|---|---|---|---|

`Recommendation`: **adopt now · roadmap (○) · reject**. Gaps adopted from the market that the
delivered case never had are labelled **cross-vertical extension** so they are never mistaken for
delivered scope. Same-vendor overlap gets one explicit line: what the native product already does,
and the boundary that keeps our claim honest.

### § 6 Failure paths and absences — list, ≤ 120 words

Only the ones the workflow does **not** handle, one line each: the step, what is missing, and the
consequence if it appears in production. Each carries a proposed disposition — *PoV scope ·
Integration scope · OUT OF SCOPE line*. This list is the source of the artifacts' OUT OF SCOPE
block; an empty list is itself a finding and is stated as one.

### § 7 Feature specificity — table + 3 lines

| Area | Customer-specific | Engine-specific | Use-case-specific | Industry-specific | Verdict |
|---|---|---|---|---|---|

Per **area** (not per feature — the feature-level table is the feature list's job). Axis cells hold
the feature names that fail that axis, or "—". `Verdict`: reusable · configurable · custom per
engagement.

Then three lines: how many capabilities are available, partial and on the roadmap (the words, not
the glyphs, when this is said in a message); the areas that are built fresh for every customer
(these are priced scope); and, if **nothing at all is on the roadmap**, a flagged warning in those
words — the capability list never left what we built for the customer.

### § 8 Candidate options — 1–3 triads, one comparison table, ≤ 120 words per triad

One table: a column per triad, headed `<letter> · <Name>` (one plain name, no customer vocabulary,
no category label), and these rows in this order:

| Row | What the cell holds |
|---|---|
| One-liner | The job and the outcome in the buyer's words. Never the packaging promise. |
| Problem | The reader's pain, in the reader's words, one sentence: a named role and a concrete situation with the nouns on their desk — a sentence that person could say about their own week (the tangibility test, `shared/references/pack-anatomy.md` §1) — and readable with zero context: the business named in the sentence, literal words, everything it refers to introduced, at most 30 words (the zero-context test, same section). |
| Solution | The change in what the person does ("review the plan, not build it"), one sentence — what they do afterwards, never the machinery ("resolved, reasoned, mapped, scored") — readable with zero context in the same way. |
| Sells best in | The vertical(s) it covers first, and the workflow steps it spans. |
| Bets on | The differentiator and the evidence behind it (which findings, which competitor gap). |
| Leaves out | The boundary that keeps it honest. |
| Risk | The one thing that would make this the wrong framing. |

Rows, not paragraphs, so the same attribute reads across the options. A blend of two triads is a
column of its own or it is not an option.

Close with a **recommendation and its reason in one sentence**, and the alternative the user is
most likely to prefer instead. Options with a recommendation, never a menu without a view.

The table is shown to the user as is (the comparison card of `signoff-flow.md`), followed by the
pick widget whose options carry only the column label and one plain line — recommended option first
and labelled, free-text "Other" always present. This section is the written backing for that card,
not a second format.

### § 9 Open questions and gaps — ≤ 120 words

Each: the question · what it blocks (a spec key or an artifact) · the cheapest way to close it ·
who closes it. Everything the research could not verify lands here rather than in a hedge inside an
earlier section. Nothing downstream may print anything that depends on an open question.

### § 10 Sources — list, tiered

Grouped by tier, newest first inside each: **(1) primary** — vendor docs, patents, engineering
blogs, case studies with specifics, and our own delivered artifacts (SoW, user guide, requirements,
KPI methodology, call notes) · **(2) practitioner commentary** · **(3) real-case reports** ·
**(4) reasoning from principles**. Each line: title, date, tier, what it was used for. Press
releases and marketing pages are never tier 1.

Then two short lists: **searched and not found** (what you looked for and where — this is what
tells the user whether a gap is real or just unsearched) and **unverified** (product names,
capabilities or figures you could not confirm, each marked "(unverified)" wherever it appears
above).

If the brief is over budget, this is the section to compress — never the one to fake.

---

## 3. Labeling rules

These apply inside every section; they are the reason the brief can be trusted at speed.

- **Label every non-trivial claim**: `[Fact / source]` · `[Practitioner consensus]` ·
  `[Inference]` · `[Speculation]`. Inference is never stated as fact. In tables, the label goes at
  the end of the cell; in lists, at the end of the line.
- **"—" for anything unsupported.** Never "various tools", "industry-standard practice",
  "typically". A fully-populated grid is template-completion bias, not a win.
- **Named specifics only**: the vendor, the system, the metric, the number, the person. If you
  cannot name it, say you cannot.
- **Don't force-fill the framework, and interrogate it**: if the research surfaced something none
  of these sections can hold, say so in §9 rather than cramming or dropping it.
- **Figures carry their status**: `pov_result · delivered_result · target · modeled`, plus the
  caveat that will print alongside them. One metric set per pack — a second, contradicting set is
  a §9 item, not a footnote.
- **Product and vendor names** are re-verified as current, or marked "(unverified)".
- **Customer names** appear only where `clearance.customer_name_allowed` permits; otherwise the
  anonymized descriptor. This brief is internal, so it may hold the name — but every sentence that
  will travel into an artifact is written so it survives anonymization.
- **What the owner has not yet confirmed says so**: anything the research generated and they have not
  accepted is marked `(awaiting your confirmation)`. The brief is allowed to contain material they have
  not ruled on; it is not allowed to look as though they have.
- **Register**: structured output by default — tables, numbered lists, bold captions with tight
  text. Prose only where structure cannot carry the meaning. Direct; density beats length; no
  hedging, no padding, no filler headers.

---

## 4. What follows the brief

The user answers the research questions put to them under the heading "Your call on what the
research found" (`generalization-method.md` §5) and picks an option.
Only then does the spec skill begin component sign-off — problem ↔ solution, one-liner, target ICP,
name, then the rest, per `signoff-flow.md`. If they send the research back instead, the brief is
**rewritten in place** to current truth, never appended to.

Every sign-off card cites this brief as its grounding by the section's printed title — (the
research summary, "The industries"), (the research summary, "What is specific to the customer") —
never by a § number, so the brief is the standing evidence base for the whole spec, not a
throwaway.

---

## 5. Word budget summary

| Section | Budget | Hard rule |
|---|---|---|
| Header | 6 lines | — |
| 1 The answer | ≤ 120 w | Recommendation and the one thing that could sink it, both present |
| 2 Generalized workflow | ~200 w | ≤ 12 steps; every step has a failure path |
| 3 Delivered-case divergence | ≤ 150 w | The one-line divergence is present verbatim for the spec |
| 4 Verticals | ~250 w | ≥ 3 rows, each with its entity difference |
| 5 Vendor landscape and gaps | ≤ 250 w | 3–5 vendors in three classes; every gap has a recommendation |
| 6 Failure paths and absences | ≤ 120 w | Empty list is stated, not omitted |
| 7 Feature specificity | ~150 w | Flags the no-○ warning when it applies |
| 8 Candidate options | ≤ 120 w × 3 | One recommendation with its reason |
| 9 Open questions | ≤ 120 w | Each names what it blocks |
| 10 Sources | as needed | Tiered; plus "searched and not found" and "unverified" |

Total ≈ 1,600 words plus tables — a 10-minute read.

---

## 6. Provenance

- **Structure and altitude**: Alex's own packaging sequence — candidate table → self-challenge from
  several angles → red team → *"TLDR of the differences"* → risks column → compress (Lakehouse
  packaging session, 2026-08-21 → 08-25) *(internal)*; and `docs/PLAN.md` §3.2, which specifies
  "a very structured research TLDR with labeled claims and source tiers".
- **Epistemic and format rules**: `research-standards.md` — labels, source tiers, named specifics,
  explicit gaps, no force-filled frameworks, answer first.
- **Section content**: `generalization-method.md` (tests T1–T9, steps 1–12) and
  `shared/schema/pack-spec.md` (the keys each section feeds).
- **Budget and compression rules**: Alex's page-budget and condensation instructions, 2026-08-21
  and 2026-09-08 *(internal)*.
- **Options-with-a-recommendation**, the three-class competitor split, and the "no theoretically-can-
  also-do-this" rule: Lakehouse packaging session, 2026-08-21 *(internal)*.
