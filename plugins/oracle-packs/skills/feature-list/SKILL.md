---
name: feature-list
description: Build the accelerator pack's feature list (.docx) from a confirmed pack spec — the Area > Category > Feature matrix with ● available / ◐ partial / ○ roadmap status and the standard customization scope per capability, no pricing. Use on /oracle-packs:feature-list <pack-spec.yaml>, "make the feature list for <pack>", "regenerate the capability matrix", or as step 1 of /oracle-packs:build.
disable-model-invocation: false
user-invocable: true
---

# /oracle-packs:feature-list — the capability matrix

> **Paths.** `shared/...` means `${CLAUDE_PLUGIN_ROOT}/shared/...` (each plugin carries a synced copy of the repo's `shared/` folder); `tools/...`, `assets/...` and `references/...` without a prefix are relative to this skill's own folder. In a plain-copy install the plugin folder sits at `.claude/skills/<plugin>/` and `${CLAUDE_PLUGIN_ROOT}` resolves to it.


The feature list is the pack's spine document: the table every other artifact condenses. It is internal / partner material, carries no prices, and states for every feature whether it is available, partial or roadmap and what is standardly customized per engagement.

## Preconditions and inputs

- A confirmed, lint-clean `pack-spec.yaml` (`python3 shared/tools/lint_spec.py`). Otherwise stop and send the user to `/oracle-packs:spec`.
- Read `shared/references/pack-anatomy.md` (the feature-list anatomy), this skill's `references/feature-list-anatomy.md`, `shared/references/naming-and-clearance.md`, and `shared/references/talking-to-the-owner.md` — every message, question and option the owner sees passes its reader's test.
- Dependencies: Python 3 with `pyyaml` and `python-docx` (`plugins/oracle-packs/requirements.txt`). Check with `python3 -c "import yaml, docx"` and tell the user what to install if it fails; do not install into system Python yourself.

## Procedure

1. **Read the spec**, not the delivered artifacts. The document opens with the mini-site lockup (the SoftServe wordmark and `Oracle AI & Data Solutions`), then the title `meta.name` + " — Feature list", then two lines: the **approved one-liner** (`one_liner.full`, or `feature_list.intro` where the pack needs a longer one) and **who it is for** (`For ` + `icp.line`). Rows = `capabilities[]` in spec order. If `icp.line` is missing, go back to `/oracle-packs:spec` for it rather than inventing a line — the build will otherwise print the one-liner alone and warn.
2. **Build**: `python3 tools/build_feature_list.py <spec> --out <dir>` (paths relative to this skill's folder; resolve via `${CLAUDE_PLUGIN_ROOT}`). Columns: Area · Category · Feature · Status (● ◐ ○) · Tier first available · Standard customization scope (the scope column stays last, as in the reference). Merge Area and Category cells like the reference. The legend is one line under the table; there is no page footer — the build writes the spec version and the generation date into the file's properties instead.
   The build guarantees **one A4 page**: it estimates the height and walks a fit ladder — a row per feature at 7.5pt, then 7pt, then compact mode (a row per category, features listed inline, the status and tier columns dropped) at 7.5 and 7pt — and where Pages is installed it verifies the real page count. `--fit none` allows several pages (only when someone has asked for the long form); `--no-check-pages` skips the verification. Read the mode it printed: needing compact mode is a signal the capability tree is too fine, worth saying to the owner.
   **Exit 3 means it does not fit on any rung and nothing was written.** Do not retry with smaller type — 7pt is the floor. Put the grouping to the owner in plain words, using the counts the build printed: which categories to merge into one, which sibling features to generalize into a single capability, which names to shorten. Get their decision, fix the tree through `/oracle-packs:spec`, and rebuild.
3. **Footnotes — cut them before building.** A footnote exists only for a tier caveat that changes what the buyer gets, typically an integration claim stating its tier ("file export at PoV; API write-back at Integration"): **15 words or fewer, at most three in the whole document** (the owner, 2026-09-22). It carries the caveat alone — never the feature name, the category, or a description repeated back, since the marker already points at the row. Anything else belongs in that area's customization-scope cell, or nowhere. The build warns on stderr when there are more than three notes or one runs long; take those to the owner in plain words ("three of these read as descriptions rather than caveats — I'd drop them and keep the two about tiers"), fix them in the spec, then build.
4. **Check**: every feature has a status; no area without a customization line; no price, no customer name (`python3 shared/tools/lint_artifact.py <file> --channel internal --spec <spec>`); counts per area match the spec. The feature list is the **internal** cut — it is the pack's internal/partner spine document, and `internal` is the channel the tools README and `/oracle-packs:build` use for it. When a copy goes to an Oracle seller as-is, lint it again on `partner_print` and expect the channel's name variant (sentence case) to be the only difference.
5. **Review pack** for the owner: the docx, a plain-text rendering of the table (so it can be read in chat), and, per area, how many capabilities are available, partial and on the roadmap — in those words, not as a count of glyphs. Say **how the page came out**: one row per feature or a row per category (and, if the latter, that the status column went away because the statuses now sit beside each feature), and whether the single page is an estimate or was verified. Then any feature whose status came from research rather than from what we actually built: name it and say so plainly, and let them confirm it or move it to the roadmap.
6. **One rebuild round** on feedback; a single-row change is a fast path (edit the spec through `/oracle-packs:spec` fast path, rebuild, re-lint).

## Rules

- **One page is a requirement** (the owner, 2026-09-22). Think in grouped, generalized capabilities from the spec onward, not at build time: a feature list that needs compact mode is a sign the capability tree is too fine, and one that needs more than compact mode is not a formatting problem at all. The sizing rule lives with the capability tree (`shared/references/pack-anatomy.md` §6): at most 6 areas, about 12 categories, 30–35 features, names of 8 words or fewer. Never shrink type below 7pt to buy space.
- The header is the mini-site's: the SoftServe wordmark lockup with `Oracle AI & Data Solutions`. No text kicker, no eyebrow, no `App.` definition label — the top block is the approved one-liner and one sentence saying who it is for.
- **Nothing in the page footer** (the owner, 2026-09-22). The spec version and build date live in the file's properties, which the build writes; never print them on the page.
- Statuses follow the owner's decision: ● available out of the box, ◐ partial, ○ roadmap / not available; never two ● with a colour as the only difference.
- Feature wording is the spec's; do not "improve" names here — one word for one thing across all artifacts.
- The four-axis specificity tag (customer / engine / use case / industry) is not printed, but a feature tagged `customer` and marked ● must be questioned before printing: it is usually ◐ with customization.
- No pricing, no tiers table, no proof figures in this document.

## Definition of done

The docx built from the spec on one A4 page, lint clean, counts matching, the review pack shown, the owner's approval recorded in `packs/<slug>/decisions.md`.

## Showing it to the owner

Everything the owner reviews is opened beside the conversation *before* the question is asked — the owner answers while looking at the thing, never at a description of it (`shared/references/review-loop.md` §3). In the Claude desktop app: the page render (the PNG from QuickLook, or the PDF when Pages exported one) opens in the side panel with the file-send tool (`SendUserFile`, `display: "render"`), with the .docx attached alongside (`display: "attach"`); then the widget. Never publish the feature list as a claude.ai artifact — it is internal material and would leave the machine. In a plain terminal with no panes, print the path and the plain-text table, and say so.

## Self-check before closing

- [ ] The feature list is one A4 page (estimated and, where Pages is available, verified); header is the mini-site lockup; fonts Azurio / Replica LL TT; top block = approved one-liner + who it is for.
- [ ] No page footer; at most three footnotes, each the caveat alone in 15 words or fewer; the three status glyphs render at the same size.
- [ ] Every message, question, option and table the owner saw passes the reader's test: no method codes, no file or key names, no packaging vocabulary as vocabulary, reasons instead of rule names.
- [ ] Everything the owner reviewed was opened beside the conversation before the question was asked.
