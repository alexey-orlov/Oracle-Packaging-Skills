---
name: exec-summary
description: Build the accelerator pack's executive summary — one slide in the style of the host deck (the internal solutions-review deck by default) from a confirmed pack spec: name, one-liner, problem → solution, solution layers, proof strip with caveat, the three tiers in one strip, planned next steps. Use on /oracle-packs:exec-summary <pack-spec.yaml> [--host-deck <pptx>], "one slide on <pack> for the AI Days deck", "exec summary slide", or as step 4 of /oracle-packs:build.
disable-model-invocation: false
user-invocable: true
---

# /oracle-packs:exec-summary — one slide that stands alone

> **Paths.** `shared/...` means `${CLAUDE_PLUGIN_ROOT}/shared/...` (each plugin carries a synced copy of the repo's `shared/` folder); `tools/...`, `assets/...` and `references/...` without a prefix are relative to this skill's own folder. In a plain-copy install the plugin folder sits at `.claude/skills/<plugin>/` and `${CLAUDE_PLUGIN_ROOT}` resolves to it.


## Preconditions and inputs

- A confirmed, lint-clean `pack-spec.yaml`.
- Channel: `internal` by default (the slide usually lands in an internal solutions-review or section deck; the pack name variant is the internal one, e.g. "Workforce Optimization App"); `partner_print` when the slide goes into a partner deck (external name variant, clearance rules apply). When you have to ask, ask it as "who will see this slide": "our own team" or "Oracle and SoftServe sellers" — store the two values, never show them.
- Optional `--host-deck <pptx>`: build on that deck's master so the slide pastes in unchanged and renumbers itself; otherwise build on the shipped brand base.
- Read this skill's `references/exec-summary-anatomy.md` (measured from the latest section-slides deck — the owner named it the reference), `shared/references/slide-design.md`, `shared/references/naming-and-clearance.md`, `shared/references/talking-to-the-owner.md` — every message, question and option the owner sees passes its reader's test.
- Dependencies as for the deck skill (`pyyaml`, `python-pptx`, `Pillow`).

## Procedure

1. **Read the spec.** The slide compresses the deck: one line per component, the solution-layers ladder, the proof strip with the one metric set and the caveat, the tiers strip with durations and price status, planned next steps from `open_questions` and the tiers.
2. **Build**: `python3 tools/build_exec_summary.py <spec> --out <dir> --fit-report [--channel internal|partner_print] [--host-deck <pptx>]`. The fit report must be clean; overflow is cut, not shrunk (`--allow-overflow` exists for review builds only and is never how a slide ships).
3. **Render and look** (the deck skill's render probe), then lint and consistency checks.
4. **Editorial pass on the strongest model**: the slide must read for someone who has not seen the deck; every number equals the spec; the status word appears once; internal-only facts (contract values, named accounts) appear only on an `internal` cut and are marked strippable.
5. **Review pack** and one rebuild round — the pack in the owner's words: the rendered slide, what was compressed and what was dropped to make it fit, anything inferred, and the open items.

## Rules

- One slide, plus the host's closing slide only when asked.
- The internal cut may carry package prices and named accounts where the spec allows; mark the slide "internal — strip prices before external use" in the notes.
- No new visual language: use the host deck's own shapes and colours; reuse the deck's existing diagram rather than inventing one.
- Deliver as a standalone pptx named `<Pack name> - Executive summary - Oracle.pptx`, and, when a host deck was given, also the slide number where it should be inserted.

## Definition of done

Built on the right master, fit and lint clean, consistent with the spec, review pack shown, approval logged.

## Self-check before closing

- [ ] Every message, question, option and table the owner saw passes the reader's test: no method codes, no file or key names, no packaging vocabulary as vocabulary, reasons instead of rule names.
