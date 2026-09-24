# Component 12 — the service packages table

**What this is.** Three tiers — **PoV Jumpstart / Integration / Scaling** — with `S / M / L` as size tags in internal tables only. Per tier: duration, services price, infrastructure price, what the customer gets, scope in and scope out, plus a per-capability-area handling row across the three tiers.

**Checks the draft must pass**

1. Tiers map to **integration depth, not feature count**: S proves the value with no integration in a test environment; M delivers a live, fully integrated deployment at one location; L scales it across markets with per-region rules and telemetry.
2. **PoV duration 4–8 weeks, 10-week hard cap** — above 8 the skill pushes back with reasons, above 10 it refuses (`shared/references/pov-rules.md`).
3. Nothing invented. Where a pack has no three tiers, the block is reframed honestly ("What the PoC buys": scope in, scope out, the real duration, the real contract value).
4. Prices beyond the PoV are never published externally, and an indicative price always carries its footnote. An absent price or duration is one grey label-sized "to be defined", never price type.
5. One tier vocabulary across the estate. The L tier is framed as telemetry and local tailoring, never as "hardening", which invites "what was wrong before?".
6. Capability rows render as `◐ partial · ● included · ●● multi-region / advanced`, with `—` where a capability is not in the tier, and the legend sits on the same page or slide.

**Good.** *"PoV · S — Manual data import, limited rule set: prove the KPI gains on the customer's data."*

**Bad.** A price on one slide contradicting the artifact thumbnail beside it. Two tier vocabularies in one estate.

**Fills:** `packages.tiers[]` — `name`, `size_tag`, `duration_weeks`, `services_price`, `infra_price_monthly`, `scope_in`, `scope_out`; `packages.capability_handling[]`.
