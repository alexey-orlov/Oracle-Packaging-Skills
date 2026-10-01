# The metrics

**What this is.** **One metric set per pack** — what the business will improve by employing the solution.

**The five tests**

1. **Business.** Already tracked, or fit for a quarterly review — money, time, volume, risk or quality, in the buyer's words: "cost per claim", "planning cycle time". Fails — *technical*: reviewer agreement, coverage, precision, recall, accuracy, latency; *vanity*: signals processed, documents ingested, users onboarded; *vague*: better decisions, more insight, visibility.
2. **Direct lever.** The solution moves it directly, not through a chain of assumptions. Where only a proxy does, the proxy is `kind: leading`; the business metric stays the metric.
3. **Outsider.** Someone outside the industry sees what it measures and why it matters; the industry's term may follow in brackets.
4. **Owner.** A named buyer-side role would sign it off (`owner_role`).
5. **Articulate when the inputs do not.** Proofs of value usually define only technical criteria. Derive the business metrics they serve, frame each where a source you could name allows (`metrics-shown`), keep the criteria as `kind: technical` for the PoV scope line, and propose that set to the owner.

**Hygiene.** One set (two in the inputs: the owner picks); its figures never change by audience, only the name on them. Its status stated (`figure_status`); how it is shown: `metrics-shown`. A `leading` metric prints only as a second line beneath its business metric; `technical` never on a sales artifact. Formulas computable and identical before/after; figures end to end, review included; attribution per audience; a caveat states a fact about the figure, never a hedge.

**Good.** "2 days to 30 minutes to plan", "cost per completed visit". **Bad.** "Reviewer agreement ↑ · Confidence calibrated · Coverage ↑" — proof criteria, not outcomes.

**Fills:** `kpis[]` — `name`, `kind`, `owner_role`, `formula`, `baseline`, `figure`, `figure_status`, `attribution`, `caveat`.
