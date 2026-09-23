# Identity and tile

**What this is.** The keys that name the pack and draw its tile and hero: `slug`, `name`, `headline`, `category`/`categoryChip`, `facet`, `oneLiner`, `tags`, `tile.outcomes`, `hero.image`, optional hero lines.

**The checks**

1. `slug` is lowercase-hyphenated and stable forever — it is the route, the switch-block key, the image paths and the demo path. `headline` is two to four words, split `{accent, rest}` so `accent` takes the accent colour.
2. `tags` is **exactly two, in order**: `categoryChip` (which equals `tags[0]`), then the platform facet's canonical vendor label, spelled the vendor's way and never abbreviated. A third entry is a build failure — a solver or retrieval engine belongs on the Technology tab. No availability string here: availability is a badge, and a capability, not a lifecycle state.
3. `oneLiner` is one string on both the tile and the hero — what it does, for whom, with what outcome — and would still be true if the pack were sold a different way. No `shortLine`: the site retired it in round 9 and its checker fails it. `tile.outcomes` is exactly three.
4. Hero slots render in a fixed order, an unset one not at all: breadcrumb → `heroLine`/`heroCaption` → `headline` → chips and badges → `oneLiner` → `statusNote` → `subLine` → `badges` → CTA. **The CTA row is always last.** `heroLine` and `heroCaption` are never both set; `statusNote` only where the pack has no package yet.
5. `hero.image` carries `file`, `alt` and `focal`, all non-empty. Imagery comes from the company's own corpus, never the web; the tile and the hero share one image.

Claims, prices and names: `claim-rules`. Wording: `copy-rules`.

**Fills / reads:** `meta.slug`, `meta.name_variants.site`, `one_liner.full`/`.short`, `meta.roadmap_block` + the workflow pattern → `category`, `oracle_products[]` with `role: required` → `facet`, `kpis[]` + `problem_solution.solution` → `tile.outcomes`.
