# Preview and QA

**What this is.** Looking at every changed screen before anyone else does. The screenshots go into the review pack.

**Run it** with `preview_start {name: <preview.launchConfig>}`. Where the session's folder has no such entry, serve `<site>/site` as the site's `docs.runbook` says and open it with `preview_start {url}`. Browse the manifest's `preview.origin`, **not `localhost`**, whose cache goes stale and quietly serves the previous build. A QA subagent can kill a shared server, so restart it before blaming the page.

**The checks**

1. **Every changed screen at the manifest's `preview.widths`, and the H1 at `preview.h1Width`**, with **no horizontal overflow at any width**. For a new product, check every tab its page renders (the site's START-HERE §3 names them), plus the catalog tile and the facet rail with this product's platform selected.
2. **Headings are counted on the rendered page**, not in the file; no lone short word on a line at the narrowest width.
3. **Fresh assets before measuring anything.** The preview caches hard: confirm the new rule is in `document.styleSheets`, or re-point the stylesheet with a `?v=` query, or `fetch(file, {cache:'reload'})` each changed file, then navigate.
4. **Shoot at scroll 0.** Screenshots taken after scrolling can come back black. Hide the other sections from the console and force the reveal class on the block you are shooting, or make the viewport tall.
5. **The site's design rules for its live theme**, which START-HERE §4 holds and the site's checker mostly asserts. Line icons, **no emoji**, peers equal height. An address is a link, never a filled button; a filled button is the screen's one ask.
6. A component moved to a new page takes its wrapper, modifier classes, container width and breakpoints with it. Moving a component breaks it quietly.
