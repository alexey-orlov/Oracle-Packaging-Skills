# QA and lint

**What this is.** A scripted click-through in headless Chrome, then the lint. Look at the frames only after the gate is green.

```sh
node tools/capture-demo-frames.mjs --demo <url-or-path> --out <dir> --scenario <json>
```

**The checks**

1. **`LOGS: none` is the gate.** Any console message or page exception is printed instead and the run exits 1, as does a failed assertion or a step that threw. A capture with console noise is not a passing capture.
2. **The counter moves on every click** — `Step 4 of 6 · 2 of 3` — and the progress segment fills fractionally. Assert it in the scenario, along with: a passive step shows Next, the card does not cover what the step describes (`window.DEMO.tour.avoidHit()`), the end card renders its doors.
3. **Hints allow only the designated control**; a blocked click nudges the card. Free exploration works after the tour. The switches `?tour=off`, `?ui=clean`, `?state=<name>` all work — a demo that does not honour them cannot produce clean step frames.
4. **Step frames and the poster at DPR 2**, tour off, chrome hidden, primed to the state that carries the cleared figure; then crop to the listing's fixed step-image frame.
5. `python3 shared/tools/lint_artifact.py <demo dir> --channel demo --spec <spec>` is clean.
6. **Node ≥ 22 and a Chrome binary** (`CHROME_BIN`); both failures **exit 3**, which is a **deferred condition to retry, never a result**. Check `node --version` before planning a capture. Webfonts are blocked by default, so trust geometry, not glyph widths, in a blocked run.
7. A browser extension generally cannot click inside an embedded preview frame: verify headlessly on `file://` or a local server, and the published demo in the viewer.

Scenario files are per-demo and live beside the demo they drive; options are in `tools/README.md`.
