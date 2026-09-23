# Building it

**What this is.** Four files under `packs/<slug>/demo/` (or the site's `site/demo/<slug>/` when a site root is given): `index.html`, `demo.css`, `demo.js`, `data.js`. Static, no build step, no dependencies.

**What to copy from.** `assets/reference-demo/` is a finished walkthrough — the fidelity yardstick and the parts bin (the KPI band, the changes list, the passive step, the mocked picker, the export tab). It is **code to adapt, not reading material**: open the one file you are adapting, never the folder. **Start from its shape, not its copy.** Never rewire it; it stays as delivered.

**The checks**

1. **Built on `assets/tour-engine.js`**, not a fourth copy of the tour object. Load order: engine → `data.js` → `demo.js`. Its API and DOM contract are in `assets/tour-engine.md`, read by the builder in its own context; `tour-engine-example.html` carries the smallest stylesheet that satisfies the contract.
2. **Ship a thin vertical slice first** — the first two steps, for early feedback — then the full run.
3. Brand-agnostic and industry-neutral, and **a cleaner UI than the real product**; vendor interfaces recognizable where the demo runs on that platform.
4. Upload, export and write-back are **mocked, and mocked elegantly**: a picker showing a prepared file, an export rendering the real import format.
5. **Call the state-changing action before the tour's `after()`** when it sets a busy flag, or the tour advances early and the real click is blocked by its own guard. Keep "pick" and "open" as **separate steps**. SVG elements have **no `.click()`** — dispatch a bubbling `MouseEvent`.
6. Scope bare-element CSS rules (a `th b { display:block }` eats the progress bar's `<b>`). An inline-SVG map needs `preserveAspectRatio="xMidYMid meet"`.
7. Long-running agents write intermediate output early; if the file has not moved when the stage should be done, take over from what it wrote.
