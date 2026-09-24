---
slug: contract-intelligence
status: confirmed
spec_version: 1
---

# Contract Intelligence

- **Site:** Contract Intelligence
- **Internal slide:** Contract Intelligence App
- **External:** Contract Intelligence
- **External subheading:** Accelerator App by SoftServe

## One-liner

- **Full:** Extracts clauses, obligations and dates from a whole contract estate and puts the deviations in front of a reviewer.
- **Short:** A contract estate, extracted once and reviewed by exception.

## Problem and solution

### Problem

Legal operations read every contract by hand: obligations, renewal dates and liability caps live in PDFs nobody can query.

### Solution

A retrieval and extraction service reads the whole estate, pulls clauses and obligations into a queryable model and flags the deviations. Reviewers work a ranked queue instead of a folder, approving or correcting each extraction.

- **Problem points:**
  - Slow answers: a single obligation question takes days of reading
  - Missed renewals: auto-renewals pass unnoticed and lock in old terms
  - Uneven review: two reviewers reach two different risk readings
- **Reframe:** Review the exceptions, don't read the estate
- **Reframe question:** What if legal reviewed only the exceptions?
- **Today:** Reviewers open contracts one by one, copy key dates into a spreadsheet and re-read the same clauses every time a question comes up.
- **Tomorrow:** The estate is extracted once and kept current; reviewers see a ranked queue of deviations and confirm or correct each one.

## Who buys it

Thousands of live contracts and a central legal operations team.

- **Buyer roles:** General Counsel; Head of Legal Operations; CFO

## Industries

### Manufacturing & industrial supply

- **What matters here:** Track supplier obligations, price-adjustment clauses and termination rights across a long tail of framework agreements.

### Financial services

- **What matters here:** Keep master agreements, annexes and regulatory covenants current, with an audit trail for every extracted term.

### Energy & utilities

- **What matters here:** Follow long-dated offtake and maintenance contracts, their indexation terms and their renewal windows.

## Capabilities

### Extraction

- **Customization in this area:** Custom clause taxonomy and extraction rules.

| Category | Feature | Status | From tier |
|---|---|---|---|
| Clause extraction | Clause and obligation extraction with citations | available | pov |

## Workflow

### Inputs

| System | Data |
|---|---|
| Contract repository | contract PDFs and metadata |

### 1. Ingest the estate

- **Actor:** ai
- **Human in the loop:** no

### 2. Extract and cite

- **Actor:** ai
- **Human in the loop:** no

### 3. Review the exceptions

- **Actor:** human
- **Human in the loop:** yes

### Outputs

| System | Data |
|---|---|
| Contract repository | confirmed terms written back |

## Architecture

### Inputs

| System | Data |
|---|---|
| Contract repository | contract PDFs, parties, effective dates |
| ERP | supplier master and spend |

### Stack, top to bottom

| Layer | Vendor | Items | Summary | Catalog id |
|---|---|---|---|---|
| Review workspace | Oracle + SoftServe | reviewer queue; citation viewer; audit trail | The reviewer queue, the citation viewer and the audit trail |  |
| Extraction engine | NVIDIA | nvidia-nemo | Retrieval, extraction and ranking over the whole estate | nvidia-nemo-agent-toolkit; nvidia-nim |
| Infrastructure | Oracle | GPU cluster; object storage; IAM | OCI compute with GPUs, object storage and IAM |  |

### Outputs

| System | Data |
|---|---|
| Contract repository | confirmed clauses and obligations |
| Obligation dashboard | renewal and deviation reporting |

## Oracle products

| Id | Name | Role | Why |
|---|---|---|---|
| oracle-fusion-erp | Oracle Fusion ERP | required | Supplier master and spend context for every contract |
| oci-object-storage | OCI Object Storage | required | Landing zone for the contract estate |

## Metrics

### Time to answer an obligation question

- **Kind:** business
- **Signed off by:** General Counsel
- **Chip:** Answer time ↓
- **Label:** to answer an obligation question across the estate
- **Baseline:** ~3 days
- **Figure:** ~10 min
- **Show baseline:** yes
- **Figure status:** pov_result
- **Attribution:**
  - **Otherwise:** a proof of value at a European industrial group
- **Caveat:** Illustrative proof-of-value result; not contractual.

### Renewal coverage

- **Kind:** business
- **Signed off by:** General Counsel
- **Chip:** Renewal coverage ↑
- **Label:** of live contracts with a tracked renewal date
- **Figure:** 98%
- **Figure status:** pov_result

### Review effort

- **Kind:** business
- **Signed off by:** Head of Legal Operations
- **Chip:** Review effort ↓
- **Label:** of pages a reviewer opens, versus reading the estate
- **Figure:** −70%
- **Figure status:** modeled

## Packages

- **Target OCI consumption:** Recurring GPU consumption per extraction run, growing with the size of the estate and the re-read frequency.
- **Anchor line:** Anchored to the customer's contract repository — every extraction run is OCI GPU consumption an account exec can sell.

### PoV Jumpstart · S

- **Id:** pov
- **Scope:** Prove extraction quality on the customer's own contracts; one contract family, manual upload.
- **Duration:** 4–8 weeks (target 6)
- **Services price:** €80K · confirmed
- **Infrastructure price per month:** €1.5K · indicative
- **What you get:** Extraction measured against the customer's own reviewers

### Integration · M

- **Id:** integration
- **Scope:** Full setup against the live repository; the reviewer queue embedded in the legal workflow.
- **Duration:** 12–20 weeks
- **Services price:** €280K–€450K · indicative
- **Infrastructure price per month:** €18K · indicative

### Scaling · L

- **Id:** scaling
- **Scope:** Scaling across jurisdictions and contract families, each with its own taxonomy.
- **Duration:** 16–52 weeks
- **Services price:** to be defined
- **Infrastructure price per month:** to be defined

### How each capability area is handled per tier

#### Clause & obligation extraction

- **PoV:** Core clause set on one contract family, with citations
- **Integration:** Full clause taxonomy across families, with confidence scoring
- **Scaling:** Per-jurisdiction taxonomies and extraction rules

#### Reviewer queue & corrections

- **PoV:** `''`
- **Integration:** Ranked queue with approve, correct and comment
- **Scaling:** Multiple region-specific review workflows

#### Obligation tracking

- **PoV:** Renewal and termination dates only
- **Integration:** Full obligation calendar with owners and reminders
- **Scaling:** Per-entity obligation reporting
- **Glyphs:**
  - **PoV:** ◐

#### Repository integration

- **PoV:** `''`
- **Integration:** In: contracts and metadata · Out: confirmed terms
- **Scaling:** Multiple repositories and jurisdictions

#### ERP & spend integration

- **PoV:** `''`
- **Integration:** Supplier master and spend joined to every agreement
- **Scaling:** Multiple ERP instances

#### Analytics & reporting

- **PoV:** Extraction quality report
- **Integration:** Deviation and renewal dashboards
- **Scaling:** Per-region dashboards and exports

#### Deployment

- **PoV:** Sandboxed
- **Integration:** Enterprise-integrated — dedicated landing zone, IAM
- **Scaling:** Enterprise-integrated, multi-region

### Why it sells for the partner

- Attaches to an ERP account the partner already owns — the contract estate is next to the supplier master
- Net-new GPU consumption per extraction run — the estate is re-read whenever it changes
- Repeatable across regulated industries — one taxonomy model, re-configured per customer
- Short first sale — a proof of value fits inside a quarter

## Proof

- **Customer:** (internal only)
- **Delivered:** Proof of value on a live contract estate: clause extraction and obligation tracking reviewed by the customer's own legal operations team.
- **Divergence from the pack:** The pack generalizes the clause taxonomy; the delivered proof of value covered two contract families in one jurisdiction.
- **Proof headline:** An estate extracted once, reviewed by exception, answered in minutes
- **Vertical case:** Vertical case: manufacturing & industrial supply

## Settings

### Clearance

| Channel | Customer may be named |
|---|---|
| Internal | no |
| Partner print | no |

- **Anonymized descriptor:** a European industrial group

### Contacts

- **Partner print:**
  - **Name:** Karsten Tramborg
  - **Title:** Alliances & Partnerships Director
  - **Email:** ktram@softserveinc.com
- **Internal:**
  - **Name:** R&D packaging team
  - **Email:** RnDrequest@softserveinc.com

### Deck

- **Running header:** Oracle AI & Data Solutions — {name}
- **Seller lead:** What this gives an account exec that a custom project does not.
- **Cta:** Ready to test the fit on one contract family?
