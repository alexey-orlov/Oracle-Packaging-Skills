---
name: one-pager
description: Build the accelerator pack's sales one-pager (HTML rendered to exactly one A4 PDF) from a confirmed pack spec — the deck condensed: hero with name and one-liner, problem ↔ solution with the data-flow line, why it sells for the partner's seller, verticals, the proof strip with its caveat, the service-packages table with the capability matrix, CTA and contact. Use on /oracle-packs:one-pager <pack-spec.md>, "make the one-pager for <pack>", "the sales one-pager overflows, fix it", or as step 3 of /oracle-packs:build.
disable-model-invocation: false
user-invocable: true
---

# /oracle-packs:one-pager — one A4 page, always

> **Paths.** `shared/...` means `${CLAUDE_PLUGIN_ROOT}/shared/...`; `tools/...`, `assets/...` and `references/...` are this skill's own folder.

**Load only what the step needs.** `references/cards/manifest.yaml` lists, per step, exactly which files that step reads. Read those and nothing else — never the whole folder, never a card for a step you are not on, never a long reference a card already points to. Each card says what its part is, the checks a build must pass, and the spec keys it reads; the checks are the specification, not prose to paraphrase.

## Preconditions

- A confirmed, lint-clean `pack-spec.md`. In the full build, the sales deck is approved first: this page condenses it, and the owner's deck feedback applies here.
- Channel `partner_print` (default) or `internal`. When it has to be asked, ask it as "who will see this one-pager": "Oracle and SoftServe sellers", or "our own team" (which carries prices in full and named accounts). Store the two values; never show them.
- Optional `--hero <image>`: an approved image from the owner. Without it the hero renders with no photo. Never fetch imagery from the web.
- Dependencies: Python 3 with `pyyaml` and `pypdf` (`shared/tools/py --check`), and headless Chrome or Chromium for the PDF (`CHROME_BIN`, then the macOS or Windows default, then PATH). Say what is missing instead of degrading silently.

## Procedure

1. **Build.** Card: `build`, plus `shared/references/anatomy/artifact-one-pager.md` for the section order. Read the spec, settle the channel, then (`<dir>` is the pack's `artifacts` folder from `shared/tools/pack_paths.py <slug>` — never the repo):
   `shared/tools/py tools/build_one_pager.py <spec> --out <dir> --channel <channel> [--hero <image>]`
   The tool renders the HTML, prints it to PDF and fails when the result is more than one page, naming the longest blocks.
2. **Overflow.** Card: `overflow`. Only when the build exits 3. Overflow means cuts, not smaller type: put the cuts to the owner in plain words, by the block's name on the page, and apply the agreed wording through the spec skill's fast path so every artifact stays consistent. Rebuild.
3. **The automatic checks.** Card: `check`.
   `shared/tools/py shared/tools/lint_artifact.py <the pdf and the html> --channel <channel> --spec <spec>`
   `shared/tools/py shared/tools/check_consistency.py <spec> <the html>`
   `shared/tools/py shared/tools/check_diagram.py packs/<slug>/architecture.json --one-pager <the html>`
   All clean before anything is shown; the owner hears one plain line about them.
4. **Editorial pass.** Card: `editorial`, on the strongest model with fresh eyes — the de-AI read of typography, voice, figures and altitude, per `shared/references/client-documents.md`. Every subagent follows `shared/references/running-agents.md`.
5. **Show it.** Card: `review-pack`. One rebuild round.
6. **One change afterwards.** Card: `fast-path`. A single-block change is never a rerun of the flow.

## Rules that bite on one-pagers

- The page is the deck condensed, never a second source of truth: a price, a duration or a figure here equals the spec, to the character.
- The architecture strip renders the pack's one model (`packs/<slug>/architecture.json`), reviewed once in the build step — its composition is the reference the deck and the mini-site follow, it carries every system and edge label the deck does, and it is never drawn here from the brief.
- The proof strip states its status once, carries its caveat, and names the customer only where the channel allows; otherwise the anonymized descriptor.
- The packages table shows three tiers named from the spec, the capability rows with their marks, and prices with status and footnote; the infrastructure row says "indicative" when the spec does.
- "Why it sells" is written for the partner's seller, in one card, and appears on no customer-facing artifact.
- The closing block carries the channel's contact; an address is a link, never a filled button.
- Deliver the PDF and the editable HTML twin: `<Pack name> - Sales one-pager - Oracle.pdf` and `.html`.

## Talking to the owner

Every message, question and option passes the reader's test in `${CLAUDE_PLUGIN_ROOT}/skills/spec/references/cards/owner-language.md`, loaded at start-up.

## Showing it to the owner

Everything the owner reviews is open beside the conversation *before* the question, so they answer while looking at the thing (`shared/references/review-loop.md` §3). Here: the PDF page opens in the side panel (`SendUserFile`, `display: "render"`) with the HTML twin attached, then the question. Internal pack material is never published as a claude.ai artifact. In a plain terminal, print the path and a text rendering, and say so.

## Self-check before closing

- [ ] One A4 page, from the tool, not from an estimate.
- [ ] All three checkers exit 0 on this artifact's own channel and files.
- [ ] Every figure, price and duration matches the spec to the character.
- [ ] Nothing the owner saw carries a rule code, file name, spec key or packaging vocabulary.
- [ ] The render was open beside the conversation before the question was asked.
- [ ] Any wording change went into the spec, not into the built file.
- [ ] The decision is logged in `<work>/decisions.md`.
