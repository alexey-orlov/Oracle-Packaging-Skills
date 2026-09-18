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
3. Read `shared/references/review-loop.md` and `shared/references/naming-and-clearance.md`. 

## The order and the pauses

Ask once, with a widget, which artifacts to build now (default: all six in this order) and for which channel the print artifacts are cut (default: `partner_print`; `internal` produces the internal variant with prices and named accounts where the spec allows):

1. **Feature list** → `/oracle-packs:feature-list`
2. **Sales deck** → `/oracle-packs:deck`
3. **Sales one-pager** → `/oracle-packs:one-pager` (condensed from the deck; built after it on purpose)
4. **Executive summary** → `/oracle-packs:exec-summary`
5. **Mini-site listing** → `/oracle-packs-web:listing` (the web plugin; tell the user to run it if the plugin is not installed)
6. **Interactive demo** → `/oracle-packs-web:demo` (asks for sources first)

After each artifact: show the review pack the artifact skill produced (renders or the file, a TLDR of decisions, the list of anything synthetic or unconfirmed, the open items), then one widget: **Approve and continue · Rebuild with changes (free text) · Stop here**. On "Rebuild", pass the free text to the artifact skill's fast path and re-present. Never start the next artifact before the current one is approved; the owner's feedback on the deck changes the one-pager.

## Consistency gate (after the last document artifact)

Run `python3 shared/tools/check_consistency.py <spec> <every produced file>`, then `lint_artifact.py` **once per artifact, on that artifact's own channel** — feature list and executive summary are `internal`, sales deck and one-pager are `partner_print` (the listing is `customer_site` and the walkthrough `demo`, in the web plugin). Do not lint the whole output directory on one channel: it reports the internal cut's own name variant as a partner-print finding and hides nothing real. All of them must be clean before the web handoff. A ✗ in the consistency matrix is fixed in the artifact, never by editing the spec silently; if the spec is what is wrong, say so and send the user to the spec skill's fast path.

## Delivery

Copy the approved files to the delivery folder the user names (ask once; the owner's convention is the pack's own folder on the practice's shared drive, next to the earlier artifacts), keeping the pack's file-name pattern `<Pack name> - <Artifact> - Oracle.<ext>`. Append one line per artifact to `packs/<slug>/decisions.md` (date, channel, file, what changed on review). Close with: the files and where they are, what was decided differently from the spec and why, and the open items the owner still holds.

## Self-check before closing

- [ ] Spec confirmed and lint-clean before the first build.
- [ ] Every artifact approved through a widget; no artifact built ahead of the previous approval.
- [ ] Consistency matrix and artifact lint clean for the delivered channel.
- [ ] Nothing internal-only in a partner or customer cut (contract values, named accounts, capacity numbers).
- [ ] Delivery paths and decisions logged.
