# Handing it to the listing

**What this is.** What the demo owes the product page once it is approved, and where it lives.

**The checks**

1. **The captures become the listing's step frames and poster** — one 16:10 frame per workflow step, cropped to the listing's fixed step-image spec, taken at DPR 2 from the state that carries the cleared figure. They land in `overview.steps[].image`; the poster is that run's final state.
2. **The listing gets the secondary CTA to the demo**, opening it **in a new tab**.
3. **The demo is published as its own page.** A walkthrough that lives inside the site tree cannot open as a top-level page when the site is served as a single preview artifact — a supporting file is not a document. So its standalone URL goes in the site's `links.json` (manifest `paths.links`) as `interactiveDemoArtifact`, while `interactiveDemo` holds the **canonical path**, `demo/<slug>/index.html`, for the real deployment.
4. **Both links are the owner's input**, never assumed and never a constant in this bundle. `videoPoster` stays in the switch block (`paths.config`); it shows only when `links.json` holds the recording (`video`), and no switch turns the frame on.
5. **Run the manifest's `paths.syncLinks`** (`node tools/sync-links.js`) **and then the site's own checker** after wiring the two links, `videoPoster` and the step images.
6. Record the round where the site keeps its records: the asks, the decisions, a before/after table, the checks run, and what is still open for the owner.

**Fills / reads:** the listing's `overview.steps[].image`; `interactiveDemo` and `interactiveDemoArtifact` in `links.json`; the switch block's `videoPoster`.
