# The sales one-pager — HTML → print → one A4 PDF

**Section order**

1. **Hero**: eyebrow (the family name, **Oracle AI & Data Solutions**), H1 (the external name variant), `p.sub` (the full one-liner), hero photograph faded behind the right 46%.
2. **Pitch**, two columns (≈57.5/39.5). Left: "The problem" + a lead sentence + three dashed bullets; "The solution: \<reframe\>" + three outcome chips + the mechanism in two sentences; then the `.arch` line: source left, platform box right, two labelled pipes between. Right: the "Why it sells: for \<partner\> account teams" card, three bullets, a "Where it applies" chip row.
3. **Proof strip**: logo where cleared, else the anonymized descriptor; the three-sentence story about the customer's business problem and what changed for them, never the engagement's mechanics (weeks, phases, source counts, contract status); three `.stat` figures, business metrics only; the caveat beneath.
4. **Packages**: three tier headers (name + size tag + scope sentence); infrastructure price, services price, timeline; capability rows as glyphs; the legend bottom-left, the price footnote bottom-right. The PoV column carries the "Proof accepted when …" line when the brief holds technical criteria.
5. **CTA footer**: the question, the offer answer, the named contact block.

**The components here.** Name → H1. One-liner → `p.sub`. ICP → the "Where it applies" chips. Capabilities → the packages table's glyph rows. Architecture → the compact `.arch` diagram. KPIs → the three stats plus the caveat. Optional products: absent by design.

**Format.** One `.page` at `210mm × 297mm`, `@page { size: A4; margin: 0 }`, exact print colour. `.page` keeps `overflow: visible` so an overflow emits a second page the tool fails, never a silent clip. No web fonts or external assets: logos inline as SVG, photographs as base64 `data:` URIs. Section order is fixed; content is cut to fit.
