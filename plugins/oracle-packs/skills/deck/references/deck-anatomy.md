# Sales deck — the 10-slide anatomy

The shape of an accelerator-pack sales deck, slide by slide: what each slide is
for, which of the 12 pack components it carries, which exemplar slide it is
filled from, what varies with the spec, what is removed, and how much text fits.

**The deck is filled, not drawn.** `tools/build_deck_v2.py` opens a copy of the
reference Workforce Optimization deck — `assets/exemplar/wfo-sales-deck.pptx`,
10 slides, 13.33 × 7.5 in — keeps the slides this anatomy maps to, duplicates the
one slide type the reference lacks, and then only ever replaces content: text
runs keep their own formatting, pictures are swapped inside their frames, table
rows are cloned from the exemplar's own row. Geometry, type sizes, colours,
corner radii and the table idiom therefore come from the exemplar by
construction, and are not restated here. The slot map is
`assets/exemplar/slots.json`; the mechanics and the few places the builder does
compute a number are in `exemplar-builder.md`. Colours and fonts, for reading a
render: `brand-tokens.md`. The numbers the linter holds a build to:
`reference-geometry.json`.

## The ten slides, and where each comes from

The reference carries **three alternates of the same package table** on slides
8, 9 and 10 (no infra row / with infra row / prose per cell) — a working
artifact, not a shipped structure. Alex's 2026-09-18 decisions add two slides the
reference folded into one: a dedicated **"why it sells for the partner's
seller"** slide, and the **solution-layers ladder** as its own slide.

| # | This anatomy | Exemplar slide |
|---|---|---|
| 1 | Cover | 1 Cover (`Title-AI` layout) |
| 2 | Use case | 2 `USE CASE` |
| 3 | Vertical applications | 3 `VERTICAL APPLICATIONS` |
| 4 | Today → tomorrow | 4 Today \| Tomorrow |
| 5 | Proof | 5 proof / commercial case (its "VALUE FOR ORACLE + NVIDIA" quadrant moves to slide 6) |
| 6 | Why it sells for the partner's seller | a duplicate of 5 — it was a quadrant on that slide |
| 7 | Solution layers | 6 `TECHNOLOGY STACK` (the ladder half) |
| 8 | Architecture | 7 `Architecture` |
| 9 | Service packages | 9 (the alternate **with** the infra row) |
| 10 | Service packages (detailed) | 10 `…PACKAGES (DETAILED)` |

Exemplar slide 8 (the table without the infra row) is dropped: a deck ships one
table, not three drafts of it.

## Standing furniture

Slides 2–10 carry the running header — **`Oracle AI & Data Solutions — <pack
name>`**, the same lockup as the mini-site, so a seller who has seen the site
recognises the deck. It is the exemplar's own header placeholder (idx 34) with
its text replaced, so the face, size, colour and alignment are the reference's;
`deck.running_header` overrides the wording. The cover carries no header and no
page number. Content titles are the exemplar's title placeholder, uppercased.

## Corners

The reference draws structure **square**. Its cards, panels and diagram boxes are
`roundRect` with adjustments of 4 000–12 000 — a 0.04–0.18 in radius on shapes
several inches wide, which reads square at slide scale. The only real pills are
its KPI chips and its vendor badges (adjustment 50 000), and both are under half
an inch tall. The builder never sets a corner; the linter holds a build to the
reference's own counts per slide and fails any rounded shape over 0.55 in tall as
a rounded card.

Word budgets below are the estimator's (Liberation-metric stand-in, +6 % safety,
1.22 line factor), stated as the *maximum before the box overflows*. The
comfortable target is about two thirds of it; a box filled to the brim reads as a
wall.

---

## 1 — Cover

**Purpose.** Name the pack and say the job it does, in the reference deck's own
composition.

**Components.** 4 name (the channel's variant) · 2 one-liner · 3 ICP.

**Filled from exemplar slide 1.** The dark ground and the hero photo are on the
`Title-AI` **layout**, not the slide; the slide carries three shapes. One
placeholder holds the pack name (paragraph 0, 44 pt) and the one-liner
(paragraph 1, 25 pt) — `one_liner.short` is what fits that block.

**Removed.** The reference's tier ladder low on the cover
("PROOF OF VALUE · ROLL-OUT · SCALING") — the owner's 2026-09-22 review dropped
it. A cover names the pack and what it does; the packages are slides 9 and 10.
That shape is reused for the ICP line, so the composition keeps its lower block.
The reference pack's **hero photo** is removed too, unless `deck.images.cover`
names one to swap in: it is that pack's picture, not this one's. Removed, the
layout's own ink ground is the cover, an explicit empty state, and the build says
which picture is still to choose.

**No subheading slot.** The exemplar's cover has nowhere for
`meta.name_variants.external_subheading`, so it is **not printed on slide 1** and
the build says so. It stays available to the artifacts that do have a place for
it — the one-pager's lockup above all.

**Budgets.** Name ≤ 26 characters on one line at 44 pt · one-liner ≤ 30 words ·
ICP ≤ ~40 words.

**Rules.** 8 — the dark ground is the one heavy ink field in the deck. 13 —
nothing internal on the cover.

---

## 2 — Use case

**Purpose.** The reader's problem in their own words, then the reframe and what
the pack actually does.

**Components.** 1 problem ↔ solution (including `reframe`) · 11 KPI names as
direction chips · 9/10 the anchor line naming the required products.

**Filled from exemplar slide 2.** Two peer cards; the problem body is one box of
prototype paragraphs — a lead with a bold clause, a blank spacer, "This leads to
the following challenges:", then one bullet per named challenge cloned from the
exemplar's own bullet. Up to three KPI chips; a chip with nothing to say is
removed, never left empty.

**Varies with the spec.** The number of named challenges (`problem_points[]`) and
the number of chips (`kpis[]`, up to the exemplar's three).

**Budgets.** Problem card ≤ 165 words (a lead sentence plus three named
challenges is the shape; ~60 words reads best) · solution card ≤ 130 words · each
chip ≤ 3 words · anchor strip one line, ≤ 25 words.

**Rules.** 2 — the two cards are identical boxes. 5 — problem neutral, solution
blue: two stages of one dimension.

---

## 3 — Vertical applications

**Purpose.** Show the pack is not one customer's project: four industries, each
with one concrete line.

**Components.** 5 verticals (`name` + `what_matters_here`, falling back to
`framing.solution`).

**Filled from exemplar slide 3.** Four identical cards, each with a full-height
blue panel carrying a 1.06 in icon picture, the industry name, a rule and the
body.

**Icons, never numerals.** The picture is replaced in place from the shared icon
library at `shared/data/icons/` — white line art on a transparent ground, matched
by keyword against the industry's name (`map.yaml`). Nothing matches → the card
keeps the exemplar's own icon and the build names that industry on stdout, so the
skill can ask the owner which picture it should carry. A number in a card is a
bug, and the linter fails on one.

**Varies with the spec.** Fewer than four verticals greys the unused card and its
panel (rule 3: an empty container, never a gap).

**Budgets.** Name ≤ 11 words over two lines · body ≤ 28 words.

---

## 4 — Today → tomorrow

**Purpose.** The narrative form of the reframe: what the day looks like now and
what it looks like with the pack.

**Components.** 1 problem ↔ solution (`today` / `tomorrow`, falling back to
problem / solution) · 2 one-liner · 5 the named vertical case.

**Filled from exemplar slide 4.** Headline, sub-line, the named vertical case,
two labelled bands with their bodies, and the two picture frames. TOMORROW's band
is orange here rather than blue — the exemplar's own choice, kept.

**Removed.** The source customer's logo, unless
`clearance.customer_name_allowed[channel]` is true **and**
`deck.images.customer_logo` names a file. With it gone the headline moves to the
left margin and widens to the content band — the only geometry the builder
computes on this slide.

**The two pictures.** `deck.images.today` and `deck.images.tomorrow` name the
files — absolute, or relative to the pack brief's own folder. Each is centre-
cropped to its frame, so any aspect ratio lands cleanly. Without them the frame
stays an explicit empty container (rule 3) labelled "image to be chosen", and the
build says which one is missing. The brief is the reference's own pairing: the
bad current experience on the left, the good future with the solution on the
right.

**Budgets.** Headline one line ≤ 12 words · each body ≤ 54 words.

---

## 5 — Proof

**Purpose.** One delivered engagement, its numbers, and honest boundaries.

**Components.** 11 the single metric set with its attribution and caveat ·
`meta.source_engagement`.

**Filled from exemplar slide 5.** Headline, three stat tiles (value + label), and
the first two of the four quadrant blocks — `CONTEXT` and the pack's own
description, the two that carry blue bars — plus the anchor strip and the
footnote.

**Removed.** The source customer's logo, on the same clearance rule as slide 4.

**Rules.** 11 — **peer claims are all or none**: a metric whose `channels` list
excludes this channel drops the entire stat strip, and the build says so.
Customer naming follows `clearance.customer_name_allowed.<channel>`; otherwise
`anonymized_descriptor`.

**Budgets.** Headline ≤ 13 words · stat value ≤ 27 characters · stat label ≤ 10
words · each block ≤ ~80 words.

---

## 6 — Why it sells for the partner's seller

**Purpose.** The slide the partner's account exec actually needs: what this pack
does for *their* number. Added by Alex's 2026-09-18 decision.

**Components.** 12 `packages.why_it_sells_for_the_partner` ·
`packages.target_oci_consumption` · contact for the channel.

**Filled from a duplicate of exemplar slide 5.** The anatomy's slide 6 has no
reference slide of its own — it was the "VALUE FOR ORACLE + NVIDIA" quadrant of
the proof slide. The builder duplicates slide 5 and fills the four quadrant
blocks with the seller claims, ink-bar pair first so the partner-value colour
leads; the consumption line takes the anchor strip and the contact takes the
footnote.

**Removed.** The stat strip and the customer logo — they belong to the proof
slide, and repeating them here would read as a second proof.

**Budgets.** Claim ≤ 24 words · detail ≤ 36 words · CTA ≤ 12 words · contact one
line.

**Rules.** 13 — this is partner-facing: no headcount, no internal package prices.

---

## 7 — Solution layers

**Purpose.** Who owns what in the stack, bottom to top, with the value arrow.

**Components.** 8 `architecture.stack[]` (layer, vendor, summary/items).

**Filled from exemplar slide 6.** The top row of the ladder carries the two white
sub-cards (what comes ready / what is tailored) and one chip per tier; the rows
below are the plain layer rows, each with its name, summary and vendor badge.

**Varies with the spec.** A stack with more layers than the exemplar's three
clones the exemplar's own plain row and redistributes the ladder band (2.85 →
6.71 in) with its 0.16 in gap; clones go *above* the last row, so infrastructure
stays at the bottom and the vendor tints keep their order.

**Budgets.** Layer name ≤ 11 words · summary ≤ 35 words · vendor badge ≤ 4 words.

**Rules.** 5 and 12 — vendor is the colour dimension, and layers differ in tint
*and* in the weight of their bar.

---

## 8 — Architecture

**Purpose.** Inputs, the platform, outputs — and where the integration effort
actually lands, per tier.

**Components.** 8 architecture inputs / stack / outputs · 9 and 10 the Oracle
products with their per-tier `integration` claims.

**Filled from exemplar slide 7**, whose frame is two columns: the systems the
pack reads on the left, the platform container on the right holding the app box,
the engine box and the infrastructure line. The nodes and every arrow are rebuilt
from the spec inside that frame.

**Naming — the diagram is derived from the pack brief, not hard-coded.**

- **The app box** is `<pack name> by SoftServe` (the channel's name variant), with
  the app layer's summary as its sub-line. Never a generic "accelerator business
  app".
- **The engine box** names the products the engine layer runs, by their catalog
  names (`catalog_id` and `items`, resolved against
  `shared/data/oracle-products.yaml`) — "NVIDIA cuOpt", or "NVIDIA NeMo Agent
  Toolkit + NVIDIA NIM". Always the full name: `NeMo`, `cuOpt` and `NIM` are
  spellings the catalog marks `not_this` on their own. An `items:` entry that
  looks like a catalog id but is not in the catalog is left off with a note,
  never printed as an id. An unnamed "agentic engine" is a bug.
- **The infrastructure line** keeps the infrastructure layer's name and items.
- **Every system box** carries the system's name, and a second line only when the
  catalog says what that system is. What flows travels on the arrow, so a data
  string is never printed twice.

**Flows.**

- Every `architecture.inputs[]` box gets **its own labelled arrow into the app**;
  the label is what that source sends.
- Every `architecture.outputs[]` system gets **its own labelled arrow out of the
  app**, and a box carrying its name.
- **No arrow from the app back to a source** unless that same system also appears
  in `architecture.outputs[]` — then it is a second, separately labelled arrow
  (the write-back) leaving the source box a little below the first, and only
  then.

**The layout rule — a right column only for destination-only systems.**

A system that is both an input and an output is one box on the left with two
arrows. When every output is a write-back like that, the diagram stays the
exemplar's own two columns at the reference's full container width.

When the spec names a system that **receives the result and is not also a
source**, the diagram becomes three columns: the platform container is narrowed
from the right, and the destination boxes stand in the freed strip at the source
boxes' own geometry — same prototype, same width, same height, so a source and a
destination read as peers (rule 2). Both system columns are set to one width, and
a corridor of 1.30 in either side of the container carries the arrow labels, each
sitting immediately above its own line. The container never narrows below 4.75 in
— under that the app box stops holding its own name — so with two full-width
system columns it also slides left, no closer to the source column than the label
corridor. Where a platform box then needs more room for its text than the
reference gave it, it grows downwards inside the container and the container
grows with it, to a floor of 6.80 in; type is never scaled down.

**The summary.** The builder prints the whole diagram in plain words — boxes,
then arrows — so the skill can put it to the owner without describing a picture
nobody has opened yet. That summary, the slide render, and
`shared/references/architecture-diagram.md` are what the fresh-context diagram
reviewer gets.

**Budgets.** System box ≤ 8 words · app and engine box ≤ 24 words including the
sub-line · arrow label ≤ 12 words. All of them are in the fit report.

**Rules.** 7 — an arrow carries a text label; a bidirectional relation is two
labelled arrows, not one box. Every integration claim states its tier
(`oracle_products[].integration.{pov,integration,scaling}`), Alex's 2026-09-18
decision: the one-pager and the feature list were both right, at different tiers.

---

## 9 — Service packages

**Purpose.** The commercial table: what each tier costs, how long it runs, and
what it includes.

**Components.** 12 tiers with services price, monthly infrastructure price and
duration · per-capability handling as glyphs.

**Filled from exemplar slide 9** — an 11 × 4 table: header, package scope,
services price, infrastructure price, timing, then one row per capability. Row 5
is the capability prototype, and its cells carry the glyph runs the builder
reuses, so the glyph type never comes from code.

**Varies with the spec.** One row per `packages.capability_handling[]` entry,
cloned from that prototype. A table that grows past the exemplar's own row count
reclaims the slack the exemplar left in its rows — a row whose declared height
exceeds what its text needs gives the difference back, tallest slack first — and
reports it rather than shrinking type.

**Type floor, 10.5 pt** — the smallest cell the reference's own table carries.
Nothing on this slide goes below it; a table that still will not fit is a
wording problem, and the build says which slide needs a row cut.

**Glyphs.** `◐` partial · `●` included · `●●` multi-region / advanced · `—` not
in this tier. Derived from `packages.capability_handling[]`: an empty or `—` cell
is "not in this tier"; otherwise the tier default (pov `◐`, integration `●`,
scaling `●●`). A `glyphs:` map on the entry overrides per tier. All three marks
keep the exemplar's own symbol face — neither brand face carries them, and a
renderer that substitutes a different face per glyph draws them at visibly
different sizes (the owner, 2026-09-22).

**Budgets.** Label column ≤ 10 words · tier scope cell ≤ 12 words.

**Rules.** Prices carry a `*` and a footnote whenever `status: indicative`; a
`tbd` price prints "To be defined", never a guess. Tier names come from the spec
(`PoV Jumpstart` / `Integration` / `Scaling`); the S/M/L letters are size tags
appended to the name, not the name.

---

## 10 — Service packages (detailed)

**Purpose.** The same table with prose in every cell — the version a seller reads
out in a scoping call.

**Filled from exemplar slide 10** — an 8 × 4 table: header, scope, one row per
capability, each cell `<glyph>  <prose>` in one paragraph (the glyph is run 0 at
16 pt, the prose the last run at 9 pt). Row 2 is the prototype.

**Type floor, 9 pt** — again the smallest cell the reference's own table carries.

**Budgets.** Every cell ≤ **12 words** — a line a seller reads out in a scoping
call, not a paragraph. A longer cell is an overflow in the fit report, and it is
fixed by shortening the wording in the pack brief, never by shrinking the type.

**Rules.** 11 — every tier column gets the same rows; a capability with nothing
in a tier shows `—`, which is a scope statement, not missing evidence.

---

## Spec keys the deck reads

Everything below the line is optional with a fallback, so a spec that carries
only the base schema still builds.

**Required:** `meta.name` (or `meta.name_variants`), `one_liner.full|short`,
`problem_solution.{problem,solution}`, `packages.tiers[]`,
`architecture.stack[]`, and `architecture.inputs[]` or `architecture.outputs[]`.

**Optional, deck-specific:**

| Key | Effect |
|---|---|
| `problem_solution.problem_points[]` | the named challenges on slide 2 |
| `problem_solution.reframe` / `reframe_question` | slide 2 solution heading / slide 4 headline |
| `problem_solution.today` / `tomorrow` | slide 4 band bodies (else problem / solution) |
| `kpis[].chip` | slide 2 chip label (else `name`) |
| `kpis[].label` | slide 5 stat caption (else `formula` / `name`) |
| `kpis[].show_baseline` | renders `baseline → figure` |
| `kpis[].channels[]` | restricts a metric to channels; any restriction drops the whole strip |
| `packages.tiers[].scope_line` | tier scope sentence (else the first `what_you_get`) |
| `packages.capability_handling[].glyphs` | per-tier glyph override |
| `packages.anchor_line` | slide 2 anchor strip (else built from required products) |
| `packages.target_oci_consumption` | slide 6 consumption line |
| `deck.running_header` | `"Oracle AI & Data Solutions — {name}"` by default |
| `deck.images.cover` | the hero photo on slide 1 (else the layout's ink ground) |
| `deck.images.today` / `deck.images.tomorrow` | the two pictures on slide 4 |
| `deck.images.customer_logo` | the logo on slides 4 and 5, when clearance allows the customer's name |
| `verticals[].icon` | the industry icon on slide 3 (else matched by keyword) |
| `architecture.stack[].catalog_id` (engine layer) | the products the engine box names |
| `deck.vertical_case`, `deck.seller_lead`, `deck.cta`, `deck.proof_headline`, `deck.layers_sub`, `deck.architecture_sub` | the short editorial lines |

## Channels

`--channel partner_print` (default) uses the external name variant, the
`contacts.partner_print` block, and refuses the customer name unless
`clearance.customer_name_allowed.partner_print` is true. `--channel internal`
uses the `internal_slide` name variant and `contacts.internal`. Nothing else
differs — an internal deck is not a licence to print internal operating numbers
(rule 13); those never reach a slide.

## Definition of done

1. `build_deck_v2.py … --fit-report` exits 0 — no box overflows, no cell over its
   word budget.
2. `lint_deck.py <deck> --spec <spec> --channel <channel>` exits 0 — ten slides,
   the running header, no tier line on the cover, the reference's own faces, no
   rounded card and no more pills than the reference's slide has, an icon per
   industry, the architecture's names and flows, table type at or above the
   reference's floor.
3. A contact sheet of all ten renders has been looked at (`tools/render_probe.sh`
   prints how to make one on this machine), and slide 8 has been through the
   diagram reviewer.
4. The clearance linter and the consistency check pass on the built file.
5. The builder's notes have been read and acted on — especially the picture slots
   on slides 1 and 4, any industry that fell back to the exemplar's own icon, and
   the architecture summary.

## Appendix — the legacy builder

`tools/build_deck.py` is the earlier builder: it **redraws** all ten slides on
the 41 KB brand shell `assets/softserve-deck-base.pptx`, from measurements rather
than from the exemplar. It exists for a machine or an install that does not carry
the 15 MB exemplar, and it is a fallback, not a choice — every fidelity finding
in `docs/DECK-FIDELITY.md` came from redrawing. Its geometry constants live in
the builder itself and in `brand-tokens.md` (content band 0.42 → 12.91, title box
0.39 / 1.40 / 11.80 × 0.95, the cover block and the icon and picture slots in
`reference-geometry.json`). It builds the same anatomy, passes the same linter,
and differs in the details a redraw cannot inherit: it adds numeral badges the
reference's proof and seller slides do not have, and its architecture slide draws
one destination box listing every output system rather than a box per system.
