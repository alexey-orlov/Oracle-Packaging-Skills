# Sign-off flow — how every proposal is put to the user

The owner's rules (2026-09-18): each suggestion comes with a very brief, non-technical, exec business-level TLDR and its grounding, then a question widget to decide; when something essential is missing, ask rather than make up; after all components are settled, show the whole brief for last-minute changes before building.

## The proposal card (one per component, in chat, before the widget)

```
<Component name> — proposal
TLDR: <two or three sentences a seller would understand; the recommendation and why>
Grounded in: <bullet list of 2–4 findings, each with its source: research-brief §x, <input file>, user:<date>>
Trade-off: <one line: what this choice gives up>
Alternatives considered: <one line each, only real ones>
```

Then one widget. The recommended option comes first and is labelled "(Recommended)". Two to four options, each with a one-line description; the free-text "Other" is always there and its answer is applied verbatim when it is a value.

## The comparison card (when the options are alternatives of one kind)

When a decision is a choice between alternatives of the same kind — candidate triads, names, metric sets, tier ladders, vertical framings — the card is **one table**: a column per option headed `<letter> · <name>`, a row per attribute (for triads: One-liner · Problem · Solution · Sells best in · Bets on · Leaves out · Risk), so the same row reads across the options. Never consecutive paragraphs, one per option. Every option the widget offers is a column; nothing pickable is left out of the table. Under it, one line: the recommendation with its reason, and the most likely alternative. The widget then carries only the pick: labels `<letter> · <name>`, one plain business-language line each (no research codes such as P2 or T4, no status-glyph counts, no restatement of the table), recommended first and labelled.

## Fixed order and what each card must contain

| # | Component | The card must show | Ask when missing |
|---|---|---|---|
| 1 | Problem ↔ solution | The reader's problem in the reader's words; the solution as a job reframe (what the app does for them, not the technology); the delivered case's divergence in one line | Which pain is primary; whether the reframe is true for the delivered case |
| 2 | One-liner | Full form and rep-sayable short form; the job and the outcome; no packaging vocabulary; banned-word check result | Whether the outcome claim is cleared |
| 3 | Target ICP | One line: who, at what kind of company, with what pain; buyer roles; qualifying signals; disqualifiers | Company size band, the platform prerequisite |
| 4 | Name | One plain name; the channel variants derived by rule; conflicts with existing packs or products | Nothing is invented here: if the user has a working name, propose to keep it |
| 5 | Verticals | Three or more, each with its own problem ↔ solution line, "what matters here", status (proven / plausible / roadmap); the label set used | Which are first and second priority; which claims are cleared |
| 6 | Capabilities | Area > Category > Feature table with status ● ◐ ○, customization scope per area, specificity tags; counts per area; the reusable-vs-custom summary | The status of any feature the inputs do not settle |
| 7 | Workflow | Inputs → steps (actor, human-in-the-loop, failure path) → outputs; the per-vertical differences that survived adjudication | Which failure paths are in scope |
| 8 | Architecture | Inputs → stack layers with vendor ladder → outputs | Nothing; derived from 6 and 7 plus the catalog |
| 9 | Oracle products | Required (built on / relies on) and optional (could logically be a source or destination), by catalog id, with the "why"; integration statement per tier | A product not in the catalog → catalog change request, not free text |
| 10 | KPIs | One metric set: name, formula, baseline, figure, figure status, attribution by channel, caveat | Any figure without a cleared source |
| 11 | Packages | Three tiers named PoV Jumpstart / Integration / Scaling with S/M/L tags; durations (PoV 4–8 weeks, cap 10), prices with status, what you get, in/out scope; the per-capability handling matrix; the partner's "why it sells" lines | Any price; any duration above 8 weeks |

## Rules of engagement

- **Ask, do not invent.** A missing essential → a widget whose options are the honest states ("tbd with footnote", "results to follow", "not in scope"), never a plausible number.
- **Respect the owner's answer.** When the user picks an alternative or types free text, that is the value; do not re-argue it. When the free text is a direction ("more concrete", "shorter"), re-propose once.
- **Contradictions surface before the widget.** If two inputs disagree (two prices, two durations, two metric sets), the card shows both with sources and the widget asks which is right.
- **Write as you go.** Each confirmed value lands in `pack-spec.yaml` and `decisions.md` before the next card.
- **One decision per widget call.** Never batch components, and never attach a second question (an adjudication, a clarification, a research follow-up) to a decision widget — it gets its own card after this decision is recorded. The order is the owner's.

## The brief (after component 11)

One screen, in this order: name + channel variants · one-liner (full / short) · problem ↔ solution · ICP · verticals (one line each) · capability areas with ● ◐ ○ counts · workflow steps (one line each) · architecture layers · products required / optional · the metric set with attribution rule · tiers with duration and price status · contacts per channel · clearance flags · open questions. Then one widget: **Confirm as is · Make changes (free text) · Stop here**. On "Make changes", apply, re-render, ask again. On "Confirm", set `meta.status: confirmed`, lint, and announce the build order and the review pause after each artifact.
