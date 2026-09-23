# Building the slide

**What this is.** One slide that puts a whole pack in front of an executive audience, built on the host deck's own master so it pastes in unchanged and renumbers itself. The six blocks: `shared/references/anatomy/artifact-exec-summary.md`. What goes inside them: card `blocks`.

```
python3 tools/build_exec_summary.py <spec> --out <dir> --fit-report \
        [--channel internal|partner_print] [--host-deck <pptx>] [--with-closing]
```

Exit 0 clean · 1 a box overflows · 2 spec error. Needs `pyyaml`, `python-pptx` and `Pillow`.

**Checks the build must pass**

1. The channel is settled first. `internal` is the default here: the slide usually lands in an internal solutions-review or section deck and takes the internal name variant. `partner_print` takes the external variant and the partner clearance rules. When it has to be asked, ask "who will see this slide": "our own team", or "Oracle and SoftServe sellers". Store both values; show neither.
2. With `--host-deck`, the slide is built on that deck's own master, and the builder prints which layout it matched. Never a slide built elsewhere and re-themed by hand. Without it, the shipped brand base.
3. The fit report is clean. Overflow is cut, not shrunk: `--allow-overflow` exists for review builds and is never how a slide ships.
4. No new visual language — the host deck's own shapes and colours, and the deck's existing diagram rather than an invented one.
5. One slide, plus the host's closing slide only when asked. On the shipped base there is no closing layout, so `--with-closing` is ignored with a note: correct, not a failure.
6. Delivered as `<Pack name> - Executive summary - Oracle.pptx` — with the slide number where it should be inserted whenever a host deck was given.

**Reads:** `meta.name_variants.internal_slide`, `one_liner`, `problem_solution`, `architecture.stack[]`, `packages.tiers[]`, `verticals[]`, `capabilities[]`, `kpis[]`, `exec_summary.*`.
