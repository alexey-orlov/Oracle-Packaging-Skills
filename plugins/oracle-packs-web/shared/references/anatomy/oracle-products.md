# Components 9 and 10 — required and optional Oracle products

**What this is.** The Oracle products the pack is built on or fully relies on (`role: required`), and those a typical buyer would plausibly connect as an additional source or destination (`role: optional`) — by `id` from `shared/data/oracle-products.yaml` only, each with a one-line `why`.

**Checks the draft must pass**

1. **Required is only what the pack cannot run without**: the platform as one entry, its `why` naming the services it uses, plus the one or two products the core executes on. Typically 1–3.
2. **Optional is plausible connections only** — typically 2–4, each with a concrete reason it would be a source or a destination. A product listed because it exists in the catalog is a sweep, and it is cut.
3. Infrastructure sub-services are not entries; they are named on the architecture's infrastructure layer.
4. Every id exists in the catalog. A name that is not there is a catalog change request, not an entry.
5. **Every integration claim states its tier** in the sentence that makes it.
6. Only Oracle products go here; the engine vendor's products live on the architecture stack.

**Good.** Required: the platform alone, its `why` naming the AI cluster for the solver, Kubernetes for the app, object storage for the period's data, the database for plan versions. Optional: the field-service system, with *"file export / import at PoV Jumpstart; API write-back at Integration; API plus telemetry at Scaling."*

**Bad.** Five required entries because the delivered case touched five systems. An integration claim with no tier.

**Fills:** `oracle_products[]` — `id`, `role`, `why`, tier statements. Capped by `lint_spec.py` (SPEC021, SPEC022).
