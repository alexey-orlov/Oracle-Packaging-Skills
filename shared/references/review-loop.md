# The review loop — how the owner reviews and approves

_How every skill in this bundle behaves around the person who owns the pack, so that all of them behave the same way. Distilled from the packaging sessions of Jul–Sep 2026 (decks, one-pagers, the mini-site and the interactive walkthroughs) and the review rounds they produced. Rewritten to current truth — never appended with dated updates._

"The owner" is the person who commissioned the pack and signs off its artifacts. Everything below applies whoever that is.

---

## 1. Before building

**Clarify when the requirement is vague — ask, don't guess.** A vague brief is the one case where a question costs less than a rebuild. Ask at most one or two tight questions, and only where a wrong guess forces a rebuild rather than an edit.

**Put choices as a small set of concrete options with trade-offs, and recommend one.** Two or three options, each with a one-line business-level rationale and its grounding, and say which one you would take and why. The owner answers fast and frequently overrides the recommendation — that is the loop working, not a failed recommendation. Never present a single option as if it were the only one, and never present five. **Put all of it in the owner's words, never the method's**: each option is an outcome for the pack, the rationale is the reason and not the name of a rule, and nothing carries a research step's id, a test's id, a file or key name or a status glyph used as a count. The reader's test is `talking-to-the-owner.md`.

**Verify the owner's stated counts and lists against the source file.** "All three use cases" has turned out to be four. Check the roster, the count and the spelling against the source of truth before building around them, and say what you found.

**Inventory the sources first and say what is missing.** What exists, what is out of reach in this environment, and what has no source at all. A source the environment cannot reach is *deferred*, never *not found* — the second closes the item forever on the strength of a network failure.

---

## 2. While building

**Never silently change something the owner authored.** Text the owner wrote and called complete is layout-only for you. If it does not fit, breaks a rule, or contradicts another artifact, **flag it and leave it** — "I left your text rather than changing it silently" — and propose the change separately. This applies to headlines, one-liners, tier names, figures and any sentence the owner supplied verbatim.

**Report progress on anything long.** Silence is not progress. A long research fan-out or multi-artifact build writes intermediate output to a file early and says where; when a stage should have finished and the file has not moved, stop and work from what it already produced rather than waiting. "Alive?" is the failure signal, and it arrives too late.

**Keep the build cheap to redo.** At least one rebuild round is normal, usually the same day, and sometimes the spine of the artifact changes wholesale. Separate data from rendering, keep the copy in one place, and make a re-spine an edit to a data file rather than a rewrite of a builder.

---

## 3. Handing the artifact over

**Show renders, not descriptions.** The review artifact is the built thing: a contact sheet of the rendered slides, the PDF, the live page, the clickable walkthrough. A description of what was built is not a deliverable and will be sent back. The owner reviews the running thing.

**Deliver where the owner can reach it.** The owner is often on a different machine than the one that did the work. Put the file in the shared location beside its source, attach it in the conversation, or publish the page and hand over the link — and say explicitly where it is. A document ships as both its editable form and a rendered twin.

**Hand back an explicit open-items list, never buried.** Three buckets, in this order: (a) what still needs the owner's decision, (b) what was inferred and on what basis, (c) what has no source anywhere. Add the checks that could not be run and why. Write every line in plain words — what is missing and what it changes about the pack, not which key or check it belongs to. An artifact delivered without this list reads as finished when it is not.

**Say what changed, what was decided differently, and why.** A short TLDR at the top. Where you deviated from the brief or from the recommendation, name the deviation and the reason; do not let it be discovered.

**List every synthetic figure.** In a demo or any illustrative artifact, name each number that is invented, and each screen or element that has no real counterpart, with the reason it was drawn that way.

---

## 4. The corrections that come back

**The owner's correction format is a screenshot of the offending block plus a few words.** Expect terse pointers of the shape "slide 5, remove the outcome claims, the block on the screenshot". Resolve the target from the image, not from a full written spec, and confirm in one line which block you understood before rebuilding it. The owner never approves silently — approval arrives as a numbered list, and every numbered item is a change.

**Fast path for a one-block rebuild.** When the correction targets a single block, slide, screen or paragraph, rebuild and show that one thing. Do not re-run the whole pipeline, re-render the whole deck or republish the whole page before showing it, and do not re-open settled decisions elsewhere in the artifact. Show the one block, then fold it into the full artifact once it is accepted. Reserve the full rebuild for a re-spine.

**Generalize the correction, then close the loop out loud.** Every correction is a class of mistake, not one instance: find the underlying rule, apply it to the work in hand, write it to the reference file that owns it (this bundle's `shared/references/`), and then **say in one line what you generalized and where you wrote it, and ask the owner to correct the generalization itself**. Over- and under-reaching are both common, and only the owner can tell you which happened. A rule that lives only in a conversation will be re-broken next round.

**Turn every new rule into an automated check in the same pass.** If the rule can be asserted by the linter or a checker, assert it there and then. A rule that is written down but not checked survives one rewrite at best.

---

## 5. The gate before "done"

An artifact is done when all of the following hold, in order:

1. The artifact is built from the signed-off pack spec, and any required value it could not find sent the owner back to the spec rather than being invented.
2. The clearance linter is green, the banned-vocabulary and deny-list sweeps are green, and any check that could not run is listed. To the owner this is one plain line — "the automatic checks passed", or "one check found: <the finding, in plain words>" — never a tool name or a raw checker output.
3. The artifact has been rendered and looked at — every changed slide, page or screen, at every width that matters for that medium.
4. It has been delivered where the owner can reach it, in the forms they use.
5. The handover carries the TLDR, the deviations, the synthetic figures and the open-items list.
6. What changed and why is recorded in the pack's own provenance, and any rule that moved has been rewritten in the reference file that owns it.

---

## 6. What the owner supplies, and what they want before approving

**Inputs only the owner can provide** — ask for them once, early, as a list, and treat each as a declared input rather than something to invent: the raw engagement material (statement of work, PoC deck, recordings, feature lists, transcripts, existing artifacts); customer-name and figure approvals; imagery rights and any brand assets; marketplace, success-story and video URLs; the contact and mailbox for each channel; the destination folder or site the artifact ships to; and any environment endpoint a build needs. Nothing on this list is ever guessed, and an artifact prints nothing that depends on an input still outstanding.

**Before approving, the owner wants:** the running artifact to click through themselves, a TLDR of what changed, the list of anything synthetic or inferred, and the decisions that remain their. Give them those four things in that order, and keep the message short enough to read on a phone.
