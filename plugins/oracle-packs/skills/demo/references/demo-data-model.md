# The demo data model

_Long form, read by the builder agent in its own context; the runtime card is `references/cards/data-model.md`._

One invariant runs through every walkthrough that has worked:

> **Current state + named changes with additive KPI effects + a `flagsFor(applied)`
> function — so every KPI is computed in the page, every number reconciles, and
> an undo recomputes everything.**

Get this right before any UI. A demo whose KPI band is a hard-coded pair of
numbers cannot honour the three requirements that matter most — lead with the
value, drill down to the rule behind each number, let the viewer override by hand
and watch the numbers follow — because there is nothing to recompute.

---

## 1 · The four parts

### 1.1 Current state — the world as it is

The entities the product works on, at rest, with their present measures. In the
reference demo: a fictional metro, a four-week period, twelve zones with today's
demand and wait, eighteen technicians with skills, home zones, booked jobs and
absences, plus the calendar and its holidays.

Rules:

- **It is the baseline, and it never mutates.** Everything the demo shows as "after" is derived from it, so "before" is always recoverable exactly.
- **Ground-truth specifics.** Named zones, real-looking identifiers, a calendar with a public holiday in it. Synthetic is not the same as vague.
- **It carries the problems the run will fix**, visible from the first screen: an absence with no cover, an uncovered postcode, an over-capacity day. The opening screen shows the current state **with its open problems flagged** — that is what makes the run's result legible.

### 1.2 Named changes — what the run decided

An array of the decisions the system made, each one an object a person can read:

```js
{ id:      "capacity",                       // stable; the tour, the URL and the KPIs key off it
  rule:    "Daily capacity · 7 visits",      // THE RULE that produced it
  kind:    "improves" | "tradeoff" | "needs-decision",
  title:   "T-1048's 8-visit day brought back to 7, Tue 13 Oct",
  what:    "Two movable visits move to the neighbour who has room that day.",
  why:     "…the reasoning, in the persona's words, naming the constraint…",
  zones:   ["HV-05"], techs: ["T-1048","T-1050"], week: 2,   // what it touches
  overrides: [ … ],                          // how the plan changes, structurally
  effects: { jobs: { "T-1050": 2, "T-1048": -2 }, waits: { "HV-05": -0.1 } },
  effect:  "T-1048 at 114% → 100% of capacity that day · 2 visits to T-1050" }
```

Rules:

- **Every change names the rule that produced it.** This is the drill-down: a number → the changes behind it → the rule behind each change. A change with no rule is a magic trick.
- **`effects` is structured and additive**, keyed by entity. It is the only thing the KPI function reads. `effect` is the human sentence beside it, and the two must agree.
- **`kind` drives the visual treatment**, and at least one change must be a **tradeoff the solver got wrong** — the one the viewer undoes in R6's manual-override step. A run where everything improved has nothing to override.
- Changes cover the **spread of rules the pack claims**, not one rule five times. This is what the red-team pass checks.

### 1.3 Additive effects — the KPI function

```js
function kpis(applied) {           // applied = the ids currently in force
  // start from the current state, add the effects of every applied change,
  // then compute each KPI the way the product's methodology computes it
}
```

Rules:

- **KPIs are a pure function of `applied`.** Nothing else. Then an undo, a redo, a re-run and a deep link all produce the same numbers by construction.
- **Compute the same way for before and after**, over the same period. `kpis([])` is the baseline and `kpis(S.applied)` is the proposal; the band shows both.
- **Compute deltas from raw means, never from the rounded displays.** Keep the unrounded mean beside the rounded one (`prodRaw` beside `prod` in the reference) and take the delta from the raw pair, or the headline drifts by a tenth of a point and stops reconciling with the drill-down.
- **Memoize by the applied set** if the function is called per render; it is called a lot.
- **Every KPI on screen comes out of this function.** A number typed into the markup is a number that will contradict the band the first time someone undoes something.

### 1.4 `flagsFor(applied)` — what still needs a person

```js
function flagsFor(applied) {
  var on = function (id) { return applied.indexOf(id) >= 0; }, out = [];
  if (!on("coverage"))  out.push({ kind: "uncovered", zone: "…", title: "…", text: "…" });
  if (on("marsh-move")) out.push({ kind: "wait-worse", zone: "…", title: "…", text: "…", decision: true });
  return out;
}
```

Rules:

- **Flags are a function of what is applied, not a stored list.** Undo a change and the problem it solved comes back; apply one with a cost and its cost appears. That is the whole mechanism behind "undo, and watch the numbers and the warnings follow".
- Flags come in two shapes: **problems a change removes** (`if (!on(id))`) and **costs a change introduces** (`if (on(id))`).
- `decision: true` marks a flag that **blocks a bulk accept**. "Accept everything else" takes every pending item that carries no flag; a flagged one always waits for a person. This is the human gate, made mechanical.

---

## 2 · The state object

```js
var S = {
  ran: false,          // has the run happened
  busy: false,         // an async stage is running (the tour's `waits` reads this)
  version: "v1",       // which plan
  applied: [],         // the change ids in force — THE source of every number
  undone: [],          // what the person overruled
  notes: {},           // per-change notes, which travel into the re-run and the export
  decisions: {},       // per-entity accept / reject / pending
  sel: {}              // selection, purely view state
};
```

`applied` is the model. Everything else is either view state or a record of what
a person did. `plans.v1` and `plans.v2` are just two arrays of ids — the re-run
after feedback is a different `applied` set, not a different data file.

---

## 3 · Where the spec's values land

| Spec key | Component | Where it goes in the demo |
|---|---|---|
| `workflow.inputs[]` | 7 | the mocked upload: the picker's file list and the input sheets it claims to hold |
| `workflow.steps[]` | 7 | **the tour's majors** — one major step per workflow step, in order; the processing stages the run animates are these steps |
| `workflow.steps[].actor` / `human_in_the_loop` | 7 | which steps the system performs and which one the viewer performs. **A human-in-the-loop step is never merged away** — it is the manual-override step |
| `workflow.steps[].failure_path` | 7 | the flags: what a step does when the input is wrong (a row is flagged, not dropped) |
| `workflow.outputs[]` | 7 | the export tab: the real import format, mocked |
| `kpis[]` | 11 | **the KPI band.** `name` → the tile label · `formula` → how `kpis()` computes it · `baseline` → the "before" value · `figure` → what the "after" must come out to · `figure_status` decides whether it may be shown at all |
| `kpis[].caveat` | 11 | the one line under the band |
| `capabilities[]` | 6 | the **spread of rules** the changes must cover — the red-team checklist |
| `capabilities[].features[].status` | 6 | a `roadmap` feature is not demonstrated as working. Do not demo what the pack does not do |
| `architecture.stack[]` | 8 | the settings surface: engines, connectors, regions — visible, not invented |
| `verticals[]` | 5 | the world the demo is set in, generalized past any one of them |
| `clearance.anonymized_descriptor` | — | the only way the source engagement may ever be referred to |
| `packages.capability_handling` | 12 | what the demo must **not** narrow to: the S/M/L rows are the coverage target of the red-team pass |

**The cleared figure is the anchor.** `kpis[]` carries one figure the pack is
cleared to claim. The demo's headline delta must come out to that figure from
the data — not be printed over it. Tune the change effects until `kpis(plans.v1)`
produces it, and the shipped stills show that state.

---

## 4 · Self-check

1. Is every number on screen returned by the KPI function?
2. Does `kpis([])` reproduce the current state exactly?
3. Does the headline delta equal the cleared figure, computed from raw means?
4. Undo any single change: do the band, the drill-down, the flags and the schedule all move together?
5. Redo it: does everything return to exactly where it was?
6. Does at least one change make something **worse**, with the cost visible as a flag?
7. Does every change name the rule that produced it?
8. Does a flagged item block the bulk accept?
9. Do the changes cover the spread of capability areas the pack claims, or one area repeatedly?
10. Is every figure in the file either the cleared one or on the synthetic list for the report?
