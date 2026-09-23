# The automatic checks

**What this is.** Three things between a clean build and the owner seeing the slide: look at the render, then run the clearance linter and the consistency check.

```
bash ../deck/tools/render_probe.sh     # prints how to render on this machine
python3 shared/tools/lint_artifact.py <the pptx> --channel <channel> --spec <spec>
python3 shared/tools/check_consistency.py <spec> <the pptx>
```

**Checks**

1. The fit report exits 0 first. A slide with an overflowing box is not checked, it is cut.
2. Look at the render — one slide, one image. Counting boxes is not looking: the title on one line, the ladder reading top to bottom, the tier prices aligned, no panel half-filled, the footnote within two lines.
3. Lint on this artifact's own channel and on this file alone. Never lint a mixed output directory on one channel: it reports another cut's name variant as a finding and hides nothing real.
4. Both checkers exit 0, or nothing ships. A rule reported "not evaluated" is not a rule that passed.
5. Consistency: every figure, price and duration on the slide equals the spec to the character. An absent component is information; a present one that differs is a finding, fixed in the artifact or in the spec through the spec skill's fast path — never by hand-editing the file.
6. What the owner hears is one plain line: the checks passed, or what one of them found and what you did about it. Never a tool name, a rule code or raw output.

**Bad.** "ART104 + CON005 — see the matrix, rebuilding."
**Good.** "The checks passed. One figure was still the old one from the deck; the slide now carries the current one."

Long form behind the codes, read only when a finding needs interpreting: `shared/references/naming-and-clearance.md`.

**Reads:** `clearance.*`, `meta.name_variants`, `kpis[]`, `packages.tiers[]`.
