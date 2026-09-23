# Inserting the entry

**What this is.** Writing the finished entry into the site, at the paths its manifest names: one `products[]` entry in `paths.content`, one figure in `paths.diagrams`, one switch block in `paths.config` (card: `switches`). Nothing else is touched — `site`, `media`, `disclaimers`, `shared`, `overview`, `productsPage`, `facets`, `services`, `forms` and `salesKit` belong to whoever owns the site.

**The checks**

1. **Read the current files from disk first**, after the `site` card's pull. The owner hand-edits delivered files; never regenerate over his edits. A file the environment cannot reach is **deferred and retried**, never recorded as absent.
2. Insert with the tool, not by hand: `node tools/insert-product.mjs --content <site>/<paths.content> --entry <entry file>`. Then `node --check` every changed `.js`.
3. `SITE_DIAGRAMS["<slug>"]` is **generated, never hand-written**: `python3 tools/diagram_to_site.py packs/<slug>/architecture.json --slug <slug>` prints the figure from the pack's one architecture model, the same one the deck and the one-pager render (`shared/references/architecture-diagram.md`). Paste it as printed; it names every system the deck and the one-pager do, the destinations on the target's second line. Its stderr notes say what was clipped to fit a box: shorten that node's `detail` in the model and regenerate, never edit the figure. A `layout: "hub"` picture is still hand-written, to the same rules.
4. `sellers.materials[]` is a **manifest, never rendered to a reader**: `{key, title, description, state}`, one row per asset, `key` matching the switch block's `materials` map. Materials are requested, not listed — the tab names no asset, gates on the corporate email domain rather than a role, promises the outcome, routes the ineligible somewhere real.
5. Anything in `content.js` is one view-source away from a customer: no seller notes, no internal file names or paths.

**Fills / reads:** the whole entry; `SITE_DIAGRAMS[slug]` from `architecture.json`; `sellers.materials[]` from the artifact set.
