# The architecture

**What this is.** What the pack is built on: inputs → the stack, each layer saying whose technology it runs on → outputs. Distinct from the workflow, which is what it does. Derived from the capabilities, the workflow and the Oracle product list — nothing here is a fresh decision, so it is drafted, not asked about.

The drawing rules the deck, the one-pager and the site all obey are in `shared/references/architecture-diagram.md`; read that file when the diagram itself is being built, not here. The spec's job is to make every box and arrow derivable.

**Checks the draft must pass**

1. Every layer, box and arrow traces to a spec entry; nothing exists on the diagram that the spec does not carry.
2. The app layer carries the pack's name (with "by SoftServe" where the channel takes it), never a generic "accelerator business app"; its sub-line is what the app does, in the owner's words.
3. The engine layer names the vendor products by their catalog names — an unnamed engine tells a seller nothing.
4. Inputs and outputs are named systems in the buyer's words, and every one of them appears in `workflow.inputs`/`outputs` too; a product named in a footnote but absent from the stack is a defect.
5. Infrastructure is one layer naming the services actually used — the AI cluster or compute, Kubernetes, storage, database, networking, identity — by catalog id.
6. The vendor ladder is explicit, top to bottom: the app (the pack's name), the engine vendor, the infrastructure vendor. It starts at the application layer; the client's own configuration above it is not a rung.

**Fills:** `architecture.inputs[]`, `architecture.stack[]` (`layer`, `vendor`, `catalog_id`), `architecture.outputs[]`.
