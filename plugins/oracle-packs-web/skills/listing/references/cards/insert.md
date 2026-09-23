# Inserting the entry

**What this is.** Writing the finished entry into the site, at the paths its manifest names: one `products[]` entry in `paths.content`, one figure in `paths.diagrams`, one switch block in `paths.config` and one kit-links entry in `paths.links` (card: `switches`). Nothing else is touched — `site`, `media`, `disclaimers`, `shared`, `overview`, `productsPage`, `facets`, `services`, `forms` and `salesKit` belong to whoever owns the site.

**The checks**

1. **Read the current files from disk first**, after the `site` card's pull. The owner hand-edits delivered files; never regenerate over his edits. A file the environment cannot reach is **deferred and retried**, never recorded as absent.
2. Insert with the tool, not by hand: `node tools/insert-product.mjs --content <site>/<paths.content> --entry <entry file>`. Then `node --check` every changed `.js`.
3. `SITE_DIAGRAMS["<slug>"]` is **generated, never hand-written**: `shared/tools/py tools/diagram_to_site.py packs/<slug>/architecture.json --slug <slug>` prints the figure from the pack's one architecture model, the same one the deck and the one-pager render (`shared/references/architecture-diagram.md`). Paste it as printed; it names every system the deck and the one-pager do, the destinations on the target's second line. Its stderr notes say what was clipped to fit a box: shorten that node's `detail` in the model and regenerate, never edit the figure. A `layout: "hub"` picture is still hand-written, to the same rules.
4. The **kit-links entry** is the tool's too: `node tools/insert-product.mjs … --links <site>/<paths.links> [--demo-path demo/<slug>/index.html]` writes six keys, all `""` except `interactiveDemo` when a walkthrough ships under `paths.demos`. Then run `paths.syncLinks` from the site root. The document links are the owner's to paste later; nothing about the kit goes into `content.js`.
5. Anything in `content.js` is one view-source away from a customer: no seller notes, no internal file names or paths.

**Fills / reads:** the whole entry; `SITE_DIAGRAMS[slug]` from `architecture.json`; the kit-links entry, empty but for the walkthrough's path.
