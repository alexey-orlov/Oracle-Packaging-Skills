# Feature list — anatomy, columns, glyph legend

Measured off the Workforce Optimization feature list of **2026-09-10**
(`Workforce Optimization - Accelerator Pack one-pager.docx`, 1 table, 4 areas / 13 categories /
39 features, 5 columns) — the canonical feature list in the estate. Vlad Butenko's Large Document
Extraction (2026-07-27) and Account Insights (2026-09-10) one-pagers are the same artifact type and
confirm the shape.

**The feature list is the master.** Every other artifact's capability view is derived from it — the
deck's capability rows, the mini-site's workflow-stage view, the packages table's areas. When a
capability is not in the feature list, it does not exist for the pack.

---

## 1. Structure, in order

| # | Element | Content |
|---|---|---|
| 1 | Kicker | `SOFTSERVE × ORACLE` in accent blue, bold, 8pt, then ` · ` + the eyebrow in grey |
| 2 | H1 | The pack name + "Feature list", bold 16pt, with a 1.5pt accent rule beneath it |
| 3 | Definition | A run-in bold accent label (`App.`) then the one-line application definition, 8pt |
| 4 | **The matrix** | One fixed-layout table; see the columns below |
| 5 | Legend | "Current status" label, then one line per glyph |
| 6 | Footnotes | `*`, `**`, `***` — one per feature carrying a note, in document order |
| 7 | Footer | Pack name · feature list · spec version · generation date, 6.5pt grey, right |

The 2026-07-07 predecessor also carried `Scope.` / `Verticals.` / `About this matrix.` lead
paragraphs. The 2026-09-10 rebuild dropped them for a single `App.` definition, which is the
current shape and what the builder produces.

## 2. Page and table geometry

- **A4 portrait**, margins 13.1 mm left/right (0.514 in), 10.0 mm top, 7.4 mm bottom.
- Body font **Arial 7.5pt** throughout; the table inherits it.
- Table width **10250 dxa (7.12 in)**, `tblLayout: fixed`, cell margins left 80 / right 65 /
  top 16 / bottom 16 dxa, all borders `single sz 4` in `#D9D9D9`.
- Rows: `cantSplit` + `trHeight 300` (a minimum, not a fixed height). The header row is marked
  `tblHeader` so it repeats when the table runs past one page — feature lists are expected to be
  several pages; unlike the one-pager there is no length rule.
- Every cell is vertically centred.

## 3. Columns

| Column | Width (dxa) | Content | Merged down across |
|---|---:|---|---|
| **Area** | 1077 / 1000 | The capability area. White bold on accent blue, centred. | its whole area |
| **Category** | 1978 / 1800 | The category within the area, on `#EDF0F2`. | its category |
| **Features** | 3420 / 3000 | One feature per row. The only column that never merges. | — |
| **Current status** | 1350 / 1150 | One glyph, centred, 10pt. | runs of equal status inside a category |
| **Tier first available** | — / 1150 | *Optional column.* `PoV Jumpstart` / `Integration` / `Scaling` from `tier_first_available`. | runs of equal tier inside a category |
| **Standard customization scope** | 2425 / 2150 | A short bulleted list of what is customized per customer. | its whole area |

Two width sets: the five-column reference layout, and the six-column layout with `Tier first
available`. Both total 10250 dxa, so the table occupies the same measure either way. The builder
adds the tier column automatically when every feature carries `tier_first_available`;
`--no-tier-column` forces the reference layout.

Merging is what makes the matrix readable: only the first row of a group carries text, and the
group reads as one block down the page. The builder also shades continuation cells, so the column
still reads correctly in viewers that do not honour vertical merges.

## 4. Glyph legend

Alex's decision of 2026-09-18 replaces the reference document's two same-glyph statuses — `●` blue
for "provided OOTB" and `●` pale blue for "partially implemented" — with three distinct shapes.
Colour alone failed: the two were indistinguishable in greyscale print, when the document was
forwarded as a screenshot, and to a screen reader.

| Glyph | Code point | Status | Legend wording | Colour |
|---|---|---|---|---|
| ● | U+25CF | `available` | provided out of the box, configuration may be required | `#1485C3` |
| ◐ | U+25D0 | `partial` | partially implemented, major improvements on the roadmap | `#1485C3` |
| ○ | U+25CB | `roadmap` | planned, not implemented today | `#AEB4BA` |

The same three levels appear on the one-pager's packages table with a different meaning — there
they describe **what a tier includes**, not what the product implements. Do not reconcile the two:
a feature can be `available` in the product and still be out of scope at PoV tier.

A feature carrying a `note` gets a footnote marker after its name (`*`, `**`, …) and a line under
the legend. Notes are where tier-specific integration caveats belong — for example "file export /
import at PoV; API write-back is Integration-tier scope" — because an integration claim must state
its tier (Alex, 2026-09-18).

## 5. No pricing in the feature list

The feature list never carries a price, a tier price range, an infrastructure cost, or a day rate.
Confirmed on all three reference feature lists in the estate; pricing lives on the sales one-pager
and the deck, where it sits next to the scope that justifies it.

The reason is practical: feature lists are forwarded internally, pasted into RFP responses, and
attached to emails long after the commercial conversation has moved on. A price on a feature list
outlives its own assumptions and comes back as a quote nobody meant to give.

`tools/build_feature_list.py` enforces this — it scans the assembled document for currency figures
and for any value in `packages.tiers[].services_price` / `.infra_price_monthly`, and exits 2
without writing the file if one is found.

## 6. What the builder reads from the pack spec

Required: `meta.name`, `meta.slug`, `one_liner.full`, and `capabilities[]` as
`area > categories[] > features[]`, each feature with a `name` and a `status`.

Optional: `capabilities[].customization_scope_area` (a list; the per-area scope cell) ·
`capabilities[].categories[].features[].customization_scope` (overrides the area scope for that
feature) · `.tier_first_available` · `.note` · `meta.eyebrow` · `meta.spec_version` ·
`feature_list.title`, `.kicker`, `.intro_label`, `.intro` (overrides `one_liner.full` where the
pack needs a longer definition than the sales one-liner).

`status` accepts `available` / `partial` / `roadmap` plus a few aliases (`ootb`, `ga`, `yes`,
`in_progress`, `partially_available`, `planned`, `no`). Anything else is an error naming the
feature — the builder never guesses a status.
