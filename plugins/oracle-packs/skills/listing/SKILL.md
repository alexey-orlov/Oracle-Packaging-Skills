---
name: listing
description: Produce the accelerator pack's product listing for the practice mini-site from a confirmed pack spec — a checker-clean `products[]` entry (overview with problem ↔ solution, workflow steps, vertical cases, metrics with qualifiers; technology with the architecture stack and required/optional flags and the capabilities-by-stage view derived from the feature list; the Jumpstart tab with only the PoV price), inserted into the site's content file and previewed at every width. Use on /oracle-packs:listing <pack-spec.md> --site <mini-site root>, "add <pack> to the mini-site", "update the <pack> product page", or as step 5 of /oracle-packs:build.
disable-model-invocation: false
user-invocable: true
---

# /oracle-packs:listing — the customer-facing product page

> **Paths.** `shared/...` means `${CLAUDE_PLUGIN_ROOT}/shared/...`; `tools/...`, `assets/...` and `references/...` are this skill's own folder.

**Load only what the step needs.** Each step below names its cards (`Card:`); read those when you reach it and nothing else — never the whole folder, never a card for a step you are not on, never a long reference a card already points to.

**Start-up:** `shared/cards/owner-language.md` (how every message to the owner is written) and `shared/cards/review-protocol.md` (how everything the owner reviews is shown, changed and approved).

The listing is the only artifact end customers read directly. It carries the same components as the print artifacts, in the site's own grammar: persona-first copy, no packaging vocabulary, no counts, no customer names, only the proof-of-value price, one status word per proof.

## Preconditions

- A confirmed, lint-clean `pack-spec.md` (`shared/tools/py shared/tools/lint_spec.py`). A required key the spec does not hold sends the user back to the spec skill; the gap is never filled here.
- **The mini-site** (card: `site`): `--site <path>`, else `$ORACLE_SITE_ROOT`, else the session's own folder when it holds `site.manifest.json`, else ask; **never guess it**. The root must hold `site.manifest.json`: the site's own description of its paths, checker, preview and publish targets. Where the site and these cards differ, the site wins.
- **Write every string in sentence case.** The live theme sets display type in sentence case and uppercases only micro-type slots in CSS, so a stored capital is a shout that cannot be undone. `site/data/content-case.js` re-cases pre-rebrand strings only: it is a one-time migration and **gets no new rows**.
- Node 14+ for the checker and the inserter, Python 3 for the derivation tool and the deny-list converter (`shared/tools/py --check`). State what is missing rather than starting and failing halfway.

## The procedure

1. **Read the site.** Card: `site`. Find the root, pull it, read its manifest, and compare its contract round with this skill's before anything is written.
2. **Map the tile and the overview tab.** Cards: `layout`, `entry-identity`, `entry-overview`, `entry-case-study`. Fill every key from the spec; a slot with no fact behind it is filled qualitatively, never omitted.
3. **Map the technology and Jumpstart tabs.** Cards: `entry-technology`, `entry-jumpstart`. The stage view is derived, not re-typed: `shared/tools/py tools/derive-stage-view.py <spec>`.
4. **Write the copy** on the strongest model, then give it a mechanical pass. Cards: `copy-rules`, `claim-rules`, `exemplar-altitude`. The exemplar entry is long: a fresh-context agent reads it and returns the strings, or you open only the keys you are filling. Agents read: `assets/exemplar-product-entry.js`, `shared/references/naming-and-clearance.md`. Every subagent follows `shared/references/running-agents.md`.
5. **Insert.** Cards: `insert`, `switches`, `shared/references/architecture-diagram.md`. `node tools/insert-product.mjs --content <site>/<paths.content> --entry <entry file> --figure-alt "<the figure in one sentence>"` (the product page finds its figure through that `media` entry), then the figure and the switch block at the manifest's `paths.diagrams` and `paths.config`, then the kit-links entry at `paths.links` (the tool's `--links`), then run the manifest's `paths.syncLinks` from the site root. The figure is **generated from the pack's architecture model, never written by hand** — `shared/tools/py tools/diagram_to_site.py <spec> --slug <slug>`, the model built from the spec in the packaging-skills repo (`shared/tools/py shared/tools/pack_paths.py <slug>` prints its path) — so the site, the deck and the one-pager draw one picture.
6. **Gates.** Cards: `gates`, `claim-rules`. `shared/tools/py tools/denylist-to-json.py --out <site>/<paths.denyList>` **first** — the customer-name gate fails open, so an unconfigured deny-list warning is a failed gate. Then the site's own checker (the manifest's `checker.run`, from the site root), a clean console on every route, the deny-list sweep, `shared/tools/py shared/tools/lint_artifact.py <entry file> --channel customer_site --spec <spec>`, and `check_consistency.py <spec> <entry file>`. The owner hears one plain line about all of it.
7. **Preview.** Card: `preview`. Every changed screen at the manifest's `preview.widths`, the H1 at `preview.h1Width`, no horizontal overflow.
8. **Review pack.** Card: `review-pack`. The screenshots open in the side panel, the entry as text in the conversation. One rebuild round.
9. **Publish only when asked.** Card: `publish`. The target and every other publish value come from the site manifest's `publish` block, never from memory.

**Fast path.** When the owner asks for one thing ("re-word the one-liner", "swap an industry"), load that part's card only, redo it, re-run the gates, and stop.

## Done, and the self-check

Done = entry inserted, three gates green, consistency clean, preview screenshots reviewed, approval logged in `<work>/decisions.md` (the local work folder `pack_paths.py` prints), publish only on the owner's word.

- [ ] The site was read first (manifest, git state, contract round), and where it is newer than this skill its rules were followed.
- [ ] Every claim maps to a spec line carrying a `source`; an unsupported clause was dropped, not swapped.
- [ ] No ceiling, total, denominator or negation anywhere; no sentence whose subject is an absence.
- [ ] Only the proof-of-value price is on the page, with its footnote; one duration everywhere.
- [ ] No customer name or logo in copy, alt text, captions, file names or anything under the publish root.
- [ ] The stage view was derived from the feature list, and drops features rather than adding any.
- [ ] The architecture figure was generated from the pack's model, and `check_diagram.py` says the site still draws it.
- [ ] The kit-links entry exists in the site's `links.json` with all six keys and `links.js` is current (`paths.syncLinks`).
- [ ] Every heading is inside its budget on the rendered page at 375 px.
- [ ] The open items were listed for the owner, not resolved by the builder.
- [ ] Everything the owner reviewed was open beside the conversation before the question was asked.
