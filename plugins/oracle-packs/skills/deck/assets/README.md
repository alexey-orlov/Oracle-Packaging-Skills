# deck — assets and how to run the builder

## What is here

| File | What it is |
|---|---|
| `exemplar/wfo-sales-deck.pptx` | **the exemplar** — the reference Workforce Optimization sales deck, 15 MB, 10 slides. The deck is built by filling *its* slides. Read-only: the builder works on an in-memory copy and the file is never edited. |
| `exemplar/slots.json` | semantic slot → shape id on each exemplar slide, with the exemplar's SHA-256. Re-derive it if the exemplar is ever replaced. |
| `softserve-deck-base.pptx` | 41 KB single-slide SoftServe shell (master, theme, logo, one layout). Only the legacy builder uses it. |
| `../references/exemplar-builder.md` | how the filling works, how every ambiguous shape was resolved, and where the builder does compute a number |
| `../references/deck-anatomy.md` | the 10-slide anatomy: purpose, components, which exemplar slide, what varies, what is removed, word budgets |
| `../references/brand-tokens.md` | colours, fonts + fallbacks, the base's layouts, the text-fit rule |
| `../references/reference-geometry.json` | the exemplar measured — per slide the rounded-shape and picture counts, fonts and sizes, the cover block, the icon and picture slots, the table type floors. What `lint_deck.py` holds a build to. |
| `../tools/build_deck_v2.py` | **the builder** |
| `../tools/exemplar.py` | the filling helpers (open, arrange, duplicate, fill, clone, connectors) |
| `../tools/build_deck.py` | the legacy builder — redraws on the 41 KB shell, for a machine without the exemplar |
| `../tools/lint_deck.py` | the deck linter — run it before anyone sees the deck |
| `../tools/deckkit.py` | shared primitives (brand tokens, shapes, spec access, fit estimator) |
| `../tools/render_probe.sh` | what can render a .pptx on this machine, and how |
| `../tests/fixture-pack-spec.yaml` | anonymized Workforce optimization spec — the acceptance fixture for both builders |
| `../tests/fixture-pack-spec_v2-variability.yaml` | a second spec (3 verticals, 7 capability rows, 3 layers, a 3-product engine) that must build with no drawing change |
| `../tests/test_build_deck_v2.py` | builds both specs and asserts what "clone, don't redraw" means in the file |
| `../tests/test_lint_deck.sh` | lints the exemplar, both builders' fixture decks, and a copy broken four ways |

**Icons live outside this folder.** The vertical-application icons come from the
shared icon library at `shared/data/icons/` (`${CLAUDE_PLUGIN_ROOT}/shared/data/icons`,
falling back to the repo's own `shared/data/icons` in a source checkout) — PNGs
plus `map.yaml`, which carries each icon's keywords, what it depicts, where it
came from and its licence. The one-pager and the mini-site listing draw from the
same library, so an industry looks the same wherever it appears; do not copy
icons into this skill.

**Why the exemplar is in the repo.** A plugin has to work in any session and on
any machine where it is installed, and a file on OneDrive can be edited by anyone
and silently change the template. A repo asset changes only by a deliberate
commit — and `slots.json` records the hash it was mapped against.

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
python3 tools/build_deck_v2.py <pack-spec.yaml> --out <dir> [--channel partner_print|internal]
python3 tools/build_deck_v2.py --help
```

Useful flags:

- `--fit-report` — print the estimate for every text box, not just the failures.
- `--allow-overflow` — exit 0 anyway; for a review build you intend to fix.
- `--exemplar <pptx>` / `--slots <json>` — build from a different exemplar and map.
- `--icons <map.yaml>` — a different icon library.

Check it:

```bash
python3 tools/lint_deck.py <dir>/<slug>-sales-deck.pptx \
  --spec <pack-spec.yaml> --channel partner_print
```

Exit 0 clean · 1 something failed, each finding on its own line · 2 the deck or
the arguments cannot be read. `--reference` lints the exemplar itself and skips
the three checks that compare a deck against a pack brief — that is the
regression test that the linter's budgets are still the exemplar's own.

Tests:

```bash
PY=.venv/bin/python tests/test_lint_deck.sh      # the four linter verdicts
.venv/bin/python tests/test_build_deck_v2.py     # both specs, 49 assertions
```

Output: `<dir>/<slug>-sales-deck.pptx`, 10 slides.

## The legacy builder

```bash
python3 tools/build_deck.py <pack-spec.yaml> --out <dir> [--channel …] [--base <pptx>]
```

It redraws every slide on `softserve-deck-base.pptx` from measurements. Use it
only where the exemplar is not available — an install that stripped the 15 MB
asset, or a machine building from the base alone. It produces the same anatomy,
but it re-derives hundreds of design decisions that the exemplar otherwise
supplies for free, and every fidelity finding in `docs/DECK-FIDELITY.md` came
from exactly that. The shell carries no photo layout, so its cover is ink only
and **fails the deck linter's cover check by design**; `lint_deck.py
--legacy-cover-ok` demotes that one failure to a loud warning so the rest can
still be checked, and such a deck is never delivered as final — set
`deck.images.cover`, or build with the exemplar builder.

## What "done" means

1. **Fit report clean.** The builder exits non-zero if any box would overflow or
   any detailed-table cell runs past its word budget; 0 means every string fits
   its box on the stand-in metrics plus 6 %.
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
- `deckkit.py` is duplicated in `../../exec-summary/tools/` so each skill copies
  standalone. If you change one, copy it to the other.
- A shape inside a group carries its coordinates in the group's child space, so
  its own frame is not what renders (`exemplar.group_scale_x` converts). The
  engine box on slide 8 is the one that bites.
