# Synthetic data

**What this is.** Everything in the demo is invented — geography, place names, postcodes, identifiers, people, documents, counterparties. The data file says so at the top.

**The checks**

1. **No customer mark of any kind** inside the demo: no name, logo, geography or identifier. **Vendor and platform marks are expected** where the demo runs on that platform — the rule is *no specific customer marks*, not *no marks*, and a vendor wordmark ships as text unless the logo file is cleared.
2. **Ground-truth specifics, not vagueness.** A fictional metro with twelve named zones and eighteen technicians is synthetic; "some regions" is not a demo.
3. **The cleared figure is reproduced exactly.** The demo's headline improvement is the figure the pack is cleared to claim, and the shipped stills show the state that carries it. No figure outside the cleared band; no time-to-deliver claim unless it is cleared.
4. **Companion figures are synthetic and modest** — they must not out-shout the cleared one, and they must reconcile with it arithmetically.
5. **List every synthetic figure for the owner in the report.** Every one. Not optional, and not a footnote.
6. **No money figure from a customer's business case** — no contract values, headcounts, salaries or operating baselines. Ratios, durations and counts only.
7. A map is **schematic**, drawn from a jittered grid: no tiles, no real geography.
8. The source engagement may be referred to only by the spec's anonymized descriptor.

**Good.** "Harbour View · HV-05 · technician T-1048". **Bad.** a real postcode, a real customer's region, or a contract value lifted from the business case.

**Fills / reads:** `clearance.anonymized_descriptor`, `kpis[].figure` and `.figure_status`, `kpis[].caveat`.
