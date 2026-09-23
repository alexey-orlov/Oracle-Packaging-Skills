# Naming and clearance

_The operative rules for what an artifact may call things and what it may disclose, per channel. Distilled from the practice's verified vendor-naming table (checked against Oracle's and NVIDIA's own product pages 2026-09-11), the mini-site standing rules, the demo and listing review rounds, and the owner's decisions of 2026-09-18. This file is the source the artifact linter encodes; when a rule moves, rewrite it here first. Rewritten to current truth — never appended with dated updates._

---

## 1. Vendor product names

⚠ **These strings are volatile.** Oracle and NVIDIA are in a sustained rebranding wave: within one wave Autonomous Data Warehouse became Autonomous AI Lakehouse, Autonomous Database became Autonomous AI Database, 23ai became 26ai, and NVIDIA's Agent Intelligence Toolkit became the NeMo Agent Toolkit. Two of four labels in one internal draft were wrong when last checked. **Re-verify every name against the vendor's own live product page before an artifact ships**, and record the check date in the pack spec's provenance.

| Write this | Not this | Why |
|---|---|---|
| **Oracle Autonomous AI Lakehouse** | "Oracle AI Lakehouse" | The product page's own H1; the older data-warehouse URL redirects to it |
| **Oracle AI Data Platform** | **"AIDP"** in anything a customer or partner reads | Oracle never uses the abbreviation in customer-facing copy. Acceptable as internal shorthand only |
| **Oracle AI for Fusion Applications** (the umbrella) | "Oracle Fusion AI" | Not a product name — only a URL slug. The page's own title and H1 read "Oracle AI for Fusion Applications" |
| **Oracle AI Agent Studio for Fusion Applications** (the build surface) | "Fusion AI Studio" | An ambiguous link label on that page, not the product name |
| **NVIDIA NeMo Agent Toolkit** | "NVIDIA NeMo Agents" | The toolkit's own page and Oracle's own GTM blog use this exact string. **NVIDIA NeMo** is the umbrella; **NVIDIA AI Enterprise** is the commercial platform sold on OCI Marketplace |
| **OCI** · **NVIDIA AI-Q** · **cuOpt** · **VSS** | — | As written |

**There is no joint OCI + NVIDIA product brand.** The joint page is a campaign, not a SKU. A card, tile or layer naming one thing must pick a side of the "+".

**Use ids, not free text.** Every Oracle product referenced by a pack is picked from the shared catalog `shared/data/oracle-products.yaml` and carried in the spec as an `id`. A product missing from the catalog is a catalog change request, not a free-text entry — otherwise the same product is named three ways across three packs and cannot be aggregated. The catalog carries the canonical display name; artifacts render that, never a local variant.

---

## 2. Pack name by channel

The pack has **one plain, noun-led name** — the thing, not the job ("Damage assessment", never "Repair or replace"; `anatomy/name.md`) — set once by the owner in the spec. Channel variants are derived from it by a fixed rule, and nothing else varies:

| Channel | Form | Example |
|---|---|---|
| Mini-site / customer-facing web | Title case, plain name | **Workforce Optimization** |
| Internal executive slide | Plain name + "App" | **Workforce Optimization App** |
| External sales one-pager and sales deck | Sentence case, plain name | **Workforce optimization** |
| — same, where a descriptor is needed | Small subheading below the name, optional | *Accelerator App by SoftServe* |

The "App" suffix is the **internal** executive-slide convention, not a second product name: internal copy may write either the plain name or the App form, but it never travels to a customer-facing artifact. On partner print, the customer site and a demo, the channel's form is the only one — the linter (ART104) flags a Title-cased name on a sentence-case channel and any "<name> App" outside internal.

The name never carries a vendor trademark inside it: Oracle asks partners not to use Oracle marks within a product or service name. A name built on any vendor trademark needs a usage-guidelines check before launch.

---

## 3. Clearance, by channel

`clearance.customer_name_allowed[channel]` in the pack spec is the switch. Default is **false** on every channel; only an explicit, recorded approval flips one. Clearance is **revocable and has been revoked after being granted** — re-check it every round rather than trusting a previous build.

| Rule | internal | partner print (one-pager, deck) | customer site (listing) | demo |
|---|---|---|---|---|
| Customer name or logo | only if `customer_name_allowed.internal` | only if allowed | only if allowed | only if allowed |
| Anonymized descriptor when not allowed | — | required | required | required |
| Vendor (Oracle / NVIDIA) product names and interfaces | yes | yes | yes | **yes — expected and correct** |
| Vendor **logo files** | no cleared file exists — ship the wordmark as text | same | same | same |
| Oracle partner-standing claim (tier, award, "preferred") | never | never | never | never |
| "AIDP" | internal shorthand only | never | never | never |
| Prices | all tiers | all tiers, each with its disclaimer | **PoV price only**; other tiers read "scoped per engagement" | none |
| Figures | the one metric set, named attribution | the one metric set | the one metric set, anonymized attribution | synthetic only |
| Internal-only facts | yes | never | never | never |

**Anonymized descriptor.** Industry plus scale, and nothing that back-solves to the customer: "a global home-appliance manufacturer" is the shape. Not the country, not the city, not the business unit, not a distinctive product line, not a combination that leaves one candidate.

**Prices.** A price never ships without its disclaimer, and the disclaimer travels in the same visual block, not a page footer. Services and infrastructure are stated separately where both exist. Only the PoV price is published on the customer site.

**Figures — one metric set per pack.** The set is taken from the customer study and recorded once in the spec. **Attribution varies by channel; the numbers do not.** Under the customer's name where approved and appropriate, anonymized everywhere else. Two contradicting, overlapping or simply different metric sets for one pack are unacceptable — if a second set exists somewhere, one of them is wrong and the spec decides which.

**"Proven" versus "proof of value".** Say **proven** only for a delivered, accepted result in production. Say **proof of value** for a PoC or PoV result, and carry the caveat with it (illustrative, not contractual). A modelled or target figure is labelled as such, in one plain word, once. Peer claims are all or none: when outcome evidence exists for only some items in a peer set, drop the evidence row for every item rather than showing a gap next to the proven ones.

**Internal-only facts never cross a channel boundary.** Contract and deal values; named customer accounts and their own customers; headcount, POD counts and capacity commitments; internal operating numbers; OKR text and internal targets; internal reference pricing and what another customer paid; superseded price sets still living in old files; reference-architecture detail that belongs to a customer; internal taxonomy names, roadmap ceilings and gap statements; internal deck filenames and paths in any publicly fetchable file. Also: the practice's other engagements are never named in an Oracle artifact.

**Unreferenced is not unshipped.** Anything that must never ship lives **outside** the deployable or publishable root — an unreferenced file inside it is still downloadable by path. After publishing, list what is actually live and confirm.

**Demos invert one rule only.** Inside a walkthrough, vendor product names, screens and idioms are expected — matching the real product is the bar. Everything else stays synthetic: geography, identifiers, names, documents, and every companion number next to a cleared headline figure. List every synthetic figure for the owner when handing the demo over.

### The deny-list

The linter carries a word-boundary deny-list of every customer name that has appeared anywhere in the practice's source material, and fails any artifact that contains one outside an allowed channel. **The list itself lives in `shared/tools/denylist.txt` and nowhere else** — not here, not in a readme, not in a skill: one file holds those names so that reading this reference never spreads them. It is **extended, never trimmed**, with every new engagement a pack is built from. Keep it in the linter's own data file rather than inline in an artifact skill, and keep a plain `grep -ri` sweep over the build output as the second, independent gate.

### Contacts by channel

One contact per channel, set in the spec's `contacts` block and printed by the builder for the
channel it is cutting. The addresses live here and in a pack's own spec — not in a skill, not in a
reference that is about something else:

| Channel | Who | Address |
|---|---|---|
| Partner print (one-pager, deck) | The alliances contact, named with their title, as printed on the existing one-pagers | `ktram@softserveinc.com` |
| Customer site (listing) | The practice mailbox, with the same person named beside it | `oracle@softserveinc.com` |
| Internal | The person doing the packaging, with the R&D request mailbox | `RnDrequest@softserveinc.com` |

A CTA prints the address as a link, never as a filled button, and never a personal mailbox that is
not one of these three.

---

## 4. Banned vocabulary in customer-facing copy

Customer-facing means the mini-site listing, the demo, and any external one-pager or deck copy. The test for every sentence: **would the seller say it out loud on a live call?**

- **Counts, totals, denominators and ceilings.** Never print the size of the catalog ("seven products"), never "5 of 7", never a zero-count facet. A number is a headline only when the number is the reader's own information — a price, a duration.
- **Negations and absences.** No "not seeing your workflow?", no "so far", no "yet", no roadmap ceiling, no gap statement. State breadth positively and only where cleared.
- **Internal taxonomy.** "workflow pattern", "L1 / L2", block and category names from the internal use-case map, "use-case map" itself.
- **Packaging vocabulary.** "packaged", "packaged offering", "ready-to-run", "accelerator pack" **as a noun in copy** (it is what we call it internally; the reader hears a product they cannot buy), "scoped", "evaluation-first".
- **Operating-model vocabulary.** "pods", "practice unit", "delivery pod", "COE build-out", "hardening", "productization", and any name that describes our org rather than their job.
- **Status words used loosely.** A case study states its status once, in one plain word (proven / measured / forecast / estimated / modeled / in preparation), with a footnote that spends its line on evidence rather than on hedging.

**The one-liner is the exception to "customer-facing only".** Packaging vocabulary is banned inside the pack's one-liner on **every** channel, internal included. The one-liner is set once in the spec and inherited verbatim by the feature list, the deck, the one-pager, the executive summary and the listing, so "packaged from proof of value to enterprise scale" on an internal cut is the same defect three artifacts later. The linter asserts it as ART206 and names the spec, not the artifact, as the place to fix it.

**What replaces them:** the job and the outcome in the reader's words. A one-liner states what the reader gets done, never how we package it. Headings are display lines — an H1 is two to four words (about 24 characters a line, two lines at most), an H2 five words or fewer — and the argument moves into the lead. No content word three times on one screen; one word for one thing across the whole piece; no claim repeated in more than two places.

---

## 5. How the linter uses this file

`shared/tools/lint_artifact.py` is the executable form of sections 1–4. It runs over **every** artifact a skill produces — the deck's text runs, the one-pager, the feature list, the demo's data file, the listing entry — not only over web content, and a skill is not done until the linter is green.

What it checks, and where each check gets its input:

| Check | Source |
|---|---|
| Customer names outside an allowed channel | the deny-list (§3), word-boundary matched |
| Logo and asset paths for denied marks | the deny-list (§3) |
| Vendor product names spelled the canonical way; "AIDP" outside internal | §1 plus `shared/data/oracle-products.yaml` |
| Product ids resolve to the catalog | `shared/data/oracle-products.yaml` |
| Pack name matches the channel's derived form | §2 plus the spec's `name_variants` |
| Every price accompanied by its disclaimer; non-PoV prices absent from the customer site | §3 plus the spec's `packages` |
| One metric set; no figure that contradicts the spec; attribution correct for the channel | §3 plus the spec's `figures` and `kpis` |
| "Proven" used only where the spec says delivered | §3 plus the spec's `figure_status` |
| Partner-standing claims | §3, phrase list |
| Banned vocabulary, counts, negations, ceilings | §4, word and pattern list |
| Packaging vocabulary inside the one-liner, on every channel | §4 plus the spec's `one_liner` |
| Heading budgets and repetition limits, where the artifact has headings | §4 |

Two rules keep it honest. **Every new owner rule becomes a linter assertion in the same pass** that the rule is written here, or it will be lost at the next rewrite. And **a check the linter cannot perform is not a check that passed** — it reports what it could not evaluate, and that list goes to the owner with the artifact.
