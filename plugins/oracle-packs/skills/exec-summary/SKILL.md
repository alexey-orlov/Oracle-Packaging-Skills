---
name: exec-summary
description: Build the accelerator pack's executive summary — one slide in the style of the host deck (the internal solutions-review deck by default) from a confirmed pack spec: name, one-liner, problem → solution, solution layers, proof strip with caveat, the three tiers in one strip, planned next steps. Use on /oracle-packs:exec-summary <pack-spec.md> [--host-deck <pptx>], "one slide on <pack> for the AI Days deck", "exec summary slide", or as step 4 of /oracle-packs:build.
disable-model-invocation: false
user-invocable: true
---

# /oracle-packs:exec-summary — one slide that stands alone

> **Paths.** `shared/...` means `${CLAUDE_PLUGIN_ROOT}/shared/...`; `tools/...`, `assets/...` and `references/...` are this skill's own folder.

**Load only what the step needs.** Each step below names its cards (`Card:`); read those when you reach it and nothing else — never the whole folder, never a card for a step you are not on, never a long reference a card already points to. Each card says what its part is, the checks a build must pass, and the spec keys it reads; the checks are the specification, not prose to paraphrase.

**Start-up:** `shared/cards/owner-language.md` (how every message to the owner is written) and `shared/cards/review-protocol.md` (how everything the owner reviews is shown, changed and approved).

## Preconditions

- A confirmed, lint-clean `pack-spec.md`.
- Channel: `internal` by default — the slide usually lands in an internal solutions-review or section deck and carries the internal name variant; `partner_print` when it goes into a partner deck, where the external variant and the clearance rules apply. When it has to be asked, ask it as "who will see this slide": "our own team", or "Oracle and SoftServe sellers". Store the two values; never show them.
- Optional `--host-deck <pptx>`: build on that deck's own master, so the slide pastes in unchanged and renumbers itself. Without it, the shipped brand base.
- Dependencies as for the deck skill: `pyyaml`, `python-pptx`, `Pillow` (`shared/tools/py --check`). Say what is missing instead of degrading silently.

## Procedure

1. **Build.** Cards: `build` and `blocks`, plus `shared/references/anatomy/artifact-exec-summary.md` for the six blocks. Read the spec, settle the channel, then (`<dir>` is the pack's `artifacts` folder from `shared/tools/pack_paths.py <slug>` — never the repo):
   `shared/tools/py tools/build_exec_summary.py <spec> --out <dir> --fit-report [--channel internal|partner_print] [--host-deck <pptx>]`
   The fit report must be clean; overflow is cut, not shrunk (`--allow-overflow` is for review builds and is never how a slide ships).
2. **The automatic checks.** Card: `check`. Render the slide and look at it (`../deck/tools/render_probe.sh` prints how), then:
   `shared/tools/py shared/tools/lint_artifact.py <the pptx> --channel <channel> --spec <spec>`
   `shared/tools/py shared/tools/check_consistency.py <spec> <the pptx>`
   Both clean before anything is shown; the owner hears one plain line about them.
3. **Editorial pass.** Card: `editorial`, on the strongest model with fresh eyes — the slide must read for someone who has not seen the deck, every number equal to the spec, the status word once, prices and the customer's name as the clearance table allows for this cut, the notes naming it. Every subagent follows `shared/references/running-agents.md`.
4. **Show it.** Card: `review-pack`. One rebuild round.
5. **One change afterwards.** Card: `fast-path`. A single-block change is never a rerun of the build.

## Rules that bite on this slide

- One slide, plus the host's closing slide only when asked.
- Prices and the customer's name follow the channel table in `shared/references/naming-and-clearance.md`, per cut: internal and partner cuts carry every tier's price, the partner cut each with its disclaimer; the notes name the cut and what it carries, so the slide never travels as another channel's cut. Naming is still not a licence to print internal operating numbers — headcount, contract values, internal costs.
- No new visual language: the host deck's own shapes and colours, and the deck's existing diagram rather than an invented one.
- The proof block is all or none; an absent component is drawn as an empty panel, never dropped and never half-filled.
- Deliver a standalone `<Pack name> - Executive summary - Oracle.pptx`, and, when a host deck was given, the slide number where it should be inserted.

## Self-check before closing

- [ ] The fit report exits 0, and the render was actually looked at.
- [ ] Built on the right master — `--host-deck` whenever the slide has a destination deck.
- [ ] Both checkers exit 0 on this artifact's own channel and file.
- [ ] Every figure, price and duration matches the spec to the character.
- [ ] Nothing the owner saw carries a rule code, file name, spec key or packaging vocabulary.
- [ ] The render was open beside the conversation before the question was asked.
- [ ] Any wording change went into the spec, not into the .pptx.
- [ ] The decision is logged in `<work>/decisions.md`.
