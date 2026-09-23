# The review pack

**What this is.** What the owner is given to approve: the document, a way to read it inside the conversation, and the things only they can settle.

**What it holds.**

- The .docx, and a plain-text rendering of the table so it can be read in chat.
- Per area, how many capabilities are available, partially available and on the roadmap — in those words, never as a count of glyphs.
- **How the page came out:** one row per feature, or a row per category — and, if the latter, that the status column went away because the statuses now sit beside each feature. Say whether the single page is an estimate or was verified.
- Any feature whose status came from research rather than from what we actually built: name it, say so plainly, and let the owner confirm it or move it to the roadmap.

**Checks**

1. The render is open beside the conversation before the question is asked.
2. Availability is stated in words, per area, never as glyph counts.
3. Both the layout used and whether the page was verified are stated.
4. Every researched status is named individually, not summarized as "some of them".
5. Nothing in the pack names a file, a spec key, a check or a tool.

**Good.** "In Signal intake, four capabilities are available today, one partially, and two are on the roadmap."
**Bad.** "Signal intake: 4 ● · 1 ◐ · 2 ○."

**Reads:** the built document and the spec. **Writes:** the owner's approval into `packs/<slug>/decisions.md`.
