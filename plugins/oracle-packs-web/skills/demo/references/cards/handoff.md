# Handing it to the listing

**What this is.** What the demo owes the product page once it is approved, and where it lives.

**The checks**

1. **The captures become the listing's step frames and poster** — one 16:10 frame per workflow step, cropped to the listing's fixed step-image spec, taken at DPR 2 from the state that carries the cleared figure. They land in `overview.steps[].image`; the poster is that run's final state.
2. **The listing gets the secondary CTA to the demo**, opening it **in a new tab**.
3. **The demo is published as its own page.** A walkthrough that lives inside the site tree cannot open as a top-level page when the site is served as a single preview artifact — a supporting file is not a document. So its own standalone URL goes in the listing's `demoPreviewUrl`, while `demoUrl` keeps the **canonical relative path** for the real deployment, unchanged.
4. **Both URLs are the owner's input**, never assumed and never a constant in this bundle.
5. **Run the site's own checker** after wiring `demoUrl`, `demoPreviewUrl`, `videoPoster` and the step images.
6. Record the round where the site keeps its records: the asks, the decisions, a before/after table, the checks run, and what is still open for the owner.

**Fills / reads:** the listing's `overview.steps[].image`, and the switch block's `demoUrl`, `demoPreviewUrl`, `videoPoster`.
