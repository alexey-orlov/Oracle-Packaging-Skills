# deck — assets and how to run the builder

## What is here

| File | What it is |
|---|---|
| `softserve-deck-base.pptx` | 41 KB single-slide SoftServe shell: real master, theme, logo, one layout (`Title-1Column`). The deck is built on this. Never edit it in place — the builder copies it. |
| `../references/brand-tokens.md` | colours, fonts + fallbacks, geometry constants, the base's layouts, the text-fit rule |
| `../references/deck-anatomy.md` | the 10-slide anatomy: purpose, components, geometry, word budgets, design rules per slide |
| `../tools/build_deck.py` | the builder |
| `../tools/deckkit.py` | shared primitives (brand tokens, shapes, spec access, fit estimator) |
| `../tools/render_probe.sh` | what can render a .pptx on this machine, and how |
| `../tests/fixture-pack-spec.yaml` | anonymized Workforce optimization spec used to smoke-test both builders |

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

Smoke test:

```bash
python3 tools/build_deck.py tests/fixture-pack-spec.yaml --out /tmp/deck-smoke --fit-report
```

Output: `<dir>/<slug>-sales-deck.pptx`, 10 slides.

## What "done" means

1. **Fit report clean.** The builder exits non-zero if any box would overflow;
   0 means every string fits its box on the stand-in metrics plus 6 %.
2. **Contact sheet reviewed.** Run `tools/render_probe.sh --deck <the deck>`;
   it reports which renderer exists here and prints the recipe. Render every
   slide, build a contact sheet, and look at it. A fit report is not a render
   and a render is not a fit report — you need both.
3. **Linter clean.** The shared clearance linter passes: no customer name the
   channel does not allow, no banned vocabulary, no invented price or tier.
4. **Builder notes read.** Notes at the end of the report are the ones a report
   cannot fail on: screenshot slots still empty, a table that had to scale below
   100 %, a metric set dropped for the channel, a slide that failed to build.

## Gotchas

- The spec is the only source: a missing required component stops the build with
  a message pointing back at `/oracle-packs:spec`. Do not fill the gap here.
- The builder keeps going when one slide raises, and records the failure as a
  note, so you get nine reviewable slides instead of nothing. Check the notes.
- `deckkit.py` is duplicated in `../../exec-summary/tools/` so each skill copies
  standalone. If you change one, copy it to the other.
- The base has one layout. A cover, dividers and a closing slide have to be
  drawn or inherited from a host deck.
