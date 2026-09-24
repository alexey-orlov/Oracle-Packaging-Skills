---
name: demo
description: Build the accelerator pack's interactive walkthrough (a static, self-contained guided demo) from a confirmed pack spec and the sources the user supplies — the real product's flow and screens, generalized to what the pack sells, on synthetic data, leading with the before → after value on the pack's own KPIs, with drill-down to the change behind each number and a manual override that recomputes. Use on /oracle-packs-web:demo <pack-spec.md>, "make the interactive demo for <pack>", "walkthrough for the mini-site", or as step 6 of /oracle-packs:build. Always asks for sources (video, screenshots, written overview or a detailed brief) before building.
disable-model-invocation: false
user-invocable: true
---

# /oracle-packs-web:demo — the guided walkthrough

> **Paths.** `shared/...` means `${CLAUDE_PLUGIN_ROOT}/shared/...`; `tools/...`, `assets/...` and `references/...` are this skill's own folder.

**Load only what the step needs.** `references/cards/manifest.yaml` lists, per step, exactly which files that step reads. Read those and nothing else — never the whole folder, never a card for a step you are not on, never a long reference a card already points to. `assets/reference-demo/` and `assets/tour-engine.js` are **code to copy from, not reading material**: open the one file you are adapting, never the folder.

## Preconditions

- A confirmed, lint-clean `pack-spec.md`.
- **Sources, asked first, always** (card: `sources`). Without at least one, stop and say why.
- Node 22+ and a Chrome binary for the capture script; a local static server for QA. Check `node --version` and `CHROME_BIN` before planning around them; exit 3 from either is a deferred condition, never a result.

## The procedure

1. **Ask for the sources.** Card: `sources`. One widget, before anything else: a recording, screenshots, a written overview, or a detailed brief — and where they are. State what you have, what is missing, and the concerns, before building.
2. **Extract the real flow.** Cards: `flow`, plus `shared/references/anatomy/artifact-demo.md`. Screens in order, the information model, where the human decides, what the system does, what the outputs are. Write `<work>/demo/flow.md` — the pack's local work folder, `shared/tools/py shared/tools/pack_paths.py <slug>`, never the packaging-skills repo — and confirm it with a widget.
3. **Design it, on the strongest model.** Cards: `design`, `word-budgets`. About six guided steps; the value band right after the run; the drill-down to the rule and effect behind each number; the manual override that recomputes; the moments where the system is seen reasoning. Confirm the design with a widget before building.
4. **Settle the data model and the figures.** Cards: `data-model`, `synthetic-data`. Current state + named changes with additive effects + `flagsFor(applied)`, so every number is computed in the page. Get this right before any UI.
5. **Build** `index.html`, `demo.css`, `demo.js` and `data.js` under `<work>/artifacts/demo/` (or, when the walkthrough goes onto the site, under the site manifest's `paths.demos/<slug>/`, finding and reading the site as the listing skill's `site` card says). Cards: `build`, `word-budgets`. Ship a thin vertical slice first, then the full run. The `index.html` head carries `<meta name="pack-spec" content="…">` with the line `shared/tools/py shared/tools/spec_stamp.py --spec <spec>` prints, so the walkthrough says which spec it was built from.
6. **Red-team, then audit fidelity.** Card: `red-team`. Both before showing it to anyone.
7. **QA and lint.** Card: `qa`. `node tools/capture-demo-frames.mjs --demo <url> --scenario <json> --out <dir>`; `LOGS: none` is the gate; then `shared/tools/py shared/tools/lint_artifact.py <demo dir> --channel demo --spec <spec>`.
8. **Review pack.** Card: `review-pack`. One rebuild round; a single-step change is the fast path.
9. **Hand to the listing.** Card: `handoff`. The captures become its step frames and poster; the demo is published standalone and linked.

**Model routing.** The mechanical majority — source extraction, research fan-out, builds from a settled design, QA loops, captures, conversions — goes to a cheaper capable model. Spend the strongest model only on the design decisions, the data model where the numbers must reconcile, the red-team pass and the final review. **Say which steps used which.** Its copy still gets a mechanical pass before it ships. Every subagent follows `shared/references/running-agents.md`.

**Every message, question and option the owner sees passes the reader's test in `references/cards/owner-language.md`.**

## Showing it to the owner

Everything the owner reviews is opened beside the conversation *before* the question, so they answer while looking at the thing (`shared/references/review-loop.md` §3). In the desktop app a text file opens in the Files pane (`mcp__ccd_view__show_pane`, pane `file`); a render opens in the side panel (`SendUserFile`, `display: "render"`) with the editable file attached. Internal pack material is never published as a claude.ai artifact. In a plain terminal, print the path and a text rendering, and say so. Here: **the walkthrough is the one thing that may be published as an artifact** — synthetic and customer-free by rule. Open it there and hand over the link.

## Done, and the self-check

Done = flow and design confirmed by the user; the value band leads; every number reconciles on undo; red-team and fidelity reports delivered; captures clean; lint clean; synthetic figures listed; approval logged.

- [ ] Sources were asked for first and received, or their absence was stated before any build.
- [ ] The real product's flow, screens and information model are kept; only the content is generalized, to what the pack sells.
- [ ] The value band is the first thing after the run, with drill-down to the rule and a manual override that recomputes.
- [ ] Every number on screen comes out of the KPI function; undo and redo reconcile.
- [ ] No customer mark anywhere; every synthetic figure listed for the owner.
- [ ] Every capability area visible, every KPI in the band, no claim beyond the spec.
- [ ] `LOGS: none` on the capture, and the counter moved on every click.
- [ ] Everything the owner reviewed was open beside the conversation before the question was asked, and nothing he read used internal letters, codes or file names.
