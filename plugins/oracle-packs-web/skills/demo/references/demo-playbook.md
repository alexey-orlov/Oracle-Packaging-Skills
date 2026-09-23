# The interactive-demo playbook

_Long form; the runtime cards are `references/cards/sources.md`, `flow.md`, `design.md`, `word-budgets.md`, `data-model.md`, `synthetic-data.md`, `build.md`, `red-team.md`, `qa.md`, `review-pack.md` and `handoff.md`._

An interactive demo is a **guided walkthrough of what the pack sells**, built to
the pack's own spec, running on synthetic data, in a UI a viewer recognizes as
the real product. Everything below was paid for across three builds and eleven
review rounds.

Read this before writing a line of demo code. The machine mechanics — how to run
it, capture it, publish it — are in the appendix at the end, deliberately, so
they do not crowd out the part that decides whether the demo works.

---

## 0 · Sources — ask first, build second

**The skill asks the user for sources before anything else.** Do not start from
the pack spec alone and do not reconstruct a product from imagination.

Ask for, in this order of usefulness:

1. **a recording** of the real product or the delivered solution (a screen-share, a customer demo, a walkthrough video);
2. **screenshots** of the real screens;
3. **a written overview** of the flow and the information model;
4. **a detailed brief**, where none of the above exists.

Then say plainly what you have and what you are missing, and **ask the questions
and raise the concerns before proceeding** — not after the first cut.

**When no product recording exists**, the "real product" is the platform the use
case runs on, and its interfaces must be **recognizable, not invented**. Widen
the search before labelling anything free design: vendor product videos
(screenshot them at timestamps), documentation pages with figures, session decks
and PDFs rendered page by page, feature-announcement posts, hands-on-lab images,
product-tour assets, the vendor's own sample applications. **Log every source
tried.** Documentation sites often build their tables of contents in JavaScript,
so a link crawl misses whole chapters: download the book PDF, grep its text,
then fetch the HTML of the chapter that matters — that route once produced
fourteen clean product figures a three-level crawl never found.

---

## 1 · The eleven standing requirements

**R1 · Keep the real product's flow, screens and information model; generalize
the content.** Generalize to what the **pack** sells — its S/M/L rows and its
feature matrix — never to the one customer case it was built on. Where there is
no delivered product, the platform is the reference, styled like the product
rather than like a generic SaaS shell.

**R2 · Customer-agnostic and industry-neutral, on synthetic data with
ground-truth specifics.** Invented geography, ids, names and documents. No
customer mark of any kind inside the demo — name, logo, geography, identifiers.
**Vendor and platform marks are expected** where the demo runs on that platform:
the rule is *no specific customer marks*, not *no marks*. No figure outside the
cleared band; no time-to-deliver claim unless it is cleared.

**R3 · No integrations, no real inputs.** Upload, export and write-back are
mocked, and mocked **elegantly** — a file picker that shows a prepared file, an
export that renders the real import format. A short guided flow of about six
steps; hints that allow only the designated control; free exploration afterwards;
a cleaner UI than the real product.

**R4 · Deliberately simplify a tedious real workflow** for demo purposes. A
faithful reproduction of a twelve-click reality is not fidelity, it is tedium.

**R5 · Red-team the first cut against the pack specs before delivering.** Hold
the demo against the pack's own S/M/L rows, feature matrix and listing copy:
*does it look too narrow next to what the pack documents claim?* Widen coverage
**without changing the flow, the interface or the information architecture** —
a gap between demo and real product is worse than a narrow demo — and report the
delta as a TLDR. The first documents demo covered one rate type, one document
type and one validator, and had to be widened.

**R6 · Lead with the value, not the screens.** The improvement is **the first
thing the viewer sees after the run**: before → after on the product's own KPIs,
in **one band**. Then a drill-down from each number to the concrete changes that
produced it — **the rule and its effect**, per change. Then a **manual override**
that recomputes the numbers, so the viewer can overrule the machine and watch
everything follow. A faithful screen tour that buries the gain fails the brief,
however real the screens are.

> *"It didn't focus my attention on what actually got optimized; I expected to
> see that the optimization clearly shows improvement compared to current while
> letting me apply manual fixes and drill down."*

**R7 · A dedicated passive step pauses on the improved metrics** — a step that
asks for no action, with a Next control and a guard that blocks every other
click — and then a step that opens **where the gain comes from**.

**R8 · The AI must be seen reasoning at every step, on an AI-native business
task with an outcome promise.** A question turning into a table is table stakes;
**heavy AI work behind a progress bar reads as ETL**. The viewer must watch the
system scan every source, rank by business impact, attribute a cause that sits in
a different system from the symptom, recommend actions, recompute after a person
overrules it, and leave artefacts people use. Pick a decision **with money on
it**, not a hygiene task, and let the promise be an **outcome**, never hours
saved. Hint titles are business sentences in the persona's words; no hint says
refresh, model, mapping, view or SQL outside an explain or trace panel. **Open
on the integrated sources, not on a job run.**

> Root cause, as stated for the next build: *the AI did its hardest work behind a
> progress bar and showed its reasoning where the work was cheapest.*

**R9 · Interface fidelity is checkable.** Audit every element against a real
reference corpus and classify each: **A** a deviation where a reference exists,
**B** an invention where none does, **C** a match. Fix every A-item, and
**report every residual invention with its reason**. Measure with
`getComputedStyle` / `getBoundingClientRect`, never by eye. The owner's standard
is *"I expect a full match"*.

**R10 · The end card is for the viewer, and the counter must move on every
click.** An end card that recaps what the build did reads as a justification of
the session. Write it as **what the viewer can act on now**: three sentences,
three "try next" doors, no figures. A `Step n of N` counter that stands still
through several sub-steps feels broken — show the position inside the step
(`Step 4 of 6 · 2 of 3`) and fill the progress segment fractionally.

**R11 · Word budgets, everywhere on screen.**

| Surface | Budget |
|---|---|
| Gate body | ≤ 40 words in two sentences, **plus** one line for the step count and the time |
| Hint title | ≤ 6 words |
| Hint body | ≤ 35 words |
| End card | ≤ 30 words |
| Toast | ≤ 15 words |
| Card description / helper line | ≤ 14 words |
| Footer | one line |

*A viewer reads a demo, not a memo.*

---

## 2 · Synthetic-data rules

- **Everything is invented**: geography, place names, postcodes, identifiers, people, documents, counterparties. State it at the top of the data file.
- **Ground-truth specifics, not vagueness.** A fictional metro with twelve named zones and eighteen technicians is synthetic; "some regions" is not a demo.
- **A cleared figure is reproduced exactly.** The demo's headline improvement is the figure the pack is cleared to claim, and the shipped stills show the state that carries it.
- **Companion figures are synthetic and modest** — they must not out-shout the cleared one, and they must reconcile with it arithmetically.
- **List every synthetic figure for the owner in the report.** Every one. This is not optional and it is not a footnote.
- **No money figure from a customer's business case**: no contract values, headcounts, salaries or operating baselines. Ratios, durations and counts only.
- **A map is schematic**, drawn from a jittered grid — no tiles, no real geography.
- **Deltas are computed from raw means, never from the rounded displays**, or the headline drifts by a tenth of a point and stops reconciling with the drill-down.

---

## 3 · The procedure

1. **Ask for sources** (§0). State what you have, what is missing, and the concerns — before building.
2. **Orient.** The pack spec → the listing copy for this pack → the reference demo's code.
3. **Reconstruct the source.** Frames from the recording, narration transcribed on-device, any spec sheet shown on screen read out. Without a recording, run the widened search of §0 and log it.
4. **Write the generalization before coding** — ten lines: the world, the period, the rules that visibly matter, the plans (current · v1 · v2 after feedback), the KPIs and how each is computed, the exceptions, the explanations, the integration surfaces, the settings surface, the tour.
5. **Build the data model**: current state + named changes with additive KPI effects + `flagsFor(applied)`. See `demo-data-model.md`. Get this right before any UI.
6. **Build on the shared tour engine** (`../assets/tour-engine.js`), not a fourth copy of it.
7. **Ship a thin vertical slice first** — the first two steps, quickly — for early feedback, then the full run.
8. **QA by scripted click-through**: the capture script in scenario mode; **`LOGS: none` is the gate**; then look at the shots.
9. **Red-team** against the pack's S/M/L rows, feature matrix and listing copy (R5). Close the gaps that do not change the flow. Report the delta.
10. **Fidelity audit** (R9): A / B / C against the reference corpus, measured; fix the A-items; report the residual B-items with reasons.
11. **Capture** the step frames and the poster at DPR 2, in the state that carries the cleared figure.
12. **Publish the demo as its own page** (appendix A4). Its standalone URL exists only from this step on, and step 13 wires it.
13. **Wire** the listing: `interactiveDemo` (the canonical path) and `interactiveDemoArtifact` (the URL step 12 returned) in the site's `links.json`, `videoPoster` in `config.js`, and the step images. Run `node tools/sync-links.js` from the site root, then the site's checker.
14. **Publish the site**, `data/links.js` included (appendix A4).
15. **Report**: what it covers, the red-team delta, every synthetic figure, the residual inventions, and the decisions that remain the owner's.

---

## 4 · What the owner wants before approving

- **The running thing to click through** — he reviews the live demo, never a description.
- **A TLDR of what changed** since the last cut.
- **The list of synthetic figures.**
- **The decisions that remain his**, stated as open items rather than resolved.

He never approves silently: expect a numbered list back, and expect a rebuild
round. Corrections arrive as a screenshot and a few words.

---

## 5 · Pitfalls already paid for

- **A screen tour is not a demo.** The viewer must see what got better, drill into why, and be able to overrule it.
- **A faithful platform tour with one visible AI step reads as ETL plus admin**, however real the screens are. Write the six hint titles as business sentences *before* building, and check that every step shows the system doing something a person could not do across systems.
- **Call the state-changing action before the tour's `after()`** when that action sets a busy flag, or the tour advances a step early and the real click is then blocked by its own guard.
- **Keep "pick" and "open" as separate steps.** Collapsing a two-click interaction makes the guard block its second half.
- **SVG elements have no `.click()`** — dispatch a bubbling `MouseEvent`.
- **A passive step needs a Next control and a guard that blocks every page click**, its own target's children included.
- **Compute deltas from raw means, not rounded displays.**
- **An inline-SVG map needs `preserveAspectRatio="xMidYMid meet"`** and a viewBox with label margins; keep markers off the label band.
- **A generic bare-element CSS rule bites** — a `th b { display:block }` will eat an inline `<b>` somewhere else, including the tour's own progress fill.
- **Machines differ.** Check `node --version` and the Chrome binary before planning around them.
- **A shared working tree and a shared preview** mean another session may be editing and publishing the same thing: check the log on the files you touch, expect record-section numbers to collide, expect publish refusals — re-read, merge, republish.
- **Verification limits:** a browser extension generally cannot click inside an embedded preview frame. Verify the page headlessly on `file://` or a local server, and the published demo in the viewer (which may show a skeleton for several seconds before rendering).
- **A stalled background agent is not progress.** Have long work write intermediate output early; if the file has not moved when the stage should be done, stop it and take over from what it wrote.

---

## 6 · Model routing (roles, not model names)

Use a **cheaper, capable model** for the mechanical majority: source extraction,
research fan-out, builds from a spec, QA loops, captures, conversions, doc
mechanics. Spend the **strongest available model** only where it changes the
outcome: the design decisions, the data model where the numbers must reconcile,
the red-team pass, and the final review. **Say which steps used which.**

Keep the strongest model's share small and deliberate — one compact pass, not a
fan-out. Its copy still gets a mechanical pass before it ships: HTML entities
render literally, retired vocabulary creeps back, and leads run long.

---

## Appendix · Machine mechanics

### A1 · Run it

Serve the demo's folder over HTTP (`python3 -m http.server`, bound to
`127.0.0.1`) and browse `http://127.0.0.1:<port>` — **not `localhost`**, whose
cache goes stale. Or open it as a `file://` URL: the walkthroughs are static and
have no build step.

### A2 · URL switches

| Switch | Effect |
|---|---|
| `?tour=off` | no guide; the demo opens primed to a state |
| `?ui=clean` | the demo hides its own chrome — screenshot mode, product UI only |
| `?state=<name>` | which primed state (`start` = untouched) |

The capture script drives these; a demo that does not honour them cannot produce
clean step frames.

### A3 · Scripted click-through and capture

`../tools/capture-demo-frames.mjs`, with a per-demo scenario JSON that lives
beside the demo. **`LOGS: none` is the gate.** Node ≥ 22 and `CHROME_BIN`; both
failures exit 3 and are **deferred conditions to retry**, never results.
Webfonts are blocked by default so a slow network cannot stall a run — trust
geometry, not glyph widths, in a blocked run. Full options in
`../tools/README.md`.

Step frames and the poster: DPR 2, tour off, UI clean, primed to the state that
carries the cleared figure; then crop to the listing's fixed step-image frame.

### A4 · Hosting

A demo that lives inside the site tree cannot open as a top-level page when the
site is served as a single preview artifact — a supporting file is not a
document. So the walkthrough is published on its own first, and the order is
fixed, because each step needs what the one before it produced:

1. **Publish the walkthrough as its own page.** Its URL exists only from here on.
2. **Wire it.** That URL goes in the site's `links.json` as
   `interactiveDemoArtifact`, while `interactiveDemo` holds the canonical path
   inside the publish root (`demo/<slug>/index.html`) for the real deployment;
   `videoPoster` and the step images go in with them.
3. **Run `node tools/sync-links.js`** from the site root, then the site's checker.
4. **Publish the site**, with `data/links.js` in the publish.

The listing's secondary CTA opens the walkthrough in a new tab. Both links are
runner inputs; neither belongs in a bundle.

### A5 · Definition of done

```
[ ] sources asked for, received or explicitly absent; concerns raised up front
[ ] generalization written before the code
[ ] data model: current state + named changes + additive effects + flagsFor()
[ ] built on the shared tour engine
[ ] six-ish steps; only the designated control acts; free exploration after
[ ] the value band is the first thing after the run; drill-down; manual override
[ ] a passive step on the metrics, then a step on where the gain comes from
[ ] the AI is visibly reasoning at every step
[ ] every word inside its budget
[ ] end card: what the viewer can act on now, three doors, no figures
[ ] counter moves on every click
[ ] scripted click-through: LOGS: none, every assertion green
[ ] red-teamed against the pack's S/M/L rows and feature matrix; delta reported
[ ] fidelity audit A/B/C done and measured; residual inventions reported
[ ] no customer mark anywhere; every synthetic figure listed for the owner
[ ] frames and poster captured at DPR 2 in the cleared state
[ ] the demo published as its own page first, its URL in hand
[ ] listing wired: links.json interactiveDemo + interactiveDemoArtifact (that URL),
    poster, step images; sync-links run; checker OK
[ ] the site published after the wiring, data/links.js included
```
