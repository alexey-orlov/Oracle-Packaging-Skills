# The automatic checks

**What this is.** What every artifact passes before the owner sees it, run on that artifact's own file and channel. The owner hears one plain line about it.

| Artifact | Channel | Its own check, first |
|---|---|---|
| Feature list | `internal` | — |
| Sales deck | `partner_print`, or `internal` | `deck/tools/lint_deck.py <pptx> --spec <spec> --channel <c>`, then `shared/tools/check_diagram.py <spec> --deck <pptx> --channel <c>` |
| Sales one-pager | `partner_print`, or `internal` | `shared/tools/check_diagram.py <spec> --one-pager <html> --channel <c>` |
| Executive summary | `internal`, or `partner_print` | — |

Then for each: `shared/tools/lint_artifact.py <file> --channel <c> --spec <spec>` (the one-pager's PDF and HTML together) and `shared/tools/check_consistency.py <spec> <file>`. Every command runs as `shared/tools/py <tool>`.

**Checks**

1. Lint each artifact alone, on its own channel: a mixed folder on one channel reports another cut's name variant and hides nothing real.
2. Everything exits 0 before anything is shown. A rule reported "not evaluated" (no `pdftotext`) has not passed: install it or say so.
3. Every price, duration and figure equals the spec to the character. An absent component is information; a present one that differs is a finding.
4. A finding is fixed in the spec, through the spec skill's fast path, or by rebuilding; never by editing the built file, loosening a check or shrinking type below its floor.
5. Diagram drift is fixed by rebuilding; a wrong picture is fixed in the brief, and all three drawings follow.

**Bad.** "ART104 on line 212, CON003 x2 — see the matrix."
**Good.** "The checks passed. One figure was missing its footnote; it is back."
