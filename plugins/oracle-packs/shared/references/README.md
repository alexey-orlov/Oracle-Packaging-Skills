# Shared references

The rule set every skill in the plugin reads. `shared/` is its single home, so a rule is
written here once and is never restated inside a skill.

**A skill does not read this folder.** It reads the cards its current step names on the
`Card:` lines of its `SKILL.md` (`shared/tools/context_budget.py` holds that honest — see
`docs/CONTEXT-BUDGET.md`): its own, and the two every skill loads at start-up from
`shared/cards/` — `owner-language.md` (how every message to the owner is written) and
`review-protocol.md` (how everything the owner reviews is shown, changed and approved).
These files are the long forms a card or a subagent's prompt points at.

## The files

| File | What it holds |
|---|---|
| `engagement-context.md` | The engagement in two pages: who Oracle is to us, why we package, what Oracle gets, who reads what, the PoV Jumpstart / Integration / Scaling model, naming, clearance, and the volatile rows to re-check before use. Background reading, not a runtime file. |
| `naming-and-clearance.md` | What an artifact may call things and what it may disclose: the vendor naming table, pack name by channel, clearance per channel (internal · partner print · customer site · demo), the customer-name deny-list, the banned vocabulary for customer-facing copy, and the contract the artifact linter encodes. |
| `architecture-diagram.md` | The one architecture diagram every artifact draws: where it is derived from, the naming rules, the flow rules, and the fresh-context reviewer's nine-point checklist. Read by that reviewer in its own context, not by the session. |
| `slide-design.md` | The fourteen numbered design rules for decks, one-pagers and executive-summary slides. |
| `visual-assets.md` | Where a pack's icons and photographs may come from: the allowed sources and licences and where their keys are read from, what is never used, how icons are rendered (QuickLook, `rsvg-convert` or `cairosvg`), the shared icon library's format and add-only rule, the customer's logo as the one owner-supplied picture (never searched for), what the picture credits record, and why an unreachable source is deferred rather than empty. |
| `client-documents.md` | Voice, de-AI typography and vocabulary, the summary-altitude rule, the living-documents rule, and persona-first marketing copy with its heading budgets. |
| `research-standards.md` | Labelled claims, source tiers, named specifics, explicit gaps, no force-filled frameworks, answer first. Governs the generalization research and the feature list. |
| `running-agents.md` | The four rules every subagent follows: model routing, the tool rules its prompt spells out, a per-unit progress log the session can check, and reporting rather than editing reference docs. Read once, when an agent's prompt is written. |

Related, outside this folder: `shared/schema/pack-spec.md` (the machine-readable spec),
`shared/data/oracle-products.yaml` (the canonical product catalog every pack picks from), and
`shared/tools/lint_artifact.py` (the executable form of `naming-and-clearance.md`).

## How these files are maintained

**Rewritten to current truth, never appended.** When a rule changes, edit the rule in place
and leave the file reading as one coherent set. No dated "UPDATE" sections, no stacked
revisions, no "superseded, see below". A rule keeps the date it was set, inline, as part of
the rule — that is provenance, not an update log.

**Rules and tests only.** The *why* — owner quotes, the round that produced a rule, the
failure it prevents — lives in `docs/DECISIONS.md`, one row per decision. These files say
what to do; that file says why.

**One home per rule.** Before adding a rule, look for the existing rule it sharpens. A rule
lives in exactly one of these files (or on one card), and everything else points at it
rather than restating it.

**Subagents report, they do not edit.** A subagent that finds one of these files wrong,
stale, or contradicted by what it just learned reports the finding to the session that
launched it; the main session makes the edit.

**A new rule becomes a check in the same pass.** If `shared/tools/lint_artifact.py` can
assert it, assert it there when you write it here. A rule that is written down but not
checked survives one rewrite at best.
