# The whole brief

**What this is.** One table, one question, then the build starts.

**The table.** A row per part, in the order settled; columns: **the part, in your words · what we decided · status** (confirmed · proposed, awaiting your OK · open). Rows: the name and how it is written per audience; the one-liner, full and short; the problem and solution; who buys it; the industries; the capabilities per area and how many are available, partial or on the roadmap; the workflow steps; the architecture layers; the Oracle products, required and optional; the metrics and whose result they are; the three packages, durations, and whether prices are settled; who to contact; what may be named where; what is still open.

**The question.** One widget, `The whole brief · Confirm, change or stop`, with **exactly three options**: confirm as is (recommended) · make changes (free text) · stop here. Never a fourth, never a flow choice — what follows confirmation is fixed. On changes: apply, re-render, ask again.

**Checks before you ask**

1. Every part has a row; nothing settled earlier is missing.
2. Every status is true — anything not ruled on says "proposed", never "confirmed".
3. Everything deferred is in the open list, in plain words, with what it blocks.
4. The brief is open beside the conversation before the question.

**On "confirm".** Mark it confirmed, run the checks silently and save it (card `save`). Then one plain line — it is settled and saved, the checks passed (or what one found and what that means) — then the artifacts chosen at the start, named in order, each reviewed before the next, and invoke `/oracle-packs:build packs/<slug>/pack-spec.yaml` **at once, in the same session**. Never ask whether or how to proceed; never build an artifact here.
