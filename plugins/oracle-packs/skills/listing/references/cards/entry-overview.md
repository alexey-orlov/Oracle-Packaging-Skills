# The overview tab

**What this is.** The first tab, one column: `problemSolution` → `metrics`, the KPI band (card `entry-metrics`) → `steps`, How it works. `features`, `scope`, `industriesNote`, `industryCases` and `caseStudy` (card `entry-case-study`) sit beside them; the last three render on Use cases.

**The checks**

1. **Two plates.** `problemSolution.problem` and `.solution` are each `{headline, text}`: the headline is the claim, ≤ 60 characters (the role and what the situation costs them; what changes in their work, and how much faster); the text one paragraph, ≤ 30 words. No word from the site's `IMPLEMENTATION_TERMS` (down to *database*, *API*, *SQL*); never the `oneLiner` again. `title` and `icon` are retired.
2. **3–5 `steps`**, `n` from 1: the spec's workflow grouped at the buyer's checkpoints. `title` ≤ 26 characters, one line; `text` ≤ 30 words.
3. **Each `shot` is measured, never typed**: `{full, zoom, region, anchor, alt}`, printed by `tools/overview-data.py --shots` from the capture's `shots.json`, its files in the site's `assets/img/steps/`. The frames are whole screens on synthetic data, from the product's walkthrough or the site's step mocks (its `docs.assets` §1). No shot, no finished entry. `image` is retired.
4. 6–8 `features` ≤ 12 words; `scope.in` and `.out` ≥ 4 items ≤ 14 words; each step keeps its `features`. None renders today; the checker holds their shape.
5. 3–6 `industryCases`: `industry` one of the sixteen, unique; `label` the site's; `image` the shared `assets/img/industries/<industry>.jpg`; `problem` and `solution` 2–3 sentences that could not move under another tab. `industriesNote` carries the buyer.
6. Build failures: `metricsNote`, `roi`, `moreDetail`, `featuresDetail`, `featuresNote`, `sideFacts`, `industries`, `successStory`.

**The sixteen industries:** manufacturing · logistics · utilities · telecom · healthcare · financial-services · insurance · retail · energy · public-sector · automotive · life-sciences · professional-services · construction · travel-transport · cross-industry.

**Fills / reads:** `problem_solution`, `workflow.steps[]`, `capabilities[]`, `verticals[]`, `icp.line`, `packages.tiers[pov]`.
