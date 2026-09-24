# The feature list — .docx, one A4 page

**What this is.** The pack's spine document and its `internal` cut: Area > Category > Feature, a status per feature, the standard customization scope per area. Every other artifact condenses it; no prices. A copy for an Oracle seller is linted again on `partner_print`; only the name variant may differ.

**The page, in order.** The mini-site lockup (SoftServe wordmark, hairline rule, `Oracle AI & Data Solutions`); H1: the internal name variant + " — Feature list"; two intro lines: `one_liner.full` (or `feature_list.intro`), then "For " + `icp.line`; the matrix `Area | Category | Features | Current status | Standard customization scope` (optional `Tier first available`), cells merged down; the legend (● available, ◐ partial, ○ roadmap); at most three footnotes. No page footer: the spec version and build date go into the file's properties.

    shared/tools/py feature-list/tools/build_feature_list.py <spec> --out <dir>

The build walks a fit ladder (a row per feature at 7.5pt, then 7pt, then a row per category without the status column) and verifies the page count where Pages or LibreOffice is installed; pass any `WARNING` line on. Exit 3: nothing was written (card `feature-list-fit`).

**Checks**

1. Rows follow the spec's order and wording, never "improved"; a missing `icp.line` goes back to the spec, never invented.
2. Three distinct glyphs at one size, never two colours of one.
3. A `customer`-tagged feature marked ● is questioned first: it is usually ◐ with customization.
4. Every feature has a status and every area its customization line; counts per area match the spec.

**The review pack adds** per area, how many capabilities are available, partial and on the roadmap, in words; the ladder rung and whether the page was verified; every status that came from research, not from what we built.
