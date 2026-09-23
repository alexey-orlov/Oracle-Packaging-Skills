# Slides 1–5 — what each carries

**What this is.** Slides 1–5: the keys each carries and what must be true of it. Long form: `deck-anatomy.md`.

**1 Cover.** `meta.name` (the channel's variant) · `one_liner.short` · `icp` · `deck.images.cover`.

- **No tier line on the cover** — packages are slides 9 and 10. No running header, no page number, nothing internal.
- The cover hero is the family's shared picture, unless `deck.images.cover` replaces it. An ink-only cover is unfinished.
- `meta.name_variants.external_subheading` has no slot here.

**2 Use case.** `problem_solution.{problem, problem_points[], reframe, solution}` · up to three `kpis[].chip` · `packages.anchor_line`.

- Two peer cards, identical boxes: problem neutral, solution blue.
- A chip with nothing to say is removed, never empty.

**3 Vertical applications.** `verticals[].{name, what_matters_here, icon}`.

- Every industry card carries a **picture, never a number**. No match → a stand-in, and an open item.
- Fewer than four industries greys the unused card — empty, never a gap.

**4 Today → tomorrow.** `problem_solution.{today, tomorrow}` (else problem / solution) · `one_liner` · `deck.vertical_case` · `deck.images.{today, tomorrow, customer_logo}`.

- The two pictures are one pair: the current way of working left, the solution right; a missing file leaves an empty container.

**5 Proof.** `meta.source_engagement.{context, delivered}` · `packages.value_for_{partner, client}` · `deck.proof_headline` · `kpis[]` · `deck.images.customer_logo`.

- **The delivered case in the reference's composition**, specific to that engagement: logo, headline, three stat tiles, four blocks labelled CONTEXT · SOLUTION · VALUE FOR ORACLE + NVIDIA · VALUE FOR CLIENT, the reference's own labels.
- **The tiles are never empty:** cleared figures, else the metrics measured, with baselines.
- The logo only where the channel clears the name and a file is named; otherwise `anonymized_descriptor`.
- **One** metric set, its attribution and caveat line. **Peer claims all or none:** a metric excluded from this channel drops the strip.
