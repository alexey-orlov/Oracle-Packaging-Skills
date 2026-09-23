# The consistency gate

**What this is.** The automatic pass after the last document artifact and before the web handoff: one cross-artifact check, one lint per artifact on that artifact's own channel, then the sales deck's own shape check.

**The commands.**

- `python3 shared/tools/check_consistency.py <spec> <every produced file>`
- `python3 shared/tools/lint_artifact.py <file> --channel <channel> --spec <spec>`, **once per artifact, on that artifact's own channel** — feature list `internal`, executive summary `internal`, sales deck `partner_print`, sales one-pager `partner_print`; the listing is `customer_site` and the walkthrough `demo`, both in the web plugin.
- `python3 ${CLAUDE_PLUGIN_ROOT}/skills/deck/tools/lint_deck.py <deck.pptx> --spec <spec> --channel partner_print` — the deck skill runs it before showing anything, and it is re-run here on the approved file.

**Checks**

1. Never lint the whole output directory on one channel: it reports the internal cut's own name variant as a partner-print finding and hides nothing real.
2. All three — consistency, per-artifact lint, deck shape check — are clean before the web handoff.
3. A ✗ in the consistency matrix is fixed in the artifact, never by editing the spec silently. Where the spec is what is wrong, say so and send the user to the spec skill's fast path.
4. Nothing internal-only survives in a partner or customer cut: contract values, named accounts, capacity numbers.
5. The owner hears one plain line — the automatic checks passed, or what one of them found and what you did about it. Never a tool name, a channel word or raw checker output.

**Reads:** the confirmed spec and every produced file. Name variants per audience: `shared/references/naming-and-clearance.md`.
