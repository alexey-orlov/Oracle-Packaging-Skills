# The review pack

**What this is.** Everything the owner needs in order to approve the deck, opened beside the conversation *before* the question is asked, and then one widget: approve, or say what to change.

**What goes in it**

- The contact sheet of all ten renders, with the .pptx attached alongside.
- A short note on the layout decisions taken.
- The architecture in plain sentences — every box and every arrow, from the builder's summary — never "see slide 8".
- Everything inferred or unconfirmed, and the open items.

**Checks it must pass**

1. Every item is named as what it is on the slide — "the photograph on the right of the before-and-after slide" — never as a spec key, a file name, a script or a design rule's number.
2. Any industry that kept a stand-in icon, and any picture slot still empty, is an open item in plain words.
3. A deck built with the legacy redraw builder says so, in the owner's words: the deck was redrawn rather than filled from the reference — and that its cover is still missing the family's picture, which is why it is not the final file.
4. The owner is looking at the thing when the question arrives, not at a description of it.
5. Nothing is published as a claude.ai artifact; pack material stays on the machine.

**Good.** "Three of your four industries have a picture. Transport kept a stand-in, so it still needs one you choose."
**Bad.** "`verticals[2].icon` unresolved; exemplar fallback applied."

**Writes:** the owner's approval and the decisions taken, into `<work>/decisions.md`.
