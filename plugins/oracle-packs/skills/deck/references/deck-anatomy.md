# Sales deck — the 10-slide anatomy

The shape of an accelerator-pack sales deck, slide by slide: what each slide is
for, which of the 12 pack components it carries, the geometry it uses, how much
text fits, and which design rules bind it. `tools/build_deck.py` implements
exactly this — one function per slide, geometry from this page.

Measured from the Workforce optimization sales deck (10 slides, 13.33 × 7.5 in,
Jul 2026), which is the only complete reference in the estate. Colours, fonts
and the content band live in `brand-tokens.md`.

## What changed from the reference deck

The reference carries **three alternates of the same package table** on slides
8, 9 and 10 (no infra row / with infra row / prose per cell) — a working
artifact, not a shipped structure. Alex's 2026-09-18 decisions add two slides
the reference folded into one: a dedicated **"why it sells for the partner's
seller"** slide, and the **solution-layers ladder** as its own slide. The 10
slots are therefore:

| # | This anatomy | Reference deck |
|---|---|---|
| 1 | Cover | 1 Cover (`Title-AI`) |
| 2 | Use case | 2 `USE CASE` |
| 3 | Vertical applications | 3 `VERTICAL APPLICATIONS` |
| 4 | Today → tomorrow | 4 Today \| Tomorrow |
| 5 | Proof | 5 proof / commercial case (its "VALUE FOR ORACLE + NVIDIA" block moves to slide 6) |
| 6 | Why it sells for the partner's seller | — (was a quadrant on slide 5) |
| 7 | Solution layers | 6 `TECHNOLOGY STACK` (the ladder half) |
| 8 | Architecture | 7 `Architecture` |
| 9 | Service packages | 9 (the alternate **with** the infra row) |
| 10 | Service packages (detailed) | 10 `…PACKAGES (DETAILED)` |

Reference slide 8 (the table without the infra row) is dropped: a deck ships one
table, not three drafts of it.

## Standing furniture

Slides 2–10 carry the running header — **`Oracle AI & Data Solutions — <pack
name>`**, the same lockup as the mini-site, so a seller who has seen the site
recognises the deck — set explicitly at 9 pt `Replica LL TT`, `6B7076`,
right-aligned in the header placeholder at 6.79, 0.31. `deck.running_header`
overrides the wording; the face, size, colour and alignment are written out on
every slide rather than inherited. The cover carries no header and no page
number. Content titles sit in the 0.39 / 1.40 / 11.80 × 0.95 box, uppercased,
24–26 pt bold ink, **anchored to the top of that box** — anchor it to the middle
and the first content band at y 1.92 collides with it.

## Corners

The reference draws structure **square**. Its cards, panels and diagram boxes
are `roundRect` with adjustments of 4 000–12 000 — a 0.04–0.18 in radius on
shapes several inches wide, which reads square at slide scale. The only real
pills are its KPI chips and vendor badges (adjustment 50 000). So in the
builder `rounded` is opt-in and only three things take it: chips, numeral
badges, and the proof slide's stat tiles (the reference rounds those, gently).
Cards, panels, source and platform boxes, the architecture container and the
package tables are square. The per-slide counts the linter holds the deck to
live in `reference-geometry.json`.

Word budgets below are computed with the same estimator the builder uses
(Helvetica-metric stand-in, +6 % safety, 1.22 line factor) and stated as the
*maximum before the box overflows*. The comfortable target is about two thirds
of the maximum; a box filled to the brim reads as a wall.

---

## 1 — Cover

**Purpose.** Name the pack and say the job it does, in the reference deck's own
composition.

**Components.** 4 name (external variant + `external_subheading` when the
channel is partner_print) · 2 one-liner · 3 ICP.

**No tier line.** The reference carried the three package names low on the
cover; the owner's 2026-09-22 review dropped them. A cover names the pack and
what it does — the packages are slides 9 and 10.

**Layout.** The reference sets its cover on a dark photo layout (`Title-AI`)
the base does not carry, so the ground is drawn as a full-bleed ink `26282B`
rectangle and everything above it keeps the reference's block: a **5.70 in text
column at x 0.55**, the name over the one-liner, and one small line low on the
slide. Every run on the cover is in the theme's title face (`+mj-lt`, Azurio),
as the reference's is; the content slides use the body face.

| Element | x | y | w | size |
|---|---|---|---|---|
| Pack name (white) | 0.55 | 2.30 | 5.70 | 44, autofit to 28, ≤ 2 lines |
| One-liner (`D9E4EC`) | 0.55 | under the name + 0.14 | 5.70 | 25, autofit to 15, down to y 5.00 |
| Subheading (white, bold) | 0.57 | 5.20 | 4.60 | 14, autofit to 10, one line |
| "WHO IT IS FOR" + ICP | 0.57 | 5.62 | 5.70 | 9 / 10 |

Measured from the reference's own placeholders — title block 0.55 / 2.30 /
5.70 × 2.35 at 44 pt over 25 pt, lower line 0.57 / 5.20 / 4.60 × 0.80 at 14 pt
bold (see `reference-geometry.json`, `cover`).

**Budgets.** Name ≤ 26 characters on one line at 44 pt in the 5.70 in column
(two lines at 44, then it shrinks) · one-liner ≤ 30 words · ICP ≤ ~40 words.

**Rules.** 8 — the dark ground is the one heavy ink fill in the deck; no other
slide gets one. 13 — nothing internal on the cover.

---

## 2 — Use case

**Purpose.** The reader's problem in their own words, then the reframe and what
the pack actually does.

**Components.** 1 problem ↔ solution (including `reframe`) · 11 KPI names as
direction chips · 9/10 the anchor line naming the required products.

**Layout.** Two peer cards, rule 2 geometry:

| Element | x | y | w | h |
|---|---|---|---|---|
| Problem card (`F4F6F7`, ink accent bar 0.10) | 0.42 | 1.92 | 6.02 | 3.68 |
| Solution card (`ECF5FB`, blue accent bar 0.10) | 6.89 | 1.92 | 6.02 | 3.68 |
| Card label (14 bold) | +0.35 | +0.18 | 5.40 | 0.30 |
| Card body | +0.34 | +0.58 | 5.40 | 2.92 / 2.30 |
| KPI chips (white, rounded) | 7.25 + i×1.84 | 5.05 | 1.78 | 0.40 |
| Anchor strip (ink, white text, centred) | 0.42 | 5.82 | 12.49 | 0.62 |

**Budgets.** Problem card ≤ 165 words (lead sentence + three named challenges is
the shape; ~60 words reads best) · solution card ≤ 130 words · each chip ≤ 3
words · anchor strip one line, ≤ 25 words.

**Rules.** 1 — the body type scales **up** to 1.35× when the card would
otherwise be half empty. 2 — the two cards are identical boxes. 5 — problem is
neutral grey, solution is blue; the two are stages of one dimension.

---

## 3 — Vertical applications

**Purpose.** Show the pack is not one customer's project: four industries, each
with one concrete line.

**Components.** 5 verticals (`name` + `what_matters_here`, falling back to
`framing.solution`).

**Layout.** A 2 × 2 grid of identical 6.00 × 2.00 in cards at x 0.42 / 6.72,
y 2.48 / 4.76. Inside each card: a 2.25 in full-height blue panel carrying the
industry's **icon**, a 1.06 × 1.06 in picture centred in the panel (the
reference's own measurement), a 0.06 in ink divider, then name (14.5 bold,
3.21 × 0.70 at +2.54/+0.24), a 0.55 × 0.04 rule, and the body (11 pt muted,
3.21 × 0.85 at +1.10).

**Icons, never numerals.** The picture comes from the shared icon library at
`shared/data/icons/` — white line art on a transparent ground, matched by
keyword against the industry's name (`map.yaml`). Nothing matches → the neutral
mark, and the builder names that industry on stdout so the skill can ask the
owner which picture it should carry. A number in a card is a bug, and the
linter fails on one.

**Budgets.** Name ≤ 11 words over two lines · body ≤ 28 words.

**Rules.** 2 — four identical cards; a vertical with a longer name gets smaller
type, never a wider card. 3 — fewer than four verticals leaves a greyed empty
card, never a gap.

---

## 4 — Today → tomorrow

**Purpose.** The narrative form of the reframe: what the day looks like now and
what it looks like with the pack.

**Components.** 1 problem ↔ solution (`today` / `tomorrow`, falling back to
problem / solution) · 2 one-liner · 5 the named vertical case.

**Layout.** Headline (24 pt bold, 0.43 / 1.37 / 12.00 × 0.45), one-liner sub at
1.96, vertical-case label at 2.36. Then two bands: `TODAY` (ink) and `TOMORROW`
(blue) at 2.82, 6.02 × 0.46, bodies at 3.38 (6.02 × 0.92), and the two
**picture slots** at 4.45 (6.02 × 2.15).

**The two pictures.** `deck.images.today` and `deck.images.tomorrow` name the
files — absolute, or relative to the pack brief's own folder. Each is scaled to
cover its slot and cropped to the centre, so any aspect ratio lands cleanly.
Without them the slot stays an empty instance of the same container (rule 3), a
dashed grey box labelled **"image to be chosen"**, and the builder says which
one is missing. The brief for the pictures is the reference's own pairing: the
bad current experience on the left, the good future with the solution on the
right.

**Budgets.** Headline one line ≤ 12 words · each body ≤ 54 words.

**Rules.** 3 — an empty slot is an empty instance of the same container, never a
gap, so the slide is complete before the pictures exist. 5 — ink for today, blue
for tomorrow.

---

## 5 — Proof

**Purpose.** One delivered engagement, its numbers, and honest boundaries.

**Components.** 11 the single metric set with its attribution and caveat ·
`meta.source_engagement` · 7 workflow steps.

**Layout.** Headline at 1.30 (12.49 × 0.55, 16–23 pt). Three stat chips at 2.10,
3.96 × 0.80, at x 0.42 / 4.68 / 8.94 — value 19 pt blue, label 8.5 pt muted.
Two peer blocks (`CONTEXT`, `WHAT THE PACK DOES`) at y 3.10, 6.02 wide, height
**sized to the longer body** (min 1.25 in). Then the workflow as a horizontal
sequence of equal boxes with arrows between, and the footnote carrying the
attribution, the caveat and `divergence_from_pack`.

**Budgets.** Headline ≤ 13 words · stat value ≤ 27 characters · stat label ≤ 10
words · each block ≤ ~80 words at the sized height · step name ≤ 5 words.

**Rules.** 11 — **peer claims are all or none**: a metric whose `channels` list
excludes this channel drops the entire stat strip, and the builder says so. 1 —
the blocks shrink to their content rather than floating text in big cards. 9 —
a true sequence runs horizontally, which also makes the band a different visual
form from the cards above it. Customer naming follows
`clearance.customer_name_allowed.<channel>`; otherwise `anonymized_descriptor`.

---

## 6 — Why it sells for the partner's seller

**Purpose.** The slide the partner's account exec actually needs: what this pack
does for *their* number. Added by Alex's 2026-09-18 decision; on the reference
it was one quadrant of the proof slide.

**Components.** 12 `packages.why_it_sells_for_the_partner` ·
`packages.target_oci_consumption` · contact for the channel.

**Layout.** Up to four peer cards filling the content band: width
`(12.49 − 0.26 × (n−1)) / n`, top y 2.72, height computed from the longest claim
and the longest detail so every card shares one internal baseline grid. Each
card: outlined orange numeral badge (0.30 in) at +0.26/+0.26, claim 14 pt bold,
detail 10 pt muted below a shared 0.18 in gap. Consumption strip (blue tint,
blue bar) below. CTA strip in ink at 6.16, 12.49 × 0.52 — question left, contact
right.

Claim text is split on an em dash: `headline — supporting clause`.

**Budgets.** Claim ≤ 24 words (three cards) · detail ≤ 36 words · CTA ≤ 12 words
· contact one line.

**Rules.** 8 — outlined badge with an ink/orange numeral, never a filled ink
circle; the CTA strip is the one dark band on the slide. 2 — card heights and
the internal baseline are computed across all cards in a pre-pass, so no card
jumps. 13 — this is partner-facing: no headcount, no internal package prices.

---

## 7 — Solution layers

**Purpose.** Who owns what in the stack, bottom to top, with the value arrow.

**Components.** 8 `architecture.stack[]` (layer, vendor, summary/items).

**Layout.** A vertical ladder filling y 2.78 → 6.28: `n` rows of height
`(3.50 − 0.14 × (n−1)) / n`, each a tinted rounded panel 0.95 → 12.40 with a
0.06 in accent bar. Layer name 14 pt bold at x 1.30 (3.10 wide), a hairline at
4.55, the summary at 4.80 (5.05 wide), and a white vendor badge 2.05 × 0.38 at
x 10.15. A thin rule at x 0.57 spans the ladder with "▲ business value" above it.

**Budgets.** Layer name ≤ 11 words · summary ≤ 35 words · vendor badge ≤ 4 words.

**Rules.** 5 and 12 — vendor is the colour dimension and each layer differs in
tint *and* in the weight of its bar; the tints are the fixed ladder in
`brand-tokens.md`, so the same vendor is the same colour on every pack.

---

## 8 — Architecture

**Purpose.** Inputs, the platform, outputs — and where the integration effort
actually lands, per tier.

**Components.** 8 architecture inputs / stack / outputs · 9 and 10 the Oracle
products with their per-tier `integration` claims.

**Layout.** Three columns across the content band (y 2.62 → 6.28), reading left
to right — where the data comes from, what runs, where the result goes — with
the two gaps as arrow lanes:

| Column | x | w |
|---|---|---|
| Source boxes (blue, one per input, up to 3) | 0.42 | 2.55 |
| arrow lane in | 3.06 | 1.12 |
| Container (white, hairline outline) | 4.18 | 5.02 |
| arrow lane out | 9.29 | 1.12 |
| Destination box (blue) | 10.41 | 2.50 |

Inside the container, boxes 4.42 wide: the app box (blue) at +0.40, the engine
box (grey) at +1.62, each 0.98 tall, and the infrastructure line at +2.78.
Everything is square.

**Naming — the diagram is derived from the pack brief, not hard-coded.**

- **The app box** is `<pack name> by SoftServe` (the channel's name variant),
  with the app layer's items as its sub-line. Never a generic "accelerator
  business app".
- **The engine box** names the products the engine layer runs, by their catalog
  names (`catalog_id`, one id or a list, resolved against
  `shared/data/oracle-products.yaml`) — "NVIDIA cuOpt", or
  "NVIDIA NeMo Agent Toolkit · NVIDIA AI-Q Blueprint". The layer's own label is
  at most the small caption underneath. An unnamed "Agentic engine" is a bug.
- **The infrastructure line** keeps the infrastructure layer's name and items.
- **The destination box** lists the `architecture.outputs[]` systems, joined
  with " · ", in the same style as the source boxes. Nothing named → an empty
  container labelled "destination to be named", and the builder says so.

**Flows.**

- Every `architecture.inputs[]` box gets **its own labelled arrow into the app**;
  the label is what that source sends.
- One labelled arrow from the app to the destination box, labelled with what the
  outputs carry.
- **No arrow from the app back to a source** unless that same system also
  appears in `architecture.outputs[]` — then it is a second, separately
  labelled arrow (the write-back), and only then.

**The summary.** The builder prints the whole diagram in plain words — boxes,
then arrows — so the skill can put it to the owner without describing a picture
nobody has opened yet.

**Budgets.** Source box ≤ 8 words · destination box ≤ 12 words · app and engine
box ≤ 24 words including the sub-line · arrow label ≤ 12 words · the integration
footnote ≤ 79 words. All of them are in the fit report.

**Rules.** 7 — an arrow carries a text label; a bidirectional relation is two
labelled arrows, not one box. Every integration claim states its tier
(`oracle_products[].integration.{pov,integration,scaling}`), which is Alex's
2026-09-18 decision: the one-pager and the feature list were both right, at
different tiers.

---

## 9 — Service packages

**Purpose.** The commercial table: what each tier costs, how long it runs, and
what it includes.

**Components.** 12 tiers with services price, monthly infrastructure price and
duration · per-capability handling as glyphs.

**Layout.** One table at x 0.42, y 1.98 → 6.58, 12.36 in wide: label column 2.92
plus one column per tier. Rows: tier header · package scope · services price ·
infrastructure price · timeline · one row per capability area. Header row is the
orange tier ladder with white bold 12.5 pt; body rows are white.

**Type floor, 11 pt.** Sizes come from the reference — header 12.5, label and
scope 11, prices 11.5, timeline 11, glyphs 18 — and **nothing on this slide goes
below 11 pt**. Rows are measured from their text; if the stack exceeds the band
the type scales down in 4 % steps until the floor bites, and then the builder
reports that the wording has to be shortened or a row dropped. It never goes
smaller. The other way round too (rule 1): when the rows are few the table does
**not** sit half the height of its band with small type — the rows grow into the
band and the type stays at or above the floor.

**Glyphs.** `◐` partial · `●` included · `●●` multi-region / advanced · `—` not
in this tier. Derived from `packages.capability_handling[]`: an empty or `—`
cell is "not in this tier"; otherwise the tier default (pov `◐`, integration
`●`, scaling `●●`). A `glyphs:` map on the entry overrides per tier. All three
marks are set in **one symbol face** — Apple Symbols, with `a:sym` naming
Segoe UI Symbol for Windows — because neither brand face carries them and a
renderer that substitutes a different face per glyph draws them at visibly
different sizes (the owner, 2026-09-22). The status key under the table uses the
same face.

**Budgets.** Label column ≤ 10 words · tier scope cell ≤ 12 words.

**Rules.** 5 — the three tier headers are three tints of one hue, never three
different colours. Prices carry a `*` and a footnote whenever
`status: indicative`; a `tbd` price prints "To be defined", never a guess.
Tier names come from the spec (`PoV Jumpstart` / `Integration` / `Scaling`); the
S/M/L letters are size tags appended to the name, not the name.

---

## 10 — Service packages (detailed)

**Purpose.** The same table with prose in every cell — the version a seller
reads out in a scoping call.

**Layout.** Table at 0.43 / 2.05 → 6.62, 12.49 wide, label column 2.55. Rows:
tier header · scope · one row per capability area, each cell rendered as
`<glyph>  <prose>` — the glyph in the symbol face, the prose in the body face,
as two runs in one cell. Same sizing behaviour as slide 9, with a **10.5 pt
floor**.

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
`architecture.stack[]`.

**Optional, deck-specific:**

| Key | Effect |
|---|---|
| `problem_solution.problem_points[]` | the three named challenges on slide 2 |
| `problem_solution.reframe` / `reframe_question` | slide 2 solution heading / slide 4 headline |
| `problem_solution.today` / `tomorrow` | slide 4 band bodies (else problem / solution) |
| `kpis[].chip` | slide 2 chip label (else `name`) |
| `kpis[].label` | slide 5 stat caption (else `formula` / `name`) |
| `kpis[].show_baseline` | renders `baseline → figure` |
| `kpis[].channels[]` | restricts a metric to channels; any restriction drops the whole strip |
| `packages.tiers[].scope_line` | tier scope sentence (else the first `what_you_get`) |
| `packages.capability_handling[].glyphs` | per-tier glyph override |
| `packages.anchor_line` | slide 2 anchor strip (else built from required products) |
| `packages.target_oci_consumption` | slide 6 consumption strip |
| `deck.running_header` | `"Oracle AI & Data Solutions — {name}"` by default |
| `deck.images.today` / `deck.images.tomorrow` | the two pictures on slide 4; absolute, or relative to the pack brief's folder |
| `architecture.stack[].catalog_id` (engine layer) | the products the engine box names |
| `deck.vertical_case`, `deck.seller_lead`, `deck.cta`, `deck.proof_headline`, `deck.layers_sub`, `deck.architecture_sub` | the short editorial lines |

## Channels

`--channel partner_print` (default) uses the external name variant plus the
`Accelerator App by SoftServe` subheading, the `contacts.partner_print` block,
and refuses the customer name unless
`clearance.customer_name_allowed.partner_print` is true.
`--channel internal` uses the `internal_slide` name variant and
`contacts.internal`. Nothing else differs — an internal deck is not a licence to
print internal operating numbers (rule 13); those never reach a slide.

## Definition of done

1. `build_deck.py … --fit-report` exits 0 — no box overflows, no cell over its
   word budget.
2. `lint_deck.py <deck> --spec <spec> --channel <channel>` exits 0 — ten slides,
   the running header, no tier line on the cover, brand faces only, corners no
   rounder than the reference's, an icon per industry, the architecture's names
   and flows, table type at or above the floor.
3. A contact sheet of all ten renders has been looked at (`tools/render_probe.sh`
   prints how to make one on this machine).
4. The clearance linter passes on the built file.
5. The builder's notes have been read and acted on — especially the two picture
   slots on slide 4, any industry that fell back to the neutral icon, and the
   architecture summary.
