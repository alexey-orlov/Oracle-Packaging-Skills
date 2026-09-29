# The case-study callout

**What this is.** `overview.caseStudy`, the anonymized telling of the delivered engagement on the Use cases tab, or `null`. The key is always present; `null` renders nothing, and there is no empty state. A case study also takes its home card (card `entry-case-card`).

**The checks**

1. No customer name or logo. `descriptor` is industry and scale only, nothing that narrows to one company; `area` is the operational area; `industry` is one of the sixteen and picks the medallion. It ships only where the spec's clearance permits an anonymized telling on the customer site, re-checked every round.
2. `status` is `measured` · `modeled` · `in-preparation`, the key of the chip (Proven · Forecast · Estimated), and the only place the status is set.
3. `metrics` is 1–2 `{value, label}`, `value` ≤ 20 characters. With nothing published, a short qualitative outcome: never an invented number or a restatement of the mechanic. The KPI band may carry the same figure.
4. `story` is 2–3 sentences, what was done and on what data, **closing on the caveat sentence the site's checker still requires**: it carries *illustrative*, *not contractual* or *modeled simulations*, and agrees with the chip (measured says measured; modeled, forecast from simulations on the customer's own history). Never the chip's word negated.
5. `scope` is exactly three `{label, value}` facts the card does not already carry: no contract value or duration, headcount or money figure.
6. `ndaLine` closes it; a case in preparation offers no reference call. `downloadLabel` is always set, though its link renders only with a success-story URL. `customer`, `logo`, `logoStacked`, `image` and `metricsEyebrow` fail the build.

**Fills / reads:** `meta.source_engagement`, `clearance.anonymized_descriptor`, `clearance.customer_name_allowed.customer_site`, `kpis[]` and `kpis[].figure_status`.
