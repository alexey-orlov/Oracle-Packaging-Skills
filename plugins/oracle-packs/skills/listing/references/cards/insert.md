# Inserting the entry

**What this is.** Writing the finished entry into the site at the paths its manifest names: one `products[]` entry in `paths.content` with its figure's `media[slug]` entry, one figure in `paths.diagrams`, one switch block in `paths.config`, one kit-links entry in `paths.links`. Nothing else is touched: the rest belongs to whoever owns the site.

**The checks**

1. **Read the current files from disk first**, after the `site` card's pull; the owner hand-edits delivered files, so never regenerate over them. A file the environment cannot reach is deferred and retried, never recorded as absent.
2. Insert with the tool, not by hand: `node tools/insert-product.mjs --content <site>/<paths.content> --entry <entry file> --figure-alt "<the figure in one sentence, written with the copy>"`. Then `node --check` every changed `.js`.
3. `SITE_DIAGRAMS["<slug>"]` is **generated, never hand-written**: `shared/tools/py tools/diagram_to_site.py <spec> --slug <slug>` prints the figure from the pack's one architecture model. Paste it as printed; its stderr notes say what was clipped to fit a box: shorten that node's `detail` in the brief and regenerate, never edit the figure.
4. **The switch block** carries the keys the site's `docs.config` lists, booleans real, never a quoted `"false"`. `productOrder` is the owner's: a new slug joins the end.
5. **The kit links live only in `links.json`**, keyed by the slug: `node tools/insert-product.mjs … --links <site>/<paths.links> [--demo-path demo/<slug>/index.html]` writes the entry, empty but for the walkthrough's path; then `paths.syncLinks` from the site root validates it. No link is repeated in any other file.
6. Anything in `content.js` is one view-source away from a customer: no seller notes, no internal file names or paths.

**Fills / reads:** the whole entry; `SITE_DIAGRAMS[slug]` from the brief's `architecture`, through the model; the switch block; the kit-links entry.
