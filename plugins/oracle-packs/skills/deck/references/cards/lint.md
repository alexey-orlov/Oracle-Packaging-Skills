# Linting the deck

**What this is.** The deck's own automatic check, every budget measured from the exemplar itself, so it holds a build to the reference rather than to an opinion. It runs before the render QA, and certainly before the owner.

    python3 tools/lint_deck.py <pptx> --spec <spec> --channel <channel>

**Checks it holds the build to**

1. Ten slides; the running header on every slide but the cover; no tier line on the cover.
2. The cover carries the family's hero — the reference's own photo title layout, with a picture reaching the cover from it or from the slide. An ink-only cover is an unfinished state.
3. The reference's own type faces, and package-table type at or above the reference's own floor.
4. No rounded card — a rounded shape over 0.55 in tall fails — and no more pills than the reference's own slide carries.
5. An icon rather than a number on every industry card.
6. **The proof slide is the delivered case in the reference's composition:** four blocks labelled CONTEXT · SOLUTION · VALUE FOR ORACLE + NVIDIA · VALUE FOR CLIENT, in that order; three stat tiles, each with a figure and a caption; the customer's logo on the slide exactly when the brief clears the name for this channel and names a logo file. Cleared with no file warns; no clearance, no picture.
7. The architecture slide names the pack, the engine's products, and every system the result goes to, with one arrow per source.

**It must exit 0** before anything is rendered. A finding is fixed in the pack brief or in the build — never by loosening the check, never by shrinking type below the floor.

**The one flag, and what it is not.** `--legacy-cover-ok` belongs to the legacy redrawing builder alone (`tools/build_deck.py`, for a machine without the exemplar): it demotes the two checks that path cannot pass — the cover's hero and the proof slide's composition — to loud warnings. A deck that needed it is not a final deliverable: set `deck.images.cover` or build with the exemplar builder. Never reach for it to get a normal build past the check.

Its numbers come from `references/reference-geometry.json`, which the tool reads and you do not.

**Reads:** the built .pptx and the spec. **Writes:** nothing.
