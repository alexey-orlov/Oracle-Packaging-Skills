# The Oracle products

**What this is.** Two short lists by catalog id, each entry with a concrete reason and what the integration is at each package.

**Required — only what the pack cannot run without:** the platform as one entry, its reason naming the services it uses (AI cluster or compute, Kubernetes, storage, database, networking, identity), plus the one or two products the core executes on. **Typically 1–3.** Infrastructure sub-services are not entries; they are named on the architecture's infrastructure layer. A system the pack reads from or writes to — even the delivered case's own — is optional, not required.

**Optional — only what a typical buyer would plausibly connect** as a source or destination, each with a concrete reason it would be one. **Typically 2–4.** A product listed because it exists in the catalog and could theoretically relate is a sweep, and it is cut.

**Checks the draft must pass**

1. Required ≤ 3, optional ≤ 4, or the overage is justified in one line.
2. Every id exists in the catalog; one that is not there is a catalog change request, never free text.
3. Only Oracle products are here — the engine vendor's belong on the architecture stack.
4. Every entry's reason names what it does for this pack, not what the product is.
5. Every integration claim states its tier: file export and import in the proof of value · API write-back in Integration · API plus telemetry in Scaling.

**Good.** One required entry — the platform, its reason naming the AI cluster for the solver, Kubernetes for the app, object storage for the data, the database for plan versions. The field-service system, the typical source and destination, sits in optional with its tier line.

**Fills:** `oracle_products[]` — `id`, `role`, `why`, `tiers`.
