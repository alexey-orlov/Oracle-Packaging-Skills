# The exemplar builder — filling the reference deck instead of redrawing it

`tools/build_deck_v2.py` builds the sales deck by opening a copy of the reference
Workforce Optimization deck and **replacing its content**. Nothing here draws a
card, a corner, a fill or a font: geometry, type, colour, corner radius, table
idiom, icons and the running header come from `assets/exemplar/wfo-sales-deck.pptx`
by construction.

This is stage 2 of `docs/DECK-FIDELITY.md`. It exists because the redrawn builder
had to re-derive hundreds of design decisions from measurements, and every one of
them could drift — the owner's seven findings were all drift of that kind.

## How a build runs

```
build_deck_v2.py <pack-spec.yaml> --out <dir> [--channel partner_print|internal]
                 [--fit-report] [--allow-overflow] [--exemplar <pptx>] [--slots <json>]
                 [--icons <map.yaml>]
```

1. `exemplar.open_exemplar()` reads the 15 MB file into memory. **The file on disk
   is never modified.**
2. The one slide type the reference lacks — "why it sells for the partner's
   seller" — is made by `duplicate_slide()` of reference slide 5, whose quadrant
   blocks are the composition the anatomy says it derives from.
3. `arrange()` keeps ten slides in the anatomy's order and drops reference slide 8
   (the third draft of the package table) with its relationship.
4. Each slide is filled through the slot map. Every filled slot is logged against
   the exemplar's own box, type size and line count.
5. The fit report, the architecture summary and the list of pictures still to
   choose print on stdout. A box that would need more lines than both its box and
   the exemplar's own text exits 1 unless `--allow-overflow`.

## The slot map

`assets/exemplar/slots.json` maps a semantic name to a shape id on one exemplar
slide. Ids are `p:cNvPr/@id` values and are stable for that file (its SHA-256 is
recorded in the map; re-derive the map if the exemplar is ever replaced).

| Anatomy slide | Exemplar | What is filled |
|---|---|---|
| 1 Cover | ref 1 (`Title-AI`) | name + one-liner (one placeholder, two paragraphs), ICP, hero photo on the layout |
| 2 Use case | ref 2 | problem card (lead + bulleted named challenges), solution card, KPI chips, anchor strip |
| 3 Verticals | ref 3 | four cards: name, body, icon picture, panel |
| 4 Today → tomorrow | ref 4 | headline, sub-line, vertical case, two band bodies, two picture frames, customer logo |
| 5 Proof | ref 5 | headline, three stat chips, four quadrant blocks, anchor strip, footnote |
| 6 Why it sells | duplicate of ref 5 | headline, tier strip, claims in the quadrant blocks, CTA strip |
| 7 Solution layers | ref 6 | ladder rows from `architecture.stack[]`, the two top-row cards, tier chips |
| 8 Architecture | ref 7 | title, sub-line, app, engine, infrastructure; nodes and arrows rebuilt from the spec |
| 9 Service packages | ref 9 | table: tiers, scope, prices, timing, one row per capability |
| 10 Service packages (detailed) | ref 10 | table: tiers, scope, `<glyph> <prose>` per capability |

### Ambiguous shapes, and how they were resolved

Each of these was decided by rendering the reference slide with QuickLook and
looking at it, then reading the shape's XML.

- **Cover (ref 1) has only three shapes.** The dark ground and the hero photo are
  on the **layout** `Title-AI`, not the slide: `Picture 4` (9.13 × 7.5 in, 2 MB
  PNG) is the hero, `Image 2` is the black freeform mask, and the layout's own
  background is `solidFill tx1`. The hero is pack-specific, so it is a slot
  (`cover.photo`), replaced from `deck.images.cover` or removed — never inherited.
  Removing it leaves the ink ground, which is the explicit empty state.
- **Cover text is one placeholder, not two.** Shape 3 holds the pack name (p0,
  44 pt) and the one-liner (p1, 25 pt). Shape 2 is the tier ladder
  ("PROOF OF VALUE · ROLL-OUT · SCALING"). The tier line is a finding
  (DECK-FIDELITY #2), so its text is replaced by the ICP line — same shape, same
  type, no tier eyebrow anywhere on the deck.
- **The problem card body (ref 2, shape 9) has five paragraph shapes in one box**:
  a lead with a bold clause, a blank spacer, "This leads to the following
  challenges:", and three bulleted paragraphs whose first run is bold. Paragraph 3
  is the bullet prototype; the named challenges are split on the first `:`.
- **Bold/regular splits do not map one run per text.** The exemplar writes its
  lead clause across four bold runs and continues in three regular runs. Text is
  therefore placed into *formatting-distinct* runs (bold/size/colour/typeface), so
  "bold lead + regular tail" lands correctly whatever the run soup underneath.
- **The verticals' icons (ref 3) are 1.06 in white PNGs**, centred on a 2.245 in
  blue panel. They are replaced in place when `assets/icons/map.yaml` exists; with
  no map, or no keyword match, the exemplar's own icon stays and the build says so.
  A numeral is never printed (DECK-FIDELITY #4).
- **Slides 4 and 5 carry the source customer's logo** (a Bosch PNG). It is removed
  unless `clearance.customer_name_allowed[channel]` is true **and**
  `deck.images.customer_logo` is given. With the logo gone, the headline moves to
  the left margin and widens to the content band — the only geometry the builder
  computes on those two slides.
- **The proof slide's four quadrant blocks** are two blue-bar blocks (CONTEXT,
  SOLUTION) and two ink-bar blocks (VALUE FOR ORACLE + NVIDIA, VALUE FOR CLIENT).
  The deck keeps all four rather than deleting two and leaving a hole: CONTEXT ·
  WHAT THE PACK DOES · HOW IT RUNS (the workflow) · WHAT IT DOES NOT CLAIM (the
  divergence and the caveat). The partner-value block moves to slide 6, as the
  anatomy says.
- **The ladder's row 0 (ref 6) is not a peer of rows 1 and 2.** It carries two
  white sub-cards and three tier chips and has no summary box or vendor badge.
  Rows 1..n are the plain rows, and row 1 is the clone prototype.
- **The architecture engine (ref 7, shape 32) is a group**; its text lives in
  child 13. The source boxes are a group (33) and a plain rounded rectangle (36).
  36 is the node prototype — cloning a plain shape is safer than cloning a group,
  and using one prototype for every node satisfies rule 2 (peer geometry).
  Shape 19 is a 0.012 in white bar left over from the reference's own editing; it
  renders as nothing and is deleted.
- **Glyph cells are prototypes, not characters.** `◐` is 11 pt, `●` and `●●` are
  18 pt orange, and "not in this tier" is an em dash in `C2C7CC` at 12 pt. The
  builder copies the paragraph formatting of the matching prototype cell and sets
  only the text, so no glyph size ever comes from code.

## The helpers (`tools/exemplar.py`)

| Helper | What it guarantees |
|---|---|
| `open_exemplar` | works on an in-memory copy; the asset is read-only |
| `arrange`, `duplicate_slide` | slide selection, order and a copy whose picture rels still resolve (the copy re-adds each source rel under the same rId) |
| `set_paragraphs`, `fill_text`, `fill_lines`, `fill_lead`, `fill_points` | text into prototype paragraphs; run formatting, bullets, indents and line spacing survive |
| `replace_picture`, `empty_picture_frame` | a new image in the same frame, centre-cropped via `a:srcRect`; or an explicit dashed container with a caption in the deck's own type |
| `clone_table_row`, `delete_table_row`, `match_row_count`, `set_cell` | table rows cloned from the exemplar's own row; cell formatting never rewritten |
| `clone_shape`, `place_connector`, `set_connector_geom` | peers built from prototypes; connectors pointed with flipH/flipV and an elbow `adj` |
| `clear_notes` | the reference's speaker notes never ship |

## Where the builder does compute a number

Four places, each because the spec's shape differs from the reference's:

1. **The ladder band** (slide 7). Top and bottom come from the exemplar's own
   first and last row; `n` rows are distributed inside it with the exemplar's
   0.16 in gap. With three layers this reproduces the reference exactly. Clones
   are inserted *above* the last row so infrastructure stays at the bottom and the
   vendor tints keep their order.
2. **The architecture columns** (slide 8). System boxes are equal — one height
   for sources and destinations alike — stacked between the exemplar's node top
   and the container's bottom, each column centred in that band. With no
   destination-only system the layout is the exemplar's own two columns at its
   full container width. With one, the container is narrowed from the right to
   free a destination strip at the source boxes' width, both columns are set to
   that one width, a 1.30 in label corridor is kept either side of the container,
   and the container slides left only as far as that corridor allows when it
   would otherwise fall below 4.75 in — the width at which the app box stops
   holding its own name. Inside the container the app, engine and infrastructure
   boxes scale with it, and any one of them that needs more room for its text
   grows downwards, the container growing with it to a floor of 6.80 in. Arrows
   fan into the app box's left edge and out of its right one, elbows turn in a
   corridor beside the container, and each arrow's label is sized to its own text
   and sits immediately above its own line.
3. **The headline shift** on slides 4 and 5 when the customer logo is removed.
4. **Table row heights and the legend** when a spec has more capability rows than
   the reference. Rows that declare more height than their text needs give the
   slack back, tallest slack first. A table that grew past the reference's own row
   count also drops its legend to the slide's bottom line (6.90 in) and prints the
   price disclaimer on the same line rather than under it — a row renders a little
   taller than any estimate, and a legend under the last row is not worth a guess.
   Type is never scaled down; if the table still runs past the bottom line, the
   build says which slide needs a row cut.

## What it deliberately does not do

- **No scaling to fit.** A deck that cannot hold the wording says so; shrinking
  below the reference's type sizes is the failure this rewrite exists to remove.
- **No invented imagery.** Cover, before and after are explicit empty states with
  a stdout line naming the spec key to set. The customer logo is only ever the one
  clearance allows.
- **No new columns.** A spec with a different number of tiers fills what the
  exemplar's four columns hold and says so; column cloning would change the table
  idiom.
- **No short product names.** `NeMo`, `cuOpt` and `NIM` are spellings the catalog
  marks `not_this` on their own, so the engine box always carries the full name.
- **No id on a slide.** An `items:` entry that looks like a catalog id but is not
  in the catalog is left off the engine box with a note, rather than printed.

## Adding a slot or a variant

1. Render the exemplar slide (`tools/render_probe.sh`, or the QuickLook
   single-slide trick in the rendering reference) and look at it.
2. Find the shape id — any inventory dump of `p:cNvPr/@id` will do — and add it
   under that slide's `slots` in `assets/exemplar/slots.json`, with a note if the
   shape is ambiguous.
3. Fill it with `fill_text` / `fill_lines` / `fill_points` and log it with
   `self.log(<slide>, "<slot>", shape, text)`. Never set a size, a colour or a
   position unless the section above already justifies one.
4. Rebuild the fixture, render it, and compare the contact sheet with the
   reference before anything else.

A **new slide type** is a `duplicate_slide()` of whichever exemplar slide has the
composition it needs, plus an entry in `slots.json` naming the source and the
mapping (see `why_it_sells`).

## Limits found while building this

- **A destination column costs the platform its width.** Two system columns at the
  source boxes' own width plus their two label corridors leave about four inches
  of the canvas for the container, against the exemplar's 7.31. The platform's
  boxes hold their text at that width, but only just — which is why 4.75 in is a
  floor, not a preference, and why a spec with three or more destination-only
  systems is worth questioning before it is drawn.
- **The cover has no subheading slot.** `meta.name_variants.external_subheading`
  is not printed on slide 1; the build says so. It is still the one-pager's.
- **Three tier columns.** The exemplar's tables are 4 columns; a spec with more or
  fewer tiers fills what fits and the build reports it.
- **The fit model is per paragraph, not per box.** `log_shape` measures each
  paragraph against the whole box, so a two-paragraph box that overflows only in
  sum passes the report. The architecture slide sizes its own boxes from the sum
  instead; elsewhere the render is what catches it.

## What was fixed downstream of this builder

- **`lint_deck.py` is now measured from the exemplar** and passes on the exemplar
  itself (`--reference`), on this builder's output and on the legacy builder's.
  Its corner check counts only a real radius (adjustment over 20 000 — the
  reference's structural boxes sit at 4 000–12 000) and fails any rounded shape
  over 0.55 in tall; its destination check accepts a box per output system.
- **`lint_artifact.py` ART101 no longer fires on correct spellings.** The catalog
  marks `NVIDIA Nemo` and `Nvidia NIM` `not_this` for a capital letter, and
  `covered_by_good_name` used to suppress only a match a *longer* accepted name
  contained. It now suppresses a match an accepted name occupies at any relative
  length, and requires an exact spelling when the two spans are the same — so
  `NVIDIA NeMo` is clean and `NVIDIA Nemo` is still a finding.
