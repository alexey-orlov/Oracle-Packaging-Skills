# exec-summary — assets and how to run the builder

## What is here

| File | What it is |
|---|---|
| `../references/exec-summary-anatomy.md` | the one-slide anatomy, measured from the Sep 11 section slides and the Jul 17 executive summary |
| `../tools/build_exec_summary.py` | the builder |
| `shared/tools/deckkit.py` | shared primitives (brand tokens, shapes, spec access, fit estimator), one copy for the deck and this slide |

This skill ships **no deck base of its own**. Without `--host-deck` it builds on
the deck skill's `../deck/assets/softserve-deck-base.pptx`; brand tokens and the
text-fit rule live in `../deck/references/brand-tokens.md`. Brand fonts ship
privately in the plugin's `fonts/` folder, for practice members only; the fit
estimate reads them from there and a slide never embeds them.

## Dependencies

Python 3 with `pyyaml`, `python-pptx`, `Pillow` (see
`plugins/oracle-packs/requirements.txt`). Nothing to install by hand: the plugin's
`shared/tools/py` runs the tools with an interpreter that has them, provisioning one on
first use — never in system Python. Check:

```bash
shared/tools/py --check
```

## Run it

```bash
shared/tools/py tools/build_exec_summary.py <pack-spec.md> --out <dir> \
        [--host-deck <deck.pptx>] [--with-closing] [--fit-report]
shared/tools/py tools/build_exec_summary.py --help
```

- `--host-deck <pptx>` — build the slide on **that deck's own master**, so it
  pastes into the host unchanged. This is the normal path when the summary is
  going into someone else's deck.
- `--with-closing` — append the host's closing slide when it has a `Close`
  layout. The shipped base has none, so on the base the flag is ignored with a
  note; that is expected.
- `--title` — override the slide title (default: the spec's `internal_slide`
  name variant, e.g. "Workforce Optimization App").

Smoke test:

```bash
shared/tools/py tools/build_exec_summary.py ../deck/tests/fixture-pack-spec.md \
        --out /tmp/es-smoke --fit-report
```

Output: `<dir>/<slug>-exec-summary.pptx` — one slide, plus the closing slide
when `--with-closing` found a `Close` layout.

## What "done" means

1. **Fit report clean** — exit 0; no box overflows on the measured metrics plus
   the margin (2 % on the shipped brand face, 6 % on a stand-in).
2. **Render reviewed** — `../deck/tools/render_probe.sh` prints how to render on
   this machine. One slide, so one PNG; look at it.
3. **Linter clean** — the shared clearance linter passes.
4. **Pastes unchanged** — when it is destined for a host deck, it was built with
   `--host-deck` and opened in that deck once to confirm.

## Gotchas

- The builder defaults to the **internal** channel (`--channel` overrides it): the
  executive summary is usually the internal artifact and uses the internal name
  variant. Internal naming is not a licence to print internal operating numbers — headcount,
  contract values and internal package costs stay off the slide.
- The proof block is all-or-none. If any metric in the set is restricted away
  from this channel, the block renders as an empty instance of the same panel
  and the builder says so. Fix the clearance, do not half-fill the block.
- The capability tree is areas and categories only — feature names belong on the
  feature list. If the tree needs more than about ten category rows, the builder
  tells you to trim it for this slide.
