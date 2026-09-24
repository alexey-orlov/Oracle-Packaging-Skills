# Identity and tile

**What this is.** The keys that name the pack and draw its tile and hero: `slug`, `name`, `headline`, `category`/`categoryChip`, `facet`, `oneLiner`, `tags`, `tile.outcomes`, `hero.image`, optional hero lines, and `contactPerson`.

**The checks**

1. `slug` is lowercase-hyphenated and stable forever: the route, the switch-block key, the image and demo paths. `headline` is two to four words, split `{accent, rest}`; `accent` takes the accent colour.
2. `tags` is **exactly two, in order**: `categoryChip` (equal to `tags[0]`), then the platform facet's vendor label, spelled the vendor's way, never abbreviated. A third entry fails the build (engines belong on the Technology tab). No availability string: availability is a badge, a capability, not a lifecycle state.
3. `oneLiner` is one string on the tile and the hero — what it does, for whom, with what outcome — true however the pack is sold. No `shortLine` (retired in site round 9; the checker fails it). `tile.outcomes` is exactly three.
4. Hero slots render in fixed order, unset ones not at all: breadcrumb → `heroLine`/`heroCaption` → `headline` → chips and badges → `oneLiner` → `statusNote` → `subLine` → `badges` → CTA. `heroLine` and `heroCaption` never both; `statusNote` only where no package exists yet.
5. `hero.image` carries `file`, `alt` and `focal`, all non-empty; imagery from the company's corpus, never the web; one image for tile and hero.
6. `contactPerson` is an id from the site's `shared.people`: the lead on the product's Contacts card (site round 13). **An owner choice, never derived**: one widget of the people the site names. Inserter and checker refuse a missing or unknown id.

Claims, prices and names: `claim-rules`. Wording: `copy-rules`.

**Fills / reads:** `meta.slug`, `meta.name_variants.site`, `one_liner.full`, `meta.roadmap_block` + the workflow pattern → `category`, `oracle_products[]` with `role: required` → `facet`, `kpis[]` + `problem_solution.solution` → `tile.outcomes`; the site's `shared.people` → `contactPerson`.
