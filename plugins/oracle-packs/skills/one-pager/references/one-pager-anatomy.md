# Sales one-pager — anatomy, word budgets, CSS tokens, print rules

Measured off the Workforce Optimization sales one-pager of **2026-07-17** — the HTML build source,
not the PDF. That file is the reference for this artifact (Alex, 2026-09-18); `assets/one-pager-template.html`
reproduces its anatomy and CSS with the content replaced by tokens.

**The one-pager is one A4 page, always.** When the content does not fit, the skill proposes cuts —
it never shrinks the type, narrows the margins, or lets the page run to two. The type scale is the
brand. `tools/build_one_pager.py` enforces this: it prints the page with headless Chrome, counts
pages with pypdf, and exits 3 with the longest blocks listed if there is more than one.

---

## 1. Section order (fixed)

| # | Block | Carries |
|---|---|---|
| 1 | **Hero** | SoftServe mark · eyebrow · pack name · optional subheading · one-liner · optional photo |
| 2 | **Pitch — left column** | The problem (paragraph + up to 3 bullets) · The solution (reframe heading + KPI chips + paragraph) · the data-flow line |
| 3 | **Pitch — right column** | "Why it sells" card for the partner's seller (3 bullets) + "Where it applies" verticals |
| 4 | **Proof** | Attribution or customer logo · story · one metric set (3 stats) · caveat |
| 5 | **Packages** | Three tiers as columns; price, timeline and capability rows; legend + price footnote + disclaimer |
| 6 | **CTA footer** | Question · answer · the named contact for this channel |

The order never changes. A block with no content in the spec renders as nothing at all — never as a
heading with an empty body, and never as a "not available" sentence.

---

## 2. Word budget per block

`reference` is the word count measured on the 2026-07-17 page; `budget` is what
`tools/build_one_pager.py` allows before it flags the block. The whole page is **450 words** in the
reference. Going over a block budget is a warning; going over one A4 page is a failure.

| Block | Reference | Budget | Shape |
|---|---:|---:|---|
| `hero.h1` — pack name | 2 | 4 | The plain name for this channel. Never a tagline. |
| `hero.h1-sub` — subheading | 0 | 5 | Optional. "Accelerator App by SoftServe" on the external channel. |
| `hero.sub` — one-liner | 17 | 20 | `one_liner.full`. States the job and the outcome. |
| `problem.para` | 17 | 22 | One sentence naming what the reader does by hand today. |
| `problem.bullets` | 28 | 34 | Up to 3, each **7–12 words**, bold label + consequence. |
| `solution.heading` | 8 | 10 | "The solution: " + `problem_solution.reframe`. |
| `solution.chips` | 6 | 12 | Up to 3 chips, 2–4 words each, with an up/down arrow. |
| `solution.para` | 33 | 38 | How it works, in two sentences, ending in the human step. |
| `data-flow` | 34 | 40 | Source box (4 + 4 words) · two pipe labels (4 each) · platform label (7) · two engine boxes (2–3 + 2–5). |
| `sell.bullets` | 48 | 54 | Exactly 3, each **13–18 words**, bold label + why the partner's seller cares. |
| `sell.chips` | 13 | 22 | 4–5 verticals, **3–5 words each**. Names only; no framing sentences. |
| `proof.story` | 43 | 48 | What the customer did by hand, and what they do now. |
| `proof.stats` | 43 | 50 | 3 stats: figure 2–3 words, label **11–13 words**. |
| `proof.caveat` | 11 | 14 | One line. How the figures were measured, and that they are not contractual. |
| `packages.table` | 87 | 95 | 3 tier names (2 words + size tag), 3 scope lines (**10–15 words**), 3 price/timeline rows, up to 7 capability rows with labels of **1–5 words**. |
| `packages.notes` | 13 | 16 | Glyph legend + the price footnote. |
| `disclaimer` | 0 | 16 | Optional, in the same fine-print row. |
| `cta.q` | 8 | 10 | A question the partner's seller would actually ask themselves. |
| `cta.a` | 15 | 18 | The next step, with the PoV duration in it. |
| **PAGE TOTAL** | **450** | **470** | |

Individual-item shapes above (7–12 words per problem bullet, 13–18 per sell bullet, 11–13 per stat
label) are the real discipline: a block can be inside its total and still look wrong if one item is
three times the length of its neighbours. Peer items are peers.

---

## 3. Height budget — the page has no slack

Measured in headless Chrome, the 2026-07-17 reference lands with its CTA footer bottom at **exactly
297.00 mm**. There is no spare millimetre. Consequences:

- **Hero 38 mm.** The optional subheading buys its line back from the hero's own paddings and
  margins (`:has(.h1-sub)` rules in the template), so the band stays 38 mm. If it grew, the CTA
  contact block would be pushed off the page.
- **The disclaimer shares the fine-print row** with the legend and the price footnote instead of
  taking a line of its own.
- Section heights in the reference: hero 38 · pitch 98.2 · proof 45.6 · packages table 73.5 ·
  notes 3.2 · footer 16.9, with a 3 mm gap between sections and 2.2 mm above the footer.
- **`.page` uses `overflow: visible`, deliberately.** The reference build source clipped overflow,
  which silently cut the contact block off the bottom of an over-full page. Letting it spill makes
  Chrome emit a second PDF page, which is exactly what the build tool checks for.
- `main` must **not** get `min-height: 0`. With it, the overflow slides under the opaque CTA footer
  and disappears without a second page — a silent clip in a new disguise.

---

## 4. CSS tokens

**Fonts.** `"Helvetica Neue", Arial, sans-serif` only. No web fonts, no `@font-face`, nothing
fetched or shipped — Helvetica Neue on macOS, Arial everywhere else, and the layout is built to
tolerate the difference. The SoftServe wordmark and the spark are inline `<svg>`.

**Palette**

| Token | Hex | Used for |
|---|---|---|
| body ink | `#26282B` | body copy |
| hero / dark | `#17191C` | hero ground, bold labels in lists |
| accent blue | `#1485C3` | section headings, bullets, stats, tier L header, glyphs |
| eyebrow | `#C1DFF3` | hero eyebrow, hero subheading |
| hero sub | `#D9E4EC` | hero one-liner |
| sell orange | `#F36949` | CTA ground, sell-card bullets |
| sell heading | `#E2542F` | "Why it sells" heading |
| verticals label | `#A8552F` | "Where it applies" |
| sell card ground | `#FFF1EB` | the seller card |
| chip border | `#F9C4B2` | vertical chips |
| pipe / arrow | `#4A8FBC` | data-flow arrows |
| grey fill | `#EDF0F2` | source box |
| light-blue fill | `#F4FAFE` | platform box |
| proof ground | `#EAF4FB` | proof strip |
| KPI chip | `#E4F1FA` on `#0F6DA0` | solution chips |
| border | `#A9D3F1` / `#D8DEE3` | platform inner boxes / table rules |
| muted | `#4C5156` · `#6B7280` · `#8A9199` | small print, caveat, disclaimer |
| tier headers | `#DCEEFA` / `#A9D3F1` / `#1485C3` | S / M / L |

**Type scale** — `h1` 25pt/1.02 700 · `.h1-sub` 8pt 600 · `.sub` 9pt/1.4 · `h2.sec` 8pt 700
uppercase `.14em` · body `p, li` 8.3pt/1.42 · `.eyebrow` 6.4pt 600 uppercase `.20em` ·
`.kpi` 7.3pt 600 · `.chip` 7pt 500 · `.stat .num` 15.5pt 700 (inner `small` 8.5pt) ·
`.stat .lbl` 6.9pt · `.caveat` 6.4pt · tier name 10.5pt 700, size tag 7pt, scope 7pt/1.28 ·
row label 6.8pt 600 · value cell 8.2pt (price 9pt 700) · dot 7.8pt · notes 6.4pt ·
disclaimer 6.2pt · CTA question 10.5pt 700, answer 7.7pt, contact 9.5/7.4/8.4pt.

**Grid** — `.page` 210 × 297 mm flex column · `.hero` 38 mm, photo 46% right with a left-to-right
fade · `main` padding `4.4mm 10mm 0`, gap 3 mm · `.pitch` `57.5% / 39.5%`, column gap 3% ·
`.arch` `25mm 1fr 54mm`, column gap 2 mm · `.stats` equal columns, gap 3 mm · `table.pk`
`table-layout: fixed`, label column 47 mm · dashed bullets are 1.5 mm circles via `li::before`.

---

## 5. Print rules

- `@page { size: A4; margin: 0 }` and `-webkit-print-color-adjust: exact; print-color-adjust: exact`
  — without the second, Chrome drops every filled background and the page prints as line art.
- Printed with `--headless --print-to-pdf --no-pdf-header-footer`. The expected PDF page box is
  **594.96 × 841.92 pt**; the tool prints the measured box so a wrong paper size is visible.
- Chrome writes the PDF and then frequently lingers instead of exiting on macOS. The tool polls for
  the file to appear and stop growing, then stops the process — waiting on process exit hangs.
- **No external resources of any kind.** The hero photo is embedded as a `data:` URI at build time;
  logos are inline SVG. A one-pager that fetches anything will print blank boxes on a machine
  without the network, and the file is mailed around as a self-contained artifact.

---

## 6. What the builder reads from the pack spec

Required: `meta.name` (or `meta.name_variants.*`), `one_liner.full`, `problem_solution.problem`
and `.solution`, `packages.tiers[]`, `contacts.<channel>`.

Optional, and the reason several blocks exist at all: `problem_solution.reframe` and
`.problem_points[]` · `one_liner.kpi_chips[]` (else derived from `kpis[].name` + `direction`) ·
`architecture` (the data-flow line is derived from `inputs[0]` and the `stack[]` layers whose
`layer` names contain "app", "engine" or "infrastructure") · `verticals[].name` and
`.one_pager_line` · `kpis[].figure`, `.figure_prefix`, `.figure_suffix`, `.one_pager_label`,
`.attribution`, `.caveat` · `packages.why_it_sells_for_the_partner[]` ·
`packages.capability_handling[].levels.<tier>` · `clearance.disclaimer`.

The `one_pager:` block in the spec holds this artifact's own overrides: `eyebrow`, `cta.question`,
`cta.answer`, `proof_story`, `proof_story_anonymized`, `proof_logo`, `data_flow`, the row labels,
and any heading the pack wants to reword.

**Channel rules.** `--channel partner_print` takes the name from `meta.name_variants.external`
(plus `external_subheading`) and the contact from `contacts.partner_print`; `--channel internal`
takes `meta.name_variants.internal_slide` and `contacts.internal`. Attribution follows
`clearance.customer_name_allowed.<channel>`: allowed, the builder uses
`kpis[].attribution.named_when_allowed` and may print the customer logo; not allowed, it uses
`.otherwise`, prints no logo, and **refuses to build** (exit 2) if the customer name reaches the
page anyway.

**Capability cells.** Each `packages.capability_handling[]` entry needs a level per tier:
`levels: {pov: partial, integration: included, scaling: advanced}`, or a glyph-prefixed string
(`"● In: staff, availability …"`), or a `{level: …}` mapping. Prose with no level is an error, not
a guess — the tool says which entry and how to fix it. Levels map to
`— none · ◐ partial · ● included · ●● multi-region / advanced`.
