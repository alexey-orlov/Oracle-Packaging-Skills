# Looking at the render

**What this is.** A contact sheet of all ten rendered slides, read by eye for what a linter cannot see. `tools/render_probe.sh` says which renderer this machine has and how to make the sheet on it.

**Checks every slide must pass**

1. Peers share geometry: things that mean the same thing are the same size and shape.
2. No free-floating text — everything sits in a container.
3. Colour carries meaning, not decoration; two stages of one dimension are two tints of one hue.
4. No empty container pretending to be content. A deliberate empty state is labelled as one.
5. Corners are square on cards, panels, diagram boxes and containers. Only chips and numeral badges are pills, and none of them is half an inch tall.
6. Contrast holds — ink on the orange, white only on the dark hues.
7. **Beside the reference.** `tools/pair_sheet.py <reference renders> <built renders> out.png --map 6=5,7=6,8=7` pairs every built slide with the reference's. A band of another height, a card outside it or relabelled, a row added or lost — any difference the brief does not explain is a defect, not an idiom.

**Trust the fit report, not the glyphs.** The brand faces render only where they are installed; elsewhere the renderer substitutes: a render proves geometry and colour, never that the real font fits. The status marks take one symbol face for the same reason.

The full design rules are `shared/references/slide-design.md`, loaded with this card. The measured brand tokens (`references/brand-tokens.md`) are the builders', not yours.

**Reads:** the built .pptx. **Writes:** the contact sheet, which goes into the review pack.
