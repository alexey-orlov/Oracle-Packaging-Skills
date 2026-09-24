# Pack anatomy — the index

_What each part of a pack is, and the form it takes in each artifact. One card per part, at most 300 words each, in `shared/references/anatomy/`. A skill reads only the card for the part it is working on — never this whole folder. Rationale belongs in `docs/DECISIONS.md`._

**Three rules bind every skill that builds from a spec.** (1) **The spec is the only source**: a builder that finds a required part missing stops and sends the user to `/oracle-packs:spec`; it never re-derives a value or invents one. (2) **A part's content is one decision; its form is per-artifact** — the same words, laid out as that artifact's card says. (3) **"Not shown by design" is a legitimate cell.**

**The twelve parts**, in the order they are settled: [problem ↔ solution](anatomy/problem-solution.md) → [one-liner](anatomy/one-liner.md) → [target ICP](anatomy/icp.md) → [name](anatomy/name.md), then [verticals](anatomy/verticals.md) → [capabilities](anatomy/capabilities.md) → [workflow](anatomy/workflow.md) → [architecture](anatomy/architecture.md) → [Oracle products](anatomy/oracle-products.md) → [KPIs](anatomy/kpis.md) → [packages](anatomy/packages.md).

**Per artifact:** the feature list, the sales deck, the sales one-pager and the executive summary are laid out on the build skill's cards; [mini-site listing](anatomy/artifact-listing.md) · [interactive demo](anatomy/artifact-demo.md). Also [standard extras](anatomy/standard-extras.md) and [what the delivered WfO artifacts get wrong](anatomy/wfo-divergences.md).
