# The context budget

_What a skill may read, when, and how the suite holds it to that. Rewritten to current truth — never appended with dated updates._

## The rule

A skill loads **only the file(s) its current step needs**, and its `SKILL.md` says which: each step names its files on a `Card:` line. `shared/tools/context_budget.py <SKILL.md>` reads those lines, counts every file they name, and fails when a step or a file is over its cap.

| Budget | Cap |
|---|---|
| Start-up: the `SKILL.md` plus the files on its `Start-up:` line | **6,000 tokens** |
| Any other step | **2,000 tokens** |
| A card (a `.md` under a `cards/` or `anatomy/` folder) | **300 words** (`owner-language.md`: 400) |
| A `SKILL.md` | **1,200 words** |

Tokens are estimated as `words × 1.35`, words counted as whitespace-separated runs (so a standalone `·`, `→` or `●` is a word). A file over its cap is reported as `card over 300 words: <path> (<n>)`, even with `--quiet`, and fails the run like a step over budget: the fix is to tighten the file without dropping a rule, never to raise the cap.

## The lines a SKILL.md uses

| Line | Means |
|---|---|
| `Card: \`x\`` · `Cards: \`x\`, \`y\`` | one step that loads these files together; the list ends at the sentence's full stop |
| `Cards, one per part: \`x\`, \`y\`` | one step per file ("one per" or "one at a time" before the colon) |
| `Start-up: \`x\`` | read with the `SKILL.md` before the first message |
| `Agents read: \`x\`` | read by a subagent in its own context: sized in the report, charged to no step |

A bare name is the skill's own card, `references/cards/<name>.md`; a name with a slash is a path from the skill's folder, and one beginning `shared/` is the plugin's `shared/`. The labels are case-sensitive, so "(card: `x`)" in running prose is a pointer, not a step. Every skill starts on the same two shared cards: `shared/cards/owner-language.md` (how every message to the owner is written) and `shared/cards/review-protocol.md` (how everything the owner reviews is shown, changed and approved).

## What enforces it

`tests/run_tests.sh` runs the tool on every `SKILL.md` it finds, so a new skill is covered the day it lands, and `tests/check_orphans.py` fails on any card that no step loads — a stub left behind by a restructure, or a rule that stopped reaching the model.

## Files no step loads, on purpose

- **Read by a tool, not the model**: measured references such as the deck's geometry table, brand tokens and exemplar slot map, the fit ladder's numbers, the icon keywords. They sit beside their tool, say in their header that a tool reads them, and the model reads what the tool prints.
- **Code to copy from**: the demo's reference walkthrough and tour engine. The build card says to open the one file being adapted, never the folder.
- **Background for a subagent**: long forms a step's `Agents read:` line names, such as `generalization-method.md` (each research agent reads its own prompt) and `architecture-diagram.md` (the diagram reviewer).

## How to add a card

1. Write `references/cards/<step>.md`, at most 300 words: **what the part is**, the **three to six checks** a draft must pass (each answerable pass or fail by a reviewer holding only the card and the draft), **one good and one bad example** where one exists, and the **spec keys it reads or fills**.
2. No rationale, owner quotes or history: those go to `docs/DECISIONS.md`.
3. One home per rule. If the rule lives on another card or in a shared reference, point at it in one line.
4. Name the card on the `Card:` line of the step that reads it, then run `shared/tools/py shared/tools/context_budget.py <SKILL.md>`. Over budget, split the step or cut the card.
