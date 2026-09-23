# Shared references

The rule set every skill in both plugins reads. `shared/` is the single source; the release
script copies it into each plugin, so a rule is written here once and is never restated
inside a skill.

**A skill does not read this folder.** It reads the file its current step's card names, and
the cards live with the skill (`references/cards/manifest.yaml` says which file each step
reads, and `shared/tools/context_budget.py` holds that honest — see `docs/CONTEXT-BUDGET.md`).
These files are the long form a card points at.

## The files

| File | What it holds |
|---|---|
| `pack-anatomy.md` | A ≤200-word **index**. The per-part detail lives in `anatomy/` — one card per part, at most 300 words each. |
| `anatomy/<part>.md` | The twelve parts of a pack — `problem-solution` · `one-liner` · `icp` · `name` · `verticals` · `capabilities` · `workflow` · `architecture` · `oracle-products` · `kpis` · `packages` — each with what the part is, the checks a draft must pass, one good and one bad example, and the spec keys it fills. |
| `anatomy/artifact-<name>.md` | The fixed section order of each of the six artifacts — `artifact-feature-list` · `artifact-deck` · `artifact-one-pager` · `artifact-exec-summary` · `artifact-listing` · `artifact-demo` — and the form each of the twelve parts takes there. Plus `anatomy/standard-extras.md` (the eight blocks on every sales artifact) and `anatomy/wfo-divergences.md` (what the delivered reference artifacts get wrong). |
| `engagement-context.md` | The engagement in two pages: who Oracle is to us, why we package, what Oracle gets, who reads what, the PoV Jumpstart / Integration / Scaling model, naming, clearance, and the volatile rows to re-check before use. Background reading, not a runtime file. |
| `naming-and-clearance.md` | What an artifact may call things and what it may disclose: the vendor naming table, pack name by channel, clearance per channel (internal · partner print · customer site · demo), the customer-name deny-list, the banned vocabulary for customer-facing copy, and the contract the artifact linter encodes. |
| `pov-rules.md` | What a PoV Jumpstart is and is not: duration, scope, what it proves, and the pushback rules. |
| `review-loop.md` | How the owner reviews and approves, so every skill behaves the same way: options with a recommendation, renders not descriptions, the one expected rebuild round, the open-items list, the fast path for a one-block rebuild, and the definition of done. §3 is the one every skill's "Showing it to the owner" section points at. |
| `architecture-diagram.md` | The one architecture diagram every artifact draws: where it is derived from, the naming rules, the flow rules, and the fresh-context reviewer's nine-point checklist. Read by that reviewer in its own context, not by the session. |
| `talking-to-the-owner.md` | **Long form.** The runtime card is each skill's `references/cards/owner-language.md`. Read this only when the card leaves a case open. |
| `slide-design.md` | The fourteen numbered design rules for decks, one-pagers and executive-summary slides. |
| `visual-assets.md` | Where a pack's icons and photographs may come from: the allowed sources and licences, what is never used, how icons are rendered on a Mac with no SVG rasterizer, the shared icon library's format and add-only rule, the customer's logo as the one owner-supplied picture (never searched for), what the picture credits record, and why an unreachable source is deferred rather than empty. |
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
