# The interactive demo — `site/demo/<slug>/`, four files, no build

The demo is not a slide deck in HTML. Its anatomy is a **data model**, the same for every pack:

- **Current state** — the world the product operates on: entities, the period, the plan as it stands.
- **Named changes** — each `{id, rule, kind, title, what, why, overrides, effects}`: the rule that produced it, what it does, why, and its **additive effect on each KPI**.
- **`flagsFor(applied)`** — exceptions computed from which changes are applied, so nothing is hard-coded.
- **Additive KPI effects** — every number computed in the page from raw means, so an undo recomputes everything and every figure reconciles.
- Around them: `inputSheets` / `pickerFiles` (the mocked upload), `stages[]` and `reoptStages[]` (the run), `settings{mode, objectives[], rules[], regions[], connectors[]}`, `exportColumns` and `priorHistory` (the audit trail), and the tour engine's `STEPS[]` with `?tour=off`, `?ui=clean`.

**The components, in the form they take here.** Name → app chrome only, no vendor or customer marks. Problem ↔ solution → live exceptions via `flagsFor(applied)`, dramatized, never stated as copy. Capabilities → the rules and objectives panels. Workflow → `inputSheets` → `stages[]` → dashboard → `flagsFor()` → `reoptStages[]` → `exportColumns`, canonical for the human-in-the-loop loop. Architecture → the connectors panel. Oracle products → de-branded connector names. KPIs → computed in the page, never quoted; the **before → after band leads**. Packages → implied as surfaces, never stated. The one-liner, the ICP and the verticals are absent by design: the demo is industry-neutral.

**Standing requirements.** Keep the real product's flow, screens and information model; generalize the **content** to what the pack sells. Synthetic data only. Lead with the value, then the drill-down, then the override. Red-team the first cut against the brief.
