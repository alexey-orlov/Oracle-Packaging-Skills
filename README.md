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

## Running it anywhere

The plugins run on the owner's Macs and on a colleague's Mac or Windows machine. What a machine lacks is found at run time and reported in plain words; nothing degrades silently.

**1. Install from GitHub.** Two private repositories: this one (the marketplace, both plugins) and the practice mini-site's, which only the listing and the demo need. Authenticate once — `gh auth login` (let it set up Git) or an SSH key on your GitHub account — then:

```bash
claude plugin marketplace add <this repo's git URL>
claude plugin install oracle-packs@oracle-packaging-skills
claude plugin install oracle-packs-web@oracle-packaging-skills   # only if you build listings or demos
```

Clone this repository as well: the pack specs live in its `packs/`, so run the skills from inside the checkout or point `ORACLE_PACKS_ROOT` at it. For the listing and the demo, clone the mini-site repository and point `ORACLE_SITE_ROOT` at the checkout (or pass `--site`). A release runs `tools/sync-shared.sh` first, so each plugin carries the current `shared/` (`--check` reports drift).

> **Note — on the owner's Mac (done 2026-09-18):** the repo folder itself is registered as a local marketplace (`source: directory`) and both plugins are installed at user scope, so `/oracle-packs:…` and `/oracle-packs-web:…` work in every session. Sessions do **not** read this repo: they read a snapshot copied into `~/.claude/plugins/cache/oracle-packaging-skills/<plugin>/<version>/`, and `claude plugin update` re-copies only when the `version` in the plugin's `.claude-plugin/plugin.json` is higher than the installed one — at the same version it reports "already at the latest version" and keeps the old snapshot (2026-09-22: four days of edits had reached no session this way). A release is therefore: bump `version` in **both** `plugins/*/.claude-plugin/plugin.json` (both, because `sync-shared.sh` touches both plugins), then
>
> ```bash
> tools/sync-shared.sh && claude plugin marketplace update oracle-packaging-skills && claude plugin update oracle-packs@oracle-packaging-skills && claude plugin update oracle-packs-web@oracle-packaging-skills
> ```
>
> then start a new session — a running one keeps the version it loaded (the old snapshot directory is kept, so a run in progress does not break). The snapshot is taken from the working tree, committed or not, while the `gitCommitSha` the plugin manager records is HEAD at that moment — commit before releasing if that provenance should mean anything.

**2. Python — nothing to install by hand.** Every tool runs as `shared/tools/py <tool>.py`. That resolver takes the first interpreter that imports PyYAML, python-docx, python-pptx, Pillow and pypdf on Python 3.9+: `$ORACLE_PACKS_PY`, then a `.venv` at the repo (or plugin) root, then the managed venv at `$ORACLE_PACKS_VENV` (default `~/.oracle-packs/venv`) — created from `requirements.txt` on first use, with one line saying so — then plain `python3`. Never system Python. `shared/tools/py --check` shows what it found. On Windows it runs under Git Bash or WSL.

**3. Other programs.** Node 22+ (the listing's checker and inserter need 14+, the demo capture 22+) · Google Chrome or Chromium, for the one-pager's PDF and the demo capture · LibreOffice, for the feature list's page count and slide rendering off macOS · poppler's `pdftotext`, optional, for PDFs in the clearance linter · `rsvg-convert` or the `cairosvg` module, for icons off macOS. `plugins/oracle-packs/skills/deck/tools/render_probe.sh` says which renderers a machine has.

**4. What a Mac adds.** QuickLook renders slides and icons with nothing installed; Pages verifies the feature list's page count; Apple Symbols draws its three status glyphs at one size.

**5. Environment variables.**

| Variable | Sets |
|---|---|
| `ORACLE_PACKS_PY` | the interpreter to try first |
| `ORACLE_PACKS_VENV` | where the managed venv lives (default `~/.oracle-packs/venv`) |
| `ORACLE_PACKS_ROOT` | the checkout of this repo that holds `packs/`; unset, it is found from the working directory — that folder or its nearest parent that is a checkout |
| `ORACLE_PACKS_OUT` | the root of the local work folders, one `<slug>/` per pack: default `~/oracle-packs` (`%USERPROFILE%\oracle-packs` on Windows), later the practice OneDrive |
| `ORACLE_SITE_ROOT` | the mini-site checkout, for the listing and the demo |
| `PEXELS_API_KEY`, `UNSPLASH_ACCESS_KEY` | the photo libraries' keys; on a Mac the Keychain entry of the same name works too |
| `CHROME_BIN` | Chrome, when it is not where the builders look |

A pack's spec lives in this repo at `packs/<slug>/pack-spec.yaml`, with the architecture model and the pictures it names beside it, committed and pushed so every colleague builds from the same spec. Everything else a run produces — the built artifacts, the intake, the inventory and its extracts of customer documents, the sources, the research, the decisions log — goes to the local work folder `$ORACLE_PACKS_OUT/<slug>/` (default `~/oracle-packs/<slug>/`), and `shared/tools/pack_paths.py <slug>` prints both places. That working record never enters the repo, because it quotes the customer's own documents and carries internal figures: one intake note held a contract value.

**6. Brand fonts.** Azurio and Replica LL TT ship in the plugin's `fonts/` folder, privately, for practice members: not redistributable, and never copied into an artifact or a customer file. The builders read the shipped files, so fit is exact on every machine (with the folder empty they fall back to metric stand-ins with headroom). To see a render as the owner sees it, install them: `shared/tools/py shared/tools/install_fonts.py`.

**7. What degrades where.**

| Feature | macOS with QuickLook and Pages | Windows or a Mac without them (LibreOffice + Chrome) |
|---|---|---|
| The Python tools | works | works (Git Bash or WSL on Windows) |
| Feature list on one page | verified by Pages | verified by LibreOffice; with neither, not verified, says so |
| One-pager on one page | verified by Chrome | verified by Chrome; without Chrome, not verified, says so |
| Deck and executive-summary fit | works, exact on the shipped fonts | works, exact on the shipped fonts |
| Slide render for review | works (QuickLook) | works (LibreOffice, then `pdftoppm`); with neither, not verified, says so |
| Feature list's status glyphs | works (Apple Symbols) | works: measured on Segoe UI Symbol or DejaVu Sans |
| Icons above 240 px | works (QuickLook) | works with `rsvg-convert` or `cairosvg`; without, skipped, says so |
| Photos from Pexels or Unsplash | works with a key in the environment or the Keychain | works with a key in the environment; without, skipped, says so |
| PDF text in the clearance linter | works with `pdftotext`; without, skipped, says so | works with `pdftotext`; without, skipped, says so |
| Demo capture | works with Node 22+ and Chrome | works with Node 22+ and Chrome; without, skipped, says so |

**8. The rules.** `shared/references/` is the plugins' own home for their rules; copies in the owner's personal repository serve his other work and may differ.

**Fewer permission prompts.** Merge the `permissions.allow` list of `docs/settings.example.json` into the `.claude/settings.json` of the folder you run the skills from.
Add the two installed resolvers in absolute form as well — `Bash(<home>/.claude/plugins/cache/oracle-packaging-skills/<plugin>/<version>/shared/tools/py *)` for each plugin, redone when the version changes — since a permission rule does not expand `${CLAUDE_PLUGIN_ROOT}`.

## Layout

```
.claude-plugin/marketplace.json     the marketplace (two plugins)
shared/                             single source, synced into each plugin by tools/sync-shared.sh
  references/                       engagement context · naming and clearance · pack anatomy · PoV rules · review loop · talking to the owner · slide-design · client-documents · research-standards · coaching rules · running agents
  data/                             oracle-products.yaml (the only allowed product names) · roadmap-items.csv (+ L2 patterns, crosswalk, tracker) · regen script
  schema/pack-spec.md               the spec schema and template
  tools/                            py (the interpreter resolver) · requirements.txt · pack_paths.py · spec_stamp.py · lint_spec.py · lint_artifact.py · check_consistency.py · denylist.txt · tests/
plugins/oracle-packs/               spec · feature-list · deck · one-pager · exec-summary · visuals · build; fonts/ (the brand faces, private)
plugins/oracle-packs-web/           listing · demo
packs/<slug>/                       one pack's shared files, and only these (.gitignore keeps out the rest): pack-spec.yaml · architecture.json (the architecture model) · visuals/ (the pictures the spec names, their provenance .json files, credits.md)
examples/workforce-optimization/    the worked example spec
docs/PLAN.md                        the build plan and the rules overview
docs/DECISIONS.md                   the owner decisions the skills implement
docs/TEST-REPORT.md                 the integration pass: what ran, what was fixed, what is still rough
docs/settings.example.json          the permission allow-list for the toolchain
```

## Rules of the repo

- `shared/references/*.md` are rewritten to current truth; never append a dated "UPDATE" section. A subagent that finds a doc wrong reports it; a person or the main session rewrites it.
- No customer names, contract values, internal capacity numbers, credentials or machine paths in anything under `shared/` or `plugins/` except the linter deny-list, which exists to catch them.
- A new owner rule becomes a linter assertion or a schema rule, so it survives the next rewrite.
- Prices, durations and figures live in pack specs, never in the references.
- The repo is SoftServe-internal: the linter deny-list (`shared/tools/denylist.txt`) is the one place customer names appear, so the linter can catch them. Do not redistribute the repo outside SoftServe; an external deny-list can be supplied instead via `ORACLE_PACK_DENYLIST`.
