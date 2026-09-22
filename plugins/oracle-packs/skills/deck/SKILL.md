---
name: deck
description: Build the accelerator pack's sales deck (.pptx on the SoftServe brand base) from a confirmed pack spec — the fixed 10-slide anatomy: cover, problem ↔ solution, verticals, how it works, proof of value, solution layers, architecture, service packages (PoV Jumpstart / Integration / Scaling) with the capability matrix, why it sells for the partner's seller, next steps and contact. Use on /oracle-packs:deck <pack-spec.yaml>, "make the sales deck for <pack>", "rebuild slide 8", or as step 2 of /oracle-packs:build.
disable-model-invocation: false
user-invocable: true
---

# /oracle-packs:deck — the sales deck for Oracle and SoftServe sellers

> **Paths.** `shared/...` means `${CLAUDE_PLUGIN_ROOT}/shared/...` (each plugin carries a synced copy of the repo's `shared/` folder); `tools/...`, `assets/...` and `references/...` without a prefix are relative to this skill's own folder. In a plain-copy install the plugin folder sits at `.claude/skills/<plugin>/` and `${CLAUDE_PLUGIN_ROOT}` resolves to it.


## Preconditions and inputs

- A confirmed, lint-clean `pack-spec.yaml`. Otherwise stop and send the user to `/oracle-packs:spec`.
- Channel: `partner_print` (default) or `internal`. Ask once with a widget if not given, and ask it as "who will see this deck": "Oracle and SoftServe sellers" (default) or "our own team" (adds prices in full, named accounts and internal notes where the pack brief allows). Store the two values; never show them.
- Read `shared/references/pack-anatomy.md`, this skill's `references/deck-anatomy.md` and `references/brand-tokens.md`, `shared/references/slide-design.md` (all rules), `shared/references/naming-and-clearance.md`, `shared/references/review-loop.md`, `shared/references/talking-to-the-owner.md` — every message, question and option the owner sees passes its reader's test.
- Pictures chosen: the icon per vertical (`verticals[].icon`) and the two photos (`deck.images.today` / `deck.images.tomorrow`) come from `/oracle-packs:visuals`, chosen by the owner from openly licensed sources. When they are missing, run it first; a slot the owner leaves unchosen stays an explicit empty container and the review pack says so.
- Dependencies: Python 3 with `pyyaml`, `python-pptx`, `Pillow`; the brand base `assets/softserve-deck-base.pptx` ships with the skill, and the industry icons come from the shared library at `shared/data/icons/`. Brand fonts are licensed and may be absent on this machine: the fit report uses metric stand-ins, so trust the report, not the rendered glyph widths.

## Procedure

1. **Read the spec** and the anatomy. Every slide's content comes from named spec keys (the anatomy file lists them); if a key is empty, the slide shows the honest state ("results to follow", "scoped per engagement") — never a placeholder that reads as fact.
2. **Ask for the two pictures — once, early, before the build.** One slide pairs the day as it is now with the day as it will be, and it has two picture slots. Ask the owner for both in one plain message, with the brief in their terms: *"the slide needs two pictures — the bad current experience on the left, the good future with the solution on the right; screenshots of the real thing are best, and I will crop them to fit."* Their answers go into the pack brief as `deck.images.today` and `deck.images.tomorrow` (paths, absolute or next to the brief). If they have none yet, build anyway: the slots stay explicit empty containers labelled "image to be chosen", and the open item goes in the review pack.
3. **Build**: `python3 tools/build_deck.py <spec> --out <dir> --channel <channel> --fit-report`. The fit report must be clean; an overflow — including a detailed-table cell over its word budget — is fixed by shortening the spec wording through the spec skill's fast path, never by shrinking type below the anatomy's floor.
4. **Lint the deck before anyone sees it**: `python3 tools/lint_deck.py <pptx> --spec <spec> --channel <channel>`. It checks the things that drift silently — the running header, no tier line on the cover, brand faces only, square corners, an icon rather than a number on every industry card, the architecture slide naming the pack, the engine's products and a destination with one arrow per source, and the package tables at or above their type floor. It must exit 0 before the render QA, and certainly before the owner. Then `python3 shared/tools/lint_artifact.py <pptx> --channel <channel> --spec <spec>` and `python3 shared/tools/check_consistency.py <spec> <pptx>`.
5. **Render QA**: run `tools/render_probe.sh` to see which renderer this machine has, render a contact sheet, and look at every slide: peers equal geometry, no free-floating text, colour semantics per the rules, no empty containers pretending to be content.
6. **Put the architecture picture to the owner in words.** The builder prints the whole diagram as plain sentences — the boxes on the left, what is in the middle, what it runs on, the box on the right, then every arrow and what it carries. Paste that into the review, in those words, and ask the one question that matters: is anything named wrong, and does anything flow the wrong way. It is the slide that has been wrong most often, and the owner can check it from the sentences alone.
7. **Editorial pass on the strongest model**: read every slide's text against the spec and the naming rules — prices match the spec, "proof of value" vs "proven" wording, tier names, the pack name variant for the channel, the integration claim states its tier, vendor names by catalog. This pass has caught a price slip and an overclaim on every previous deck; do not skip it.
8. **Review pack**, in the owner's words: the contact sheet, the pptx, a TLDR of the layout decisions, the architecture summary from step 6, the list of anything inferred or unconfirmed, and the open items — each named as what it is on the slide, never as a spec key or a design rule's number. Any industry that fell back to the neutral icon, and any picture slot still empty, is an open item named in plain words. Then one rebuild round. The builder writes the whole deck from the spec every time — there is no per-slide flag — so a single-slide change is a single-line change in the spec (through `/oracle-packs:spec`'s fast path) followed by the same `build_deck.py` call, and only the changed slide is re-reviewed.

## Rules that bite on decks

- Ten slides, the anatomy's order; packs differ in content, never in anatomy.
- The running header is the mini-site's own lockup, `Oracle AI & Data Solutions — <pack name>`, on every slide but the cover.
- No tier line on the cover. The three packages are slides 9 and 10.
- Corners are square — cards, panels, diagram boxes, containers. Only chips and numeral badges are pills, because those are the only things the reference rounds.
- Every industry card carries a picture, never a number. Nothing in the icon library matches → the neutral mark goes in, and that industry becomes an open item for the owner to pick a picture for.
- The architecture slide is derived from the pack brief: the app box carries the pack's own name "by SoftServe", the engine box names the products it runs by their catalog names, every data source has its own labelled arrow in, the result has a destination box and a labelled arrow out — and the only arrow back to a source is a write-back the brief actually states.
- The proof slide carries the one metric set with the channel's attribution and the caveat line; peer claims all-or-none (no "pending" next to a proven peer).
- Solution-layers ladder: partner layer on top, official logo images where the assets exist, layers differing in weight and shape, not tint alone.
- "Why it sells for the partner's seller" is its own slide: cross-sell path, net-new OCI consumption, repeatability; target consumption only when the spec has it.
- Deliver as a standalone pptx on the base's master. A section that has to paste into someone else's deck is the executive-summary skill's job, which does take `--host-deck <pptx>` and builds on that deck's master.
- Customer logo only when `clearance.customer_name_allowed[channel]` is true.

## Definition of done

Fit report clean, deck linter clean, contact sheet reviewed, clearance and consistency clean, the architecture put to the owner in words, editorial pass done, the owner's approval recorded in `packs/<slug>/decisions.md`, file delivered under `<Pack name> - Sales deck - Oracle.pptx`.

## Showing it to the owner

Everything the owner reviews is opened beside the conversation *before* the question is asked — the owner answers while looking at the thing, never at a description of it (`shared/references/review-loop.md` §3). In the Claude desktop app: a text file (the research summary, the pack brief, a spec) opens in the Files pane with the view-pane tool (`mcp__ccd_view__show_pane`, pane `file`, the path); a render (a page PNG, a PDF, an HTML page) opens in the side panel with the file-send tool (`SendUserFile`, `display: "render"`), with the editable file attached alongside (`display: "attach"`); then the widget. Never publish internal pack material as a claude.ai artifact — it leaves the machine; artifacts stay reserved for the mini-site demos. In a plain terminal with no panes, print the path and a text rendering, and say so. Here: the contact sheet of the rendered slides opens in the side panel, the .pptx is attached.

## Self-check before closing

- [ ] The automatic checks on the deck itself ran and came back clean, before the first render was shown.
- [ ] The owner was asked for the two pictures, and either they are in the deck or the empty slots are named as an open item.
- [ ] The architecture picture was put to the owner in plain sentences — every box and every arrow — not as "see slide 8".
- [ ] Every industry card carries a picture; any that fell back to the neutral mark is named for the owner to choose one.
- [ ] Every message, question, option and table the owner saw passes the reader's test: no method codes, no file or key names, no packaging vocabulary as vocabulary, reasons instead of rule names.
- [ ] Everything the owner reviewed was opened beside the conversation before the question was asked.
