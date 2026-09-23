# Inserting the entry

**What this is.** Writing the finished entry into the site: one `products[]` entry in `site/data/content.js`, one figure in `diagrams.js`, one switch block in `config.js` (card: `switches`). Nothing else is touched — `site`, `media`, `disclaimers`, `shared`, `overview`, `productsPage`, `facets`, `services`, `forms` and `salesKit` belong to whoever owns the site.

**The checks**

1. **Read the current files from disk first.** The owner hand-edits delivered files; never regenerate over his edits. On a machine other than the one that last worked on the site, `git pull` first and commit explicitly. A file the environment cannot reach is **deferred and retried**, never recorded as absent.
2. Insert with the tool, not by hand: `node tools/insert-product.mjs --content <site>/site/data/content.js --entry <entry file>`. Then `node --check` every changed `.js`.
3. `SITE_DIAGRAMS["<slug>"]` is the architecture figure, following the naming and flow rules of `shared/references/architecture-diagram.md` and reusing the reviewed diagram rather than drawing a new one: `layout: "flow"` (`sources[]` → a `group` holding `nodes[]` → a `target`, plus `note` or `loop`) or `layout: "hub"` (a `hub` with `items[]`, fed by `sources[]`). Titles and subs are **arrays of lines** — the renderer sets each entry as its own line. The `target` is always the human gate; `note` or `loop` states the one invariant that keeps the workflow honest.
4. `sellers.materials[]` is a **manifest, never rendered to a reader**: `{key, title, description, state}`, one row per asset, `key` matching the switch block's `materials` map. Materials are requested, not listed — the tab names no asset, gates on the corporate email domain rather than a role, promises the outcome, routes the ineligible somewhere real.
5. Anything in `content.js` is one view-source away from a customer: no seller notes, no internal file names or paths.

**Fills / reads:** the whole entry; `SITE_DIAGRAMS[slug]` from `architecture`; `sellers.materials[]` from the artifact set.
