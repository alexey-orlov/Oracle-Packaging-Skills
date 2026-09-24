# The architecture picture — built once, reviewed once

**What this is.** The review of the pack's ONE architecture model, after the feature list and before the deck. Every artifact builds it from the brief with one function, so it is never stored; none draws its own, none reviews it again.

**The commands**

```
shared/tools/py shared/tools/build_diagram.py <spec>
shared/tools/py ${CLAUDE_PLUGIN_ROOT}/skills/one-pager/tools/build_one_pager.py <spec> --out <dir>
```

The one-pager's strip is the canonical picture. With no Chrome for it, render the deck's architecture slide instead and say which the reviewer saw.

**Checks**

1. The model builds clean: a source with no edge, an output with no destination, an unnamed engine or an app box without the pack's name stops here, not on a slide.
2. **One fresh-context reviewer**, model `opus`, sees only the render, the brief's `architecture` component and `shared/references/architecture-diagram.md` — never this conversation — and returns that file's nine-point checklist, pass/fail with a reason each.
3. Every fail is fixed in the brief's `architecture`, through the spec skill's fast path, and re-rendered; there is no model file to edit. Stop on a pass or after three rounds; what still fails goes to the owner in plain words, never as a rule number.
4. The picture goes to the owner in plain sentences — every box, then every arrow. `build_diagram.py` prints that summary.
5. A later change to the picture is a change to the brief, so the deck, the one-pager and the listing move together. The pass is one line in `<work>/decisions.md` with the spec stamp.

**Bad.** "Point 4 failed: unlabelled edge."
**Good.** "The line from the dispatch system doesn't say what it sends; I've labelled it 'job status every 5 minutes' — tell me if that's wrong."

**Reads:** `architecture.{inputs[], stack[], outputs[]}`, `oracle_products[]`, `workflow.steps[]`. **Writes:** one line in `<work>/decisions.md`.
