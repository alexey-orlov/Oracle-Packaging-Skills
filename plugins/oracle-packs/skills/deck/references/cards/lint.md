# Linting the deck

**What this is.** The deck's automatic check, its budgets measured from the exemplar and kept in `references/reference-geometry.json`, which the tool reads and you do not: it holds a build to the reference, not an opinion, before render QA and the owner.

    shared/tools/py tools/lint_deck.py <pptx> --spec <spec> --channel <channel>

**What it checks**

1. Ten slides; the running header on all but the cover, which has no tier line.
2. The cover carries the family's hero: the reference's photo title layout, pictured from the layout or the slide. An ink-only cover is unfinished.
3. The reference's type faces; package-table type at or above its floor.
4. No rounded card over 0.55 in tall; no more pills than the reference slide.
5. An icon, not a number, on every industry card.
6. **The proof slide is the delivered case in the reference's composition:** blocks CONTEXT · SOLUTION · VALUE FOR ORACLE + NVIDIA · VALUE FOR CLIENT, in that order; three stat tiles, each a figure and a caption; the customer's logo exactly when the brief clears the name for this channel and names a logo file. Cleared with no file warns.
7. The architecture slide names the pack, the engine's products and every destination system, one arrow per source.

**It must exit 0** before any render. Fix findings in the brief or the build, never by loosening the check or shrinking type below the floor.

**The one flag, and what it is not.** `--legacy-cover-ok` serves only the legacy redrawing builder (`tools/build_deck.py`, when the exemplar is missing), turning the cover's hero and proof-slide composition checks into loud warnings. A deck that needed it is not final: set `deck.images.cover` or use the exemplar builder. Never use it on a normal build.

**Reads:** the built .pptx and the spec. **Writes:** nothing.
