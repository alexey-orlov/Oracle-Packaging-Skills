# When it does not fit on one page

**What this is.** Exit 3 from the build: the capability tree does not fit one A4 page even in compact mode at 7pt, and **nothing was written**.

**Do not retry with smaller type.** 7pt is the floor — below it the matrix stops being readable, and the answer is a coarser capability tree, never smaller type. Group in the spec, where the tree lives, not at build time, where the only lever is type size. The sizing rule is on `shared/references/anatomy/capabilities.md`.

**What to put to the owner**, in plain words, using the counts the build printed — the estimated height against the budget, the number of areas / categories / features, the three largest areas and the five largest categories:

- which categories to merge into one,
- which sibling features to generalize into a single capability,
- which names to shorten.

Get their decision, fix the tree through `/oracle-packs:spec`, and rebuild.

**Checks**

1. Nothing was written, and no retry was made at a smaller size.
2. The counts quoted to the owner are the build's own, not re-counted by hand.
3. The proposal names specific areas, categories and features — never "the tree is too big".
4. The tree is changed in the spec through `/oracle-packs:spec`, never edited in the document.
5. The owner hears no exit code, tool name or raw build output.

**Good.** "Intake and normalization carry nine features between them; merged into one category they read as three, and the page fits."
**Bad.** "The build exited 3 — I'll rerun it at 6.5pt."

**Reads:** the build's exit-3 report. **Changes:** `capabilities[]`, through the spec skill.
