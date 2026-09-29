---
slug: workforce-optimization
status: confirmed
spec_version: 1
generated_with: { roadmap_version: 2026-09-17, catalog_version: 2026-09-18 }
roadmap_item_id: workforce-optimization
roadmap_block: Data analysis & optimization
---

# Workforce Optimization

- **Site:** Workforce Optimization
- **Internal slide:** Workforce Optimization App
- **External:** Workforce optimization
- **External subheading:** Accelerator App by SoftServe
- **Source of the name:** user:2026-09-18
- **Eyebrow:** Oracle AI & Data Solutions

## One-liner

- **Full:** The same technicians complete more jobs a day, with less driving and waiting, on a four-week plan balanced across every zone.
- **Short:** A region's four-week field plan, optimized in minutes and approved by dispatchers.
- **Banned words checked:** yes
- **Source:** user:2026-09-18
- **KPI chips:**
  - **Productivity:** up
  - **Capacity utilization:** up
  - **Customer wait time:** down

## Problem and solution

### Problem

Field-service operators plan their mobile workforce by hand: work zones, technician assignments, dozens of rules and constraints.

### Solution

NVIDIA cuOpt ingests demand, availability, skills and constraints, and computes the best technician-to-zone-to-job plan in minutes. Dispatchers review it on a live map, re-optimize and write the plan back to Oracle Fusion Field Service.

- **Problem points:**
  - **Suboptimal efficiency:** uneven workloads and under-used capacity
  - **Lower customer satisfaction:** longer wait times from suboptimal allocations
  - **Poor scalability:** planning hinges on scarce senior dispatchers; new zones launch slowly
- **Reframe:** review the plan, not build it
- **Source:** user:2026-09-18

## Who buys it

Field-service operations leaders at companies running Oracle Fusion Field Service with 200+ technicians.

- **Buyer roles:** VP Field Service; COO
- **Qualifying signals:** centralized dispatch team; manual zone planning; seasonal demand spikes
- **Disqualifiers:** fewer than 50 technicians; no route or zone constraints
- **Source:** user:2026-09-18

## Industries

### Appliance & white-goods repair

- **Framing:**
  - **Problem:** Home-repair demand swings daily and technicians carry different part sets.
  - **Solution:** Dispatch by skill, spare parts and travel, absorbing urgent call-outs and no-shows without re-planning the day.
- **What matters here:** First-visit fix rate and same-day absorption of urgent jobs.
- **Status:** proven

### Utilities: water, gas, electric

- **Framing:**
  - **Problem:** Planned maintenance competes with outage response across large territories.
  - **Solution:** Schedule crews against SLAs, outage spikes and certifications, balancing planned and emergency work.
- **What matters here:** SLA compliance per territory and crew certification coverage.
- **Status:** plausible

### Telecom & cable

- **Framing:**
  - **Problem:** Install-and-repair appointments carry tight customer windows.
  - **Solution:** Route technicians to tight appointment windows across regions, matching line skills and cutting customer wait time.
- **What matters here:** Appointment-window adherence and repeat-visit rate.
- **Status:** plausible

### Industrial, medical & IT equipment

- **Framing:**
  - **Problem:** Contracted equipment uptime is the commercial commitment, not visit count.
  - **Solution:** Allocate asset-based service engineers by skill, SLA and location, keeping high-value machines uptime-critical.
- **What matters here:** Contracted uptime per asset class and engineer specialization depth.
- **Status:** plausible

## Capabilities

### Allocation rules

- **Customization in this area:**
  - Custom rules implementation
  - Rules configuration
  - Matching rules with source data formats
  - Balancing optimization function with penalty / rewards, allocation rules weights tuning to achieve optimal allocation per customer
  - Introduction of additional optimization objectives

| Category | Feature | Status | From tier | Note |
|---|---|---|---|---|
| Workforce availability rules | Skill-based allocation | available | pov |  |
| Workforce availability rules | Maximal load per day | available | pov |  |
| Workforce availability rules | Planned vacation reallocation | available | pov |  |
| Workforce availability rules | Same-day sickness handling | partial | integration |  |
| Distance-based | Maximal distance / travel time rules | partial | integration |  |
| Distance-based | Real-time traffic / live travel data | roadmap | scaling |  |
| Dynamic | Within-day job reassignment | roadmap | scaling |  |
| Dynamic | Urgent / emergency request handling | roadmap | scaling |  |
| Workzone-based rules | Default work zones per technician | available | pov |  |
| Workzone-based rules | Work zone-level demand | available | pov |  |
| Workzone-based rules | Neighboring workzones | available | integration |  |
| Workzone-based rules | Cross-zone allocation of selected technicians | partial | integration |  |
| Forecast-based rules | Forecast-based allocation | available | integration | forecast data to be provided by the customer |
| Commitment-based rules | Non-movable appointments | partial | pov |  |
| Commitment-based rules | Different SLA types per appointment | available | integration |  |
| Other rules | Spare-parts availability | roadmap | scaling |  |
| Other rules | Crew-based assignments | roadmap | scaling |  |
| Other rules | Other custom rules | roadmap | scaling |  |
| Optimization function & rule weights | Multi-objective optimization (productivity, waiting time, workload balance) | available | pov |  |
| Optimization function & rule weights | Allocation rules weighting (hard / soft) | available | pov |  |
| Optimization function & rule weights | Minimal disruption of current allocation | available | integration |  |

### Review and approval workflow

- **Customization in this area:**
  - Model decisions explanations / recommendations tuning to match custom allocation rules

| Category | Feature | Status | From tier |
|---|---|---|---|
| Review | Dispatcher UI (map, table views) | available | pov |
| Review | Dispatcher approval / rejection | available | pov |
| Review | Model decisions explanation and recommendations | partial | integration |
| Feedback loop | Iterative feedback-based re-optimization | available | integration |
| Feedback loop | Human-feedback-driven model tuning | roadmap | scaling |
| Feedback loop | Alternative allocation options (what-if) | roadmap | scaling |

### KPIs and analytics

- **Customization in this area:**
  - Custom (additional) KPIs
  - Custom formula for KPI calculation

| Category | Feature | Status | From tier |
|---|---|---|---|
| KPI | Productivity (jobs / technician / day) | available | pov |
| KPI | Capacity utilization | available | pov |
| KPI | Travel reduction | available | pov |
| KPI | Workload balance | available | pov |
| Baseline comparison | Compare baseline vs optimized allocation | available | pov |

### Integrations

- **Customization in this area:**
  - Integration configuration
  - Custom integrations

| Category | Feature | Status | From tier | Note |
|---|---|---|---|---|
| Integrations | Oracle Fusion Field Service as a datasource / destination | partial | integration | file export / import at PoV; API write-back is Integration-tier scope |
| Integrations | Demand forecasting datasource | roadmap | scaling |  |
| Integrations | Visits booking system | roadmap | scaling |  |
| Integrations | Inventory system for spare-parts availability | roadmap | scaling |  |
| Integrations | HRM system for people availability | roadmap | scaling |  |
| Integrations | BI system for KPIs / analytics exports | roadmap | integration |  |

## Workflow

### Inputs

| System | Data | technicians | zones |
|---|---|---|---|
| Oracle Fusion Field Service | work orders | — | — |

### 1. Load the period's data

- **Actor:** system
- **Human in the loop:** no
- **If it fails:** Missing fields → row flagged, not dropped; dispatcher resolves

### 2. Set the rules

- **Actor:** human
- **Human in the loop:** yes
- **If it fails:** Conflicting hard rules → solver reports the conflict before running

### 3. Solve the plan

- **Actor:** ai
- **Human in the loop:** no
- **If it fails:** No feasible plan → relax soft constraints and report which

### 4. Review

- **Actor:** human
- **Human in the loop:** yes
- **If it fails:** Rejected zones return to step 2 with the dispatcher's comment attached

### Outputs

| System | Data |
|---|---|
| Oracle Fusion Field Service | optimized plan written back |

## Architecture

### Inputs

| System | Data | Note |
|---|---|---|
| Oracle Fusion Field Service | technicians data, default allocations | field workforce & assignments |

### Stack, top to bottom

| Layer | Name | Vendor | Items | Catalog id | Note |
|---|---|---|---|---|---|
| Custom configuration |  | SoftServe | client rules; constraints; KPI definitions |  |  |
| Accelerator business app | Accelerator business app | Oracle + SoftServe |  |  | optimization engine + dispatcher UI |
| Optimization engine | NVIDIA cuOpt | NVIDIA |  | `nvidia-cuopt` | GPU-accelerated solver |
| Infrastructure |  | Oracle Cloud Infrastructure | OCI Dedicated AI cluster |  |  |

### Outputs

| System | Data |
|---|---|
| Oracle Fusion Field Service | optimized allocations: zones, visits |

## Oracle products

| Id | Role | Why | At PoV | At Integration | At Scaling |
|---|---|---|---|---|---|
| oracle-fusion-field-service | required | Source of work orders and destination of the plan | file export / import | API write-back | API + telemetry |
| oci-dedicated-ai-cluster | required | Runs the optimization engine |  |  |  |
| oci-object-storage | required | Landing zone for plan inputs and exports |  |  |  |
| oci-iam | required | Access control for the dispatcher application |  |  |  |
| oracle-analytics-cloud | optional | Destination for per-plan KPI exports |  |  |  |

## Metrics

### Planning cycle time

- **Kind:** business
- **Signed off by:** VP Field Service
- **Chip label:** Planning cycle time
- **Direction:** down
- **Formula:** Time from demand freeze to an approved plan for one region
- **Baseline:** ~2 days manual
- **Figure:** ~30 min
- **Figure status:** pov_result
- **One-pager label:** to optimize and approve a region's 4-week plan: down from ~2 days
- **Attribution:**
  - **Named when allowed:** Proof of value · \<customer, on clearance>
  - **Otherwise:** proof of value at a global home-appliance manufacturer
- **Caveat:** KPIs measured before/after on proof-of-value data; figures are illustrative, not contractual.
- **Source:** one-pager 2026-07-17

### Productivity gain

- **Kind:** business
- **Signed off by:** VP Field Service
- **Direction:** up
- **Formula:** Total jobs ÷ days with at least one job, averaged across technicians
- **Baseline:** current manual plan for the same window
- **Figure:** +26%
- **Figure prefix:** up to
- **Figure status:** pov_result
- **One-pager label:** productivity gain on proof-of-value data across three countries
- **Attribution:**
  - **Named when allowed:** Proof of value · \<customer, on clearance>
  - **Otherwise:** proof of value at a global home-appliance manufacturer
- **Caveat:** KPIs measured before/after on proof-of-value data; figures are illustrative, not contractual.
- **Source:** one-pager 2026-07-17

### Staffing cost avoided

- **Kind:** business
- **Signed off by:** COO
- **Direction:** down
- **Formula:** Avoided additional technician headcount valued at fully loaded cost
- **Baseline:** planned hiring for the same demand
- **Figure:** €190K
- **Figure suffix:** / month
- **Figure status:** modeled
- **One-pager label:** estimated savings at full launch, valued as the cost of additional staffing avoided
- **Attribution:**
  - **Named when allowed:** Proof of value · \<customer, on clearance>
  - **Otherwise:** modeled at a global home-appliance manufacturer
- **Caveat:** KPIs measured before/after on proof-of-value data; figures are illustrative, not contractual.
- **Source:** one-pager 2026-07-17

## Packages

- **Target OCI consumption:** Dedicated AI cluster, 4-8 GPUs, running on each planning cycle

### PoV Jumpstart · S

- **Id:** pov
- **Scope:** Manual data import, limited rule set: prove the KPI gains on the customer's data.
- **Duration:** 4–8 weeks (target 6, hard cap 10)
- **Services price:** €90K · confirmed
- **Infrastructure price per month:** €2K · indicative · Indicative; depends on the usage and optimization rules complexity
- **What you get:** A measured before/after on the customer's own data; A sandboxed dispatcher UI
- **In scope:** one region; one rule set; file-based data exchange
- **Out of scope:** production integration; multi-region rules

### Integration · M

- **Id:** integration
- **Scope:** Full setup and integration, live at one location: no manual work, embedded in the workflow.
- **Duration:** 12–20 weeks
- **Services price:** €300K–€500K · indicative
- **Infrastructure price per month:** €25K · indicative
- **What you get:** Live write-back to Oracle Fusion Field Service; Customer rules and weights

### Scaling · L

- **Id:** scaling
- **Scope:** Scaling across locations: heterogeneous rules and data workflows per region.
- **Duration:** 12–52 weeks
- **Services price:** to be defined
- **Infrastructure price per month:** to be defined

### How each capability area is handled per tier

| Area | PoV | Integration | Scaling | Level at PoV | Level at Integration | Level at Scaling |
|---|---|---|---|---|---|---|
| Optimization rules & guardrails | Foundational allocation with the recurring, most typical constraints — zones, skills, planned absences | Advanced allocation with all operational complexities — urgent jobs, crews, SLAs, inventory coupling | Multiple region-specific optimization-rule configurations | partial | included | advanced |
| Re-optimization & feedback loop |  |  |  | none | included | advanced |
| Analytics & efficiency KPIs |  |  |  | included | included | advanced |
| Oracle Fusion Field Service integration | — out of PoV scope; data arrives by file export / import | ● In: staff, availability, booking data · Out: allocations · In: factual durations & times | ●● Multi-region write-back with telemetry |  |  |  |
| Additional data sources & BI |  | Up to 5 typical integrations — booking, inventory, HR/WFM, demand forecasting, BI |  | none | included | advanced |
| Deployment | Sandboxed | Enterprise-integrated (dedicated landing zone, IAM, observability) | Enterprise-integrated, multi-zone | partial | included | advanced |

### Why it sells for the partner

- **A natural OFS cross-sell:** native Oracle Fusion Field Service integration - known endpoints, a warm path into the account
- **Net-new OCI consumption:** recurring GPU workloads on dedicated OCI clusters, on top of the existing Fusion SaaS seat
- **Repeatable:** fits any OFS customer with a heavy, centralized dispatch and scheduling routine

## Proof

- **Customer:** —
- **Delivered:** proof of value, 2026, GPU-accelerated zone and technician allocation on field-service data across three countries
- **Divergence from the pack:** The pack ships a standard rule set; the delivered proof of value hard-coded the customer's zone rules.
- **Proof story, anonymized:** At a global home-appliance manufacturer, dispatchers planned a repair field force by hand: ZIP-code work zones and technician allocations, region by region. With the cuOpt-powered dispatcher app on OCI they now review, approve or re-run an optimized plan and export it straight to Oracle Fusion Field Service.

## Open questions

(none)

## Settings

### Clearance

| Channel | Customer may be named |
|---|---|
| Internal | no |
| Partner print | no |
| Customer site | no |
| Demo | no |

- **Anonymized descriptor:** a global home-appliance manufacturer
- **Forbidden strings:** (none)
- **Internal-only facts:** contract value; named customer accounts; headcount
- **Disclaimer:** Indicative scope and pricing for discussion; not an offer.
- **Approvals:** (none)

### Contacts

- **Partner print:**
  - **Name:** Karsten Tramborg
  - **Title:** Alliances & Partnerships Director
  - **Organization:** SoftServe
  - **Email:** ktram@softserveinc.com
- **Site:**
  - **Mailbox:** oracle@softserveinc.com
  - **Named:** Karsten Tramborg
- **Internal:**
  - **Name:** Alex Orlov
  - **Title:** Product advisor, R&D
  - **Organization:** SoftServe
  - **Email:** RnDrequest@softserveinc.com

### One-pager

- **Cta:**
  - **Question:** See the fit in one of your accounts?
  - **Answer:** Let's discuss a Proof of Value on the customer's data: 6 weeks to measurable KPIs.

### Feature list

- **Intro label:** App.
- **Intro:** Workforce Optimization automates the planning of a mobile field-service workforce — computing the optimal technician-to-zone-to-job allocation against skills, availability, SLAs, travel and business constraints, so dispatchers review and approve an optimized plan instead of building it by hand.

### Provenance

- **Inputs:**
  - **Path:** Workforce Optimization - Sales one-pager - Oracle.html
    - **Kind:** one-pager
    - **Read:** 2026-09-17
  - **Path:** Workforce Optimization - Accelerator Pack one-pager.docx
    - **Kind:** feature-list
    - **Read:** 2026-09-17
- **Research brief:** packs/workforce-optimization/research-brief.md

## Other fields

```yaml
workflow.steps[3].approve: null
workflow.steps[3].measure: null
```
