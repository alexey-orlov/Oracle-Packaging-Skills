# Building the deck

**What this is.** The ten-slide sales deck, **filled** rather than drawn: `tools/build_deck_v2.py` opens a copy of the reference deck (`assets/exemplar/wfo-sales-deck.pptx`) and only replaces content, so geometry, type, colour, corners, icons and the table idiom come from the reference by construction.

    python3 tools/build_deck_v2.py <spec> --out <dir> --channel <channel> --fit-report

Per-slide content and order: `references/cards/slides-1-5.md` and `references/cards/slides-6-10.md` — this skill's ten, which supersede the delivered reference deck's order in `shared/references/anatomy/artifact-deck.md`.

**Checks the build must pass**

1. Ten slides in the anatomy's order. Packs differ in content, never in anatomy.
2. The running header — `Oracle AI & Data Solutions — <pack name>` — on every slide but the cover (`deck.running_header` overrides the wording).
3. The fit report is clean: no overflowing box, no detailed-table cell over its 12-word budget. An overflow is fixed by shortening the wording through the spec skill's fast path, never by shrinking type below the floor.
4. An empty spec key shows the honest state — "results to follow", "scoped per engagement" — never a placeholder that reads as fact.
5. The reference pack's customer logo never ships on this deck: it is replaced from this brief or removed, and an empty frame is labelled "image to be chosen".
6. Delivered as a standalone .pptx on the exemplar's own master, `<Pack name> - Sales deck - Oracle.pptx`. A section that pastes into someone else's deck is the executive-summary skill's job.
7. `tools/build_deck.py` is the **legacy** builder: it redraws all ten slides on the brand shell. Use it only where the exemplar is unavailable, and declare in the review pack that the deck was redrawn rather than filled.

**Reads:** the whole spec. **Writes:** the .pptx; the fit report, the architecture summary and the pictures still to choose print on stdout.
