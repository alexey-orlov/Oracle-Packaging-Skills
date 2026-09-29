# The Jumpstart tab

**What this is.** One screen, the same shape on every product: pilot this pack fast, at low risk, with a tangible output.

**The checks**

1. `title` is exactly `Jumpstart Proof-of-Value`; `next` is exactly two, `Integration` then `Scaling`, of the three tiers **PoV Jumpstart · Integration · Scaling**.
2. **Only the proof-of-value price ships.** `next[].price` carries a figure only where a signed-off source publishes one, else `Scoped per engagement`; no money figure outside `investment` and `next`. Every rendered price carries a one-line footnote in its card, never a stack.
3. `investment` is `{price, duration, includes ≥ 3, footnote}`; `price` and `duration` may each be `null`. Both null prints one scoped-at-scoping line and no footnote; one known prints what it has.
4. One proof-of-value duration (`durationShort`), identical everywhere in the data; any second duration fails the checker.
5. `pillars` is exactly three, in order — `fast` (kickoff to result), `low-risk` (fixed scope and price, your tenancy, no production change), `tangible` (the headline outcome) — claiming only what the evidence supports. `outcomes` is 3–4 **customer outcomes**, not deliverables; `timeline` 3–4 nodes, node 1 the pre-flight gate, if any; `needs` exactly three short asks.
6. `promise` is written per pack and closes on its own clause: lines ending on the same six words are the template tell a seller sees flipping between two tabs live. Packaging-internal disclaimers ("framed scope", "flexible add-ons", "beyond the frame") fail the checker.
7. The brief's technical criteria (`kpis[].kind: technical`) ride here only: one "Proof accepted when …" line in the scope, never on the Overview's metric tiles.

**Good.** "an optimized four-week plan for one region, measured against your current plan." **Bad.** "a plan document."

**Fills / reads:** `packages.tiers[pov]` (`services_price`, `duration_weeks`, `scope_in`/`scope_out`), `packages.tiers[integration]`, `packages.tiers[scaling]`, `kpis[]` where `kind: technical`.
