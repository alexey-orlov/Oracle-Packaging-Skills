# Component 11 — key performance metrics

**What this is.** **One metric set per pack**: the numbers the buyer's business will directly improve by employing the solution.

**The five tests**

1. **Business.** Already tracked, or fit for a quarterly review — money, time, volume, risk or quality, in the buyer's words ("cost per claim", "planning cycle time"). Fails: precision, recall, accuracy, latency, coverage, reviewer agreement, confidence calibration (technical); documents ingested, users onboarded (vanity); better decisions, visibility (vague).
2. **Direct lever.** The solution moves it directly, not through a chain of assumptions. Where only a proxy does, the proxy is `kind: leading`; the business metric stays the metric.
3. **Outsider.** A reader outside the industry understands what it measures and why it matters; the industry's term may follow in brackets.
4. **Owner.** A named buyer-side role would sign it off (`owner_role`).
5. **Articulate when the inputs do not.** Where the engagement defined only technical acceptance criteria, derive the business metrics they serve, mark the figures `modeled` or "results to follow", record the criteria as `kind: technical`, and propose that set to the owner.

**Where each kind prints.** `business` on sales tiles and chips; `leading` only as a second line beneath it; `technical` never on a sales artifact — it belongs to the PoV package's success line ("Proof accepted when …").

**Hygiene.** One set for every artifact; figures never change by channel, only the name on them. Each states its status, ships its caveat, is end to end rather than the engine's, and is computed identically before and after.

**Good.** *"~30 min to plan a region's four weeks, down from ~2 days"* · *"€190K/month saved"*. **Bad.** *"Reviewer agreement ↑ · Confidence calibrated · Coverage ↑"* — acceptance criteria as outcomes.

**Fills:** `kpis[]` — `name`, `kind`, `owner_role`, `formula`, `baseline`, `figure`, `figure_status`, `caveat`, `attribution`.
