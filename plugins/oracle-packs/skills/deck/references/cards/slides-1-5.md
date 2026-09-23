# Slides 1–5 — what each carries

**What this is.** Slides 1–5: the spec keys each carries, and what must be true of it. Long form: `references/deck-anatomy.md`.

**1 Cover.** `meta.name` (the channel's variant) · `one_liner.short` · `icp` · `deck.images.cover`.

- **No tier line on the cover.** The packages are slides 9 and 10.
- No running header, no page number, nothing internal.
- The cover hero is the pack family's shared picture: it stays unless `deck.images.cover` replaces it. An ink-only cover is an unfinished state, never the default.
- `meta.name_variants.external_subheading` has no slot here and is not printed.

**2 Use case.** `problem_solution.{problem, problem_points[], reframe, solution}` · `kpis[].chip`, up to three · `packages.anchor_line`.

- Two peer cards, identical boxes; problem neutral, solution blue.
- A chip with nothing to say is removed, never left empty.

**3 Vertical applications.** `verticals[].{name, what_matters_here, icon}`.

- Every industry card carries a **picture, never a number**. Nothing in the icon library matches → the card keeps a stand-in and that industry is an open item for the owner.
- Fewer than four industries greys the unused card: an empty container, never a gap.

**4 Today → tomorrow.** `problem_solution.{today, tomorrow}` (falling back to problem / solution) · `one_liner` · `deck.vertical_case` · `deck.images.{today, tomorrow, customer_logo}`.

- The two pictures are one pair: the current way of working on the left, the solution on the right. A missing file leaves an empty container labelled "image to be chosen".

**5 Proof.** `kpis[]` with their attribution and caveat · `meta.source_engagement`.

- **One** metric set, with the channel's attribution and the caveat line.
- **Peer claims all or none:** a metric whose `channels` list excludes this channel drops the whole stat strip.
- The customer is named only per `clearance.customer_name_allowed.<channel>`; otherwise `anonymized_descriptor`.
