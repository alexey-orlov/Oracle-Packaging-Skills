---
name: one-pager
description: Build the accelerator pack's sales one-pager (HTML rendered to exactly one A4 PDF) from a confirmed pack spec — the deck condensed: hero with name and one-liner, problem ↔ solution with the data-flow line, why it sells for the partner's seller, verticals, the proof strip with its caveat, the service-packages table with the capability matrix, CTA and contact. Use on /oracle-packs:one-pager <pack-spec.yaml>, "make the one-pager for <pack>", "the sales one-pager overflows, fix it", or as step 3 of /oracle-packs:build.
disable-model-invocation: false
user-invocable: true
---

# /oracle-packs:one-pager — one A4 page, always

> **Paths.** `shared/...` means `${CLAUDE_PLUGIN_ROOT}/shared/...` (each plugin carries a synced copy of the repo's `shared/` folder); `tools/...`, `assets/...` and `references/...` without a prefix are relative to this skill's own folder. In a plain-copy install the plugin folder sits at `.claude/skills/<plugin>/` and `${CLAUDE_PLUGIN_ROOT}` resolves to it.


## Preconditions and inputs

- A confirmed, lint-clean `pack-spec.yaml`; the sales deck approved first when running the full build (the one-pager condenses it; the owner's deck feedback applies here).
- Channel `partner_print` (default) or `internal` — asked, when it has to be asked, as "who will see this one-pager": "Oracle and SoftServe sellers" or "our own team" (which adds prices in full and named accounts). Store the two values; never show them. Optional `--hero <image>`: an approved image from the owner; the template hides the hero when none is given. Never fetch imagery from the web.
- Read `shared/references/pack-anatomy.md`, this skill's `references/one-pager-anatomy.md` (section order and word budgets measured from the reference), `shared/references/client-documents.md`, `shared/references/slide-design.md` (rule 9, compositional variety, is one-pager feedback), `shared/references/naming-and-clearance.md`, `shared/references/talking-to-the-owner.md` — every message, question and option the owner sees passes its reader's test.
- Dependencies: Python 3 with `pyyaml` and `pypdf`; a headless Chrome or Chromium for the PDF (`CHROME_BIN`, else the macOS default, else on PATH). Say what is missing instead of degrading silently.

## Procedure

1. **Read the spec.** Content per block comes from named keys; the anatomy file says which. Cut by design what the partner already knows: no technology-stack section, no full feature matrix — the capability rows in the packages table are the summary.
2. **Build**: `python3 tools/build_one_pager.py <spec> --out <dir> --channel <channel> [--hero <image>]`. The tool renders the HTML and prints to PDF; it fails when the PDF has more than one page and names the longest blocks.
3. **Overflow means cuts, not smaller type.** Propose the cuts to the owner as a widget, using the word budgets to work out the ask but putting it to them in plain words: which block on the page — named as they would name it ("the problem paragraph", "the packages table") — and roughly how many words it has to lose, with what each cut costs. Apply the wording through the spec skill's fast path so every artifact stays consistent; rebuild.
4. **Lint and consistency**: `lint_artifact.py <pdf and html> --channel <channel> --spec <spec>`, `check_consistency.py <spec> <html>`.
5. **Editorial pass on the strongest model**: de-AI the typography and vocabulary (no em-dashes, no arrows in prose, "customers" not "users"), third person, no internal framings, no internal reference pricing, every figure caveated, the summary altitude reads as the whole offering, the pack name variant and subheading per channel.
6. **Review pack**: the PDF page as an image, the HTML, which blocks are at or over length and by how much (in plain words, by the block's name on the page), anything inferred, open items. One rebuild round; a single-block change is the fast path.

## Rules that bite on one-pagers

- The one-pager is the deck condensed, never a second source of truth: a price, a duration or a figure here equals the spec, to the character.
- The proof strip states its status once ("proof of value" / "proven"), carries the caveat, and names the customer only where the channel allows; otherwise the anonymized descriptor.
- The packages table shows three tiers named from the spec, the capability rows with ◐ ● ●● cells, prices with status and footnote; the infrastructure row says "indicative" when the spec does.
- "Why it sells" is written for the partner's seller, in one card; it never appears on customer-facing artifacts.
- CTA + the channel's contact from the spec; an address is a link, never a filled button.
- Deliver the PDF and the HTML twin (editable), under `<Pack name> - Sales one-pager - Oracle.pdf/.html`.

## Definition of done

One page, lint and consistency clean, editorial pass done, review pack shown, approval logged in `packs/<slug>/decisions.md`.

## Self-check before closing

- [ ] Every message, question, option and table the owner saw passes the reader's test: no method codes, no file or key names, no packaging vocabulary as vocabulary, reasons instead of rule names.
