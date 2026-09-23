# The capabilities

**What this is.** The pack's single feature truth: **Area > Category > Feature**, a status per row (● available · ◐ partial · ○ roadmap), and what is standardly customized per area. Every other document derives its capability view from it, dropping features but never adding one.

**Sized for one page** — the feature list is one A4 page, a requirement, not a preference. At most **6 areas, about 12 categories, about 25 features with one row per feature** (up to about 50 in the compact layout, features inline per category), feature names of 8 words or fewer. Past that the build falls back to a row per category, which drops the status column. Group here — merge sibling features, fold a small category into its neighbour, shorten names — never at build time, where the only lever is type size.

**Checks the draft must pass**

1. Within the size above, and stated per area: how many are available, partially available and on the roadmap — in those words, never as glyph counts.
2. Every status is supported by the inputs at the granularity claimed; a status the source only supports per category is not claimed per feature.
3. Nothing "theoretically also possible"; no pricing anywhere on this tree.
4. Each area carries its customization scope in sellable words — what the engagement configures for this customer, not a spec dump.
5. Every feature is tagged reusable as it stands or built per engagement; the latter are the priced scope.
6. If nothing at all is on the roadmap, say so plainly: the list never left what we built for the customer.

**Good.** Customization scope: "Balancing the optimization function with penalties and rewards; tuning allocation-rule weights per customer."

**Fills:** `capabilities[]` — areas, categories, features, `status`, `customization_scope`, specificity.
