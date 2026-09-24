# `demo/assets/`

_`tour-engine.js`, and the site's reference walkthrough, are code to copy from, not reading material: open the one file you are adapting, never the folder, and never into the conversation. The runtime card is `references/cards/build.md`._

| Path | What it is |
|---|---|
| `tour-engine.js` | The guided-walkthrough mechanics, extracted from three demos into one module. Build the next demo on this. |
| `tour-engine.md` | Its DOM contract, step shape, API, URL switches, and the rules each behaviour encodes. |
| `tour-engine-example.html` | A runnable three-step example: the smallest complete CSS, a `waits` step, a passive value step, an `avoid` step, and an end card with doors. Open it directly or serve the folder. |

## The order to read them in

1. **The skill's cards** (`../references/cards/`) — the standing requirements, the sources-first intake, the procedure, one step at a time.
2. **`../references/demo-data-model.md`** — current state + named changes with additive effects + `flagsFor(applied)`. Settle this before any UI.
3. **The site's reference walkthrough**, `<site>/<paths.demos>/<exemplarProduct>/` in the site manifest's names — open it and click through. Watch the value band arrive before the screens, drill into a change, undo it, and see the numbers follow.
4. **`tour-engine.md`** + **`tour-engine-example.html`** — then wire your own steps.

## Two rules about this folder

**The reference demo is not rewired.** It carries its own copy of the tour
object because it predates the module. It stays exactly as delivered: it is the
reviewed build, and changing it to demonstrate the module would cost the
yardstick its value. The module is for the next demo.

**Nothing here carries a customer mark.** No name, logo, geography or
identifier, in any file — verified by sweep. Every value is synthetic, with
ground-truth specifics: a fictional metro with named zones, invented postcodes,
synthetic identifiers, a schematic map from a jittered grid. Keep it that way in
whatever you build from it, and **list every synthetic figure for the owner in
your report**.

## What is deliberately not here

- **Per-demo capture scenarios.** They name one product's selectors; they live beside the demo they drive. `../tools/README.md` shows their shape.
- **Images, posters and step frames.** Each demo produces its own, at DPR 2, from the state that carries the cleared figure.
- **Preview URLs.** Where a demo is published is a runner input (`interactiveDemoArtifact` in the site's `links.json`), never a constant in a bundle.
