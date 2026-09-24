# The sales deck — .pptx, ten slides

**What this is.** The ten-slide deck for Oracle and SoftServe sellers, **filled, not drawn**: `deck/tools/build_deck_v2.py` copies the reference deck (`deck/assets/exemplar/wfo-sales-deck.pptx`) and replaces only content, so geometry, type, colour, icons and the table idiom are the reference's. What each slide carries: cards `deck-slides-1-5` and `deck-slides-6-10`.

    shared/tools/py deck/tools/build_deck_v2.py <spec> --out <dir> --channel <channel> --fit-report

The channel is `partner_print` unless the owner said "our own team" (`internal`: prices in full, named accounts and internal notes where the brief allows). An unchosen picture slot stays an empty container labelled "image to be chosen": an open item.

**Checks**

1. Ten slides in the fixed order: packs differ in content, never anatomy. The running header `Oracle AI & Data Solutions — <pack name>` on every slide but the cover.
2. The fit report is clean; an overflow is answered by shorter wording in the spec, never type below the floor.
3. The deck's own check (`deck/tools/lint_deck.py`) exits 0 before any render: slide count and header, the family's hero on the cover, the reference's faces and table floor, card heights and pills, an icon on every industry card, the proof slide's composition, the architecture's names and arrows. Fix the brief or the build, never the check.
4. Slide 8 renders the pack's one reviewed model: `check_diagram.py` clean, never reviewed again here.
5. The reference pack's customer logo never ships: replaced from this brief or removed.
6. Delivered as `<Pack name> - Sales deck - Oracle.pptx`, on the exemplar's master.

**The review pack adds** the contact sheet of all ten, the .pptx attached; the layout decisions; the architecture in plain sentences, every box and arrow (the build prints them), never "see slide 8"; every industry that kept a stand-in icon and every empty picture slot, as open items.
