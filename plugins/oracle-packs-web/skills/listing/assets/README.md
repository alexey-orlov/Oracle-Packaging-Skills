# `listing/assets/`

| File | What it is |
|---|---|
| `exemplar-product-entry.js` | One complete `products[]` entry from a shipped practice site, plus its `config.js` switch block and its `diagrams.js` figure. **The spec, not a template.** |

## How to use the exemplar

**Match it, do not paraphrase it.** When you fill a structure that already
carries an exemplar, the existing cells are the specification: match their
**altitude, length and phrasing**. The source documents are evidence; the
exemplar is the register. Distilling to that register is the job — a dump of
everything the research found is a failure of the same task.

Read it beside:

- `../references/listing-schema.md` — the key-by-key contract, the invariants, and the map from each key back to the pack-spec component it comes from;
- `../references/listing-rules.md` — the content, messaging and design rules every string obeys.

Then validate with `../tools/check-grammar.js`. The checker is the acceptance
gate, not a formality: it carries 300-plus assertions, most of which are a rule
an owner won in a review round.

**Generate its deny-list first.** The customer-name gate is the one assertion
that fails *open*: with no deny-list configured the checker prints a warning and
still exits 0, which is exactly how a customer name reaches a published page. So
before the gate runs:

```bash
python3 ../tools/denylist-to-json.py --out <site-root>/tools/deny-list.json
node <site-root>/tools/check-grammar.js
```

Run **the site's own** `tools/check-grammar.js`, not this skill's copy under
`tools/`. The site's gate has since grown a brand block the port does not have
(retired teal in the CSS *and* in `assets/img/**`, non-brand heading weights,
retired radius tokens, an over-spent orange accent, the `@font-face` set, the
`content-case.js` load order, and the archived theme's integrity). The port
would pass a listing the site rejects. Until the two are reconciled, the site's
copy is the gate.

The converter reads `shared/tools/denylist.txt` — the one list the practice keeps —
so the names never diverge between the Python linters and this checker. The
generated file is internal: it belongs beside the site, never inside a published
root. `tools/deny-list.example.json` is the empty shape, kept for reference.

## Calibration points worth copying deliberately

- **`oneLiner`** — a product statement: what it does, for whom, with what outcome. Read it and ask whether it would still be true if the pack were sold a different way. If the answer is no, it is packaging copy.
- **`overview.metrics[].qualifier`** — ≤ 14 words, and it carries the baseline the figure is measured against. A figure without its baseline is not a result.
- **`overview.industryCases[].problem/solution`** — 2–3 sentences that could **not** be moved under another industry tab unchanged. Generic vertical paragraphs are the standard failure here.
- **`overview.steps[].features`** — the exact strings from `overview.features`, partitioned across the steps: union equal, no bullet twice, none missing. This invariant is what lets the stepper replace a flat checklist without losing a fact.
- **`caseStudy.story`** — closes on the caveat that qualifies the figures, in the same plain word as the status chip, and never states the negation.
- **`jumpstart.outcomes`** — what the customer *has* afterwards, not what we hand over.
- **`jumpstart.next[].price`** — `Scoped per engagement` unless a signed-off source publishes a figure. Only the proof-of-value price ships.

## What is deliberately not here

- **Images.** A new pack brings its own, from the company's own corpus — never the web. The checker treats a missing image file as a warning, not a failure, precisely so copy and imagery ship on separate tracks.
- **Customer names, logos, geography or identifiers.** Anywhere, in any file.
- **URLs that belong to one account** — the exemplar's `demoPreviewUrl` is blanked. Preview and marketplace URLs are runner inputs.
- **The per-capability S/M/L handling matrix.** It belongs in the pack documents, never on the listing.
