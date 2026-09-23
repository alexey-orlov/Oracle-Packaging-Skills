# Oracle Packaging Skills

Claude Code skills that turn one delivered Oracle + NVIDIA AI engagement into a repeatable **accelerator pack** and produce its standard artifact set from **one signed-off pack spec**: feature list, sales deck, sales one-pager, executive summary, mini-site listing, interactive demo.

Owner: Alex Orlov (SoftServe R&D). Internal to SoftServe. Started 2026-09-18.

## How it works

```
/oracle-packs:spec          intake (questions) → generalization research → options → 12 components signed off one by one → brief
/oracle-packs:build         feature-list → deck → one-pager → exec-summary → (web) listing → demo, one review pause after each
```

Every artifact reads its content from `packs/<slug>/pack-spec.yaml`. Nothing is invented: a missing fact is a question to the user, a price without a source is "tbd" with a footnote, a figure without clearance is "results to follow". The schema is `shared/schema/pack-spec.md`; the worked example is `examples/workforce-optimization/`.

| Command | What it produces | Plugin |
|---|---|---|
| `/oracle-packs:spec` | `pack-spec.yaml`, research brief, intake and decisions log | oracle-packs |
| `/oracle-packs:feature-list` | `.docx` capability matrix (Area > Category > Feature, ● ◐ ○, customization scope) | oracle-packs |
| `/oracle-packs:deck` | 10-slide `.pptx` on the SoftServe brand base | oracle-packs |
| `/oracle-packs:one-pager` | HTML → one A4 PDF | oracle-packs |
| `/oracle-packs:exec-summary` | one slide, on the host deck's master when given | oracle-packs |
| `/oracle-packs:build` | all of the above in order, with review pauses; hands off to the web plugin | oracle-packs |
| `/oracle-packs-web:listing` | a `products[]` entry for the practice mini-site, checker-clean | oracle-packs-web |
| `/oracle-packs-web:demo` | a guided interactive walkthrough (asks for sources first) | oracle-packs-web |

## Install

**As plugins from this marketplace** (recommended once the plugin spike in `docs/PLAN.md` §7 has passed):

```bash
claude plugin marketplace add <this repo's git URL>
claude plugin install oracle-packs@oracle-packaging-skills
claude plugin install oracle-packs-web@oracle-packaging-skills   # only if you build listings or demos
```

**As a plain copy (pilot)**: copy `plugins/oracle-packs/` to `<your repo>/.claude/skills/oracle-packs/` (and the web plugin likewise). A folder under `.claude/skills/` that carries `.claude-plugin/plugin.json` loads as a plugin in place, with the same `/oracle-packs:<name>` commands, when the session starts at that repo's root.

Before either, run `tools/sync-shared.sh` so each plugin carries the current `shared/` copy (the release step; `--check` reports drift).

**On the owner's Mac (done 2026-09-18):** the repo folder itself is registered as a local marketplace (`source: directory`) and both plugins are installed at user scope, so `/oracle-packs:…` and `/oracle-packs-web:…` work in every session. Sessions do **not** read this repo: they read a snapshot copied into `~/.claude/plugins/cache/oracle-packaging-skills/<plugin>/<version>/`, and `claude plugin update` re-copies only when the `version` in the plugin's `.claude-plugin/plugin.json` is higher than the installed one — at the same version it reports "already at the latest version" and keeps the old snapshot (2026-09-22: four days of edits had reached no session this way). A release is therefore: bump `version` in **both** `plugins/*/.claude-plugin/plugin.json` (both, because `sync-shared.sh` touches both plugins), then

```bash
tools/sync-shared.sh && claude plugin marketplace update oracle-packaging-skills && claude plugin update oracle-packs@oracle-packaging-skills && claude plugin update oracle-packs-web@oracle-packaging-skills
```

then start a new session — a running one keeps the version it loaded (the old snapshot directory is kept, so a run in progress does not break). The snapshot is taken from the working tree, committed or not, while the `gitCommitSha` the plugin manager records is HEAD at that moment — commit before releasing if that provenance should mean anything.

## Requirements

Python packages go in a virtualenv, never in system Python. From the repo root:

```bash
python3 -m venv .venv
.venv/bin/pip install -r plugins/oracle-packs/requirements.txt
.venv/bin/python shared/tools/lint_spec.py examples/workforce-optimization/pack-spec.yaml --strict
```

Then call every tool with `.venv/bin/python` (the suite takes `PY=.venv/bin/python shared/tools/tests/run_tests.sh`). Without PyYAML each tool exits 2 and prints that install line.

| Plugin | Needs | Pinned floor (verified) |
|---|---|---|
| oracle-packs | Python 3.9+ with `plugins/oracle-packs/requirements.txt` | PyYAML ≥ 6.0 (6.0.3) · python-docx ≥ 1.1.0 (1.2.0) · python-pptx ≥ 1.0.0 (1.0.2) · Pillow ≥ 10.0 (12.3.0) · pypdf ≥ 4.0 (6.19.0), on Python 3.14.6 |
| oracle-packs | **Google Chrome or Chromium** for the one-pager: the builder prints the HTML to PDF and proves it is one A4 page. Found via `$CHROME_BIN`, the macOS default application path, or `google-chrome` / `chromium` on PATH; without it the tool writes the HTML and exits 4 | any current Chrome |
| oracle-packs | `pdftotext` (poppler) — optional. Without it `lint_artifact.py` skips a `.pdf` with a warning and reports it as *not evaluated*, never as a pass | — |
| oracle-packs-web | **Node** for the site's checker, the inserter and the deny-list converter; **Node 22+** for the demo capture script (built-in `fetch` and `WebSocket`), plus Chrome and a checkout of the practice mini-site repository (it carries `site.manifest.json` and is found through `--site`, `$ORACLE_SITE_ROOT` or a session opened in it) | Node ≥ 14 for listing, ≥ 22 for the demo capture (verified on 26.0.0) |

Brand fonts are licensed and are not shipped; the deck fit report uses metric stand-ins, so trust the report, not what a machine without the fonts renders. For slide QA, `plugins/oracle-packs/skills/deck/tools/render_probe.sh` reports which renderer this machine has and prints the contact-sheet recipe for it.

## Layout

```
.claude-plugin/marketplace.json     the marketplace (two plugins)
shared/                             single source, synced into each plugin by tools/sync-shared.sh
  references/                       engagement context · naming and clearance · pack anatomy · PoV rules · review loop · talking to the owner · slide-design · client-documents · research-standards · coaching rules
  data/                             oracle-products.yaml (the only allowed product names) · roadmap-items.csv (+ L2 patterns, crosswalk, tracker) · regen script
  schema/pack-spec.md               the spec schema and template
  tools/                            lint_spec.py · lint_artifact.py · check_consistency.py · denylist.txt · tests/
plugins/oracle-packs/               spec · feature-list · deck · one-pager · exec-summary · build
plugins/oracle-packs-web/           listing · demo
examples/workforce-optimization/    the worked example spec
docs/PLAN.md                        the build plan and the rules overview
docs/DECISIONS.md                   the owner decisions the skills implement
docs/TEST-REPORT.md                 the integration pass: what ran, what was fixed, what is still rough
```

## Rules of the repo

- `shared/references/*.md` are rewritten to current truth; never append a dated "UPDATE" section. A subagent that finds a doc wrong reports it; a person or the main session rewrites it.
- No customer names, contract values, internal capacity numbers, credentials or machine paths in anything under `shared/` or `plugins/` except the linter deny-list, which exists to catch them.
- A new owner rule becomes a linter assertion or a schema rule, so it survives the next rewrite.
- Prices, durations and figures live in pack specs, never in the references.
- The repo is SoftServe-internal: the linter deny-list (`shared/tools/denylist.txt`) is the one place customer names appear, so the linter can catch them. Do not redistribute the repo outside SoftServe; an external deny-list can be supplied instead via `ORACLE_PACK_DENYLIST`.
