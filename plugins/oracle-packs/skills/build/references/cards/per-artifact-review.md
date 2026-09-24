# The review after each artifact

**What this is.** The pause that follows every artifact: the review pack the artifact skill produced, opened beside the conversation, then one widget with three ways out.

**What is shown.** The review pack as the artifact skill produced it — the renders or the file, a TLDR of the decisions taken, the list of anything synthetic or unconfirmed, and the open items — all of it in the owner's words, with no key names, check names or method vocabulary in it. Before the question, that artifact's render opens in the side panel and its editable file is attached alongside.

**The widget.** Title `Artifacts · n of N · <artifact name>: approve, change or stop`. Exactly three options: **Approve and continue · Rebuild with changes (free text) · Stop here**. On "Rebuild", pass the free text to that artifact skill's fast path and present the rebuilt artifact again.

**Checks**

1. Every artifact is approved through a widget, and the next artifact never starts before that approval.
2. The render was open beside the conversation before the question was asked.
3. The review pack names the artifact's parts — never spec keys, file names, check names or the tool that produced it.
4. "Rebuild with changes" goes through the artifact skill's fast path, never a hand edit of the produced file.
5. `n of N` counts only the artifacts actually being built.

**Good.** "Two of the capability rows come from the research rather than from what we built — confirm them, or move them to the roadmap."
**Bad.** "`capabilities[2].status` failed the third check; rerun the linter."

**Reads:** the artifact skill's review pack. **Writes:** the approval into `<work>/decisions.md`, with the file's spec stamp.
