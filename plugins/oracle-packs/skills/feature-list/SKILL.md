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

1. **Read the spec**, not the delivered artifacts. Title = `meta.name` + " — Feature list"; definition line = `one_liner.full`; rows = `capabilities[]` in spec order.
2. **Build**: `python3 tools/build_feature_list.py <spec> --out <dir>` (paths relative to this skill's folder; resolve via `${CLAUDE_PLUGIN_ROOT}`). Columns: Area · Category · Feature · Status (● ◐ ○) · Tier first available · Standard customization scope (the scope column stays last, as in the reference). Merge Area and Category cells like the reference. Legend and the generated date plus `meta.spec_version` in the footer.
3. **Check**: every feature has a status; no area without a customization line; no price, no customer name (`python3 shared/tools/lint_artifact.py <file> --channel internal --spec <spec>`); counts per area match the spec. The feature list is the **internal** cut — it is the pack's internal/partner spine document, and `internal` is the channel the tools README and `/oracle-packs:build` use for it. When a copy goes to an Oracle seller as-is, lint it again on `partner_print` and expect the channel's name variant (sentence case) to be the only difference.
4. **Review pack** for the owner: the docx, a plain-text rendering of the table (so it can be read in chat), and, per area, how many capabilities are available, partial and on the roadmap — in those words, not as a count of glyphs. Then any feature whose status came from research rather than from what we actually built: name it and say so plainly, and let them confirm it or move it to the roadmap.
5. **One rebuild round** on feedback; a single-row change is a fast path (edit the spec through `/oracle-packs:spec` fast path, rebuild, re-lint).

## Rules

- Statuses follow the owner's decision: ● available out of the box, ◐ partial, ○ roadmap / not available; never two ● with a colour as the only difference.
- Feature wording is the spec's; do not "improve" names here — one word for one thing across all artifacts.
- The four-axis specificity tag (customer / engine / use case / industry) is not printed, but a feature tagged `customer` and marked ● must be questioned before printing: it is usually ◐ with customization.
- No pricing, no tiers table, no proof figures in this document.

## Definition of done

The docx built from the spec, lint clean, counts matching, the review pack shown, the owner's approval recorded in `packs/<slug>/decisions.md`.

## Self-check before closing

- [ ] Every message, question, option and table the owner saw passes the reader's test: no method codes, no file or key names, no packaging vocabulary as vocabulary, reasons instead of rule names.
