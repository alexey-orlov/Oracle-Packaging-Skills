# The sales one-pager — HTML → print → one A4 PDF

**Section order**

1. **Hero** — eyebrow, H1 (the external name variant), `p.sub` (the full one-liner), the hero photograph faded behind the right 46%.
2. **Pitch**, two columns (≈57.5/39.5). Left: "The problem" + one lead sentence + three dashed sub-problem bullets; "The solution: \<reframe\>" + three outcome chips + the mechanism in two sentences; then the `.arch` line: source system left, platform box right, two labelled pipes between. Right: the "Why it sells: for \<partner\> account teams" card, three bullets, and a "Where it applies" chip row.
3. **Proof strip** — logo where cleared or the anonymized descriptor, the three-sentence story, three `.stat` figures, the caveat beneath.
4. **Packages** — three tier headers (name + size tag + scope sentence); infrastructure price, services price, timeline; capability rows as glyphs; the legend bottom-left, the price footnote bottom-right.
5. **CTA footer** — the question, the offer answer, the named contact block.

**The components, in the form they take here.** Name → the H1. One-liner → `p.sub`, canonical. ICP → the "Where it applies" chips. Capabilities → the packages table's capability rows, glyphs only. Workflow → one sentence in the solution body. Architecture → the `.arch` diagram, canonical compact form. KPIs → the three stats plus the caveat. Packages → the canonical compact table. Optional products are absent by design.

**Format.** One `.page` at `210mm × 297mm`, `@page { size: A4; margin: 0 }`, exact print colour. `.page` keeps `overflow: visible` deliberately: clipping hides an overflow instead of failing the build, and visible is what makes the renderer emit the second page the tool checks for. No web fonts, no external assets: logos inline as SVG, photographs as base64 `data:` URIs. The section order is not negotiable; content is cut to fit.
