# One change, not a rebuild

**What this is.** The owner asks for one thing — a shorter problem line, a different next step, a price that moved, the slide on another deck's master. Change that, rebuild, re-check, show it, stop.

**Checks**

1. Load this card and the card for the part being changed; nothing else. Never rerun the flow for one field, and never re-ask a settled question.
2. Wording that also appears in another artifact changes in the spec, through the spec skill's fast path — the slide is the deck compressed, never a second source of truth.
3. Wording that belongs only to this slide changes in the spec's `exec_summary:` block, through `packspec.py set` (or `--title` for the title alone). The file is regenerated, never hand-edited in PowerPoint: a hand edit is lost on the next build.
4. A new host deck means a new build with `--host-deck`, not a re-theme of the slide you already have.
5. Rebuild with `--fit-report` and re-run both checkers: a few added words can push a panel into overflow, and overflow is cut, not shrunk.
6. Re-show it the same way — the render open beside the conversation, the file attached, then the question — and close in one line: what changed, and what deliberately did not.

**Bad.** Nudging a text box in PowerPoint so the owner sees the fix sooner.
**Good.** Moving the duration in the spec, rebuilding the deck and this slide from it, and saying which two files changed.

**Reads/writes:** the `exec_summary:` block and whichever component key the change touches, each with its source.
