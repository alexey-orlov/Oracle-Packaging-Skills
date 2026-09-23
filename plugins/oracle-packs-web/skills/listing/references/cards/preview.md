# Preview and QA

**What this is.** Looking at every changed screen before anyone else does. The screenshots go into the review pack.

**Run it locally**

```sh
cd "<site root>/site" && python3 -m http.server 8765 --bind 127.0.0.1
```

Browse **`http://127.0.0.1:8765`** — **not `localhost`**, whose cache goes stale and quietly serves the previous build. Point an editor's preview launcher at the same origin rather than starting a second server; a QA subagent can kill a shared server, so restart it before blaming the page.

**The checks**

1. **Every changed screen at 1440 · 1280 · 1024 · 768 · 375, and the H1 at 320**, with **no horizontal overflow at any width**. For a new product that is Overview · Technology · Jumpstart · Contacts · For sellers, plus the catalog tile and the facet rail with this product's platform selected.
2. **Headings are counted on the rendered page**, not in the file; no lone short word on a line at 375.
3. **Fresh assets before measuring anything.** The preview caches hard: confirm the new rule is in `document.styleSheets`, or re-point the stylesheet with a `?v=` query, or `fetch(file, {cache:'reload'})` each changed file, then navigate.
4. **Shoot at scroll 0.** Screenshots taken after scrolling can come back black — hide the other sections from the console and force the reveal class on the block you are shooting, or make the viewport tall.
5. One ground and one accent per screen, display type for headlines, **at most one light band per page**, peers equal height, line icons, **no emoji**. An address is a link, never a filled button; a filled button is the screen's one ask.
6. A component moved to a new page takes its wrapper, modifier classes, container width and breakpoints with it. Moving a component breaks it quietly.
