# The data model

**What this is.** `data.js`, settled **before any UI**. The invariant behind every walkthrough that has worked: **current state + named changes with additive KPI effects + `flagsFor(applied)`**, so every number is computed in the page and an undo recomputes everything.

**The four parts**

- **Current state** — the entities at rest with their measures. The baseline, and it **never mutates**, so "before" stays exactly recoverable. It **carries the problems the run will fix**, flagged on the opening screen: that is what makes the result legible.
- **Named changes** — decisions a person can read: `id`, **`rule`** (what produced it), `kind` (`improves` / `tradeoff` / `needs-decision`), `title`, `what`, `why` in the persona's words, what it touches, `overrides`, structured **`effects`** keyed by entity, and the human `effect` sentence agreeing with them. A change with no rule is a magic trick.
- **`kpis(applied)`** — a pure function of the applied ids, so undo, redo, a re-run and a deep link agree by construction. `kpis([])` is the baseline, `kpis(S.applied)` the proposal, computed the same way over the same period. **Deltas from raw means, never rounded displays.**
- **`flagsFor(applied)`** — flags computed, not stored: problems a change removes, costs a change introduces. `decision: true` blocks a bulk accept — the human gate, made mechanical.

**The checks**

1. Every number on screen comes out of `kpis()`; `kpis([])` reproduces the current state exactly.
2. The headline delta equals the cleared figure, computed from raw means.
3. Undo any change: band, drill-down, flags and schedule move together; redo returns everything.
4. At least one change is a **tradeoff the solver got wrong**, its cost visible as a flag.
5. Changes cover the **spread of capability areas the pack claims**, not one area five times.

**Fills / reads:** `workflow.*`, `kpis[]`, `capabilities[]`, `architecture.stack[]`, `verticals[]`, `packages.capability_handling[]`.
