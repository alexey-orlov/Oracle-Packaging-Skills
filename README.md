# Oracle Packaging Skills

Claude Code skills that turn one delivered Oracle + NVIDIA AI engagement into a repeatable **accelerator pack** and produce its standard artifact set from **one signed-off pack spec**: feature list, sales deck, sales one-pager, executive summary, mini-site listing, interactive demo.

Owner: Alex Orlov (SoftServe R&D). Internal to SoftServe. Started 2026-09-18.

## How it works

```
/oracle-packs:spec          inputs and intake → research → your call on it → the pack's story (one pick) → the rest drafted and reviewed → the whole brief
/oracle-packs:build         feature-list → pictures → deck → one-pager → exec-summary → listing → demo, one review pause after each
```

Every artifact reads its content from `packs/<slug>/pack-spec.md` — one Markdown file per pack, readable as the pack's brief and written through the plugin's `shared/tools/packspec.py`. Nothing is invented: a missing fact is a question to the user, a price without a source is "tbd" with a footnote, a figure without clearance is "results to follow". The schema is `plugins/oracle-packs/shared/schema/pack-spec.md`; the worked example is `examples/workforce-optimization/`.

| Command | What it produces |
|---|---|
| `/oracle-packs:spec` | `pack-spec.md`, research brief, intake and decisions log |
| `/oracle-packs:build <pack>` | every artifact below, in order, each checked and reviewed before the next, then the listing and the demo |
| `/oracle-packs:build <pack> feature-list` | `.docx` capability matrix (Area > Category > Feature, ● ◐ ○, customization scope) |
| `/oracle-packs:build <pack> deck` | 10-slide `.pptx` on the SoftServe brand base |
| `/oracle-packs:build <pack> one-pager` | HTML → one A4 PDF |
| `/oracle-packs:build <pack> exec-summary` | one slide, on the host deck's master when given |
| `/oracle-packs:visuals` | the pack's pictures: an icon per industry, the today / tomorrow pair, an optional cover |
| `/oracle-packs:listing` | a `products[]` entry for the practice mini-site, checker-clean |
| `/oracle-packs:demo` | a guided interactive walkthrough (asks for sources first) |

## Running it anywhere

The plugin runs on the owner's Macs and on a colleague's Mac or Windows machine. What a machine lacks is found at run time and reported in plain words; nothing degrades silently.

**1. Install from GitHub.** Two private repositories: this one (the marketplace and its one plugin) and the practice mini-site's, which only the listing and the demo need. Authenticate once — `gh auth login` (let it set up Git) or an SSH key on your GitHub account — then:

```bash
claude plugin marketplace add <this repo's git URL>
claude plugin install oracle-packs@oracle-packaging-skills
```

Clone this repository as well: the pack specs live in its `packs/`, so run the skills from inside the checkout or point `ORACLE_PACKS_ROOT` at it. For the listing and the demo, clone the mini-site repository and point `ORACLE_SITE_ROOT` at the checkout (or pass `--site`).

**Releasing.** An install from git runs a copy of the plugin in `~/.claude/plugins/cache/oracle-packaging-skills/oracle-packs/<version>/`, and `claude plugin update` skips the copy when the version equals the installed one — so a release bumps `version` in `plugins/oracle-packs/.claude-plugin/plugin.json`, is committed and pushed, and then on each machine:

```bash
claude plugin marketplace update oracle-packaging-skills && claude plugin update oracle-packs@oracle-packaging-skills
```

followed by a new session — a running one keeps the version it loaded.

> **Note — on the owner's Mac:** the repo folder itself is registered as a local marketplace (`source: directory`) and `oracle-packs` is installed at user scope. Claude Code's plugin reference says a plugin from a local-directory marketplace loads in place, so terminal sessions see an edit at the next session or `/reload-plugins`; the desktop app is reported to still run the install-time copy (claude-code issue #96223), so the release steps above are what reach every session. Until 0.1.40 the marketplace carried a second plugin, `oracle-packs-web` (the listing and the demo); both skills now live in `oracle-packs`, so remove the old one once: `claude plugin uninstall oracle-packs-web@oracle-packaging-skills`.

**2. Python — nothing to install by hand.** Every tool runs as `shared/tools/py <tool>.py`, from the plugin folder (`plugins/oracle-packs/` in the checkout). That resolver takes the first interpreter that imports PyYAML, python-docx, python-pptx, Pillow and pypdf on Python 3.9+: `$ORACLE_PACKS_PY`, then a `.venv` at the repo root, then the managed venv at `$ORACLE_PACKS_VENV` (default `~/.oracle-packs/venv`) — created from the plugin's `requirements.txt` on first use, with one line saying so — then plain `python3`. Never system Python. `shared/tools/py --check` shows what it found. On Windows it runs under Git Bash or WSL.

**3. Other programs.** Node 22+ (the listing's checker and inserter need 14+, the demo capture 22+) · Google Chrome or Chromium, for the one-pager's PDF and the demo capture · LibreOffice, for the feature list's page count and slide rendering off macOS · poppler's `pdftotext`, optional, for PDFs in the clearance linter · `rsvg-convert` or the `cairosvg` module, for icons off macOS. `plugins/oracle-packs/skills/build/deck/tools/render_probe.sh` says which renderers a machine has.

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

A pack's spec lives in this repo at `packs/<slug>/pack-spec.md`, with the pictures it names beside it, committed and pushed so every colleague builds from the same spec. Everything else a run produces — the built artifacts, the intake, the inventory and its extracts of customer documents, the sources, the research, the decisions log — goes to the local work folder `$ORACLE_PACKS_OUT/<slug>/` (default `~/oracle-packs/<slug>/`), and `shared/tools/pack_paths.py <slug>` prints both places. That working record never enters the repo, because it quotes the customer's own documents and carries internal figures: one intake note held a contract value.

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

**8. The rules.** `plugins/oracle-packs/shared/references/` is the plugin's own home for its rules; copies in the owner's personal repository serve his other work and may differ.

**Fewer permission prompts.** Merge the `permissions.allow` list of `docs/settings.example.json` into the `.claude/settings.json` of the folder you run the skills from.
Add the installed resolver in absolute form as well — `Bash(<home>/.claude/plugins/cache/oracle-packaging-skills/oracle-packs/<version>/shared/tools/py *)`, redone when the version changes — since a permission rule does not expand `${CLAUDE_PLUGIN_ROOT}`.

## Layout

```
.claude-plugin/marketplace.json     the marketplace (one plugin)
plugins/oracle-packs/               the plugin
  skills/                           spec · visuals · build (with feature-list/ · deck/ · one-pager/ · exec-summary/: each artifact's tools, assets and tests) · listing · demo
  shared/                           what several skills read, in one place
    cards/                          the two cards every skill loads at start-up: owner-language · review-protocol
    references/                     engagement context · naming and clearance · slide-design · client-documents · research-standards · running agents · architecture diagram · visual assets
    data/                           oracle-products.yaml (the only allowed product names) · roadmap-items.csv (the only allowed roadmap ids) · icons/ (the deck's industry icon library)
    schema/pack-spec.md             the spec schema and template
    tools/                          py (the interpreter resolver) · packspec.py (the spec's loader and writer) · pack_paths.py · spec_stamp.py · lint_spec.py · lint_artifact.py · check_consistency.py · deckkit.py · specfmt.py · denylist.txt
  fonts/                            the brand faces, private
  requirements.txt                  the Python dependencies
tests/run_tests.sh                  the suite: every tool, every card's spec keys, every skill's context budget
packs/<slug>/                       one pack's shared files, and only these (.gitignore keeps out the rest): pack-spec.md · visuals/ (the pictures the spec names, their provenance .json files, credits.md)
examples/workforce-optimization/    the worked example spec
docs/DECISIONS.md                   the owner decisions the skills implement
docs/settings.example.json          the permission allow-list for the toolchain
```

## Rules of the repo

- `plugins/oracle-packs/shared/references/*.md` are rewritten to current truth; never append a dated "UPDATE" section. A subagent that finds a doc wrong reports it; a person or the main session rewrites it.
- No customer names, contract values, internal capacity numbers, credentials or machine paths in anything under `plugins/` except the linter deny-list, which exists to catch them.
- A new owner rule becomes a linter assertion or a schema rule, so it survives the next rewrite.
- Prices, durations and figures live in pack specs, never in the references.
- The repo is SoftServe-internal: the linter deny-list (`plugins/oracle-packs/shared/tools/denylist.txt`) is the one place customer names appear, so the linter can catch them. Do not redistribute the repo outside SoftServe; an external deny-list can be supplied instead via `ORACLE_PACK_DENYLIST`.
