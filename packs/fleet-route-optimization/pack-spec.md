---
slug: fleet-route-optimization
status: confirmed
spec_version: 1
generated_with: { roadmap_version: 2026-09-17, catalog_version: 2026-09-22 }
roadmap_item_id: fleet-route-optimization
roadmap_block: Data analysis & decision agents
---

# Fleet route optimization

- **Site:** Fleet route optimization
- **Internal slide:** Fleet route optimization App
- **External:** Fleet route optimization
- **External subheading:** Accelerator App by SoftServe
- **Note:** The name is the use-case map card Alex widened and shaded WinP on 2026-09-17 ("Delivery route planning" became "Fleet route optimization" — delivery vans, field engineers, EV fleets), so the map, the tracker and the pack share one noun. Deliberately NOT the Workforce optimization pack: that one decides which engineers cover which zones and how many are needed (work-zone allocation, a MILP on cuOpt); this one plans each van's day — the order of visits, the route and the charging stop (vehicle routing with time windows and EV charging, a different cuOpt API). The delivery team's own risk register (R9) draws the same line.
- **Source:** use-case-map-2026-09-17
- **Source of the name:** user:2026-09-28

## One-liner

- **Full:** Lower cost per visit from the van fleet you already run: more visits per engineer, fewer second visits and less paid time at chargers — every route planned around booked slots, skills and charging, and tested first on your own past days.
- **Short:** Lower cost per visit from the fleet you already run — van routes re-planned around charging.
- **Banned words checked:** yes
- **Note:** Business value first (owner feedback 2026-09-29: not enough focus on business value). Of what — the daily routes of an engineer or delivery van fleet. So what — a lower cost per visit and more visits from the same fleet. How — re-planned on GPU around booked slots, skills and charging, tested on the operator's own history first. No engine or platform words in a one-liner (Alex, 2026-09-29, via the mini-site copy review): the how-clause names the job, the tech lives on the chips and the Technology tab.
- **Source:** user:2026-09-28

## Problem and solution

### Problem

Field-service planners route hundreds of vans a day by hand; the operator pays in extra miles, idle time at chargers and second visits.

### Solution

The planner reviews each engineer's day instead of building it, after testing the plan on the company's own past days, and the operator pays for fewer miles, charger waits and second visits.

- **Problem points:**
  - **Paid time on the road:** fuel, wear and an engineer not on a job
  - **Second visits:** a missed slot costs a repeat visit and compensation
  - **Paid time at chargers:** a badly timed charge takes an engineer off the job
- **Outcome chips:** Cost per visit ↓; Visits per engineer ↑; Missed appointments ↓
- **Reframe:** See the saving on your own days
- **Reframe question:** What if you saw the saving on your own past days first?
- **Today:** Planners build the day from the scheduling system's rules and patch the rest by hand; charging an electric van is left to the engineer, and nobody can say how much of each visit's cost was avoidable.
- **Tomorrow:** Each day is planned on GPU with slots, skills, priorities and charging stops in one solve, and every electric route is checked against the battery. Operations see what it is worth — cost per visit, visits per engineer, second visits avoided — before any live schedule changes.
- **Note:** Recast around business value (owner feedback 2026-09-29): the problem names what the operator pays for, the points are cost lines, the chips are the three business metrics. Written for a seller outside the industry — a named role, the nouns on the desk.
- **Source:** user:2026-10-01

## Who buys it

Operators of engineer and delivery van fleets — especially fleets going electric.

- **Buyer roles:** Director of Field Operations; Head of Resource Planning and Scheduling; Head of Fleet; Chief Operating Officer; EV Transition Program Lead
- **Qualifying signals:**
  - Dozens to thousands of vans making several customer visits a day against booked windows
  - A scheduling system of record — Oracle Fusion Field Service or equivalent — with exportable job and engineer history
  - Engineers with different skills or jobs with different priorities, so who goes where is a real choice
  - A fleet moving to electric, where range and charging now shape the working day
  - Telematics or GPS history that shows what past days actually looked like
- **Disqualifiers:**
  - One depot, a few vans and one job type — the routing is already easy
  - No history of past days to replay — nothing to prove the plan against
  - Real-time dispatch needed from day one — the proof of value re-plans past days
  - Long-haul freight with few stops and no customer windows
- **Note:** Not the Workforce optimization pack's buyer question (how many engineers, covering which zones); this pack answers how each van's day should run.
- **Source:** user:2026-09-28

## Industries

### Telecom and pay-TV home installation

- **Site label:** Telecom & TV
- **Framing:**
  - **Problem:** Engineers installing and repairing home broadband and TV lose hours between booked slots, and a late arrival to a customer who took the day off means a second visit.
  - **Solution:** Installs and repairs are sequenced so each engineer reaches every booked slot, and each job goes to an engineer whose skills let them finish it on the first visit.
  - **Entities:** home visits, booked slots, engineer skills, vans
- **Status:** plausible
- **Note:** The source engagement's domain; nothing delivered yet, hence plausible, not proven.
- **Source:** scope-doc-v1, hlr
- **Icon:**
  - **File:** visuals/vertical-0-home-signal-ink.png
  - **Name:** home-signal
  - **Source:** Tabler Icons
  - **Licence:** MIT
  - **File, white:** visuals/vertical-0-home-signal-white.png

### Utilities and energy field service

- **Site label:** Utilities
- **Framing:**
  - **Problem:** Meter fitters and repair crews work to booked or regulated windows, and a gas or electrical job sent to an engineer without the right certificate is a wasted trip.
  - **Solution:** Jobs go to certified engineers inside their windows, with charging planned in, so crews spend the day on jobs rather than driving.
  - **Entities:** meter installs, repairs, certificates, booked windows
- **Status:** plausible
- **Source:** research-brief-2026-09-28
- **Icon:**
  - **File:** visuals/vertical-1-bolt-ink.png
  - **Name:** bolt
  - **Source:** Tabler Icons
  - **Licence:** MIT
  - **File, white:** visuals/vertical-1-bolt-white.png

### Facilities and building maintenance

- **Site label:** Facilities
- **Framing:**
  - **Problem:** Technicians covering lifts, heating and fire systems across many sites juggle planned maintenance with penalty-backed response times.
  - **Solution:** Call-outs and planned visits are routed together, weighted by each contract's response time, so urgent work lands in time and no penalty is paid.
  - **Entities:** sites, service contracts, response times, planned visits
- **Status:** plausible
- **Source:** research-brief-2026-09-28
- **Icon:**
  - **File:** visuals/vertical-2-building-ink.png
  - **Name:** building
  - **Source:** Tabler Icons
  - **Licence:** MIT
  - **File, white:** visuals/vertical-2-building-white.png

### Parcel and last-mile delivery

- **Site label:** Last-mile delivery
- **Framing:**
  - **Problem:** Drivers run electric vans against promised delivery windows; a route that misjudges range ends at a charger, and its missed drops are driven twice.
  - **Solution:** Routes are planned with the delivery windows and a battery check on every leg, so vans finish their drops and fewer roll over to tomorrow.
  - **Entities:** drops, delivery windows, vans, depots
- **Status:** plausible
- **Note:** Skills matching matters less here; windows, stop order and range carry the value.
- **Source:** use-case-map-2026-09-17, research-brief-2026-09-28
- **Icon:**
  - **File:** visuals/vertical-3-truck-delivery-ink.png
  - **Name:** truck-delivery
  - **Source:** Tabler Icons
  - **Licence:** MIT
  - **File, white:** visuals/vertical-3-truck-delivery-white.png

## Capabilities

### Data and day replay

- **Stage:** Replay the real day
- **Customization in this area:** Which days, regions and exports · Calibration tolerances per metric · Business rules and exclusions agreed with the operations experts · Live Field Service read through Oracle's accelerator

| Category | Feature | Status | From tier | Source |
|---|---|---|---|---|
| Data intake | Field Service history read from exports — jobs, windows, engineers, skills, shifts, start points | partial | pov | scope-doc-v1 |
| Data intake | Telematics, GPS traces and charging history aligned to each engineer-day | partial | pov | scope-doc-v1 |
| Data intake | Live read from Field Service over its API | partial | integration | scope-doc-v1 |
| Replay | Real operating days rebuilt engineer by engineer | partial | pov | scope-doc-v1 |
| Replay | Replay calibrated against actual visits, journey times and appointment outcomes | partial | pov | scope-doc-v1 |
| Replay | Traffic-aware travel times per departure window | partial | pov | scope-doc-v1 |

### Route planning

- **Stage:** Plan every route
- **Customization in this area:** Objective weights — what a missed appointment is worth against travel · Skills framework and priority rules · Fleet mix

| Category | Feature | Status | From tier | Note | Source |
|---|---|---|---|---|---|
| The rules of the day | Booked appointment windows kept | partial | pov |  | scope-doc-v1 |
| The rules of the day | Jobs matched to engineer skills, including multi-skill jobs | partial | pov |  | scope-doc-v1 |
| The rules of the day | Job priorities weighed against travel | partial | pov |  | scope-doc-v1 |
| The rules of the day | Electric and combustion vans planned in one run | partial | pov |  | scope-doc-v1 |
| The rules of the day | Van load capacity respected | roadmap | integration |  | review-spec-2026-09-28 |
| The solve | A region's whole day solved in one GPU run | partial | pov | About 10,000 locations per single-GPU solve; larger regions are split | scope-doc-v1 |
| The solve | Visits that cannot be served returned with the reason | partial | pov |  | scope-doc-v1 |
| The solve | Check that a dropped visit is truly infeasible, not just expensive | partial | pov |  | scope-doc-v1 |

### EV and charging

- **Stage:** Plan every route
- **Customization in this area:** Charging policy — home charging, depot rules, battery reserve · Charger sources and connector types

| Category | Feature | Status | From tier | Note | Source |
|---|---|---|---|---|---|
| Range | Battery level and range needed for the remaining work tracked per van | partial | pov |  | scope-doc-v1 |
| Range | Every electric route checked leg by leg against a battery reserve | available | pov |  | scope-doc-v1 |
| Charging | Charging stop placed by location, connector, speed and listed availability | partial | pov |  | scope-doc-v1 |
| Charging | Home-charging policy, with exceptions for engineers without a charger | partial | pov |  | scope-doc-v1 |
| Charging | A second charging stop in one shift | partial | pov | One stop inside the solve; further stops through a re-planning loop | scope-doc-v1 |
| Charging | Queueing and contention at shared chargers | roadmap | scaling |  | scope-doc-v1 |

### Comparison and decision

- **Stage:** See what it saves
- **Customization in this area:** The headline metrics and pass thresholds · Report layout for executives and planners

| Category | Feature | Status | From tier | Note | Source |
|---|---|---|---|---|---|
| Comparison | Actual, replayed and re-planned days side by side on the agreed metrics | partial | pov |  | scope-doc-v1 |
| Comparison | Route maps and drill-down to each engineer-day and visit | partial | pov |  | scope-doc-v1 |
| Comparison | Decision pack — each metric against its pass threshold, go or stop | partial | pov |  | scope-doc-v1 |
| Money | Savings in money and carbon worked out from travel and charging | roadmap | scaling | The proof of value reports the physical drivers for the client's finance team to price | scope-doc-v1 |

### Dispatch and operations

- **Stage:** Send it to dispatch
- **Customization in this area:** Dispatcher workflow in Field Service, on Oracle's cuOpt and Field Service accelerator · Write-back rules and approvals · Security and retention

| Category | Feature | Status | From tier | Source |
|---|---|---|---|---|
| Dispatch | Dispatcher asks for a re-plan and reviews it in Field Service | partial | integration | scope-doc-v1 |
| Dispatch | Approved routes and charging stops written back to Field Service | partial | integration | scope-doc-v1 |
| Dispatch | Re-plan during the day as jobs overrun or vans break down | roadmap | scaling | scope-doc-v1 |
| Running it | Every run kept with its inputs and results | available | pov | scope-doc-v1 |
| Running it | Sign-in, roles and audit trail for production use | roadmap | integration | scope-doc-v1 |

## Workflow

### Inputs

| System | Data | Tier |
|---|---|---|
| Oracle Fusion Field Service | jobs, booked windows, engineers, skills, shifts, start locations | PoV Jumpstart: historic exports. Integration: API read. |
| Fleet telematics and charging records | trips, GPS traces, battery state, charging events | PoV Jumpstart: historic files. Integration: a live feed. |
| Traffic and charger data | travel times by time of day, charger locations and connectors | PoV Jumpstart: a licensed historic dataset. Integration: live APIs. |

### 1. Pull the day's history

- **Actor:** system
- **Covers:** jobs, windows, engineers, skills, shifts, telematics, GPS, charging
- **Description:** The chosen days are loaded from the scheduling exports and the fleet's telematics and charging records, checked, and lined up into one record per engineer per day.
- **If it fails:** A day missing a source — no GPS, no link between van and engineer — is flagged and left out, never filled in by guesswork.

### 2. Replay the real day

- **Actor:** system
- **Human in the loop:** yes
- **Covers:** rebuilding each engineer-day, travel times, calibration against actuals
- **Description:** Each engineer's day is rebuilt as it really ran and checked against the actual visits, journey times and appointment outcomes; the operations experts confirm the replay is close enough to compare against.
- **If it fails:** Where a day cannot be replayed within the agreed tolerance, the gap is written down and agreed, or the day is dropped — no comparison runs on an unchecked day.

### 3. Plan every route

- **Actor:** ai
- **Covers:** booked windows, skills, priorities, electric and diesel vans, the charging stop
- **Description:** The same day is re-planned on GPU in one run, keeping every booked window, matching each job to an engineer with the right skills, weighing job priority against travel and placing each electric van's charging stop where it costs least.
- **If it fails:** A visit no engineer can serve comes back unassigned with its reason; the hard rules are never relaxed to make the plan look complete.

### 4. Check every electric route

- **Actor:** system
- **Covers:** battery reserve leg by leg, a second charging stop, home-charging policy
- **Description:** Every electric route is checked leg by leg against a battery reserve, with the home-charging policy applied; a day that needs a second stop goes back through the solve.
- **If it fails:** A route that breaks the reserve on any leg is rejected and re-planned; a day that needs a second stop goes through a re-planning loop.

### 5. See what it saves

- **Actor:** human
- **Human in the loop:** yes
- **Covers:** actual, replayed and re-planned days, route maps, the decision pack
- **Description:** Operations see the actual, replayed and re-planned days side by side on the agreed metrics, down to each engineer's route, and decide to go further, refine or stop.
- **If it fails:** Where the re-plan does not beat the replayed day on the agreed metrics, the decision pack says so — stop is a valid outcome.

### 6. Send it to dispatch

- **Actor:** human
- **Covers:** dispatcher request, review, write-back of routes and charging stops
- **Description:** A dispatcher asks for a re-plan, reviews the recommended routes and charging stops, and approves what is written back to Field Service.
- **If it fails:** In the proof of value nothing is written back; write-back is the Integration tier, and the dispatcher approves every change before it lands.
- **Human in the loop:** yes

### Outputs

| System | Data | Tier |
|---|---|---|
| Oracle Fusion Field Service | re-planned routes, charging stops, unassigned visits with reasons | PoV Jumpstart: reports and route maps, nothing written back. Integration: write-back after the dispatcher approves. Scaling: re-planned during the day. |

### Notes

- **Grouping note:** Six steps (a workflow is grouped to 5-7). The engagement's five delivery phases and thirteen work packages sit under them; the feature-level view is in capabilities, whose five areas are the same process one level down.

## Architecture

### Inputs

| System | Data |
|---|---|
| Oracle Fusion Field Service | jobs, windows, engineers, skills |
| Fleet telematics | trips, battery state, charging events |
| Traffic and charger data | travel times, charger locations |

### Stack, top to bottom

#### Custom configuration

- **Vendor:** SoftServe
- **Items:**
  - Objective weights — a missed appointment against travel
  - Skills framework and job priority rules
  - Charging policy — home charging, battery reserve
  - Reason codes for unassigned visits
- **Summary:** Objective weights, skills and priority rules, charging policy, reason codes

#### Fleet route optimization by SoftServe

- **Name:** Fleet route optimization by SoftServe
- **Vendor:** Oracle + SoftServe
- **Summary:** replay, charging stops, battery check, compare
- **Items:** Replay, calibration, travel times; Charging stops, battery check, comparison UI

#### NVIDIA cuOpt optimization engine

- **Name:** NVIDIA cuOpt optimization engine
- **Vendor:** NVIDIA
- **Catalog id:** nvidia-cuopt
- **Summary:** GPU route solve, charging stops included
- **Note:** Runs Oracle's extended cuOpt server image (charging stops inside the solve, partial solutions, sparse matrices). Sparse matrices and time-of-day travel are validated but not yet in NVIDIA's mainline; Oracle manages that change with NVIDIA.

#### Cloud infrastructure and GPUs

- **Vendor:** Oracle
- **Catalog id:** oci-gpu-instances; oci-kubernetes-engine; oci-object-storage; oracle-ai-database; oci-api-gateway; oci-vault
- **Items:** GPU instance and Kubernetes

### Outputs

| System | Detail | Data |
|---|---|---|
| Oracle Fusion Field Service | or the scheduling system in use | re-planned routes, charging stops, unassigned visits with reasons |

## Oracle products

| Id | Role | Why | At PoV | At Integration | At Scaling | Note |
|---|---|---|---|---|---|---|
| oci | required | The tenancy the pack runs in — Kubernetes for the services, Object Storage for the exports and run evidence, Oracle AI Database for the replayed days and results; each is a row on the architecture's infrastructure layer, the platform is this one entry |  |  |  |  |
| oci-gpu-instances | required | The route solve runs on an OCI GPU shape — one NVIDIA A10 shape at PoV Jumpstart, about four-fifths of the environment's monthly cost; this is the consumption line an Oracle account team sells |  |  |  | At Scaling the capacity moves to reserved GPU capacity, the form the Oracle field sells; raw GPU procurement is never proposed. |
| oracle-fusion-field-service | optional | The scheduling system the jobs come from and the re-planned routes go back to | historic exports in, nothing written back | API read and write-back after dispatcher approval | in-day re-planning triggered from dispatch | Optional by the owner's precedent on the Workforce optimization pack — a system the pack reads from or writes to is optional even when it is the go-to-market anchor. |
| oci-ai-accelerator-packs | optional | Oracle's cuOpt and Field Service accelerator — API read and write, dispatcher review, energy check — which the pack builds on rather than rebuilds |  |  |  |  |

## Metrics

- **Kpis note:** One metric set, business value first (owner feedback 2026-09-29): the money and capacity lines of the buyer's own KPI framework — cost per completed visit and cost to serve, jobs per engineer per day, missed-appointment charges — which it asks any supplier to baseline against Field Service actuals. The proof of value measures the physical drivers (driving and charging minutes, overtime, visits served) and the operator's finance team prices them at its own unit costs; the engagement computes no money itself. No figure is measured or cleared (the engagement is starting), so every figure prints "results to follow". Charging downtime and travel time per job are drivers, measured alongside and never tiled. Technical acceptance criteria stay the proof's "accepted when" line.

### Cost per completed visit

- **Kind:** business
- **Signed off by:** Chief operating officer
- **One-pager label:** cost of each completed visit: driving, paid charging time and overtime
- **Chip:** Cost per visit ↓
- **Label:** what each completed visit costs: driving, paid charging time and overtime
- **Formula:** Driving minutes, in-day charging minutes and overtime hours priced at the operator's own unit costs, over completed visits — the re-planned day against the replayed actual day
- **Baseline:** The replayed actual days, priced at the operator's own unit costs
- **Figure:** -
- **Caveat:** Re-planned past days, not live operations; priced by the operator's finance team, not by the engagement.
- **Note:** Answers all three problem points; it is the number a finance team signs. Charging downtime and travel time per job are its drivers, measured alongside.
- **Source:** kpi-framework, scope-doc-v1

### Visits per engineer per day

- **Kind:** business
- **Signed off by:** Director of field operations
- **One-pager label:** visits each engineer completes in a day: capacity without new hires
- **Chip:** Visits per engineer ↑
- **Label:** visits each engineer completes in a working day — more work from the same fleet
- **Formula:** Completed visits over engineer-days worked — the re-planned day against the replayed actual day
- **Baseline:** The actual days from Field Service, replayed and calibrated in the proof of value
- **Figure:** -
- **Caveat:** Re-planned past days, not live operations. Demand is fixed on a replayed day, so the gain comes from visits that were missed or late.
- **Note:** The capacity line: more booked work taken on without hiring engineers or adding vans.
- **Source:** kpi-framework, scope-doc-v1

### Missed appointments

- **Kind:** business
- **Signed off by:** Head of customer service
- **One-pager label:** missed or late appointments, each a second visit
- **Chip:** Missed appointments ↓
- **Label:** booked appointments missed or reached late — each a second visit, often a payment
- **Formula:** Missed plus late appointments over booked appointments, per day; priced at the operator's own cost of a repeat visit and compensation
- **Baseline:** The replayed days, calibrated to Fusion Field Service actuals
- **Figure:** -
- **Caveat:** Re-planned past days, not live operations; one region, a few days.
- **Note:** Answers the second problem point; the buyer's framework tracks missed-appointment charges as a cost line.
- **Source:** kpi-framework, scope-doc-v1

## Packages

- **Anchor line:** Runs on OCI — every route solve is GPU consumption an Oracle account team can sell; Oracle Fusion Field Service is the natural system of record.
- **Tier vocabulary note:** PoV Jumpstart / Integration / Scaling per decisions-2026-09-18. S/M/L survive only as internal size tags.
- **Legend:** ◐ partial · ● included · ●● advanced / multi-source · — not included
- **Value for Oracle and NVIDIA:** GPU route solves run inside {customer}'s own OCI tenancy, beside its Fusion Field Service data, and a measured result opens the write-back conversation for its whole engineer fleet.
- **Value for the client:** {Customer} sees what a GPU-planned day is worth before any live schedule changes: cost per visit, visits per engineer and second visits avoided, measured against its own Fusion Field Service actuals.
- **Target OCI consumption:** About €3.4K a month for the PoV Jumpstart environment — indicative, at OCI list price, most of it one NVIDIA A10 GPU shape; production sized after the proof
- **Source:** scope-doc-v1, decisions-2026-09-18

### PoV Jumpstart · S

- **Id:** pov
- **Scope:** One region, a handful of real days, files in and out: prove the re-plan beats the real day.
- **Duration:** 6–8 weeks (target 8, hard cap 10)
- **Duration note:** Deliberately narrower than the source engagement, which takes 14 weeks for one region and a few days with two UAT rounds. Dropping the UAT rounds leaves about 12; reaching 8 needs cuts still to confirm with the delivery lead — one replay-and-calibration cycle on one set of days, reports instead of a built comparison UI, the accelerator's solver checks reused. The 14-week shape is the full-scope proof and sits a tier above.
- **Services price:** to be defined · To be set from the engagement's scope, narrowed to 8 weeks.
- **Infrastructure price per month:** €3.4K · indicative · OCI list price for the proof-of-value environment; the A10 GPU is about 80%.
- **What you get:**
  - Your own past days replayed from Field Service and telematics exports, calibrated against what actually happened
  - The same days re-planned on GPU with your windows, skills, priorities and charging stops
  - Actual, replayed and re-planned days side by side, down to each engineer's route
  - A decision pack: the agreed metrics against their thresholds, and a costed next step
- **Entry gate:**
  - Field Service exports for the chosen days — jobs, engineers, skills, shifts, start locations
  - Telematics and charging history for the same days, and which van each engineer drove
  - Operations experts for the replay workshops and the calibration review
  - A named operations owner who signs off the metrics and pass thresholds in week one
- **In scope:**
  - Replay and calibration of the chosen days
  - Traffic-aware travel times from a historic dataset
  - Route planning with booked windows, skills and priorities
  - One charging stop per shift inside the solve, with the battery check on every electric route
  - Unassigned visits with their reasons
  - Side-by-side comparison, route maps and the decision pack
- **Out of scope:**
  - Live Field Service integration and write-back
  - Re-planning during the day as disruptions happen
  - Savings in money and carbon — the physical drivers are reported for finance to price
  - Queueing at shared chargers
  - Production security — sign-in, roles, audit
  - More than one region

### Integration · M

- **Id:** integration
- **Scope:** Wired into dispatch: Field Service in, recommended routes back for the dispatcher to approve.
- **Duration:** to be defined
- **Services price:** to be defined
- **Infrastructure price per month:** to be defined
- **In scope:**
  - Live read from Field Service over its API
  - Dispatcher request and review of the recommended routes
  - Write-back of approved routes and charging stops
  - Live traffic and charger data
  - More than one charging stop per shift
  - Sign-in, roles and audit trail for production use
- **Out of scope:** Re-planning during the day; Queueing at shared chargers; Savings in money and carbon; More than one region

### Scaling · L

- **Id:** scaling
- **Scope:** Every region, every day: re-planning as the day unfolds, and the savings in money.
- **Duration:** to be defined
- **Services price:** to be defined
- **Infrastructure price per month:** to be defined
- **In scope:**
  - Re-planning during the day as jobs overrun or vans break down
  - Every region, on reserved GPU capacity
  - Savings in money and carbon worked out from the drivers
  - Queueing and contention at shared chargers
- **Out of scope:** Fleet purchase and charger installation decisions; Workforce sizing and zone allocation — the Workforce optimization pack

### How each capability area is handled per tier

| Area | Feature areas | PoV | Integration | Scaling |
|---|---|---|---|---|
| Data and replay | Data and day replay | ◐ Historic exports for a few days in one region; calibrated replay | ● Live read from Field Service; live traffic | ●● Every region, every day |
| Route planning | Route planning | ● Windows, skills, priorities, mixed fleet; unassigned visits with reasons | ● Re-plans on the dispatcher's request | ●● Re-planning during the day on disruption |
| EV and charging | EV and charging | ◐ One charging stop per shift; battery check on every route | ● Several stops per shift; live charger data | ●● Queueing at shared chargers |
| Comparison and decision | Comparison and decision | ● Actual, replayed and re-planned side by side; decision pack | ● The same metrics tracked on live days | ●● Savings in money and carbon |
| Dispatch and operations | Dispatch and operations | — Reports only; nothing written back | ● Dispatcher review, write-back to Field Service; sign-in, roles, audit | ●● Per-region dispatch rules and run telemetry |

### Why it sells for the partner

- Net-new GPU consumption: solves grow with a fleet's engineers and days, not seats
- Starts from Oracle's accelerator: each deal builds on Oracle's cuOpt and Field Service integration
- An electric-fleet story: range, charging downtime and cost to serve are what fleet boards already ask about

## Proof

- **Customer:** Sky
- **Context:** At {customer}, home-service engineers work from Oracle Fusion Field Service schedules while the van fleet moves to electric, and nobody can say how much travel, missed appointments and charging time a better plan would remove.
- **Delivered:** {Customer}'s real operating days are rebuilt engineer by engineer from Fusion Field Service, telematics and charging records, and checked against what actually happened. The same days are then re-planned on NVIDIA cuOpt around appointment windows, skills, priorities and charging stops, and operations compare the two side by side.
- **Divergence from the pack:** The engagement is one operator, one region, historic days only and file-based, with one in-solver charging stop per shift and no write-back; it runs 14 weeks with two UAT rounds. The pack generalizes the objective weights, skills rules and charging policy as per-client configuration, cuts the proof of value to 6-8 weeks, and carries the Field Service write-back (Oracle's existing accelerator) and in-day re-planning as the Integration and Scaling tiers.
- **Divergence line:** Not one operator's set-up: objective weights, skills rules and charging policy are configured per client; every client gets its own past days replayed and re-planned on GPU, compared on the numbers it already tracks.
- **Source:** scope-doc-v1, kpi-framework, oracle-pipeline-2026-09-16
- **Proof headline:** A 14-week proof of concept starting at {customer} — results to follow
- **Vertical case:** Vertical case: the field engineers of {customer}
- **Proof story:** At {customer}, engineers work from Fusion Field Service schedules while the van fleet goes electric. Their real days are replayed, re-planned on NVIDIA cuOpt with windows, skills and charging stops, and compared side by side.

## Next steps

1. Set the PoV Jumpstart price and confirm the three metrics with the delivery lead; both are open.
2. Run the Sky proof of concept and measure the three metrics against Field Service actuals.
3. Publish the app on the Oracle AI & Data Solutions site; brief SoftServe's Oracle alliance team.

## Open questions

### pov_price

- **Question:** What is the PoV Jumpstart services price?
- **Why:** The source scope document leaves its delivery cost as a placeholder, so there is no signed figure to derive from. Every artifact prints a footnote until it is set.
- **Blocks:** packages; one_pager; deck; listing

### clearance

- **Question:** May the customer be named on partner print or the mini-site?
- **Why:** Oracle already cites the account publicly, but SoftServe holds no written clearance; the name is internal-only until one arrives. The proof prints the anonymized descriptor.
- **Blocks:** deck; one_pager; listing

### results

- **Question:** When do the first measured figures arrive?
- **Why:** Delivery is only starting; every metric tile prints "results to follow" until the proof of concept measures them against Field Service actuals.
- **Blocks:** kpis; deck; one_pager

### reuse_rights

- **Question:** May what is built in the engagement be reused across clients?
- **Why:** No document in the source set states who owns the replay engine, the comparison UI and the charging logic. The pack assumes reuse.
- **Blocks:** capabilities; packages

### cuopt_mainline

- **Question:** When do sparse matrices and time-of-day travel reach NVIDIA's mainline cuOpt?
- **Why:** The pack depends on Oracle's extended cuOpt image; production at scale depends on the merge Oracle manages with NVIDIA.
- **Blocks:** architecture

### wfo_positioning

- **Question:** How is this pack shown beside Workforce optimization on the site and in the section deck?
- **Why:** Both are cuOpt and Field Service packs for field engineers; the use-case map separates them (zone allocation against daily van routing). Sellers need one line that tells them apart.
- **Blocks:** listing; deck

### scale_limit

- **Question:** What is the answer for regions larger than one GPU solve?
- **Why:** One A10 solve holds about 10,000 locations; larger regions need splitting or a larger GPU, untested so far.
- **Blocks:** capabilities; packages

### agent_picks

- **Question:** Do the name, one-liner, problem, buyer, metrics and PoV shape stand?
- **Why:** The owner delegated every pick for this run ("without asking me anything"); each was taken from the use-case map, the scope document and the buyer's KPI framework and is logged in decisions.md for review. Metrics and messaging recast around business value on 2026-09-29 (owner feedback).
- **Blocks:** meta; one_liner; problem_solution; icp; kpis; packages; verticals

### pov_duration

- **Question:** Can the proof of value really run in 8 weeks?
- **Why:** The source engagement takes 14 weeks for one region and a few days. The cuts that reach 8 (one calibration cycle, reports instead of a built UI, reused solver checks) are proposed, not confirmed by the delivery lead.
- **Blocks:** packages; deck; one_pager

### accelerator_licence

- **Question:** Is Oracle's cuOpt and Field Service accelerator licensed for use beyond a proof of concept?
- **Why:** The scope document says Oracle provides and licenses it for PoC use. The pack's Integration tier (API read, dispatcher review, write-back) rests on it, so those rows are partial until this is answered.
- **Blocks:** capabilities; packages; oracle_products

## Settings

### Clearance

| Channel | Customer may be named |
|---|---|
| Internal | yes |
| Partner print | no |
| Customer site | no |
| Demo | no |

- **Anonymized descriptor:** a large home-services operator
- **Descriptor warning:** A descriptor combining TV or broadband installation with one country back-solves to one company. External artifacts rest on the domain and name no source engagement detail beyond this descriptor.
- **Internal-only facts:** the customer name outside internal material; the prior validation work by another supplier and its figures; the engagement's commercial terms; team member names
- **Approvals:** (none)
- **Source:** agent-pick:2026-09-28 (owner delegated every pick); 1:1 2026-09-18 (strip client names from anything public)

### Contacts

- **Partner print:**
  - **Name:** Karsten Tramborg
  - **Title:** Oracle Partnership Director
  - **Email:** ktram@softserveinc.com
- **Site:**
  - **Mailbox:** oracle@softserveinc.com
  - **Named:** Karsten Tramborg
- **Internal:**
  - **Name:** Oleksii Orlov
  - **Email:** RnDrequest@softserveinc.com
- **Source:** decisions-2026-09-18

### Deck

- **Running header:** Oracle AI & Data Solutions
- **Seller lead:** What this pack does for an Oracle account team's number.
- **Cta:** Ready to replay one region's real days?
- **Layers subtitle:** How the fleet-route accelerator is layered — from the infrastructure up to the tailored service.
- **Architecture subtitle:** Reference architecture: Field Service and telematics in, re-planned routes out.
- **Source:** agent-pick:2026-09-28 (owner delegated every pick)

### One-pager

- **Eyebrow:** Oracle AI & Data Solutions
- **Reframe:** See the saving on your own days
- **Sub:** short
- **Data-flow notes:** yes
- **Tier scope:**
  - **Scaling:** Every region, re-planned during the day, savings in money.
- **Cta:**
  - **Question:** Ready to replay one region's real days?
- **Source:** user:2026-10-01

### Executive summary

- **Running header:** Oracle AI & Data Solutions
- **Source:** agent-pick:2026-09-28 (owner delegated every pick)

### Provenance

- **Inputs:**
  - **Id:** scope-doc-v1
    - **Path:** \<practice-drive>/Projects/Oracle/Customers/\<account>/…/Outputs from SoftServe/UC Scope … EV Fleet Route Optimization with cuOpt v1.docx
    - **Kind:** sow
    - **Read:** 2026-09-28
  - **Id:** kpi-framework
    - **Path:** \<practice-drive>/Projects/Oracle/Customers/\<account>/…/Inputs from \<account>/… Performance KPI Framework.pdf
    - **Kind:** requirements
    - **Read:** 2026-09-28
  - **Id:** hlr
    - **Path:** \<practice-drive>/Projects/Oracle/Customers/\<account>/…/… High Level Requirements.docx
    - **Kind:** requirements
    - **Read:** 2026-09-28
  - **Id:** use-case-map-2026-09-17
    - **Path:** \<practice-drive>/Projects/Oracle/Packs/Use case maps/ (the Fleet route optimization card)
    - **Kind:** map
    - **Read:** 2026-09-28
  - **Id:** oracle-pipeline-2026-09-16
    - **Path:** AO-Personal-OS context/areas/softserve/oracle-pipeline.md (Neil + Gero sync, 2026-09-16)
    - **Kind:** wiki
    - **Read:** 2026-09-28
  - **Id:** research-brief-2026-09-28
    - **Path:** research-brief.md (compact, from the inputs; no research fan-out in this run)
    - **Kind:** research
    - **Read:** 2026-09-28

## Other fields

```yaml
workflow.integration_by_tier:
  pov: file exports in, reports and route maps out
  integration: API read and write-back to Field Service, after dispatcher approval
  scaling: in-day re-planning across every region
```
