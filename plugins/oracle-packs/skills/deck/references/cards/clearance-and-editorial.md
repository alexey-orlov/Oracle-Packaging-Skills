# Clearance, consistency and the editorial pass

**What this is.** Two passes before the owner sees anything: the automatic clearance and consistency checks, then a reading of every slide's text on the strongest model.

    python3 shared/tools/lint_artifact.py <pptx> --channel <channel> --spec <spec>
    python3 shared/tools/check_consistency.py <spec> <pptx>

Both clean before the first render is shown.

**Checks the editorial pass must pass**

1. Prices on the slides match the spec, tier for tier.
2. "Proof of value" and "proven" are used as the pack brief uses them — a proof of value is not a proven result.
3. Tier names are the spec's, and the pack name is the variant for this audience.
4. Every integration claim states the tier it holds at.
5. Vendor and product names are the catalog's full names, never a short spelling the catalog marks as wrong.
6. The customer's name or logo appears only where `clearance.customer_name_allowed[<channel>]` is true; otherwise the anonymized descriptor stands in its place.
7. Nothing internal reaches a slide — no headcount, no internal operating numbers — whichever audience the deck is for.

This pass has caught a price slip and an overclaim on every previous deck. Do not skip it.

The full naming, trade-mark and clearance rules, including how each audience's name variant is derived, are `shared/references/naming-and-clearance.md` — read the part a finding actually turns on.

**Reads:** `meta.name_variants`, `clearance.*`, `packages.tiers[]`, `oracle_products[]`, `kpis[]`.
