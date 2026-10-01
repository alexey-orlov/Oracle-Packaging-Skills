# The technology tab

**What this is.** Exactly two blocks: `narrative` + `stack` under Architecture, then `capabilities`, never sharing a container; "how it runs" gets no block of its own.

**The checks**

1. `narrative` is two short sentences, about 40 words, heading the Architecture block. A second platform is named in full here and opens a `data-platform` item's name (card `entry-identity`).
2. `stack` is **4–5 layers**, top to bottom, a subsequence of `application` → `ai-engine` → `data-platform` → `infrastructure` → `custom`; all but `ai-engine` always present, a layer omitted but never re-ordered. `summary` is one sentence; `vendors` is non-empty and picks the wordmarks; every layer carries at least one `required: true`, a real boolean rendering Required / Optional. `note` is a short second chip, never ladder vocabulary. `direction` is legal only on `custom`, which names at least one inbound and one outbound.
3. `capabilities` is **exactly four** `{stage, items}` groups — stages unique, in workflow order, in the pack's own vocabulary, the same four `overview.steps` walks — ≥ 3 items each, together covering every feature the page claims anywhere.
4. The stage view is **derived, not re-typed**: `shared/tools/py tools/derive-stage-view.py <spec>` applies the spec's per-area `stage` mapping. The feature list stays the master; the derived view may **drop** a feature, never **add** one. A feature with no stage is reported, never dropped. Reconcile its count with the spec's before using it.
5. `state` is `supported` / `partial` / `roadmap`, **omitted** unless a real capability matrix states one — a guessed tag is worse than none. Spec to listing: `available` → no key · `partial` → `partial` · `roadmap` → `roadmap`.
6. `groups`, `layers`, `integration`, `notUsed`, `flow` and `security` fail the build. `governance` is optional: one band below the accordion.

**Fills / reads:** `architecture` and `architecture.stack[]`, `oracle_products[].role`, `capabilities[]` with `capabilities[].stage`.
