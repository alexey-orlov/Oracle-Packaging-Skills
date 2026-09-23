# The automatic checks

**What this is.** Two shared checkers, run on the files this skill wrote before anything reaches the owner: the clearance and naming linter, and the consistency check against the spec.

```
python3 shared/tools/lint_artifact.py <the pdf and the html> --channel <channel> --spec <spec>
python3 shared/tools/check_consistency.py <spec> <the html>
```

**Checks**

1. Lint on this artifact's own channel, on this artifact's own files. Never lint a mixed output directory on one channel: it reports another cut's name variant as a finding and hides nothing real.
2. Both exit 0, or nothing ships. A rule reported "not evaluated" (no `pdftotext`) is not a rule that passed — install it or say so.
3. Consistency: every price, duration and figure on the page equals the spec to the character. An absent component is information; a present one that differs is a finding.
4. A finding is fixed in the artifact, or in the spec through the spec skill's fast path — never by editing the built page silently.
5. Look at the render, not only the counts: the contact block fully on the page, no tier scope line orphaning a single word, the capability marks reading left to right as an increasing ladder, every figure carrying its footnote, the proof attribution matching the channel.
6. What the owner hears is one plain line — the checks passed, or what one of them found and what you did about it. Never a tool name, a rule code or raw output.

**Bad.** "ART104 on line 212, CON003 x2 — see the matrix."
**Good.** "The checks passed. One figure was missing its footnote on the page; it is back."

Long form behind the codes, read only when a finding needs interpreting: `shared/references/naming-and-clearance.md`.

**Reads:** `clearance.*`, `meta.name_variants`, `packages.tiers[]`, `kpis[]`, `contacts.<channel>`.
