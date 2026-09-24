# The capabilities

**What this is.** The pack's single feature truth: **Area > Category > Feature**, a status per feature, and what is standardly customized per area. Every other document derives its capability view from it, dropping features but never adding one. How each row is written: card `capabilities-rows`.

**The statuses**, as the owner settled them: ● **available** out of the box, configuration may be required; ◐ **partial**, partially implemented, major improvements on the roadmap; ○ **roadmap**, planned, not implemented today.

**Sized for one page** — the feature list is one A4 page, a requirement. At most **6 areas, about 12 categories, about 25 features at a row each** (up to about 50 in the compact layout, features inline per category), names of 8 words or fewer; past that the build drops to a row per category, without the status column. Group here — merge siblings, fold a small category into its neighbour, shorten names — never at build time, where the only lever is type size.

**Checks the draft must pass**

1. Within the size above, and stated per area in words: how many are available, partial and on the roadmap.
2. Nothing "theoretically also possible"; no pricing anywhere on this tree.
3. Each area carries its customization scope in sellable words: what stays custom per engagement once the feature is finished, not the build backlog.
4. Every feature is tagged reusable as it stands or built per engagement; the latter are the priced scope.
5. If nothing at all is on the roadmap, say so plainly: the list never left what we built for the customer.

**Good.** Customization scope: "Balancing the optimization function with penalties and rewards; tuning allocation-rule weights per customer."

**Fills:** `capabilities[]` (`area`, `customization_scope_area`) and `capabilities[].categories[].features[]` (`name`, `status`, `tier_first_available`, `customization_scope`, `specificity`).
