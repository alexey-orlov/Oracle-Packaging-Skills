---
slug: workforce-optimization
status: draft
spec_version: 1
generated_with: { roadmap_version: 2026-09-18, catalog_version: 2026-09-18 }
roadmap_item_id: workforce-optimization
roadmap_block: Data analysis & optimization
---

# Workforce Optimization

- **Site:** Workforce Optimization
- **Internal slide:** Workforce Optimization App
- **External:** Workforce optimization
- **External subheading:** Accelerator App by SoftServe
- **Note:** Rule from decisions-2026-09-18. The live mini-site currently ships the sentence-case "Workforce optimization" as `name`; it is relabelled at the next site rebuild.
- **Source:** decisions-2026-09-18
- **Source of the name:** one-pager-2026-07-17, decisions-2026-09-18

## One-liner

- **Full:** The same technicians complete more jobs a day, with less driving and waiting, on a four-week plan balanced across every zone.
- **Short:** A region's four-week field plan, optimized in minutes and approved by dispatchers.
- **Banned words checked:** yes
- **Note:** `full` is the mini-site's `oneLiner` as rewritten in site round 19 (2026-09-29): it sells the business value and names no platform, engine or data architecture. The line it replaced, "Optimizes field-service work zones and schedules with NVIDIA cuOpt: …", named the engine, which a one-liner never does (SPEC031). `short` is the site's retired `shortLine`, and the deck cover's line. The one-pager hero line both replace ("…packaged from proof of value to enterprise scale") was rejected by the owner: a one-liner never says how we package it (naming-and-clearance §4, asserted as ART206 on every channel). The delivered sales deck cover carries a third, deck-scoped line ("AI accelerator service packages on Oracle OCI + NVIDIA cuOpt…") that describes the deck rather than the product; it is retired at the deck's next rebuild.
- **Source:** site-2026-09-29, site-2026-09-17, decisions-2026-09-18

## Problem and solution

### Problem

Field-service operators plan their mobile workforce by hand: work zones, technician assignments, dozens of rules and constraints.

### Solution

NVIDIA cuOpt ingests demand, availability, skills and constraints, and computes the best technician-to-zone-to-job plan in minutes. Dispatchers review it on a live map, re-optimize and write the plan back to Oracle Fusion Field Service.

- **Problem points:**
  - **Suboptimal efficiency:** uneven workloads and under-used capacity
  - **Lower customer satisfaction:** longer wait times from suboptimal allocations
  - **Poor scalability:** planning hinges on scarce senior dispatchers; new zones launch slowly
- **Outcome chips:** Productivity ↑; Capacity utilization ↑; Customer wait time ↓
- **Reframe:** Review the plan, don't build it
- **Source:** one-pager-2026-07-17

## Who buys it

Any mobile field force planned against skills, availability and geography.

- **Buyer roles:** VP Field Service; Head of Service Operations; Head of Dispatch; COO
- **Qualifying signals:**
  - Zone-based planning: technicians are allocated to geographic work zones, not routed job by job
  - A heavy, centralized dispatch and scheduling routine run by a small number of senior dispatchers
  - Oracle Fusion Field Service, or an equivalent field-service management system, as the system of record
  - A recurring planning horizon of two or more weeks (roster mode), with bookings already on the calendar
  - More than one region or market, with rules that differ between them
- **Disqualifiers:**
  - Distance-based (zoneless) planning — a separate future product, not this pack
  - Within-day dynamic dispatch as the primary need — on the roadmap, not in the pack today
  - Jobs that routinely require two or more technicians on site (out of the delivered PoC's scope)
  - No historical planning data the customer can hand over for a proof of value
- **Note:** `line` is the only clean customer-side ICP sentence in the delivered estate (the one-pager's nearest equivalent is filed under partner value and gates on owning Oracle Fusion Field Service). Qualifying signals and disqualifiers are internal and reach no external artifact.
- **Source:** site-2026-09-17, call-2026-07-07, spec-doc-2026-09-16

## Industries

### Residential appliance & white-goods repair

- **Site label:** Manufacturing
- **Framing:**
  - **Problem:** In-home repair of manufactured goods is planned by hand: work zones and technician allocations, region by region, juggling skills, spare parts, travel and absences. Urgent call-outs and no-shows mean re-planning the day.
  - **Solution:** The solver plans the whole region against skills, parts, travel and existing bookings at once, and the dispatcher reviews and approves the result. Rules that differ by market — working time, holidays, service commitments — are configuration, so setting up a new region is a configuration job.
- **What matters here:** Dispatch home-repair technicians by skill, spare parts and travel, absorbing urgent call-outs and no-shows without re-planning the day.
- **Worked example:** The delivered proof of value: a residential appliance-repair field force across three countries, planned on postcode-based work zones, optimized and approved by its own dispatchers. Anonymized as "a global home-appliance manufacturer" outside internal use.
- **Status:** proven
- **Source:** deck-2026-07-13, site-2026-09-17

### Utilities — water · gas · electric

- **Site label:** Utilities
- **Framing:**
  - **Problem:** Water, gas and electric crews are scheduled across service territories against SLAs, crew certifications and outage spikes. Planned and emergency work compete for the same capacity, and the balance is struck manually by a handful of senior dispatchers.
  - **Solution:** Territories, certifications and SLA commitments become weighted constraints, and the plan is re-solved as the day's demand changes. Planned and emergency work are balanced against the objectives you weight, and no allocation reaches a crew until a dispatcher approves it.
- **What matters here:** Schedule field crews across service territories against SLAs, outage spikes and crew certifications, balancing planned and emergency work.
- **Worked example:** -
- **Status:** plausible
- **Source:** deck-2026-07-13, site-2026-09-17

### Telecom & cable

- **Site label:** Telecom & cable
- **Framing:**
  - **Problem:** Install-and-repair technicians have to be routed to tight appointment windows across regions, matched to line skills. Missed windows cost customer satisfaction directly, and launching a new service zone depends on scarce planning expertise.
  - **Solution:** Appointment windows and line skills are modeled as commitment and skill rules, and the solver routes against them while minimizing travel. Launching a new zone comes down to a configuration change.
- **What matters here:** Route install-and-repair technicians to tight appointment windows across regions, matching line skills and cutting customer wait time.
- **Worked example:** -
- **Status:** plausible
- **Source:** deck-2026-07-13, site-2026-09-17

### Industrial · medical-device · IT equipment service

- **Site label:** Healthcare
- **Framing:**
  - **Problem:** Medical-device and equipment service engineers are allocated to contracted assets by skill, SLA and location. Uptime on high-value machines is contractual, and the allocation is worked out by hand against a rising number of installed assets.
  - **Solution:** Contracted SLAs, engineer certifications and asset locations become the constraint set the solver works against, with uptime-critical commitments weighted as hard rules. The KPI readout compares the current and the optimized plan on identical definitions.
- **What matters here:** Allocate asset-based service engineers to contracted equipment by skill, SLA and location, keeping high-value machines uptime-critical.
- **Worked example:** -
- **Status:** plausible
- **Source:** deck-2026-07-13, site-2026-09-17

## Capabilities

### Allocation rules

- **Stage:** Set the rules
- **Customization in this area:** Custom rules implementation · Rules configuration · Matching rules with source data formats · Balancing optimization function with penalty / rewards, allocation rules weights tuning to achieve optimal allocation per customer · Introduction of additional optimization objectives

| Category | Feature | Status | From tier | Specificity | Footnote marker | Source | deck-2026-07-13 |
|---|---|---|---|---|---|---|---|
| Workforce availability rules | Skill-based allocation | available | pov | (none) |  | feature-list-2026-09-10 |  |
| Workforce availability rules | Maximal load per day | available | pov | (none) |  | feature-list-2026-09-10 |  |
| Workforce availability rules | Planned vacation reallocation | available | pov | (none) |  | feature-list-2026-09-10 |  |
| Workforce availability rules | Same-day sickness handling | available | pov | (none) |  | feature-list-2026-09-10 |  |
| Distance-based | Maximal distance / travel time rules | roadmap |  | use_case |  | feature-list-2026-09-10 |  |
| Distance-based | Real-time traffic / live travel data | roadmap |  | use_case |  | feature-list-2026-09-10 |  |
| Dynamic | Within-day job reassignment | roadmap |  | use_case |  | feature-list-2026-09-10 |  |
| Dynamic | Urgent / emergency request handling | roadmap | integration | use_case |  | feature-list-2026-09-10 | — |
| Workzone-based rules | Default work zones per technician | available | pov | use_case |  | feature-list-2026-09-10 |  |
| Workzone-based rules | Work zone-level demand | available | pov | use_case |  | feature-list-2026-09-10 |  |
| Workzone-based rules | Neighboring workzones | available | pov | use_case |  | feature-list-2026-09-10 |  |
| Workzone-based rules | Cross-zone allocation of selected technicians | available | pov | use_case |  | feature-list-2026-09-10 |  |
| Forecast-based rules | Forecast-based allocation (forecast data to be provided) | available | pov | customer |  | feature-list-2026-09-10 |  |
| Commitment-based rules | Non-movable appointments | partial | pov | (none) | *** | feature-list-2026-09-10 |  |
| Commitment-based rules | Different SLA types per appointment | partial | integration | customer |  | feature-list-2026-09-10 | — |
| Other rules | Spare-parts availability | roadmap | integration | industry |  | feature-list-2026-09-10 | — |
| Other rules | Crew-based assignments | roadmap | integration | industry |  | feature-list-2026-09-10 | — |
| Other rules | Other custom rules | roadmap | integration | customer |  | feature-list-2026-09-10 |  |
| Optimization function & rule weights | Multi-objective optimization (productivity, waiting time, workload balance) | available | pov | engine |  | feature-list-2026-09-10 |  |
| Optimization function & rule weights | Allocation rules weighting (hard / soft) | available | pov | engine |  | feature-list-2026-09-10 |  |
| Optimization function & rule weights | Minimal disruption of current allocation | available | pov | engine |  | feature-list-2026-09-10 |  |

| Category | Note |
|---|---|
| Workforce availability rules | Status cell `●` available, merged across all four features. |
| Distance-based | Status cell `○` roadmap. No tier carries these; zoneless planning is a separate future product. |
| Dynamic | Status cell `○` roadmap. Urgent / emergency handling is named in the Integration tier's advanced-allocation cell. |
| Workzone-based rules | Status cell `●` available, merged across all four features. The pack's defining use case. |
| Forecast-based rules | Status cell `●` available. The customer supplies the forecast; the pack does not produce it. |
| Commitment-based rules | Status cell is the pale `●` = partially implemented out of the box, major improvements on the roadmap. Rendered `◐` from now on. The delivered docx also hangs a `***` footnote marker on "Non-movable appointments" whose footnote text is missing from the file. |
| Other rules | Status cell `○` roadmap. Crews and inventory-coupling are named in the Integration tier's advanced-allocation cell. |
| Optimization function & rule weights | Status cell `●` available, merged across all three features. |

### Review and approval workflow

- **Stage:** Review, approve, measure
- **Customization in this area:** Model decisions explanations / recommendations tuning to match custom allocation rules

| Category | Feature | Status | From tier | Specificity | Source | one-pager-2026-07-17 |
|---|---|---|---|---|---|---|
| Review | Dispatcher UI (map, table views) | available | pov | (none) | feature-list-2026-09-10 |  |
| Review | Dispatcher approval/rejection | available | pov | (none) | feature-list-2026-09-10 |  |
| Review | Model decisions explanation and recommendations | available | pov | engine | feature-list-2026-09-10 |  |
| Feedback loop | Iterative feedback-based re-optimization | roadmap | integration | (none) | feature-list-2026-09-10 | — |
| Feedback loop | Human-feedback-driven model tuning | roadmap | integration | engine | feature-list-2026-09-10 |  |
| Feedback loop | Alternative allocation options (what-if) | roadmap | integration | engine | feature-list-2026-09-10 |  |

| Category | Note |
|---|---|
| Review | Status cell `●` available. The most reusable part of the delivered product (call-2026-07-07). |
| Feedback loop | Status cell `○` roadmap. Sold as Integration-tier scope: the one-pager's re-optimization row is `—` at PoV. |

### KPIs and analytics

- **Stage:** Solve the plan
- **Customization in this area:** Custom (additional) KPIs · Custom formula for KPI calculation

| Category | Feature | Status | From tier | Specificity | Source |
|---|---|---|---|---|---|
| KPI | Productivity (Jobs / Technician / Day) | available | pov | (none) | feature-list-2026-09-10 |
| KPI | Capacity Utilization | available | pov | (none) | feature-list-2026-09-10 |
| KPI | Travel Reduction | available | pov | (none) | feature-list-2026-09-10 |
| KPI | Workload Balance | available | pov | (none) | feature-list-2026-09-10 |
| Baseline comparison | Compare baseline vs optimized allocation | available | pov | (none) | feature-list-2026-09-10 |

| Category | Note |
|---|---|
| KPI | Status cell `●` available, merged across all four KPI features and down into Baseline comparison. |
| Baseline comparison | No status cell of its own; the merged `●` from the KPI category covers it. |

### Integrations

- **Stage:** Load the period's data
- **Customization in this area:** Integration configuration · Custom integrations

| Category | Feature | Status | From tier | Specificity | Oracle product | Source | one-pager-2026-07-17 |
|---|---|---|---|---|---|---|---|
| Integrations | Oracle Fusion Field Service as a datasource / destination | roadmap | integration | (none) | oracle-fusion-field-service | feature-list-2026-09-10 | — |
| Integrations | Demand forecasting datasource | roadmap | integration | customer |  | feature-list-2026-09-10 |  |
| Integrations | Visits booking system | roadmap | integration | customer |  | feature-list-2026-09-10 |  |
| Integrations | Inventory system for spare-parts availability | roadmap | integration | industry |  | feature-list-2026-09-10 |  |
| Integrations | HRM system for people availability | roadmap | integration | (none) |  | feature-list-2026-09-10 |  |
| Integrations | BI system for KPIs / analytics exports | roadmap | integration | customer |  | feature-list-2026-09-10 |  |

| Category | Note |
|---|---|
| Integrations | Status cell `○` roadmap — correct for the pack's own shipped code, and NOT a contradiction of the one-pager's architecture: the PoV Jumpstart is file export / import, and every system integration below is Integration-tier scope. State the tier with every claim. |

## Workflow

### Inputs

| System | Data | Tier |
|---|---|---|
| Oracle Fusion Field Service | work orders and bookings, technicians with skills and home postcode, work zones and their postcodes, technician calendars with day status and capacity | PoV Jumpstart: exported to XLSX by the customer. Integration: API. |
| Customer demand forecast | forecast volumes per zone and period, supplied by the customer | PoV Jumpstart: file. Integration: source system. |

### 1. Load the period's data

- **Actor:** human
- **Human in the loop:** yes
- **Description:** The dispatcher selects a region and a planning period of up to four weeks and loads the period's data: demand, technician availability, skills, work zones and existing bookings.
- **If it fails:** Validation names the missing sheet or field rather than failing silently; the row is flagged, not dropped, and the dispatcher fixes the input and re-runs. A warning does not block the run.
- **Vertical differences:**
  - **Residential appliance & white-goods repair:** -
  - **Utilities — water · gas · electric:** -
  - **Telecom & cable:** -
  - **Industrial · medical-device · IT equipment service:** -
- **Source:** spec-doc-2026-09-16, site-2026-09-17, demo-2026-09-16

### 2. Set the rules

- **Actor:** human
- **Human in the loop:** yes
- **Description:** Zone, forecast and commitment rules are configured, then weighted as hard or soft constraints against the objectives that matter — productivity, waiting time, workload balance — with minimal disruption of the current allocation as a standing objective.
- **If it fails:** A constraint set that makes the period infeasible is surfaced before the solve, and a hard rule is relaxed to soft only with the dispatcher's agreement (inferred — no delivered artifact states the infeasibility path).
- **Vertical differences:**
  - **Residential appliance & white-goods repair:** Working time, holidays and service commitments differ by market and are configuration, so a new region is a configuration job.
  - **Utilities — water · gas · electric:** Territories, crew certifications and SLA commitments become weighted constraints; planned and emergency work are balanced against the weights.
  - **Telecom & cable:** Appointment windows and line skills are modeled as commitment and skill rules; travel is minimized against them.
  - **Industrial · medical-device · IT equipment service:** Contracted SLAs, engineer certifications and asset locations form the constraint set, with uptime-critical commitments weighted as hard rules.
- **Source:** site-2026-09-17, feature-list-2026-09-10

### 3. Solve the plan

- **Actor:** ai
- **Human in the loop:** no
- **Description:** NVIDIA cuOpt computes the technician-to-zone-to-job plan against every constraint at once on the GPU solver, after a travel matrix is built and the rules and objectives are loaded. Minutes rather than days; up to about 20 minutes on a full region in the delivered product.
- **If it fails:** A solver timeout or an infeasible model returns the current plan unchanged with the blocking constraint named, rather than a partial plan (inferred).
- **Vertical differences:**
  - **Residential appliance & white-goods repair:** -
  - **Utilities — water · gas · electric:** -
  - **Telecom & cable:** -
  - **Industrial · medical-device · IT equipment service:** -
- **Source:** spec-doc-2026-09-16, demo-2026-09-16

### 4. Review, approve, measure

- **Actor:** human
- **Human in the loop:** yes
- **Description:** The dispatcher compares the current and the optimized plan on a live map, drills into a zone or a technician, and approves, rejects or comments per zone in the Zone View. KPIs are shown before and after on identical definitions. Re-running with feedback is an Integration-tier capability.
- **If it fails:** A rejected zone keeps its current allocation; nothing is exported until the dispatcher approves, so a bad plan never reaches the field.
- **Vertical differences:**
  - **Residential appliance & white-goods repair:** -
  - **Utilities — water · gas · electric:** No allocation reaches a crew until a dispatcher approves it.
  - **Telecom & cable:** -
  - **Industrial · medical-device · IT equipment service:** The KPI readout compares the current and the optimized plan on identical definitions.
- **Source:** spec-doc-2026-09-16, site-2026-09-17, demo-2026-09-16

### Outputs

| System | Data | Tier |
|---|---|---|
| Oracle Fusion Field Service | optimized allocations — zones and visits — with the dispatcher's decisions and comments | PoV Jumpstart: file export. Integration: API write-back. Scaling: API plus telemetry. |
| BI | KPIs per plan version | Integration |

### Notes

- **Source:** spec-doc-2026-09-16, site-2026-09-17, one-pager-2026-07-17

## Architecture

### Inputs

| System | Data |
|---|---|
| Oracle Fusion Field Service | technicians, availability, bookings, default allocations |
| Additional data sources | booking, parts inventory, HR/WFM, demand forecast (Integration tier) |

### Stack, top to bottom

#### Custom configuration

- **Vendor:** SoftServe
- **Items:** Client allocation rules and constraints; KPI definitions and formulas; Data integrations and mappings

#### Accelerator business app

- **Vendor:** Oracle + SoftServe
- **Name:** Accelerator business app
- **Summary:** optimization engine wrapper and dispatcher UI
- **Items:** Optimization engine wrapper and dispatcher UI; Approval workflow and re-solve loop; KPI and analytics layer

#### Optimization engine

- **Vendor:** NVIDIA
- **Name:** NVIDIA cuOpt
- **Summary:** GPU-accelerated solver
- **Items:** NVIDIA cuOpt — GPU-accelerated solver
- **Catalog id:** `nvidia-cuopt`

#### Infrastructure

- **Vendor:** Oracle
- **Catalog id:** oci-dedicated-ai-cluster; oci-kubernetes-engine; oci-object-storage; oracle-autonomous-ai-database; oci-vcn; oci-iam
- **Label:** Oracle · OCI dedicated AI cluster, Object Storage, IAM
- **Items:**
  - OCI dedicated AI cluster, 4–8 NVIDIA A100 GPUs
  - OCI Object Storage for the period's data
  - OCI networking and IAM
  - OKE / containers and Oracle Database 26ai for persistence (delivered PoC scope; not shown on the published architecture diagrams)

### Outputs

| System | Data |
|---|---|
| Oracle Fusion Field Service | optimized allocations: zones and visits |
| BI | KPIs per plan version |
| Plan export | the approved plan with the dispatcher's decisions and comments (18 columns in the delivered product) |

### Notes

- **Note:** The one-pager's `.arch` diagram is the canonical compact form (source system left, OCI box right, two labelled pipes); deck slide 7 is the canonical detailed form. The four-rung ladder above is the attribution device used on the executive summary and the section deck, and is a different component from the data flow.
- **Source:** one-pager-2026-07-17, deck-2026-07-13, site-2026-09-17, spec-doc-2026-09-16

## Oracle products

| Id | Role | Why | At PoV | At Integration | At Scaling | Note | Name note | Catalog note | Inferred | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| oci | required | The platform: a dedicated AI cluster of 4–8 NVIDIA A100 GPUs (A10 in the delivered PoC) runs the NVIDIA cuOpt solver, Kubernetes runs the app and the pre/post-processing services, Object Storage holds the period's data, Autonomous AI Database keeps plan versions, decisions and KPI history, VCN and IAM carry networking and identity — each in the Infrastructure layer's catalog_id list |  |  |  | Until 2026-09-22 these were seven required entries (oracle-fusion-field-service, oci-dedicated-ai-cluster — first coined as oci-compute-gpu —, oci-object-storage, oci-vcn — first coined as oci-networking —, oci-iam, oci-kubernetes-engine, oracle-autonomous-ai-database). OKE and the database come from the delivered PoC's technical scope and sit on no published diagram. |  |  |  | one-pager-2026-07-17, deck-2026-07-13, site-2026-09-17, spec-doc-2026-09-16 |
| oracle-fusion-field-service | optional | The typical source of work orders, technicians, zones and bookings, and destination of the approved plan — the delivered case's system; a buyer on another field-service system connects that one instead | File export / import — the customer exports XLSX and imports the optimized plan | API write-back: in — staff, availability, booking data; out — optimized allocations (zones, visits); back — factual durations and times | API plus telemetry, multi-region | Moved from required to optional on 2026-09-22: the pack reads from and writes to it; it does not run on it. | Canonical vendor name is "Oracle Fusion Field Service" (the Jul-17 one-pager). The deck, the feature list and the mini-site still say "Oracle Field Service"; relabel at next rebuild. |  |  | one-pager-2026-07-17, site-2026-09-17 |
| oracle-fusion-cloud-hcm | optional | Could be the HR/WFM source for people availability, one of the five typical Integration-tier integrations |  |  |  |  |  | The example first coined `oracle-fusion-hcm`; the catalog's id is `oracle-fusion-cloud-hcm` (Workforce Management is a module inside it — name the module when a pack depends on one). | yes | one-pager-2026-07-17, deck-2026-07-13 |
| oracle-fusion-cloud-scm | optional | Could be the inventory source for spare-parts availability and the demand-forecast source the forecast-based allocation rules consume |  |  |  |  |  | The example first coined two ids, `oracle-fusion-inventory-management` and `oracle-fusion-demand-management`. The catalog carries neither: both are modules of Fusion SCM, so the two entries collapse into one. Logged as a catalog change request — if the catalog ever splits the modules out, this entry splits with it. | yes | deck-2026-07-13 |
| oracle-analytics-cloud | optional | Could be the BI destination for KPIs per plan version |  |  |  |  |  |  | yes | feature-list-2026-09-10, deck-2026-07-13 |

## Metrics

### Planning cycle time

- **Kind:** business
- **Signed off by:** VP Field Service
- **Formula:** Elapsed time to optimize and approve a region's four-week plan, end to end including dispatcher review
- **Baseline:** ~2 days, planned by hand
- **Figure:** ~30 min
- **Label:** to optimize and approve a region's four-week plan, down from ~2 days
- **Figure status:** pov_result
- **Attribution:**
  - **Named when allowed:** Proof of value · \<the delivery customer>
  - **Otherwise:** proof of value at a global home-appliance manufacturer
- **Caveat:** KPIs measured before/after on proof-of-value data; figures are illustrative, not contractual.
- **Note:** Headline discipline (call-2026-07-09): the end-to-end figure, not the ~15-minute solve time.
- **Source:** one-pager-2026-07-17, call-2026-07-09

### Technician productivity

- **Kind:** business
- **Signed off by:** VP Field Service
- **Formula:** For each technician, total jobs ÷ days with at least one job; headline is the simple average across technicians, two decimals
- **Baseline:** the customer's current plan for the same window, computed on the identical formula
- **Figure:** up to +26%
- **Label:** productivity gain on proof-of-value data across three markets
- **Figure status:** pov_result
- **Attribution:**
  - **Named when allowed:** Proof of value · \<the delivery customer>
  - **Otherwise:** proof of value at a global home-appliance manufacturer
- **Caveat:** Productivity gain on proof-of-value data across the US, UK and Netherlands; illustrative, not contractual.
- **Note:** Pair any single-digit percentage with the sentence explaining why it is large at scale (call-2026-07-09).
- **Source:** one-pager-2026-07-17, spec-doc-2026-09-16

### Estimated savings at full launch

- **Kind:** business
- **Signed off by:** COO
- **Formula:** Cost of the additional staffing avoided at the optimized productivity, extrapolated to full launch
- **Baseline:** current staffing cost at the current plan
- **Figure:** €190K / month
- **Label:** estimated saving at full launch, valued as the staffing it avoids
- **Figure status:** modeled
- **Attribution:**
  - **Named when allowed:** Proof of value · \<the delivery customer>
  - **Otherwise:** proof of value at a global home-appliance manufacturer
- **Caveat:** Estimated savings at full launch, valued as the cost of additional staffing avoided; illustrative, not contractual.
- **Note:** The one-pager types this as an estimate at full launch, not a measured proof-of-value outcome, so `figure_status` is `modeled` rather than `pov_result`. Flagged for the owner.
- **Source:** one-pager-2026-07-17

### Capacity utilization

- **Kind:** business
- **Signed off by:** VP Field Service
- **Formula:** round(jobs ÷ (working days × 7) × 100), capped 0–100; the model assumes at most 7 jobs per technician per working day
- **Baseline:** the current plan for the same window
- **Figure:** -
- **Figure status:** -
- **Caveat:** Computed identically on the current and the optimized plan; measured per engagement.
- **Note:** Defined and measured, no cleared headline figure. The schema's figure_status enum has no value for this state.
- **Source:** spec-doc-2026-09-16, feature-list-2026-09-10

### Customer wait time

- **Kind:** business
- **Signed off by:** VP Customer Service
- **Formula:** Booking date to appointment date in whole calendar days, averaged across jobs
- **Baseline:** the current plan for the same window
- **Figure:** -
- **Figure status:** -
- **Caveat:** Computed identically on the current and the optimized plan; measured per engagement.
- **Source:** spec-doc-2026-09-16

### Travel reduction

- **Kind:** business
- **Signed off by:** VP Field Service
- **Formula:** Total planned travel across the period, current plan against optimized plan
- **Baseline:** the current plan for the same window
- **Figure:** -
- **Figure status:** -
- **Caveat:** Computed identically on the current and the optimized plan; measured per engagement.
- **Source:** feature-list-2026-09-10

### Workload balance

- **Kind:** business
- **Signed off by:** VP Field Service
- **Formula:** Spread of jobs per technician across the period, current plan against optimized plan
- **Baseline:** the current plan for the same window
- **Figure:** -
- **Figure status:** -
- **Caveat:** Computed identically on the current and the optimized plan; measured per engagement.
- **Source:** feature-list-2026-09-10

## Packages

- **Tier semantics:** Tiers map to integration depth, not feature count (call-2026-06-26). PoV Jumpstart proves the value on the customer's data with zero integration in a separate environment; Integration delivers a live, fully-integrated deployment at one location; Scaling extends it across markets with per-region rules and telemetry. PoV Jumpstart and Scaling are both optional — a bought-in customer goes straight to Integration, and a uniform global customer may never need Scaling.
- **Legend:** ◐ partial · ● included · ●● multi-region / advanced · — not included
- **Target OCI consumption:** -
- **Source:** one-pager-2026-07-17, decisions-2026-09-18

### PoV Jumpstart · S

- **Id:** pov
- **Scope:** Manual data import, limited rule set: prove the KPI gains on the customer's data.
- **Duration:** 6–8 weeks (target 8, hard cap 10)
- **Duration note:** The delivered print artifacts say "2 months" and the mini-site says "4–8 weeks"; normalized to 8 weeks per decisions-2026-09-18. The skill pushes back above 8 with reasons and rejects above 10. The standing rule (shared/references/pov-rules.md) allows a 4-week floor; this pack's own floor is 6 because the PoV needs a full four-week planning period of the customer's data plus a dispatcher review cycle on top.
- **Services price:** €90K · confirmed · One-time. €100K on an early deck slide was a slip; €90K is the confirmed figure.
- **Infrastructure price per month:** €2K · indicative · Indicative; depends on the usage and optimization rules complexity.
- **What you get:**
  - An optimized four-week plan for one real region, computed on the customer's own historical data
  - A before/after KPI readout — productivity, capacity utilization and wait time — computed identically on the current and the optimized plan
  - The dispatcher review UI running in a sandboxed environment on the customer's own tenancy
  - A costed plan for the next step: integration scope, additional sources, timeline
- **Entry gate:**
  - One real region and a period of historical planning data — demand, availability, skills, work zones and bookings
  - The allocation rules that actually apply: zones, skills, absences, service commitments
  - A dispatcher and a business owner who will review the plan and sign the baseline
- **In scope:**
  - Foundational allocation with the recurring, most-typical constraints — zones, skills, planned absences
  - Core KPIs predicted at scheduling and measured against the signed benchmark
  - The dispatcher review UI, with approve, reject and re-run
  - Sandboxed deployment on the customer's own tenancy
  - A before/after KPI readout computed identically on both plans
- **Out of scope:**
  - Oracle Fusion Field Service integration — Integration tier; the PoV is file export / import
  - Additional data sources and BI integration — Integration tier
  - The re-optimization feedback loop — Integration tier
  - Live-traffic travel rules, within-day reassignment, spare-parts and crew-based assignment — roadmap
- **Source:** one-pager-2026-07-17, site-2026-09-17, decisions-2026-09-18

### Integration · M

- **Id:** integration
- **Scope:** Full setup and integration, live at one location: no manual work, embedded in the workflow.
- **Duration:** 12–20 weeks
- **Services price:** €300K–€500K · indicative
- **Infrastructure price per month:** €25K · indicative · Indicative; depends on the usage and optimization rules complexity.
- **What you get:**
  - Oracle Fusion Field Service integration: staff, availability and booking data in; optimized allocations out; factual durations and times back
  - Up to five further integrations — booking, inventory for parts availability, HR/WFM for people availability, demand forecasting, BI
  - The re-optimization feedback loop with alternative allocation options
  - Advanced allocation with the full operational complexity — urgent jobs, crews, SLAs, inventory-coupling
  - Enterprise-integrated deployment: dedicated landing zone, IAM, observability
- **Name note:** Printed as "Roll-out · M" on the delivered artifacts; relabelled to "Integration" at next rebuild.
- **Source:** one-pager-2026-07-17, deck-2026-07-13, decisions-2026-09-18

### Scaling · L

- **Id:** scaling
- **Scope:** Scaling across locations: heterogeneous rules and data workflows per region.
- **Duration:** 12–52 weeks
- **Services price:** to be defined
- **Infrastructure price per month:** to be defined
- **What you get:**
  - Multiple region-specific optimization-rule configurations
  - Region-specific KPI sets and analytics
  - Multi-region integration and enterprise-integrated, multi-zone deployment
- **Name note:** Frame as telemetry and local tailoring. Never label this tier "hardening" — it invites "what was wrong before?" (call-2026-06-26).
- **Source:** one-pager-2026-07-17, deck-2026-07-13, call-2026-06-26

### How each capability area is handled per tier

| Area | Feature areas | PoV | Integration | Scaling |
|---|---|---|---|---|
| Optimization rules & guardrails | Allocation rules | ◐ Foundational allocation with recurring, most-typical constraints — zones, skills, planned absences | ● Advanced allocation with all operational complexities — urgent jobs, crews, SLAs, inventory-coupling | ●● Multiple region-specific optimization-rule configurations |
| Re-optimization & feedback loop | Review and approval workflow | — Not included | ● Feedback-driven re-optimization with alternative allocation options | ●● Region-specific workflows |
| Analytics & efficiency KPIs | KPIs and analytics | ● Core KPIs predicted at scheduling | ● Plus execution-data feedback and custom analytics | ●● Region-specific KPI sets |
| Oracle Fusion Field Service integration | Integrations | — Not included; file export / import | ● In: staff, availability, booking data · Out: allocations · Back: factual durations and times | ●● Multi-region |
| Additional data sources & BI | Integrations | — Not included | ● Up to 5 typical integrations — booking system, inventory for parts availability, HR/WFM for people availability, demand forecasting, BI | ●● Per-region data workflows |
| Deployment | (none) | ◐ Sandboxed | ● Enterprise-integrated — dedicated landing zone, IAM, observability | ●● Enterprise-integrated, multi-zone |

### Why it sells for the partner

- A natural Oracle Fusion Field Service cross-sell: native integration, known endpoints, a warm path into the account
- Net-new OCI consumption: recurring GPU workloads on dedicated OCI clusters, on top of the existing Fusion SaaS seat
- Repeatable: fits any Oracle Fusion Field Service customer with a heavy, centralized dispatch and scheduling routine

## Proof

- **Customer:** \<the delivery customer — a global home-appliance manufacturer>
- **Delivered:** Work-zone optimization PoC: NVIDIA cuOpt on OCI computing technician-to-zone allocations from the customer's own historical field-service data, with dispatcher approval in the loop. File-based in and out (XLSX upload, file export); no Oracle Fusion Field Service integration. Results modeled from 12 simulations across three countries. Three months.
- **Divergence line:** The pack generalizes the allocation rules the proof of value hard-coded; system integration and the feedback loop are Integration-tier scope.
- **Divergence from the pack:** The pack generalizes what the PoC hard-coded. Business logic — allocation rules, constraints, KPI formulas, forecasting — was written for one customer and is per-client configuration in the pack; the dispatcher UI and approval workflow are the reusable core. The PoC ran file-based with a limited rule set, which is exactly the PoV Jumpstart tier; Oracle Fusion Field Service integration, additional data sources and the feedback loop are sold as Integration-tier scope and were not delivered. Distance-based (zoneless) planning is a separate future product, not a gap in this pack.
- **Source:** spec-doc-2026-09-16, call-2026-07-07, site-2026-09-17
- **Proof story, anonymized:** Delivered as a proof of value with a global home-appliance manufacturer: zone and technician allocation computed on the operator's own historical data, reviewed and approved by its own dispatchers.

## Open questions

1. Customer name on partner-print artifacts: `clearance.customer_name_allowed.partner_print` is false here, but the delivered one-pager, deck, executive summary and section deck all print the customer's name and logo. Alex has not confirmed whether that approval stands. Until he does, every builder emits the anonymized descriptor and the delivered artifacts are out of compliance with their own spec.
2. Two figure sets for one pack. The print artifacts carry ~30 min / up to +26% / €190K per month; the mini-site carries the anonymized, modeled set (+4.5% median jobs per technician per day, ~5x three-year return, 83% of 12 simulations positive, 15–20% dispatcher productivity, no € figures). decisions-2026-09-18 says one metric set per pack, so one of the two has to go. This spec carries the one-pager set; the site set is not reproduced here.
3. `figure_status` for the €190K/month figure. The one-pager types it as an estimate at full launch, so it is recorded as `modeled`, not `pov_result`. Confirm.
4. Scaling-tier pricing is `tbd` on every artifact. Services and infrastructure both need a number or an explicit "scoped per engagement" line.
5. Target OCI consumption per tier was committed on the 2026-07-09 offering-deck review and never added to an artifact. Recorded as "-".
6. The `***` footnote marker on "Non-movable appointments" in the delivered feature-list docx has no footnote text in the file. What did it say?
7. The four optional Oracle products are inferred from the pack's integration list, not sourced from any artifact. Confirm or replace.
8. Catalog ids were reconciled against shared/data/oracle-products.yaml (version 2026-09-18): every id here now resolves. Three had no catalog entry and use the closest catalogued product — `oci-dedicated-ai-cluster` for the GPU cluster, `oci-vcn` for networking, and one merged `oracle-fusion-cloud-scm` entry where the example had separate inventory and demand-management ids. All three are logged as catalog change requests in shared/data/oracle-products.README.md; the catalog owner decides whether to split them out. Details in this folder's README.md.
9. `meta.source_engagement.delivered` carries no delivery window. The mini-site case study says three months; the exact start and end dates are not in any source read here.
10. Vertical labels: three different four-item lists exist (deck and feature list · mini-site generic industries · the productization workbook's Sheet3). This spec carries the deck labels with the site labels alongside; confirm which set is canonical for new artifacts.
11. Feature-level customization scope is unset by design — the delivered feature list scopes customization per AREA, and only `customization_scope_area` is filled. If the schema wants a feature-level value, it needs a source that does not exist today.
12. Feature-level `status` inherits the category's merged cell; the source has no per-feature granularity. Same question for the schema.
13. `specificity` tags are set only where the 2026-07-07 standard-vs-custom session supports them; everything else is `[]` rather than guessed. The full four-axis pass has not been run for this pack.
14. `vertical_differences` is filled only for workflow step 2 (Set the rules), which is the one step the vertical framings actually speak to. Steps 1, 3 and 4 are "-" for three of the four verticals.
15. Resolved in the schema, left here so the decision is visible: a KPI that is defined and measured per engagement but has no cleared headline figure is written `figure: "-"` (and `figure_status: "-"`), and needs no `attribution` — the enum did not need a fifth value, because `-` already means 'deliberately empty' everywhere in a spec. Four of the seven KPIs here sit in that state and keep their formula, baseline and caveat. What is still open is whether any of the four gets a cleared figure for the next artifact round.
16. `meta.name_variants.site` is Title Case per decisions-2026-09-18; the live listing ships sentence case. Which wins at the next site rebuild?

## Settings

### Clearance

| Channel | Customer may be named |
|---|---|
| Internal | yes |
| Partner print | no |
| Customer site | no |
| Demo | no |

- **Anonymized descriptor:** a global home-appliance manufacturer
- **Internal-only facts:**
  - named customer accounts and logos
  - contract values and per-engagement pricing beyond the published PoV price
  - the customer's service-zone geography, zone-naming convention and zone counts
  - technician identifiers and per-technician uplifts above the cleared median
  - headcount, POD and capacity numbers
  - the roadmap ceiling and any "gap" statement
- **Approvals:** (none)
- **Source:** site-2026-09-17, decisions-2026-09-18

### Contacts

- **Partner print:**
  - **Name:** Karsten Tramborg
  - **Title:** Alliances & Partnerships Director
  - **Email:** ktram@softserveinc.com
- **Site:**
  - **Mailbox:** oracle@softserveinc.com
  - **Named:** Karsten Tramborg
- **Internal:**
  - **Name:** Bohdan Khomych
  - **Email:** RnDrequest@softserveinc.com
  - **Note:** The person doing the packaging; the delivered section deck carries this name.
- **Source:** decisions-2026-09-18, one-pager-2026-07-17

### One-pager

- **Cta:**
  - **Question:** See the fit in one of your accounts?
  - **Answer:** Let's scope a proof of value on the customer's own data: 8 weeks to measured KPIs.

### Provenance

- **Inputs:**
  - **Id:** one-pager-2026-07-17
    - **Path:** \<practice-drive>/Projects/Oracle/Packs/Workforce optimization package/Workforce Optimization - Sales one-pager - Oracle.pdf
    - **Kind:** one-pager
    - **Read:** 2026-09-18
    - **Note:** The canonical sales one-pager (decisions-2026-09-18). The Jul-13 file at this path was overwritten in place with the Jul-17 version under the same name so the share link survived; the superseded Jul-13 PDF is archived locally. HTML build source lives only at \<owner-local>/Oracle/Workforce Optimization - Sales one-pager - Oracle.html
    - **Supplies:** problem_solution; one_liner; kpis; packages; architecture; oracle_products; contacts
  - **Id:** feature-list-2026-09-10
    - **Path:** \<practice-drive>/Projects/Oracle/Packs/Workforce optimization package/Workforce Optimization - Accelerator Pack one-pager.docx
    - **Kind:** feature-list
    - **Read:** 2026-09-18
    - **Note:** 4 areas / 13 categories / 38 features. Status glyph colours read from word/document.xml: #1485C3 available, #C1E4F5 partial, #AEB4BA roadmap.
    - **Supplies:** capabilities
  - **Id:** deck-2026-07-13
    - **Path:** \<practice-drive>/Projects/Oracle/Packs/Workforce optimization package/Workforce Optimization - Service packages - Oracle.pptx
    - **Kind:** deck
    - **Read:** 2026-09-17
    - **Note:** 10 slides. Read second-hand through component-map-2026-09-17, not opened in this pass.
    - **Supplies:** verticals; packages; architecture
  - **Id:** exec-summary-2026-07-17
    - **Path:** \<owner-local>/Oracle/Workforce Optimization - Executive summary - Oracle.pptx
    - **Kind:** deck
    - **Read:** 2026-09-17
    - **Note:** Read second-hand through component-map-2026-09-17.
    - **Supplies:** kpis
  - **Id:** section-deck-2026-09-11
    - **Path:** \<practice-drive>/Projects/Oracle/Packs/Monthly AI products overviews/AI Solutions review - Sep/Oracle AI Packages - section slides.pptx
    - **Kind:** deck
    - **Read:** 2026-09-17
    - **Note:** Latest executive-summary style; WfO is slides 5–6. Read second-hand through component-map-2026-09-17.
    - **Supplies:** contacts
  - **Id:** site-2026-09-17
    - **Path:** \<site-repo>/site/data/content.js
    - **Kind:** listing
    - **Read:** 2026-09-18
    - **Note:** products[] slug workforce-optimization, lines 1751–2088.
    - **Supplies:** icp; verticals; workflow; architecture; oracle_products; packages; clearance
  - **Id:** site-2026-09-29
    - **Path:** \<site-repo>/site/data/content.js
    - **Kind:** listing
    - **Read:** 2026-09-29
    - **Note:** products[] slug workforce-optimization: the `oneLiner` as rewritten in site round 19, the business value with no engine or platform name.
    - **Supplies:** one_liner
  - **Id:** demo-2026-09-16
    - **Path:** \<site-repo>/site/demo/workforce-optimization/data.js
    - **Kind:** demo
    - **Read:** 2026-09-17
    - **Note:** Read second-hand through component-map-2026-09-17 and spec-doc-2026-09-16.
    - **Supplies:** workflow
  - **Id:** spec-doc-2026-09-16
    - **Path:** \<owner-repo>/context/areas/softserve/docs/2026-09-16_wfo-pack-spec-for-demo.md
    - **Kind:** call-note
    - **Read:** 2026-09-18
    - **Note:** Distillation of the PoC user guide v3, requirements 1.6, UC #3 scope and the KPI methodology PDF.
    - **Supplies:** workflow; kpis; architecture; meta
  - **Id:** component-map-2026-09-17
    - **Path:** \<owner-repo>/context/areas/softserve/docs/2026-09-17_packaging-skills-prep/B-artifact-component-map.md
    - **Kind:** call-note
    - **Read:** 2026-09-18
    - **Supplies:** all
  - **Id:** decisions-2026-09-18
    - **Path:** \<owner-repo>/context/areas/softserve/docs/2026-09-17_packaging-skills-prep/decisions-2026-09-18.md
    - **Kind:** call-note
    - **Read:** 2026-09-18
    - **Supplies:** meta; packages; kpis; capabilities; contacts
  - **Id:** call-2026-06-26
    - **Path:** \<owner-repo>/context/areas/softserve/calls/oracle/2026-06-26_sales-call_gero-tshirt-packaging.md
    - **Kind:** call-note
    - **Read:** 2026-09-17
    - **Note:** Tier semantics co-designed with the partner. Read second-hand through A1-sessions-decks-onepagers.md.
    - **Supplies:** packages
  - **Id:** call-2026-07-07
    - **Path:** \<owner-repo>/context/areas/softserve/calls/oracle/
    - **Kind:** call-note
    - **Read:** 2026-09-17
    - **Note:** The standard-vs-custom classification session. Read second-hand through A1-sessions-decks-onepagers.md §2.
    - **Supplies:** capabilities; icp; meta
  - **Id:** call-2026-07-09
    - **Path:** \<owner-repo>/context/areas/softserve/calls/oracle/
    - **Kind:** call-note
    - **Read:** 2026-09-17
    - **Note:** Offering-deck review with partner sales. Read second-hand through A1-sessions-decks-onepagers.md §2.
    - **Supplies:** kpis; packages
- **Research brief:** packs/workforce-optimization/research-brief.md
