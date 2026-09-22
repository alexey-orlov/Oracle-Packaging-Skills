# deck — assets and how to run the builder

## What is here

| File | What it is |
|---|---|
| `softserve-deck-base.pptx` | 41 KB single-slide SoftServe shell: real master, theme, logo, one layout (`Title-1Column`). The deck is built on this. Never edit it in place — the builder copies it. |
| `../references/brand-tokens.md` | colours, fonts + fallbacks, geometry constants, corners, the base's layouts, the text-fit rule |
| `../references/deck-anatomy.md` | the 10-slide anatomy: purpose, components, geometry, word budgets, design rules per slide |
| `../references/reference-geometry.json` | the reference deck measured — rounded-shape, picture and table counts, fonts and sizes per slide, the cover block, the icon and picture slots, the table type floors. What `lint_deck.py` holds a build to. |
| `../tools/build_deck.py` | the builder |
| `../tools/lint_deck.py` | the deck linter — run it before anyone sees the deck |
| `../tools/deckkit.py` | shared primitives (brand tokens, shapes, spec access, fit estimator) |
| `../tools/render_probe.sh` | what can render a .pptx on this machine, and how |
| `../tests/fixture-pack-spec.yaml` | anonymized Workforce optimization spec used to smoke-test both builders |
| `../tests/test_lint_deck.sh` | builds the fixture, asserts the linter is clean, breaks a copy and asserts it is caught |

**Icons live outside this folder.** The vertical-application icons come from the
shared icon library at `shared/data/icons/` (`${CLAUDE_PLUGIN_ROOT}/shared/data/icons`,
falling back to the repo's own `shared/data/icons` in a source checkout) — PNGs
plus `map.yaml`, which carries each icon's keywords, what it depicts, where it
came from and its licence. The one-pager and the mini-site listing draw from the
same library, so an industry looks the same wherever it appears; do not copy
icons into this skill.

Brand fonts are **not** shipped (licensing). The deck names them; whoever opens
it in PowerPoint sees them if they have them, and the fit check never depends on
having them — see "Text fit" in `brand-tokens.md`.

## Dependencies

Python 3 with `pyyaml`, `python-pptx`, `Pillow` (listed in
`plugins/oracle-packs/requirements.txt`). Check:

```bash
python3 -c "import yaml, pptx, PIL"
```

If that fails, create a virtualenv and install there — never into system Python:

```bash
python3 -m venv .venv && .venv/bin/pip install -r plugins/oracle-packs/requirements.txt
```

## Run it

```bash
python3 tools/build_deck.py <pack-spec.yaml> --out <dir> [--channel partner_print|internal]
python3 tools/build_deck.py --help
```

Useful flags:

- `--fit-report` — print the estimate for every text box, not just the failures.
- `--allow-overflow` — exit 0 anyway; for a review build you intend to fix.
- `--base <pptx>` — build on a different shell.

Check it:

```bash
python3 tools/lint_deck.py <dir>/<slug>-sales-deck.pptx \
  --spec <pack-spec.yaml> --channel partner_print
```

Exit 0 clean · 1 something failed, each finding on its own line · 2 the deck or
the arguments cannot be read.

Smoke test — build, lint, break, lint again:

```bash
PY=.venv/bin/python tests/test_lint_deck.sh
```

Output: `<dir>/<slug>-sales-deck.pptx`, 10 slides.

## What "done" means

1. **Fit report clean.** The builder exits non-zero if any box would overflow or
   any detailed-table cell runs past its word budget; 0 means every string fits
   its box on the stand-in metrics plus 6 %.
2. **Deck linter clean.** `tools/lint_deck.py` — ten slides, the running header
   on slides 2–10, no tier line on the cover, brand faces only, corners no
   rounder than the reference's, an icon on every industry card, the
   architecture slide naming the pack, the engine's products and a destination
   with one arrow per source, table type at or above the floor.
3. **Contact sheet reviewed.** Run `tools/render_probe.sh --deck <the deck>`;
   it reports which renderer exists here and prints the recipe. Render every
   slide, build a contact sheet, and look at it. A fit report is not a render
   and a render is not a fit report — you need both.
4. **Clearance linter clean.** `shared/tools/lint_artifact.py`: no customer name
   the channel does not allow, no banned vocabulary, no invented price or tier.
5. **Builder notes read.** Notes at the end of the report are the ones a report
   cannot fail on: a picture slot still empty, an industry that fell back to the
   neutral icon, a table that could not fit at the type floor, a metric set
   dropped for the channel, a slide that failed to build. The architecture
   summary printed after the report is for the owner, not the log.

## Gotchas

- The spec is the only source: a missing required component stops the build with
  a message pointing back at `/oracle-packs:spec`. Do not fill the gap here.
- The builder keeps going when one slide raises, and records the failure as a
  note, so you get nine reviewable slides instead of nothing. Check the notes.
- `deckkit.py` is duplicated in `../../exec-summary/tools/` so each skill copies
  standalone. If you change one, copy it to the other.
- The base has one layout. A cover, dividers and a closing slide have to be
  drawn or inherited from a host deck.
