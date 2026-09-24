---
name: feature-list
description: Build the accelerator pack's feature list (.docx) from a confirmed pack spec — the Area > Category > Feature matrix with ● available / ◐ partial / ○ roadmap status and the standard customization scope per capability, no pricing. Use on /oracle-packs:feature-list <pack-spec.yaml>, "make the feature list for <pack>", "regenerate the capability matrix", or as step 1 of /oracle-packs:build.
disable-model-invocation: false
user-invocable: true
---

# /oracle-packs:feature-list — the capability matrix

> **Paths.** `shared/...` means `${CLAUDE_PLUGIN_ROOT}/shared/...` (each plugin carries a synced copy of the bundle's `shared/`); `references/...`, `tools/...` and `assets/...` are this skill's own folder.

**Load only what the step needs.** `references/cards/manifest.yaml` lists, per step, exactly which files that step reads. Read those and nothing else — never the whole folder, never a card for a step you are not on, never a long reference a card already points to. Every subagent follows `shared/references/running-agents.md`.

The feature list is the pack's spine document: the table every other artifact condenses. It is internal / partner material, carries no prices, and states for every feature whether it is available, partial or roadmap and what is standardly customized per engagement.

## Preconditions

1. A confirmed, lint-clean `pack-spec.yaml` (`shared/tools/py shared/tools/lint_spec.py`). Otherwise stop and send the user to `/oracle-packs:spec`.
2. Dependencies: Python 3 with `pyyaml` and `python-docx` (`plugins/oracle-packs/requirements.txt`). Check with `shared/tools/py --check` and tell the user what to install if it fails; never install into system Python yourself.
3. This document is the `internal` cut. A copy going to an Oracle seller is linted again on `partner_print` (step 4).

## 1. Build

Cards: `build`, `statuses-and-wording`. Read the spec, not the delivered artifacts. Then `shared/tools/py tools/build_feature_list.py <spec> --out <dir>`, where `<dir>` is the pack's `artifacts` folder from `shared/tools/pack_paths.py <slug>` — never the repo. The build guarantees one A4 page by walking a fit ladder and, where Pages or LibreOffice is installed, verifying the real page count. Read the rung it printed, and pass on any `WARNING` line.

## 2. If it does not fit

Card: `does-not-fit`. **Exit 3 means nothing was written.** Do not retry with smaller type — 7pt is the floor. Put the grouping to the owner in plain words using the counts the build printed, fix the tree through `/oracle-packs:spec`, and rebuild.

## 3. Footnotes

Card: `footnotes`. Cut them before the document goes out: at most three, each 15 words or fewer, each a tier caveat and nothing else. The build warns on stderr when there are too many or one runs long; take those cuts to the owner, fix them in the spec, then build.

## 4. Check

Card: `check`. `shared/tools/py shared/tools/lint_artifact.py <file> --channel internal --spec <spec>`, plus: every feature has a status, no area without a customization line, counts per area match the spec.

## 5. The review pack

Card: `review-pack`. The docx, a plain-text rendering of the table, per-area availability in words, how the page came out, and any status that came from research rather than from what we built.

## 6. One rebuild round

Card: `fast-path`. One rebuild on feedback; a single-row change goes through the spec skill's fast path, rebuild, re-lint, stop.

## Talking to the owner

Every message, question, option and table passes the reader's test in `${CLAUDE_PLUGIN_ROOT}/skills/spec/references/cards/owner-language.md` (the spec skill's card, read at start-up).

## Showing it to the owner

Everything the owner reviews opens beside the conversation *before* the question (`shared/references/review-loop.md` §3): the page render — the PNG from QuickLook, or a PDF exported by Pages or LibreOffice — in the side panel (`SendUserFile`, `display: "render"`), with the .docx attached (`display: "attach"`). Never publish the feature list as a claude.ai artifact; it is internal material and would leave the machine. In a plain terminal, print the path and the plain-text table, and say so.

## Done, and the self-check

Done = the docx built from the spec on one A4 page, lint clean, counts matching, the review pack shown, the owner's approval recorded in `<work>/decisions.md`.

- [ ] One A4 page, estimated and — where Pages or LibreOffice is available — verified; header is the mini-site lockup (Azurio title, Replica LL TT body, both set by the build); top block = approved one-liner + who it is for.
- [ ] No page footer; at most three footnotes, each the caveat alone in 15 words or fewer.
- [ ] The three status glyphs render at the same size, and no two statuses share a glyph.
- [ ] Feature wording is the spec's; every `customer`-tagged feature marked ● was questioned.
- [ ] No pricing, no tiers table, no proof figures.
- [ ] Lint clean on `internal`; counts per area match the spec.
- [ ] Every message, question, option and table the owner saw passed the reader's test.
- [ ] Everything the owner reviewed was open beside the conversation before the question.
