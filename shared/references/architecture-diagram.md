# The architecture diagram — derived from the spec, named, reviewed

_How the pack's architecture is drawn on the sales deck, the one-pager and the mini-site. One diagram, one set of rules, one reviewer pass. Rewritten to current truth — never appended with dated updates._

## Where it comes from

The diagram is **derived** from the spec's architecture component — `architecture.inputs[]` → the pack's app → the engine → the infrastructure → `architecture.outputs[]` — never drawn from a fixed set of three boxes. Every box and every arrow traces to a spec entry, and a box or arrow with no spec entry behind it does not exist.

## Naming rules (2026-09-22)

- **The app box carries the pack's name**, in the channel's variant, with "by SoftServe": "Account Insights by SoftServe", never a generic "Accelerator business app". Its sub-line is what the app does, from the app layer's items, in the owner's words.
- **The engine box names the vendor products**, by their catalog names from `shared/data/oracle-products.yaml`: "NVIDIA NeMo Agent Toolkit · NVIDIA AI-Q Blueprint". The layer's role ("agentic engine") is at most a small caption; an unnamed engine tells the seller nothing.
- **Sources and destinations are named systems**, in the buyer's words: "Signal feeds — news, filings, disclosures, commercial data feeds"; "Oracle Customer Experience (CX), or any CRM or sales system". The system of record the pack writes to is on the diagram when it is in `architecture.outputs[]`; a product named in the footnote but absent from the picture is a defect.
- **Infrastructure is one line** naming the OCI services actually used, as the spec's architecture stack lists them.

## Flow rules

- **Every input box has a labelled arrow into the app**; a source box with no arrow is a defect ("Organization context — not pointing to anything").
- **Every output has a destination box** with a labelled arrow from the app; outputs never point back at a source box unless that system is also an output (write-back) — and then it is a second, labelled arrow, not a reversal of the first.
- **Arrow labels are the data**, not verbs: "news, filings, disclosures" in; "structured per-account records" out.
- **Boxes of one role share one geometry** (slide-design rule 2): all source boxes equal, all destination boxes equal; the app and the engine differ from them in weight and shape, not tint alone (rule 5).
- **No decoration**: no arrow, box or icon that carries no spec entry.

## The reviewer pass — before the diagram reaches any artifact

The diagram is reviewed by a **fresh-context reviewer**: a subagent that receives only the rendered slide (PNG), the spec's architecture component and this file — never the build conversation — and returns the checklist below with a pass/fail and a one-line reason per item. The builder fixes every fail and re-renders; the loop stops when the reviewer passes or after three rounds, in which case the remaining fails are put to the owner in plain words.

Checklist:

1. The app box shows the pack's name with "by SoftServe".
2. The engine box names at least one catalog product; no box is an unnamed role.
3. Every source box has a labelled arrow into the app.
4. Every output in the spec has a destination box with a labelled arrow from the app.
5. No arrow runs from the app back to a source unless the spec lists that system as an output too.
6. The system of record named in the footnote or the tiers is on the diagram.
7. Boxes of one role share one geometry; the app and the engine are distinguishable by weight or shape.
8. Every label is readable at the rendered size (no label under the artifact's floor) and none is truncated.
9. Nothing on the diagram lacks a spec entry.

The same rendered diagram, once passed, is the one the one-pager's architecture strip and the mini-site's architecture view are derived from — one picture, three places.
