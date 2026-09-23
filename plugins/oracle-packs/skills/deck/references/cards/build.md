# Building the deck

**What this is.** The ten-slide sales deck, **filled**, not drawn: `tools/build_deck_v2.py` copies the reference deck (`assets/exemplar/wfo-sales-deck.pptx`), replacing only content, so geometry, type, colour, corners, icons and the table idiom are the reference's by construction.

    python3 tools/build_deck_v2.py <spec> --out <dir> --channel <channel> --fit-report

Per-slide content and order: cards `slides-1-5` and `slides-6-10`, the same ten slides `shared/references/anatomy/artifact-deck.md` fixes.

**Checks the build must pass**

1. Ten slides in the anatomy's order. Packs differ in content, never in anatomy.
2. The running header `Oracle AI & Data Solutions — <pack name>` on every slide but the cover (`deck.running_header` overrides it).
3. The fit report is clean: no overflowing box, no detailed-table cell over its 12-word budget. Fix an overflow by shortening the wording (the spec skill's fast path), never by shrinking type below the floor.
4. An empty spec key shows the honest state ("results to follow", "scoped per engagement"), never a placeholder posing as fact.
5. The reference pack's customer logo never ships: replaced from this brief or removed; an empty frame is labelled "image to be chosen".
6. Delivered as a standalone .pptx on the exemplar's master, `<Pack name> - Sales deck - Oracle.pptx`; a section for someone else's deck is the executive-summary skill's job.
7. `tools/build_deck.py` is the **legacy** builder: it redraws the ten slides on the brand shell (no photo layout), so its cover is ink only and **fails the linter's cover check by design** (`--legacy-cover-ok` makes that a warning). Use it only without the exemplar, say in the review pack that the deck was redrawn, not filled, and never deliver it as final without the hero: set `deck.images.cover` or use the exemplar builder.

**Reads:** the whole spec. **Writes:** the .pptx; the fit report, architecture summary and pictures still to choose go to stdout.
