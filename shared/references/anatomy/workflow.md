# Component 7 — workflow architecture

**What this is.** Inputs → processing steps → outputs, with the human-in-the-loop marked per step and a failure path per step. This is the product's behaviour, and it is the axis the mini-site and the interactive demo are both organized around.

**Checks the draft must pass**

1. **Five to seven steps**, hard cap seven. Fewer than three hides the work.
2. Grouped at the buyer's checkpoints — where a human decides, where an output appears, where data changes hands.
3. Mechanics — normalization, dedup, entity resolution, routing, outcome capture — are named inside a step's description, never steps of their own.
4. Every step carries its **failure path**: what happens to a bad row, and who resolves it.
5. Steps are named after the work, not after system components.
6. Heavy AI work is visible as work, never hidden behind a progress bar, which reads as ETL.

**Good.** `Load the period's data` → `Set the rules` → `Solve the plan` → `Review, approve, measure`, each carrying the features it exercises, with the human step spelled out: the dispatcher compares the current and the optimized plan on a live map, approves or rejects per zone with an optional comment, re-runs, and nothing is exported until approval.

**Bad.** Twelve steps, four of them normalization, dedup, entity resolution and routing. A happy path with no failure branch — the failure path is what a buyer's operations lead actually asks about.

**Fills:** `workflow.steps[]` — `n`, `name`, `description`, `hitl`, `failure_path`, `features[]`. Capped by `lint_spec.py` (SPEC019).
