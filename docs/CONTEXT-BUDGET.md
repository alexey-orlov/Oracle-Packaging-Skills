# The context budget

_Why a skill reads cards instead of tomes, what the budget is, and how to add one. Rewritten to current truth — never appended with dated updates._

## The rule

A skill loads **only the file(s) its current step needs**. Which files those are is not a judgement call: each skill carries a `references/cards/manifest.yaml` that lists, per step, exactly what that step reads. `shared/tools/context_budget.py <manifest.yaml>` holds it honest.

| Budget | Cap |
|---|---|
| The start-up set — everything read before the first message | **6,000 tokens** |
| Any other step | **2,000 tokens** |
| A card | **300 words** (`owner-language.md`: 400) |
| A skill's `SKILL.md` | **1,200 words** |

Tokens are estimated as `words × 1.35`. The tool exits 1 and names the offending files and sizes when a step is over, 0 with a per-step table when it is not, and 2 on a usage or dependency error. `shared/tools/tests/run_tests.sh` runs it on the spec skill's manifest, so a card that grows past its share fails in the test suite rather than in a live run.

**`session` vs `agents`.** A manifest step lists `session` files — which enter the conversation and are charged to that step — and, optionally, `agents` files, which a subagent reads in its own fresh context. Agent files are sized and printed in the report but charged to no step: a research prompt a subagent reads costs the session nothing. This is what keeps `generalization-method.md` (6,071 words of research prompts) out of the conversation entirely — each research agent reads its own prompt from it.

## What it changed, measured

Before, `/oracle-packs:spec` read 14 files before its first question:

| Set | Files | Words | ~Tokens |
|---|---|---|---|
| Before — everything read up front | 14 | 38,742 (34,031 of it prose; the rest the product catalog and the roadmap extract) | ~52,300 |
| After — the start-up set (`SKILL.md` + `owner-language.md` + the manifest) | 3 | 1,909 | ~2,577 |
| After — every session file of all 14 steps added together | 18 | 7,205 | ~9,727 |

The start-up read is **5% of what it was**; a whole run, every step included, is about a quarter. The heaviest single step is writing the research summary (1,195 words, ~1,613 tokens); every other step is under 1,300 tokens.

The same restructuring cut the run's questions from about 30 (up to 11 intake, 7 research questions, 1 story pick, 11 sign-off cards, 1 brief) to **at most 12**, by asking the intake in one or two calls, capping the research questions at four, settling name, one-liner, problem, solution and buyer as **one** story pick, and drafting the remaining seven parts in one pass with a fresh-context reviewer instead of a card each.

## How to add a card

1. Write `references/cards/<part>.md`, at most 300 words, with four things and nothing else: **what the part is**, the **three to six checks** a draft must pass (each testable — a reviewer with only the card and the draft can answer pass or fail), **one good and one bad example** where one exists, and the **spec keys it fills**.
2. No rationale, no owner quotes, no history. Those go to `docs/DECISIONS.md`, which is where a rule's *why* lives. A card is what to do, not why.
3. One home per rule. If a rule is already on another card or in a shared reference, point at it in one line instead of copying it.
4. Add the card to the step that reads it in `manifest.yaml` — `session` if the conversation reads it, `agents` if only a subagent does.
5. Run `python3 shared/tools/context_budget.py <manifest.yaml>`. If the step is over, the fix is to split the step or cut the card, never to raise the cap.

## What is still to do

Only the spec skill has a manifest today. Every other skill in both plugins gets one in the next stage, on the same shape and the same caps; until then they still read what their `SKILL.md` tells them to.
