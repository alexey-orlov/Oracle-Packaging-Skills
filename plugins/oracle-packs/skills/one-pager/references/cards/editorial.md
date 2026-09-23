# The editorial pass

**What this is.** The last read before the owner sees the page, on the strongest model, with fresh eyes: it has to read as a document a partner's seller would print, not as generated copy. Long form: `shared/references/client-documents.md`.

**Checks**

1. Typography and rhythm: no em-dashes, no arrows in prose (the data-flow strip's own arrows stay), no three same-shape blocks in a row: the page alternates paragraph, bullets, chips, figures, table (`slide-design.md`, compositional variety).
2. Voice: "customers", never "users"; third person throughout; no internal framings ("we packaged this", "the practice"), no packaging vocabulary as vocabulary.
3. No internal reference pricing on a partner-facing cut. Every figure carries its caveat, and the proof status word ("proof of value" / "proven") appears exactly once.
4. The proof strip speaks about the customer's business (their problem and what changed for them), never the engagement's mechanics (weeks, phases, contract status, "a proof of value" as a noun phrase), which belong to the caveat or the packages table. Its figures are business metrics only, never acceptance criteria. It names the customer only where the channel allows, else the anonymized descriptor, and no logo.
5. Summary altitude: the page reads as the whole offering, not as the delivered case with the names changed. "Why it sells" is written for the partner's seller and appears on no customer-facing artifact.
6. The name variant and subheading are the channel's, the tier names the spec's, the closing block the channel's contact — an address is a link, never a filled button.

**Bad.** "We leveraged the customer's data — enabling users to action insights in real time."
**Good.** "Planners review the proposed allocation instead of building it. Figures are from the eight-week proof of value and are not contractual."

**Reads:** `meta.name_variants`, `clearance.*`, `contacts.<channel>`, `one_pager.cta`, `packages.why_it_sells_for_the_partner[]`, `kpis[].kind`, `kpis[].caveat`.
