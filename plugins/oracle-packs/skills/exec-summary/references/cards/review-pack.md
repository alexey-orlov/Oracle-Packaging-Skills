# Showing the slide

**What this is.** What goes in front of the owner once the slide is built, checked and edited: the render, the file, and the few things they need in order to judge it — then one question.

**Checks**

1. The rendered slide is open beside the conversation as an image, with the editable file attached, *before* the question is asked (`shared/cards/review-protocol.md`). Never a description of the slide instead of the slide.
2. The pack says what was compressed and what was dropped to make it fit — in plain words, by the block's name on the slide.
3. Anything inferred is named as inferred, with what it was inferred from.
4. Open items are listed as items, in the owner's words, not buried in a paragraph.
5. One question, one choice: approve, change (free text), or stop. No rule codes, file names, spec keys, script names or packaging vocabulary anywhere in it.
6. One rebuild round. A change to a single block is the fast path (card `fast-path`), not a rerun of the build.

**Delivery.** `<Pack name> - Executive summary - Oracle.pptx`, plus the slide number where it should be inserted whenever a host deck was given.

**Done means** built on the right master, fit and lint clean, consistent with the spec, review pack shown, and the owner's decision logged in `<work>/decisions.md`.

**Bad.** "Exec summary built, fit report clean, 0 lint findings — approve?"
**Good.** "Here is the slide, built on your section deck so it drops in as slide 14. The three metrics are on it; the workflow and the feature names are not, because they belong on the deck and the feature list."
