# Switches and kit links

**What this is.** `SITE_CONFIG.products["<slug>"]` at `paths.config`: which optional surfaces a product renders. An **empty string renders no control**: absence is an empty container, never a dead button.

**The keys**, as of site round 12; the site's `docs.config` §3 wins.

| Key | Contract |
|---|---|
| `marketplace` | real boolean; drives the availability badge |
| `marketplaceUrl` | the listing URL; a build failure while `marketplace` is `false` |
| `video` | real boolean: a recording exists or is coming; shows the hero's video frame |
| `videoPoster` | that frame's still; a key even when empty |
| `successStoryUrl` | gates the case-study download link |

**The kit links**, at `paths.links`: six keys per product, in order `onePager`, `salesDeck`, `featureList`, `interactiveDemo`, `interactiveDemoArtifact`, `video`, each `""` until its artifact exists. `interactiveDemo`: the walkthrough's path, `demo/<slug>/index.html`, or an https URL; `interactiveDemoArtifact`: the same walkthrough as its own artifact, while the site runs as one. The last three drive the site's buttons: after changing one, run `paths.syncLinks` from the site root, and the publish includes `data/links.js`. `links.json` and `mail/` never ship.

Retired, and failed by the site's checker: `config.js` `demoUrl`, `demoPreviewUrl`, `videoUrl`, `materials`; `content.js` `sellers`, `shared.materialStates`.

**The checks**

1. Every key above is present; both booleans are real, never a quoted `"false"`.
2. Every `products[]` slug has a key here and in `paths.links`; `facet` and `category` are ids the site defines.
3. `productOrder` is **owner-controlled, never derived**: a new slug joins the end; the owner moves it. Equal-size tiles, one CTA each.
4. A demo and a marketplace listing together never crowd the tag row.
5. A missing **image file** warns, never fails: copy and imagery ship on separate tracks.

**Fills / reads:** runner inputs (URLs, posters); the `links.json` entry the inserter writes and the owner fills.
