# Component 8 — high-level architecture

**What this is.** Data inputs → the stack → outputs, with the vendor ladder explicit: which layer is the partner's, which the engine vendor's, which ours. Distinct from component 7 — this is what the pack is built on, not what it does.

**Checks the draft must pass**

1. **One diagram per pack**, reused by every artifact. A second diagram invented for one artifact is the failure this rule exists for.
2. Every data source has its own labelled arrow in; every system the result goes to has its own box and its own labelled arrow out; the only arrow back to a source is a write-back the brief actually states.
3. The stack names products by catalog id, and the app box carries the pack's own name.
4. The **ladder** is a separate device from the flow: custom configuration (ours) → accelerator business app (partner + ours) → engine (engine vendor) → infrastructure (partner). Partner layer on top, real logo images, layers differing in weight and shape, never in tint alone.
5. Infrastructure sub-services are named on the infrastructure layer, not promoted to products.

Full naming and flow rules, and the reviewer's checklist: `shared/references/architecture-diagram.md`.

**Good.** Source system on the left, the platform box on the right containing the app and the solver, two labelled pipes — *"technicians data, default allocations"* out, *"optimized allocations: zones, visits"* in.

**Bad.** Four rungs in four tints. A stack layer whose product names come from an internal deck rather than the catalog. The ladder drawn as if it were the data flow.

**Fills:** `architecture.stack[]`, `architecture.sources[]`, `architecture.outputs[]`, `architecture.layers[]`.
