# The mini-site listing — a `products[]` entry

The listing is a data object, checked by the site's own checker, and the only artifact end customers read directly.

**Keys, in file order**

```
slug · name · headline{accent,rest} · category · categoryChip · facet|facet[] · oneLiner · heroCaption · contactPerson
tags[] · hero{image{file,alt,focal}} · tile{outcomes[3]}
overview{ problemSolution{problem,solution: {headline,text}} · metrics[] · features[] · industriesNote
          steps[]{n,title,text,shot{full,zoom,region,anchor,alt},features} · industryCases[] · scope{in,out} · caseStudy|null }
technology{ narrative · stack[]{items[]{name,required,direction,note}} · capabilities[]{stage,items[]} }
jumpstart{ title, promise, durationShort, pillars[3], outcomes[], timeline[], needs[], investment, next[], cta }
```

`diagrams.js` separately carries the architecture flow — `{layout, sources[], group, target, loop}`, titles and subtitles as pre-broken line arrays. The kit's six links live in the site's private `links.json`, never in `content.js`.

**The components, in the form they take here.** Name → `name` + `slug` + the two-part `headline`. One-liner → `oneLiner` + `heroCaption`. ICP → `overview.industriesNote`, canonical. Verticals → `overview.industryCases[]`, the estate's only per-vertical problem ↔ solution pair. Capabilities → `technology.capabilities[]`, the stage view **derived** from the feature list. Workflow → `overview.steps[]`, canonical, one measured frame per step. Architecture → `technology.narrative` + `stack[]` + the `diagrams.js` entry. Oracle products → `stack[].items[].required`, the only explicit flag in the estate. KPIs → `overview.metrics[]`, the KPI band printed from the spec's framed metrics, + `tile.outcomes[3]`. Packages → the Jumpstart narrative with the **PoV price only**; Integration and Scaling read "Scoped per engagement". The lead → `contactPerson`, an id in the site's `shared.people`, the owner's choice.

**Standing rules.** A number never renders unframed: a KPI tile under its kind chip, a price beside its footnote. An absent optional key means the block does not render — absence renders as an empty instance or nothing, never as a "missing" sentence. No customer names or logos anywhere under the deployable root.
