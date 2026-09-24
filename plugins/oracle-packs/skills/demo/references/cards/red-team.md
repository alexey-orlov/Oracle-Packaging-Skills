# Red-team and fidelity

**What this is.** Two passes over the first cut, **before it is shown to anyone**: one against the pack's own documents, one against the real product's screens.

**The red-team, against the spec**

1. Hold the demo against the pack's S/M/L rows, its feature matrix and its listing copy, and ask the owner's question: **does it look too narrow next to what the pack documents claim?** The first documents demo covered one rate type, one document type and one validator, and had to be widened.
2. **Every capability area the pack sells is visible somewhere**; **every KPI in the spec appears in the value band**; **no claim goes beyond the spec**. A `roadmap` feature is not demonstrated as working — do not demo what the pack does not do.
3. Widen coverage **without changing the flow, the interface or the information architecture**. A gap between the demo and the real product is worse than a narrow demo.
4. Report the delta to the owner in two or three plain lines: what got wider, and why.

**The fidelity audit, against the real screens**

5. Where the platform's own screens are available, audit **every element** against the reference corpus and classify it internally: **A** a deviation where a reference exists · **B** an invention where none does · **C** a match. Measure with `getComputedStyle` and `getBoundingClientRect`, **never by eye**.
6. **Fix every A item.** Then report what is left **in plain words** — each element that has no counterpart in the real product, and why it was drawn that way. **Never as A/B/C**: those letters are internal and never reach the owner.

**Reads:** the pack spec's `capabilities[]`, `kpis[]` and `packages.capability_handling[]`; the listing copy; the reference corpus of real screens.
