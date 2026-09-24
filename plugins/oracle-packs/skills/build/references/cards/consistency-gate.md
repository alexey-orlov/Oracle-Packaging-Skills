# The consistency gate

**What this is.** The automatic pass after the last document artifact and before the web handoff: one cross-artifact check, one lint per artifact on its own channel, the deck's shape check, the diagram check.

**The commands.**

- `shared/tools/py shared/tools/check_consistency.py <spec> <every produced file>`
- `shared/tools/py shared/tools/lint_artifact.py <file> --channel <channel> --spec <spec>`, **once per artifact, on its own channel** — feature list and executive summary `internal`, deck and one-pager `partner_print`; the listing `customer_site` and the walkthrough `demo`, both in the web plugin.
- `shared/tools/py ${CLAUDE_PLUGIN_ROOT}/skills/deck/tools/lint_deck.py <deck.pptx> --spec <spec> --channel partner_print` — re-run here on the approved file.
- `shared/tools/py shared/tools/check_diagram.py <spec> --deck <deck.pptx> --one-pager <one-pager.html>` — all three still draw the one architecture model the brief gives (add `--site <diagrams.js> --slug <slug>` once the listing is in).

**Checks**

1. Never lint a whole output directory on one channel: it reports the internal cut's name variant as a partner-print finding and hides nothing real.
2. All four — consistency, per-artifact lint, deck shape check, diagram check — are clean before the web handoff.
3. Diagram drift is fixed by rebuilding the artifact from the brief, never by editing a built file; a wrong picture is fixed in the brief and all three follow.
4. A ✗ in the consistency matrix is fixed in the artifact, never by editing the spec silently. Where the spec is what is wrong, say so and send the user to the spec skill's fast path.
5. Nothing internal-only survives in a partner or customer cut: contract values, named accounts, capacity numbers.
6. The owner hears one plain line — the checks passed, or what one found and what you did. Never a tool name, a channel word or raw output.

**Reads:** the confirmed spec and every produced file. Name variants per audience: `shared/references/naming-and-clearance.md`.
