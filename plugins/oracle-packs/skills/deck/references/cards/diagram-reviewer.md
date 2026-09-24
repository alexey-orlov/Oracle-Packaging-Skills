# The architecture picture — reviewed elsewhere, checked here

**What this is.** Slide 8 does not draw its own diagram and does not review one. The pack's architecture model was built and reviewed ONCE, in `/oracle-packs:build` (its `architecture-picture` card), and this slide renders it. The deck's job here is to prove it still does.

**The check**

    shared/tools/py shared/tools/check_diagram.py <spec> --deck <pptx> --channel <channel>

It asserts every node name in the model is on the slide, letter for letter, that every arrow carries its data label, and that no box on the slide is missing from the model.

**Checks this step must pass**

1. `check_diagram.py` exits 0. A finding is drift: the slide is rebuilt from the model, never edited in PowerPoint.
2. The picture is wrong → fix the brief's architecture through the spec skill's fast path, not the slide, and rebuild the one-pager and the listing figure with it. The model is built from the brief, so all three move together.
3. Never review the picture here: it is reviewed once, in the build's architecture step, and a second reviewer on a picture three artifacts share is how they diverged.
4. The builder's plain-sentence summary of the diagram — the boxes, then the arrows — goes into the review pack, so the owner can check naming and direction without opening the slide. The build prints it under `architecture diagram:`.

**Bad.** "Point 4 failed: unlabelled edge."
**Good.** "The line from the dispatch system doesn't say what it sends; I've labelled it 'job status every 5 minutes' — tell me if that's wrong."

Rules and levels of detail: `shared/references/architecture-diagram.md`. What slide 8 places where: `references/cards/slides-6-10.md`.

**Reads:** the brief's `architecture`, through the model. **Writes:** nothing.
