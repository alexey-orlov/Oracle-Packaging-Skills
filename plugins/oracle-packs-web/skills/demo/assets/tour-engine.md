# `tour-engine.js` — the guided-walkthrough mechanics

_Long form, read by the builder agent in its own context; the runtime card is `references/cards/build.md`._

One module, plain ES5, no dependencies. It owns the callout, the click guard,
the counter, the positioner and the end card. It owns nothing about the product
being demonstrated.

**Why it exists.** Three walkthroughs were built before it, and each carried its
own copy of the same object. The copies drifted: the counter learned to move
inside a step in the third one only; the "never cover what this step is
describing" rule existed in one. The third demo cost four review rounds, partly
for that reason. Build the fourth on this.

**The reference demo does not use it.** `reference-demo/` is the shipped,
reviewed build, kept working exactly as it was delivered. This module is for the
next demo. Do not rewire the reference to prove the module works — build on the
module and keep the reference as the fidelity yardstick.

---

## 1 · Load order

```html
<script src="tour-engine.js"></script>   <!-- first: defines window.TourEngine -->
<script src="data.js"></script>          <!-- the demo's data model -->
<script src="demo.js"></script>          <!-- the demo; calls TourEngine.create -->
```

---

## 2 · The DOM contract

The engine reads and writes these ids. Every one is overridable through
`config.ids`; the defaults are what the three existing demos use.

| Default id | Role |
|---|---|
| `#tour` | the callout, positioned `fixed`; the engine sets `top`/`left`/`data-side` and toggles `hidden` |
| `#tour-step` | the counter text |
| `#tour-title`, `#tour-body` | the step's copy (set as text, never HTML) |
| `#tour-progress` | the segment bar; the engine writes `<i><b style="width:N%"></b></i>` per major |
| `#tour-next` | shown on **passive** steps only |
| `#tour-skip` | shown on every other step; calls the step's own `auto()` |
| `#tour-pill` | the "guided walkthrough" chip in the header |
| `#tour-toggle` | exit while running, restart when not |
| `#gate` | the modal that is both the welcome card **and** the end card |
| `#gate-title`, `#gate-body`, `#gate-start`, `#gate-free` | inside it |
| `#gate-try` | where the end card's "try next" doors are written |
| `#gate-steps` | an optional welcome-only list; hidden when the end card renders |
| `.gate-note` | the one-line demo-data note |

Classes the engine sets, which the demo's CSS must style:

| Class | On | Meaning |
|---|---|---|
| `.tour-target` | the step's target element | the one live control |
| `.is-nudge` | `#tour` | a blocked click just happened |
| `body.tour-on` | `<body>` | the tour is running |
| `body.tour-gutter` | `<body>` | a **docked** step is showing; reserve a side gutter so the card never lands on the analysis |

Minimum CSS for the fractional progress bar — an older stylesheet that only
styles `.tour-progress i.is-done` will render an empty bar:

```css
.tour-progress i   { flex:1; height:3px; border-radius:999px; background:#E6EAF1; overflow:hidden; }
.tour-progress i b { display:block; height:100%; border-radius:999px; background:var(--primary); }
```

`tour-engine-example.html` carries the smallest complete stylesheet that
satisfies the contract.

---

## 3 · The step shape

```js
{
  id:      "kpis",              // the string the demo passes to tour.after()
  major:   2,                   // what the VIEWER counts in; several steps may share one
  side:    "bottom",            // preferred side; the engine flips it when it does not fit
  title:   "Read what improved",// ≤ 6 words
  body:    "…",                 // ≤ 35 words
  target:  function () { … },   // REQUIRED — the one live element; re-evaluated on re-render
  anchor:  function () { … },   // optional — position against this instead (highlight a row, sit beside its table)
  avoid:   function () { … },   // optional — never cover this; the card moves out of its way
  before:  function () { … },   // optional — runs ONCE before target() is first asked for
  auto:    function () { … },   // what Skip performs; a passive step's auto is tour.next()
  passive: true,                // asks for nothing: every click blocked, Next is the way on
  waits:   true,                // starts an async stage: the callout hides until the demo calls next()
  dock:    "right",             // park the card in the gutter for this step
  scroll:  "center"             // scrollIntoView block; default "nearest"
}
```

`target()` is a function, not a node, because a re-render replaces nodes. The
engine re-resolves it on every reposition and waits up to ~90 frames for one
that has not rendered yet.

---

## 4 · The API

```js
var tour = TourEngine.create({ steps: STEPS, busy: function () { return S.busy; }, end: { … } });

tour.start();          // from the gate's Start button
tour.after("run");     // from inside the handler of the action step "run" asked for
tour.next();           // advance (Next on a passive step; or when an async stage lands)
tour.skip();           // perform this step's own action
tour.exit();           // stop, clean up, restore the toggle label
tour.finish();         // reached automatically past the last step: renders the end card
tour.reposition();     // called on resize/scroll; call it after your own layout changes
tour.nudge();          // shake the card (the guard does this for you)
tour.stepId();         // the current step's id
tour.counterText();    // "Step 4 of 6 · 2 of 3"
tour.avoidHit();       // QA hook: is the card covering this step's `avoid` element?
tour.active, tour.i, tour.steps, tour.majors
```

`TourEngine.params()` returns the URL's `URLSearchParams`.
`TourEngine.boot({ tour, prime, clean, defaultState, freeState })` wires the
gate and the switches so every demo behaves the same way.

### Config

| Key | Default | Notes |
|---|---|---|
| `steps` | — | required |
| `majors` | max `step.major` | the number the viewer counts to |
| `ids` | see §2 | override any id |
| `clickableSelector` | a generic control list | **extend it** with the demo's own clickable rows, map shapes and list items, or the guard cannot tell a real control from a stray click |
| `alwaysAllowSelector` | — | things that must keep working during the tour (a toast's close button) |
| `busy()` | `false` | true while an async stage runs; read by `waits` |
| `width`, `gap` | 306, 14 | the card's box |
| `stepDelay` | 280 | ms before the next step paints |
| `labels` | Exit guide / Restart walkthrough | the toggle's two states |
| `end` | — | `{ title, body, doors[{id,label,hint,go}], replayLabel, exploreLabel, note }` |
| `onStart`, `onExit`, `onStep` | noop | hooks |

---

## 5 · URL switches

| Switch | Effect |
|---|---|
| `?tour=off` | no guide; the gate is hidden and the demo is primed to a state |
| `?ui=clean` | the demo hides its own chrome — **screenshot mode: product UI only** |
| `?state=<name>` | which primed state to open in; `start` means the untouched one |

`boot()` applies all three. Everything else is the demo's own; `params()` hands
it the rest. The capture script drives these, so a demo that does not honour
them cannot produce clean step frames.

---

## 6 · The rules these behaviours encode

Each of these is a review-round correction, not a preference.

1. **Only the designated control acts.** The guard is a **capturing** listener, so it stops the event before the page's handlers see it. A blocked click nudges the card rather than doing nothing.
2. **A passive step blocks everything, including its own target's children.** Its target is a container (the KPI grid), and the viewer's job there is to read, not to click. Next is the way on.
3. **Lead with the value.** The step right after the run is that passive step, on the before → after band. Then a step that opens where the gain came from.
4. **The counter must move on every click.** A "Step 4 of 6" that stands still through four sub-steps reads as broken. The engine shows the position inside the major (`Step 4 of 6 · 2 of 3`) and fills the current segment fractionally.
5. **Skip performs the step's action**, it does not jump over it, so the page state never drifts from the narration.
6. **State first, then `after()`.** Calling `after()` before the state-changing action advances the tour while the page is still busy, and the real click is then blocked by the guard. This cost a round.
7. **Never cover what the step is describing.** `avoid()` moves the card; `avoidHit()` lets the scripted click-through assert it. Measure with rects, not by eye.
8. **The end card is for the viewer** — what they can act on now, three sentences, three doors, no figures. It is never a recap of what the build did.
9. **Word budgets.** Hint titles ≤ 6 words, bodies ≤ 35, end card ≤ 30, gate body ≤ 40 in two sentences plus one line for the step count and time.
10. **Hint titles are business sentences in the persona's words.** No hint says refresh, model, mapping, view or SQL outside an explain/trace panel.

---

## 7 · Known sharp edges

- **SVG elements have no `.click()`.** In the capture script and in any programmatic path, dispatch a bubbling `MouseEvent` instead.
- **Keep "pick" and "open" as separate steps.** Collapsing them makes the guard block the second half of a two-click interaction.
- **A generic `th b { display:block }`-style rule will eat the progress bar's `<b>`.** Scope stylesheet rules that target bare elements.
- **An inline-SVG map needs `preserveAspectRatio="xMidYMid meet"`** and a viewBox with label margins; keep markers off the label band.
- **The engine throws** if `config.steps` is empty or the callout element is missing. That is deliberate: a silent no-op tour ships.
