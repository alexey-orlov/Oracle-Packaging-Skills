# One rebuild round, and the fast path

**What this is.** What happens after the owner's feedback: one rebuild round, and a shorter route when only one row changes.

**One rebuild round.** Take the feedback, change the spec, rebuild, re-lint, present again. If a second round would be needed, the feedback is about the capability tree itself rather than the document — say so and take it back to `/oracle-packs:spec`.

**A single-row change is a fast path.** Edit that row in the spec through the spec skill's fast path, rebuild, re-lint, and stop. Never re-run the whole procedure for one field.

**The change is always made in the spec**, never in the .docx: the feature list is the master every other artifact derives from, and a row edited only in the document is a divergence nobody else will see.

**Checks**

1. Every change went into the spec first, then the rebuild.
2. The .docx was never hand-edited.
3. The rebuild was re-linted on `internal` (card: `check`) before it was shown again.
4. One rebuild round; a second is escalated to the spec, not repeated here.
5. A single-row change stops at rebuild and re-lint — but if the fit ladder moved to a different rung, say so (card: `review-pack`).

**Good.** "Changed that one status to partially implemented; the page still fits at one row per feature."
**Bad.** Opening the .docx and editing the cell.

**Reads / writes:** the touched keys of `capabilities[]`, through `/oracle-packs:spec`.
