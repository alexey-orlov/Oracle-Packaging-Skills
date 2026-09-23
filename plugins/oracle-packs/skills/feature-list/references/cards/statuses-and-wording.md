# What the cells may say

**What this is.** The rules governing the matrix's own text: the status glyphs, the feature names, and what this document never carries.

**Statuses**, as the owner settled them: **●** available out of the box, configuration may be required · **◐** partially implemented, major improvements on the roadmap · **○** planned, not implemented today. Three distinct shapes, never two ● separated only by colour — colour alone cannot be read in greyscale print, in a forwarded screenshot, or by a screen reader. All three are set in one symbol face so they come out the same size.

**Feature wording is the spec's.** Do not "improve" a name here: one word for one thing across every artifact.

**The four-axis specificity tag** (customer / engine / use case / industry) is not printed. But a feature tagged `customer` and marked ● must be questioned before printing — it is usually ◐ with customization.

**Checks**

1. No two statuses share a glyph, and the three glyphs render at the same size.
2. No feature name was rewritten, shortened or prettified against the spec.
3. Every `customer`-tagged feature marked ● was put to the owner before the document went out.
4. No pricing, no tiers table, no proof figures anywhere in this document.
5. The legend's three entries match the three glyphs used, in the wording above.

**Good.** Customization scope: "Tuning the allocation-rule weights per customer."
**Bad.** A row reading "Dispatcher UI — from £12k at PoV tier".

**Reads:** `capabilities[]` — feature names, `status`, `customization_scope`, and the specificity tags. Writes nothing.
