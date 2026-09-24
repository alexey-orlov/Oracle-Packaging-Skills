# The packages

**What this is.** Three packages — **PoV Jumpstart · Integration · Scaling** — the last decision, because price and promise are one decision and the promise is the capability set. Per package: duration, services price, infrastructure price, what the customer gets, scope in and scope out; plus a row per capability area with its level in each package. The proof of value's own rules: card `packages-pov`.

**What each package means.** The proof proves the value with no integration, in a test environment, on the customer's own data. Integration delivers a live, fully integrated deployment at one location. Scaling takes it across markets with per-region rules and telemetry. Packages map to **integration depth, not feature count**.

**Checks the draft must pass**

1. Exactly these three names. S/M/L appear only as size tags in internal tables, never in customer-facing text.
2. No invented price, duration or scope line. A package without a settled price is marked "to be confirmed" with a footnote; prices beyond the proof are not published externally. A pack without three real packages says so honestly: what the proof buys, its scope, its real duration.
3. Every capability area has a level in every package: ◐ partial, ● included, ●● multi-region or advanced, — not in this package.
4. Scope out is written for each package, drawn from the failure paths the owner put out of scope.
5. Scaling is framed as telemetry and local tailoring, never as "hardening", which invites "what was wrong before?".

**Good.** "PoV Jumpstart · S — manual data import, a limited rule set: prove the gains on the customer's own data."

**Fills:** `packages.tiers[]` — `name`, `size_tag`, `duration_weeks`, `services_price`, `infra_price_monthly`, `scope_in`, `scope_out`; `packages.capability_handling[]` (`area`, `levels`).
