# Shared references

The rule set every skill in both plugins reads. `shared/` is the single source; the release
script copies it into each plugin, so a rule is written here once and is never restated
inside a skill.

## The files

| File | What it holds |
|---|---|
| `engagement-context.md` | The engagement in two pages: who Oracle is to us, why we package, what Oracle gets, who reads what, pack anatomy in brief, the PoV Jumpstart / Integration / Scaling model, naming, clearance, and the volatile rows to re-check before use. |
| `naming-and-clearance.md` | What an artifact may call things and what it may disclose: the vendor naming table, pack name by channel, clearance per channel (internal · partner print · customer site · demo), the customer-name deny-list, the banned vocabulary for customer-facing copy, and the contract the artifact linter encodes. |
| `pack-anatomy.md` | The twelve components of a pack, their definitions, and the map of which component lands in which artifact. |
| `pov-rules.md` | What a PoV Jumpstart is and is not: duration, scope, what it proves, and the pushback rules. |
| `review-loop.md` | How the owner reviews and approves, so every skill behaves the same way: options with a recommendation, renders not descriptions, the one expected rebuild round, the open-items list, the fast path for a one-block rebuild, and the definition of done. |
| `slide-design.md` | The fourteen numbered design rules for decks, one-pagers and executive-summary slides. |
| `client-documents.md` | Voice, de-AI typography and vocabulary, the summary-altitude rule, the living-documents rule, and persona-first marketing copy with its heading budgets. |
| `research-standards.md` | Labelled claims, source tiers, named specifics, explicit gaps, no force-filled frameworks, answer first. Governs the generalization research and the feature list. |
| `packaging-coaching-rules.md` | The coaching rules for turning one delivered engagement into a pack. |

Related, outside this folder: `shared/schema/pack-spec.md` (the machine-readable spec),
`shared/data/oracle-products.yaml` (the canonical product catalog every pack picks from), and
`shared/tools/lint_artifact.py` (the executable form of `naming-and-clearance.md`).

## How these files are maintained

**Rewritten to current truth, never appended.** When a rule changes, edit the rule in place
and leave the file reading as one coherent set. No dated "UPDATE" sections, no stacked
revisions, no "superseded, see below". A rule keeps the date it was set, inline, as part of
the rule — that is provenance, not an update log. Two agents once left a reference doc
carrying three contradictory verdicts on the same question; that is the failure this rule
exists to prevent.

**One home per rule.** Before adding a rule, look for the existing rule it sharpens. A rule
lives in exactly one of these files, and the others point at it rather than restating it.

**Subagents report, they do not edit.** A subagent that finds one of these files wrong,
stale, or contradicted by what it just learned reports the finding to the session that
launched it; the main session makes the edit. This is how the contradictions above got in.

**A new rule becomes a check in the same pass.** If `shared/tools/lint_artifact.py` can
assert it, assert it there when you write it here. A rule that is written down but not
checked survives one rewrite at best.
