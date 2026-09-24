---
name: deck
description: Build the accelerator pack's sales deck (.pptx, filled from the SoftServe reference deck) from a confirmed pack spec — the fixed 10-slide anatomy: cover, problem ↔ solution, verticals, how it works, proof of value, solution layers, architecture, service packages (PoV Jumpstart / Integration / Scaling) with the capability matrix, why it sells for the partner's seller, next steps and contact. Use on /oracle-packs:deck <pack-spec.md>, "make the sales deck for <pack>", "rebuild slide 8", or as step 2 of /oracle-packs:build.
disable-model-invocation: false
user-invocable: true
---

# /oracle-packs:deck — the sales deck for Oracle and SoftServe sellers

> **Paths.** `shared/...` means `${CLAUDE_PLUGIN_ROOT}/shared/...`; `tools/...`, `assets/...` and `references/...` without a prefix are relative to this skill's own folder.

> **Load only what the step needs.** `references/cards/manifest.yaml` lists, per step, exactly which files that step reads. Read those and nothing else — never the whole folder, never a card for a step you are not on, never a long reference a card already points to.

## Preconditions and inputs

- A confirmed, lint-clean `pack-spec.md`. Otherwise stop and send the user to `/oracle-packs:spec`.
- Channel: `partner_print` (default) or `internal`. Ask once with a widget if not given, and ask it as "who will see this deck": "Oracle and SoftServe sellers" (default) or "our own team" (adds prices in full, named accounts and internal notes where the pack brief allows). Store the two values; never show them.
- Pictures chosen: the icon per industry (`verticals[].icon`) and the photographs (`deck.images.cover`, `deck.images.today`, `deck.images.tomorrow`) come from `/oracle-packs:visuals`, chosen by the owner from openly licensed sources. Run it first when the brief has none; build anyway if the owner has not picked yet, and each unchosen slot stays an explicit empty container labelled "image to be chosen" and becomes an open item.
- Dependencies: Python 3 with `pyyaml`, `python-pptx`, `Pillow` — `shared/tools/py --check` says what is missing. The exemplar deck `assets/exemplar/wfo-sales-deck.pptx` and its slot map ship with the skill; the industry icons come from `shared/data/icons/`. The fit report measures with the brand fonts the plugin ships in `fonts/`; a render shows them only where they are installed — trust the fit report, not the rendered glyph widths.

## Procedure

1. **Build.** *Card: `build.md`, with `slides-1-5.md` and `slides-6-10.md`.* Every slide's content comes from named spec keys; an empty key shows the honest state, never a placeholder that reads as fact. `<dir>` is the pack's `artifacts` folder from `shared/tools/pack_paths.py <slug>` — never the repo.

       shared/tools/py tools/build_deck_v2.py <spec> --out <dir> --channel <channel> --fit-report

2. **Lint the deck before anyone sees it.** *Card: `lint.md`.* It must exit 0 before the render QA, and certainly before the owner. Among its checks: the cover carries the family's hero picture on the reference's own photo title layout — an ink-only cover is an unfinished state, never a build anyone delivers.

       shared/tools/py tools/lint_deck.py <pptx> --spec <spec> --channel <channel>

3. **Render and look at every slide.** *Card: `render-qa.md`.* `tools/render_probe.sh` says which renderer this machine has; make a contact sheet of all ten and read it by eye.

4. **The architecture picture on slide 8.** *Card: `diagram-reviewer.md`.* The picture is not drawn or reviewed here: `/oracle-packs:build` built the pack's one architecture model and had it reviewed once, and this slide renders it. Check that it still does.

       shared/tools/py shared/tools/check_diagram.py <spec> --deck <pptx> --channel <channel>

5. **Clearance, consistency and the editorial pass.** *Card: `clearance-and-editorial.md`.* Both scripts clean, then read every slide's text against the spec and the naming rules on the strongest model. Every subagent follows `shared/references/running-agents.md`.

       shared/tools/py shared/tools/lint_artifact.py <pptx> --channel <channel> --spec <spec>
       shared/tools/py shared/tools/check_consistency.py <spec> <pptx>

6. **The review pack, then the question.** *Card: `review-pack.md`.* The contact sheet, the .pptx, the layout decisions, the architecture in plain sentences, everything inferred or unconfirmed, and the open items — opened beside the conversation before the widget asks: approve, or say what to change.

7. **One rebuild round.** *Card: `fast-path.md`.* A single-slide change is a single-line change in the pack brief through the spec skill's fast path, then the same build call; only the changed slide is re-reviewed.

**How we talk to the owner:** `${CLAUDE_PLUGIN_ROOT}/skills/spec/references/cards/owner-language.md`, loaded at start-up, governs every message, question, option and table this run produces.

## Showing it to the owner

Everything the owner reviews is opened beside the conversation *before* the question is asked (`shared/references/review-loop.md` §3). In the Claude desktop app the contact sheet opens in the side panel with the file-send tool (`SendUserFile`, `display: "render"`), the .pptx attached alongside (`display: "attach"`), then the widget. Never publish pack material as a claude.ai artifact — artifacts stay reserved for the mini-site demos. In a plain terminal with no panes, print the path and a text rendering, and say so.

## Definition of done

Fit report clean, deck linter clean, contact sheet reviewed, the diagram check clean on slide 8, clearance and consistency clean, the architecture put to the owner in words, editorial pass done, the approval recorded in `<work>/decisions.md`, the file delivered as `<Pack name> - Sales deck - Oracle.pptx`.

## Self-check before closing

- [ ] The automatic checks on the deck ran and came back clean, before the first render was shown.
- [ ] The pictures were settled through the visuals step, or the empty slots are named as an open item.
- [ ] Slide 8 draws the pack's reviewed architecture model, and `check_diagram.py` says so — no second review of the picture here.
- [ ] The architecture was put to the owner in plain sentences — every box, every arrow — not as "see slide 8".
- [ ] Every industry card carries a picture; any that kept a stand-in is named for the owner to choose one.
- [ ] The cover carries the family's picture — the linter's cover check passed on its own, without `--legacy-cover-ok`.
- [ ] A deck redrawn by the legacy builder said so in the review pack, and was not handed over as final with an ink-only cover.
- [ ] Every message, question, option and table passed the reader's test: no method codes, no file or key names, no packaging vocabulary as vocabulary, reasons instead of rule names.
- [ ] Everything the owner reviewed was opened beside the conversation before the question was asked.
