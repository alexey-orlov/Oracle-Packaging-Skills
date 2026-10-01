# Inserting the entry

**What this is.** Writing the finished entry at the paths the site's manifest names: the `products[]` entry and its `media[slug]` in `paths.content`, the figure in `paths.diagrams`, the switch block in `paths.config`, the kit links in `paths.links`, a case study's home card, and the checker's catalog pins. Nothing else.

**The checks**

1. **Read the current files from disk first**, after the `site` card's pull: the owner hand-edits them; never regenerate over them. A file out of reach is retried, never recorded as absent.
2. Insert with the tool: `node tools/insert-product.mjs --content <site>/<paths.content> --entry <entry file> --figure-alt "<the figure in one sentence>"`, with `--case-card <file>` for a product with a case study (card `entry-case-card`). Then `node --check` every changed `.js`.
3. `SITE_DIAGRAMS["<slug>"]` is **generated, never hand-written**: `shared/tools/py tools/diagram_to_site.py <spec> --slug <slug>` prints it from the pack's architecture model. Paste it as printed; a clipped box is fixed in the spec's `detail`, then regenerated.
4. **The switch block** holds exactly the keys `docs.config` lists (never the retired `video`), real booleans. **No placeholder link:** `marketplace` is `true` only with its listing's https `marketplaceUrl`, else `false` and the URL empty. `productOrder` is the owner's.
5. **The kit links live only in `links.json`**, keyed by the slug: `node tools/insert-product.mjs … --links <site>/<paths.links> [--demo-path demo/<slug>/index.html]` writes it, empty but for the walkthrough's path; `paths.syncLinks` validates it. No link lives in any other file.
6. `content.js` is one view-source away from a customer: no seller notes, no internal names or paths.
7. **The checker may pin the catalog**: a product count, the walkthrough and unpackaged lists. A new product moves each pin it meets, in the same pass and in the site's round record.

**Fills / reads:** the whole entry; `SITE_DIAGRAMS[slug]` from `architecture`, through the model; the switch block; the kit links.
