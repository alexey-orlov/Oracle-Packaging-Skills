# Feature list — anatomy, columns, glyph legend

_Long form; not loaded at run time. The measured geometry, colours, fit ladder and height model here are implemented inside `tools/build_feature_list.py` — they are not read from this file. The runtime cards are the build skill's `feature-list` and `feature-list-fit`._

The feature list follows the practice mini-site (its 2026-09-18 rebrand) and the owner's
requirements of **2026-09-22**: the site's header lockup instead of a text kicker, the site's
faces and styles, the approved one-liner plus one sentence saying who the pack is for, and
**one A4 page**.

**The feature list is the master.** Every other artifact's capability view is derived from it —
the deck's capability rows, the mini-site's workflow-stage view, the packages table's areas. When
a capability is not in the feature list, it does not exist for the pack.

---

## 1. Structure, in order

| # | Element | Content |
|---|---|---|
| 1 | **Lockup** | The SoftServe wordmark (1.0 in), a hairline rule, `Oracle AI & Data Solutions` — the mini-site's header, left-aligned and vertically centred |
| 2 | **Title** | `<meta.name> — Feature list`, Azurio Regular 20pt black, over a 0.75pt hairline |
| 3 | **One-liner** | The approved `one_liner.full` (or `feature_list.intro`), Replica 9pt on `#26292B` |
| 4 | **Who it is for** | `For ` + `icp.line`, Replica 8pt on `#4C5156`. Missing `icp.line` → the one-liner alone, and the build says so on stderr |
| 5 | **The matrix** | One fixed-layout table; see the columns below |
| 6 | **Legend** | One line, muted 7pt, the three glyphs in their colours |
| 7 | **Footnotes** | `*`, `**`, `***` — the caveat alone, one per feature carrying a `note`, in document order |

There is no kicker, no eyebrow and no run-in `App.` definition label. The document opens with the
brand and then says, in the pack's own approved words, what it is and who it is for.

**There is no page footer** (the owner, 2026-09-22) — nothing at the foot of the page at all. The
traceability it used to carry moves into the file's own properties, where a reader can ask for it
and a customer never sees it: `title` (the document title), `subject` (pack · feature list · spec
version), `comments` (the build date, the spec it came from, and that the document carries no
pricing) and `category`. The build writes them on every run.

## 2. Fonts and colours

Both faces are the mini-site's, and only the title uses the display face.

| | Face | Where | Fallback |
|---|---|---|---|
| Display | **Azurio** Regular, sentence case | the title, and nothing else | Georgia |
| Body | **Replica LL TT** | lockup name, intro lines, table, legend, footnotes | Arial |
| Symbol | **Apple Symbols** | the three status glyphs, everywhere they appear | Segoe UI Symbol |

The builder sets `rFonts` on every run and style, and post-processes the saved `.docx` to name
both faces in `word/fontTable.xml` with an `altName`, so Word substitutes predictably on a machine
that does not have them. On the owner's Mac they are installed in `/Library/Fonts/Managed/`.

| Token | Hex | Where |
|---|---|---|
| text | `#000000` | title, lockup name |
| body | `#26292B` | the one-liner, table text |
| muted | `#4C5156` | the ICP line, legend, footnotes |
| hairline | `#D1DAE2` | the title rule and every table border (4 eighths of a point) |
| decor | `#BDCBD7` | the lockup's vertical rule |
| raised | `#EDF0F2` | Category cells |
| accent | `#1485C3` | Area cells (white bold text), the available and partial glyphs |
| ink | `#26282B` | the table's header row (white bold text) |
| roadmap | `#AEB4BA` | the roadmap glyph — legible where `--decor-dim` is not |

## 3. Page and table geometry

- **A4 portrait**, margins 13.1 mm left/right (0.514 in), 10.0 mm top, 7.4 mm bottom. Nothing sits
  in the bottom margin: there is no footer.
- Table width **10250 dxa (7.12 in)**, `tblLayout: fixed`, cell margins left 80 / right 65 /
  top 16 / bottom 16 dxa, all borders `single sz 4` in the hairline grey.
- Table text **7.5pt**, and **7pt is the floor** — below it the matrix stops being readable and the
  answer is a coarser capability tree, not smaller type.
- Rows: `cantSplit` + `trHeight 300` (a minimum, not a fixed height). Every cell vertically centred.
- The header row repeats (`tblHeader`) only under `--fit none`, where the document may run long.

## 4. Columns

| Column | Width (dxa) | Content | Merged down across |
|---|---:|---|---|
| **Area** | 1077 / 1000 | The capability area. White bold on accent blue, centred. | its whole area |
| **Category** | 1978 / 1800 | The category within the area, on `#EDF0F2`. | its category |
| **Features** | 3420 / 3000 | One feature per row. The only column that never merges. | — |
| **Current status** | 1350 / 1150 | One glyph, centred. | runs of equal status inside a category |
| **Tier first available** | — / 1150 | *Optional column.* `PoV Jumpstart` / `Integration` / `Scaling` from `tier_first_available`. | runs of equal tier inside a category |
| **Standard customization scope** | 2425 / 2150 | A short bulleted list of what is customized per customer. | its whole area |

Two width sets — the five-column reference layout and the six-column layout with `Tier first
available` — both totalling 10250 dxa, so the table occupies the same measure either way. The
builder adds the tier column when every feature carries `tier_first_available`; `--no-tier-column`
forces the reference layout. Compact mode has its own four-column set (1000 / 1500 / 5400 / 2350).

**The Area column sizes itself** to the longest single word in any area name, between 1000 and 1500
dxa, taking the difference from the Features column so the table's measure never changes. Area
names are short and their words are long — "normalization", "Optimization" — and a word wider than
its column is broken mid-word rather than overflowed, which is what "Signal intake & normalizatio /
n" looked like before the column learned to fit it.

Merging is what makes the matrix readable: only the first row of a group carries text, and the
group reads as one block down the page. The builder also shades continuation cells, so the column
still reads correctly in viewers that do not honour vertical merges (QuickLook among them — a
continuation cell looking separate there is a previewer artefact, not a defect).

## 5. One A4 page, and the fit ladder

One page is a **requirement** (the owner, 2026-09-22). The build does not hope for it: it estimates
the document's height first — usable page height less the margins, the header block, the legend,
the footnotes and a 4% safety margin — by wrapping every cell's text at its column's usable width
with the real installed face, and walks a ladder until the estimate fits:

| Rung | Layout | Type |
|---|---|---|
| a | one row per feature | 7.5pt |
| b | one row per feature | 7pt |
| c | **compact**: one row per category | 7.5pt |
| d | compact | 7pt |

**Compact mode** lists a category's features inline in the Features cell as
`name ●  ·  name ◐  ·  name ○`, each glyph in its legend colour and footnote markers kept. It
**drops the Current status and Tier first available columns** — the status travels with each
feature instead — and keeps Area and the per-area scope merged as usual. The build says on stdout
which rung it used and the estimated fill.

If no rung fits, **nothing is written** and the build exits 3 with a plain report: the estimated
height against the budget, the number of areas / categories / features, the three largest areas and
five largest categories, and the instruction to group or generalize the capabilities. That report
goes to the owner as it stands — the fix is a coarser capability tree
(`shared/references/anatomy/capabilities.md` sizes it), never smaller type.

`--fit none` restores the old behaviour — one row per feature at 7.5pt over as many pages as it
takes, with the header row repeating. On macOS with Pages installed the build also **verifies** the
real page count by exporting to PDF (hard 90-second limit; any failure prints
`page count not verified (estimate only): <reason>` and the build still succeeds). The estimate is
the contract; the real count is the confirmation, and a document that renders longer than one page
sends the ladder to its next rung.

The height model is measured, not assumed: both brand faces set a line at 1.20 em, and every table
cell renders one body-size line taller than the text it holds. Ignoring that last term under-read a
13-row table by a quarter of a page — an estimate of "75% of one page" that printed two. A line
carrying status glyphs costs the same as any other while the symbol face is named; where the build
falls back to the renderer's own substitution, such a line measures 1.36 em and the estimator uses
that instead.

## 6. Glyph legend

The owner's decision of 2026-09-18 replaces the reference document's two same-glyph statuses — `●`
blue for "provided OOTB" and `●` pale blue for "partially implemented" — with three distinct
shapes. Colour alone failed: the two were indistinguishable in greyscale print, when the document
was forwarded as a screenshot, and to a screen reader.

| Glyph | Code point | Status | Legend wording | Colour |
|---|---|---|---|---|
| ● | U+25CF | `available` | provided out of the box, configuration may be required | `#1485C3` |
| ◐ | U+25D0 | `partial` | partially implemented, major improvements on the roadmap | `#1485C3` |
| ○ | U+25CB | `roadmap` | planned, not implemented today | `#AEB4BA` |

**All three are set in one symbol face**, everywhere they appear — the status column, the inline
glyphs of compact mode, and the legend. Neither brand face carries any of the three code points, so
left to itself the renderer substitutes a *different* face per glyph and they come out at different
sizes: the first regenerated list had ● and ○ visibly smaller than ◐ (the owner, 2026-09-22). The
build names **Apple Symbols**, which draws them within 4% of each other in width and 2% in height,
and writes a `Segoe UI Symbol` altName into the font table so Word on Windows lands on a face that
also has all three. Where no such face is found, the build falls back to per-glyph point sizes that
look equal on the page (● and ○ at 1.15× the size of ◐) and says so on stderr.

The legend is **one line**, the three entries separated by ` · `, in muted 7pt with the glyphs at
8pt in their own colours.

The same three levels appear on the one-pager's packages table with a different meaning — there
they describe **what a tier includes**, not what the product implements. Do not reconcile the two:
a feature can be `available` in the product and still be out of scope at PoV tier.

A feature carrying a `note` gets a footnote marker after its name (`*`, `**`, …) and a line under
the legend. The line is **the caveat alone** — `**  file export / import at PoV; API write-back is
Integration-tier scope` — never the feature name or the category description repeated back: the
marker already says which row it belongs to.

A note exists only for a **tier caveat that changes what a buyer gets**, typically an integration
claim stating its tier, because an integration claim must state its tier (the owner, 2026-09-18).
Keep it to **15 words or fewer** and to **at most three notes in the whole document** (the owner,
2026-09-22). Anything else belongs in the area's customization-scope cell, or nowhere. The build
warns on stderr — it does not fail — when the list carries more than three notes or one runs past
20 words, naming them, so the skill can put the cuts to the owner before the document goes out.

## 7. No pricing in the feature list

The feature list never carries a price, a tier price range, an infrastructure cost, or a day rate.
Confirmed on all three reference feature lists in the estate; pricing lives on the sales one-pager
and the deck, where it sits next to the scope that justifies it.

The reason is practical: feature lists are forwarded internally, pasted into RFP responses, and
attached to emails long after the commercial conversation has moved on. A price on a feature list
outlives its own assumptions and comes back as a quote nobody meant to give.

`tools/build_feature_list.py` enforces this — it scans the assembled document for currency figures
and for any value in `packages.tiers[].services_price` / `.infra_price_monthly`, and exits 2
without writing the file if one is found.

## 8. What the builder reads from the pack spec

Required: `meta.name`, `meta.slug`, `one_liner.full`, and `capabilities[]` as
`area > categories[] > features[]`, each feature with a `name` and a `status`.

Expected: `icp.line` — the sentence saying who the pack is for. Its first character is lower-cased
so it reads on from "For …", unless the line starts with a proper noun.

Optional: `capabilities[].customization_scope_area` (a list; the per-area scope cell) ·
`capabilities[].categories[].features[].customization_scope` (overrides the area scope for that
feature) · `.tier_first_available` · `.note` · `meta.spec_version` · `feature_list.title` ·
`feature_list.intro` (overrides `one_liner.full` where the pack needs a longer definition than the
sales one-liner).

`status` accepts `available` / `partial` / `roadmap` plus a few aliases (`ootb`, `ga`, `yes`,
`in_progress`, `partially_available`, `planned`, `no`). Anything else is an error naming the
feature — the builder never guesses a status.

## 9. The capability table in the spec

In `pack-spec.md` each capability area is a `###` heading with one table under it: a row per
feature, its category first (`shared/schema/pack-spec.md`). Values go in through `packspec.py set`,
never by editing cells by hand — a `|` inside a cell has to be written `\|`, and a row with a cell
too many or too few is refused on its line. A spec converted from YAML can still carry the old
flow-style damage, a value split at its commas into junk keys (`name: Dispatcher UI (map, table
views)` read as `Dispatcher UI (map` plus a key); in Markdown it shows as an extra column, and
`lint_spec.py` warns (SPEC024) naming the key.
