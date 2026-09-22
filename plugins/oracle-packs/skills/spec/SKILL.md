---
name: spec
description: Turn one delivered Oracle + NVIDIA AI engagement into a generalized accelerator-pack specification — interactively. Locates the raw inputs, asks the predefined intake questions (skipping what the context already answers), runs the generalization research (domain workflow across industries, vendor and competitor taxonomies, vertical differentiation, failure paths, feature specificity), proposes name · one-liner · problem↔solution options with a structured research TLDR, then signs off the 12 shared components one at a time in the fixed order (problem↔solution → one-liner → target ICP → name → verticals → capabilities → workflow → architecture → Oracle products → KPIs → packages) and confirms the whole brief before any artifact is built. Use on /oracle-packs:spec, "package this case", "create a pack spec for X", "generalize the <customer> PoC into a pack", or before any pack artifact when no confirmed pack-spec.yaml exists.
disable-model-invocation: false
user-invocable: true
---

# /oracle-packs:spec — the pack spec, signed off component by component

> **Paths.** `shared/...` means `${CLAUDE_PLUGIN_ROOT}/shared/...` (each plugin carries a synced copy of the repo's `shared/` folder); `tools/...`, `assets/...` and `references/...` without a prefix are relative to this skill's own folder. In a plain-copy install the plugin folder sits at `.claude/skills/<plugin>/` and `${CLAUDE_PLUGIN_ROOT}` resolves to it.


You produce **one file the other skills trust**: `packs/<slug>/pack-spec.yaml`, valid against `shared/schema/pack-spec.md`, with every component confirmed by the user through the question widget. Nothing in it is invented: every value carries a source, and a gap is a question, not a guess.

## 0. Before you start

1. Read, in this order: `shared/references/engagement-context.md`, `shared/references/pack-anatomy.md`, `shared/references/naming-and-clearance.md`, `shared/references/packaging-coaching-rules.md`, `shared/references/review-loop.md`, `shared/references/talking-to-the-owner.md` — every message, question and option the owner sees passes its reader's test — and this skill's `references/generalization-method.md`, `references/research-brief-format.md`, `references/intake-questions.md`, `references/signoff-flow.md`. Load `shared/data/oracle-products.yaml` (the only allowed product names) and `shared/data/roadmap-items.csv` (the only allowed roadmap ids).
2. Working folder: `packs/<slug>/` under the directory the user names (default: the current working directory). If `packs/<slug>/pack-spec.yaml` already exists, read it and resume at the first unconfirmed component; say so.
3. Model split (as roles): the research fan-out, source extraction, catalog and roadmap lookups run on the mechanical model (Opus in the owner's setup); the research synthesis, every TLDR, every option and every component proposal, and the final consistency pass run on the strongest model available (Fable). Name the split once in your first status line. Never fan out more than four research agents at once, and have each write its output file within minutes so silence is visible (check the file's modification time, and take the work over when nothing moves).

## 1. Intake — ask, do not assume

**Show the map first.** Before the first question, one short message with the six-stage map from `shared/references/talking-to-the-owner.md` ("Where we are"), in the owner's words, with the number of questions each stage will actually ask after skipping. From then on every widget title carries `<Stage> · n of N · <question name>`, and every stage ends with a one-line "done, next" message.

Run the question list in `references/intake-questions.md` — stage 1, "Before we start", **all three blocks before any research runs**, titled `Before we start · n of N · <question name>` — one widget at a time, in order: **Block A** (locate the raw inputs, name the delivered case, find prior packaging work), **Block B** (roadmap item, verticals, artifacts wanted, internal contact), **Block C** (clearance of the customer name and logo per channel, cleared figures, PoV duration and price constraints, internal-only facts). Skip a question only when the answer is already in the context, and say where you found it. Write answers to `packs/<slug>/intake.md` as you go.

Inventory the inputs: list every file with what it is (SoW, deck, recording, feature list, transcript, note), extract text where you can (python-docx, python-pptx, `pdftotext`, the transcript itself), and write `packs/<slug>/inventory.md`. A file you cannot open is reported as unreadable, never treated as absent.

## 2. Generalization research — the step that decides everything

Follow `references/generalization-method.md` exactly. In short:

1. **Inventory the delivered case** as a step table: steps, actors, systems, data, human-in-the-loop points; per step the three lenses (what the Oracle/NVIDIA pack provided · what we implemented · what stays custom).
2. **Domain workflow across industries**: how this job is generally done, canonical step names, where industries differ, how the delivered case differs from the general shape.
3. **Vendor and competitor taxonomy study**: how three to five vendors structure capabilities for this job; direct competitors, indirect substitutes, same-vendor overlaps; the gap check — which steps we miss or over-split.
4. **Vertical differentiation**: at least three scenarios × every step, with a "what matters here" cell; widen the prompt deliberately; then adjudicate real differences vs filler (that adjudication is a user question, not your call alone).
5. **Failure path per step**; absence is a finding and becomes an out-of-scope line.
6. **Feature specificity**: tag every feature customer / engine / use case / industry; reusable vs custom.
7. **Placement**: the roadmap item (from the extract, by id), candidate Oracle products from the catalog with required / optional roles, KPI candidates with formulas and baselines.
8. **Red-team** the whole set: is this product really the answer; is the PoV feasible in 4–8 weeks; what is AI slop; remove or defend each item.

Fan the sub-tasks 2–6 out to research agents with the prompts in the method file; each writes `packs/<slug>/research/<topic>.md`. Synthesize the **research brief** yourself in the exact format of `references/research-brief-format.md` (answer first, labeled claims, source tiers, ≤ 10 minutes to read) to `packs/<slug>/research-brief.md`. The "general enough but not too general" test in the method file must pass before you go on; if it does not, say which criterion fails and what extra research would fix it.

This is stage 2: report progress in plain words (which research is running, what it has produced so far), then present the research summary. Then stage 3, **Your call on the research** — the questions in section 5 of the method file, in widget calls of their own, titled `Your call on the research · n of N · <question name>` (N = the questions actually asked after skipping) — closed with the one-line "done, next" message.

## 3. Options — one to three triads

From the brief, propose **one to three candidate triads** (name · one-liner · problem · solution). Present the research TLDR first, then the triads **as one comparison table in chat** — one column per triad, headed `<letter> · <Name>`, one row per attribute in this order: One-liner · Problem · Solution · Sells best in · Bets on · Leaves out · Risk — so the same row reads across the options; never as consecutive paragraphs. Every triad the user can pick is a column (a blend of two triads is offered only when it is written out as its own column). Under the table, one line: the recommendation with its reason, and the alternative the user is most likely to prefer. Then one widget — stage 4, titled `The pack's story · Which name, one-liner, problem and solution we build on` — with **only this question**: one option per column, labelled `<letter> · <Name>`, with a one-line description in plain business words (what it bets on, what it gives up — no research codes, no status-glyph counts, no restatement of the table), plus "Research further" (free text: what to research). The adjudication questions from the method file are asked before this step, never inside this widget. Loop until the user picks. Log the choice in `packs/<slug>/decisions.md`.

## 4. Sign-off — one component at a time, fixed order

Follow `references/signoff-flow.md`. This is stage 5 — every card and its widget titled `Confirm the pack · n of 11 · <the part, in the owner's words>` — and the order is fixed by the owner: **problem ↔ solution → one-liner → target ICP → name**, then verticals and their framings → capabilities, features and customization scope → workflow architecture with human-in-the-loop and failure paths → high-level architecture → required and optional Oracle products (catalog ids only) → key performance metrics (one set) → service-package table (PoV Jumpstart / Integration / Scaling: per-capability handling, timeframe, cost).

For every component: a very brief non-technical TLDR of the proposal, its grounding (source lines from the brief or the inputs), then the widget with the proposal as the first option and two or three real alternatives. When the user answers with free text, apply it verbatim where it is a value and re-propose where it is a direction. Write the confirmed value into `pack-spec.yaml` immediately, with `source: user:<date>`.

Hard rules while signing off:
- If something essential is missing (no figure, no price, no vertical evidence, no delivered scope), **ask** — never make it up. A tier without a price is `status: tbd` with a footnote; a metric without a cleared figure prints "results to follow".
- PoV duration: propose within 4–8 weeks; above 8 requires a written justification; above 10 you push back with the reasons (scope too wide for a proof, integration work leaking into the PoV, unclear success metric) and offer a narrower PoV.
- One metric set per pack. If the inputs carry two sets, put both in front of the user and confirm one; never keep both.
- Names: Oracle and NVIDIA products only by catalog id; the pack name is one plain string, with channel variants derived per `naming-and-clearance.md`; no customer name inside any component text.
- Integration claims state their tier (e.g. "file export / import in the PoV, API write-back in Integration").
- Anything the user defers goes to `open_questions`; an artifact that depends on an open question prints nothing for it.

## 5. The brief — confirm everything, then hand over

Render the whole pack brief **as one table** — a row per part in the fixed order; columns: the part, in the owner's words · what we decided · status (confirmed by you / proposed, awaiting your OK / open). The rows: the name and how it is written for each audience · one-liner (full / short) · problem ↔ solution · who buys it, at what kind of company · the industries · capabilities per area with the available / partial / roadmap counts · workflow steps · architecture layers · Oracle products required / optional · the metrics and who they are attributed to · the three packages with durations and prices · who to contact · what may be named where · what is still open. Ask one widget, titled `The whole brief · Confirm, change or stop` (stage 6), with **exactly three options and no others**: confirm as is (Recommended) · make changes (free text) · stop here. Never add flow choices here ("build only the feature list", "confirm but stop before building", "anything else to change?"): which artifacts get built was settled in stage 1, and what happens after confirmation is fixed. Apply changes and re-render until confirmed. Then set `meta.status: confirmed` and run `python3 shared/tools/lint_spec.py packs/<slug>/pack-spec.yaml`, both silently, and report the result in one plain line ("the automatic checks passed", or what one of them found and what it means for the pack). Then hand over **at once, in the same session**: one line on what happens next — the artifacts the owner chose in stage 1, by name and in order, each reviewed before the next — and invoke `/oracle-packs:build packs/<slug>/pack-spec.yaml` through the Skill tool. Do not ask whether or how to proceed, and never build artifacts yourself inside this skill.

## 6. Fast path

When the user asks for one thing ("re-propose the one-liner", "add a vertical", "change the PoV price"), skip to that component, re-run only the research it needs, re-confirm it, re-lint, and stop. Never re-run the whole flow for one field.

## 7. Definition of done and self-check

Done = `pack-spec.yaml` confirmed and lint-clean; `research-brief.md`, `intake.md`, `inventory.md`, `decisions.md` in the pack folder; the closing message lists the open questions and the artifacts to build next. Before you close, check:

- [ ] Every component has a `source`; the first four carry `user:` sources.
- [ ] No customer name in any component text; clearance flags set per channel.
- [ ] Products are catalog ids; the roadmap id exists in the extract; the extract version is recorded in `meta.generated_with`.
- [ ] One metric set; every figure has a status and a caveat; attribution rule present.
- [ ] PoV within the cap or justified; tier names are PoV Jumpstart / Integration / Scaling.
- [ ] The research brief passes the "general enough but not too general" test and names its gaps.
- [ ] You asked instead of inventing wherever the inputs were silent.
- [ ] Every message, question, option and table the owner saw passes the reader's test: no method codes, no file or key names, no packaging vocabulary as vocabulary, reasons instead of rule names.
- [ ] The map was shown first; every question carried its stage, number and name; every stage ended with a "done, next" line; no question was asked outside the map, and every question stood alone.
