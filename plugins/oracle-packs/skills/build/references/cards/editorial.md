# The editorial pass

**What this is.** The last read before the owner sees a deck, one-pager or executive summary: one fresh-context subagent on the strongest model reads every line of the built file against the spec and returns pass or fail per check, with a reason. The artifact's own card adds its checks. It has caught a price slip or an overclaim on every deck so far; never skip it.

**Checks**

1. Prices, durations and figures equal the spec, tier for tier; a `tbd` price reads "To be defined", never a guess.
2. "Proof of value" and "proven" are used as the brief uses them, the status word once: a proof of value is not a proven result. Figures are business metrics the buyer already tracks, each with its caveat, never acceptance criteria.
3. Tier names are the spec's; the pack name is this audience's variant; vendor and product names are the catalog's full names; every integration claim states its tier.
4. The customer's name or logo appears only where the brief clears it for this audience, else the anonymized descriptor. No internal operating numbers on any cut: headcount, contract values, internal costs.
5. Third person; "customers", never "users"; no internal framings ("we packaged this", "the practice"), no packaging vocabulary; no em-dashes or arrows in prose (a diagram's own arrows stay).
6. Nothing is invented to fill a block: an empty panel with one grey line is the correct absence.

**Bad.** "We leveraged the customer's data — enabling users to action insights in real time."
**Good.** "Planners review the proposed allocation instead of building it. Figures are from the eight-week proof of value and are not contractual."

**Reads:** `meta.name_variants`, `clearance.*`, `packages.tiers[]`, `oracle_products[]`, `kpis[]`.
