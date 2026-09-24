---
name: spec
description: Turn one delivered Oracle + NVIDIA AI engagement into a generalized accelerator-pack specification — interactively, in six stages and at most twelve questions. Locates the raw inputs, asks only what the documents cannot answer, runs the generalization research, puts two or three complete pack stories (name, one-liner, problem, solution, buyer) side by side as one comparison table, drafts the rest in one pass with a fresh-context reviewer per part, then confirms the whole brief as one table and hands over to the build. Use on /oracle-packs:spec, "package this case", "create a pack spec for X", "generalize the <customer> PoC into a pack", or before any pack artifact when no confirmed pack-spec.md exists.
disable-model-invocation: false
user-invocable: true
---

# /oracle-packs:spec — the pack brief, in six stages

> **Paths.** `shared/...` means `${CLAUDE_PLUGIN_ROOT}/shared/...` (each plugin carries a synced copy of the bundle's `shared/`); `references/...` and `tools/...` are this skill's own folder.

**Load only what the step needs.** `references/cards/manifest.yaml` lists, per step, exactly which files that step reads. Read those and nothing else — never the whole folder, never a card for a step you are not on, never a long reference a card already points to. A card's checks are the specification, not prose to paraphrase. Background, only if a term is unfamiliar: `shared/references/engagement-context.md` and `pack-anatomy.md`.

You produce one file the other skills trust: `packs/<slug>/pack-spec.md`, valid against `shared/schema/pack-spec.md`. Nothing in it is invented — every value carries a source, and a gap is a question, not a guess. Values go in only through `shared/tools/py shared/tools/packspec.py set <spec> <key.path> <value> --source <src>` (the first call creates the file; a list or record is JSON), never by editing it.

**At most 12 questions in the whole run**, and fewer is better. Say the number in the map.

## 0. Before you start

1. `shared/tools/py shared/tools/pack_paths.py <slug> --create` prints the repo and `<work>`. The spec and its pictures live in the repo's `packs/<slug>/`; everything else goes to `<work>/`, never the repo. `git -C <repo> pull --ff-only` before reading or writing the spec; a pull that cannot run is deferred and retried, never skipped silently. An existing `pack-spec.md`: read it, resume at the first unsettled part, say so.
2. Load `shared/data/oracle-products.yaml` (the only allowed product names) and `shared/data/roadmap-items.csv` (the only allowed roadmap ids) at the step that needs them, not before.
3. Roles: research agents, extraction and lookups on the mechanical model; the synthesis, the story candidates and the final consistency pass on the strongest available. Name the split once. Never more than four research agents at once. Every subagent follows `shared/references/running-agents.md`.
4. **Show the map first** — one short message: the six stages below in the owner's words, how many questions each will actually ask after skipping, and the total. Every widget title then carries `<Stage> · n of N · <question name>`, and every stage ends with one line: what is done, what is next.

## 1. Before we start

Cards: `intake-a`, `intake-b`, `intake-c`. Inventory the inputs first — every file with what it is, text extracted where you can (python-docx, python-pptx, `pdftotext`), written to `<work>/inventory.md`. Then ask only what the inventory did not answer, **all of it in one or two widget calls**. Propose before you ask: state what you found and where, and let the owner correct it. Answers go to `<work>/intake.md`.

## 2. Research

Card: `research`. No questions here. Fan the five topics out to agents, each reading its own prompt from `references/generalization-method.md` §4 — that file never enters this conversation. Report progress in plain words, then read `references/research-brief-format.md` and synthesize `<work>/research-brief.md` yourself, opening it beside the conversation before the next question.

## 3. Your call on the research

Card: `research-review`. At most four questions, **one widget call**, only what the research genuinely raised.

## 4. The pack's story

Card: `story`. Two or three complete candidates — name, one-liner, problem, solution, who buys it — as **one comparison table**, every cell grounded in the research summary or the inputs, then one widget carrying only the pick. Free text that is a value is applied as given; a direction is re-proposed once. Log the choice in `<work>/decisions.md`.

## 5. Everything else, drafted in one pass

Cards, one per part as you write that part: `industries`, `capabilities`, `workflow`, `architecture`, `oracle-products`, `metrics`, `packages`, and `proof`, the delivered case behind the deck's proof slide. Draft all eight from the story, the research summary and each part's card, **asking nothing**.

Then the **reviewer pass**. For each part, one fresh-context subagent that receives only the drafted part, the inputs it was drawn from and that part's card, and returns pass or fail per check with a one-line reason. Fix every fail; at most two rounds. What still fails goes to the owner as an open item in plain words, and into `open_questions`.

While drafting: when something essential is missing, ask rather than invent — a package without a price is marked to be confirmed with a footnote, a metric without a cleared figure prints "results to follow". Oracle and NVIDIA products by catalog id only. No customer name in any component text. Every integration claim states its tier. Each settled value is written immediately, with its source.

## 6. The whole brief

Cards: `brief`, `save`. One table, one widget — exactly confirm · change · stop. Then set the status, run `shared/tools/py shared/tools/lint_spec.py packs/<slug>/pack-spec.md` silently, save it, report it in one plain line, and invoke `/oracle-packs:build packs/<slug>/pack-spec.md` at once, in the same session.

## Showing it to the owner

Everything the owner reviews is opened beside the conversation *before* the question, so they answer while looking at the thing (`shared/references/review-loop.md` §3): a text file in the Files pane (`mcp__ccd_view__show_pane`, pane `file`), a render in the side panel. Internal pack material is never a claude.ai artifact. In a plain terminal, print the path and a text rendering, and say so. Here: the research summary before stage 3; `pack-spec.md` at the brief, before the confirm question.

## Fast path

When the user asks for one thing ("re-propose the one-liner", "add an industry", "change the price"), load that part's card only, redo it, re-lint, save it (card `save`), and stop. Never re-run the flow for one field.

## Done, and the self-check

Done = `pack-spec.md` settled, lint-clean and pushed from the repo's `packs/<slug>/`; `research-brief.md`, `intake.md`, `inventory.md`, `decisions.md` in `<work>/`; the closing message lists the open items and the artifacts to build next. Before you close:

- [ ] Every part has a source; the story's parts carry `user:` sources.
- [ ] No customer name in any component text; clearance set per audience.
- [ ] Products are catalog ids; the roadmap id exists; the extract version is recorded.
- [ ] One metric set; every figure has its kind and caveat; the proof is within its cap or justified.
- [ ] Every part passed its card's checks, through the reviewer, and every remaining fail reached the owner.
- [ ] Twelve questions or fewer, each in its stage, each standing alone.
- [ ] Every message, question, option and table passed the reader's test in `references/cards/owner-language.md`.
- [ ] Everything the owner reviewed was open beside the conversation before the question.
