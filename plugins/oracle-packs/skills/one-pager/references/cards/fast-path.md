# One change, not a rebuild

**What this is.** The owner asks for one thing — a shorter problem paragraph, a different closing question, a price that moved, one more industry. Change that, rebuild, re-check, show it, stop.

**Checks**

1. Load this card and the card for the part being changed; nothing else. Never rerun the flow for one field, and never re-ask a settled question.
2. Wording that also appears in another artifact changes in the spec, through the spec skill's fast path — the page is the deck condensed, never a second source of truth.
3. Wording that belongs only to this page changes in the spec's `one_pager:` overrides, through `packspec.py set`. The output file is regenerated, never hand-edited: a hand edit is lost on the next build.
4. Rebuild and re-run the one-page check as well as both checkers — a few added words can push the page to two (card `overflow`).
5. Re-show it the same way: the render open beside the conversation, the editable file attached, then the question.
6. Close in one line: what changed and what deliberately did not.

**Bad.** Editing the built HTML so the owner sees the fix faster.
**Good.** Moving the price in the spec, rebuilding both the deck and this page from it, and saying which two files changed.

**Reads/writes:** the `one_pager:` block and whichever component key the change touches, each with its source.
