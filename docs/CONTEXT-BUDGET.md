# The context budget

_Why a skill reads cards instead of tomes, what the budget is, and how to add one. Rewritten to current truth — never appended with dated updates._

## The rule

A skill loads **only the file(s) its current step needs**. Which files those are is not a judgement call: every skill carries a `references/cards/manifest.yaml` that lists, per step, exactly what that step reads. `shared/tools/context_budget.py <manifest.yaml>` holds it honest.

| Budget | Cap |
|---|---|
| The start-up set — everything read before the first message | **6,000 tokens** |
| Any other step | **2,000 tokens** |
| A card | **300 words** (`owner-language.md`: 400), enforced per file |
| A skill's `SKILL.md` | **1,200 words**, enforced per file (the largest are `spec` at 1,177 and `listing` at 1,067; the other seven are under 1,000) |

Tokens are estimated as `words × 1.35`. **The word caps are enforced per file, not only per step:** every `.md` a manifest lists (`session` or `agents`) under a `cards/` or `anatomy/` folder, and every listed `SKILL.md`, is counted on its own, and a file over its cap is reported as `card over 300 words: <path> (<n>)` — even with `--quiet` — and fails the run exactly as a step over budget does. The tool exits 1 and names the offending files and sizes when a step or a file is over, 0 with a per-step table when nothing is, and 2 on a usage or dependency error. A `shared/…` path is measured in the plugin's synced copy (`plugins/<plugin>/shared/`), so a trim to the repo's `shared/` counts once `tools/sync-shared.sh` has run. `shared/tools/tests/run_tests.sh` **finds every manifest** under `plugins/*/skills/*/references/cards/` and runs the tool on each, and asserts that the count of manifests equals the count of `SKILL.md` files — so a card that grows past its cap or its step's share, or a skill that loses its manifest, fails in the test suite rather than in a live run. A card no manifest lists is outside the tool's reach and is held to the same 300 words by hand.

**`session` vs `agents`.** A manifest step lists `session` files — which enter the conversation and are charged to that step — and, optionally, `agents` files, which a subagent reads in its own fresh context. Agent files are sized and printed in the report but charged to no step: a prompt a subagent reads costs the session nothing. That is what keeps `generalization-method.md` (6,071 words of research prompts) out of the spec conversation entirely, `architecture-diagram.md` out of the deck build (the build skill's one diagram reviewer reads it), and `client-documents.md` out of the one-pager build (the fresh-eyes editor reads it).

**Tool-only references.** A long measured reference that a *tool* consumes — geometry tables, brand tokens, the exemplar slot map, the fit ladder's own numbers — is not a session file. It keeps its place next to the skill, carries a header line saying it is read by tools and not by the model, and appears in no `session` list. The model reads what the tool *prints*, not the file behind it.

## What it changed, measured

Start-up = everything the skill's `SKILL.md` told the model to read before its first message.

| Skill | Before: files | Before: ~tokens | After: files | After: ~tokens | Steps |
|---|---|---|---|---|---|
| `spec` | 14 | 52,300 | 3 | 2,561 | 15 |
| `build` | 4 | 9,378 | 3 | 1,963 | 6 |
| `feature-list` | 5 | 21,198 | 3 | 1,878 | 7 |
| `visuals` | 5 | 10,024 | 3 | 2,125 | 6 |
| `deck` | 9 | 29,576 | 3 | 2,226 | 8 |
| `one-pager` | 8 | 23,512 | 3 | 1,968 | 7 |
| `exec-summary` | 5 | 9,512 | 3 | 1,881 | 6 |
| `listing` | 8 | 22,912 | 3 | 2,381 | 9 |
| `demo` | 10 | 47,459 | 3 | 2,178 | 10 |
| **All nine** | **68** | **~226,000** | **27** | **~19,200** | **74** |

Every skill now opens on the same three files — its `SKILL.md`, its owner-language card, and its manifest — and reads the rest a step at a time. The heaviest single step in the bundle is the listing's insert step, ~1,890 of its 2,000 tokens (its two cards plus `shared/references/architecture-diagram.md`), so anything added there has to come out of it first; the next heaviest, around 1,600, are the deck's render QA, the spec's research summary and the listing's entry mapping.

The same restructuring cut `/oracle-packs:spec`'s run from about 30 questions to at most 12, by asking the intake in one or two calls, capping the research questions at four, settling name, one-liner, problem, solution and buyer as **one** story pick, and drafting the remaining seven parts in one pass with a fresh-context reviewer instead of a card each.

### Where the big references went

| Reference | Words | Now |
|---|---|---|
| `shared/references/pack-anatomy.md` | 7,727 | A 189-word index. The detail is 19 cards in `shared/references/anatomy/` — one per part, one per artifact, plus the standard extras and the reference estate's divergences. |
| `spec/references/generalization-method.md` | 6,071 | `agents` only — each research agent reads its own prompt. |
| `demo/assets/reference-demo/` + `tour-engine.js` | 26,463 | Code to copy and adapt, never reading material. In no list; the build card says to open the one file being adapted, never the folder. |
| `listing/references/listing-schema.md` | 4,175 | Long form; the runtime cards are `entry-identity`, `entry-overview`, `entry-case-study`, `entry-technology`, `entry-jumpstart`. |
| `listing/assets/exemplar-product-entry.js` | 3,543 | `agents` only, on the copy step. Generated from the live site by `tools/refresh-exemplar.mjs`, never edited by hand. |
| `feature-list/references/feature-list-anatomy.md` | 2,421 | Long form; the runtime cards are `build`, `does-not-fit`, `footnotes`, `statuses-and-wording`. |
| `listing/references/listing-rules.md` | 2,121 | Long form; the runtime cards are `claim-rules`, `copy-rules`, `exemplar-altitude`. |
| `shared/references/talking-to-the-owner.md` | 1,785 | Long form. The runtime card is each skill's `owner-language.md` (≤400 words). |
| `demo/references/demo-data-model.md`, `demo/assets/tour-engine.md` | 3,146 | `agents` only — too large for a session step, and the steps that need them run a subagent. |
| `listing/references/preview-and-publish.md` | 1,659 | Long form; the runtime cards are `preview` and `publish`. |
| `deck/references/reference-geometry.json`, `brand-tokens.md`, `exemplar-builder.md`, `one-pager/references/one-pager-anatomy.md`, `exec-summary/references/exec-summary-anatomy.md`, `visuals/references/icon-keywords.yaml` | — | Tool-only. Marked in their own headers, in no `session` list. |

## How to add a card

1. Write `references/cards/<step>.md`, at most 300 words, with four things and nothing else: **what the part is**, the **three to six checks** a draft must pass (each testable — a reviewer with only the card and the draft can answer pass or fail), **one good and one bad example** where one exists, and the **spec keys it reads or fills**.
2. No rationale, no owner quotes, no history. Those go to `docs/DECISIONS.md`, which is where a rule's *why* lives. A card is what to do, not why.
3. One home per rule. If a rule already lives on another card or in a shared reference, point at it in one line instead of copying it.
4. Add the card to the step that reads it in `manifest.yaml` — `session` if the conversation reads it, `agents` if only a subagent does.
5. Run `shared/tools/py shared/tools/context_budget.py <manifest.yaml>`. If the step is over, the fix is to split the step or cut the card; if the card is over 300 words, the tool names it and the fix is to tighten it without dropping a rule. Never raise a cap.

A new skill needs a manifest from its first commit: the test suite counts manifests against `SKILL.md` files and fails when one is missing.
