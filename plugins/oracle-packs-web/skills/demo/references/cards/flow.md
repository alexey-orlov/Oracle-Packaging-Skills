# The real flow

**What this is.** What the sources actually show, written down and confirmed before any design: the screens in order, the information model, where the human decides, what the system does at each step, what the outputs are. Written to `<work>/demo/flow.md`.

**The checks**

1. **The real product's flow, screens and information model are kept.** Only the **content** is generalized — to what the **pack** sells, its S/M/L rows and feature matrix, never to the one customer case. With no delivered product, the platform is the reference (card: `sources`).
2. **A tedious real workflow is deliberately simplified.** Reproducing a twelve-click reality is tedium, not fidelity. What may be cut is clicks; what may not is the **order** and the **information model**.
3. One major tour step per workflow step, in order. **A human-in-the-loop step is never merged away**: it becomes the manual-override step.
4. Each step's failure path is recorded — a wrong input flags a row, never drops it — and these become the demo's flags. The inputs become the mocked upload's file list, the outputs the export tab, in the real import format.
5. **Write the generalization before coding** — ten lines: the world, the period, the rules that visibly matter, the plans (current · v1 · v2 after feedback), the KPIs and how each is computed, the exceptions, the explanations, the integration and settings surfaces, the tour.
6. The flow is **confirmed with the user through a widget** — steps in order, which to keep, which to simplify.

**Good.** "Load the period's data → Set the rules → Solve the plan → Review, approve, measure." **Bad.** A twelve-step list making normalization, dedup and routing steps of their own; those happen *inside* a step.

**Fills / reads:** `workflow.inputs[]`, `workflow.steps[]` (`actor`, `human_in_the_loop`, `failure_path`), `workflow.outputs[]`, `verticals[]`.
