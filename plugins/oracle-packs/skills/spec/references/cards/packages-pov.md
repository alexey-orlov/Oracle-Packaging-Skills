# The proof of value

**What this is.** The first package, PoV Jumpstart: the customer gives data and we prove the value on it, in a separate or test environment, with **zero integration** into live systems — file export and import is the proof-grade integration; API integration belongs to Integration. A fixed scope, a fixed price where the pack has one, and the one metric set it is measured on. A customer already bought in may start at Integration, but every pack carries the proof.

**Duration.** Ideally 4–8 weeks. Above 8 it needs a written reason, and the owner keeps or narrows it; above 10 the linter refuses the brief. Printed in weeks, never months, in one wording everywhere.

**When it runs long**, say which of these applies and propose the cut:

1. **Scope leak**: more than one use case or data domain; cut to the one that carries the metric.
2. **Integration leaking in**: live connectors, write-back, identity work; move them to Integration and prove on exported data.
3. **Data readiness counted as proof work**: cleansing or collection the customer does before week 0 is an entry gate, not proof weeks.
4. **No number to hit**: a proof without one fills the time; fix the metric and its baseline first.
5. **Tuning without a stop rule**: cap the iterations and define "good enough" from the metric.
6. **The customer's calendar, not our work**: say so; the effort stays within the cap.

**Checks**

1. The target duration sits in 4–8 weeks, or its reason is in the brief.
2. Technical acceptance criteria ride this package's scope as "Proof accepted when …", never the metric set.
3. Its result is a proof-of-value result; "proven" is kept for a delivered production result.

**Fills:** the proof's `packages.tiers[]` entry — `duration_weeks`, `entry_gate`, `scope_in`, `scope_out`.
