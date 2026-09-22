---
name: listing
description: Produce the accelerator pack's product listing for the practice mini-site from a confirmed pack spec — a checker-clean `products[]` entry (overview with problem ↔ solution, workflow steps, vertical cases, metrics with qualifiers; technology with the architecture stack and required/optional flags and the capabilities-by-stage view derived from the feature list; the Jumpstart tab with only the PoV price; sellers' materials manifest), inserted into the site's content file and previewed at every width. Use on /oracle-packs-web:listing <pack-spec.yaml> --site <mini-site root>, "add <pack> to the mini-site", "update the <pack> product page", or as step 5 of /oracle-packs:build.
disable-model-invocation: false
user-invocable: true
---

# /oracle-packs-web:listing — the customer-facing product page

> **Paths.** `shared/...` means `${CLAUDE_PLUGIN_ROOT}/shared/...` (each plugin carries a synced copy of the repo's `shared/` folder); `tools/...`, `assets/...` and `references/...` without a prefix are relative to this skill's own folder. In a plain-copy install the plugin folder sits at `.claude/skills/<plugin>/` and `${CLAUDE_PLUGIN_ROOT}` resolves to it.


The listing is the only artifact end customers read directly. It carries the same components as the print artifacts but in the site's own grammar: persona-first copy, no packaging vocabulary, no counts, no customer names, only the PoV price, one status word per proof.

## Preconditions and inputs

- A confirmed, lint-clean `pack-spec.yaml` (`python3 shared/tools/lint_spec.py`).
- The mini-site repository root (`--site <path>`): it must contain `site/data/content.js`, `site/data/config.js`, `site/data/diagrams.js` and `tools/check-grammar.js`. Ask for the path if not given; never guess it.
- **Write every string in sentence case.** The site moved to SoftServe's current brand on 2026-09-18, where display type is sentence case and uppercase survives only as 12-16 px micro-type that the CSS uppercases itself (`.eyebrow`, `.hero-badges li`, chips, buttons). `content.js` still stores the *pre-rebrand* strings in CAPITALS, and `site/data/content-case.js` re-cases exactly those at load time. That overlay is a one-time migration: **do not add rows to it for a new product.** Store `headline.accent` / `headline.rest`, the problem and solution `title`s and `badges[]` in sentence case and both themes render correctly — the live one shows them as written, and the archived `index-legacy.html` uppercases the same slots in CSS.
- Node 14+ for the checker and the inserter, both dependency-free (`node --version`); Python 3 for the derivation tool and the deny-list converter. (The demo skill's capture script is the one that needs Node 22+.) State what is missing.
- Read this skill's `references/listing-schema.md` (the `products[]` keys and which spec component feeds each), `references/listing-rules.md` (the site's content, messaging and design rules as checkable statements), `references/preview-and-publish.md`, `shared/references/naming-and-clearance.md`, and `shared/references/talking-to-the-owner.md` — every message, question and option the owner sees passes its reader's test.
- Study `assets/exemplar-product-entry.js`: the shape and altitude of a finished entry. Match its altitude; do not copy its copy.

## Procedure

1. **Map the spec to the entry.** Fill every key from the spec: `name` = `meta.name_variants.site`; `oneLiner` / `shortLine` from `one_liner`; `overview.problemSolution` from component 1; `industryCases[]` from `verticals[]` (each with its own problem and solution line); `overview.steps[]` from `workflow.steps[]` (four to six steps, one frame each — frames come from the demo captures when the demo exists, otherwise the step ships without an image and the key stays empty); `overview.metrics[]` from `kpis[]` with the qualifier and the caveat in `metricsNote`; `technology.stack[]` from `architecture.stack` with `required` from `oracle_products[].role`; `technology.capabilities[]` = the stage view **derived** from `capabilities[]` via `python3 tools/derive-stage-view.py <spec>` (the feature list stays the master); `jumpstart` from `packages.tiers[pov]` only — the other tiers read "Scoped per engagement"; `caseStudy` anonymized unless `clearance.customer_name_allowed.customer_site` is true; `sellers.materials` from the artifacts that exist. `icp` is proposed as a new key when the schema has none — raise it with the owner in plain words ("who buys it has nowhere to live on the product page today; here is where I would put it") rather than hiding it in another field.
2. **Write the copy on the strongest model**, then give it a mechanical pass: heading budgets (H1 two to four words, H2 five or fewer), no content word three times on a screen, one word for one thing, no `&amp;`-style entities, retired vocabulary absent.
3. **Insert**: `node tools/insert-product.mjs --content <site>/site/data/content.js --entry <entry file>`; add the diagram block to `diagrams.js`; add the per-slug switches to `config.js` (demo and video switches empty until those exist).
4. **Gates, all three**: `python3 tools/denylist-to-json.py --out <site>/tools/deny-list.json` first — the checker's customer-name gate fails open, so an unconfigured deny-list is a warning and a pass, and the converter keeps it identical to `shared/tools/denylist.txt`. Then `node tools/check-grammar.js --site-root <site>` prints OK (and no `deny-list … no customer names configured` warning); the browser console is clean on the product route; `python3 shared/tools/lint_artifact.py <entry file> --channel customer_site --spec <spec>` is clean. Then `check_consistency.py <spec> <entry file>`. The owner hears one line about all of this: the automatic checks passed, or what one of them found, in plain words.
5. **Preview** per `references/preview-and-publish.md`: the local server, every changed screen at 1440 / 1280 / 1024 / 768 / 375, the H1 at 320, no horizontal overflow. Screenshots go in the review pack.
6. **Review pack**, in the owner's words: the screenshots, the entry as text, which parts were derived from the capability table and which were written fresh, anything the pack brief left open (a missing figure means the metric tile is left out, not faked), and the decisions about the site itself that only they can settle — where it sits in the site's filters, the availability badge, the category chip. One rebuild round.
7. **Publish only when asked**, with the site's own procedure (wrapper strip, files map, post-publish file list check); the artifact URL is the owner's input, never assumed.

## Rules that bite on listings

- Never state a ceiling, a total, a denominator or a negation; no "so far", "yet", "N of M".
- Prices: PoV only, with the disclaimer; no € on the services page.
- Status word once, in the chip; the footnote spends its line on evidence.
- Customer names and logos: absent unless cleared for the customer site; also absent from alt text, captions, file names and any file under the publish root.
- The tier names are PoV Jumpstart / Integration / Scaling; the Jumpstart tab sells one idea: pilot fast, low risk, tangible outputs.

## Definition of done

Entry inserted, three gates green, consistency clean, preview screenshots reviewed, approval logged in `packs/<slug>/decisions.md`, publish done only on the owner's word.

## Showing it to the owner

Everything the owner reviews is opened beside the conversation *before* the question is asked — the owner answers while looking at the thing, never at a description of it (`shared/references/review-loop.md` §3). In the Claude desktop app: a text file (the research summary, the pack brief, a spec) opens in the Files pane with the view-pane tool (`mcp__ccd_view__show_pane`, pane `file`, the path); a render (a page PNG, a PDF, an HTML page) opens in the side panel with the file-send tool (`SendUserFile`, `display: "render"`), with the editable file attached alongside (`display: "attach"`); then the widget. Never publish internal pack material as a claude.ai artifact — it leaves the machine; artifacts stay reserved for the mini-site demos. In a plain terminal with no panes, print the path and a text rendering, and say so. Here: the screenshots open in the side panel; the entry is shown as text in the conversation.

## Self-check before closing

- [ ] Every message, question, option and table the owner saw passes the reader's test: no method codes, no file or key names, no packaging vocabulary as vocabulary, reasons instead of rule names.
- [ ] Everything the owner reviewed was opened beside the conversation before the question was asked.
