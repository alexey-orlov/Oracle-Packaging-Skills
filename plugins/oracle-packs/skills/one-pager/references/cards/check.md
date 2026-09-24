# The automatic checks

**What this is.** Three shared checkers on this skill's files, before anything reaches the owner: clearance and naming, consistency against the spec, the diagram.

```
shared/tools/py shared/tools/lint_artifact.py <the pdf and the html> --channel <channel> --spec <spec>
shared/tools/py shared/tools/check_consistency.py <spec> <the html>
shared/tools/py shared/tools/check_diagram.py <spec> --one-pager <the html> --channel <channel>
```

**Checks**

1. Lint on this artifact's own channel and files. Never lint a mixed output directory on one channel: it flags another cut's name variant and hides nothing real.
2. All exit 0, or nothing ships. A rule "not evaluated" (no `pdftotext`) has not passed: install it or say so.
3. Consistency: every price, duration and figure equals the spec to the character. An absent component is information; a present one that differs is a finding.
4. Fix a finding in the artifact, or in the spec through the fast path, never in the built page.
5. The strip draws the pack's one model, reviewed once in the build, with **every** system and edge label the deck carries — a destination-only system gets its own box. Drift is fixed by rebuilding; a wrong picture is fixed in the brief.
6. Look at the render, not only the counts: the contact block fully on the page, no scope line orphaning a word, capability marks rising left to right, every figure footnoted.
7. The owner hears one plain line — the checks passed, or what one found and what you did. Never a tool name, a rule code or raw output.

**Bad.** "ART104 on line 212, CON003 x2 — see the matrix."
**Good.** "The checks passed. One figure was missing its footnote; it is back."

When a finding needs interpreting: `shared/references/naming-and-clearance.md`; diagram rules: `shared/references/architecture-diagram.md`.

**Reads:** `clearance.*`, `meta.name_variants`, `packages.tiers[]`, `kpis[]`, `contacts.<channel>`, `architecture.*` (through the model).
