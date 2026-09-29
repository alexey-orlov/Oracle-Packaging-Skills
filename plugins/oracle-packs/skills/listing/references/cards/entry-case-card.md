# The home case card

**What this is.** The home page shows one card per product with a case study (the site's `overview.caseStudies[]`), and its checker fails a product without one. The inserter builds it: `--case-card <file>` gives only its two lines, `{ line, metric: { label } }`, and the descriptor, area, industry, status, figure and product come from the entry, so the card and the product page cannot disagree.

**The checks**

1. `line` is one sentence, about 25 words at most, in business terms: the customer's old way and what changes. An Estimated card whose engagement has no result yet states the problem as it stands, in the present tense, claiming nothing done.
2. `metric.label` is the small line under the figure: what it measures and against what, in the buyer's words.
3. **No implementation and no hedge in either**: no word from the site's `IMPLEMENTATION_TERMS` and none of its `CASE_HEDGES` (*illustrative*, *not contractual*, *proof of value*, *first engagement*, *will run*, *success metrics*, *signed before*, *scored against*). The chip is the status. The product page's story keeps its caveat sentence; the card never carries it.
4. A Forecast card (`modeled`) says in `metric.label` that the figure was simulated on the customer's own history.
5. Its figure, the case study's first `metrics[].value`, never opens on the same word as another card's: peers each make their own claim.

**Good.** *Rates were keyed in page by page, and a wrong one surfaced only at invoice matching; now reviewers catch it before it reaches the system.* **Bad.** *A proof of value on the vision engine, illustrative, not contractual.*

**Fills / reads:** the entry's `overview.caseStudy`; the site's `overview.caseStudies[]`.
