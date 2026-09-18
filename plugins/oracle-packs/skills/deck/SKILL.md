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
- Channel: `partner_print` (default; Oracle and SoftServe sellers) or `internal` (adds prices in full, named accounts and internal notes where the spec's clearance allows). Ask once with a widget if not given.
- Read `shared/references/pack-anatomy.md`, this skill's `references/deck-anatomy.md` and `references/brand-tokens.md`, `shared/references/slide-design.md` (all rules), `shared/references/naming-and-clearance.md`, `shared/references/review-loop.md`.
- Dependencies: Python 3 with `pyyaml`, `python-pptx`, `Pillow`; the brand base `assets/softserve-deck-base.pptx` ships with the skill. Brand fonts are licensed and may be absent on this machine: the fit report uses metric stand-ins, so trust the report, not the rendered glyph widths.

## Procedure

1. **Read the spec** and the anatomy. Every slide's content comes from named spec keys (the anatomy file lists them); if a key is empty, the slide shows the honest state ("results to follow", "scoped per engagement") — never a placeholder that reads as fact.
2. **Build**: `python3 tools/build_deck.py <spec> --out <dir> --channel <channel> --fit-report`. The fit report must be clean; an overflow is fixed by shortening the spec wording through the spec skill's fast path or by the anatomy's fallback layout, never by shrinking type below the token minimum.
3. **Render QA**: run `tools/render_probe.sh` to see which renderer this machine has, render a contact sheet, and look at every slide: peers equal geometry, no free-floating text, colour semantics per the rules, no empty containers pretending to be content.
4. **Lint**: `python3 shared/tools/lint_artifact.py <pptx> --channel <channel> --spec <spec>` and `python3 shared/tools/check_consistency.py <spec> <pptx>`.
5. **Editorial pass on the strongest model**: read every slide's text against the spec and the naming rules — prices match the spec, "proof of value" vs "proven" wording, tier names, the pack name variant for the channel, the integration claim states its tier, vendor names by catalog. This pass has caught a price slip and an overclaim on every previous deck; do not skip it.
6. **Review pack**: the contact sheet, the pptx, a TLDR of layout decisions, the list of anything inferred or unconfirmed, and the open items. Then one rebuild round. The builder writes the whole deck from the spec every time — there is no per-slide flag — so a single-slide change is a single-line change in the spec (through `/oracle-packs:spec`'s fast path) followed by the same `build_deck.py` call, and only the changed slide is re-reviewed.

## Rules that bite on decks

- Ten slides, the anatomy's order; packs differ in content, never in anatomy.
- The proof slide carries the one metric set with the channel's attribution and the caveat line; peer claims all-or-none (no "pending" next to a proven peer).
- Solution-layers ladder: partner layer on top, official logo images where the assets exist, layers differing in weight and shape, not tint alone.
- "Why it sells for the partner's seller" is its own slide: cross-sell path, net-new OCI consumption, repeatability; target consumption only when the spec has it.
- Deliver as a standalone pptx on the base's master. A section that has to paste into someone else's deck is the executive-summary skill's job, which does take `--host-deck <pptx>` and builds on that deck's master.
- Customer logo only when `clearance.customer_name_allowed[channel]` is true.

## Definition of done

Fit report clean, contact sheet reviewed, lint and consistency clean, editorial pass done, the owner's approval recorded in `packs/<slug>/decisions.md`, file delivered under `<Pack name> - Sales deck - Oracle.pptx`.
