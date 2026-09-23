# The Jumpstart tab

**What this is.** One screen, the same shape on every product — fast · low-risk · tangible: pilot this pack fast, at low risk, with a tangible output.

**The checks**

1. `title` is exactly `Jumpstart Proof-of-Value`; `next` is exactly two, `Integration` then `Scale`. The three tiers are named **PoV Jumpstart · Integration · Scaling**.
2. **Only the proof-of-value price ships.** `next[].price` carries a figure only where a signed-off source publishes one, else `Scoped per engagement`; no money figure outside `investment` and `next`; no € on the services page. Every rendered price has its footnote in the same card, one line, never a stack.
3. `investment` is `{price, duration, includes ≥ 3, footnote}`; `price` and `duration` may each be `null`. With both null it prints one scoped-at-scoping line and no footnote; with one known it prints what it has.
4. One proof-of-value duration, stated identically everywhere in the data (`durationShort`). Any second duration anywhere fails the checker.
5. `pillars` is exactly three, in order — `fast` (kickoff to result), `low-risk` (fixed scope and price, your tenancy, no production change), `tangible` (the headline outcome) — claiming only what the evidence supports. `outcomes` is 3–4 **customer outcomes**, not deliverables; `timeline` 3–4 nodes, node 1 the pre-flight gate where there is one; `needs` exactly three short asks.
7. The brief's technical criteria (`kpis[].kind: technical`) ride here and nowhere else: one "Proof accepted when …" line in the scope — never on the Overview's metric tiles.
6. `promise` is written per pack and closes on its own clause — a catalog of lines ending on the same six words is the template tell a seller sees when they flip between two tabs live. Packaging-internal disclaimers ("framed scope", "flexible add-ons", "beyond the frame") fail the checker.

**Good.** "an optimized four-week plan for one region, measured against your current plan." **Bad.** "a plan document."

**Fills / reads:** `packages.tiers[pov]` (`services_price`, `duration_weeks`, `scope_in`/`scope_out`), `packages.tiers[integration]`, `packages.tiers[scaling]`, `kpis[]` where `kind: technical`.
