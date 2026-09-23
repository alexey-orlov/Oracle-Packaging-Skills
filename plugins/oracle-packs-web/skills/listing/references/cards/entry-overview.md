# The overview tab

**What this is.** The first tab, in fixed order: `problemSolution` → `features` as `steps`, a frame each → `industryCases` as tabs → `metrics` in a side rail; plus `metricsNote`, `roi`, `featuresDetail`, `industriesNote`, `scope`, `moreDetail`, `caseStudy` (card: `entry-case-study`).

**The checks**

1. **Every product fills every slot**; none is optional. A slot with no fact behind it is filled *qualitatively* — a `null` metric tile, a `cross-industry` chip, `Scoped per engagement` — never omitted, never as an apology.
2. 1–4 `metrics`, **business metrics only** (`kpis[].kind != technical`): what the business improves, never a proof criterion (reviewer agreement, coverage) — those stay on the Jumpstart tab's scope. `value` ≤ 20 chars or `null`; `qualifier` ≤ 14 words, carrying the baseline. `metricsNote` is mandatory. One `value` or more heads the row "metrics improved"; all-qualitative, "what the proof of value measures". A note opening on an absence is a build failure.
3. 6–8 `features` ≤ 12 words each; `featuresDetail` ≥ 6; `featuresNote` carries partial coverage. 3–5 `steps`, `text` ≤ 30 words, `steps[].features` partitioning `overview.features` exactly — union equal, no bullet twice, none missing. `image` is a demo frame; with no demo the key stays empty.
4. 3–6 `industryCases`; `industry` one of the sixteen keys, unique; `label` the site's. `problem` and `solution` are 2–3 sentences that could **not** move under another tab unchanged.
5. `scope.in`/`.out` ≥ 4 items each, ≤ 14 words; `moreDetail` ≥ 3, one per vertical. `sideFacts`, `industries`, `successStory`, top-level `pov`: build failures.
6. Who buys it has no field today: it rides in `industriesNote`, and the missing home is raised with the owner.

**The sixteen industries:** manufacturing · logistics · utilities · telecom · healthcare · financial-services · insurance · retail · energy · public-sector · automotive · life-sciences · professional-services · construction · travel-transport · cross-industry. No seventeenth; `cross-industry` ships an `industriesNote` saying why.

**Fills / reads:** `problem_solution`, `kpis[]`, `figures`, `capabilities[]`, `workflow.steps[]`, `verticals[]`, `icp.line`, `packages.tiers[pov]`.
