---
name: visuals
description: Choose the pack's pictures with the owner — one icon per industry, the two photographs for the today → tomorrow slide, and the delivered customer's logo where their name is cleared — from openly licensed sources only, the logo excepted: that one the owner supplies. Records where each came from and writes the choices into the pack for the deck, the one-pager and the site. Use on /oracle-packs:visuals <pack-spec.yaml>, "pick the pictures for <pack>", "find icons for the industries", "we need photos for the before-and-after slide", "add the customer's logo", or as the step before the sales deck in /oracle-packs:build.
disable-model-invocation: false
user-invocable: true
---

# /oracle-packs:visuals — the pack's pictures, chosen by the owner

> **Paths.** `shared/...` means `${CLAUDE_PLUGIN_ROOT}/shared/...`; `tools/...`, `assets/...` and `references/...` without a prefix are relative to this skill's own folder.

> **Load only what the step needs.** `references/cards/manifest.yaml` lists, per step, which files that step reads. Read those and nothing else — never the whole folder, never a card for a step you are not on. Every subagent follows `shared/references/running-agents.md`.

This step searches openly licensed sources, puts three candidates per picture in front of the owner, and records what they choose.

**Nothing here is invented and nothing is guessed.** Every picture comes from a source whose licence permits commercial use without a credit line — except the customer's own logo, which only the owner can supply — and every file keeps its record of where it came from. A slot with no choice stays an explicit empty container in the deck, the standing rule for absence (`shared/references/slide-design.md`, rule 3) — never a stand-in, never a number.

## Preconditions and inputs

- A confirmed, lint-clean `pack-spec.yaml` (`shared/tools/py shared/tools/lint_spec.py`). Otherwise stop and send the owner to `/oracle-packs:spec` — the industries and the problem/solution wording build the searches. The spec is the packaging-skills repo's: `shared/tools/py shared/tools/pack_paths.py <slug>` prints `<repo>` and `<work>`; `git -C <repo> pull --ff-only` before writing into it.
- Dependencies: Python 3 with `pyyaml` and `Pillow` (`plugins/oracle-packs/requirements.txt`), plus an SVG renderer: `qlmanage` (on every Mac), else `rsvg-convert` or `cairosvg`. Check with `shared/tools/py --check`; tell the owner what to install if it fails, never install into system Python yourself.
- **Say what is reachable before you start.** Run one search and read what the tool reports: which sources answered, which need a key. When a source that carries contemporary working-life pictures needs a key this machine has not got, say so *before* the first question.

## Procedure

1. **List the pictures and count the questions.** One icon per entry in `verticals[]`, plus `today` and `tomorrow`, plus the customer's logo where clearance allows it — not the cover, which carries the family's shared picture unless the owner asks for one of this pack's own. Say the count in one line, in the owner's words: "Six pictures to pick: an icon for each of your four industries, and the two photographs for the before-and-after slide." That count is the `N` every question title carries.

2. **The icon for each industry.** *Cards: `icons.md` and `sources.md`.* Propose three, fetch them in both colours, lay them out as one sheet, open the sheet beside the conversation, then ask. Candidates and sheets go under the pack's work folder — `<dir>` is `<work>/candidates/<slot>` (`shared/tools/pack_paths.py <slug>`) — never into the repo.

       shared/tools/py tools/suggest_icons.py "<industry>" --context "<its 'what matters here' line>"
       shared/tools/py tools/fetch_icon.py <name> --out <dir> --slot vertical:<i>
       shared/tools/py tools/contact_sheet.py <dir> --out <sheet.png>

3. **The two photographs.** *Cards: `photos.md` and `sources.md`.* Build the search terms from the pack's own words — the current way of working for `today`, the person using the solution for `tomorrow` — and read the pair on the sheet before asking.

       shared/tools/py tools/search_photos.py "<terms>" --out <dir> --slot today --n 3

4. **The customer's logo.** *Card: `customer-logo.md`.* Only when `clearance.customer_name_allowed` is true for some audience. One question — a widget offering "I'll give the path" free text, or skip — from the owner's engagement materials. **Never search the web for a logo:** a company's mark is a trademark, not an openly licensed picture.

5. **Record each choice.** *Card: `record.md`.* One command per picture; it copies the file into the repo's `packs/<slug>/visuals/` — the spec names it, and a colleague's build needs it — writes the key, credits it and logs the decision in `<work>/decisions.md`.

       shared/tools/py tools/apply_choice.py <spec> --slot <slot> --file <the chosen file> --note "<their reason>"

6. **Close.** *Cards: `close.md`, and the spec skill's `save`.* Save the pictures and the brief to the shared repo (`<what>` = `pictures`). Then what was chosen, where the files are, and every slot still open with what would unblock it. That list is the open items; do not bury it.

**How we talk to the owner:** `${CLAUDE_PLUGIN_ROOT}/skills/spec/references/cards/owner-language.md`, loaded at start-up, governs every message, question and option.

## Showing it to the owner

Everything the owner reviews is opened beside the conversation *before* the question (`shared/references/review-loop.md` §3). In the Claude desktop app the contact sheet opens in the side panel (`SendUserFile`, `display: "render"`), then the widget. Never publish a pack's pictures as a claude.ai artifact — pack material stays on the machine. In a plain terminal, print the sheet's path and the candidates with source and licence, and say so.

## Definition of done

Every industry has an icon, both photographs are chosen, and the logo is recorded or named as open. Every chosen file is in the repo's `packs/<slug>/visuals/` with its credits row, the brief carries the choices and still passes `lint_spec.py`, both are saved to the shared repo, and the decisions are logged in `<work>/decisions.md`.

## Self-check before closing

- [ ] Every picture came from the allowed list, with its licence and creator in the credits file; nothing came from a search engine or a stock-library preview, and no logo came off the web at all.
- [ ] The contact sheet was opened beside the conversation *before* each question, and the letters in the question match the letters on the sheet.
- [ ] Every question, option and closing line passed the reader's test: no codes, no file or key names, no packaging vocabulary, reasons instead of rule names.
- [ ] The today and tomorrow photographs read as a pair — same era, same register, both landscape.
- [ ] No two industries ended up with the same icon.
- [ ] Any slot with no choice is named as open, with what would unblock it; no slot was filled with a stand-in.
- [ ] A source that could not be reached was reported as deferred, with what it needs — never as "nothing found".
