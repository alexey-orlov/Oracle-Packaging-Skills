---
slug: large-document-extraction
status: confirmed
spec_version: 1
generated_with: { roadmap_version: '2026-09-22', catalog_version: '2026-10-01' }
roadmap_item_id: large-document-extraction-and-validation
roadmap_block: Document processing
---

# Large docs processing and review

- **Site:** Large docs processing and review
- **Internal slide:** Large docs processing and review App
- **External:** Large docs processing and review
- **External subheading:** Accelerator App by SoftServe
- **Note:** The name Alex settled on 2026-09-15, live on the site since; sentence case everywhere, the internal slide adds App. The earlier names (Large Document Extraction and Validation; Intelligent Document Extraction; DOX) are retired.
- **Source:** naming-and-clearance §2; the site's product name
- **Source of the name:** user:2026-09-15
- **Eyebrow:** Oracle AI & Data Solutions
- **Roadmap note:** Same item: the roadmap keeps the older name (Large document extraction & validation); the site and the pack use the settled one.

## One-liner

- **Full:** Contracts reach your systems without days of keying by hand, and a wrong rate is caught at review, not on the invoice.
- **Source:** user:2026-09-29
- **Short:** Contracts in your systems without days of keying.
- **Banned words checked:** yes
- **Note:** The full line is the site's published one-liner (round 19, kept in the 2026-10-01 so-what pass), verbatim.

## Problem and solution

### Problem

Operations staff read 60 to 100 pages of supplier terms and key rate cards into the cost system. Few can read them, so contracts queue and new partners go live late.

### Solution

Values arrive extracted, each beside its page in the agreement. The reviewer confirms each, correcting the flagged ones, so the first invoice is checked against the signed rate.

- **Source:** user:2026-10-01
- **Sub-problems:**
  - **Few can read them:** tiered rates, derived charges and exceptions take an experienced specialist, and the know-how is written down nowhere.
  - **Errors surface late:** a wrong or missed rate is found at month-end invoice matching, after the invoice is disputed or paid.
  - **Openings come in bursts:** a new location brings eight to ten agreements at once, about a month of keying.
- **Reframe:** Review instead of typing, and new partners go live sooner
- **Today:** Specialists read each agreement page by page and key every rate, tier and condition into the cost system: 3–5 days a contract, errors found at invoice matching.
- **Tomorrow:** Rates arrive extracted and cited to their page; the reviewer confirms each, guided by confidence and rule warnings, and the checked data is ready for the cost system before the first invoice.
- **Note:** The site's plates (2026-10-01 copy) with two corrections proposed with the listing change: the problem says what few can do ('read them'), and the solution says the reviewer confirms every value, as the delivered review screen requires, instead of checking only the flagged ones. The reframe is the solution plate's headline; the problem plate's headline: Every new supplier waits for a specialist to type its rates.
- **Reframe question:** What if rates were checked, not keyed for days?
- **Problem points:**
  - **Few can read them:** tiered rates and derived charges need an expert.
  - **Errors surface late:** a wrong rate is found at invoice matching.
  - **Openings come in bursts:** a new site brings eight to ten agreements.

## Who buys it

Contract operations losing days to keying and money to wrong rates

- **Source:** user:2026-10-02
- **Buyer roles:** Head of contract management; Head of procurement operations; Head of cost control or finance operations; Underwriting or policy operations lead; Credit operations lead
- **Buyer roles, operator:** Contract and data-entry specialists; Reviewers in contract, claims or credit operations
- **Buyer roles, payer:** Head of cost control or finance operations; Head of procurement operations
- **Qualifying signals:**
  - Specialists key prices, tiers and terms from documents of 30 to 200 pages by hand
  - The documents follow a recognizable family: a standard template, a rate schedule, a policy schedule
  - A wrong value costs money downstream: invoice disputes, over-payment, mis-priced cover
  - New suppliers, sites or renewals arrive in bursts that queue behind a few experts
  - The target system takes an import file or has an interface
- **Disqualifiers:**
  - Short standard forms, such as invoices, receipts or ID documents, that off-the-shelf document recognition already handles
  - Wants the data used with no human review
  - No agreed target layout, and no documents already keyed by hand to measure accuracy against
  - Documents mostly in a language the proof has not tested (English at the proof of value)
- **Buyer by industry:**
  - **Airlines and logistics:** Head of contract management or cost control; for carriers' rates, transportation procurement or freight audit
  - **Leases and supplier contracts:** Lease accounting lead or controller; head of procurement operations
  - **Insurance:** Head of underwriting or policy operations
  - **Banking and lending:** Head of credit or loan operations

## Industries

### Airlines and logistics

- **Site label:** Travel & transport
- **Framing:**
  - **Problem:** Ground-handling agreements run to 60–100 pages, and their rate cards are keyed into the cost system by hand — 3–5 days per contract, about a month to bring a new station online. A rate keyed wrong surfaces late, at invoice matching, and ground handling carries 7–12% of an airline's direct operating cost.
  - **Solution:** Each agreement's rate card arrives extracted, every rate beside the page it came from, and an operator confirms it rather than reading the agreement page by page; lease and maintenance agreements take the same path. A new station opens on time and invoices match the signed rates.
  - **Entities:** ground-handling, catering, fuel and maintenance agreements with their rate annexes; carriers' freight rate agreements
- **Status:** plausible
- **What matters here:** Services by aircraft type and tier into exact rows; one schema per contract category; errors surface at invoice matching.
- **How the entities differ:** Rate annexes per station and service; for carriers, lanes, weight breaks and surcharges.
- **Note:** A proof of value delivered for one airline's ground-handling agreements (June 2026), not yet in production, so plausible rather than proven. The problem is the site's tab, verbatim; the solution is rewritten in business words (proposed with the listing change). Carriers' freight rates fold in: the same rate-card objects.
- **Source:** site (§66 copy); br3 §2; demo-deck; research-brief: The industries
- **Icon:**
  - **File:** visuals/vertical-0-plane-departure-ink.png
  - **Name:** plane-departure
  - **Source:** Tabler Icons
  - **Creator:** Tabler Icons
  - **Licence:** MIT
  - **Source URL:** https://tabler.io/icons/icon/plane-departure
  - **File, white:** visuals/vertical-0-plane-departure-white.png

### Leases and supplier contracts

- **Site label:** Every industry
- **Framing:**
  - **Problem:** Rent schedules, escalations, break options and supplier price terms sit inside long leases and agreements, keyed into the lease or procurement system by hand and rarely re-read. A missed break date keeps rent running that could have stopped, and a wrong schedule misstates the lease liability the auditors test.
  - **Solution:** Each lease and agreement's rents, escalations, options and price terms are extracted and cited to their clause, the reviewer confirms them, and the data loads into the lease or procurement system as the contract reads, so payments and options follow the terms signed.
  - **Entities:** property, equipment and aircraft leases with their amendments; master services and supplier agreements with price schedules
- **Status:** plausible
- **What matters here:** An exact match to the lease system's import fields; the latest amendment wins; every option date sits inside the term.
- **How the entities differ:** A dated payment schedule, options and key dates instead of a rate matrix; the amendment family matters.
- **Note:** A corporate function in every industry, not a vertical, and the strongest Oracle fit: Oracle's lease accounting import fixes the lease field set. Replaces the site's Professional services tab (proposed with the listing change). Amendments applied over earlier terms are on the roadmap.
- **Source:** research-brief: The industries; site (professional-services tab, re-scoped)
- **Icon:**
  - **File:** visuals/vertical-1-building-skyscraper-ink.png
  - **Name:** building-skyscraper
  - **Source:** Tabler Icons
  - **Creator:** Tabler Icons
  - **Licence:** MIT
  - **Source URL:** https://tabler.io/icons/icon/building-skyscraper
  - **File, white:** visuals/vertical-1-building-skyscraper-white.png

### Insurance

- **Site label:** Insurance
- **Framing:**
  - **Problem:** Underwriting operations re-key coverage, limits, deductibles and endorsements from policy schedules into the policy system by hand. A missed or mis-keyed endorsement surfaces only at claim time, when the insurer pays outside the cover it priced.
  - **Solution:** Each schedule's limits, deductibles and endorsements are extracted and cited to their page, the schedule's own list of forms shows nothing is missing, and the reviewer confirms each value, so the policy system holds the cover that was sold.
  - **Entities:** declarations pages, policy schedules and endorsements; delegated-authority bordereaux
- **Status:** plausible
- **What matters here:** The schedule lists its own forms, so completeness can be checked; an endorsement changes the form it amends.
- **How the entities differ:** Coverage, limits and endorsements tied to forms instead of a rate matrix.
- **Tier note:** Claim packs, a bundle of short documents checked against the policy, need splitting and cross-document checks: on the roadmap.
- **Source:** research-brief: The industries; research-brief: What happens when things go wrong
- **Icon:**
  - **File:** visuals/vertical-2-shield-check-ink.png
  - **Name:** shield-check
  - **Source:** Tabler Icons
  - **Creator:** Tabler Icons
  - **Licence:** MIT
  - **Source URL:** https://tabler.io/icons/icon/shield-check
  - **File, white:** visuals/vertical-2-shield-check-white.png

### Banking and lending

- **Site label:** Financial services
- **Framing:**
  - **Problem:** Credit teams key covenants, margins and repayment schedules from 100-page loan agreements, and spread private borrowers' statements into the bank's template by hand. A covenant keyed wrong is found at the next test date, after lending decisions already rest on it.
  - **Solution:** Covenant definitions and thresholds, margin grids and repayment terms are extracted with the clause behind each, the reviewer confirms them, and the lending system tests each loan against what its agreement actually says.
  - **Entities:** credit agreements on standard loan-market forms, margin grids, covenant schedules, private borrowers' financial statements
- **Status:** plausible
- **What matters here:** Defined terms govern every page; covenant wording kept verbatim; two-person sign-off comes at Integration.
- **How the entities differ:** Definitions, covenants and payment schedules instead of rate rows; statements must tie out.
- **Scope note:** Listed companies' statements are out: they are already published as tagged data.
- **Source:** research-brief: The industries
- **Icon:**
  - **File:** visuals/vertical-3-building-bank-ink.png
  - **Name:** building-bank
  - **Source:** Tabler Icons
  - **Creator:** Tabler Icons
  - **Licence:** MIT
  - **Source URL:** https://tabler.io/icons/icon/building-bank
  - **File, white:** visuals/vertical-3-building-bank-white.png

### Held out

- **Note:** Considered and held for a buyer to appear; the last two fold into an industry above.
- **Candidates:**
  - Healthcare payer–provider contracts (US hospitals billing on Oracle Health; the same rate-card objects, under a price-transparency rule)
  - Telecom roaming and interconnect agreements (tariffs often arrive machine-readable)
  - Public-sector framework agreements (with leases and supplier contracts)
  - Carriers' freight rate agreements (with airlines and logistics)

### Rejected

| Name | Reason |
|---|---|
| Listed companies' annual reports | already published as tagged data (XBRL, ESEF): read the tags, not the PDF (industries research) |
| Power-purchase agreements | the destination is an energy-trading system, rarely Oracle; weak fit (industries research) |
| Insurance claim packs, now | a bundle of short documents with no answer key, checked against the policy: needs splitting and cross-document checks first (workflow and failure-path research) |

## Capabilities

### Take in the documents

- **Stage:** Collect
- **Customization in this area:**
  - The document types and file formats in scope
  - Size and language limits

| Category | Feature | Status | From tier | Customization | Specificity | Source |
|---|---|---|---|---|---|---|
| Intake | PDF and Word files read, native or scanned | available | pov | Scan quality and file formats |  | arch §3, §6.1, §6.3 |
| Intake | Many documents picked up from a repository | roadmap | integration | The repository and its folders | customer | backlog-post #9; br3 §2.2 |
| Intake | Every document's status tracked in one list | available | pov |  |  | guide §2, §3; arch §5 |
| Document type | Document type checked before anything is extracted | available | pov | The types in scope | use_case | arch §3, §8.1.1 |
| Document type | Several document types, set up without code | roadmap | scaling | A schema per document type | use_case | backlog-post #2, #10, #13 |
| Document type | Languages beyond English | roadmap | scaling | Languages per customer | customer | backlog-post #15; arch §6.1 |

### Extract the fields

- **Stage:** Extract
- **Customization in this area:**
  - The field schema and mapping rules per document type
  - The page types and the rules for each

| Category | Feature | Status | From tier | Customization | Specificity | Source |
|---|---|---|---|---|---|---|
| Reading | The schema's fields found in any layout | available | pov | The schema per document type | use_case | arch §8; br3 §7.3 |
| Reading | Tables read whole, even across pages | available | pov |  |  | arch §8.1.3 |
| Reading | Every value cited to its page and clause | available | pov |  |  | arch §6.2, §8.2 |
| Structuring | Tiers and conditions turned into one row each | available | pov | Mapping rules per document type | use_case | arch §8.1.7; br3 §6 |
| Structuring | Derived charges and formulas tied to their parent | available | integration | Derivation rules per document type | use_case | arch §8.1.7; br3 §6.2–§6.9 |
| Structuring | Amendments applied over the terms they replace | roadmap | integration |  |  | backlog-post #11; research-brief: What happens when things go wrong |

### Flag what needs a person

- **Stage:** Validate
- **Customization in this area:**
  - Business rules, thresholds and reference lists per document type

| Category | Feature | Status | From tier | Customization | Specificity | Note | Source |
|---|---|---|---|---|---|---|---|
| Checks | Confidence on every row; thin pages re-read | available | pov | Thresholds per document type | use_case |  | arch §8.1.6, §8.1.7 |
| Checks | Business-rule checks raise warnings for review | available | pov | The rule set per document type | use_case |  | arch §8.1.7 |
| Checks | Values matched to the customer's reference lists | partial | pov | The customer's lists and aliases | customer | Service names mapped to the target's catalogue today; typos, synonyms and code variants per a customer rule set next. | arch §8.1.2, §8.1.7; sync-0724; research-brief: What happens when things go wrong |
| Checks | Missing required fields flagged | roadmap | integration | Required fields per document type | use_case |  | br3 §5; sync-0724; research-brief: What happens when things go wrong |
| Checks | Terms the schema has no place for flagged | roadmap | integration |  |  |  | backlog-post #3; research-brief: What happens when things go wrong |
| Checks | Values checked against a related document | roadmap | scaling |  | industry |  | research-brief: The industries; research-brief: What happens when things go wrong |

### Review against the source

- **Stage:** Review
- **Customization in this area:**
  - The review screen's columns per document type
  - Who reviews and who approves

| Category | Feature | Status | From tier | Customization | Specificity | Source |
|---|---|---|---|---|---|---|
| Review | Each value one click from its source page | available | pov |  |  | arch §5; guide §3 |
| Review | Approve, edit or reject per row or group | available | pov | Columns per document type |  | arch §4; guide §3 |
| Review | Search, filters, added rows and AI re-reads | roadmap | integration |  |  | backlog-post #1, #6; guide §6 |
| Control | Every edit logged: who, when, before, after | available | pov |  |  | arch §5, §6.2 |
| Control | Roles, queues and sign-off limits for reviewers | roadmap | integration | Roles and limits per team | industry | backlog-post #5; research-brief: The industries |

### Hand over the approved data

- **Stage:** Load
- **Customization in this area:**
  - The export layout and the target system's import

| Category | Feature | Status | From tier | Customization | Specificity | Note | Source |
|---|---|---|---|---|---|---|---|
| Export | Approved values exported as a spreadsheet or JSON | available | pov | The target data layout | customer | Nothing exports until every row is reviewed; loading into the target system comes at Integration. | arch §3, §4; guide §3 |
| Export | Approved data loaded into the target system | roadmap | integration | The target system's import or interface | customer |  | br3 §3.3; backlog-post #12 |

### Measure and improve

- **Stage:** Improve
- **Customization in this area:**
  - The answer key and the accuracy target
  - New document types and their rules

| Category | Feature | Status | From tier | Customization | Specificity | Note | Source |
|---|---|---|---|---|---|---|---|
| Accuracy | Accuracy measured against hand-keyed answers | partial | pov | The answer key per document type | use_case |  | br3 §8; demo-deck slide 7; arch §6.2 |
| Accuracy | Reviewer corrections folded back into the rules | roadmap | integration |  |  |  | backlog-post #4 |
| Accuracy | Review time and corrections tracked per type | roadmap | scaling |  |  |  | research-brief: What the other vendors ship |
| Operations | Runs in an OCI tenancy, set up by script | available | pov |  | engine | A sandboxed tenancy in the proof of value; the customer's production tenancy from Integration. | arch §7; br3 §9.3 |
| Operations | Single sign-on, high availability and disaster recovery | roadmap | integration |  |  |  | arch §6.1, §6.2 |

## Workflow

### Inputs

| System | Detail | Data | Tier |
|---|---|---|---|
| Contract repository | or a shared drive; the documents uploaded by hand in the proof of value | agreements, leases and policies, native or scanned | manual upload in the proof of value; picked up from the repository in Integration |

### 1. Take in the documents

- **Actor:** system
- **Human in the loop:** no
- **Covers:** upload, or pickup from a repository at Integration; PDF or Word, native or scanned; the document type checked (in scope, out of scope, uncertain); size and language limits; every document's status in one list
- **Description:** Documents arrive by upload in the proof of value and from the contract repository at Integration. Before anything is extracted, each is checked against the document types the pack holds a schema for: out-of-scope documents are rejected at upload, uncertain ones go on with a warning the reviewer sees, and files over the size limit or in an untested language are stopped with a clear message.
- **If it fails:** Unknown type rejected; bundles and duplicates not covered until Integration.
- **Vertical differences:**
  - **Airlines and logistics:** carriers' rate sheets often arrive as spreadsheets
  - **Leases and supplier contracts:** a lease and its amendments arrive as one family
  - **Insurance:** policy, endorsement and schedule told apart
  - **Banking and lending:** standard loan-market form or bespoke
- **Source:** arch §3 (Pass 0, guards); guide §3; research-brief: What happens when things go wrong

### 2. Extract the fields

- **Actor:** ai
- **Human in the loop:** no
- **Covers:** each page labelled by content and read with that content's rules; tables joined across pages; every schema field found; terms taken from the prose only when written; tiers and conditions expanded into one row each, derived charges and formulas tied to their parent; units, codes and currencies normalized; duplicates removed; every value cited to its page and clause
- **Description:** Every page is labelled by what it holds (rate tables, discounts, surcharges, terms, the header) and read with the rules for that content, and tables that run onto the next page are joined. Each field the document type's schema asks for is extracted; tiers and conditions become one row per combination, derived charges point to the rate they derive from, and every value keeps the page and clause it came from.
- **If it fails:** Unclear page read with every rule; amendments not covered until Integration.
- **Vertical differences:**
  - **Airlines and logistics:** exact rows against an agreed rate layout: service, aircraft type, tier
  - **Leases and supplier contracts:** rents, escalations and options against the lease import fields
  - **Insurance:** limits, sub-limits and deductibles with the endorsement each belongs to
  - **Banking and lending:** covenant definitions verbatim, with a computable threshold
- **Source:** arch §3, §8; br3 §6

### 3. Flag what needs a person

- **Actor:** system
- **Human in the loop:** no
- **Covers:** a confidence level per row with a hint where it is doubtful; pages re-read when fewer rows come out than expected; business-rule checks (gaps in tiers, prices out of order, missing follow-on tiers, rows not covered) shown as warnings; service names matched to the target's catalogue
- **Description:** Every extracted row gets a confidence level, and a doubtful one carries a hint on what to check. Pages that yield fewer rows than expected are read again, and business-rule checks raise a warning wherever the extracted data breaks a rule, so the reviewer sees where to look closer.
- **If it fails:** A check with no answer becomes a warning, never a silent pass.
- **Vertical differences:**
  - **Airlines and logistics:** gaps in tiers and prices out of sequence
  - **Leases and supplier contracts:** payments add up; option dates inside the term
  - **Insurance:** every form on the schedule found
  - **Banking and lending:** statements tie out (on the roadmap)
- **Source:** arch §8.1.2, §8.1.6, §8.1.7

### 4. Review against the source

- **Actor:** human
- **Human in the loop:** yes
- **Covers:** the source page beside the extracted rows, one click from a value to its page; confidence badges and rule warnings; approve, edit or reject per row, per group or all; every edit logged with who, when, before and after; the review saved as it goes
- **Description:** The reviewer opens the document with its source pages beside the extracted rows and jumps from any value to the page it came from. Confidence badges and rule warnings show where to look; the reviewer decides every row (approve, correct or reject, or a whole group at once), and every edit is logged with who, when and the value before and after.
- **If it fails:** A value nobody can confirm is rejected.
- **Vertical differences:**
  - **Leases and supplier contracts:** evidence per value for the auditor
  - **Insurance:** approval limits by amount (on the roadmap)
  - **Banking and lending:** two-person sign-off (on the roadmap)
- **Source:** arch §3, §5; guide §3, §4

### 5. Hand over the approved data

- **Actor:** system
- **Human in the loop:** yes
- **Covers:** export blocked until every row is reviewed; the approved values as a spreadsheet or JSON in the target data layout in the proof of value; at Integration, loaded through the target system's import or interface
- **Description:** Nothing leaves until every row is reviewed. The reviewer then exports the approved values as a spreadsheet or JSON in the target data layout; at Integration they load through the target system's import or interface instead of a file.
- **If it fails:** Rows still unreviewed keep the export closed.
- **Vertical differences:**
  - **Airlines and logistics:** the cost system's data layout; transport systems' rate records
  - **Leases and supplier contracts:** the lease accounting system's import
  - **Insurance:** the policy administration system
  - **Banking and lending:** the lending system and its covenant tracking
- **Source:** arch §3; guide §3; br3 §3.3, §4.3

### 6. Measure and improve

- **Actor:** system
- **Human in the loop:** no
- **Covers:** accuracy field by field against documents the customer's experts already keyed (exact, equivalent, wrong, missing, invented), per section of the layout; at Integration, reviewer corrections folded back into the rules; at Scaling, new document types set up
- **Description:** Accuracy is measured field by field against documents the customer's experts already keyed by hand, per section of the layout, with missing and invented rows counted apart; the customer's lead sets the accuracy target and decides whether the proof is accepted. From Integration the reviewers' corrections are folded back into the rules, and at Scaling new document types are added with their own schema and checks.
- **If it fails:** No hand-keyed answers: the proof does not start (entry gate).
- **Vertical differences:**
  - **Leases and supplier contracts:** the lease system's import validates the load
  - **Banking and lending:** covenant figures checked against reported ones (on the roadmap)
- **Source:** br3 §8; demo-deck slide 7; backlog-post #2, #4

### Outputs

| System | Detail | Data | Tier |
|---|---|---|---|
| Cost / ERP systems | the customer's cost-management, lease or procurement system; Oracle Fusion Cloud ERP or Oracle Fusion Cloud Procurement where it holds the terms (inferred) | approved rates and terms, cited | export file in the target data layout in the proof of value; loaded through its import or interface in Integration |

### Notes

- **Source:** arch §3, §4; br3 §2.2
- **Not ours:**
  - **Matching invoices against the extracted terms:** the cost or ERP system's job, and a separate use case
  - **Deciding what to pay, renew or approve:** the buyer's decision; the pack supplies the terms
  - **Drafting or negotiating contracts:** contract lifecycle tools do it
  - **Tracking renewal, break and covenant dates after loading:** the lease, procurement or lending system tracks them
  - **Using extracted data with no human review:** a person approves every value by design
- **Integration by tier:**
  - **PoV:** Manual upload in; an export file in the target system's layout out.
  - **Integration:** Documents from the repository; data loaded into the target system; reference lists looked up.
  - **Scaling:** Several document types, sources and target systems, many documents at once.
- **Grouping note:** Twelve practitioner steps grouped into six at the buyer's checkpoints: capture, splitting and classification inside step 1; page routing, extraction and normalization inside step 2; confidence, coverage and business rules inside step 3; review inside step 4; export and loading inside step 5; accuracy, feedback and new types inside step 6.
- **Domain steps note:** Practitioner names: intelligent document processing (capture, classify, extract, validate, human-in-the-loop validation, export), exception handling and straight-through processing; lease abstraction, policy checking and credit spreading in the industries.

## Architecture

### Inputs

| System | Detail | Data | Tier |
|---|---|---|---|
| Contract repository | or a shared drive; the documents uploaded by hand in the proof of value | agreements, leases and policies, native or scanned | manual upload in the proof of value; picked up from the repository in Integration |

### Stack, top to bottom

#### Application

- **Name:** Large docs processing and review by SoftServe
- **Vendor:** SoftServe
- **Summary:** extraction pipeline and review screen
- **Items:** Document intake and type check; Page-by-page extraction with citations; Confidence, coverage and business-rule checks; Review screen and export

#### AI engine

- **Name:** NVIDIA AI-Q Blueprint
- **Vendor:** NVIDIA
- **Summary:** model serving and orchestration
- **Catalog id:** `nvidia-aiq`
- **Note:** Deployed through Oracle's AI Accelerator Pack for NVIDIA AI-Q, the stack's foundation in the delivered case (serving, orchestration, monitoring). The vision-language extraction model runs on the Dedicated AI Cluster and is picked per engagement; it is never named on a sales artifact.

#### Infrastructure

- **Name:** Oracle Cloud Infrastructure
- **Vendor:** Oracle
- **Summary:** Dedicated AI Cluster (H100), OKE, Autonomous AI Database, Object Storage
- **Items:** Dedicated AI Cluster (H100); OKE; Autonomous AI Database; Object Storage
- **Catalog id:** oci-dedicated-ai-cluster; oci-kubernetes-engine; oracle-autonomous-ai-database; oci-object-storage

### Outputs

| System | Detail | Data | Tier |
|---|---|---|---|
| Cost / ERP systems | the customer's cost-management, lease or procurement system; Oracle Fusion Cloud ERP or Oracle Fusion Cloud Procurement where it holds the terms (inferred) | approved rates and terms, cited | export file in the target data layout in the proof of value; loaded through its import or interface in Integration |

### Notes

- **Source:** arch §3, §4
- **Note:** Scanned pages are read by the vision-language model directly, with no separate OCR step. The pipeline is file-based in the proof of value, set up by script in a sandboxed OCI tenancy.
- **Platform overlap note:** Oracle already reads supplier invoices (Fusion Payables), pulls a few key terms from text contracts (Fusion Enterprise Contracts) and extracts fields with a generative model (OCI Document Understanding; its documentation shows no review screen or business-rule checks). This pack is for long agreements whose rate tables and conditions must become hundreds of validated rows, each reviewed against its cited page, handed to the system that pays or bills on them (an Oracle application: inferred). Positioning ours, not yet agreed with Oracle.

## Oracle products

| Id | Name | Role | Why | At PoV | At Integration | At Scaling | Note | Name note | Inferred | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| oci | Oracle Cloud Infrastructure | required | Runs the pack in an OCI tenancy: a Dedicated AI Cluster (H100) serves the vision-language extraction model, OCI Kubernetes Engine (OKE) runs the app and the AI-Q stack, Object Storage holds the uploads, with the network and access around them. | A sandboxed tenancy, set up by script within the proof | The customer's production tenancy | The same tenancy across document types and business units |  |  |  | arch §4, §7 |
| oracle-autonomous-ai-database | Oracle Autonomous AI Database | required | Holds each document, every extracted value in the target layout with its citation, and the audit trail of reviewer edits. | Inside the proof's tenancy | A production instance | One store across document types and business units |  | The delivered case's 'Oracle Database 26ai' ran as Autonomous Database; the catalog name is Oracle Autonomous AI Database. |  | arch §4, §7.1.1 |
| oracle-fusion-cloud-erp | Oracle Fusion Cloud ERP | optional | Its lease accounting import takes each lease's payments, escalations and options, so extracted lease terms load without rekeying. | An export file in its import layout | Loaded through its import or interface | Loaded through its interface across business units, with telemetry per document type | Oracle's lease import fixes the lease field set (industries research). In the source case, cleared invoices flow on to the customer's Oracle ERP for payment. |  | yes | research-brief: The industries; br3 §2.2 |
| oracle-fusion-cloud-procurement | Oracle Fusion Cloud Procurement | optional | The home of supplier agreements' price terms: approved terms written into its agreements instead of keyed. | Terms exported in its import layout | Terms written into its agreements through its interface | Written through its interface across business units, with telemetry per document type | Its own contract agent summarizes key terms from text contracts; it does not turn price tables into rows (vendor research). |  | yes | research-brief: What the other vendors ship |
| oracle-fusion-cloud-scm | Oracle Fusion Cloud Supply Chain and Manufacturing (SCM) | optional | Its transportation management holds carriers' rates as rate records, so extracted freight rates load without rekeying. | Rates exported in its import layout | Loaded as rate records through its interface | Loaded through its interface across carriers and regions, with telemetry per document type |  | Oracle Transportation Management is the module that holds the rates. | yes | research-brief: The industries |

## Metrics

- **Kpis note:** One set: three business metrics, results to follow. The proof of value measured one stage, the extraction: 5–15 minutes a contract for agreements of up to 40 pages (3–4 for up to 15), printed in the proof's headline and story, never as an end-to-end time. Earlier drafts' 'up to −20% manual effort' (a target) and '5–15 minutes for 60–100 pages, review included' (an estimate) are not printed. Two technical criteria print only as 'Proof accepted when'.

### Time to get a contract's rates into the cost system

- **Kind:** business
- **Signed off by:** Head of contract management
- **Formula:** Working days from a signed agreement to its rates checked and in the cost system, review included
- **Baseline:** 3–5 days a complex agreement, read and keyed by hand (the customer's own estimate)
- **Figure:** -
- **Direction:** down
- **Chip:** Days to load a contract ↓
- **Label:** Today 3–5 days an agreement, keyed by hand
- **One-pager label:** Days from signed agreement to loaded rates
- **Note:** The proof of value timed the extraction alone: 5–15 minutes a contract for agreements of up to 40 pages, ready for review. The review was not timed, and in the source case operators still entered the checked rates by hand, because the cost system has no import.
- **Source:** br3 §2.4; demo-deck slide 5; guide §6

### Time to bring a new supplier or site live

- **Kind:** business
- **Signed off by:** Head of procurement operations
- **Formula:** Calendar days from a new site's or supplier's signed agreements to their rates checked and in the cost system
- **Baseline:** About a month for a new station's 8–10 agreements (the customer's own estimate)
- **Figure:** -
- **Direction:** down
- **Chip:** Time to go live ↓
- **Label:** Today about a month for a new station
- **One-pager label:** Days to bring a new site live
- **Note:** The source case's onboarding measure; the proof did not run a whole station.
- **Source:** br3 §2.4; arch §2.3

### Invoice variances from wrong rates

- **Kind:** business
- **Signed off by:** Head of cost control
- **Formula:** Invoice variances traced to a wrong or missing contract rate, per month
- **Baseline:** Measured at the start of the proof from the last quarter's invoice variances
- **Figure:** -
- **Direction:** down
- **Chip:** Wrong-rate invoices ↓
- **Label:** Baseline: last quarter's invoice variances
- **One-pager label:** Invoice variances from wrong rates
- **Note:** The customer estimates billing errors (rate mismatches, duplicate charges, flights not operated) add about 1% to ground-handling spend; only the rate share is this pack's lever.
- **Source:** arch §2.3; br3 §2.5

### fields match the answer key

- **Kind:** technical
- **Formula:** Fields that match documents the customer's experts already keyed ÷ fields expected, per section of the layout, with missing and invented rows counted apart
- **Figure:** -
- **Note:** The source case's validation method; the threshold is agreed in the first weeks.
- **Source:** br3 §8

### values cite the right page

- **Kind:** technical
- **Formula:** Extracted values whose page and clause reference points to the right place ÷ extracted values, on a checked sample
- **Figure:** -
- **Note:** The source case's citation-quality check.
- **Source:** br3 §8.2

## Packages

- **Status:** confirmed
- **Anchor line:** Runs on OCI beside the cost or ERP system that pays on the extracted terms.
- **Value for Oracle and NVIDIA:** {Customer}'s extraction runs on OCI: the vision-language model on a Dedicated AI Cluster of H100 GPUs, the NVIDIA AI-Q stack on OCI Kubernetes Engine (OKE) and the results in Oracle Autonomous AI Database. Each further contract category and station adds documents to the same environment.
- **Value for the client:** {Customer}'s reviewers confirm each rate beside its clause instead of reading the whole agreement, and the rules a few operators held are now written down, so interpretation errors are caught before they reach an invoice.
- **Legend:** ◐ partial · ● included · ●● multi-type / advanced
- **Source:** op-0910 and deck-0910 (prices, durations, packages detail); site Delivery tab; backlog-post; research-brief

### PoV Jumpstart · S

- **Id:** pov
- **Scope:** One document type by upload, cited and reviewed.
- **Duration:** 8–8 weeks (target 8, hard cap 10, status confirmed)
- **Duration label:** 8 weeks
- **Duration note:** The package deck's 2 months (2026-09-10), printed in weeks; the delivered case ran 8 weeks of build and 2 of acceptance, which the package counts outside the proof. The sample documents, the hand-keyed answers and named reviewers are an entry gate, not proof weeks.
- **Services price:** €75K · indicative · Indicative, confirmed at scoping; no cloud charge to the customer during the proof.
- **Infrastructure price per month:** €0 · confirmed · Indicative, confirmed at scoping; no cloud charge to the customer during the proof.
- **What you get:**
  - One document type's core fields extracted from your own documents, native or scanned
  - Every value cited to its page, with doubtful rows and rule breaks flagged
  - A review screen: the source beside the rows; approve, edit or reject; every edit logged
  - Approved data exported as a spreadsheet or JSON in your target layout
  - Accuracy measured against documents your experts already keyed
- **Entry gate:**
  - A sample of the chosen document type, native and scanned
  - The target layout: a template or an export from the target system
  - The same documents already keyed by your experts, as the answer key
  - Named reviewers with time in the proof's last weeks
  - An agreed secure transfer route and an OCI tenancy for the delivery team
- **In scope:**
  - One document type, in English, PDF or Word, native or scanned
  - The core fields and the most common rules: header, items, base rates, tiers
  - Confidence, coverage and the core business-rule checks
  - The review screen and the export file
  - Measured on the time from agreement to checked rates, review included
  - Proof accepted when the fields match the hand-keyed answers at the agreed rate and every value points to the right page
- **Out of scope:**
  - Loading data into the target system (file export only)
  - Documents picked up from a repository; bundles, duplicates and missing annexes
  - More than one document type, or languages other than English
  - Derived charges, formulas and amendments beyond the core rules
  - Terms the schema has no place for
  - Second approval, roles and review queues
  - Matching invoices against the extracted terms
  - Using the data with no human review
- **Source:** op-0910; deck-0910 slides 8–10; demo-deck; br3 §8; research-brief: What happens when things go wrong

### Integration · M

- **Id:** integration
- **Scope:** Live for one document type, inside the team's workflow: repository in, target system out.
- **Duration:** 13–22 weeks (status indicative)
- **Duration note:** Approximate, confirmed at scoping: the site's standard row (3–5 months), as in the package deck.
- **Services price:** to be defined
- **Infrastructure price per month:** to be defined
- **What you get:**
  - Documents picked up from the contract repository
  - The full schema with every rule: derived charges, formulas, discounts, amendments
  - Reference lists, required-field checks and exception rules tuned to your data
  - Roles, queues, search and filters in the review screen
  - Approved data loaded into your cost, lease or procurement system
  - Your production tenancy, with single sign-on, monitoring and recovery
- **In scope:**
  - Documents from the repository
  - The full schema and rule set for one document type, amendments included
  - Reference lists, required-field checks and exception rules
  - Roles, queues, search and filters; reviewer corrections folded back into the rules
  - Loading through the target system's import or interface
  - Production tenancy with single sign-on, high availability, disaster recovery and monitoring
- **Out of scope:** More than one document type; Languages other than English; Matching invoices against the extracted terms; Using the data with no human review
- **Source:** site Delivery tab (deck-0910 slide 10); backlog-post; mini-site round 22 Duration row

### Scaling · L

- **Id:** scaling
- **Scope:** Several document types, volumes and business units.
- **Duration:** 13–52 weeks (status indicative)
- **Duration note:** Approximate, confirmed at scoping: the site's standard row (3–12 months), as in the package deck.
- **Services price:** to be defined
- **Infrastructure price per month:** to be defined
- **What you get:**
  - Several document types, each set up without code
  - Values checked against related documents, such as an endorsement against its policy
  - Languages beyond English
  - Several target systems and business units
  - Telemetry per document type: review time and corrections
- **In scope:**
  - Several document types, sources and target systems
  - Cross-document checks; new document types set up without code
  - Languages beyond English
  - Thresholds and rules tailored per business unit
  - Telemetry per document type and business unit
- **Out of scope:** Matching invoices against the extracted terms; Using the data with no human review
- **Source:** site Delivery tab (deck-0910 slide 10); backlog-post; research-brief: The industries; mini-site round 22 Duration row

### How each capability area is handled per tier

#### Documents in

- **Feature areas:** `Take in the documents`
- **PoV:** Manual upload of one document type, native or scanned
- **Integration:** Picked up from the repository
- **Scaling:** Several document types and languages
- **Levels:**
  - **PoV:** partial
  - **Integration:** included
  - **Scaling:** advanced

#### Fields extracted

- **Feature areas:** `Extract the fields`
- **PoV:** Core fields and the most common rules for one type
- **Integration:** Full schema: derived charges, formulas, amendments
- **Scaling:** A schema per document type
- **Levels:**
  - **PoV:** partial
  - **Integration:** included
  - **Scaling:** advanced

#### Exceptions flagged

- **Feature areas:** `Flag what needs a person`
- **PoV:** Confidence, coverage and core rule checks
- **Integration:** Full rule set, reference lists, required fields
- **Scaling:** Checks against related documents
- **Levels:**
  - **PoV:** partial
  - **Integration:** included
  - **Scaling:** advanced

#### Review

- **Feature areas:** `Review against the source`
- **PoV:** Source beside the rows; approve, edit, reject; edits logged
- **Integration:** Roles, queues, search and filters
- **Scaling:** Several teams and workflows
- **Levels:**
  - **PoV:** included
  - **Integration:** included
  - **Scaling:** advanced
- **Glyphs:**
  - **PoV:** ●

#### Data handed over

- **Feature areas:** `Hand over the approved data`
- **PoV:** Spreadsheet or JSON in the target layout
- **Integration:** Loaded into the target system
- **Scaling:** Several target systems
- **Levels:**
  - **PoV:** partial
  - **Integration:** included
  - **Scaling:** advanced

#### Accuracy and operations

- **Feature areas:** `Measure and improve`
- **PoV:** Accuracy against hand-keyed answers; a sandboxed tenancy
- **Integration:** Corrections loop; production tenancy, single sign-on, recovery
- **Scaling:** Telemetry per document type
- **Levels:**
  - **PoV:** partial
  - **Integration:** included
  - **Scaling:** advanced

### Why it sells for the partner

- **Consumption on the customer's own documents:** GPU cluster and database use, growing with each document type
- **A path into Oracle applications:** terms load into the ERP or procurement system at Integration
- **A door to Integration:** loading, then more document types and business units
- **A contained start:** manual upload, a file out, nothing integrated

### What each buyer gets

- **Operator:** Contract specialists confirm extracted values beside their page instead of reading every agreement to find them, and stop being the queue new suppliers wait in.
- **Payer:** The head of cost control gets checked rates in the system before the first invoice, each traceable to its clause, so a wrong rate is caught before it is paid.

## Proof

- **Customer:** Riyadh Air
- **Context:** At {Customer}, operators read ground-handling agreements of 60 to 100 pages and key every rate, tier and condition into the cost system by hand: three to five days a contract, about a month to open a new station. A wrong or missed rate surfaces at month-end invoice matching, and the know-how sits with a few experienced operators.
- **Delivered:** {Customer}'s reviewers get an agreement's rates extracted in 5–15 minutes for agreements of up to 40 pages, every value cited to its page and clause, doubtful ones flagged. They check each row beside its source page and export a file that mirrors the cost system's structure.
- **Divergence from the pack:** The source case is one airline's ground-handling agreements on the industry's standard template, in English, one document type (cargo handling was secondary scope), run in a SoftServe-controlled OCI environment the customer approved. Its export is a checked reference in the target data layout that operators key from, because the cost system has no import; built in 8 weeks with 2 of acceptance, delivered on 9 June 2026. The pack generalizes to long agreements, leases and policies with a definable target layout in four industries; adds repository pickup, loading into the target system, reference lists, roles and search at Integration (the source case's post-PoC backlog); and several document types, languages and business units at Scaling.
- **Divergence line:** The source case is a proof of value on an airline's ground-handling agreements (June 2026); its checked rates were entered into the cost system by hand.
- **Source:** demo-deck; arch; br3; guide; backlog-post
- **Proof headline:** Rates of agreements up to 40 pages extracted for review in 5–15 minutes
- **Proof story:** Riyadh Air's operators keyed ground-handling rates into the cost system by hand, three to five days an agreement. In its June 2026 proof of value, an agreement of up to 40 pages was extracted for review in 5–15 minutes, every rate cited to its page.
- **Proof story, anonymized:** An international airline's operators keyed ground-handling rates into the cost system by hand, three to five days an agreement. In its June 2026 proof of value, an agreement of up to 40 pages was extracted for review in 5–15 minutes, every rate cited to its page.

## Next steps

1. **Time the whole job:** Extraction plus review, on a 60–100-page agreement.
2. **Write the case study:** Riyadh Air may be named; the website keeps it anonymous.
3. **Build the Integration backlog:** Search, roles, schema set-up and loading into the target system.
4. **Agree the Oracle position:** Beside OCI Document Understanding and Oracle AI for Fusion Applications.

## Open questions

### review-time

- **Question:** How long does the reviewer's check take per contract? The proof timed only the extraction.
- **Why:** The end-to-end time a buyer will ask about is extraction plus review, and the first metric is measured end to end.
- **Blocks:** `'Any end-to-end time claim, and the ''reviewer''s check included'' line the site carries.'`

### long-contracts

- **Question:** Has an agreement of 60 to 100 pages been timed? The dry run's contracts ran up to 40 pages.
- **Why:** Earlier drafts and the site state 5–15 minutes for 60–100 pages, which is the architecture's estimate.
- **Blocks:** `Printing 5–15 minutes against 60–100 pages.`

### accuracy-result

- **Question:** What field accuracy did the proof reach against the customer's hand-keyed files? Only the average confidence (90–95%) is on record.
- **Why:** Accuracy is the proof's acceptance criterion and a technical buyer's first question.
- **Blocks:** `Any accuracy claim in any document.`

### proof-cloud

- **Question:** Who funds the proof's cloud, which the package deck prices at €0 to the customer?
- **Why:** Sellers will be asked, and the Dedicated AI Cluster is billed by the hour.
- **Blocks:** `Explaining the €0 line beyond 'confirmed at scoping'.`

### oracle-destination

- **Question:** Which Oracle system receives the data in a typical deal: Fusion Cloud ERP, Fusion Cloud Procurement or Transportation Management?
- **Why:** Every Oracle destination in this brief is inferred; Vlad's open item since 2026-07-24.
- **Blocks:** `Naming one Oracle destination as fact in a partner document.`

### delivered-ui

- **Question:** Did the delivered review screen ship adding rows, and did a second document type (cargo handling) run end to end?
- **Why:** The architecture describes both; the user guide and the dry run do not show them.
- **Blocks:** `Marking either as available.`

### oracle-overlap

- **Question:** How do Oracle's teams see the pack beside OCI Document Understanding and Fusion's own contract and invoice agents?
- **Why:** The positioning in the brief is ours, from vendor research, not agreed with Oracle.
- **Blocks:** `Naming those Oracle products in a partner-facing comparison.`

### integration-price

- **Question:** Integration and Scaling prices: the package deck's €300–500K and about €10K a month at Integration are not printed (entry price only).
- **Why:** Oracle asked for field-quotable tier prices (2026-09-16).
- **Blocks:** `Nothing printed; recorded for the pricing work.`

## Settings

### Clearance

| Channel | Customer may be named |
|---|---|
| Internal | yes |
| Partner print | yes |
| Customer site | no |
| Demo | no |

- **Source:** user:2026-09-28
- **Anonymized descriptor:** an international airline
- **Descriptor warning:** A new airline, the Gulf, Saudi Arabia or a named airport next to 'airline' narrows it to one company: keep them out of every anonymized artifact.
- **Internal-only facts:**
  - the customer's systems and their vendors (the cost-management system, its operator, the contract repository, the flight-operations system)
  - station codes, contract names and vendors' names
  - the customer's and the delivery team's people
  - the model names, the cloud region and the GPU sizing
  - the post-PoC backlog and its priorities
- **Forbidden strings:** AltraDOC; altraDOC; SGS; Sirion; NetLine; DOX; Qwen; Maverick; LlamaStack; Corrino; RUH
- **Approvals:**
  - Oleksii Orlov: Riyadh Air publishable, 2026-09-28 (told to the site team, 2026-09-29)
  - Oleksii Orlov: every other pick delegated to the session, 2026-10-02 (only very important questions); the brief confirmed under that delegation, each pick logged in decisions.md for review

### Build

- **Artifacts:** feature-list; deck; one-pager; exec-summary; listing; demo
- **Source:** user:2026-10-02
- **Audience:** partner_print

### Contacts

- **Partner print:**
  - **Name:** Karsten Tramborg
  - **Title:** Oracle Partnership Director
  - **Email:** ktram@softserveinc.com
- **Source:** naming-and-clearance §3; Karsten's title per Alex 2026-09-23
- **Site:**
  - **Mailbox:** oracle@softserveinc.com
  - **Named:** Karsten Tramborg
- **Internal:**
  - **Name:** Oleksii Orlov
  - **Email:** RnDrequest@softserveinc.com
  - **Note:** Pack owner and the site's product lead: Vlad Butenko, AI Product Manager (Alex, 2026-09-23).

### Deck

- **Seller lead:** What Large docs processing and review gives an account executive that a custom project does not.
- **Layers subtitle:** How Large docs processing and review is layered, from the infrastructure it runs on to the screen the reviewer works in.
- **Images:**
  - **Today:**
    - **File:** visuals/today-tomorrow-b-writing-papers.jpg
    - **Source:** Openverse / stocksnap
    - **Creator:** Helloquence
    - **Licence:** CC0 1.0
    - **Source URL:** https://stocksnap.io/photo/writing-papers-Y01VDYAX63
  - **Tomorrow:**
    - **File:** visuals/tomorrow-C-woman-laptop.jpg
    - **Source:** Openverse / stocksnap
    - **Creator:** Burst
    - **Licence:** CC0 1.0
    - **Source URL:** https://stocksnap.io/photo/woman-laptop-C7ARZC9TPU
  - **Customer logo:**
    - **File:** visuals/customer-logo-riyadh-air-logo-ink.png
    - **Source:** supplied by the owner from the engagement materials
    - **Licence:** used under the customer's clearance recorded in the pack brief
    - **Note:** the customer's own logo from the delivery's 9 June demo deck (supplied engagement material), used under the brief's clearance: our own team and Oracle and SoftServe sellers

### One-pager

- **Sub:** full
- **Tier scope:**
  - **PoV:** One document type, manual upload, core fields cited and reviewed.
  - **Integration:** Live for one type: repository in, target system out.
  - **Scaling:** Several document types, volumes and business units.
- **Reframe:** Review instead of typing

### Executive summary

- **Running header:** Oracle AI & Data Solutions · Large docs processing and review App

### Provenance

- **Inputs:**
  - **Id:** arch
    - **Path:** Customers/RiyahdAir/NEW_Architecture Vision - Riyadh Air v3.docx
    - **Kind:** sow
    - **Read:** `'2026-10-02'`
    - **Note:** the delivered architecture and pipeline, June 2026
    - **Supplies:** `'what was built: pipeline, checks, review screen, stack, constraints, out of scope'`
  - **Id:** guide
    - **Path:** Customers/RiyahdAir/BA.zip › BA/PoC_User_Guide.docx
    - **Kind:** sow
    - **Read:** `'2026-10-02'`
    - **Note:** the delivered reviewer flow
    - **Supplies:** `'the review flow, what the screen does not do'`
  - **Id:** br3
    - **Path:** Customers/RiyahdAir/BA.zip › BA/RiyadhAir PoC Business Requirements v3.0.docx
    - **Kind:** sow
    - **Read:** `'2026-10-02'`
    - **Note:** Apr 23, 2026
    - **Supplies:** `'process, baseline effort, pain points, data model, mapping rules, edge cases, validation method'`
  - **Id:** demo-deck
    - **Path:** Customers/RiyahdAir/NEW_09.06 Riyadh Air - Oracle - SoftServe PoC Demo.pptx
    - **Kind:** deck
    - **Read:** `'2026-10-02'`
    - **Note:** the final demo, 2026-06-09
    - **Supplies:** `'delivery dates, dry-run processing times and confidence, deliverables and acceptance'`
  - **Id:** backlog-post
    - **Path:** Customers/RiyahdAir/Post Poc Product Feature Backlog.docx
    - **Kind:** feature-list
    - **Read:** `'2026-10-02'`
    - **Note:** Jun 19, 2026
    - **Supplies:** `what was not built`
  - **Id:** case
    - **Path:** Customers/RiyahdAir/RiyadhAir_AI-Q_case_slides.pptx
    - **Kind:** deck
    - **Read:** `'2026-10-02'`
    - **Supplies:** `the case summary and the post-PoC roadmap`
  - **Id:** op-0910
    - **Path:** Packs/Large Document Extraction and review package/Intelligent Document Extraction - Sales one-pager - Oracle.pdf
    - **Kind:** deck
    - **Read:** `'2026-10-02'`
    - **Note:** Vlad Butenko's draft, Sep-10
    - **Supplies:** `package prices and durations; earlier pitch`
  - **Id:** deck-0910
    - **Path:** Packs/Large Document Extraction and review package/Intelligent Document Extraction - Service packages deck.pptx
    - **Kind:** deck
    - **Read:** `'2026-10-02'`
    - **Note:** Vlad Butenko's draft, Sep-10, image slides with notes
    - **Supplies:** `the detailed packages table`
  - **Id:** op-0727
    - **Path:** Packs/Large Document Extraction and review package/[Oracle Packages] Large Document Extraction and Validation - Acceleration Pack One-pager.pdf
    - **Kind:** feature-list
    - **Read:** `'2026-10-02'`
    - **Note:** Vlad Butenko's draft, Jul-27
    - **Supplies:** `'the earlier capability matrix in three lenses, use-case boundaries'`
  - **Id:** site
    - **Path:** Oracle-Solutions-Site site/data/content.js, product large-document-extraction (round 22, 2026-10-01 copy)
    - **Kind:** feature-list
    - **Read:** `'2026-10-02'`
    - **Note:** the approved story copy; superseded by this brief where they differ
  - **Id:** demo
    - **Path:** Oracle-Solutions-Site site/demo/large-document-extraction/
    - **Kind:** video
    - **Read:** `'2026-10-02'`
    - **Note:** the interactive walkthrough, 2026-09-15/16
  - **Id:** sync-0724
    - **Path:** AO-Personal-OS context/areas/softserve/calls/oracle/2026-07-24_133119_one-on-one_vlad-productization-sync.md
    - **Kind:** call-note
    - **Read:** `'2026-10-02'`
    - **Supplies:** `the owner's rules for the capability table and its missing rows`
- **Source:** session, 2026-10-02
- **Research brief:** research-brief.md
- **Inventory:** `.scratch/inventory.md`
- **Research:** .scratch/research/T1-workflow.md; .scratch/research/T2-vendors.md; .scratch/research/T3-industries.md; .scratch/research/T4-failure-paths.md

## Other fields

```yaml
clearance.note: 'Riyadh Air is named for our own team and for Oracle and SoftServe sellers. The site keeps
  ''an international airline'': its standing rule and its deny-list still bar customer names, and changing
  that is the owner''s call on the site.'
```
