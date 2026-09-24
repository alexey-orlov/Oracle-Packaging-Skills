# The executive summary — one slide in the host deck's style

**What this is.** The whole pack on one slide for an executive audience, built on the host deck's own master so it pastes in unchanged and renumbers itself (else the shipped brand base). What each block holds: card `exec-summary-blocks`.

    shared/tools/py exec-summary/tools/build_exec_summary.py <spec> --out <dir> --fit-report [--channel internal|partner_print] [--host-deck <pptx>] [--with-closing]

Exit 0 clean · 1 a box overflows · 2 spec error.

**The layout.** Six blocks, two rows by three: use case · solution layers · proof of value, over service packages · capabilities · planned next steps; a footnote; the internal contact block; speaker notes that name the cut.

**Checks**

1. The channel is `internal` by default, since the slide usually lands in an internal section deck; `partner_print` for a partner deck, with the external name variant and the partner clearance. Both cuts carry every tier's price, the partner cut each with its disclaimer.
2. With `--host-deck`, built on that master (the builder prints the layout it matched), never re-themed by hand.
3. The fit report is clean: overflow is cut, not shrunk; an `--allow-overflow` build never ships.
4. One slide, plus the host's closing slide only when asked; on the shipped base `--with-closing` is ignored with a note.
5. No new visual language: the host deck's shapes and colours, the deck's ladder, never an invented diagram.
6. Look at the render (`deck/tools/render_probe.sh` says how): the title on one line, the ladder top to bottom, the prices aligned, no panel half filled, the footnote within two lines.

**The review pack adds** what was compressed or dropped to fit, by the block's name. **Delivery:** `<Pack name> - Executive summary - Oracle.pptx`, with the slide number where it goes when a host deck was given.

**Reads:** `meta.name_variants.internal_slide`, `one_liner`, `exec_summary.*`.
