# Deck fidelity — why the sales deck drifts from the reference, and the rewiring

_Written 2026-09-22 from the owner's review of the first Account Insights sales deck. This is the plan the deck work follows; the skill and reference files are rewritten to current truth as each stage lands._

## The diagnosis, in one sentence

The deck is **redrawn** from measured numbers on a 41 KB stripped base, so fidelity to the Workforce Optimization reference deck depends on hundreds of hand-coded choices — corner radius, fonts, header text, icons versus numerals, box labels — each of which can drift, and **nothing checks the output against the reference** before the owner sees it.

The owner's findings, mapped to that cause:

| Finding | Where it came from |
|---|---|
| Header says "OCI AI Accelerators" | a default string in the builder; the mini-site lockup says "Oracle AI & Data Solutions" |
| Cover unlike the reference cover; a tier subtitle nobody asked for | the base has no dark title layout, so the cover is drawn, and the builder invented an eyebrow |
| Rounded blocks on the use-case slide | `rounded=True` hard-coded in the drawing helpers; the reference cards are square |
| Numerals instead of icons on the verticals | the plugin ships no icon library, so the builder prints numbers |
| Empty image slots on today → tomorrow with no way to fill them | no asset step; no picker |
| Architecture: generic "Accelerator business app", an unnamed engine, a source box pointing nowhere, an arrow from the app back to the feeds, the destination system missing | the diagram is drawn from three fixed boxes, not derived from the spec's inputs, stack and outputs; no naming rule; no reviewer |
| Font and size problems on the package slides; a wordy detailed table in small type | per-cell sizes chosen by code, no floor, no word budget enforced |

## The rewiring — four moves

1. **Clone, don't redraw.** The reference deck becomes the exemplar: its own slides, one per slide type, with named content slots. The builder fills slots — text runs keep their formatting, pictures are replaced in place, table rows are cloned — and never draws a card, a corner or a font. Geometry, fonts, corners, icons and the header come from the exemplar by construction. (`tools/build_deck_v2.py` + `assets/exemplar/`.)
2. **A deck linter against the reference**, run before the owner sees anything: fonts in the brand set only; the running header text; no tier eyebrow on the cover; corner geometry per slide as in the reference; icons not numerals on the verticals; the architecture slide's naming and flow rules; type-size floors and word budgets on the package tables; ten slides in order. (`tools/lint_deck.py`, exit 1 with plain messages.) **The cover hero is enforced here too** (added 2026-09-23, after the owner found a plain black title slide on a sales deck): the cover must sit on the reference's own `Title-AI` photo layout with a picture reaching it, so an ink-only cover cannot pass — the legacy redraw builder fails this by construction, and only `--legacy-cover-ok` demotes it to a loud warning, on that documented path and never on a deck being delivered. **The proof slide's composition is enforced here too** (added 2026-09-23, after the owner found a delivered case told as generic pack copy): the reference's four quadrant labels in order, three stat tiles that are never empty, and the customer's logo on slide 5 exactly when the brief clears the name for that channel and names a logo file — cleared with no file warns, no clearance means no picture, and the legacy redraw, which draws its own slide 5, is demoted to a warning by the same flag.
3. **A dedicated diagram step with its own QA.** The architecture diagram is derived from the spec (inputs → the pack's app → engine → infrastructure → destinations) under naming and flow rules — the app box carries the pack's name "by SoftServe"; the engine box names the vendor products from the catalog (NVIDIA NeMo Agent Toolkit, AI-Q); every input has a labelled arrow into the app; every output has a destination box (Oracle CX, or any CRM); no arrow from the app back to a source unless the spec says write-back — and it is reviewed by a **fresh-context reviewer** (a subagent given only the render, the rules and the spec, never the build context) before it enters any artifact. The same diagram data feeds the one-pager's architecture strip and the mini-site.
4. **Visual assets with human choice.** Icons per vertical come from a curated library (seeded from the reference deck's own icons); photos for today → tomorrow are proposed as three candidates per slot, shown in the side panel, and chosen by the owner in a widget — never invented. Until chosen, the slot is an explicit empty container. The slot list is extensible: the reference cover carries a photo on its right half, so a `cover` slot is the next one to add. The owner used to hand-pick these (2026-09-22); the skill now searches openly licensed sources itself — only sources whose licence permits commercial use without attribution, with the licence and creator recorded per file (`shared/references/visual-assets.md`). The icon library lives in `shared/data/icons/`, shared by the deck, the one-pager and the site, seeded from the reference deck and grown by each choice.

**The exemplar lives in the repo** (`assets/exemplar/`, read-only, ~15 MB, never edited in place): a plugin must work in any session and on any machine where it is installed, and a file on OneDrive can be edited by anyone and silently change the template; a repo asset changes only by a deliberate commit.

The loop for every visual artifact becomes: build → lint against the reference → render → reviewer pass (not the builder) → fix → then the owner.

## Stages

| Stage | What lands | Status |
|---|---|---|
| 1 | Quick fixes on the current builder (header, cover eyebrow, square corners, icon seeds, architecture naming and flows, package-table floors) and `lint_deck.py` | landed 2026-09-22 — the linter finds 22 defects on the pre-fix deck and none on the fixed one; the reference's structural corners measure 0.04–0.18 in, square at slide scale, so square it is |
| 2 | The exemplar builder (`build_deck_v2.py`) with the slot map, acceptance-tested by rebuilding the reference deck from its own spec and comparing renders side by side | landed 2026-09-23 — the fixture build is indistinguishable from the reference except where the anatomy says it differs, and the variability spec (3 verticals, 7 capability rows, a 3-product engine, a destination-only system) builds with no drawing change. `build_deck_v2.py` is the skill's builder; `build_deck.py` stays as the legacy redraw for a machine without the exemplar. `lint_deck.py` is re-based on the exemplar and holds five verdicts: green on the exemplar itself (`--reference`) and on the v2 fixture, red on the legacy fixture (its cover is ink only) and green on that same deck under `--legacy-cover-ok`, and red on a copy broken four ways |
| 3 | The diagram step with the reviewer pass, shared by deck, one-pager and listing | rules and checklist in `shared/references/architecture-diagram.md`; the reviewer pass is step 6 of the deck skill — a fresh-context subagent given only the slide-8 render, the spec's architecture component and that file. Landed for the deck 2026-09-23; the one-pager's strip and the mini-site's view still derive their own |
| 4 | The `visuals` skill: icons per vertical from permissively licensed open sets (Tabler, Lucide), photos from sources whose licence allows commercial use without attribution (Openverse CC0/public domain, Pexels, Unsplash), three candidates per slot shown in the side panel, the owner picks in a widget, provenance recorded per file; never a search-engine image | landed 2026-09-22 — icons and the public-domain photo pool need no key; the photo step needs a free Pexels key in the Keychain (`PEXELS_API_KEY`), because the keyless pool is archive material with no modern office scenes; the cover photo is the next slot |

## Acceptance

The fixture (the anonymized Workforce Optimization spec) builds to a deck whose contact sheet is indistinguishable from the reference deck in layout, fonts, corners, header and icons; only the content differs where the anatomy says it does (the added "why it sells" slide, the dropped duplicate table). A second spec with three verticals and seven package rows builds without a drawing change. The linter is green on both and red on a deck with any of the seven findings above re-introduced.
