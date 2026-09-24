---
name: build
description: Build the full artifact set for a confirmed accelerator-pack spec, sequentially with a review pause after each artifact — feature list, sales deck, sales one-pager, executive summary — then hand off to the web plugin for the mini-site listing and the interactive demo. Use on /oracle-packs:build <pack-spec.md>, "build all the artifacts for <pack>", "produce the pack collateral", or after /oracle-packs:spec confirms a brief. Refuses to start on an unconfirmed spec.
disable-model-invocation: false
user-invocable: true
---

# /oracle-packs:build — all artifacts, in order, one review at a time

> **Paths.** `shared/...` means `${CLAUDE_PLUGIN_ROOT}/shared/...` (each plugin carries a synced copy of the bundle's `shared/`); `references/...` and `tools/...` are this skill's own folder.

**Load only what the step needs.** `references/cards/manifest.yaml` lists, per step, exactly which files that step reads. Read those and nothing else — never the whole folder, never a card for a step you are not on, never a long reference a card already points to.

You produce nothing yourself: each artifact is built by its own skill, shown to the owner, and approved before the next one starts.

## Preconditions

1. Argument: the spec, `packs/<slug>/pack-spec.md`, or the pack's slug. `shared/tools/py shared/tools/pack_paths.py <slug> --create` prints the repo, `<work>` and the `artifacts` folder; with no argument, list the repo's `packs/*/` and ask which. `git -C <repo> pull --ff-only` first — a pull that cannot run is deferred and retried, never skipped silently — then build from the repo's spec, never from a copy.
2. `meta.status` must be `confirmed` and `shared/tools/py shared/tools/lint_spec.py <spec>` must be clean. Otherwise stop and send the user to `/oracle-packs:spec` (resume mode) — never patch the spec here.
3. Who will see the printed documents is settled once, at the map, and holds for every artifact and for the consistency gate.

## 1. The map, and the one question

Cards: `plan-and-ask`, `artifact-order`. Read `<work>/intake.md` before asking anything: stage 1 already settled which artifacts the owner wants and, often, who will see the printed documents. A machine that did not run the spec has no intake; then the map asks. Send one short message with the map in the owner's words — the artifacts by name, in order, each reviewed before the next; where they will land; and the audience the printed documents are cut for. Only where the intake is silent, ask once, in a single widget call.

## 2. Build, and the review after each artifact

Card: `per-artifact-review` (with `artifact-order` for what comes next). Run each artifact's own skill in the fixed order — feature list, pictures, sales deck, sales one-pager, executive summary, then the web plugin's mini-site listing and interactive demo. After each one: show its review pack, open its render beside the conversation, then one widget — approve, rebuild with changes, or stop. Never start the next artifact before the current one is approved. Every artifact is written to the `artifacts` folder `pack_paths.py` printed (the skills' `--out`), never into the repo, and each approval is logged in `<work>/decisions.md` with the artifact's spec stamp (`shared/tools/py shared/tools/spec_stamp.py <file>` prints it).

## 3. The architecture picture

Card: `architecture-picture`. After the feature list and before the deck, once for the whole pack: build the model (`shared/tools/build_diagram.py`), render the one-pager's strip — the canonical picture — and put it to ONE fresh-context reviewer. Every subagent follows `shared/references/running-agents.md`. The deck, the one-pager and the mini-site listing then render that reviewed model; none of them reviews the picture again, and none draws its own. The reviewed model is shared: save it to the repo (the spec skill's card `save`, `<what>` = `architecture model`).

## 4. The consistency gate

Card: `consistency-gate`. After the last document artifact and before the web handoff: `check_consistency.py` across every produced file, then `lint_artifact.py` once per artifact on that artifact's own channel, then the sales deck's own shape check re-run on the approved file. All clean before the handoff. A file it reports as built from an earlier version of the spec — typically the feature list, once the pictures step has written into the spec — is rebuilt from the current spec first. The owner hears one plain line about it.

## 5. Delivery

Card: `delivery`. Copy the approved files from `<work>/artifacts/` to the folder the owner names, keeping the pack's file-name pattern. Log one line per artifact in `<work>/decisions.md`. Close with the files and where they are, what was decided differently from the pack brief and why, and the open items the owner still holds.

## Talking to the owner

Every message, question, option and table passes the reader's test in `${CLAUDE_PLUGIN_ROOT}/skills/spec/references/cards/owner-language.md` (the spec skill's card, read at start-up).

## Showing it to the owner

Everything the owner reviews opens beside the conversation *before* the question (`shared/references/review-loop.md` §3): a render in the side panel (`SendUserFile`, `display: "render"`) with the editable file attached (`display: "attach"`), a text file in the Files pane (`mcp__ccd_view__show_pane`, pane `file`). Internal pack material is never published as a claude.ai artifact — artifacts stay reserved for the mini-site demos. In a plain terminal, print the path and a text rendering, and say so. Here: before every `Artifacts · n of N` widget.

## Self-check before closing

- [ ] Spec confirmed and lint-clean before the first build.
- [ ] Nothing the intake already settled was asked again.
- [ ] Every artifact approved through a widget; no artifact built ahead of the previous approval.
- [ ] The architecture picture was built once, reviewed once by a fresh-context reviewer, and rendered by all three artifacts from that one model.
- [ ] Consistency matrix and per-artifact lint clean on each artifact's own channel, and the sales deck's own shape check clean.
- [ ] `check_diagram.py` clean: the deck, the one-pager and the site figure all draw the model.
- [ ] Nothing internal-only in a partner or customer cut (contract values, named accounts, capacity numbers).
- [ ] Delivery paths and decisions logged; file names follow `<Pack name> - <Artifact> - Oracle.<ext>`.
- [ ] Every artifact was written to the `artifacts` folder and each approval logged with its spec stamp; only the architecture model went into the repo.
- [ ] Every message, question, option and table the owner saw passed the reader's test.
- [ ] Everything the owner reviewed was opened beside the conversation before the question was asked.
