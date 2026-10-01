---
slug: plan-vs-actual-investigation
status: confirmed
spec_version: 1
generated_with: { roadmap_version: '2026-09-22', catalog_version: '2026-09-18' }
roadmap_item_id: plan-vs-actual-investigation
roadmap_block: Deep research & investigation
---

# Plan vs actual investigation

- **Site:** Plan vs actual investigation
- **Internal slide:** Plan vs actual investigation App
- **External:** Plan vs actual investigation
- **External subheading:** Accelerator App by SoftServe
- **Note:** The site writes every string in sentence case since its rebrand; the internal slide adds App. Spelling: 'vs', no full stop, as on the site.
- **Source:** naming-and-clearance §2; the site's existing product name
- **Source of the name:** user:2026-10-01
- **Eyebrow:** Oracle AI & Data Solutions
- **Roadmap note:** Exact match: the roadmap item and the site's product share the name and the slug.

## One-liner

- **Full:** Stop the next project repeating the last one's overruns: project controllers see each work package's cost and schedule against plan, with the cause and the record behind every gap.
- **Source:** user:2026-10-01
- **Short:** Stop the next project repeating the last one's overruns, every cause backed by its record.
- **Banned words checked:** yes

## Problem and solution

### Problem

When a big project finishes late or over budget, project controllers can't say which work packages caused it or why: schedules, cost reports, change logs and contracts don't link.

### Solution

Project controllers review each package's plan against actual with its likely causes and the document behind each; planners confirm or reject, and confirmed causes become the next bid's lessons.

- **Source:** user:2026-10-01
- **Sub-problems:**
  - **Rebuilt by hand:** explaining one package's overrun means joining schedule, cost and contract files line by line.
  - **The cause sits elsewhere:** the change order, design delay or contractor swap is in a contract or a log, not in the schedule.
  - **The next bid repeats it:** lessons stay in people's heads and never reach the next plan.
- **Reframe:** Confirm the cause, don't hunt for it
- **Today:** Project controllers rebuild an overrun by hand from the schedule, the cost reports and the contracts, for the few packages someone has time for.
- **Tomorrow:** Every package's plan against actual arrives with its candidate causes and the record behind each; experts confirm, and the lessons go into the next bid.

## Who buys it

Heads of project controls at contractors and capital-programme owners whose schedules, cost reports and contracts don't link.

- **Source:** user:2026-10-01
- **Buyer roles:** Head of project controls; Commercial director; PMO director; Head of planning
- **Buyer by industry:**
  - **Construction:** Commercial director or head of project controls at a contractor
  - **Utility capital programmes:** VP capital delivery or the capital PMO
  - **Engineer-to-order manufacturing:** VP operations or head of estimating
  - **Shipbuilding and defence programmes:** Programme controls director
  - **Professional services:** COO or VP delivery
- **Qualifying signals:**
  - Runs large projects split into work packages or control accounts
  - Keeps schedule baselines and monthly updates, in Oracle Primavera P6 or another scheduling tool
  - Cost reports, contracts and change logs sit in separate systems or spreadsheets
  - Decides per package whether its own crews or subcontractors deliver the work
  - A recent overrun nobody could explain package by package
- **Disqualifiers:**
  - Plan, actuals and changes already sit in one system that explains its own variances
  - No retained baselines or monthly history
  - Wants automated subcontractor selection or ranking
  - Wants a forecast for a live project rather than an explanation of what happened

## Industries

### Construction and engineering contractors

- **Site label:** Construction
- **Framing:**
  - **Problem:** A contractor picks its own crews or a subcontractor for every work package, but after an overrun nobody can say which packages, under which choice, caused it: schedule updates, monthly cost reports and the variations log link only by package name.
  - **Solution:** Each package's overrun is shown with its likely causes (a variation, a design delay, a contractor change), each cited to the record, and packages built by own crews are compared with subcontracted ones before the next bid is priced.
  - **Entities:** scheduled activities with baselines and monthly updates, bills of quantities, subcontracts, variations and claims, provisional sums
- **Status:** plausible
- **What matters here:** Records link by name only; provisional sums distort budgets; own crews or subcontract is decided per package.
- **How the entities differ:** Activity-level schedules with baselines and monthly updates, bills of quantities, subcontracts and a variations log.
- **Note:** The source case's industry; its proof of value is in preparation, so the standing is plausible, not proven.
- **Source:** research-brief: The industries; user:2026-10-01

### Utility capital programmes

- **Site label:** Utility capital programmes
- **Framing:**
  - **Problem:** A utility's capital programme runs thousands of similar jobs a year (poles, mains, substations), and unit costs drift above estimate without anyone knowing which work types or crews drove it.
  - **Solution:** Jobs are compared with their estimates by work type and region, own crews against contractor crews, and each overrun comes back with its cited cause, ready for the regulator's review.
  - **Entities:** work orders, standard design units, contractor unit-rate invoices, crew types
- **Status:** plausible
- **What matters here:** Many small jobs, so samples are large; regulators want each overrun explained; own versus contractor crews.
- **How the entities differ:** Work orders and standard units by work type instead of one project's packages; crews instead of subcontracts.
- **Source:** research-brief: The industries; user:2026-10-01
- **Tier note:** Runs on the proof's mapping with the work order as the unit; a native work-type hierarchy and comparison over many small jobs come in later packages.

### Engineer-to-order manufacturing

- **Site label:** Engineer-to-order manufacturing
- **Framing:**
  - **Problem:** An equipment maker quotes every custom order, and when orders finish over their quote, the estimate, the job cost and the engineering changes sit in different systems, so nobody can say why.
  - **Solution:** Each closed order is compared with its quote, operation by operation, and every overrun comes back with its cause (an engineering change, rework, a late part) and whether outside processing paid off.
  - **Entities:** quotes, planned bills of materials and routings, job cost, engineering change orders, non-conformance reports
- **Status:** plausible
- **What matters here:** Quote mapped to what was built; engineering changes carried as scope; make or buy per component.
- **How the entities differ:** Orders, routings and engineering changes instead of scheduled activities and variations; no critical-path schedule.
- **Scope note:** Engineer-to-order only: repetitive manufacturing already gets standard-cost variance from its ERP.
- **Source:** research-brief: The industries; user:2026-10-01
- **Tier note:** Runs on the proof's mapping with the order as the unit; a native order, assembly and operation hierarchy comes in a later package.

### Shipbuilding and defence programmes

- **Site label:** Shipbuilding and defence
- **Framing:**
  - **Problem:** A programme team writes monthly variance explanations for every control account over threshold, from memory and email, and the customer's auditors challenge the ones the records don't support.
  - **Solution:** Each variance explanation is checked against the schedule, cost and change records, the unsupported ones are flagged, and the confirmed causes feed the next make-or-buy plan.
  - **Entities:** control accounts, integrated master schedules, variance analysis reports, make-or-buy plans
- **Status:** plausible
- **What matters here:** Variance reports already exist and get audited; formal make-or-buy plans; export controls limit who sees data.
- **How the entities differ:** Control accounts and mandated variance reports instead of packages joined by name; the make-or-buy plan is a formal document.
- **Note:** Export controls (ITAR) can limit an offshore-staffed delivery team on defence programmes; commercial shipbuilding avoids it (inferred).
- **Source:** research-brief: The industries; user:2026-10-01

### Professional services

- **Site label:** Professional services
- **Framing:**
  - **Problem:** A services firm's engagement ends below its planned margin; the project ledger shows the gap, but why (scope creep, the staffing mix, client delays) sits in change requests and email.
  - **Solution:** Each closed engagement's overrun is traced to the change requests, staffing and correspondence behind it, so the next bid prices the scope and the staffing mix on evidence.
  - **Entities:** engagements, role-and-rate estimates, timesheets, change requests, client correspondence
- **Status:** plausible
- **What matters here:** The ledger already shows the variance; the cause sits in change requests and email; the lesson is the staffing mix.
- **How the entities differ:** Timesheets by role and rate and change requests instead of schedules and bills of quantities; the decision is the staffing mix.
- **Note:** Kept on the owner's call against the research (2026-10-01): the pack claims the explanation and the staffing-mix lesson, never the margin variance the project ledger already shows.
- **Source:** user:2026-10-01; research-brief: The industries

### Held out

- **Note:** Considered and held for a buyer to appear; the first two fold into an industry above.
- **Candidates:**
  - Public infrastructure owners (with utility capital programmes)
  - Plant turnarounds and outages (with utility capital programmes)
  - Outsourced clinical-study delivery (not researched for Oracle fit)

### Rejected

| Name | Reason |
|---|---|
| Repetitive manufacturing | the ERP already computes and explains standard-cost variance (industries research) |
| Telecom fibre roll-out | no Oracle installed base found on the network-build side (industries research) |
| Marketing campaigns | the evidence sits in platform data that already reports pacing (workflow research) |

## Capabilities

### Gather the records

- **Stage:** Gather
- **Customization in this area:**
  - Loaders for the customer's export formats and report layouts
  - OCR languages and handwriting

| Category | Feature | Status | From tier | Customization | Specificity | Note | Source |
|---|---|---|---|---|---|---|---|
| Loading | Schedule, cost, contract and change exports loaded as-is | partial | pov | Export formats per source system | customer |  | sow §2.4; brief §5 |
| Loading | Scanned contracts and amendments read by OCR | available | pov | Languages and handwriting | engine | Shipped by the platform's document understanding; quality on handwriting and Arabic is untested. | sow §2.4; research-brief: Sources (unverified OCR quality) |
| Loading | Every record's source file and version kept | partial | pov |  | use_case |  | sow §2.4, §7 |
| Loading | Live feeds from scheduling, cost and document systems | roadmap | integration |  | customer |  | research-brief: The workflow, generalized |
| Checks | Completeness and plan-quality checks per source | partial | pov |  | use_case |  | sow §2.2; research-brief: What the other vendors ship |

### Line up plan and actual

- **Stage:** Reconcile
- **Customization in this area:**
  - Mapping rules and package codes
  - Reconciliation conventions for baselines, change orders, currencies, calendars and provisional sums

| Category | Feature | Status | From tier | Customization | Specificity | Note | Source |
|---|---|---|---|---|---|---|---|
| Mapping | Records mapped to project, area and package | partial | pov | Mapping rules and package codes | customer |  | sow §2.4 |
| Mapping | Unresolved records listed with their reason | partial | pov |  | use_case |  | sow §2.4, §7 |
| Mapping | Unit hierarchy configurable per industry | roadmap | integration |  | industry | Work type and work order for utilities; order, assembly and operation for engineer-to-order. | research-brief: The industries |
| Reconciliation | Plan of record chosen per package | partial | pov |  | use_case | From standard practice; not in the source scope. | research-brief: The workflow, generalized |
| Reconciliation | Baselines, changes, currencies, calendars and provisional sums reconciled | partial | pov | The customer's conventions | customer; industry |  | sow §6 (2026-09-10 version); data-0929 |
| Reconciliation | Activities matched across re-baselined schedules | roadmap | integration |  | use_case |  | research-brief: What happens when things go wrong |

### Measure the variances

- **Stage:** Measure
- **Customization in this area:**
  - Materiality thresholds
  - The categories of the variance split

| Category | Feature | Status | From tier | Customization | Specificity | Note | Source |
|---|---|---|---|---|---|---|---|
| Comparison | Cost and schedule against plan, per package | partial | pov |  | use_case | To date for running work, in full for finished work. | sow §2.2; brief §3 |
| Comparison | Forecast drift tracked month by month | partial | pov |  | use_case |  | data-0929; pov-deck |
| Comparison | Variance split: scope, rate, quantity, timing | partial | pov | Categories of the split | use_case | From standard practice; not in the source scope. | research-brief: The workflow, generalized |
| Comparison | Re-planning separated from real slippage | roadmap | integration |  | use_case | From standard practice; not in the source scope. | research-brief: What the other vendors ship |
| Materiality | Material variances flagged, with critical-path impact | partial | pov | Thresholds | use_case |  | research-brief: What the other vendors ship |
| Materiality | First month each gap showed in the record | partial | pov |  | use_case | Read from the monthly record; a change entered late makes it lag. | pov-deck (early-warning lead time) |

### Trace the causes

- **Stage:** Explain
- **Customization in this area:**
  - The cause list, which document types count as evidence, and the languages they are written in
  - Delivery models named in the customer's own words

| Category | Feature | Status | From tier | Customization | Specificity | Note | Source |
|---|---|---|---|---|---|---|---|
| Evidence | Evidence search across contracts, changes and reports | partial | pov | Document types that count as evidence | engine | Built on the engine's cited search; the evidence index is set up in the proof of value. | sow §2.4; research-brief: Where the pack differs from what we built |
| Evidence | Candidate causes, each cited to its record | partial | pov | The cause list | customer |  | sow §2.4; brief §6 |
| Evidence | Confidence per cause; unexplained gaps marked | partial | pov |  | use_case |  | brief §6; research-brief: What happens when things go wrong |
| Attribution | Who carried the risk behind each cause | partial | pov |  | use_case | From standard practice; not in the source scope. | research-brief: What the other vendors ship |
| Attribution | Own crews compared with subcontractors, same trade | partial | pov | Delivery models per industry | industry |  | brief §3; user:2026-10-01 |

### Review with experts

- **Stage:** Confirm
- **Customization in this area:**
  - Reviewers, validation cases and who rules on a disagreement

| Category | Feature | Status | From tier | Customization | Specificity | Source |
|---|---|---|---|---|---|---|
| Review | Confirm or reject each cause, with a reason | partial | pov | Reviewers and validation cases | customer | sow §2.2, §7 |
| Review | Disagreements kept for the decision owner | partial | pov | Who rules on a disagreement | use_case | research-brief: What happens when things go wrong |
| Access | Record-level access for restricted or export-controlled data | roadmap | integration |  | industry | research-brief: The industries |

### Carry the lessons forward

- **Stage:** Learn
- **Customization in this area:**
  - The report's layout and the decisions it feeds

| Category | Feature | Status | From tier | Customization | Specificity | Note | Source |
|---|---|---|---|---|---|---|---|
| Lessons | Recurring patterns, with the sample size stated | partial | pov |  | use_case |  | brief §6; research-brief: What happens when things go wrong |
| Lessons | Insight report and evidence pack exported | partial | pov | Report layout and the decisions it feeds | use_case |  | brief §6; sow §7 |
| Lessons | Lessons written back to planning and estimating | roadmap | integration |  | customer |  | research-brief: What the other vendors ship |
| Comparison at scale | Several projects and portfolios compared | roadmap | scaling |  | use_case |  | brief §9 |
| Comparison at scale | Plans checked against completed history | roadmap | scaling |  | use_case |  | research-brief: What the other vendors ship |
| Comparison at scale | Many small jobs compared as one group | roadmap | scaling |  | industry | Utilities: thousands of similar jobs, with the sample size shown. | research-brief: The industries |

## Workflow

### Inputs

| System | Detail | Data | Tier |
|---|---|---|---|
| Oracle Primavera P6 | or another scheduling tool | schedule baselines and monthly updates | file export (XER or XML) in the proof of value; API feed in Integration |
| Oracle Fusion Cloud ERP | or Oracle E-Business Suite, another ERP, or spreadsheets | budget, forecast and actual cost per package, month by month | file export in the proof of value; API feed in Integration |
| Oracle Aconex | or another document store | contracts, bills of quantities, amendments, letters, progress reports | file export in the proof of value; API feed in Integration |
| Oracle Primavera Unifier | or a spreadsheet register | variations, claims, approvals | file export in the proof of value; API feed in Integration |

### 1. Gather and check the records

- **Actor:** system
- **Human in the loop:** yes
- **Covers:** scope of the review, export loading, origin kept for every record, completeness and plan-quality flags
- **Description:** The controls lead picks the projects, packages and period. Schedule, cost, contract and change exports are loaded as they are, with each record's file and version kept, and each source is profiled for completeness and plan quality before anything is compared. The lead accepts or rejects a source.
- **If it fails:** A source missing for a package is listed as a gap.
- **Vertical differences:**
  - **Utility capital programmes:** a cohort of similar jobs by work type and year, not one project (roadmap)
  - **Engineer-to-order manufacturing:** closed orders: quote, planned routing, job cost, change list
  - **Shipbuilding and defence programmes:** export-control screening before any data leaves the client
- **Source:** research-brief: The workflow, generalized; industries research grid (per-industry differences)

### 2. Line up plan and actual

- **Actor:** system
- **Human in the loop:** yes
- **Covers:** mapping every record to its project, area and package; choosing the plan of record; reconciling baselines, change orders, currencies, calendars and provisional sums
- **Description:** Records are resolved to the lowest level the data reliably supports, and whatever cannot be resolved is listed as a coverage gap with its reason. The controls lead confirms the mapping and which plan counts: the original, the current approved or a re-baselined one.
- **If it fails:** Unlinkable records: gaps, never guessed; re-baselined activities matched at Integration.
- **Vertical differences:**
  - **Construction and engineering contractors:** links by name only; provisional sums; progress measured on different bases
  - **Utility capital programmes:** standard units exist; jobs join by work-order number
  - **Engineer-to-order manufacturing:** quote lines mapped to the as-built bill of materials and routing (roadmap)
  - **Professional services:** plan and actual already share one project ledger
- **Source:** research-brief: The workflow, generalized; research-brief: What happens when things go wrong; industries research grid (per-industry differences)

### 3. Measure the variances

- **Actor:** system
- **Human in the loop:** yes
- **Covers:** plan against actual on cost and schedule to date, month-by-month drift, the split into scope change, rate, quantity and timing, materiality, the critical-path flag, the first month the gap was visible; at Integration, re-planning separated from slippage
- **Description:** Each package is compared with its plan on cost and schedule, to date for running work and in full for finished work, month by month. Variances are split into scope change, rate, quantity and timing, and flagged as material above a threshold the controls lead sets, with whether they moved the end date.
- **If it fails:** Change entered late: first-visible month lags; not covered, disclosed.
- **Vertical differences:**
  - **Construction and engineering contractors:** cost and schedule per package across monthly snapshots
  - **Utility capital programmes:** unit cost per standard unit against estimate; in-service date
  - **Engineer-to-order manufacturing:** estimated against actual hours and cost, engineering changes counted as scope; promised against shipped date
  - **Shipbuilding and defence programmes:** cost and schedule indices already reported monthly
  - **Professional services:** the project ledger already shows the variance; the pack explains the cause
- **Source:** research-brief: The workflow, generalized; industries research grid (per-industry differences)

### 4. Trace the causes

- **Actor:** ai
- **Human in the loop:** no
- **Covers:** evidence search across contracts, change records and reports; candidate causes with citation and confidence; who carried the risk; own crews compared with subcontractors
- **Description:** For each material variance, the contracts, amendments, change and claims records and progress reports are searched for what explains it. Candidate causes come back each cited to the record or passage, with a confidence level and who carried the risk, and packages delivered by own crews are compared with subcontracted ones of the same trade.
- **If it fails:** A cause recorded nowhere is marked unexplained, never invented.
- **Vertical differences:**
  - **Construction and engineering contractors:** claims log, scanned amendments, design delays, site access
  - **Utility capital programmes:** permits, cancelled outages, crews diverted to storms
  - **Engineer-to-order manufacturing:** engineering changes, rework, late supplier parts
  - **Shipbuilding and defence programmes:** existing variance explanations checked against the records
  - **Professional services:** change requests and client correspondence
- **Source:** research-brief: The workflow, generalized; research-brief: What the other vendors ship; industries research grid (per-industry differences)

### 5. Confirm the causes

- **Actor:** human
- **Human in the loop:** yes
- **Covers:** confirm or reject each cause with a reason; disagreements kept; review status
- **Description:** Planners and project controllers confirm or reject each candidate cause in the review app, with a reason. Where two reviewers disagree, both verdicts and reasons are kept and the decision owner rules. Only confirmed, evidenced causes become lessons.
- **If it fails:** Reviewers disagree: both verdicts are kept; the decision owner rules.
- **Vertical differences:**
  - **Utility capital programmes:** findings may enter a rate case, so review must be auditable
  - **Shipbuilding and defence programmes:** control-account managers own the explanations
- **Source:** research-brief: What happens when things go wrong; industries research grid (per-industry differences)

### 6. Carry the lessons forward

- **Actor:** system
- **Human in the loop:** yes
- **Covers:** patterns across packages by trade, delivery model and contractor, with the sample stated; the insight report and evidence pack; at Integration, lessons written back to planning
- **Description:** The system groups confirmed causes into what recurs across packages, by trade, delivery model and contractor, with the sample size stated. The commercial and planning leads take the insight report and its evidence pack into the next bid, packaging or make-or-buy decision; at Integration the lessons are written back to the planning tool.
- **If it fails:** Too few packages: reported as cases, not patterns, sample stated.
- **Vertical differences:**
  - **Construction and engineering contractors:** next bid: own crews, subcontract or mixed, per package
  - **Utility capital programmes:** next capital plan: which work types go to contractors
  - **Engineer-to-order manufacturing:** next quote: make or outside processing
  - **Shipbuilding and defence programmes:** the next proposal's make-or-buy plan
  - **Professional services:** the next bid's staffing mix
- **Source:** research-brief: The workflow, generalized; user:2026-10-01; industries research grid (per-industry differences)

### Outputs

| System | Detail | Data | Tier | Note |
|---|---|---|---|---|
| Review app |  | findings, citations, review status and the coverage-gap list | in the proof of value |  |
| Insight report and evidence pack | file export | confirmed causes and recurring patterns per package, each with its record | file in the proof of value |  |
| Oracle Primavera P6 | or another scheduling or estimating tool | lessons attached to the next plan or estimate | write-back in Integration; not in the proof of value | The receiving system is confirmed with the first Integration customer (inferred). |

### Notes

- **Source:** research-brief: The workflow, generalized; user:2026-10-01
- **Not ours:**
  - **Deciding the next packaging, make-or-buy or bid:** the buyer's decision; the pack supplies the evidence
  - **Ranking or selecting subcontractors:** the buyer's choice; the pack compares, never ranks
  - **Forecasting a live project's outcome:** scheduling and controls tools already ship it
  - **Pursuing claims or entitlement:** a different job with a different standard of proof
  - **Rebuilding missing monthly updates:** gaps are reported, never reconstructed
  - **Splitting one variance among concurrent causes:** causes are listed, not apportioned
  - **Judging whether a lesson transfers to another project:** the buyer's call
- **Integration by tier:**
  - **PoV:** File exports in; the review app, a report and an evidence pack out.
  - **Integration:** API feeds from the schedule, cost, document and change systems; activities matched across re-baselines; re-planning separated from slippage; lessons written back to planning.
  - **Scaling:** Several projects and portfolios; comparison against completed history.
- **Grouping note:** Ten practitioner steps grouped into six at the buyer's checkpoints: scoping and source validation inside step 1; the plan of record and the reconciliation inside step 2; the variance split, materiality, critical path and first visibility inside step 3; finding what recurs inside step 6.
- **Domain steps note:** Practitioner names: performance assessment and forensic schedule analysis (AACE TCM 10.1 and 6.4; RP 29R-03), variance analysis at the control account (ANSI/EIA-748).

## Architecture

### Inputs

| System | Detail | Data | Tier |
|---|---|---|---|
| Oracle Primavera P6 | or another scheduling tool | schedule baselines and monthly updates | file export (XER or XML) in the proof of value; API feed in Integration |
| Oracle Fusion Cloud ERP | or Oracle E-Business Suite, another ERP, or spreadsheets | budget, forecast and actual cost per package, month by month | file export in the proof of value; API feed in Integration |
| Oracle Aconex | or another document store | contracts, bills of quantities, amendments, letters, progress reports | file export in the proof of value; API feed in Integration |
| Oracle Primavera Unifier | or a spreadsheet register | variations, claims, approvals | file export in the proof of value; API feed in Integration |

### Stack, top to bottom

#### Application

- **Name:** Plan vs actual investigation by SoftServe
- **Vendor:** SoftServe
- **Summary:** traces each variance to its cause; experts confirm
- **Items:** Mapping and reconciliation; Variance measurement; Cause tracing with citations; Expert review and reporting

#### AI engine

- **Name:** NVIDIA AI-Q Blueprint
- **Vendor:** NVIDIA
- **Summary:** cited search and reasoning over the records
- **Items:**
  - NVIDIA AI-Q Blueprint: the research and reasoning workflow
  - NVIDIA NeMo: NeMo Retriever microservices for document processing, embedding and reranking
  - NVIDIA NIM: model serving
  - NVIDIA Nemotron: the reasoning models
- **Catalog id:** nvidia-aiq; nvidia-nemo; nvidia-nim; nvidia-nemotron
- **Note:** NeMo Retriever sits under the NVIDIA NeMo entry of the product list. Models are picked in the first two weeks of each engagement; open-source alternatives where licensed.

#### Infrastructure

- **Name:** Oracle Cloud Infrastructure
- **Vendor:** Oracle
- **Summary:** GPU compute, Kubernetes, storage, the database with vector search, identifier search, OCR, networking and identity
- **Items:**
  - OCI GPU Instances
  - OCI Kubernetes Engine (OKE)
  - OCI Object Storage
  - Oracle AI Database
  - Oracle AI Vector Search
  - OCI Search with OpenSearch
  - OCI Document Understanding
  - OCI API Gateway
  - OCI Virtual Cloud Network (VCN)
  - OCI Identity and Access Management
- **Catalog id:**
  - oci-gpu-instances
  - oci-kubernetes-engine
  - oci-object-storage
  - oracle-ai-database
  - oracle-ai-vector-search
  - oci-search-opensearch
  - oci-document-understanding
  - oci-api-gateway
  - oci-vcn
  - oci-iam

### Outputs

| System | Detail | Data | Tier | Note |
|---|---|---|---|---|
| Review app |  | findings, citations, review status and the coverage-gap list | in the proof of value |  |
| Insight report and evidence pack | file export | confirmed causes and recurring patterns per package, each with its record | file in the proof of value |  |
| Oracle Primavera P6 | or another scheduling or estimating tool | lessons attached to the next plan or estimate | write-back in Integration; not in the proof of value | The receiving system is confirmed with the first Integration customer (inferred). |

### Notes

- **Source:** sow §2.4 (updated 2026-10-01); research-brief: What the other vendors ship
- **Note:** Hybrid retrieval: vector search for meaning, OpenSearch for package codes, activity numbers and contract references. The pipeline is file-based in the proof of value.
- **Platform overlap note:** Where records already sit in Oracle's construction systems, Oracle Construction and Engineering Intelligence shows the variance and predicts delay. This pack explains the cause from records across systems, Oracle's and others, and has experts confirm it: it reads those systems' exports and does not replace their analytics.

## Oracle products

| Id | Name | Role | Why | At PoV | At Integration | At Scaling | Note | Inferred | Source |
|---|---|---|---|---|---|---|---|---|---|
| oci | Oracle Cloud Infrastructure | required | Runs the pack: GPU instances for the reasoning and retrieval models, Kubernetes for the app, API Gateway for its interfaces, Object Storage for the exports and the evidence, Document Understanding for scanned contracts, OpenSearch for package codes and contract references, and the network and identity setup around them. | A test tenancy, set up within the proof of value | The customer's production tenancy | The same tenancy across business units and regions |  |  | sow §2.4 (updated 2026-10-01) |
| oracle-ai-database | Oracle AI Database | required | Holds the reconciled project model and its relationships, and runs AI Vector Search over the evidence, so every cause traces back to its record. | Inside the proof's tenancy | A production instance fed monthly | One model across business units |  |  | sow §2.4 (updated 2026-10-01) |
| oracle-primavera-p6-eppm | Oracle Primavera P6 Enterprise Project Portfolio Management | optional | The schedules: every package's baseline and monthly updates, the record each schedule variance is measured against. | XER or P6 XML file export | API feed of each monthly update; lessons written back if it is the chosen destination | API feed for every project in the portfolio, with feed-health monitoring |  |  | sow §2.4; data-0929; AO wiki sbg-poc (central P6 EPPM on Oracle cloud, Aug-17 workshop) |
| oracle-fusion-cloud-erp | Oracle Fusion Cloud ERP | optional | Project costs: budgets, forecasts and actuals per package from project financials, the record each cost variance is measured against. | Cost report export | API feed from project costing | API feed across business units, with feed-health monitoring | The source case's costs sit in Oracle applications and monthly cost reports; buyers on Fusion Cloud ERP connect it directly. | yes | brief §5; research-brief: The workflow, generalized |
| oracle-aconex | Oracle Aconex | optional | The contracts, amendments and formal correspondence where the cause of a variance is usually written down. | File export of the document register and project mail | API feed from the document register and project mail | API feed from every project's register and mail, with feed-health monitoring |  |  | sow §2.4 (raw Aconex exports; contracts, amendments and correspondence as the evidence layer) |
| oracle-primavera-unifier | Oracle Primavera Unifier | optional | Change and claims registers as evidence of why cost and schedule moved, and a candidate destination for lessons at Integration. | Register export | API read of change and claims records; lessons written back if it is the chosen destination | API read and write-back across the portfolio, with feed-health monitoring |  | yes | research-brief: What the other vendors ship |

## Metrics

- **Kpis note:** One set: three business metrics, figures to follow; the statement of work's two quality criteria print only as 'Proof accepted when'. The statement of work (updated 2026-10-01) is taken as the current set; the approach deck's early-warning lead time and decision relevance are left out unless the owner picks them.

### Time to explain an overrun

- **Kind:** business
- **Signed off by:** Head of project controls
- **Formula:** Expert hours per package, from its raw records to a reviewed explanation with its record
- **Baseline:** The planner hours the same analysis takes by hand today, timed on the proof's packages
- **Figure:** -
- **Direction:** down
- **One-pager label:** Expert time to explain an overrun
- **Note:** The source case's operational-efficiency measure: person-hours to prepare an equivalent package-level analysis.
- **Source:** sow §2.3

### Overrun explained

- **Kind:** business
- **Signed off by:** Commercial director
- **Formula:** Overrun value with a cause the experts confirmed, and its record ÷ total overrun value in the sample
- **Baseline:** The share of each package's overrun with a documented cause today, measured at the start of the proof
- **Figure:** -
- **Direction:** up
- **One-pager label:** Share of the overrun explained, by value
- **Note:** Derived from the source case's quality criteria: the money question they serve. A reported reason or a claim amount is not an approved impact until the experts confirm it.
- **Source:** sow §2.3 (derived); research-brief

### Delay explained

- **Kind:** business
- **Signed off by:** Head of planning
- **Formula:** Days late on finished packages with an expert-confirmed cause and its record ÷ total days late in the sample
- **Baseline:** Today's share at close-out, measured on the same sample at the start of the proof
- **Figure:** -
- **Direction:** up
- **One-pager label:** Share of the delay explained, in days
- **Note:** The schedule counterpart of Overrun explained; the job covers cost and schedule.
- **Source:** sow §2.3, §2.4 (derived)

### Causes the experts confirm

- **Kind:** technical
- **Formula:** Variances, patterns and candidate causes the experts confirm ÷ those reviewed, on the agreed validation cases
- **Figure:** -
- **Note:** The source case's output validation rate; the threshold is agreed in the first weeks.
- **Source:** sow §2.3

### Findings traced to their record

- **Kind:** technical
- **Formula:** Material findings carrying the package, source file and version, passage, basis, confidence, review status and the data gaps that limit them ÷ material findings
- **Figure:** -
- **Note:** The source case's evidence coverage.
- **Source:** sow §2.3, §7

## Packages

- **Status:** confirmed
- **Anchor line:** Runs on OCI beside the customer's Oracle Primavera P6 schedules and Oracle Aconex contract records.
- **Value for Oracle and NVIDIA:** {Customer}'s schedules already run on Oracle Primavera P6, and each project analysed brings its full schedule history, cost reports, contracts and variations onto OCI. NVIDIA AI-Q and NeMo Retriever read them on GPU, Oracle AI Database holds the reconciled package data, and {Customer}'s unified ERP programme can reuse it.
- **Value for the client:** {Customer}'s planners will see why packages overran before the next project is packaged, and how its own crews and subcontractors delivered each trade against plan. The lessons will reach the next project director instead of staying with the last one.
- **Source:** user:2026-10-01 (proof length and price); sow (updated 2026-10-01); research-brief

### PoV Jumpstart · S

- **Id:** pov
- **Scope:** One project's file exports: each linkable package's plan against actual, with candidate causes cited to the record for your experts to confirm or reject.
- **Duration:** 8–8 weeks (target 8, hard cap 10, status confirmed)
- **Duration note:** CONFIRMED (user:2026-10-01): an 8-week proof, narrower than the source case's 12 weeks plus 2 of acceptance: one project's file exports, the packages the first weeks confirm as linkable, file in and out. The exports, the validation cases and named reviewers are an entry gate, not proof weeks.
- **Services price:** €171K · confirmed · Services, including the Oracle cloud environment setup; cloud consumption is billed separately.
- **Infrastructure price per month:** to be defined · Client-paid cloud consumption, sized at scoping.
- **What you get:**
  - Every package in the sample compared with its plan on cost and schedule, month by month
  - Each material variance with its candidate causes, cited to the record
  - Own crews compared with subcontractors on the same trade
  - A review app where your experts confirm or reject each cause
  - An insight report and evidence pack, with the coverage gaps listed
- **Entry gate:**
  - Schedule, cost, contract and change exports for one project, with monthly history
  - Who delivered each package: own crews or a subcontractor
  - Ten scope and ten schedule variance cases your experts already know, for validation
  - Named planners and controllers with review time
  - An agreed secure transfer route
  - An OCI tenancy with access for the delivery team
- **In scope:**
  - One project's file exports
  - The packages the first weeks confirm as linkable
  - Plan against actual on cost and schedule, to date for running work
  - Cited candidate causes with confidence and who carried the risk
  - Expert review in the app; the report and evidence pack
  - Proof accepted when the project's packages are linked at the lowest reliable level, each with plan against actual on cost and schedule, and reviewers can trace every material finding to its record, calculation, confidence and review status
- **Out of scope:**
  - Live connections to scheduling, cost or document systems
  - Lessons written back into planning
  - Matching activities across re-baselined, renumbered schedules
  - Rebuilding missing schedule updates
  - Splitting one variance among concurrent causes
  - Dating a gap from documents rather than the monthly record
  - Judging whether a lesson transfers to another project
  - Subcontractor ranking or selection, and the packaging decision itself
  - Claims or entitlement analysis
  - Forecasting a live project's outcome
- **Source:** user:2026-10-01; sow §5.3 (entry gate); research-brief: What happens when things go wrong
- **Duration label:** 8 weeks

### Integration · M

- **Id:** integration
- **Scope:** Live feeds from the scheduling, cost and document systems, and lessons written back into planning, for one business unit.
- **Duration:** 13–22 weeks (status indicative)
- **Services price:** to be defined · Set after the proof; not published.
- **What you get:**
  - Live feeds in place of exports
  - Activities matched across re-baselined schedules
  - The unit hierarchy and delivery models configured
  - Record-level access for sensitive claims
  - Lessons written back to planning and estimating
- **Out of scope:**
  - Several business units or regions
  - Comparison against completed history
  - Rebuilding missing schedule updates
  - Splitting one variance among concurrent causes
  - Dating a gap from documents rather than the monthly record
  - Judging whether a lesson transfers to another project
  - Subcontractor ranking or selection
- **Source:** mini-site round 22 Duration row (the owner's site); research-brief
- **Duration note:** Approximate, confirmed at scoping: the site's standard row (3–5 months).
- **Infrastructure price per month:** to be defined · Set after the proof; not published.
- **In scope:**
  - Live feeds in place of exports
  - Activities matched across re-baselined schedules
  - The unit hierarchy and delivery models configured
  - Record-level access for restricted or export-controlled data
  - Lessons written back to planning and estimating

### Scaling · L

- **Id:** scaling
- **Scope:** Every project in the portfolio, per-region thresholds and comparison against completed history.
- **Duration:** 13–52 weeks (status indicative)
- **Services price:** to be defined · Set after the proof; not published.
- **What you get:**
  - Several projects and portfolios compared
  - Plans checked against completed history
  - Many small jobs compared as one group
  - Thresholds and cause lists tailored per region and business unit
  - Telemetry per region on confirmed causes, evidence coverage and review time
- **Source:** mini-site round 22 Duration row (the owner's site); research-brief
- **Duration note:** Approximate, confirmed at scoping: the site's standard row (3–12 months).
- **Infrastructure price per month:** to be defined · Set after the proof; not published.
- **In scope:**
  - Several projects and portfolios compared
  - Plans checked against completed history
  - Many small jobs compared as one group
  - Thresholds and cause lists tailored per region and business unit
  - Telemetry per region: share of causes your experts confirm, share of material variances backed by a record, time to prepare a package review
- **Out of scope:**
  - Rebuilding missing schedule updates
  - Splitting one variance among concurrent causes
  - Judging whether a lesson transfers to another project
  - Subcontractor ranking or selection

### How each capability area is handled per tier

| Area | Feature areas | PoV | Integration | Scaling | Level at PoV | Level at Integration | Level at Scaling |
|---|---|---|---|---|---|---|---|
| Records in | `Gather the records` | File exports from one project: schedules, cost, contracts, changes | Live feeds from the scheduling, cost and document systems | Every project in the portfolio, refreshed monthly | partial | included | advanced |
| Plan and actual lined up | `Line up plan and actual` | Mapping and conventions for one project's packages | Activities matched across re-baselines; unit hierarchy configured | One mapping across business units and regions | partial | included | advanced |
| Variances measured | `Measure the variances` | Cost and schedule against plan, drift, split and materiality | The same, refreshed with every monthly update | Thresholds per region and business unit | included | included | advanced |
| Causes traced | `Trace the causes` | Cited candidate causes; own crews against subcontractors | The same, refreshed monthly, with the customer's own cause list | Causes compared across projects and contractors | included | included | advanced |
| Expert review | `Review with experts` | Confirm or reject in the review app | Record-level access; review inside the monthly controls routine | Review across business units, with the decision trail | partial | included | advanced |
| Lessons forward | `Carry the lessons forward` | Insight report and evidence pack | Lessons written back to planning and estimating | Comparison against completed history; groups of small jobs | partial | included | advanced |

### Why it sells for the partner

- **Consumption on the customer's own data:** GPU compute, Oracle AI Database and OCI Search with OpenSearch, for every project analysed
- **An Oracle anchor already in the account:** schedules in Oracle Primavera P6, contracts in Oracle Aconex
- **A door to Integration:** live schedule, cost and document feeds, and lessons written back into planning and estimating
- **A contained start:** file exports only, nothing integrated during the proof

### What each buyer gets

- **Operator:** Project controls stop rebuilding overruns by hand: each package's gap arrives with its causes and records, ready to confirm.
- **Payer:** The commercial director takes confirmed lessons into the next bid and sees, trade by trade, how own crews and subcontractors delivered against plan.

## Proof

- **Customer:** Saudi Binladin Group
- **Context:** {Customer} builds mega-projects split into dozens of work packages and decides for each whether its own crews or a subcontractor does the work. Execution rarely comes close to the original assumptions, and the reasons sit in schedules, monthly cost reports, contracts and a variations log nobody has joined, so each new project director meets the same traps.
- **Delivered:** {Customer}'s planners will see each package's cost and schedule against plan, month by month, with every overrun's candidate causes cited to the schedule update, cost report or variation behind it, and own crews compared with subcontractors on the same trade. Their own experts will confirm each cause before it becomes a lesson for the next project.
- **Divergence from the pack:** The source case is one unfinished construction project, two sites and the work packages its data assessment shortlisted, with three fixed delivery models and file exports from Primavera P6, monthly cost reports, contracts and a claims log, over 12 weeks plus 2 of acceptance with the cloud setup included. The pack generalizes to any project-based unit of work in five industries, an 8-week proof, configurable units and delivery models, and adds live feeds and write-back (Integration) and portfolio comparison (Scaling). The proof has not run: no results yet.
- **Divergence line:** The source case is one construction project's work packages, in preparation; the pack applies the same method to any project-based work, results to follow.
- **Source:** data-0929; brief; sow; user:2026-10-01
- **Proof headline:** Work packages on a live mega-project, investigated against their schedules, cost reports and variations: results to follow

## Next steps

1. **Run the source case:** Kick off once the customer agrees the package sample, the validation cases and the reviewers.
2. **Confirm what already exists:** Check what the sibling packs already ship before any capability is marked available.
3. **Agree the Integration destination:** Settle with the first Integration customer where lessons are written back.
4. **Brief Oracle's construction team:** Agree how the pack sits beside Oracle's own construction analytics.

## Open questions

### validation-cases

- **Question:** The source case's validation cases, expected results and reviewers are not agreed yet.
- **Why:** Every result the proof slide could print depends on them.
- **Blocks:** `'Any figure on the proof slide, the deck''s stat tiles and the one-pager''s proof strip (they print ''results to follow'').'`

### integration-destination

- **Question:** Which system receives the lessons at Integration: the planning tool, the estimating system or the analytics layer?
- **Why:** The architecture names a planning and estimating tool as an inference.
- **Blocks:** `Any document that names one write-back target as fact.`

### oracle-overlap

- **Question:** How does Oracle's construction team see the pack beside Oracle Construction and Engineering Intelligence?
- **Why:** The positioning (the pack explains causes from records across systems; Oracle's analytics keeps the numbers) is ours, not yet agreed with Oracle.
- **Blocks:** `Naming Oracle Construction and Engineering Intelligence in any partner-facing document.`

### sibling-reuse

- **Question:** Which parts already exist in sibling packs: cited extraction (Large docs processing and review), cited research (Account insights), the review screen?
- **Why:** Today only two capabilities are marked available, both shipped by the vendor platform.
- **Blocks:** `Marking any other capability available rather than built in the proof.`

### cloud-consumption

- **Question:** What cloud consumption does the proof of value carry? The source case's estimate (one H200 node, about USD 114K for three months) contradicts its own monthly line (USD 46.9K a month).
- **Why:** Sellers will be asked; Oracle's consumption is part of the case for the partner.
- **Blocks:** `Printing an infrastructure price per month.`

### ocr-quality

- **Question:** Is OCR on handwritten and Arabic amendments good enough for evidence?
- **Why:** The vendor claims it; nobody has tested it on the customer's documents.
- **Blocks:** `Claiming handwriting or Arabic support in any document.`

### vendor-claims

- **Question:** Unverified competitor and Oracle claims: Unifier AI change summaries, Construction and Engineering Intelligence benchmarks, the EcoSys assistant.
- **Why:** Read from trade press and search summaries; the vendor pages refused automated fetches.
- **Blocks:** `Naming any of them in a document.`

## Settings

### Clearance

| Channel | Customer may be named |
|---|---|
| Internal | yes |
| Partner print | no |
| Customer site | no |
| Demo | no |

- **Source:** user:2026-10-01
- **Anonymized descriptor:** a major construction and engineering contractor
- **Descriptor warning:** The region (Saudi Arabia, the Gulf) or the project type (stadium, entertainment complex, marine works) next to 'construction contractor' narrows it to one company: keep both out of every external artifact.
- **Internal-only facts:**
  - the customer's name and the contract value
  - the project and site names and the reference failure case
  - package codes and the data-assessment counts
  - the customer's and the delivery team's people
  - the cloud bill of materials and GPU sizing
- **Forbidden strings:** Saudi Binladin; Binladin; SBG; Dammam; Khobar; King Fahd; KFSC
- **Approvals:** Oleksii Orlov (pack owner's lead): customer named for our own team only, 2026-10-01; Oleksii Orlov: the whole brief confirmed, 2026-10-01

### Build

- **Artifacts:** feature-list; deck; one-pager; exec-summary; listing; demo
- **Source:** user:2026-10-01
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
  - **Note:** Pack owner and the site's product lead: Dmytro Dudchenko, AI Product Manager (Alex, 2026-09-23).

### Provenance

- **Inputs:**
  - **Id:** brief
    - **Path:** Customers/\<account>/Materials from SoftServe/… Project Packaging Strategy Optimization.pdf
    - **Kind:** sow
    - **Read:** `'2026-10-01'`
    - **Note:** the current use-case brief
    - **Supplies:** `'scope, data, outputs, out of scope, timeline'`
  - **Id:** pov-deck
    - **Path:** Customers/\<account>/Materials from SoftServe/… PoV approach and options.pdf
    - **Kind:** deck
    - **Read:** `'2026-10-01'`
    - **Note:** the approach deck sent to the customer, Aug 2026
    - **Supplies:** `'process, success measures, options, data shape'`
  - **Id:** data-0929
    - **Path:** Customers/\<account>/Materials from SoftServe/Data Assessment/29.09.2026/
    - **Kind:** sow
    - **Read:** `'2026-10-01'`
    - **Note:** the latest data assessment (summary + checklist)
    - **Supplies:** `the source case's sample and data reality`
  - **Id:** data-0922
    - **Path:** Customers/\<account>/Materials from SoftServe/Data Assessment/22.09.2026/
    - **Kind:** sow
    - **Read:** `'2026-10-01'`
    - **Note:** the first data assessment
  - **Id:** checklist
    - **Path:** Customers/\<account>/Materials from SoftServe/… PoC_Data_Checklist_and_Prerequisites.xlsx
    - **Kind:** sow
    - **Read:** `'2026-10-01'`
    - **Supplies:** `'data categories, kick-off prerequisites'`
  - **Id:** sow
    - **Path:** Customers/\<account>/UC #5.1 … Historical Package Performance Insights.docx
    - **Kind:** sow
    - **Read:** `'2026-10-01'`
    - **Note:** updated by Alex 2026-10-01 14:09; the 2026-09-10 version read the same morning
    - **Supplies:** `'architecture, components, price, timeline, deliverables'`
  - **Id:** wbs
    - **Path:** Customers/\<account>/… PoC_WBS_… v0.9.2.xlsx
    - **Kind:** sow
    - **Read:** `'2026-10-01'`
    - **Supplies:** `'effort, risks, bill of materials'`
  - **Id:** site
    - **Path:** Oracle-Solutions-Site site/data/content.js, product plan-vs-actual-investigation (round 22)
    - **Kind:** feature-list
    - **Read:** `'2026-10-01'`
    - **Note:** the existing product page; superseded by this brief where they differ
- **Source:** session, 2026-10-01
- **Research brief:** research-brief.md
- **Inventory:** `.scratch/inventory.md`
- **Research:** .scratch/research/T1-workflow.md; .scratch/research/T2-vendors.md; .scratch/research/T3-industries.md; .scratch/research/T4-failure-paths.md
