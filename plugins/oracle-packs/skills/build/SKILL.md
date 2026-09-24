---
name: build
description: Build a confirmed accelerator pack's artifacts from its spec — the feature list (.docx capability matrix), the sales deck (10-slide .pptx), the sales one-pager (one A4 PDF with its HTML), the executive summary (one slide, on a host deck's master when given) — each checked and reviewed before the next, then the mini-site listing and the interactive demo. Use on /oracle-packs:build <pack> for the whole set, /oracle-packs:build <pack> <artifact> for one (feature-list, deck, one-pager, exec-summary), "make the sales deck for <pack>", "rebuild slide 8", "the one-pager overflows", "one slide on <pack> for the section deck", "regenerate the capability matrix", or after /oracle-packs:spec confirms a brief. Refuses to start on an unconfirmed spec.
disable-model-invocation: false
user-invocable: true
---

# /oracle-packs:build — the pack's artifacts, one review at a time

> **Paths.** `shared/...` means `${CLAUDE_PLUGIN_ROOT}/shared/...`; `references/...` and the artifact folders `feature-list/`, `deck/`, `one-pager/` and `exec-summary/` (each with its `tools/` and `assets/`) are this skill's own.

**Load only what the step needs.** Each step below names its cards (`Card:`); read those when you reach it and nothing else — never the whole folder, never a card for a step you are not on, never a long reference a card already points to. Every subagent follows `shared/references/running-agents.md`.

**Start-up:** `shared/cards/owner-language.md` (how every message to the owner is written) and `shared/cards/review-protocol.md` (how everything the owner reviews is shown, changed and approved).

Every artifact is built by its tool from the confirmed spec; you never draw or write one by hand. Each goes to the pack's `artifacts` folder, never the repo, and each is checked and approved before the next one starts.

## Preconditions

1. The argument is the spec (`packs/<slug>/pack-spec.md`) or the slug, optionally followed by one artifact. `shared/tools/py shared/tools/pack_paths.py <slug> --create` prints the repo, `<work>` and the `artifacts` folder (`<dir>` below); with no argument, list the repo's `packs/*/` and ask which. `git -C <repo> pull --ff-only` first — a pull that cannot run is deferred and retried, never skipped silently — then build from the repo's spec, never a copy.
2. `meta.status` is `confirmed` and `shared/tools/py shared/tools/lint_spec.py <spec>` is clean; otherwise stop and send the owner to `/oracle-packs:spec`. Never patch the spec here.
3. `shared/tools/py --check` shows the Python packages; the one-pager also needs Chrome or Chromium. Say what is missing instead of degrading silently.

## 1. The map, and the one question

Card: `plan-and-ask`. Read the brief's `build` settings first: the spec run usually settled which artifacts the owner wants and who will see the printed documents. One short message with the map, and a question only where the brief is silent. Who will see the printed documents is settled once, here, and holds for every artifact.

## 2. The feature list

Card: `feature-list`. Build it, pass on any warning, and read the rung the build printed.

Card for a page that does not fit, or footnotes the build warns about: `feature-list-fit`.

## 3. The pictures

Run `/oracle-packs:visuals` when the brief has no pictures chosen: the icon per industry and the before-and-after pair, chosen by the owner, before the deck that places them. Build anyway if the owner has not picked yet; each unchosen slot stays an explicit empty container and an open item.

## 4. The architecture picture

Card: `architecture-picture`. Once per spec, before the deck: build the model, render the one-pager's strip and put it to one fresh-context reviewer. Agents read: `shared/references/architecture-diagram.md`. The deck, the one-pager and the listing then draw that same model, which each builds from the brief; none reviews it again. A later run skips this step while `<work>/decisions.md` holds a pass for the same spec stamp.

## 5. The sales deck

Cards: `deck`, `deck-slides-1-5`, `deck-slides-6-10`. Build with the fit report, then the deck's own check before any render.

Cards for the render: `deck-render`, `shared/references/slide-design.md`. Make a contact sheet of all ten and read it by eye.

## 6. The sales one-pager

Card: `one-pager`. Only after the deck is approved: it condenses the deck, and the owner's deck feedback applies here.

Card for a page that runs to two: `one-pager-overflow`.

## 7. The executive summary

Cards: `exec-summary`, `exec-summary-blocks`. With `--host-deck` whenever the slide has a destination deck.

## After each artifact: checks, editorial pass, review

Card: `checks`. The artifact's own checks, then the clearance linter and the consistency check on its file, all clean before the owner sees anything.

Card: `editorial`. For the deck, the one-pager and the executive summary: one fresh-context subagent on the strongest model. Agents read: `shared/references/client-documents.md`, `shared/references/slide-design.md`, `shared/references/naming-and-clearance.md`.

Card for the one-pager's copy: `one-pager-review`.

Card: `artifact-review`. The render opens beside the conversation, then one widget: approve, rebuild with changes, or stop. Never start the next artifact before this one is approved; log each approval with the file's spec stamp.

## 8. The consistency gate

Card: `consistency-gate`. After the last document and before the listing and the demo: the consistency check across every produced file, the clearance linter once per artifact on its own channel, the deck's check re-run on the approved file, and the diagram check across all three drawings. A file built from an earlier version of the spec — typically the feature list, once the pictures step has written into the spec — is rebuilt first. The owner hears one plain line.

## 9. The listing and the demo

`/oracle-packs:listing`, then `/oracle-packs:demo`, each its own skill with its own review, for the artifacts the owner chose.

## 10. Delivery

Card: `delivery`. The approved finals go to the pack's OneDrive folder, one line per delivered file in `<work>/decisions.md`, and one closing message: the files and where they are, what was decided differently from the brief and why, and the open items the owner still holds.

## Self-check before closing

- [ ] Spec confirmed and lint-clean before the first build; nothing the brief settled was asked again.
- [ ] Every artifact built by its tool from the spec, into the `artifacts` folder; none hand-edited, nothing from the build in the repo.
- [ ] The architecture picture reviewed once by a fresh-context reviewer, and `check_diagram.py` clean on every drawing of it.
- [ ] Each artifact's checks clean on its own channel before the owner saw it, and the editorial pass made on the deck, the one-pager and the executive summary.
- [ ] Every artifact approved through the widget, in order, each approval logged with its spec stamp.
- [ ] The consistency gate clean; nothing internal-only (contract values, named accounts, capacity numbers) in a partner or customer cut.
- [ ] Finals delivered as `<Pack name> - <Artifact> - Oracle.<ext>`.
