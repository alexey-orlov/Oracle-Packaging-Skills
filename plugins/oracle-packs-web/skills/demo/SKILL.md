---
name: demo
description: Build the accelerator pack's interactive walkthrough (a static, self-contained guided demo) from a confirmed pack spec and the sources the user supplies — the real product's flow and screens, generalized to what the pack sells, on synthetic data, leading with the before → after value on the pack's own KPIs, with drill-down to the change behind each number and a manual override that recomputes. Use on /oracle-packs-web:demo <pack-spec.yaml>, "make the interactive demo for <pack>", "walkthrough for the mini-site", or as step 6 of /oracle-packs:build. Always asks for sources (video, screenshots, written overview or a detailed brief) before building.
disable-model-invocation: false
user-invocable: true
---

# /oracle-packs-web:demo — the guided walkthrough

> **Paths.** `shared/...` means `${CLAUDE_PLUGIN_ROOT}/shared/...` (each plugin carries a synced copy of the repo's `shared/` folder); `tools/...`, `assets/...` and `references/...` without a prefix are relative to this skill's own folder. In a plain-copy install the plugin folder sits at `.claude/skills/<plugin>/` and `${CLAUDE_PLUGIN_ROOT}` resolves to it.


## Preconditions and inputs

- A confirmed, lint-clean `pack-spec.yaml`.
- **Sources, asked first, always**: a widget asking which of these the user can provide — a demo video of the real product, screenshots, a written overview of the flow, a detailed brief — and where they are. Without at least one, stop: a demo invented from the spec alone fails the fidelity rule. Also ask for the delivered product's reference corpus when the demo must match a vendor's real interface (the platform's own published screens).
- Node 22+ and Chrome for the capture script; a local static server (Python 3 `http.server` is enough) for QA.
- Read this skill's `references/demo-playbook.md` (the eleven requirements, the value-first rule, the reasoning-visible rule, word budgets, the fidelity audit), `references/demo-data-model.md`, `shared/references/naming-and-clearance.md`, and study `assets/reference-demo/` (a finished walkthrough) and `assets/tour-engine.js` (the shared tour mechanics — use it, do not re-implement the tour).

## Procedure

1. **Extract the real flow** from the sources: screens in order, the information model, where the human decides, what the AI does at each step, what the outputs are. Write `packs/<slug>/demo/flow.md` and confirm it with the user through a widget (steps in order, which to keep, which to simplify). A tedious real workflow is deliberately simplified for the demo, but the order and the information model stay real.
2. **Design on the strongest model**: the six-step guided tour; the value band that appears right after the run (before → after on the spec's KPIs, one band); the drill-down from each number to the named changes that produced it (rule and effect); the manual override that recomputes; the moments where the AI is seen reasoning (never a progress bar over the interesting work); the end card for the viewer (what they can act on now, three doors, no figures). Word budgets from the playbook. Confirm the design with a widget before building.
3. **Data model**: `data.js` as current state + named changes with additive KPI effects + `flagsFor(applied)`, so every number is computed in the page and an undo recomputes everything; deltas from raw means. Synthetic everywhere: no customer geography, ids, names or documents; the cleared headline figure reproduced exactly, companions modest; **list every synthetic figure for the owner**.
4. **Build** `index.html`, `demo.css`, `demo.js` (on `tour-engine.js`), `data.js` under `packs/<slug>/demo/` (or the site's `site/demo/<slug>/` when `--site` is given). Brand-agnostic and industry-neutral; vendor interfaces recognizable where the demo runs on that platform; no vendor logo files unless cleared, the wordmark as text.
5. **Red-team against the spec** before showing it: every capability area the pack sells is visible somewhere; every KPI in the spec appears in the value band; no claim beyond the spec; then widen without changing the flow and report the delta as a TLDR.
6. **Fidelity audit** when a reference corpus exists: classify every element A (deviates from a reference) / B (invented, no reference) / C (matches); fix the A items; report every residual B with its reason.
7. **QA**: scripted click-through with `node tools/capture-demo-frames.mjs --demo <url> --scenario <json> --out <dir>`; `LOGS: none` is the gate; then look at the frames. The counter must move on every click ("Step 4 of 6 · 2 of 3"); hints allow only the designated control; free exploration after the tour; URL switches `?tour=off&ui=clean` work.
8. **Lint**: `python3 shared/tools/lint_artifact.py <demo dir> --channel demo --spec <spec>`.
9. **Review pack**: the frames as a contact sheet, the value band, the synthetic-figure list, the residual inventions, the open items. One rebuild round; a single-step change is the fast path.
10. **Hand to the listing**: the captures become the listing's step frames and poster; the listing gets the secondary CTA to the demo. Hosting: the demo is its own standalone page or artifact, linked from the listing; the URL is the owner's input.

## Definition of done

Flow and design confirmed by the user; the value band leads; every number reconciles on undo; red-team and fidelity reports delivered; captures clean with no console logs; lint clean; synthetic figures listed; approval logged.
