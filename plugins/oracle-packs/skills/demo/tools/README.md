# `demo/tools/`

| File | What it does |
|---|---|
| `capture-demo-frames.mjs` | Drives a walkthrough in headless Chrome over the DevTools protocol: scripted click-through for QA, and screenshot capture for the listing's step frames and poster. |

## Serving a walkthrough for QA

Serve the demo's folder over HTTP bound to 127.0.0.1 (`python3 -m http.server --bind 127.0.0.1`)
and browse `http://127.0.0.1:<port>` — not `localhost`, whose cache goes stale — or open it as a
`file://` URL: the walkthroughs are static and have no build step.

## Requirements — check before planning around them

- **Node ≥ 22.** The script uses the built-in `fetch` and `WebSocket`; there is nothing to `npm install`. It prints a clear message and **exits 3** on an older Node. Exit 3 means *the environment cannot do this yet* — retry after fixing it; never record it as a result.
- **A Chrome or Chromium binary**, found through **`CHROME_BIN`**, else the standard macOS and Windows install paths:

  ```sh
  # macOS and Windows: the standard installs are found — no need to set it
  export CHROME_BIN="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
  export CHROME_BIN="C:/Program Files/Google/Chrome/Application/chrome.exe"
  # Linux
  export CHROME_BIN=/usr/bin/google-chrome     # or /usr/bin/chromium
  ```

  A missing binary is also **exit 3**, with the paths to try.

- **Machines differ.** Before planning a capture, run `node --version` and
  `echo $CHROME_BIN`. On a machine with neither on the PATH, say so and hand the
  capture back rather than half-running it.

## Usage

```sh
node capture-demo-frames.mjs --demo <url-or-path> --out <dir> [--scenario <json>]
```

A bare filesystem path is turned into a `file://` URL, so a demo can be captured
with no web server:

```sh
node capture-demo-frames.mjs --demo <site>/site/demo/workforce-optimization/index.html --out ./qa --scenario tour.json
```

| Option | Default | Notes |
|---|---|---|
| `--demo` | — | required; url or path; a query string survives the `file://` conversion |
| `--out` | `./capture-out` | created if missing |
| `--scenario` | — | the step array; without one the script opens the page and shoots `00-open` |
| `--width` / `--height` | 1600 × 1000 | viewport in CSS px |
| `--dpr` | 1 | **2 for shipped stills** |
| `--port` | 9333 | DevTools port |
| `--allow-net` | off | webfont hosts are **blocked by default** so a slow network cannot stall a run; system fallbacks render instead, so glyph widths differ from the real page — trust geometry, not text fit, in a blocked run |
| `--keep-open` | off | leave Chrome running to debug |

## Scenario steps

A JSON array, run in order:

```json
[
  { "sleep": 1200 },
  { "shot": "00-gate" },
  { "click": "#gate-start" },
  { "assert": { "expr": "document.querySelector('#tour-step').textContent.indexOf('Step 1') === 0",
                "name": "counter shows Step 1" } },
  { "type": { "sel": "#q", "text": "…" } },
  { "eval": "window.DEMO.tour.stepId()" }
]
```

- **`click`** — SVG elements have no `.click()`; a bubbling `MouseEvent` is dispatched for them, so map zones and markers work.
- **`assert`** — fails the run if the expression is falsy. Use it to hold the tour to its contract: the counter moves, a passive step shows Next, the card does not cover what the step describes (`window.DEMO.tour.avoidHit()` is the hook), the end card renders its doors.
- **`eval`** — arbitrary expression in the page; top-level `await` is allowed.

## The gate

**`LOGS: none` is the gate.** Any console message or page exception is printed
instead and the process exits 1. A capture with console noise is not a passing
capture — look at the shots only after the gate is green. Failed assertions and
a step that threw are printed after the log line and also exit 1.

## The two standard runs

**Tour regression** — the whole guided flow, guide visible, DPR 1. Every step's
click in order, a shot after each, plus the contract assertions. Run it after
any change to the tour or the layout.

```sh
node capture-demo-frames.mjs --demo ./index.html --out ./qa --scenario tour.json
```

**Step frames and poster** — tour off, chrome hidden, DPR 2, primed to the state
that carries the cleared figure:

```sh
node capture-demo-frames.mjs \
  --demo './index.html?tour=off&ui=clean&state=final' \
  --out ./frames --dpr 2 --scenario frames.json
```

Then crop each frame to the listing's step-image spec (a fixed 16:10 frame, one
per workflow step) and drop them in as `overview.steps[].image`. The poster is
the same run's final state. When cropping with a tool whose offsets are
`Y` then `X`, remember `0 0` means centred.

**Scenario files are per-demo and live with the demo**, not here: they name that
product's selectors. Keep them beside the walkthrough they drive.
