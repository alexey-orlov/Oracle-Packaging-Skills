---
slug: workforce-optimization
status: confirmed
spec_version: 1
generated_with: { roadmap_version: 2026-09-17, catalog_version: 2026-09-18 }
roadmap_item_id: workforce-optimization
roadmap_block: Data analysis & decision agents
---

# Workforce Optimization

- **Site:** Workforce Optimization
- **Internal slide:** Workforce Optimization App
- **External:** Workforce optimization
- **External subheading:** Accelerator App by SoftServe
- **Source of the name:** user:2026-09-18

## One-liner

- **Full:** Re-plan technician zones and daily routes on your own field-service data, and hand the dispatcher a plan to approve instead of a blank grid.
- **Short:** Your dispatchers approve the plan instead of building it.
- **Banned words checked:** yes
- **Source:** user:2026-09-18

## Problem and solution

### Problem

Dispatchers plan technician work zones by hand, so the plan is stale before the day starts.

### Solution

The app re-optimizes zones and daily plans on the customer's own data and hands the dispatcher a plan to review.

- **Reframe:** Review the plan, don't build it
- **Source:** user:2026-09-18

## Who buys it

Field-service operations leaders at companies running Oracle Fusion Field Service with 200+ technicians

- **Buyer roles:** VP Field Service; COO
- **Qualifying signals:** Manual zone planning; Overtime above plan; Technician utilization below 70%
- **Disqualifiers:** Fewer than 50 technicians; No digital work-order system
- **Source:** user:2026-09-18

## Industries

### Industrial equipment service

- **Framing:**
  - **Problem:** Skill-matched technicians are scarce, so a mis-assigned job costs a second visit.
  - **Solution:** Allocation weights skills and travel together, and flags the jobs no one nearby can take.
- **What matters here:** First-time fix rate, not raw travel time
- **Worked example:** A regional service arm re-plans 1,800 weekly work orders across 14 zones.
- **Status:** plausible

## Capabilities

### Allocation rules

- **Customization in this area:** Rule weights and the constraint set, per customer

| Category | Feature | Status | From tier | Customization | Specificity | Source |
|---|---|---|---|---|---|---|
| Availability | Technician availability and skills constraints | available | pov | Rule weights and constraint set per customer | use_case | feature-list 2026-07-17 |

## Workflow

### Inputs

| System | Data | technicians | zones |
|---|---|---|---|
| Oracle Fusion Field Service | work orders | — | — |

### 1. Ingest and validate demand

- **Actor:** system
- **Human in the loop:** no
- **If it fails:** Missing fields flag the row, they never drop it; the dispatcher resolves

### 2. Optimize zones and daily plan

- **Actor:** ai
- **Human in the loop:** no
- **If it fails:** No feasible plan returns the previous plan plus the broken constraints

### 3. Review and approve

- **Actor:** human
- **Human in the loop:** yes
- **If it fails:** An edited plan is re-checked before write-back

### Outputs

| System | Data |
|---|---|
| Oracle Fusion Field Service | approved plan written back |

## Architecture

### Inputs

- work orders
- technician roster
- zone geometry

### Stack, top to bottom

| Layer | Vendor | Items | Catalog id |
|---|---|---|---|
| Custom configuration | SoftServe | rule weights; review UI |  |
| Accelerator business app | Oracle + SoftServe | planning app |  |
| Optimization engine | NVIDIA | NVIDIA cuOpt | `nvidia-cuopt` |
| Infrastructure | Oracle | OCI compute with GPUs; Object Storage |  |

### Outputs

- approved plan
- plan telemetry

## Oracle products

| Id | Role | Why | At PoV | At Integration | At Scaling |
|---|---|---|---|---|---|
| oci-gpu-instances | required | Runs the optimization engine |  |  |  |
| oracle-fusion-field-service | required | Source of work orders and destination of the approved plan | file export / import | API write-back | API + telemetry |
| oci-object-storage | optional | Landing zone for demand forecasts |  |  |  |

## Metrics

### Planning cycle time

- **Kind:** business
- **Signed off by:** VP Field Service
- **Formula:** Time from demand freeze to approved plan
- **Baseline:** ~2 days manual
- **Figure:** ~30 min
- **Figure status:** pov_result
- **Attribution:**
  - **Named when allowed:** Proof of value
  - **Otherwise:** proof of value at a global home-appliance manufacturer
- **Caveat:** Illustrative proof-of-value result, not contractual
- **Source:** pov-report 2026-06-30

## Packages

- **Target OCI consumption:** GPU compute for the optimization run, per market

### PoV Jumpstart · S

- **Id:** pov
- **Duration:** 4–8 weeks (target 6, hard cap 10)
- **Services price:** €90K · indicative · Indicative; scope confirmed at kickoff
- **Infrastructure price per month:** €2K · indicative
- **What you get:** A plan on your data; A measured baseline; A go / no-go readout
- **In scope:** One region; One planning horizon
- **Out of scope:** Write-back integration; Custom KPIs

### Integration · M

- **Id:** integration
- **Duration:** 12–20 weeks
- **Services price:** €300K–€500K · indicative
- **What you get:** A live integrated app; Write-back to the system of record
- **In scope:** One to two API integrations
- **Out of scope:** Market-local rules

### Scaling · L

- **Id:** scaling
- **Duration:** 12–52 weeks
- **Services price:** to be defined
- **What you get:** Rollout across markets; Market-local rules and custom KPIs
- **In scope:** Many markets
- **Out of scope:** (none)

### How each capability area is handled per tier

| Area | PoV | Integration | Scaling |
|---|---|---|---|
| Allocation rules | Standard rule set on customer data | Customer rules and weights | Per-market rules, custom KPIs |

### Why it sells for the partner

- A natural Oracle Fusion Field Service cross-sell
- Net-new OCI GPU consumption on top of the SaaS seat
- Repeatable across comparable accounts

## Proof

- **Customer:** Northwind Appliances
- **Delivered:** PoC, Jun 2026, zone and technician allocation on field-service data
- **Divergence from the pack:** The pack generalizes the allocation rules; the PoC hard-coded one customer's.

## Open questions

(none)

## Settings

### Clearance

| Channel | Customer may be named |
|---|---|
| Internal | yes |
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
  - **Name:** Pack owner
  - **Email:** RnDrequest@softserveinc.com

### Provenance

- **Inputs:**
  - **Path:** fixtures/feature-list.docx
    - **Kind:** feature-list
    - **Read:** 2026-09-18
- **Research brief:** packs/workforce-optimization/research-brief.md
