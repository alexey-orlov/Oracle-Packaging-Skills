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

Slides 2–10 carry the running header (`OCI AI Accelerators — <pack name>`,
9 pt, `6B7076`, right-aligned at 6.79, 0.31) and the slide-number placeholder;
the cover carries neither. Content titles sit in the 0.39 / 1.40 / 11.80 × 0.95
box, uppercased, 24–26 pt bold ink, **anchored to the top of that box** — anchor
it to the middle and the first content band at y 1.92 collides with it.

Word budgets below are computed with the same estimator the builder uses
(Helvetica-metric stand-in, +6 % safety, 1.22 line factor) and stated as the
*maximum before the box overflows*. The comfortable target is about two thirds
of the maximum; a box filled to the brim reads as a wall.

---

## 1 — Cover

**Purpose.** Name the pack, say the job it does, and show the tier ladder so the
reader knows this is a productized offer, not a project pitch.

**Components.** 4 name (external variant + `external_subheading` when the
channel is partner_print) · 2 one-liner · 3 ICP · 12 tier names.

**Layout.** The base has no dark title layout, so the cover is drawn: full-bleed
ink `26282B` rectangle, a 0.90 × 0.045 in orange rule at y 2.05, then

| Element | x | y | w | h | size |
|---|---|---|---|---|---|
| Tier eyebrow (blue_light, bold) | 0.55 | 1.45 | 8.00 | 0.28 | 11.5 |
| Pack name (white) | 0.55 | 2.40 | 9.20 | 1.05 | 30–44, autofit |
| Subheading (blue_light) | 0.55 | 3.52 | 9.20 | 0.32 | 15 |
| One-liner (`D9E4EC`) | 0.55 | 4.10 | 8.60 | 1.20 | 13–18, autofit |
| "WHO IT IS FOR" + ICP | 0.55 | 5.70 | 8.60 | 0.50 | 9 / 10 |

**Budgets.** Name ≤ 31 characters on one line at 44 pt (it shrinks to 30 pt for
two lines) · one-liner ≤ 36 words · ICP ≤ ~40 words.

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
vertical's number in 40 pt white (the reference used an icon; the plugin ships
none), a 0.06 in ink divider, then name (14.5 bold, 3.21 × 0.70 at +2.54/+0.24),
a 0.55 × 0.04 rule, and the body (11 pt muted, 3.21 × 0.85 at +1.10).

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
(blue) at 2.82, 6.02 × 0.46, bodies at 3.38 (6.02 × 0.92), and two
**screenshot slots** at 4.45 (6.02 × 2.15) drawn as dashed grey containers with
a caption.

**Budgets.** Headline one line ≤ 12 words · each body ≤ 54 words · captions 4–6
words.

**Rules.** 3 — the screenshot slots are empty instances of the same container,
so the slide is complete before the images exist; the builder prints a note
telling you to drop the real before/after screens in before review. 5 — ink for
today, blue for tomorrow.

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

**Layout.** Left: up to three source boxes at x 0.55 (2.95 wide) stacked between
y 2.70 and 5.80. Right: a hairline-outlined container at 5.36 / 2.55,
7.31 × 3.70 holding the app box (blue) and the engine box (grey), each
6.47 × 0.92, with the infrastructure layer named underneath inside the
container. Two labelled arrows at x 3.55 cross the gap — in at y 3.10, out at
3.72.

**Budgets.** Source box ≤ 23 words · platform box ≤ 32 words · arrow label ≤ 8
words · the integration footnote ≤ 79 words.

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
orange tier ladder with white bold 12.5 pt; body rows are white. Row heights are
measured from the text and, if the stack still exceeds the band, the whole table
scales down in 4 % steps to 80 % — below that the builder stops scaling and
reports that rows or wording must be cut.

**Glyphs.** `◐` partial · `●` included · `●●` multi-region / advanced · `—` not
in this tier. Derived from `packages.capability_handling[]`: an empty or `—`
cell is "not in this tier"; otherwise the tier default (pov `◐`, integration
`●`, scaling `●●`). A `glyphs:` map on the entry overrides per tier.

**Budgets.** Label column ≤ 10 words · tier scope cell ≤ 19 words at 80 % type.

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
`<glyph>  <prose>` at 9 pt. Same scaling behaviour as slide 9.

**Budgets.** Detailed cell ≤ 26 words.

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
| `deck.running_header` | `"OCI AI Accelerators — {name}"` by default |
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

1. `build_deck.py … --fit-report` exits 0 — no box overflows.
2. A contact sheet of all ten renders has been looked at (`tools/render_probe.sh`
   prints how to make one on this machine).
3. The clearance linter passes on the built file.
4. The builder's notes have been read and acted on — especially the screenshot
   slots on slide 4 and any table that had to scale below 100 %.
