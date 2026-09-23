# Footnotes

**What this is.** The `*` / `**` / `***` lines under the legend. A footnote exists only for a **tier caveat that changes what the buyer gets** — typically an integration claim stating its tier.

**The shape.** Fifteen words or fewer, at most three in the whole document. It carries the caveat alone — never the feature name, the category, or a description repeated back, since the marker already points at the row. Anything else belongs in that area's customization-scope cell, or nowhere.

**Cut them before building.** The build warns on stderr, without failing, when there are more than three notes or one runs long, naming them. Take those to the owner in plain words — "three of these read as descriptions rather than caveats; I'd drop them and keep the two about tiers" — fix them in the spec, then build.

**Checks**

1. At most three footnotes in the document.
2. Each is 15 words or fewer.
3. Each carries a caveat that changes what the buyer gets — not a description, not a restatement of the feature.
4. No footnote repeats the feature name or its category.
5. Every cut was agreed with the owner, in plain words, before the document went out.

**Good.** `**  file export / import at PoV; API write-back is Integration-tier scope`
**Bad.** `**  Dispatcher UI (map and table views) — the interface dispatchers use to see and assign work.`

**Reads / writes:** `capabilities[].categories[].features[].note`, changed through `/oracle-packs:spec`.
