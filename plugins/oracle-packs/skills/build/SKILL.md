---
name: build
description: Build the full artifact set for a confirmed accelerator-pack spec, sequentially with a review pause after each artifact — feature list, sales deck, sales one-pager, executive summary — then hand off to the web plugin for the mini-site listing and the interactive demo. Use on /oracle-packs:build <pack-spec.yaml>, "build all the artifacts for <pack>", "produce the pack collateral", or after /oracle-packs:spec confirms a brief. Refuses to start on an unconfirmed spec.
disable-model-invocation: false
user-invocable: true
---

# /oracle-packs:build — all artifacts, in order, one review at a time

> **Paths.** `shared/...` means `${CLAUDE_PLUGIN_ROOT}/shared/...` (each plugin carries a synced copy of the repo's `shared/` folder); `tools/...`, `assets/...` and `references/...` without a prefix are relative to this skill's own folder. In a plain-copy install the plugin folder sits at `.claude/skills/<plugin>/` and `${CLAUDE_PLUGIN_ROOT}` resolves to it.


## Preconditions

1. Argument: the path to `packs/<slug>/pack-spec.yaml`. If missing, look for exactly one `packs/*/pack-spec.yaml` under the working directory; if none or several, ask.
2. `meta.status` must be `confirmed` and `python3 shared/tools/lint_spec.py <spec>` must be clean. Otherwise stop and send the user to `/oracle-packs:spec` (resume mode) — never patch the spec here.
3. Read `shared/references/review-loop.md`, `shared/references/naming-and-clearance.md`, and `shared/references/talking-to-the-owner.md` — every message, question and option the owner sees passes its reader's test. 

## The order and the pauses

**Do not re-ask what stage 1 already settled.** Read `packs/<slug>/intake.md`: which artifacts the owner wants (the answer to "Which of these do you want at the end?") and, if recorded there, who will see the printed documents. When the intake holds the answer, there is no question here at all. First, one short message with the map in the owner's words: the artifacts to be built, by name, in order, each reviewed before the next; where they will land; and that the printed documents are cut for Oracle and SoftServe sellers (`partner_print`) unless the owner says "our own team" (`internal`, which adds prices in full and named accounts where the pack brief allows) — they can say so in reply to this message or at any review, in free text. Then build. Only when the intake has no answer, ask once, in a single widget call — never one question with several artifacts bundled into an option (the widget caps a question at four options; there are six artifacts): (1) **Documents**, multi-select: Feature list (.docx) · Sales deck (.pptx) · Sales one-pager (.pdf) · Executive summary (.pptx); (2) **For the mini-site**, multi-select: Mini-site listing (a product page) · Interactive demo (a clickable walkthrough); (3) **Who will see the printed documents**, in exactly those terms: "Oracle and SoftServe sellers" (default) or "our own team". Store `partner_print` / `internal`; those two words never appear in the question, and neither does the name of the plugin that builds each artifact. One artifact per option, labels in that `<Artifact> (<format>)` form, each with a one-line description of what it is and who reads it. Skipping means all six. The default flow, in this order:

1. **Feature list** → `/oracle-packs:feature-list`
   ↳ then **Pictures** → `/oracle-packs:visuals` — before the deck: the icon for each industry and the two photos for today → tomorrow, proposed from openly licensed sources and chosen by the owner (the sheet opens in the side panel, then one widget per slot); a slot left unchosen stays an explicit empty container. It has its own place in the map ("Pictures"), right before the sales deck.
2. **Sales deck** → `/oracle-packs:deck`
3. **Sales one-pager** → `/oracle-packs:one-pager` (condensed from the deck; built after it on purpose)
4. **Executive summary** → `/oracle-packs:exec-summary`
5. **Mini-site listing** → `/oracle-packs-web:listing` (the web plugin; tell the user to run it if the plugin is not installed)
6. **Interactive demo** → `/oracle-packs-web:demo` (asks for sources first)

After each artifact: show the review pack the artifact skill produced (renders or the file, a TLDR of decisions, the list of anything synthetic or unconfirmed, the open items) — all of it in the owner's words, with no key names, check names or method vocabulary in it — then one widget, titled `Artifacts · n of N · <artifact name>: approve, change or stop`: **Approve and continue · Rebuild with changes (free text) · Stop here**. On "Rebuild", pass the free text to the artifact skill's fast path and re-present. Never start the next artifact before the current one is approved; the owner's feedback on the deck changes the one-pager.

## Consistency gate (after the last document artifact)

Run `python3 shared/tools/check_consistency.py <spec> <every produced file>`, then `lint_artifact.py` **once per artifact, on that artifact's own channel** — feature list and executive summary are `internal`, sales deck and one-pager are `partner_print` (the listing is `customer_site` and the walkthrough `demo`, in the web plugin). Do not lint the whole output directory on one channel: it reports the internal cut's own name variant as a partner-print finding and hides nothing real. The sales deck also has its own shape check, which the deck skill runs before showing anything and which is re-run here on the approved file: `python3 ${CLAUDE_PLUGIN_ROOT}/skills/deck/tools/lint_deck.py <deck.pptx> --spec <spec> --channel partner_print`. All of them must be clean before the web handoff. A ✗ in the consistency matrix is fixed in the artifact, never by editing the spec silently; if the spec is what is wrong, say so and send the user to the spec skill's fast path. What the owner hears about this gate is one plain line: the automatic checks passed, or what one of them found and what you did about it — never a tool name or raw checker output.

## Delivery

Copy the approved files to the delivery folder the user names (ask once; the owner's convention is the pack's own folder on the practice's shared drive, next to the earlier artifacts), keeping the pack's file-name pattern `<Pack name> - <Artifact> - Oracle.<ext>`. Append one line per artifact to `packs/<slug>/decisions.md` (date, channel, file, what changed on review). Close with: the files and where they are, what was decided differently from the pack brief and why, and the open items the owner still holds — named as parts of the pack, not as keys or steps.

## Showing it to the owner

Everything the owner reviews is opened beside the conversation *before* the question is asked — the owner answers while looking at the thing, never at a description of it (`shared/references/review-loop.md` §3). In the Claude desktop app: a text file (the research summary, the pack brief, a spec) opens in the Files pane with the view-pane tool (`mcp__ccd_view__show_pane`, pane `file`, the path); a render (a page PNG, a PDF, an HTML page) opens in the side panel with the file-send tool (`SendUserFile`, `display: "render"`), with the editable file attached alongside (`display: "attach"`); then the widget. Never publish internal pack material as a claude.ai artifact — it leaves the machine; artifacts stay reserved for the mini-site demos. In a plain terminal with no panes, print the path and a text rendering, and say so. Here: before each `Artifacts · n of N` widget, that artifact's render opens in the side panel and its editable file is attached.

## Self-check before closing

- [ ] Spec confirmed and lint-clean before the first build.
- [ ] Every artifact approved through a widget; no artifact built ahead of the previous approval.
- [ ] Consistency matrix and artifact lint clean for the delivered channel, and the sales deck's own shape check clean.
- [ ] Nothing internal-only in a partner or customer cut (contract values, named accounts, capacity numbers).
- [ ] Delivery paths and decisions logged.
- [ ] Every message, question, option and table the owner saw passes the reader's test: no method codes, no file or key names, no packaging vocabulary as vocabulary, reasons instead of rule names.
- [ ] Everything the owner reviewed was opened beside the conversation before the question was asked.
