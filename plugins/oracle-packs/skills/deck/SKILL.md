---
name: deck
description: Build the accelerator pack's sales deck (.pptx, filled from the SoftServe reference deck) from a confirmed pack spec — the fixed 10-slide anatomy: cover, problem ↔ solution, verticals, how it works, proof of value, solution layers, architecture, service packages (PoV Jumpstart / Integration / Scaling) with the capability matrix, why it sells for the partner's seller, next steps and contact. Use on /oracle-packs:deck <pack-spec.yaml>, "make the sales deck for <pack>", "rebuild slide 8", or as step 2 of /oracle-packs:build.
disable-model-invocation: false
user-invocable: true
---

# /oracle-packs:deck — the sales deck for Oracle and SoftServe sellers

> **Paths.** `shared/...` means `${CLAUDE_PLUGIN_ROOT}/shared/...` (each plugin carries a synced copy of the repo's `shared/` folder); `tools/...`, `assets/...` and `references/...` without a prefix are relative to this skill's own folder. In a plain-copy install the plugin folder sits at `.claude/skills/<plugin>/` and `${CLAUDE_PLUGIN_ROOT}` resolves to it.


## Preconditions and inputs

- A confirmed, lint-clean `pack-spec.yaml`. Otherwise stop and send the user to `/oracle-packs:spec`.
- Channel: `partner_print` (default) or `internal`. Ask once with a widget if not given, and ask it as "who will see this deck": "Oracle and SoftServe sellers" (default) or "our own team" (adds prices in full, named accounts and internal notes where the pack brief allows). Store the two values; never show them.
- Read `shared/references/pack-anatomy.md`, this skill's `references/deck-anatomy.md` and `references/brand-tokens.md`, `shared/references/slide-design.md` (all rules), `shared/references/architecture-diagram.md`, `shared/references/naming-and-clearance.md`, `shared/references/review-loop.md`, `shared/references/talking-to-the-owner.md` — every message, question and option the owner sees passes its reader's test.
- Pictures chosen: the icon per vertical (`verticals[].icon`) and the photos (`deck.images.cover`, `deck.images.today`, `deck.images.tomorrow`) come from `/oracle-packs:visuals`, chosen by the owner from openly licensed sources. When they are missing, run it first; a slot the owner leaves unchosen stays an explicit empty container and the review pack says so.
- Dependencies: Python 3 with `pyyaml`, `python-pptx`, `Pillow`; the exemplar deck `assets/exemplar/wfo-sales-deck.pptx` and its slot map ship with the skill, and the industry icons come from the shared library at `shared/data/icons/`. Brand fonts are licensed and may be absent on this machine: the fit report uses metric stand-ins, so trust the report, not the rendered glyph widths.

## Procedure

1. **Read the spec** and the anatomy. Every slide's content comes from named spec keys (the anatomy file lists them); if a key is empty, the slide shows the honest state ("results to follow", "scoped per engagement") — never a placeholder that reads as fact.
2. **Make sure the pictures are chosen — once, early, before the build.** The icons per industry and the three photos (cover, and the pair on the today → tomorrow slide) come from `/oracle-packs:visuals`; run it first when the brief has none. If the owner has not picked yet, build anyway: each slot stays an explicit empty container labelled "image to be chosen", and the open item goes in the review pack in plain words.
3. **Build**: `python3 tools/build_deck_v2.py <spec> --out <dir> --channel <channel> --fit-report`. It fills the exemplar deck's own slides — geometry, type, colour, corners and the table idiom come from the reference by construction, and nothing here draws a card. The fit report must be clean; an overflow — including a detailed-table cell over its word budget — is fixed by shortening the spec wording through the spec skill's fast path, never by shrinking type below the anatomy's floor. `tools/build_deck.py` is the **legacy** builder, which redraws every slide on the 41 KB brand shell; use it only where the exemplar is not available, and say in the review pack that the deck was redrawn rather than filled.
4. **Lint the deck before anyone sees it**: `python3 tools/lint_deck.py <pptx> --spec <spec> --channel <channel>`. Every budget in it is measured from the exemplar itself: the running header, no tier line on the cover, the reference's own faces, no rounded card and no more pills than the reference's slide carries, an icon rather than a number on every industry card, the architecture slide naming the pack, the engine's products and every system the result goes to with one arrow per source, and the package tables at or above the reference's own type floor. It must exit 0 before the render QA, and certainly before the owner.
5. **Render the contact sheet**: run `tools/render_probe.sh` to see which renderer this machine has, render all ten slides, and look at every one: peers equal geometry, no free-floating text, colour semantics per the rules, no empty containers pretending to be content.
6. **The diagram reviewer pass on slide 8.** The architecture slide is the one that has been wrong most often, and the builder is the worst judge of it. Send a **fresh-context subagent** — model `opus` — the render of slide 8, the spec's `architecture` component, and `shared/references/architecture-diagram.md`, and nothing else: no build conversation, no rationale. It returns that file's nine-point checklist with pass/fail and a one-line reason each. Fix every fail and re-render; stop when it passes or after three rounds, and then put the remaining fails to the owner in plain words. The builder also prints the whole diagram as plain sentences — boxes, then arrows — and that summary goes into the review pack so the owner can check the naming and the direction without opening the slide.
7. **Clearance and consistency**: `python3 shared/tools/lint_artifact.py <pptx> --channel <channel> --spec <spec>` and `python3 shared/tools/check_consistency.py <spec> <pptx>`. Both clean before the owner sees anything.
8. **Editorial pass on the strongest model**: read every slide's text against the spec and the naming rules — prices match the spec, "proof of value" vs "proven" wording, tier names, the pack name variant for the channel, the integration claim states its tier, vendor names by catalog. This pass has caught a price slip and an overclaim on every previous deck; do not skip it.
9. **Review pack**, in the owner's words: the contact sheet, the pptx, a TLDR of the layout decisions, the architecture summary from step 6, the list of anything inferred or unconfirmed, and the open items — each named as what it is on the slide, never as a spec key or a design rule's number. Any industry that kept a stand-in icon, and any picture slot still empty, is an open item named in plain words. Everything goes beside the conversation before the question is asked (below), and the question itself is **a widget**: approve, or say what to change. Then one rebuild round. The builder writes the whole deck from the spec every time — there is no per-slide flag — so a single-slide change is a single-line change in the spec (through `/oracle-packs:spec`'s fast path) followed by the same `build_deck_v2.py` call, and only the changed slide is re-reviewed.

## Rules that bite on decks

- Ten slides, the anatomy's order; packs differ in content, never in anatomy.
- The running header is the mini-site's own lockup, `Oracle AI & Data Solutions — <pack name>`, on every slide but the cover.
- No tier line on the cover. The three packages are slides 9 and 10.
- Corners are square — cards, panels, diagram boxes, containers. Only chips and numeral badges are pills, because those are the only things the reference rounds, and none of them is half an inch tall.
- Every industry card carries a picture, never a number. Nothing in the icon library matches → the card keeps a stand-in, and that industry becomes an open item for the owner to pick a picture for.
- The architecture slide is derived from the pack brief: the app box carries the pack's own name "by SoftServe", the engine box names the products it runs by their catalog names, every data source has its own labelled arrow in, every system the result goes to has its own box and its own labelled arrow out — and the only arrow back to a source is a write-back the brief actually states. A system that only receives stands in a right-hand column, at the source boxes' own geometry; when every output is a write-back, the diagram keeps the reference's two columns.
- The proof slide carries the one metric set with the channel's attribution and the caveat line; peer claims all-or-none (no "pending" next to a proven peer).
- Solution-layers ladder: partner layer on top, official logo images where the assets exist, layers differing in weight and shape, not tint alone.
- "Why it sells for the partner's seller" is its own slide: cross-sell path, net-new OCI consumption, repeatability; target consumption only when the spec has it.
- Deliver as a standalone pptx on the exemplar's own master. A section that has to paste into someone else's deck is the executive-summary skill's job, which does take `--host-deck <pptx>` and builds on that deck's master.
- Customer logo only when `clearance.customer_name_allowed[channel]` is true.
- The reference pack's own pictures never ship on another pack's deck: the cover photo and the customer logo are replaced from the brief or removed.

## Definition of done

Fit report clean, deck linter clean, contact sheet reviewed, the diagram reviewer passed on slide 8, clearance and consistency clean, the architecture put to the owner in words, editorial pass done, the owner's approval recorded in `packs/<slug>/decisions.md`, file delivered under `<Pack name> - Sales deck - Oracle.pptx`.

## Showing it to the owner

Everything the owner reviews is opened beside the conversation *before* the question is asked — the owner answers while looking at the thing, never at a description of it (`shared/references/review-loop.md` §3). In the Claude desktop app: a text file (the research summary, the pack brief, a spec) opens in the Files pane with the view-pane tool (`mcp__ccd_view__show_pane`, pane `file`, the path); a render (a page PNG, a PDF, an HTML page) opens in the side panel with the file-send tool (`SendUserFile`, `display: "render"`), with the editable file attached alongside (`display: "attach"`); then the widget. Never publish internal pack material as a claude.ai artifact — it leaves the machine; artifacts stay reserved for the mini-site demos. In a plain terminal with no panes, print the path and a text rendering, and say so. Here: the contact sheet of the rendered slides opens in the side panel, the .pptx is attached.

## Self-check before closing

- [ ] The automatic checks on the deck itself ran and came back clean, before the first render was shown.
- [ ] The pictures were settled through the visuals step, and either they are in the deck or the empty slots are named as an open item.
- [ ] Slide 8 went to a fresh-context diagram reviewer that saw only the render, the brief's architecture and the diagram rules — not to me re-reading my own build.
- [ ] The architecture picture was put to the owner in plain sentences — every box and every arrow — not as "see slide 8".
- [ ] Every industry card carries a picture; any that kept a stand-in is named for the owner to choose one.
- [ ] Every message, question, option and table the owner saw passes the reader's test: no method codes, no file or key names, no packaging vocabulary as vocabulary, reasons instead of rule names.
- [ ] Everything the owner reviewed was opened beside the conversation before the question was asked.
