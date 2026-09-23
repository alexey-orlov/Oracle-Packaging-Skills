# What goes in the six blocks

**What this is.** The slide compresses the deck to one line per component. As the builder draws it: use case (problem → solution, with the verticals under it), solution layers, and proof of value across the top row; service packages, the area-and-category tree and planned next steps below; a footnote along the bottom.

**What fits.** Problem and solution ≈ 75 words together, verticals ≈ 20 · layer name ≤ 5 words, four rungs the shape and six the practical maximum · proof figure ≤ 20 characters, caption ≤ 10 words · tier scope ≤ 18 words · about 10 category rows · next-step title ≤ 6 words, detail ≤ 10. Past these the fit report starts failing.

**Checks**

1. One line per component, and it reads for someone who has not seen the deck: every term it uses, it introduces.
2. The proof set is all or none. When any figure is restricted away from this channel, the block is drawn as an empty panel with one grey line and the builder says so — never half-filled. Fix the clearance instead.
3. The tree carries areas and categories only; feature names belong on the feature list. More than about ten rows means trimming areas or categories, not shrinking them.
4. Up to four planned next steps, from the spec. With none, the panel is still drawn, empty with one grey line — an absent component is an empty container, never a dropped block.
5. The tiers strip carries each tier's scope, price with its status, and duration; an indicative price gets its footnote.
6. The footnote carries the caveat, the price footnote and any stated divergence from the pack, in two lines at most.

**Reads:** `problem_solution`, `verticals[].name`, `architecture.stack[]`, `kpis[]`, `packages.tiers[]`, `capabilities[]`, `exec_summary.next_steps[]`, `clearance.*`.
