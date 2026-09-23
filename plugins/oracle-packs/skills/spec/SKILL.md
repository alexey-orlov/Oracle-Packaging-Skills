---
name: spec
description: Turn one delivered Oracle + NVIDIA AI engagement into a generalized accelerator-pack specification — interactively, in six stages and at most twelve questions. Locates the raw inputs, asks only what the documents cannot answer, runs the generalization research, puts two or three complete pack stories (name, one-liner, problem, solution, buyer) side by side as one comparison table, drafts the rest of the pack in a single pass with a fresh-context reviewer per part, then confirms the whole brief as one table and hands over to the build. Use on /oracle-packs:spec, "package this case", "create a pack spec for X", "generalize the <customer> PoC into a pack", or before any pack artifact when no confirmed pack-spec.yaml exists.
disable-model-invocation: false
user-invocable: true
---

# /oracle-packs:spec — the pack brief, in six stages

> **Paths.** `shared/...` means `${CLAUDE_PLUGIN_ROOT}/shared/...` (each plugin carries a synced copy of the bundle's `shared/`); `references/...` and `tools/...` are this skill's own folder.

**Load only what the step needs.** `references/cards/manifest.yaml` lists, per step, exactly which files that step reads. Read those and nothing else — never the whole folder, never a card for a step you are not on, never a long reference a card already points to. A card's checks are the specification, not prose to paraphrase. Background, only if a term is unfamiliar: `shared/references/engagement-context.md` and `pack-anatomy.md`.

You produce one file the other skills trust: `packs/<slug>/pack-spec.yaml`, valid against `shared/schema/pack-spec.md`. Nothing in it is invented — every value carries a source, and a gap is a question, not a guess.

**At most 12 questions in the whole run**, and fewer is better. Say the number in the map.

## 0. Before you start

1. Working folder `packs/<slug>/`, under the directory the user names (default: the working directory). If a `pack-spec.yaml` is already there, read it, resume at the first unsettled part, and say so.
2. Load `shared/data/oracle-products.yaml` (the only allowed product names) and `shared/data/roadmap-items.csv` (the only allowed roadmap ids) at the step that needs them, not before.
3. Roles: research agents, extraction and lookups on the mechanical model; the synthesis, the story candidates and the final consistency pass on the strongest available. Name the split once. Never more than four research agents at once.
4. **Show the map first** — one short message: the six stages below in the owner's words, how many questions each will actually ask after skipping, and the total. Every widget title then carries `<Stage> · n of N · <question name>`, and every stage ends with one line: what is done, what is next.

## 1. Before we start

Cards: `intake-a`, `intake-b`, `intake-c`. Inventory the inputs first — every file with what it is, text extracted where you can (python-docx, python-pptx, `pdftotext`, the transcript itself), written to `packs/<slug>/inventory.md`; a file you cannot open is reported as unreadable, never treated as absent. Then ask only what the inventory did not answer, **all of it in one or two widget calls**. Propose before you ask: state what you found and where, and let the owner correct it. Answers go to `packs/<slug>/intake.md`.

## 2. Research

Card: `research`. No questions here. Fan the five topics out to agents, each reading its own prompt from `references/generalization-method.md` §4 — that file never enters this conversation. Report progress in plain words, check each agent's output file is actually growing, then read `references/research-brief-format.md` and synthesize `packs/<slug>/research-brief.md` yourself, opening it beside the conversation before the next question.

## 3. Your call on the research

Card: `research-review`. At most four questions, **one widget call**, only what the research genuinely raised. Where the research is confident and the owner has no stake in the answer, state it and move on.

## 4. The pack's story

Card: `story`. Two or three complete candidates — name, one-liner, problem, solution, who buys it — as **one comparison table**, every cell grounded in the research summary or the inputs, then one widget carrying only the pick. Free text that is a value is applied as given; a direction is re-proposed once. Log the choice in `packs/<slug>/decisions.md`.

## 5. Everything else, drafted in one pass

Cards, one per part as you write that part: `industries`, `capabilities`, `workflow`, `architecture`, `oracle-products`, `metrics`, `packages`. Draft all seven from the story, the research summary and each part's card, **asking nothing**.

Then the **reviewer pass**. For each part, one fresh-context subagent that receives only the drafted part, the inputs it was drawn from and that part's card — never this conversation — and returns pass or fail per check with a one-line reason. Fix every fail; at most two rounds. What still fails goes to the owner as an open item in plain words, and into `open_questions`.

While drafting: when something essential is missing, ask rather than invent — a package without a price is marked to be confirmed with a footnote, a metric without a cleared figure prints "results to follow". Oracle and NVIDIA products by catalog id only. No customer name in any component text. Every integration claim states its tier. Each settled value is written into `pack-spec.yaml` immediately, with its source.

## 6. The whole brief

Card: `brief`. One table, one widget — exactly confirm · change · stop. Then set the status, run `python3 shared/tools/lint_spec.py packs/<slug>/pack-spec.yaml` silently, report it in one plain line, and invoke `/oracle-packs:build packs/<slug>/pack-spec.yaml` at once, in the same session.

## Showing it to the owner

Everything the owner reviews is opened beside the conversation *before* the question, so they answer while looking at the thing (`shared/references/review-loop.md` §3): a text file in the Files pane (`mcp__ccd_view__show_pane`, pane `file`), a render in the side panel. Internal pack material is never a claude.ai artifact. In a plain terminal, print the path and a text rendering, and say so. Here: the research summary before stage 3, `pack-spec.yaml` before the confirm question.

## Fast path

When the user asks for one thing ("re-propose the one-liner", "add an industry", "change the price"), load that part's card only, redo it, re-lint, and stop. Never re-run the flow for one field.

## Done, and the self-check

Done = `pack-spec.yaml` settled and lint-clean; `research-brief.md`, `intake.md`, `inventory.md`, `decisions.md` in the pack folder; the closing message lists the open items and the artifacts to build next. Before you close:

- [ ] Every part has a source; the story's parts carry `user:` sources.
- [ ] No customer name in any component text; clearance set per audience.
- [ ] Products are catalog ids; the roadmap id exists; the extract version is recorded.
- [ ] One metric set; every figure has its kind and caveat; the proof is within its cap or justified.
- [ ] Every part passed its card's checks, through the reviewer, and every remaining fail reached the owner.
- [ ] Twelve questions or fewer, each in its stage, each standing alone.
- [ ] Every message, question, option and table passed the reader's test in `references/cards/owner-language.md`.
- [ ] Everything the owner reviewed was open beside the conversation before the question.
