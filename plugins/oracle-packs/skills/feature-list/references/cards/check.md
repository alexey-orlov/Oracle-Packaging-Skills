# The checks before showing it

**What this is.** The automatic pass on the written .docx, run before the owner sees anything.

**The command.** `shared/tools/py shared/tools/lint_artifact.py <file> --channel internal --spec <spec>`.

**The feature list is the `internal` cut** — the pack's internal/partner spine document, and `internal` is the channel the tools README and `/oracle-packs:build` use for it. When a copy goes to an Oracle seller as it stands, lint it again on `partner_print` and expect the channel's name variant (sentence case) to be the only difference.

**Checks**

1. Every feature has a status.
2. No area without a customization line.
3. No price and no customer name anywhere in the document — the lint is clean on `internal` before anything is shown.
4. Counts per area match the spec: areas, categories and features.
5. A second run on `partner_print` differs only in the name variant; any other finding is a real one and is fixed, not waved through.

**Good.** The `partner_print` run reports one finding, the sentence-case name variant, and it is named as such.
**Bad.** A finding dismissed as "expected" without saying which one it was.

**Reads:** the built .docx and the confirmed spec. Name variants per audience: `shared/references/naming-and-clearance.md`. Writes nothing.
