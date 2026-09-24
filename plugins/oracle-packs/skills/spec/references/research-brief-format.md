# Research brief format

The summary the owner reads **after** the research and **before** they pick a pack story. Written by `/oracle-packs:spec` stage 2 to `<work>/research-brief.md` (the pack's local work folder, `shared/tools/pack_paths.py`; never the repo), cited by `provenance.research_brief`. The method that fills it is `generalization-method.md`, read by the research agents; the epistemic rules are `shared/references/research-standards.md`. Rewrite this file in place when the format changes.

**One decision it serves:** which generalized pack we are building; anything that does not support that choice is cut. It is internal — counts, internal framings and open risks belong here, and the artifact skills strip them later. **Its reader** is the owner, who knows the delivered engagement and nothing about how the research ran: no step or test ids, no file or key names, no packaging vocabulary. Findings are named by what they are — "the research on what the vendors already ship" — never by the prompt behind them.

**Hard budget: a ten-minute read** — about 1,600 words plus tables, ten sections, none longer than a screen. Over budget, cut the least load-bearing section whole rather than shaving all of them.

## The sections, in order

Fixed. A section with nothing in it prints its heading and one "—" line saying what is missing and why: absence is a finding. The brief prints these titles and **no numbers**; anything pointing at one names it by title.

| Section | What it must hold | Budget |
|---|---|---|
| The answer | Lead with it: the generalized job in one sentence, for whom; the recommended story with the one clause that makes it win; the single finding that could sink it. If the honest answer is *this is not a pack*, say so here with the reason and stop after "Still open". | ≤ 120 w |
| The workflow, generalized | Table, ≤ 12 rows: step · actor (system / human / ai) · input → output · human in the loop, and what they decide · failure path in ≤ 12 words, where "not covered" is permitted and required. ≤ 15 words per cell; canonical domain step names, not our screen names. Below it, one line each for inputs and outputs, naming the systems and the tier at which each integration is real. | ~200 w |
| Where the pack differs from what we built | One line first, in the form the spec carries: *the pack generalizes X; the delivered case hard-codes Y.* Then a table by capability area: in the vendor pack · we built · stays custom per engagement. Close with what we built that the pack will not do, and what the project left out but the pack includes. | ≤ 150 w |
| The industries | Table, 3–5 rows: industry · the entities that differ — the evidence it is a different business; one that cannot fill it is the same thing renamed · framing in 15–30 words of business language · what matters here (2–3 step-level differences, ≤ 20 words) · standing: proven, plausible, or not built yet. Under three rows means the pack has not widened past its one customer; say so in the answer. | ~250 w |
| What the other vendors ship | Two tables. Vendors, 3–5 rows: vendor · class (direct · substitute, a team doing it by hand included · same-vendor overlap) · how they group this job · steps they have that we lack · steps we split that they do not. Then gaps: gap · who treats it as a step · recommendation (adopt now · roadmap · reject) · reason. A market gap the delivered case never had is labelled as such; same-vendor overlap gets one line — what the native product already does, and the boundary that keeps our claim honest. | ≤ 250 w |
| What happens when things go wrong | Only what the workflow does **not** handle: the step, what is missing, the consequence in production, and a disposition — in the proof · in Integration · out of scope. This is where the artifacts' out-of-scope block comes from; an empty list is itself a finding and is stated as one. | ≤ 120 w |
| What is specific to the customer | Table per capability **area**: customer-specific · engine-specific · use-case-specific · industry-specific · verdict (reusable · configurable · custom per engagement); cells hold the feature names that fail that axis, or "—". Then three lines: how many capabilities are available, partial and on the roadmap, in words; the areas built fresh for every customer (that is priced scope); and, if nothing is on the roadmap, a flagged warning that the list never left what we built for the customer. | ~150 w |
| The options | The 2–3 complete candidates as one comparison table, and the recommendation with its reason. The rows and the tests each cell must pass are in `cards/story.md`; this section is that table's written backing. | ≤ 120 w each |
| Still open | Each: the question · what it blocks · the cheapest way to close it · who closes it. Everything unverified lands here, not as a hedge inside an earlier section. Nothing downstream prints anything that depends on an open item. | ≤ 120 w |
| Sources | Grouped by tier, newest first: (1) primary — vendor docs, patents, engineering blogs, case studies with specifics, our delivered artifacts; (2) practitioner commentary; (3) real-case reports; (4) reasoning from principles. Each line: title, date, tier, use. Press releases and marketing pages are never tier 1. Then **searched and not found** — what you looked for and where, which tells the owner whether a gap is real or just unsearched — and **unverified**. Over budget, compress here; never fake it. | as needed |

**Header, six lines, no prose:** working title · delivered engagement and date · researched on · status · sources read · still open.

## Labeling

`shared/references/research-standards.md` holds the epistemic and register rules — named specifics, source tiers, explicit gaps, structure over prose. What this brief adds:

- Label every non-trivial claim — `[Fact / source]` · `[Practitioner consensus]` · `[Inference]` · `[Speculation]` — at the end of the cell or line. Inference is never stated as fact.
- **"—" for anything unsupported.** Never "various tools", "industry-standard", "typically". A fully populated grid is template-completion bias, not a win.
- Figures carry their kind and the caveat that will print with them; a second, contradicting metric set is an open item, not a footnote.
- Product and vendor names are re-verified as current, or marked "(unverified)".
- The customer's name may appear here (the brief is internal), but every sentence that will travel into an artifact must survive anonymization.
- Anything the owner has not ruled on says "(awaiting your confirmation)": the brief may hold unconfirmed material; it may not look as though they confirmed it.

## What follows

The owner answers at most four questions under "Your call on what the research found" (`cards/research-review.md`), then picks a story (`cards/story.md`). If they send the research back, this brief is **rewritten in place**, never appended to. Every later part cites it by section title.
