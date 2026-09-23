# The mini-site listing — a `products[]` entry

The listing is a data object, checked by the site's own checker, and the only artifact end customers read directly.

**Keys, in file order**

```
slug · name · headline{accent,rest} · category · categoryChip · facet · oneLiner · heroCaption
tags[] · hero{image{file,alt,focal}} · tile{outcomes[3]}
overview{ problemSolution · metrics[] · metricsNote · roi · features[] · featuresNote · featuresDetail[]
          industriesNote · steps[] · industryCases[] · scope{in,out} · moreDetail[] · caseStudy|null }
technology{ narrative · stack[]{items[]{name,required,direction,note}} · capabilities[]{stage,items[]} }
jumpstart{ title, promise, durationShort, pillars[3], outcomes[], timeline[], needs[], investment, next[], cta }
```

`diagrams.js` separately carries the architecture flow — `{layout, sources[], group, target, loop}`, titles and subtitles as pre-broken line arrays. The kit's six links (one-pager, sales deck, feature list, walkthrough, its standalone artifact, video) live in the site's private `links.json`, never in `content.js`.

**The components, in the form they take here.** Name → `name` + `slug` + the two-part `headline`. One-liner → `oneLiner` + `heroCaption`. ICP → `overview.industriesNote`, canonical. Verticals → `overview.industryCases[]`, the only full problem ↔ solution pair per vertical in the estate. Capabilities → `technology.capabilities[]`, the stage view **derived** from the feature list. Workflow → `overview.steps[]`, canonical, one captured demo frame per step. Architecture → `technology.narrative` + `stack[]` + the `diagrams.js` entry. Oracle products → `stack[].items[].required`, the only explicit flag in the estate. KPIs → `overview.metrics[]` + `metricsNote` + `roi` + `tile.outcomes[3]`, anonymized attribution. Packages → the Jumpstart narrative with the **PoV price only**; Integration and Scaling read "Scoped per engagement".

**Standing rules.** A number never renders without its footnote. An absent optional key means the block does not render — absence renders as an empty instance or nothing, never as a "missing" sentence. No customer names or logos anywhere under the deployable root.
