# Packaging coaching rules — how to generalize a delivered case into a pack

_Alex's rules, as given to Vlad in the 2026-07-24 productization sync, reviewing a capability table generalized from the delivered document-extraction case. Quotes are EN glosses of the Russian. Components are the pack-spec's: 1 problem↔solution · 2 one-liner · 3 ICP · 4 name · 5 verticals + framings · 6 capabilities/features/customization · 7 workflow + human-in-the-loop · 8 architecture · 9/10 required/optional Oracle products · 11 KPIs · 12 service-package tiers._

**1. Make the vision complete, and honestly bounded.**
*Why:* "Otherwise the client wants X, we show Y, so it doesn't fit — when actually there was only something small left to finish. **Our vision must be complete.**" The other edge: "we can't say we have a ball and we'll make soup out of it."
*Governs:* all — most visibly 1, 2, 5, 6.

**2. Find the constraints the delivery silently assumed; make each a variability axis.**
*Why:* "it rests on constraints that clearly aren't universal — did we realise that, and do we reflect that variability in this table?" One document type, one language, one nomenclature, one integration target.
*Governs:* 5, 6, 7.

**3. Derive features from the real workflow: map the table against the delivered flow diagram pane by pane, and order rows in flow order.**
*Why:* "features arise from the real workflow, don't they?" A table nobody mapped is unsynchronized by default.
*Governs:* 6, 7, 8.

**4. Give every block a plain-language row for its core job, before its quality rows.**
*Why:* asked where field extraction lives, the table answered "confidence scoring, coverage" — "my task is direct: there are fields scattered in the document that we need, and they have to be recognised. Something else is written here."
*Governs:* 6, 7.

**5. Name features at task altitude — not at component altitude, not at the pilot customer's.**
*Why:* "'Classifier' — you have to guess what classifier"; "contract header extraction" "already implies it's a contract and that it has a header. Maybe they won't be contracts." Never name the model: "not a property of the feature, and why hard-wire ourselves to it."
*Governs:* 6, 4.

**6. Split a row where the futures diverge, merge rows that are the same task, and make every distinction name what it changes.**
*Why:* "upload implies a future API import too — that's a separate feature", but two extraction passes are "conceptually the same thing: finding the fields we need". The test: "what does that lead to? What does it affect?"
*Governs:* 6, 7.

**7. The customization lens means what stays custom *after* the feature is finished — not the build backlog.**
*Why:* read the cell back as a sentence — "the feature is perfect, we come to a client, and the custom work is: *use a better model for classification*. Is that a true statement?" It isn't. The real cell: take the client's nomenclature and configure it.
*Governs:* 6, 12.

**8. Record status from the delivered system; an unverified cell carries a flag, not a mark.**
*Why:* "if it maps to types and the types differ, we've already built non-binary classification — you said binary." The tell was "I haven't seen their system, I'm assuming."
*Governs:* 6.

**9. Untested is not a capability.**
*Why:* "theoretically the LLM can do it, but we have no guarantee, no testing that it will work that way." A theoretical ability is a roadmap row, never a selling point.
*Governs:* 6, 11.

**10. Interrogate every step twice: what else can happen here, and what happens when the expected thing isn't there.**
*Why:* "what do we do with a document where we expected 5 parameters and didn't find them? We don't foresee that flow" — probed by running a restaurant menu through it. Then: "imagine the abstract task — what else can there be?" Answer in concrete variants (typo · synonym · wrong format), and state what the client must configure, not the mechanism ("a confidence score is already an implementation method").
*Governs:* 6, 7.

**11. Reconcile step names against the market taxonomy, and run a vendor gap check as its own up-front task.**
*Why:* "their human-in-the-loop isn't validation, it's human-in-the-loop exception handling." A term we can't define becomes a written question with a method attached — "google it, or rather *Claude* it" — and "then our table has to cover that". The gap prompt: "look at such-and-such vendors, and from how they structure their capabilities, highlight which steps I'm missing." Expect noise; harvest gaps only.
*Governs:* 6, 7.

**12. A vertical scenario counts only if its entities differ — not its industry label.**
*Why:* "which scenarios are, in your view, different in their **entities** — not different industries that are identical under the hood."
*Governs:* 5.

**13. Differentiate every step across the scenarios; the differences are the product.**
*Why:* "for each of the 10 steps, what the specific differences may be across each scenario — here a wide level of trust in the LLM matters, there an exact match to a pre-set list matters." One "what matters here" cell per step × scenario.
*Governs:* 5, 6.

**14. Generate for coverage, adjudicate for truth.**
*Why:* "there will be a lot of water and Claude trying to satisfy you and find differences; you then work out which actually are differences — but then you'll be more confident that you really considered all these scenarios and generalized enough."
*Governs:* all.

**15. If no row is unbuilt, the table was reverse-engineered from the delivery. Fail it.**
*Why:* "almost all rows are done, some half, some fully — and there are no undone ones. **There must be one that is definitely not done.**" Said as a repeat finding: this is the default failure mode.
*Governs:* 6 — the cheapest gate in the set.

**16. Re-decide every scope boundary as the pack's; never inherit the project's.**
*Why:* "that looks like out-of-scope in the *project*, not in our package." Write-back left the list ("any client needs it integrated at the entry and the exit"); untested extras moved onto it. Standard import/export API is product; each concrete integration is custom.
*Governs:* 6, 7, 12.

**17. Anchor the integration point and the ICP to the partner's concrete product, even when the build is product-agnostic.**
*Why:* "we don't write 'integration into some system of yours', we name the Oracle product — we decided the ICP is those who have it. Although in fact nothing is wired to it, zero. But it simplifies perception and positions it under a concrete story." When the anchor isn't obvious, go hunt for it.
*Governs:* 3, 9/10, 8.

**18. Finish the table's contents before any formatting.**
*Why:* "let's definitely finish this table next time — maybe except the styling — so that we have the table with the contents." It is the spine; deck, one-pager, demo and listing all derive from it.
*Governs:* 6 first, then everything downstream.

**19. Turn each engagement into self-acceleration skills, named post-factum from the work actually done.**
*Why:* "my discovery work de facto consisted of three steps… two are probably one skill, the third another. Do it as you go — our goal on the way out is to give birth from each engagement to these self-acceleration skills."
*Governs:* the method itself; surfaces in 6 as an "artifact that accelerates the development" column.

---

## The process Alex prescribed

Steps 4–6 are his explicit "three-step process"; step 3 is the gap task he appended to the front of it.

1. **Start from one delivered engagement**; enumerate its workflow as N steps against the delivery diagram, in flow order (rules 3–6).
2. **Fill the lenses per step** — what the vendor pack gave · what we built and verified · what stays custom per engagement — and name the assumed constraints (rules 2, 7, 8).
3. **Vendor gap task, as its own prompt, before anything else** (rule 11).
4. **Move 1 — validate the scenario set:** "I see 10 steps and 4 principally different vertical cases — validate; maybe I'm missing an important fifth" (rule 12).
5. **Move 2 — challenge the step list against those scenarios:** "are the steps exactly the same everywhere, or am I missing one?" A corrected step list, no differences yet.
6. **Move 3 — generate the per-step differences**, seeded with hand-written examples so the model has the altitude (rule 13).
7. **Adjudicate the output yourself** (rule 14).
8. **Run the failure-path and nuance passes**; each un-built answer is an empty-circle row (rule 10).
9. **Evidence pass:** demote the untested, verify the assumed, re-decide boundaries as the pack's (rules 8, 9, 16).
10. **Completeness gate:** any rows definitely not built? Complete enough to be recognized, bounded enough to be honest? (rules 15, 1)
11. **Finish contents; formatting is a later pass** (rule 18). Then derive the external artifacts, anchored per rule 17.
12. **Close the loop:** describe post-factum what the analytical work consisted of, cluster it into 2–3 skills, write them (rule 19).
