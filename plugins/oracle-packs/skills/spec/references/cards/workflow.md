# The workflow

**What this is.** What the product does: inputs → **5 to 7 steps** → outputs, with the human marked per step and a failure path per step. It is the axis the mini-site and the demo are both organized around.

**Checks the draft must pass**

1. Five to seven steps (hard cap 7; under three hides the work), grouped at the **buyer's checkpoints** — where a human decides, where an output appears, where data changes hands.
2. Mechanics — normalization, dedup, entity resolution, routing, outcome capture — live **inside** a step's description, never as steps of their own.
3. Steps are named after the work, not after system components.
4. Every step says who acts (system, human, or the model), and where a human decides, what they decide.
5. Every step has a failure path: what happens when the expected thing is not there, ≤ 12 words. "Not covered" is a permitted and required answer — it becomes an out-of-scope line, and the owner has already ruled on which package handles which failure.
6. Inputs and outputs name real source and destination systems, each with the tier at which the integration is real: "file export and import in the proof of value, API write-back in Integration".
7. The per-industry differences confirmed as real are carried on the steps they affect.

**Good / bad.** Good: `Load the period's data` → `Set the rules` → `Solve the plan` → `Review, approve, measure`, with the human step spelled out — the dispatcher compares the current and the optimized plan, approves or rejects per zone, re-runs, and nothing is exported until approval. Bad: twelve steps in which "deduplicate", "score" and "map to accounts" each got promoted to a step of its own.

**Fills:** `workflow.inputs[]`, `workflow.steps[]` (`name`, `actor`, `human_in_the_loop`, `failure_path`), `workflow.outputs[]`.
