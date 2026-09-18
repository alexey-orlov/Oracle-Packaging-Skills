# Executive summary — the one-slide anatomy

One slide that puts a whole pack in front of an executive audience: what the
problem and the solution are, who owns which layer, what it proved, what it
costs, what it can do, and what happens next. `tools/build_exec_summary.py`
implements exactly this.

Measured from two references:

- **Sep 11 2026, `Oracle AI Packages - section slides.pptx`, slides 5–6** — the
  newest style and the one Alex named as the reference. Six blocks on a
  three-column grid, layout `Title-1Column`.
- **Jul 17 2026, `Workforce Optimization - Executive summary - Oracle.pptx`,
  slide 1** — the same grid with a different block assignment, plus the
  `PLANNED NEXT STEPS` block and the closing slide.

Both sit on the 13.33 × 7.5 in SoftServe EMEA master. Colours, fonts and the
fit-estimation rule are in `../deck/references/brand-tokens.md`.

## The grid

| Element | x | y | w | h |
|---|---|---|---|---|
| Running header (placeholder idx 34) | 6.79 | 0.31 | 5.48 | 0.23 |
| Title (placeholder idx 0) | 0.39 | 1.18 | 12.05 | 0.43 |
| Subtitle line | 0.42 | 1.70 | 12.50 | 0.30 |
| Section label, top row | col x | 2.12 | col w | 0.24 |
| Panel, top row | col x | 2.41 | col w | 1.86 |
| Section label, bottom row | col x | 4.43 | col w | 0.24 |
| Panel, bottom row | col x | 4.72 | col w | 1.92 |
| Footnote | 0.42 | 6.80 | 12.50 | 0.30 |

Columns: **(0.42, 4.62) · (5.22, 3.78) · (9.18, 3.75)**. Section labels are
10.5 pt bold — blue for descriptive blocks, orange for the two that carry a
claim (proof, next steps). Panels are tinted with a 0.05 in left accent bar and
a `DCE1E5` hairline. The title is 28 pt, autofitted down to 16 pt and always one
line; the builder resets the placeholder to the box above because the base
layout's own title placeholder is 4.50 in wide and the master uppercases.

## The six blocks

| Column | Top | Bottom |
|---|---|---|
| 1 | USE CASE — problem → solution + verticals | SERVICE PACKAGES — one row per tier |
| 2 | SOLUTION LAYERS — the vendor ladder | CAPABILITIES — area → category tree |
| 3 | PROOF OF VALUE — the metric set | PLANNED NEXT STEPS — numbered |

The Jul 17 slide put SERVICE PACKAGES in column 1 and a *thumbnail* of the
feature list in column 2; the Sep 11 slide drew the capability tree as shapes
instead (its slide 6). The builder uses the drawn tree: it needs no image, it
comes straight from `capabilities[]`, and it survives a rebuild.

### USE CASE (col 1, top)

`PROBLEM:` and `SOLUTION:` as bold run-in leads at 9.5 pt, then a `VERTICALS`
label (8 pt blue) and the vertical names joined with `·` at 8.5 pt. The whole
stack autofits down to 70 % before it is reported as overflowing.
**Budget:** problem + solution ≈ 75 words together; verticals ≈ 20 words.

### SOLUTION LAYERS (col 2, top)

One row per `architecture.stack[]` entry, `(1.86 − 0.06 × (n−1)) / n` tall, tint
and bar by vendor (the fixed ladder in `../deck/references/brand-tokens.md`). Layer name 10 pt bold
left, vendor 7.5 pt muted right. A right-aligned "▲ business value" sits on the
label row. **Budget:** layer name ≤ 5 words; four rungs is the shape, six is the
practical maximum.

### PROOF OF VALUE (col 3, top)

The attribution line (8 pt muted) then up to three stats: figure 12.5 pt blue
bold (with `baseline → figure` when `show_baseline`), caption 7.5 pt muted.
The label reads `PROOF OF VALUE` or `PROOF OF VALUE · <customer>` when
`clearance.customer_name_allowed.internal` is true.
**Budget:** figure ≤ 20 characters; caption ≤ 10 words.

**Peer claims are all or none** (slide-design rule 11). If any metric in the set
is restricted away from this channel, the block is drawn as an *empty instance*
of the same panel with one grey line, and the builder notes it — never a
half-filled proof block.

### SERVICE PACKAGES (col 1, bottom)

One row per tier, `(1.92 − 0.09 × (n−1)) / n` tall: tier name + size tag 10 pt
bold, scope sentence 6–8 pt muted below, price 12 pt blue right-aligned,
duration 8.5 pt muted underneath. A price with `status: indicative` gets a `*`
and the footnote. **Budget:** scope ≤ 18 words.

### CAPABILITIES (col 2, bottom)

The `Area > Category` tree as shapes: a 1.40 in area cell spanning its
categories, category cells 2.36 in wide, rows 0.20 in (shrinking when the tree
is tall). Feature names are *not* on this slide — the feature list carries them.
**Budget:** about 10 category rows; beyond that the builder reports that areas
or categories have to be trimmed for this slide.

### PLANNED NEXT STEPS (col 3, bottom)

Up to four numbered entries from `exec_summary.next_steps[]` — an outlined
orange badge (0.26 in), title 10 pt bold, detail 8.5 pt muted.
**Budget:** title ≤ 6 words, detail ≤ 10 words. With no next steps the panel is
drawn empty with one grey line (rule 3).

### Footnote

Caveat + the price footnote + `divergence_from_pack`, 8 pt `8A9095`, two lines
maximum.

## Naming and channel

The executive summary is the **internal** artifact, so the builder loads the
spec with `channel="internal"` unconditionally and titles the slide with
`meta.name_variants.internal_slide` — "Workforce Optimization **App**" — per the
2026-09-18 naming decision. `--title` overrides it. Internal naming is not a
licence to print internal operating numbers: headcount, contract values and
internal package costs stay off the slide (slide-design rule 13).

## Host decks

`--host-deck <pptx>` builds on that deck's own master: the file is opened, its
slides are stripped, and the one slide is added on its `Title-1Column` layout
(or the closest match the picker finds — the builder prints which). The result
is a standalone one-slide pptx that pastes into the host with its theme, fonts
and furniture intact. This is the deck-kit rule: deliver new slides as a
standalone pptx built on the host deck's own master, never as a slide built
elsewhere and re-themed by hand.

Without `--host-deck` it builds on `../deck/assets/softserve-deck-base.pptx`.

`--with-closing` appends the host's own closing slide when a layout whose name
starts with `Close` exists, filled with `exec_summary.closing_line` (default:
"We look forward to continuing the conversation."). The shipped base has no
`Close` layout, so on the base the flag is ignored with a note — that is
correct, not a failure.

## Spec keys this slide reads

**Required:** `meta.name_variants.internal_slide` (or `meta.name`),
`one_liner.short|full`, `problem_solution.{problem,solution}`,
`architecture.stack[]`, `packages.tiers[]`.

**Optional:** `verticals[].name` · `capabilities[].area` and
`categories[].name` · `kpis[]` with `figure`, `label`, `baseline`,
`show_baseline`, `attribution`, `caveat`, `channels` ·
`packages.tiers[].scope_line` · `exec_summary.goal` (renders as an orange `GOAL`
lead before the one-liner) · `exec_summary.next_steps[].{title,detail}` ·
`exec_summary.running_header` · `exec_summary.closing_line`.

## Definition of done

1. `build_exec_summary.py … --fit-report` exits 0.
2. The render has been looked at (`../deck/tools/render_probe.sh` prints how).
3. The clearance linter passes.
4. When it is going into a host deck, it was built with `--host-deck` and opened
   in that deck once to confirm it pastes unchanged.
