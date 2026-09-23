---
name: visuals
description: Choose the pack's pictures with the owner — one icon per industry for the sales deck's industries slide, and the two photographs for the today → tomorrow slide — from openly licensed sources only, record where each came from, and write the choices into the pack so the deck, the one-pager and the site all use them. Use on /oracle-packs:visuals <pack-spec.yaml>, "pick the pictures for <pack>", "find icons for the industries", "we need photos for the before-and-after slide", or as the step before the sales deck in /oracle-packs:build.
disable-model-invocation: false
user-invocable: true
---

# /oracle-packs:visuals — the pack's pictures, chosen by the owner

> **Paths.** `shared/...` means `${CLAUDE_PLUGIN_ROOT}/shared/...` (each plugin carries a synced copy of the repo's `shared/` folder); `tools/...`, `assets/...` and `references/...` without a prefix are relative to this skill's own folder. In a plain-copy install the plugin folder sits at `.claude/skills/<plugin>/` and `${CLAUDE_PLUGIN_ROOT}` resolves to it.

The sales deck's industries slide carries a picture per industry, and its today → tomorrow slide carries two photographs: the way the work is done now on the left, the way it is done with the solution on the right. The owner used to pick those by hand. This step searches openly licensed sources, puts three candidates per picture in front of them, and records what they choose — so the deck is built with real pictures rather than numbers in boxes or empty frames.

**Nothing here is invented and nothing is guessed.** Every picture comes from a source whose licence permits commercial use without a credit line, and every file keeps a record of where it came from. A slot the owner does not choose for stays an empty container in the deck, which is the standing rule for absence (`shared/references/slide-design.md`, rule 3) — never a stand-in, never a number.

## Preconditions and inputs

- A confirmed, lint-clean `pack-spec.yaml` (`python3 shared/tools/lint_spec.py`). Otherwise stop and send the owner to `/oracle-packs:spec` — the industries and the problem/solution wording are what the searches are built from.
- Read `shared/references/visual-assets.md` (the sources, the licences, the house style and the traps), `shared/references/talking-to-the-owner.md` (every message, question and option passes its reader's test), `shared/references/review-loop.md` (§3: the thing is opened beside the conversation *before* the question) and `shared/references/slide-design.md`.
- Dependencies: Python 3 with `pyyaml` and `Pillow` (`plugins/oracle-packs/requirements.txt`), plus `qlmanage`, which is on every Mac. Check with `python3 -c "import yaml, PIL"`; tell the owner what to install if it fails and do not install into system Python yourself.
- **Say what is reachable before you start.** Run one search and read what the tool reports: which sources answered and which need a key. If the photograph sources that carry contemporary working-life pictures need a key this machine does not have, say so in one plain line *before* the first question — "the library I can reach has mostly archive photography; a free key for one stock library would give modern ones" — and let the owner decide whether to add one or work with what is reachable. A source that cannot be reached is **deferred**, never "nothing found".

## Procedure

1. **Read the spec and list the pictures.** The slots are one icon per entry in `verticals[]`, plus `cover` (the photograph on the right half of the title slide: the industry at work, wide, no text, no faces implying endorsement), `today` and `tomorrow` for the deck. Say it in one line, in the owner's words: "Twelve pictures to pick: an icon for each of your four industries, and the two photographs for the before-and-after slide. Three candidates each, you choose." Count the questions now — that is the `N` every question title carries.

2. **The icon for each industry.** `tools/suggest_icons.py "<the industry's name>" --context "<its 'what matters here' line>"` proposes three names; `tools/fetch_icon.py <name> --out <dir> --slot vertical:<i>` fetches each in both colours. Then `tools/contact_sheet.py <dir> --out <sheet.png>` lays them out.
   **Open the sheet beside the conversation before you ask** — `SendUserFile` with `display: "render"` — then one widget titled `Pictures · <n> of <N> · The icon for <the industry>`, with options `A` / `B` / `C`, one plain line each saying **what the icon shows** ("a washing machine", "a house with a gear", "a wrench"), plus **"Search again"** as free text: what the owner types becomes the next search. Options are pictures, never actions — no "keep looking", no "skip for now" as an option label.
   Judge the three yourself before showing them. If none of them says the industry, search again *before* asking: a question offering three wrong pictures wastes the owner's turn.

3. **The two photographs.** Build the search terms from the pack's own words, not from the industry name alone:
   - **today** — the pain in the way the work is done now, from `problem_solution.problem` and `problem_solution.today`: the desk, the paperwork, the manual step. Never a picture of the software.
   - **tomorrow** — the person using the solution, from `problem_solution.solution` and `problem_solution.tomorrow`: the reviewed plan, the screen, the decision being made.
   `tools/search_photos.py "<terms>" --out <dir> --slot today --n 3` (then `--slot tomorrow`), one contact sheet, opened beside the conversation, then one widget per slot titled `Pictures · <n> of <N> · The photograph for <today / tomorrow>`: options `A` / `B` / `C` with one plain line each — **what is in the picture, who took it and where it is from** ("a control-room wall of live maps, three people in front of it · Openverse, UrusHyby") — plus **"Search again"** (free text, which becomes the new search terms).
   The two photographs are read as a pair: same era, same register, both landscape. A 1950s archive photo opposite a modern one reads as a joke, not a contrast — check the pair on the sheet before asking.

4. **Record each choice.** `tools/apply_choice.py <spec> --slot <slot> --file <the chosen file>` copies the file into the pack, writes it into the pack brief, adds its row to the picture credits and logs the decision. Add `--note "<the owner's reason, in their words>"` when they gave one. For an icon worth reusing on other packs, add `--add-to-library` (it never overwrites an existing name).

5. **Close.** List what was chosen, one line per picture, and say where the files are and that the credits file records the licence for each. Name every slot with no choice, plainly: "the photograph for 'today' has nothing you liked yet — the deck will show an empty frame there until it does", and what would unblock it (different words to search for, or a key for a stock library). That list is the open items; do not bury it.

## Rules

- **Only sources whose licence permits commercial use without a credit line**, and only where the licence and the creator are recorded per file — CC0 and the Public Domain Mark through Openverse, the Pexels License, the Unsplash License, and for icons the MIT and ISC open sets. Never an image from a search engine, never a stock-library preview (Getty, Shutterstock, Adobe Stock, iStock), never a file whose licence nobody recorded, never a vendor's logo as an icon. The full rule set, with what each source needs, is `shared/references/visual-assets.md`.
- **The owner chooses; the skill never picks for them.** Three candidates, one widget, the sheet open beside it. Where the owner does not answer, the slot stays empty.
- **Never invent, never substitute.** No generated pictures, no "close enough" picture of a different industry, no icon standing in for a missing photograph, no numeral where an icon belongs.
- **People in a photograph are a decision, not a detail.** Prefer pictures where nobody is identifiable in a way that reads as an endorsement, and where the clothing, screens and equipment do not date the picture. Say it plainly when a candidate has this problem rather than letting it reach the deck.
- **Landscape, at least 1600 px wide, no text or watermark in the picture.** The deck's frames are wide; a portrait photograph is cropped to nothing.
- **Icons are one family.** All from one set, all one weight, rendered white for the dark panels and ink for light grounds. Mixing sets shows immediately when four sit in a row (`slide-design.md`, rule 2: peers share geometry).
- **A source that cannot be reached is deferred.** Say which source, what it needs, and that the picture is still open. Never write "nothing found" on the strength of a missing key or a timeout — that closes the item forever.
- **The picture credits file is part of the pack.** Every chosen file has a row in `packs/<slug>/visuals/credits.md`, including the ones whose licence asks for no credit: the record is what lets anyone check the right to use it a year later.

## Definition of done

Every industry has an icon and both photographs are chosen — or the ones without a choice are named to the owner as open. Every file is in `packs/<slug>/visuals/` with its row in the credits, the pack brief carries the choices and still passes its checks (`python3 shared/tools/lint_spec.py <spec>`), and the decisions are logged in `packs/<slug>/decisions.md`.

## Showing it to the owner

Everything the owner reviews is opened beside the conversation *before* the question is asked (`shared/references/review-loop.md` §3). In the Claude desktop app: the contact sheet opens in the side panel with the file-send tool (`SendUserFile`, `display: "render"`), then the widget. Never publish a pack's pictures as a claude.ai artifact — pack material stays on the machine. In a plain terminal with no panes, print the sheet's path and the candidate list with source and licence per candidate, and say so.

## Self-check before closing

- [ ] Every picture came from the allowed list, and its licence and creator are recorded in the credits file; nothing came from a search engine or a stock-library preview.
- [ ] The contact sheet was opened beside the conversation *before* each question, and the letters in the question match the letters on the sheet.
- [ ] Every question, option and closing line passes the reader's test: no method codes, no file or key names, no packaging vocabulary as vocabulary, reasons instead of rule names.
- [ ] The today and tomorrow photographs read as a pair — same era, same register, both landscape.
- [ ] No two industries ended up with the same icon — a wrench can be the best candidate for two of them, and two identical pictures in one row read as a mistake. Search again for the second rather than shipping the pair.
- [ ] Any slot with no choice is named as open, with what would unblock it; no slot was filled with a stand-in.
- [ ] A source that could not be reached was reported as deferred, with what it needs — never as "nothing found".
