# Showing the page

**What this is.** What goes in front of the owner once the page is built, checked and edited: the render, the editable file, and the few things they need in order to judge it — then one question.

**Checks**

1. The PDF page is open beside the conversation as an image, with the editable file attached, *before* the question is asked (`shared/cards/review-protocol.md`). Never a description of the page instead of the page.
2. The pack says which blocks are at or over length and by how much — in plain words, by the block's name on the page.
3. Anything inferred is named as inferred, with what it was inferred from.
4. Open items are listed as items, in the owner's words, not buried in a paragraph.
5. One question, one choice: approve, change (free text), or stop. No rule codes, file names, spec keys, script names or packaging vocabulary anywhere in it.
6. One rebuild round. A change to a single block is the fast path (card `fast-path`), not a rerun of the whole build.

**Delivery.** The PDF and its editable HTML twin, named `<Pack name> - Sales one-pager - Oracle.pdf` and `<Pack name> - Sales one-pager - Oracle.html`. The HTML ships with it on purpose: it is the editable source, the PDF is a render of it.

**Done means** one A4 page, both checkers clean, the editorial pass made, the review pack shown, and the owner's decision logged in `<work>/decisions.md`.

**Bad.** "Built the one-pager, lint clean, 2 blocks OVER budget — approve?"
**Good.** "Here is the page. The packages table is the fullest block and the proof story is at its limit; the infrastructure price is marked indicative because the spec marks it so."
