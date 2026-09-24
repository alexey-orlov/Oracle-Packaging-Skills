# The altitude to write at

**What this is.** `assets/exemplar-product-entry.js` is the live site's `exemplarProduct` entry — **the spec, not a template**. Generated, never edited by hand: `node tools/refresh-exemplar.mjs --site <site>` rewrites it whenever `--check` reports drift (card `site`). Where a key carries an example, that cell's altitude, length and phrasing is the specification; the source documents are evidence, the exemplar is the register.

**How to read it.** Never open the whole file into the conversation. A fresh-context agent reads it and returns the strings, or you read **only the two or three keys you are filling**. Distilling to the register is the job; a dump of everything the research found fails it.

**The checks**

1. `oneLiner` reads as a product statement — what it does, for whom, with what outcome — and would still be true if the pack were sold a different way. If not, it is packaging copy.
2. `metrics[].qualifier` is ≤ 14 words and carries the baseline. A figure without its baseline is not a result.
3. `industryCases[].problem`/`.solution` are 2–3 sentences that could not move under another tab unchanged. Generic vertical paragraphs are the standard failure.
4. `steps[].features` are the exact strings from `overview.features`, partitioned: union equal, no bullet twice, none missing.
5. `caseStudy.story` closes on the caveat that qualifies the figures, in the same plain word as the status chip, never its negation.
6. `jumpstart.outcomes` name what the customer *has* afterwards, not what we hand over.

**Not in the exemplar, by design:** images, customer names and logos, account-specific URLs, and the per-capability S/M/L matrix, which belongs in the pack documents.

**A stalled agent is not progress.** Have the drafting agent write intermediate output early; when its stage should be done, check that file; on no movement, stop it and take over from what it wrote.
