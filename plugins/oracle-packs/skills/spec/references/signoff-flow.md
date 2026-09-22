# Sign-off flow — how every proposal is put to the user

The owner's rules (2026-09-18): each suggestion comes with a very brief, non-technical, exec business-level TLDR and its grounding, then a question widget to decide; when something essential is missing, ask rather than make up; after all components are settled, show the whole brief for last-minute changes before building.

Everything in this file that the owner reads — card, table, question, option, the brief — is written to the reader's test in `shared/references/talking-to-the-owner.md`: the owner knows the delivered engagement and the pack, and nothing about this method. Instructions addressed to you may name files and keys freely; the text you show them may not.

## The proposal card (one per component, in chat, before the widget)

```
<The part of the pack, in the owner's words> — proposal
TLDR: <two or three sentences a seller would understand; the recommendation and why>
Grounded in: <bullet list of 2–4 findings, each naming where it came from the way the owner would name it: (the research summary, "Competitors") · (the statement of work, p. 4) · (your answer, 22 Sep)>
Trade-off: <one line: what this choice gives up>
Alternatives considered: <one line each, only real ones>
```

Then one widget. Its title carries the place and the decision in plain words — `Confirm the pack · 4 of 11 · The name`, `Confirm the pack · 5 of 11 · The industries we lead with` — never this step's internal name. The recommended option comes first and is labelled "(Recommended)". Two to four options, each with a one-line description in the same plain words; the free-text "Other" is always there and its answer is applied verbatim when it is a value.

## The comparison card (when the options are alternatives of one kind)

When a decision is a choice between alternatives of the same kind — candidate triads, names, metric sets, tier ladders, vertical framings — the card is **one table**: a column per option headed `<letter> · <name>`, a row per attribute (for triads: One-liner · Problem · Solution · Sells best in · Bets on · Leaves out · Risk), so the same row reads across the options. Never consecutive paragraphs, one per option. Every option the widget offers is a column; nothing pickable is left out of the table. Under it, one line: the recommendation with its reason, and the most likely alternative. The widget then carries only the pick: labels `<letter> · <name>`, one plain business-language line each — what it bets on and what it gives up, never a research step's id, a test's id, a file or key name, or a count of ● ◐ ○ rows, and never a restatement of the table — recommended first and labelled.

## Fixed order and what each card must contain

The numbers below are the running order the owner sees in every title (`Confirm the pack · n of 11 · …`); the part names are theirs, not the method's. Each card names the part of the pack the way they would: the problem and the solution · the one-liner · who buys it · the name · the industries · the capabilities · the workflow · the architecture · the Oracle products · the metrics · the packages. Never "component 4", never "sign-off step 4".

| # | Component | The card must show | Ask when missing |
|---|---|---|---|
| 1 | Problem ↔ solution | The reader's problem in the reader's words — a named role and a concrete situation with the nouns on their desk, a sentence that person could say about their own week (the tangibility test, `shared/references/pack-anatomy.md` §1: "commercial teams work out what a development means for their accounts" fails; "account managers can't keep up with the market signals, internal insights and updates in their accounts" passes); the solution as a job reframe (what the app does for them, not the technology); one line on where the pack differs from what we built for the customer | Which pain is primary; whether the reframe is true for what we delivered |
| 2 | One-liner | Full form and rep-sayable short form; the job and the outcome; no packaging vocabulary; and, in one plain line, whether any word we keep out of customer copy turned up in it | Whether the outcome claim is cleared |
| 3 | Target ICP | One line: who, at what kind of company, with what pain; buyer roles; qualifying signals; disqualifiers | Company size band, the platform prerequisite |
| 4 | Name | One plain name; how it is written for each audience, derived by rule; conflicts with existing packs or products | Nothing is invented here: if the user has a working name, propose to keep it |
| 5 | Verticals | Three or more industries, each with its own problem ↔ solution line, "what matters here", and where it stands — proven with a customer / plausible / not built yet; and the words we use to name them | Which are first and second priority; which claims are cleared |
| 6 | Capabilities | Area > Category > Feature table with a legend for ● ◐ ○ the first time it appears, what is standardly customized per area, and per area how many are available, partial and on the roadmap; plus which features are reusable as they stand and which are built per customer (the specificity tags, said in those words) | The status of any feature the inputs do not settle |
| 7 | Workflow | Inputs → 5–7 steps (actor, human-in-the-loop, failure path), grouped at the buyer's checkpoints, mechanics inside a step and never as steps → outputs; the per-industry differences you confirmed as real | Which failure paths are in scope |
| 8 | Architecture | Inputs → the stack layers, each saying whose technology it runs on → outputs | Nothing; derived from 6 and 7 plus the Oracle product list |
| 9 | Oracle products | Required (built on / relies on) and optional (could logically be a source or destination), by catalog id, with the "why"; and, for each package, what the integration actually is | A product not in the catalog → catalog change request, not free text |
| 10 | KPIs | One metric set: name, formula, baseline, figure, what kind of figure it is (delivered result, proof result, target, modelled), who it is attributed to for each audience, and the caveat printed with it | Any figure without a cleared source |
| 11 | Packages | Three tiers named PoV Jumpstart / Integration / Scaling with S/M/L tags; durations (PoV 4–8 weeks, cap 10), prices and whether each is settled, what you get, what is in and out of scope; what each capability gets in each package; the partner's "why it sells" lines | Any price; any duration above 8 weeks |

## Rules of engagement

- **Ask, do not invent.** A missing essential → a widget whose options are the honest states, each written as what it does to the artifact: "leave the price out and mark it 'to be confirmed'" (`status: tbd` with a footnote) · "print 'results to follow' instead of a figure" · "say it is not in scope". Never a plausible number.
- **Respect the owner's answer.** When the user picks an alternative or types free text, that is the value; do not re-argue it. When the free text is a direction ("more concrete", "shorter"), re-propose once.
- **Contradictions surface before the widget.** If two inputs disagree (two prices, two durations, two metric sets), the card shows both with sources and the widget asks which is right.
- **Write as you go.** Each confirmed value lands in `pack-spec.yaml` and `decisions.md` before the next card.
- **One decision per widget call.** Never batch components, and never attach a second question (an adjudication, a clarification, a research follow-up) to a decision widget — it gets its own card after this decision is recorded. The order is the owner's.

## The brief (after component 11)

**One table**, a row per part in the fixed order, with three columns — the part, in the owner's words · what we decided · status (confirmed by you / proposed, awaiting your OK / open). The rows: the name, and how it is written for each audience · one-liner (full / short) · problem ↔ solution · who buys it, at what kind of company · industries (one line each) · capabilities per area, with the available / partial / roadmap counts · workflow steps (one line each) · architecture layers · Oracle products, required and optional · the metrics, and whose result they are called on each audience · the three packages with their duration and whether the price is settled · who to contact, per audience · what may be named where · what is still open. Then one widget, titled `The whole brief · Confirm, change or stop`, with **exactly these three options**: **Confirm as is (Recommended) · Make changes (free text) · Stop here** — no flow choices ("build only X", "confirm but stop before building"), no "anything else?": the artifacts were chosen in stage 1 and the flow after confirmation is fixed. On "Make changes", apply, re-render, ask again. On "Confirm", set `meta.status: confirmed` and run the linter — both silently. What the owner is told is plain: the brief is settled, the automatic checks passed (or, in one plain line, what one of them found), and what gets built next — the artifacts they chose, by name, in order, with a pause for their review after each — and the build starts at once (`/oracle-packs:build`), without asking whether or how to proceed.
