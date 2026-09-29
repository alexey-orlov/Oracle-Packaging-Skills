# The one-liner

**What this is.** The pack's one sentence, checked on every story candidate beside card `story`. It comes in two lengths: full, for print and hero copy, and short, said in one breath and derived from the full one. Every artifact inherits it verbatim, and the full one is the site's `oneLiner`.

**The checks**

1. It leads with the specific business value (time, money, risk or capacity) for a named role and object of work, in the buyer's terms. Any how is what changes in that person's work, in plain words.
2. No platform, vendor, engine, model or data-architecture word: Oracle, OCI, NVIDIA, cuOpt, NeMo, AI-Q, Lakehouse, GPU, LLM, gold, governed or semantic layer, confidence score, structured data (`lint_spec.py` holds the full list). They belong in the architecture.
3. A figure in it is Proven, a delivered result. It never repeats the metric chips, the tile bullets or the hero line word for word.
4. A qualifier only the delivered customer's circumstance explains is cut.
5. It describes the product, not an artifact ("AI accelerator service packages on Oracle OCI" describes a deck), with no packaging vocabulary ("accelerator pack", "ready-to-run", "packaged"), counts or taxonomy.

**Good.** "A region's four-week field plan, optimized in minutes and approved by dispatchers."
**Bad.** "Intelligent field-service planning with NVIDIA cuOpt on Oracle OCI: packaged from proof of value to enterprise scale": the engine, the platform and the packaging, and no value for anyone. "Decide repair or replace from the photos a customer already sends": of what? And the qualifier narrows it to one customer.

**Fills:** `one_liner.full`, `one_liner.short`.
