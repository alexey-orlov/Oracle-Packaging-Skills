# Identity and tile

**What this is.** The keys that name the pack and draw its tile and hero, from `slug` to `contactPerson`.

**The checks**

1. `slug` is lowercase-hyphenated and stable forever: the route, the switch-block key, the file paths. `headline` is two to four words, split `{accent, rest}`.
2. **`facet` is where the product's own engine runs**, a `facets.technology` id: one platform as a string; two or more as an array, in the site's order, only where the engine is part of each (a database layer that also runs inside AI Data Platform). A platform it merely sits beside stays on the Technology tab. Each one after the first is named in full in `technology.narrative` and opens the name of an item in the `data-platform` layer. Never `oracle-ai-fusion`.
3. `tags` is `categoryChip`, then each platform's short label, in `facet`'s order; one more fails the build. No availability string.
4. `oneLiner` is one string on the tile and the hero — the business value, for whom, never the implementation — true however the pack is sold. No `shortLine`. `tile.outcomes` is exactly three.
5. `heroLine` or `heroCaption`, never both, held to the one-liner's rule; `statusNote` only where no package exists yet. `hero.image` carries `file`, `alt` and `focal`, from the company's corpus, one image for tile and hero.
6. `contactPerson` is an id from the site's `shared.people`, the product's lead: **an owner choice, never derived**, asked in one widget. Inserter and checker refuse a missing or unknown id.

Claims, prices and names: `claim-rules`. Wording: `copy-rules`.

**Fills / reads:** `meta.slug`, `meta.name_variants.site`, `one_liner.full`, `meta.roadmap_block` + the workflow pattern → `category`; `oracle_products[]`, the platforms the engine runs on → `facet` (`oracle-autonomous-ai-lakehouse` → `oracle-ai-lakehouse`, `oracle-ai-data-platform` as is, `oci` under an NVIDIA engine → `oci-nvidia`); `kpis[]` + `problem_solution.solution` → `tile.outcomes`; the site's `shared.people` → `contactPerson`.
