# The switch block

**What this is.** `SITE_CONFIG.products["<slug>"]` in `site/data/config.js` — the per-product controls that decide which optional surfaces render. Every key must exist; an **empty string means the control does not render**, which is how absence stays an empty container rather than a dead button.

**The keys**

| Key | Contract |
|---|---|
| `marketplace` | real boolean; drives the availability badge |
| `marketplaceUrl` | the listing URL; a URL set while `marketplace` is `false` is a build failure |
| `demoUrl` | the canonical relative path to the walkthrough (`demo/<slug>/index.html`), kept canonical for the real deployment even while previewing |
| `demoPreviewUrl` | where the demo actually opens while previewing — a **runner input, never a repo constant** |
| `video` / `videoUrl` / `videoPoster` | the demo-video switches; `videoPoster` exists as a key even when empty |
| `successStoryUrl` | gates the case-study download link |
| `materials` | `{ <key>: <url> }`, one per `sellers.materials[].key` |

**The checks**

1. Every key above is present; the demo and video switches stay empty strings until those assets exist.
2. Every slug in `products[]` has a matching key here, and `facet` and `category` are ids the site already defines.
3. `productOrder` is site-level and **owner-controlled data, never derived**: a new slug joins the end and the owner moves it. Equal-size tiles, one CTA per tile.
4. Availability is a **capability, not a lifecycle state** — a demo exists, a marketplace listing exists. A product carrying both must not crowd the tag row.
5. A missing **image file** is a warning, not a failure: copy and imagery ship on separate tracks.

**Fills / reads:** runner inputs (URLs, posters, kit links); `sellers.materials[].key`.
