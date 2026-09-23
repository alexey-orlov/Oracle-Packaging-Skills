# Linting the deck

**What this is.** The deck's own automatic check. Every budget in it is measured from the exemplar itself, so it holds a build to the reference rather than to an opinion. It runs before the render QA, and certainly before the owner.

    python3 tools/lint_deck.py <pptx> --spec <spec> --channel <channel>

**Checks it holds the build to**

1. Ten slides; the running header on every slide but the cover; no tier line on the cover.
2. The reference's own type faces, and package-table type at or above the reference's own floor.
3. No rounded card — a rounded shape over 0.55 in tall fails — and no more pills than the reference's own slide carries. Chips and numeral badges are the only pills.
4. An icon rather than a number on every industry card.
5. The architecture slide names the pack, the engine's products, and every system the result goes to, with one arrow per source.

**It must exit 0** before anything is rendered for review. A finding is fixed in the pack brief or in the build — never by loosening the check, and never by shrinking type below the floor.

Its numbers come from `references/reference-geometry.json`, which the tool reads and you do not.

**Reads:** the built .pptx and the spec. **Writes:** nothing.
