# `reference-demo/` — a delivered walkthrough, kept whole

A complete, reviewed interactive demo of a **workforce-optimization** pack:
a dispatcher plans four weeks of field work for a metro region, runs the
optimizer, reads what improved, drills into the changes behind each number,
overrules one the solver got wrong, re-plans around the fix and exports the
approved plan.

Four files, no build step, no dependencies:

| File | Size | What it holds |
|---|---|---|
| `index.html` | 16 KB | the shell: header, dashboard, map, schedule, modals, the tour callout and the gate |
| `demo.css` | 46 KB | the whole look, including the tour and highlight states |
| `demo.js` | 86 KB | the app, the KPI computation, the tour steps and its own copy of the tour object |
| `data.js` | 27 KB | the synthetic world and the change list |

Open `index.html` directly, or serve the folder
(`python3 -m http.server 8791 --bind 127.0.0.1`) and browse
`http://127.0.0.1:8791/reference-demo/index.html`.
The only network request is a webfont; it degrades to system fonts, and the
capture script blocks it on purpose.

---

## What it demonstrates

**The requirements, made concrete.** Read the playbook beside it — each of these
is a requirement you can watch working:

| Requirement | Where to look |
|---|---|
| **Lead with the value** (R6) | the KPI band appears the moment the run lands: four KPIs, before → after, same method, same four weeks |
| **A passive step on the metrics** (R7) | tour step 6 (`kpis`) asks for nothing, blocks every click and offers Next |
| **Drill down to the rule behind each number** (R6) | *Review changes* → a list of eleven changes, each with its rule, what it did, why, and its effect on the KPIs |
| **Manual override that recomputes** (R6) | *Undo* on the Marsh End change: the band, the flags and the schedule all move at once |
| **A tradeoff the solver got wrong** | that same change made one zone's wait worse — the demo does not pretend everything improved |
| **The human gate** | *Accept remaining* takes every pending zone that carries no flag; a flagged zone always waits for a person |
| **Feedback into a re-run** | the note written on the undo travels into plan v2 and into the export |
| **Mocked I/O, elegantly** (R3) | the file picker shows prepared files and nothing uploads; the export renders the field-service system's own import format |
| **Only the designated control acts** (R3) | the capturing click guard, with a nudge on a blocked click |
| **The data model** | `data.js` — current state, eleven named changes with additive `effects`, and `flagsFor(applied)`; every KPI is computed in the page |
| **URL switches** | `?tour=off`, `?ui=clean`, `?state=start|v1|v2|final`, plus `view`, `plan`, `week`, `filters`, `focus` |
| **A QA surface** | `window.DEMO` exposes the state, the tour and the main actions for a scripted click-through |

## What is synthetic — all of it

The header of `data.js` says it, and it is true of every value in the folder:
a **fictional coastal metro**, invented districts and postcodes, synthetic
technician identifiers, a synthetic dispatcher persona, a schematic map drawn
from a jittered grid (no tiles, no real geography), and deltas inside the band
the pack is cleared to claim.

There is **no customer name, logo, geography or identifier** anywhere in these
files — verified by deny-list sweep. There are no vendor marks either; this
particular pack's demo did not need them. A demo that runs **on** a platform is
expected to carry that platform's marks and to look like its product: the rule
is *no specific customer marks*, not *no marks*.

## How to use it

**As the fidelity yardstick.** Open it beside your first cut and ask the
questions the owner asks: does the gain arrive before the screens? can I see the
rule behind a number? can I overrule the machine? does the counter move on every
click? is anything on screen over its word budget?

**As a parts bin**, named in the playbook: the KPI band, the changes list with
Show / Undo / Note, the additive-effect data model, the passive tour step, the
mocked picker and the export tab.

**Not as a starting fork.** It is one pack's product, at the altitude that pack
needed. Start from its shape, not its copy.

## One thing it deliberately does *not* do

It carries **its own copy of the tour object**, because it predates
`../tour-engine.js`. That is left exactly as delivered: this is the reviewed,
shipped build, and rewiring it would cost the yardstick its value while proving
nothing. **Build the next demo on the module**, which carries everything this
copy does plus the behaviours two later demos earned — the fractional counter,
docked steps, `before()`, `avoid()` and the end card with its doors.
