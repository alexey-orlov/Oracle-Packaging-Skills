---
name: visuals
description: Choose the pack's pictures with the owner — one icon per industry for the sales deck's industries slide, and the two photographs for the today → tomorrow slide — from openly licensed sources only, record where each came from, and write the choices into the pack so the deck, the one-pager and the site all use them. Use on /oracle-packs:visuals <pack-spec.yaml>, "pick the pictures for <pack>", "find icons for the industries", "we need photos for the before-and-after slide", or as the step before the sales deck in /oracle-packs:build.
disable-model-invocation: false
user-invocable: true
---

# /oracle-packs:visuals — the pack's pictures, chosen by the owner

> **Paths.** `shared/...` means `${CLAUDE_PLUGIN_ROOT}/shared/...`; `tools/...`, `assets/...` and `references/...` without a prefix are relative to this skill's own folder.

> **Load only what the step needs.** `references/cards/manifest.yaml` lists, per step, exactly which files that step reads. Read those and nothing else — never the whole folder, never a card for a step you are not on, never a long reference a card already points to.

The deck's industries slide carries a picture per industry, and its today → tomorrow slide two photographs: the work as it is done now, and as it is done with the solution. This step searches openly licensed sources, puts three candidates per picture in front of the owner, and records what they choose.

**Nothing here is invented and nothing is guessed.** Every picture comes from a source whose licence permits commercial use without a credit line, and every file keeps a record of where it came from. A slot the owner does not choose for stays an explicit empty container in the deck, the standing rule for absence (`shared/references/slide-design.md`, rule 3) — never a stand-in, never a number.

## Preconditions and inputs

- A confirmed, lint-clean `pack-spec.yaml` (`python3 shared/tools/lint_spec.py`). Otherwise stop and send the owner to `/oracle-packs:spec` — the industries and the problem/solution wording build the searches.
- Dependencies: Python 3 with `pyyaml` and `Pillow` (`plugins/oracle-packs/requirements.txt`), plus `qlmanage`, which is on every Mac. Check with `python3 -c "import yaml, PIL"`; tell the owner what to install if it fails, and do not install into system Python yourself.
- **Say what is reachable before you start.** Run one search and read what the tool reports: which sources answered, which need a key. When the sources carrying contemporary working-life pictures need a key this machine has not got, say so in one plain line *before* the first question and let the owner decide.

## Procedure

1. **List the pictures and count the questions.** The slots are one icon per entry in `verticals[]`, plus `today` and `tomorrow` — not the cover, which carries the family's shared picture and is offered only if the owner asks for one of this pack's own. Say it in one line, in the owner's words: "Six pictures to pick: an icon for each of your four industries, and the two photographs for the before-and-after slide. Three candidates each, you choose." That count is the `N` every question title carries.

2. **The icon for each industry.** *Cards: `icons.md` and `sources.md`.* Propose three, fetch them in both colours, lay them out as one sheet, open the sheet beside the conversation, then ask.

       python3 tools/suggest_icons.py "<industry>" --context "<its 'what matters here' line>"
       python3 tools/fetch_icon.py <name> --out <dir> --slot vertical:<i>
       python3 tools/contact_sheet.py <dir> --out <sheet.png>

3. **The two photographs.** *Cards: `photos.md` and `sources.md`.* Build the search terms from the pack's own words — the current way of working for `today`, the person using the solution for `tomorrow` — and read the pair on the sheet before asking.

       python3 tools/search_photos.py "<terms>" --out <dir> --slot today --n 3

4. **Record each choice.** *Card: `record.md`.* One command per picture; it copies the file, writes the key, credits it and logs the decision.

       python3 tools/apply_choice.py <spec> --slot <slot> --file <the chosen file> --note "<their reason>"

5. **Close.** *Card: `close.md`.* What was chosen, where the files are, and every slot still open with what would unblock it. That list is the open items; do not bury it.

**How we talk to the owner:** `${CLAUDE_PLUGIN_ROOT}/skills/spec/references/cards/owner-language.md`, loaded at start-up, governs every message, question and option this run produces.

## Showing it to the owner

Everything the owner reviews is opened beside the conversation *before* the question is asked (`shared/references/review-loop.md` §3). In the Claude desktop app the contact sheet opens in the side panel with the file-send tool (`SendUserFile`, `display: "render"`), then the widget. Never publish a pack's pictures as a claude.ai artifact — pack material stays on the machine. In a plain terminal with no panes, print the sheet's path and the candidates with source and licence, and say so.

## Definition of done

Every industry has an icon and both photographs are chosen — or the ones without a choice are named to the owner as open. Every file is in `packs/<slug>/visuals/` with its credits row, the brief carries the choices and still passes `lint_spec.py`, and the decisions are logged in `packs/<slug>/decisions.md`.

## Self-check before closing

- [ ] Every picture came from the allowed list, with its licence and creator in the credits file; nothing came from a search engine or a stock-library preview.
- [ ] The contact sheet was opened beside the conversation *before* each question, and the letters in the question match the letters on the sheet.
- [ ] Every question, option and closing line passed the reader's test: no method codes, no file or key names, no packaging vocabulary, reasons instead of rule names.
- [ ] The today and tomorrow photographs read as a pair — same era, same register, both landscape.
- [ ] No two industries ended up with the same icon.
- [ ] Any slot with no choice is named as open, with what would unblock it; no slot was filled with a stand-in.
- [ ] A source that could not be reached was reported as deferred, with what it needs — never as "nothing found".
