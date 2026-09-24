# The review after each artifact

**What this is.** The pause after every artifact, on top of the shared review protocol: the review pack (the artifact's card says what it adds), then one widget.

**The widget.** Title `Artifacts · n of N · <artifact name>`, with exactly three options: **Approve and continue · Rebuild with changes (free text) · Stop here**. `n of N` counts only the artifacts being built.

**The rebuild round.** One per artifact. Every builder writes the whole file from the spec, so a change to one slide, block or row is a change to one line of the brief, through the spec skill's fast path; wording that belongs only to the one-pager or the executive summary goes into its own block of the spec (`one_pager:`, `exec_summary:`) through `packspec.py set`. Rebuild, re-run every check on the whole file, show the changed part. A second round on the same point is about the brief, not the document: say so and send it to `/oracle-packs:spec`. A change to the architecture goes back through the architecture step, and all three drawings move with it.

**Checks**

1. Every artifact is approved through the widget, and the next never starts before that approval: the owner's feedback on one changes the next.
2. The review pack names the artifact's parts, never spec keys, files, checks or tools.
3. A change to a price or figure rebuilds every artifact that prints it; say which files changed.
4. The approval goes into `<work>/decisions.md` with the file's spec stamp (`shared/tools/py shared/tools/spec_stamp.py <file>`).

**Good.** "Two of the capability rows come from the research rather than from what we built — confirm them, or move them to the roadmap."
**Bad.** "`capabilities[2].status` failed the third check; rerun the linter."

**Writes:** the approval into `<work>/decisions.md`.
