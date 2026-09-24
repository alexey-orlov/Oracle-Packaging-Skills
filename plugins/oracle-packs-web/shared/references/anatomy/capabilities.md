# Component 6 — capabilities → features → customization

**What this is.** The master capability tree, **Area > Category > Feature**, with a status per row (● available · ◐ partial · ○ roadmap) and a standard customization scope per area. Every other capability rendering in every other artifact derives from it.

**Checks the draft must pass**

1. **Sized for one A4 page** — at most 6 areas, about 12 categories, about 25 features at a row per feature (up to about 50 in the compact layout, features inline per category), feature names of 8 words or fewer. Group here — merge sibling features, fold a small category into its neighbour, shorten names — never at build time, where the only lever left is type size.
2. Every status is supported by the inputs at the granularity claimed; a status the source supports only per category is not claimed per feature.
3. Each area carries its customization scope in sellable words — what the engagement configures for this customer, not a spec dump.
4. Nothing "theoretically also possible". No pricing anywhere on this tree.
5. Three distinct glyphs, never two colours of the same one: a colour distinction vanishes in plain text, in print and in any converted copy.
6. The site's stage view is **derived** from this tree by mapping each feature to a workflow step. It may drop features; it may never add one.

**Good.** Customization scope: *"Balancing the optimization function with penalties and rewards; tuning allocation-rule weights per customer."*

**Bad.** A feature list with prices on it. `●` in two shades, one meaning available and the other partial.

**Fills:** `capabilities[]` (`area`, `customization_scope_area`) and `capabilities[].categories[].features[]` (`name`, `status`, `tier_first_available`, `customization_scope`, `specificity`). Sizes checked by `lint_spec.py` (SPEC023).
