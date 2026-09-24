# deck — assets and how to run the builder

## What is here

| File | What it is |
|---|---|
| `exemplar/wfo-sales-deck.pptx` | **the exemplar** — the reference Workforce Optimization sales deck, 15 MB, 10 slides. The deck is built by filling *its* slides. Read-only: the builder works on an in-memory copy and the file is never edited. |
| `exemplar/slots.json` | semantic slot → shape id on each exemplar slide, with the exemplar's SHA-256. Re-derive it if the exemplar is ever replaced. |
| `softserve-deck-base.pptx` | 41 KB single-slide SoftServe shell (master, theme, logo, one layout). The executive summary builds on it when no host deck is given. |
| `../references/exemplar-builder.md` | how the filling works, how every ambiguous shape was resolved, and where the builder does compute a number |
| `../references/deck-anatomy.md` | the 10-slide anatomy: purpose, components, which exemplar slide, what varies, what is removed, word budgets |
| `../references/brand-tokens.md` | colours, fonts + fallbacks, the base's layouts, the text-fit rule |
| `../references/reference-geometry.json` | the exemplar measured — per slide the rounded-shape and picture counts, fonts and sizes, the cover block, the icon and picture slots, the table type floors. What `lint_deck.py` holds a build to. |
| `../tools/build_deck_v2.py` | **the builder** |
| `../tools/exemplar.py` | the filling helpers (open, arrange, duplicate, fill, clone, connectors) |
| `../tools/lint_deck.py` | the deck linter — run it before anyone sees the deck |
| `shared/tools/deckkit.py` | shared primitives (brand tokens, shapes, spec access, fit estimator), one copy for the deck and the executive summary |
| `../tools/render_probe.sh` | what can render a .pptx on this machine, and how |
| `../tests/fixture-pack-spec.md` | anonymized Workforce optimization spec — the acceptance fixture for both builders and the executive summary. Not a delivered artifact and not a source of truth for pricing: its figures are the July collateral's, kept so the builders fit realistic string lengths |
| `../tests/fixture-pack-spec_v2-variability.md` | a second spec, not a real pack (3 verticals with one empty card, 7 capability rows, 2 architecture inputs and 2 outputs, 3 layers, a 3-product engine) that must build with no drawing change |
| `../tests/test_build_deck_v2.py` | builds both specs and asserts what "clone, don't redraw" means in the file |
| `../tests/test_lint_deck.sh` | lints the exemplar, both builders' fixture decks, and a copy broken four ways |

**Icons live outside this folder.** Each industry card carries the icon the owner
picked in `/oracle-packs:visuals` (`verticals[].icon`, its white render, as the
reference cards are white). With no pick, the shared icon library at
`shared/data/icons/` supplies one by keyword (`map.yaml` carries each icon's
keywords, what it depicts, where it came from and its licence); with neither, the
card keeps the reference deck's icon and the build says so. Only the deck draws
industry icons; do not copy icons into this skill.

**Why the exemplar is in the repo.** A plugin has to work in any session and on
any machine where it is installed, and a file on OneDrive can be edited by anyone
and silently change the template. A repo asset changes only by a deliberate
commit — and `slots.json` records the hash it was mapped against.

Brand fonts ship privately in the plugin's `fonts/` folder, for practice members
only, and are never embedded in a deck. The deck names them; whoever opens it in
PowerPoint sees them if they have them installed, and the fit check reads the
shipped files (falling back to metric stand-ins when the folder is empty) — see
"Text fit" in `brand-tokens.md`.

## Dependencies

Python 3 with `pyyaml`, `python-pptx`, `Pillow` (listed in
`plugins/oracle-packs/requirements.txt`). Nothing to install by hand: `shared/tools/py`
(the plugin's `shared/tools/py`) runs every tool with an interpreter that has them,
provisioning one in `~/.oracle-packs/venv` on first use — never in system Python. Check:

```bash
shared/tools/py --check
```

## Run it

```bash
shared/tools/py tools/build_deck_v2.py <pack-spec.md> --out <dir> [--channel partner_print|internal]
shared/tools/py tools/build_deck_v2.py --help
```

Useful flags:

- `--fit-report` — print the estimate for every text box, not just the failures.
- `--allow-overflow` — exit 0 anyway; for a review build you intend to fix.
- `--exemplar <pptx>` / `--slots <json>` — build from a different exemplar and map.
- `--icons <map.yaml>` — a different icon library.

Check it:

```bash
shared/tools/py tools/lint_deck.py <dir>/<slug>-sales-deck.pptx \
  --spec <pack-spec.md> --channel partner_print
```

Exit 0 clean · 1 something failed, each finding on its own line · 2 the deck or
the arguments cannot be read. `--reference` lints the exemplar itself and skips
the three checks that compare a deck against a pack brief — that is the
regression test that the linter's budgets are still the exemplar's own.

Tests:

```bash
PY=shared/tools/py tests/test_lint_deck.sh       # the four linter verdicts
shared/tools/py tests/test_build_deck_v2.py      # both specs, 66 checks
```

Output: `<dir>/<slug>-sales-deck.pptx`, 10 slides.

## What "done" means

1. **Fit report clean.** The builder exits non-zero if any box would overflow or
   any detailed-table cell runs past its word budget; 0 means every string fits
   its box on the measured metrics plus the margin — 2 % on the shipped brand
   face, 6 % on a stand-in; the report's first line says which.
2. **Deck linter clean.** `tools/lint_deck.py` — ten slides, the running header on
   slides 2–10, no tier line on the cover, the family's hero on the cover (the
   exemplar's own photo title layout, with a picture on it), the exemplar's own
   faces, no rounded card and no more pills than the exemplar's slide carries, an
   icon on every industry card, the architecture slide naming the pack, the
   engine's products and every destination with one arrow per source, table type
   at or above the exemplar's own floor.
3. **Contact sheet reviewed.** Run `tools/render_probe.sh --deck <the deck>`; it
   reports which renderer exists here and prints the recipe. Render every slide,
   build a contact sheet, and look at it. A fit report is not a render and a
   render is not a fit report — you need both. Slide 8 also goes to the
   fresh-context diagram reviewer (`shared/references/architecture-diagram.md`).
4. **Clearance and consistency clean.** `shared/tools/lint_artifact.py` and
   `shared/tools/check_consistency.py` on the built file.
5. **Builder notes read.** Notes at the end of the report are the ones a report
   cannot fail on: a picture slot still empty, an industry that kept the
   exemplar's own icon, a table that could not fit at the type floor, a metric set
   dropped for the channel, a slide that failed to build. The architecture summary
   printed after the report is for the owner, not the log.

## Gotchas

- The spec is the only source: a missing required component stops the build with
  a message pointing back at `/oracle-packs:spec`. Do not fill the gap here.
- The builder keeps going when one slide raises, and records the failure as a
  note, so you get nine reviewable slides instead of nothing. Check the notes.
- A shape inside a group carries its coordinates in the group's child space, so
  its own frame is not what renders (`exemplar.group_scale_x` converts). The
  engine box on slide 8 is the one that bites.
