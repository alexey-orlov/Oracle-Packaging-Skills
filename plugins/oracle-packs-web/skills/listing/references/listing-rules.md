# Listing rules — the owner's standing rules, as checkable statements

Every rule below was won in a review round on a live practice site. Each is
written so it can be **checked**, not admired: a person or a script can hold the
draft against it and say pass or fail. Where `tools/check-grammar.js` already
asserts one, the line says **[checker]**.

The standing discipline behind all of them: **turn every new owner rule into a
checker assertion, so it survives the next rewrite.** A rule that lives only in
prose is a rule the next rebuild loses.

---

## A · Content

**A1. Every word lives in the data file.** Renderers read data and invent
nothing. Check: no literal copy string in a page renderer for this product.

**A2. No invented facts, numbers, customers or URLs.** Every claim traces to a
signed-off source. Check: each clause of `oneLiner`, `metrics[]`, `caseStudy` and
`jumpstart` maps to a line in the pack spec with a `source`. An unsupported
clause is **dropped**, never swapped for a different claim.

**A3. No customer name or logo in anything shipped** — copy, alt text, captions,
data files, or unreferenced files under the deployable root. Describe a customer
by industry and scale, with nothing that back-solves to one company. **[checker]**
Check: the deny-list gate passes *and* a shell sweep of the publish root returns
nothing. Clearance is **revocable** — a name cleared in one round can be
withdrawn in the next, so re-check every round rather than trusting a prior pass.

**A4. Unreferenced is not unshipped.** Anything that must never ship lives
**outside** the publish root. Whole-tree publishes carry unreferenced files, and
a link-shared preview makes them downloadable by path. **[checker]** Check: the
banned asset folder does not exist under the site root, and a post-publish file
listing shows nothing that should not be live.

**A5. No partner-standing claim.** No tier, no award, no status. What may be
said is joint delivery. Check: grep the entry for tier and award vocabulary.

**A6. Canonical vocabulary per axis.** The platform chip carries the facet's
canonical vendor product name, verbatim and spelled the vendor's way. Engine and
system specifics live on the Technology tab. **[checker]** Check: `tags[1]`
equals the facet label exactly; no abbreviation of a vendor product name
anywhere; no product-specific variant of a platform name.

**A7. A price never ships without its disclaimer.** Check: every rendered price
has a footnote in the same card.

**A8. Only the proof-of-value price ships.** Integration and Scale read
`Scoped per engagement`; every other package price goes in the sales materials,
not on the page. Check: `jumpstart.next[].price` carries a figure only where a
signed-off source publishes one, and no money figure appears outside
`jumpstart.investment` and `jumpstart.next`.

**A9. The three tiers are named `PoV Jumpstart` · `Integration` · `Scaling`.**
On the listing the PoV tier's block is titled `Jumpstart Proof-of-Value` and the
two forward steps are labelled `Integration` then `Scale`. **[checker]** Check:
`jumpstart.title` is exact; `jumpstart.next[].tier` is `Integration` then `Scale`.

**A10. Commitments are enforced, not written.** One proof-of-value duration,
identical everywhere on the site. A duration, a price or a promise is a
commitment, not copy — it is flagged for delivery sign-off, never shipped as
settled on the builder's say-so. **[checker]** Check: no other duration appears
anywhere in the data.

**A11. Never state a ceiling, a total, a denominator or a negation.** No catalog
size, no "N of M", no zero-count facet, no "not seeing your workflow?", no
"so far", no "yet". State breadth positively and only where cleared. **[checker]**

**A12. A status is said once, in one plain word** — proven / forecast /
estimated / measured / modeled / in preparation — and the footnote spends its
line on **evidence**, not on a restatement of the chip. Never the negation of
the chip's word. **[checker]** Check: the status word appears exactly once per
card; the caveat clause names what the figure is measured or modeled against.

**A13. Truthful confirmations.** Never say something was sent unless something
sent it. Check: each confirmation state maps to an outcome that can actually
occur in this build.

**A14. Nothing internal ships in site copy** — no internal taxonomy, no internal
company or product names, no internal file names or paths, no meeting dates, no
operating numbers, no personal mailbox. Check: the deny-list and banned-string
gates pass.

**A15. Only the practice contact ships:** a named person plus a shared practice
mailbox, never a personal one. **[checker]**

---

## B · Messaging

**B1. Persona first, in the reader's words.** Every headline and lead is written
from the seat of (a) a partner rep opening the page live on a call and (b) an
enterprise buyer reading alone. Check: read the headline out loud as the rep —
would they say it to a customer?

**B2. No counts, no taxonomy, no packaging vocabulary in copy.** "seven
products", "three workflow patterns", "packaged", "ready-to-run", "accelerator
pack", "pods", "scoped", "evaluation-first" are internal. A number is a headline
only when the number is the reader's information — a price, a duration.
**[checker]** for the packaging phrases in `oneLiner`.

**B3. One-liners state the job and the outcome, never the packaging.** Two
lengths: a full `oneLiner` and a rep-sayable `shortLine`. **[checker]** Check:
the one-liner would still be true and useful if the pack were sold a different way.

**B4. Heading budgets, measured on the rendered page.** H1 two to four words,
≤ ~24 characters a line, ≤ 2 lines. H2 ≤ 5 words, ≤ ~30 characters. Light-band
title ≤ ~28 characters. **The argument moves into the lead.** Check: count on
the page at 375 px, not characters in the file; no lone short word on a line.

**B5. Structure before copy.** Audience → positioning as distinct from the
sibling page → three or four messages, each answering a reader problem → one
screen per message → **length target set up front**. A page is an argument, not
an inventory. Check: name the four messages before writing a sentence.

**B6. Cut any block that carries no message.** The owner removes more than he
adds. Check: for each block, state the one message it carries; if you cannot,
it goes.

**B7. Repetition limits.** No content word three times on one screen. One word
for one thing across the whole piece. No claim in more than two places. Check:
word-frequency pass before delivering.

**B8. Say what is here, never how many and never what is not.** Check: no
sentence whose subject is an absence.

---

## C · Design and grammar

**C1. One component grammar across every listing.** Each information type has
one fixed visual form — verticals get icons, features get lists, metrics get
tiles — and every product fills every slot. **[checker]** Check: the checker
prints OK; a slot with no fact is filled qualitatively, never omitted.

**C2. Absence renders as an empty container, never a dead control.** An optional
asset renders only where it exists; the control is not drawn otherwise.
**[checker]** Check: every config switch that is an empty string renders nothing.

**C3. Overview block order is fixed and priority-ordered:** problem ↔ solution →
features as workflow steps **with a frame per step** → vertical use cases as a
tabbed component → ROI metrics in a side rail.

**C4. Architecture ≠ capability.** Technology is an architecture layer diagram
(with per-item required/optional flags) **plus** a capability list grouped by
workflow stage. "How it runs" never gets its own block. **[checker]**

**C5. The packages block sells one idea** — pilot fast, low risk, tangible
output. Deliverables are restated as **customer outcomes**. Check: read each
`outcomes[]` line — does it name what the customer has afterwards, or what we
hand over?

**C6. Three tag families, three visual codes**, each with its own icon and
tooltip: workflow pattern (outlined chip) · platform (filled pill = a fact) ·
availability (badge: a demo exists / listed on a marketplace). **Availability is
a capability, not a lifecycle state.** Badge density is a design constraint: a
product carrying both must not occupy the tag row heavily. **[checker]**

**C7. Owner-controlled order** via a config parameter, never derived. Equal-size
tiles. One CTA per tile. Legibility over imagery. **[checker]** for the order key.

**C8. Imagery only in the identity block**, sourced from the company's own
corpus, never the web. Body tabs are diagrammatic and structured. Check: no
photograph outside the hero; the tile and the product hero share one image.

**C9. Palette and type.** One ground, one accent per screen; display type for
headlines, light body; **at most one light band per page**; peers equal height;
line icons, **no emoji**.

**C10. Buttons and links.** An address is a link, never a filled button. A
filled button is the screen's one ask.

**C11. Mobile.** Clean at 375; the H1 still holds at 320. Check horizontal
overflow at every width.

---

## D · Process

**D1. The derived-view rule.** The site's `technology.capabilities[]` — the
capability list **by workflow stage** — is **derived** from the spec's
**Area > Category > Feature** through a per-pack mapping (`capabilities[].stage`
in the spec). It is not a copy and not a re-typing. Every feature lands in
exactly one of four stages; a feature with no stage is **reported, never
dropped**; the four stages are the same four the How-it-works stepper walks.
Check: run `tools/derive-stage-view.py` and reconcile its count against the
spec's feature count.

**D2. Seller materials are requested, not listed.** Gate on the corporate email
domain, never on a role field; promise the outcome, do not expose the inventory;
route the ineligible somewhere real. Check: the tab names no asset.

**D3. Ship the prototype with its own unconfirmed-assumptions checklist** — one
tickable line per item, in the lightest storage that does the job; the analysis
lives in the docs, not in the panel. **A checklist is for ticking, not reading.**
Check: each item ≤ one short line; no status chips, no paragraphs.

**D4. The owner's statements about his own pipeline outrank a QA finding.** A
finding may change the phrasing of an item; it may never remove it. Suppressing
the item is not a fix available to a fix round.

**D5. Absence of a record is a gap in the record.** When the owner asserts a
fact the sources do not hold, the conclusion is "the sources have a gap" — say
so and ask. Never substitute a similar-sounding thing the sources *do* hold.

**D6. Living documents.** Before updating or matching any delivered file, read
the current file **from disk**. The owner hand-edits delivered files; never
regenerate over his edits.

**D7. Three gates, all green, before publishing.** The checker prints OK · the
browser console is clean on every route · the deny-list sweep returns nothing.
Then look at every changed screen at 1440 / 1280 / 1024 / 768 / 375, and the H1
at 320. See `preview-and-publish.md`.

**D8. Surface the open items; do not resolve them.** A trademark check on a name
built on a vendor mark, image rights on corpus-sourced art, a figure with no
clearance — the listing skill **names** these and leaves them to the owner. A
pack with no cleared outcome figure takes the "no figure available" path
(qualitative tiles plus a metrics note that leads with the measure) rather than
inventing one.

**D9. A stalled background agent is not progress.** Have long-running work write
intermediate output early; when a stage should be done, check that file. On no
movement, stop it and take over from what it wrote.

**D10. Report what changed, what was decided differently and why, and what is
still open.** The owner reviews the running page, not a description, and returns
a numbered list. Expect a rebuild round.

---

## E · The self-check before handing a listing over

Run these in order; each is a yes/no.

1. `node tools/check-grammar.js --site-root <site>` prints **OK**.
2. The deny-list sweep over the publish root returns nothing.
3. The browser console is clean on the product's five tabs.
4. Every heading is inside its budget **on the rendered page at 375 px**.
5. Every number on the page has a qualifier or a footnote, and its status word appears once.
6. Only the proof-of-value price is on the page.
7. One duration for the proof of value, everywhere.
8. Each block carries one message you can state in a sentence.
9. No sentence whose subject is an absence, a total or a denominator.
10. The one-liner would still be true if the pack were sold a different way.
11. Every claim maps to a spec line that carries a `source`.
12. The open items are listed for the owner, not resolved by the builder.
