# Proof-of-value (PoV Jumpstart) rules

The owner's standing rule (2026-09-18): a PoV is determined per package, but ideally fits into **4–8 weeks**; **10 weeks is a hard cap**. The skills push back on longer PoVs and explain why.

## What a PoV is

- Tier one of three (PoV Jumpstart / Integration / Scaling), size tag S. "Proving AI value": the customer gives data, we prove value on that data, in a separate or test environment, with **zero integration** into live systems (file export / import is the PoV-grade integration; API integration belongs to the Integration tier).
- Fixed scope, fixed price where the pack has one (`packages.tiers[pov].services_price` with its status and footnote), one metric set that the PoV is measured on.
- Optional for a bought-in customer, who may start at Integration; never optional in the artifacts — every pack carries a PoV row.

## Duration rules the skills enforce

| Duration | Behaviour |
|---|---|
| 4–8 weeks | Proposed range; the spec's `duration_weeks.target` sits here |
| 8 < weeks ≤ 10 | Allowed only with `duration_weeks.justification` in the spec; the sign-off card states the justification and asks the user to keep or narrow |
| > 10 weeks | Rejected by `lint_spec.py`; the skill pushes back with the reasons below and proposes a narrower PoV |

## The pushback, when a PoV runs long

State which of these applies and propose the cut:

1. **Scope leak** — more than one use case or more than one data domain in the proof; cut to the one that carries the metric.
2. **Integration leaking into the proof** — live-system connectors, write-back, identity work; move them to Integration and prove on exported data.
3. **Data readiness treated as proof work** — cleansing or collection that the customer must do before week 0; make it an entry gate (`jumpstart.needs`), not PoV weeks.
4. **Unclear success metric** — a proof without a number to hit expands to fill the time; fix the metric and baseline first.
5. **Model or rule tuning without a stop rule** — cap tuning iterations and define "good enough" from the metric.
6. **Customer calendar, not our work** — if the elapsed time is waiting, say so: the PoV effort stays within the cap and the calendar is the customer's.

## Wording on artifacts

- Print the duration as weeks ("6–8 weeks"), never as months; one wording across all artifacts, taken from the spec.
- A price never appears without its status and footnote; the PoV price is the only price on customer-facing surfaces.
- The proof's outcome is a **proof of value** result unless a delivered, production result exists; "proven" is reserved for that.
