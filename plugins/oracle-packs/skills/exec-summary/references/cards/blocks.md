# What goes in the six blocks

**What this is.** The slide compresses the deck to one line per component: use case (problem → solution, verticals under it), solution layers and proof of value across the top row; service packages, the area-and-category tree and planned next steps below; a footnote along the bottom.

**What fits.** Problem and solution ≈ 75 words together, verticals ≈ 20 · layer name ≤ 5 words, four rungs the shape, six the maximum · proof figure ≤ 20 characters, caption ≤ 10 words · tier scope ≤ 18 words · about 10 category rows · next-step title ≤ 6 words, detail ≤ 10. Past these the fit report fails.

**Checks**

1. One line per component, and it reads for someone who has not seen the deck: every term it uses, it introduces.
2. The proof strip carries **business metrics only** (`kind != technical`); technical criteria ride the PoV tier's scope as "Proof accepted when …". The set is all or none: a figure restricted away from this channel empties the panel to one grey line, never half-filled. **No cleared figure is a different state** — the strip names the metrics being measured, where the figures will stand, under one line: "Measured in the proof of value; results to follow."
3. The tree carries areas and categories only; feature names belong on the feature list. Above about ten rows, trim areas or categories rather than shrink them.
4. Up to four planned next steps. With none, the panel is still drawn, empty with one grey line — an absent component is an empty container, never a dropped block.
5. The tiers strip carries each tier's scope, price with its status, and duration; an indicative price gets its footnote.
6. The footnote carries the price footnote and any stated divergence, two lines at most. The metric caveat travels with the figures — with none printed, it is dropped. A divergence line that is a full sentence stands alone; only a fragment takes the "Pack scope differs…" run-in.

**Reads:** `problem_solution`, `verticals[].name`, `architecture.stack[]`, `kpis[]` (`kind`, `figure`), `packages.tiers[]`, `capabilities[]`, `exec_summary.next_steps[]`, `clearance.*`.
