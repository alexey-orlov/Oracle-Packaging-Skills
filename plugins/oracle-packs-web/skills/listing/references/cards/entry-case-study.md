# The case-study callout

**What this is.** `overview.caseStudy` — the anonymized telling of the delivered engagement, or `null`. The key is always present; `null` renders nothing, and there is no empty state.

**The checks**

1. No customer is named and no logo is rendered. `descriptor` is industry and scale only: no name, no country, nothing that narrows to one company. An industry medallion stands where a logo would. The card renders only where the spec's clearance permits an anonymized telling for the customer site; otherwise `null`. **Clearance is revocable** — re-check it every round rather than trusting a prior pass.
2. `status` is `measured` | `modeled` | `in-preparation`, and this is **the only place the status word is set**; it is said once, in the chip.
3. `metrics` is 1–2 figures, `value` ≤ 20 chars. Where nothing is published, a short qualitative outcome instead — never an invented number, never a restatement of the mechanic, and never a repeat of a side-rail tile.
4. `story` is 2–3 sentences — what was done, on what data, with which stack — **closing on the caveat that qualifies the figures**, in the chip's own plain word and never its negation. A story with no caveat clause fails the checker.
5. `scope` is **exactly three** `{label, value}` facts the rest of the card does not carry, and carries no contract value, no contract duration, no headcount and no money figure.
6. `customer`, `logo`, `logoStacked`, `image` and `metricsEyebrow` are removed and are build failures if they return. `downloadLabel` renders only where the success-story switch is non-empty.
7. `ndaLine` closes it. A case in preparation does not offer a reference call about results that do not exist yet.

**Fills / reads:** `meta.source_engagement`, `clearance.anonymized_descriptor`, `clearance.customer_name_allowed.customer_site`, `kpis[]` and `kpis[].figure_status`.
