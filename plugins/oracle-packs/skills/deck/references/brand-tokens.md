# SoftServe deck brand tokens

_Read by tools, not by the model. The measured constants `tools/build_deck.py`
(the legacy redraw builder) and the executive-summary skill draw a slide with.
The runtime card is `references/cards/render-qa.md`._

Everything a builder needs to put a slide on the SoftServe EMEA master. Measured
from the master, the Workforce optimization sales deck (Jul 2026) and the
Oracle AI packages section slides (Sep 2026). Values are authoritative for the
**12192000 × 6858000 EMU (13.33 × 7.5 in)** canvas only — other SoftServe deck
families use a different canvas and none of this geometry transfers.

## The base

`assets/softserve-deck-base.pptx` — a 41 KB single-slide shell derived from the
full 26 MB EMEA template: real master, theme and logo, **one layout**
(`Title-1Column`), one placeholder table slide, no media bloat. A builder opens
it, strips its slides and adds its own, so the master, theme and fonts come along
and nothing has to be re-derived.

**The sales deck no longer starts here.** `build_deck_v2.py` fills the exemplar
deck (`assets/exemplar/wfo-sales-deck.pptx`), which brings its own master, theme,
layouts — the dark `Title-AI` cover among them — and every geometry this page
lists. The base is what the **legacy** builder (`build_deck.py`) and the
executive-summary skill draw on, and what the tokens below are for.

| Layout | Placeholders (idx) | Notes |
|---|---|---|
| `Title-1Column` | title (0), body / running header (34), slide number (4), content (37) | the only layout in the base |

The base's own slide carries a 4-row placeholder table plus a footnote text box
as a copy-ready exemplar of the table idiom; the builders do not use it (they
create their own tables), and it is removed with the rest of the slides.

**What the base does NOT have:** a dark photo title layout (`Title-AI`), the
orange gradient section dividers, the `Close` layout, `ShortTitle-Empty`. A
builder that wants a dark cover draws one (a full-bleed ink rectangle), and
`--with-closing` only produces a closing slide when the deck is built on a host
that has a `Close` layout.

## Placeholder geometry (inches)

| Element | x | y | w | h |
|---|---|---|---|---|
| Running header (idx 34) | 6.79 | 0.31 | 5.48 | 0.23 |
| Slide number (idx 4) | 12.33 | 0.22 | 0.63 | 0.40 |
| Title, section-slide style (idx 0) | 0.39 | 1.18 | 12.05 | 0.43 |
| Title, sales-deck content slide | 0.39 | 1.40 | 11.80 | 0.95 |

The base layout's own title placeholder is only 4.50 in wide; both builders
reset it to the 12.05 in box above, because the master uppercases the title and
a pack name wraps in the narrow box.

## Content band

| Constant | Value |
|---|---|
| Left margin / content x | 0.42 in |
| Content width | 12.49 in |
| Two peer cards | 6.02 in wide at x = 0.42 and 6.89 |
| Four-card grid | 6.00 × 2.00 in at x = 0.42 / 6.72, y = 2.48 / 4.76 |
| Package table | 12.36–12.49 in wide, 4 columns, 8–11 rows |
| Footnote row | y ≈ 6.63–6.84, 0.18–0.33 in tall |
| Three-column section grid | (0.42, 4.62) · (5.22, 3.78) · (9.18, 3.75) |

## Colours

| Token | Hex | Where it is used |
|---|---|---|
| ink | `26282B` | body text, dark anchor strips, cover ground |
| ink_soft | `44515A` | secondary ink, neutral accent bars, vendor badge text |
| muted | `6B7076` | secondary body text, sub-lines |
| muted_light | `8A9095` | footnotes, source lines |
| hairline | `DCE1E5` | panel outlines |
| hairline_alt | `D2D8DD` | card outlines, dividers |
| panel_grey | `F4F6F7` | neutral panel fill |
| blue | `1485C3` | Oracle / solution side, section labels, stat values |
| blue_mid | `459FDD` | diagram fills, second blue |
| blue_light | `6DB2E2` | third blue, tier accent |
| blue_dark | `0E5E8A` | outline on a blue fill, "▲ business value" |
| blue_tint | `EAF3FB` | tinted panel |
| blue_tint_2 | `ECF5FB` | solution card |
| orange | `F36949` | SoftServe accent, proof labels, numeral badges |
| orange_light | `FE8D6B` | tier S header |
| orange_dark | `D84F2E` | tier L header |
| orange_tint | `FDEDE8` | SoftServe layer, next-steps panel |

Two ladders are load-bearing (slide-design rule 5 — two stages of one dimension
are two tints of ONE hue):

- **Tier headers**, light → dark orange: `FE8D6B` → `F36949` → `D84F2E`.
- **Solution layers by vendor**: SoftServe `FDEDE8` / bar `F36949` · Oracle +
  SoftServe `D2E7F6` / `1485C3` · NVIDIA `EAF3FB` / `6DB2E2` · Oracle (infra)
  `EEF1F3` / `6B7680`.

Contrast, checked on the renders: white text on `F36949` is 3.0:1 — use ink on
orange, and keep white only on hues at 6:1 or better. `8A9095` on white is for
footnotes; anything that must be read on a tinted panel uses `6B7076` or darker.

## Fonts

| Role | Face | Fallback if the brand face is absent |
|---|---|---|
| Cover, titles | `+mj-lt` (theme major latin = Azurio) | keep the theme reference — never hardcode the family |
| Body, labels, table cells | `Replica LL TT` | Helvetica Neue, Helvetica, Arial, sans-serif |
| Status marks ● ◐ ○ ●● | `Apple Symbols`, with `a:sym` = `Segoe UI Symbol` | any one face that has all of them |
| Small keys, numerals | `Roboto Mono` | Menlo, Consolas, monospace |

Azurio and Replica LL TT ship privately in the plugin's `fonts/` folder, for
practice members only, and are never embedded in a deck (see the README there).
A machine that has not installed them (`shared/tools/py
shared/tools/install_fonts.py`) renders substitutes; the deck file is still
correct, because the runs name the brand faces and PowerPoint resolves them
wherever they are installed.

The reference deck's cover is set entirely in `+mj-lt`; its content slides are
`Replica LL TT` throughout. Neither brand face carries U+25CF / U+25D0 / U+25CB,
so a renderer substitutes a *different* face per glyph and they come out at
visibly different sizes (the owner, 2026-09-22). One symbol face for all of them
fixes it by construction; `.pptx` has no font table, so the Windows equivalent
is named on the run as `<a:sym typeface="Segoe UI Symbol"/>` — the counterpart
of the `altName` the feature-list builder writes into Word's font table. Every
deck run names its face and its size explicitly, including the running header;
nothing is left to inherit from a host master.

Sizes that hold up on this master: slide title 24–28 · section label 10.5 bold ·
card heading 13–15 bold · body 9.5–12 · table values 10.5–11.5 · table glyphs
15–18 · small caption 7.5–8.5 · footnote 8.

## Text fit

The builders measure with the Replica LL TT the plugin ships in its `fonts/`
folder and add a **+2 % margin** for rendering slack. Where that folder holds
no files they measure with a Helvetica-metric stand-in — Liberation Sans, then
Arial, then Helvetica, whichever exists — and add a **+6 % safety margin**. Either
way the width is compared against the box width in EMU, and the fit report's
first line names the face measured and the margin. Line height is
`1.22 × point size`.

This is the deck-kit rule restated: a render proves geometry and colour; it does
not prove that the real font fits, because the renderer substitutes. Any string
that must stay on one line is checked in the builder, not in the render. When
the master uppercases a string (titles), measure the uppercase form — lowercase
under-reads by roughly 15 %.

## Corners

Structure is **square**. In the reference, cards, panels and diagram boxes are
`roundRect` with adjustments of 4 000–12 000 — a 0.04–0.18 in radius on shapes
several inches wide, which reads square at slide scale — and only chips and
vendor badges are real pills (adjustment 50 000). The builders therefore draw
square rectangles and reserve the pill (`adj = 0.5`) for chips and numeral
badges, plus the gentle 0.10 the reference gives the proof slide's stat tiles.
Per-slide counts: `reference-geometry.json`.

## Table idiom

`tableStyleId = {2D5ABB26-0587-4C30-8999-92F81FD0307C}` ("No Style, No Grid"),
`firstRow` and `horzBanding` off, every cell fill set explicitly so no style
bleeds through. Cell insets: 109728 EMU left/right, 45720 top/bottom, vertical
anchor middle. Header row: ink label cell + the orange tier ladder. Body rows:
white fill, a 12700 EMU bottom rule under the price/timeline block only.
