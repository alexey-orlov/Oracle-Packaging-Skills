# The architecture picture — built once, reviewed once

**What this is.** The pack's ONE architecture model, made after the feature list and before the deck. The three artifacts are levels of detail on it — none draws its own, none reviews it again.

**The commands**

```
python3 shared/tools/build_diagram.py <spec> --out packs/<slug>/architecture.json
python3 ${CLAUDE_PLUGIN_ROOT}/skills/one-pager/tools/build_one_pager.py <spec> --out <dir>
```

The one-pager's strip is the canonical picture. With no Chrome for it, render the deck's architecture slide instead and say which the reviewer saw.

**Checks**

1. The model builds clean: a source with no edge, an output with no destination, an unnamed engine or an app box without the pack's name stops here, not on a slide. Fix what it reports in the pack brief, through the spec skill's fast path.
2. **One fresh-context reviewer**, model `opus`, sees only the render, the brief's `architecture` component and `shared/references/architecture-diagram.md` — never this conversation — and returns that file's nine-point checklist, pass/fail with a reason each.
3. Every fail is fixed in the model and re-rendered. Stop on a pass or after three rounds; what still fails goes to the owner in plain words, never as a rule number.
4. The picture goes to the owner in plain sentences — every box, then every arrow — so naming and direction can be checked without opening a file. `build_diagram.py` prints that summary.
5. The deck, the one-pager and the listing then render the reviewed model. An artifact that wants the picture changed changes the model and rebuilds, so all three move together.

**Bad.** "Point 4 failed: unlabelled edge."
**Good.** "The line from the dispatch system doesn't say what it sends; I've labelled it 'job status every 5 minutes' — tell me if that's wrong."

**Reads:** `architecture.{inputs[], stack[], outputs[]}`, `oracle_products[]`, `workflow.steps[]`. **Writes:** `packs/<slug>/architecture.json`.
