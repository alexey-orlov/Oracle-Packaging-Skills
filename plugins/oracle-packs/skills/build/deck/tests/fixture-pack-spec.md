---
slug: workforce-optimization
status: confirmed
spec_version: 1
roadmap_item_id: workforce-optimization
roadmap_block: Data analysis & optimization
---

# Workforce Optimization

- **Site:** Workforce Optimization
- **Internal slide:** Workforce Optimization App
- **External:** Workforce optimization
- **External subheading:** Accelerator App by SoftServe
- **Source of the name:** user:2026-09-18

## One-liner

- **Full:** The same technicians complete more jobs a day, with less driving and waiting, on a four-week plan balanced across every zone.
- **Short:** A region's four-week field plan, optimized in minutes and approved by dispatchers.
- **Banned words checked:** yes
- **Source:** user:2026-09-18

## Problem and solution

### Problem

Field-service operators plan their mobile workforce by hand: work zones, technician assignments, dozens of rules and constraints.

### Solution

A GPU optimization engine ingests demand, availability, skills and constraints and computes the best technician-to-zone-to-job plan in minutes. Dispatchers review it on a live map, re-optimize and write the approved plan back to the field-service system.

- **Problem points:**
  - Suboptimal efficiency: uneven workloads and under-used capacity
  - Lower customer satisfaction: longer wait times from suboptimal allocations
  - Poor scalability: planning hinges on scarce senior dispatchers; new zones launch slowly
- **Reframe:** Review the plan, don't build it
- **Reframe question:** What if dispatchers reviewed the plan instead of building it?
- **Today:** Dispatchers maintain work zones and technician allocations by hand — region by region, juggling postcode coverage, skills, working days and absences, with little room left to optimize.
- **Tomorrow:** The dispatcher uploads the period's data, runs the optimizer, and reviews the proposed allocation on a live map — comparing, approving or re-running before the plan is exported.
- **Source:** user:2026-09-18

## Who buys it

Any mobile field force planned against skills, availability and geography.

- **Buyer roles:** VP Field Service; COO; Head of Dispatch
- **Qualifying signals:** central dispatch team planning 200+ technicians; a field-service system of record already in place
- **Disqualifiers:** fully self-scheduling workforce with no central planning
- **Source:** user:2026-09-18

## Industries

### Residential appliance & white-goods repair

- **Framing:**
  - **Problem:** In-home repair is planned by hand against parts, skills and travel.
  - **Solution:** The solver plans the whole region against skills, parts, travel and existing bookings at once.
- **What matters here:** Dispatch home-repair technicians by skill, spare parts and travel — absorbing urgent call-outs and no-shows without re-planning the day.
- **Status:** proven

### Utilities — water · gas · electric

- **Framing:**
  - **Problem:** Crews are scheduled across territories against SLAs and outage spikes.
  - **Solution:** Planned and emergency work are balanced in one optimization pass.
- **What matters here:** Schedule field crews across service territories against SLAs, outage spikes and crew certifications, balancing planned and emergency work.
- **Status:** plausible

### Telecom & cable

- **Framing:**
  - **Problem:** Install-and-repair visits must hit tight appointment windows.
  - **Solution:** Line skills and travel are matched to the window before the day starts.
- **What matters here:** Route install-and-repair technicians to tight appointment windows across regions, matching line skills and cutting customer wait time.
- **Status:** plausible

### Industrial · medical-device · IT equipment service

- **Framing:**
  - **Problem:** Contracted equipment needs engineers matched by skill and SLA.
  - **Solution:** Asset-based allocation keeps uptime-critical machines covered.
- **What matters here:** Allocate asset-based service engineers to contracted equipment by skill, SLA and location — keeping high-value machines uptime-critical.
- **Status:** plausible

## Capabilities

### Allocation rules

- **Customization in this area:** Custom rules implementation · rules configuration · matching rules with source data formats · objective balancing and weight tuning.

| Category | Feature | Status | From tier | Customization |
|---|---|---|---|---|
| Workforce availability rules | Technician availability, skills and planned absences | available | pov | Rule weights and constraint set per customer |
| Distance-based rules | Travel time and zone contiguity constraints | available | pov |  |
| Optimization function & rule weights | Objective weighting and penalty/reward tuning | partial | integration |  |

### Review and approval workflow

- **Customization in this area:** Model-decision explanations and recommendation tuning to match custom allocation rules.

| Category | Feature | Status | From tier |
|---|---|---|---|
| Review | Side-by-side current vs optimized plan on a live map | available | pov |
| Feedback loop | Per-zone approve / reject / comment, then re-optimize | partial | integration |

### KPIs and analytics

- **Customization in this area:** Custom KPIs and custom calculation formulas.

| Category | Feature | Status | From tier |
|---|---|---|---|
| KPI | Productivity, capacity utilization, travel, workload balance | available | pov |
| Baseline comparison | Baseline vs optimized plan on the same window | available | pov |

### Integrations

- **Customization in this area:** Integration configuration and custom integrations.

| Category | Feature | Status | From tier |
|---|---|---|---|
| Integrations | Field-service system as source and destination | partial | integration |

## Workflow

### Inputs

| System | Data |
|---|---|
| Field-service system of record | work orders, technicians, zones, availability |

### 1. Load the period's data

- **Actor:** human
- **Human in the loop:** yes
- **If it fails:** Missing fields flag the row, never drop it; the dispatcher resolves.

### 2. Set the rules

- **Actor:** human
- **Human in the loop:** yes
- **If it fails:** A conflicting hard rule blocks the run with the conflicting pair named.

### 3. Solve the plan

- **Actor:** ai
- **Human in the loop:** no
- **If it fails:** No feasible plan → the binding constraint is reported, not a partial plan.

### 4. Review, approve, measure

- **Actor:** human
- **Human in the loop:** yes
- **If it fails:** Rejected zones return to step 2 with the dispatcher's comment attached.

### Outputs

| System | Data |
|---|---|
| Field-service system of record | approved plan written back |

## Architecture

### Inputs

| System | Data |
|---|---|
| Field-service system of record | technicians, availability, bookings, default allocations |
| Additional data sources | booking system, parts inventory, HR/WFM, demand forecasting |

### Stack, top to bottom

| Layer | Vendor | Items | Summary | Catalog id |
|---|---|---|---|---|
| Custom configuration | SoftServe | rule set; objective weights; KPI definitions | Client rules, constraints and KPI definitions |  |
| Accelerator business app | Oracle + SoftServe | optimizer service; dispatcher UI; plan versioning | The optimization app and its dispatcher console |  |
| Optimization engine | NVIDIA | NVIDIA cuOpt | GPU-accelerated solver for large-scale workforce and route optimization | `nvidia-cuopt` |
| Infrastructure | Oracle | dedicated GPU cluster (4–8 GPUs); object storage; networking; IAM | OCI compute with GPUs, object storage, networking and IAM |  |

### Outputs

| System | Data |
|---|---|
| Field-service system of record | optimized allocations — zones and visits |
| BI | KPIs per plan version |

## Oracle products

| Id | Name | Role | Why | At PoV | At Integration | At Scaling |
|---|---|---|---|---|---|---|
| oracle-fusion-field-service | Oracle Fusion Field Service | required | Source of work orders and destination of the approved plan | file export / import | API write-back | API plus execution telemetry |
| oci-dedicated-ai-cluster | Dedicated AI Cluster | required | Runs the optimization engine |  |  |  |
| oci-object-storage | OCI Object Storage | required | Landing zone for the period's data |  |  |  |
| oracle-analytics-cloud | Oracle Analytics Cloud | optional | Could consume the per-plan KPI extract |  |  |  |

## Metrics

### Planning cycle time

- **Kind:** business
- **Signed off by:** VP Field Service
- **Chip:** Planning time ↓
- **Label:** to optimize and approve a region's 4-week plan
- **Formula:** Time from demand freeze to approved plan
- **Baseline:** ~2 days
- **Figure:** ~30 min
- **Show baseline:** yes
- **Figure status:** pov_result
- **Attribution:**
  - **Named when allowed:** Proof of value
  - **Otherwise:** a proof of value at a global home-appliance manufacturer
- **Caveat:** Illustrative proof-of-value result, measured before/after; not contractual.

### Technician productivity

- **Kind:** business
- **Signed off by:** VP Field Service
- **Chip:** Productivity ↑
- **Label:** productivity gain on proof-of-value data across three markets
- **Formula:** Jobs per technician per working day
- **Baseline:** manual plan
- **Figure:** up to +26%
- **Figure status:** pov_result
- **Attribution:**
  - **Otherwise:** a proof of value at a global home-appliance manufacturer
- **Caveat:** Productivity gain on proof-of-value data across three markets; illustrative, not contractual.

### Avoided staffing cost

- **Kind:** business
- **Signed off by:** COO
- **Chip:** Capacity utilization ↑
- **Label:** estimated saving at full launch, valued as staffing avoided
- **Formula:** Productivity gain valued at the cost of the staffing it avoids
- **Figure:** €190K / month
- **Figure status:** modeled
- **Attribution:**
  - **Otherwise:** modeled from the proof-of-value result
- **Caveat:** Estimated saving at full launch, valued as the staffing it avoids; illustrative, not contractual.

## Packages

- **Target OCI consumption:** Recurring dedicated-GPU consumption per planning region, growing with the number of regions planned.
- **Anchor line:** Anchored to the customer's field-service system — every optimization run is OCI GPU consumption an account exec can sell.

### PoV Jumpstart · S

- **Id:** pov
- **Scope:** Prove the KPI gains on the customer's own data and rules.
- **Duration:** 4–8 weeks (target 6, hard cap 10)
- **Services price:** €90K · confirmed
- **Infrastructure price per month:** €2K · indicative
- **What you get:** An optimized plan on the customer's own data, measured against their baseline
- **In scope:** one region; one rule set; file-based import
- **Out of scope:** write-back; multi-region rules

### Integration · M

- **Id:** integration
- **Scope:** Live at one location, embedded in the dispatch workflow.
- **Duration:** 12–20 weeks
- **Services price:** €300K–€500K · indicative
- **Infrastructure price per month:** €25K · indicative

### Scaling · L

- **Id:** scaling
- **Scope:** Scaling across locations: heterogeneous rules and data workflows per region.
- **Duration:** 12–52 weeks
- **Services price:** to be defined
- **Infrastructure price per month:** to be defined

### How each capability area is handled per tier

#### Optimization rules & guardrails

- **PoV:** Foundational allocation with the recurring constraints — zones, skills, planned absences
- **Integration:** Full operational complexity — urgent jobs, crews, SLAs, parts coupling
- **Scaling:** Multiple region-specific optimization-rule configurations

#### Re-optimization & feedback loop

- **PoV:** `''`
- **Integration:** Feedback-driven re-optimization with alternative allocation options
- **Scaling:** Multiple region-specific re-optimization workflows

#### Analytics & efficiency KPIs

- **PoV:** Core KPIs predicted at scheduling time against the baseline
- **Integration:** KPIs with an execution-data feedback loop plus custom analytics
- **Scaling:** Multiple region-specific KPI sets
- **Glyphs:**
  - **PoV:** ●

#### Field-service system integration

- **PoV:** `''`
- **Integration:** In: staff, availability, bookings · Out: allocations · Back: actual durations
- **Scaling:** Multiple region-specific integrations

#### Additional data sources & BI

- **PoV:** `''`
- **Integration:** Up to five integrations — booking, parts, HR/WFM, forecasting, BI
- **Scaling:** Multiple region-specific integration landscapes

#### Deployment

- **PoV:** Sandboxed
- **Integration:** Enterprise-integrated — landing zone, IAM, observability
- **Scaling:** Enterprise-integrated, multi-zone

### Why it sells for the partner

- A natural field-service cross-sell — the pack attaches to an application the account already runs
- Net-new GPU consumption on top of the SaaS seat — every optimization run is metered compute
- Repeatable across similar accounts — one rule model, re-configured per customer rather than rebuilt

## Proof

- **Customer:** (internal only — not set in this fixture)
- **Delivered:** Proof of value on live field-service data across three markets: zone and technician allocation computed by a GPU solver, reviewed and approved by the customer's own dispatchers before export.
- **Divergence from the pack:** The pack generalizes the allocation rule set; the delivered proof of value hard-coded one operator's rules and imported data by file.
- **Proof headline:** A 4-week plan, optimized in ~30 minutes, with measurable productivity gains
- **Vertical case:** Vertical case: residential appliance & white-goods repair

## Next steps

1. **Internal enablement webinar:** for the SoftServe and partner sales teams
2. **Customer-facing webinar:** present the use case to field-service accounts
3. **Replicate the structure for the next pack:** same package structure, next delivered engagement

## Open questions

1. Which vertical label set ships externally — the print set or the site's generic industries?

## Settings

### Clearance

| Channel | Customer may be named |
|---|---|
| Internal | no |
| Partner print | no |
| Customer site | no |
| Demo | no |

- **Anonymized descriptor:** a global home-appliance manufacturer
- **Internal-only facts:** contract value; named customer accounts; headcount
- **Approvals:** (none)

### Contacts

- **Partner print:**
  - **Name:** Karsten Tramborg
  - **Title:** Alliances & Partnerships Director
  - **Email:** ktram@softserveinc.com
- **Site:**
  - **Mailbox:** oracle@softserveinc.com
  - **Named:** Karsten Tramborg
- **Internal:**
  - **Name:** R&D packaging team
  - **Email:** RnDrequest@softserveinc.com

### Deck

- **Seller lead:** What the pack gives an account exec that a custom project does not.
- **Cta:** Ready to test the fit in one of your accounts?

### Executive summary

- **Goal:** Better sales enablement and customer acquisition on delivered, referenceable use cases.

### Provenance

- **Inputs:**
  - **Path:** (fixture — derived from the WfO artifact/component map)
    - **Kind:** feature-list
    - **Read:** 2026-09-18
- **Research brief:** packs/workforce-optimization/research-brief.md
