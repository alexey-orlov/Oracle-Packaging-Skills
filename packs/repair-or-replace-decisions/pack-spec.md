---
slug: repair-or-replace-decisions
status: confirmed
spec_version: 1
generated_with: { roadmap_version: 2026-09-17, catalog_version: 2026-09-22 }
roadmap_item_id: visual-inspection-and-classification
roadmap_block: Per-item processing pipelines
---

# Repair-or-replace decisions

- **Site:** Repair-or-replace decisions
- **Internal slide:** Repair-or-replace decisions App
- **External:** Repair-or-replace decisions
- **External subheading:** Accelerator App by SoftServe
- **Source of the name:** user:2026-09-22
- **Roadmap note:** Closest existing item, already marked in progress. The pack extends past it: "visual inspection and classification" does not cover the rule layer, the measurement, or the decision record, which are the pack's differentiators. Flagged for the roadmap owner as a possible new item.

## One-liner

- **Full:** A replacement paid for only when the rules require one, and the right job booked first time: repair-or-replace calls on damaged vehicles, containers and equipment, measured from photos.
- **Short:** A replacement paid for only when the rules require one, and the right job booked first time.
- **Banned words checked:** yes
- **Source:** user:2026-09-29

## Problem and solution

### Problem

Call agents, surveyors and claims handlers decide repair or replace from photos of damaged vehicles, containers and equipment, and each wrong call costs a needless replacement or a repeat visit.

### Solution

The agent, surveyor or handler confirms or overrules a measured call before the job is booked, with its rule and any recalibration listed. Replacements are funded only when the rules require them, and the job is done once.

- **Sub-problems:**
  - **Needless replacements:** a full replacement is paid for when a repair would have met the rules.
  - **Repeat visits:** a repair that should have been a replacement fails and comes back.
  - **Follow-on work found late:** work a replacement triggers, such as camera recalibration, surfaces after booking and adds days.
- **Reframe:** Check the call, don't make it
- **Outcomes:** Needless replacements ↓; Repeat visits ↓; Avoidable recalibrations ↓
- **Source:** user:2026-09-29

## Who buys it

Operators who decide repair or replace, and the insurers and lessors who pay.

- **Dual-buyer rule:** CONFIRMED DECISION (user:2026-09-22): the pack addresses BOTH buyers, and every artifact must carry both. Concretely — the deck and one-pager name both in the audience line and give each its own value row; the listing's problem-and-solution strip reads for both; each industry names which buyer leads there; the metrics say whose number each one is; and the packages say what each buyer gets. No artifact may silently address only one.
- **Buyer roles:** Director of Operations; Network Operations Director; Head of Technical Standards; Head of Claims; Claims Operations Director; Fleet or Lease Portfolio Manager
- **Buyer roles, operator:** Director of Operations; Network Operations Director; Head of Technical Standards
- **Buyer roles, payer:** Head of Claims; Claims Operations Director; Fleet or Lease Portfolio Manager
- **Buyer by industry:**
  - **Vehicle glazing:** operator leads; the payer applies the repair-first pressure
  - **Shipping containers:** operator leads (the depot), with the lessor approving line by line
  - **Rental and lease handover:** payer leads (the lessor), because the output is a charge
  - **Vehicle body and paint at first notice of loss:** payer leads (the insurer)
  - **Aircraft skin:** operator leads (the airline or maintenance organisation)
- **Qualifying signals:**
  - operates across markets or contracts whose repair limits differ
  - already reports a repair-versus-replace rate, or is asked to by a payer
  - can count disputes, supplements or repeat visits
  - customer- or technician-captured media already arrives, or a capture channel exists
  - a booking, dispatch or claims system exists to write a resolved scope into
- **Disqualifiers:**
  - single site with one rule set
  - the decision is made by a technician already physically at the asset
  - assets with no identifier that resolves to known geometry
  - the deciding variable is not visible in ordinary photography
- **Why both:** The value of replacing less accrues to the payer, while the operator earns on replacements and carries no software budget line for this today. Addressing only the operator asks them to fund a saving someone else banks; addressing only the payer leaves the decision with the party that does not make it. The pack is sold to the pair.
- **Source:** user:2026-09-22

## Industries

### Vehicle glazing

- **Framing:**
  - **Problem:** Call agents book a repair or a replacement before anyone sees the vehicle.
  - **Solution:** The agent confirms a measured call and books the right job, kit and slot.
- **How the entities differ:** one safety-critical panel whose function is the driver's sight-line
- **What matters here:** Operator-led. Size limits differ by country, and a replacement can mean recalibrating the car's cameras.
- **Worked example:** A chip in the driver's viewing area: repairable in the US under 25 mm, prohibited outright in Germany.
- **Status:** plausible

### Shipping containers

- **Framing:**
  - **Problem:** Depot surveyors propose repairs the owner approves line by line.
  - **Solution:** The surveyor submits coded damage with only the permissible remedies attached.
- **How the entities differ:** a steel unit with published standard geometry and its identifier beside the defect
- **What matters here:** Operator-led. The allowed repair for each kind of damage is already codified, so each call can be checked line by line.
- **Worked example:** A hole in a panel cannot be straightened — only patched or replaced.
- **Status:** plausible

### Rental and lease handover

- **Framing:**
  - **Problem:** Branch staff decide what a returning customer is charged for damage.
  - **Solution:** New damage is separated from pre-existing, with the evidence attached to the charge.
- **How the entities differ:** a whole unit compared against a prior condition record
- **What matters here:** Payer-led. The result is a charge to the customer, so the evidence has to stand up to a dispute.
- **Worked example:** A scratch within the fair-wear allowance on return versus one added during the hire.
- **Status:** plausible

### Vehicle body and paint at first notice of loss

- **Framing:**
  - **Problem:** Claims handlers decide repair, replace or write-off from photos of the damage.
  - **Solution:** The handler reviews a costed scope with the write-off threshold already applied.
- **How the entities differ:** a set of panels priced against a parts list and published labour times
- **What matters here:** Payer-led. The limit is economic: repair until it costs more than replacing.
- **Worked example:** Repair cost against a share of the vehicle's value, where the share is set locally.
- **Status:** plausible

### Aircraft skin

- **Framing:**
  - **Problem:** Engineers disposition surface damage against published structural limits.
  - **Solution:** The engineer gets the limit, the measurement and the record in one place.
- **How the entities differ:** a structural panel with a permanent, mandatory damage history
- **What matters here:** Operator-led. Some damage is accepted and recorded, within published limits, rather than repaired.
- **Worked example:** A dent inside allowable limits, logged to the aircraft's damage chart rather than repaired.
- **Status:** plausible

### Held out

- **Note:** Passed on reasoning but not on evidence; the research ran out of search budget before they could be checked. They are deliberately NOT in the pack and must not appear in any artifact until verified. Lifting and rigging gear is the one to check first — it may outrank rental handover.
- **Candidates:** lifting and rigging gear; micromobility fleets; agricultural and construction machinery

### Rejected

| Name | Reason |
|---|---|
| Property and roof claims | The decision is a sampled hit count over an area, plus reconstructing a structure with no parts list. |
| Industrial equipment condition | Severity is a rate of change across inspections, with no external rule to cite and no scale anchor. |
| Phone and laptop grading | No dimensional threshold exists on either side, and the volume version runs on a fixed rig. |
| Utility poles | The deciding variable is internal decay, invisible in any photograph. |

## Capabilities

### Capture & intake

- **Stage:** Capture
- **Customization in this area:** The capture channel, its branding and languages, and the prompts per asset class

| Category | Feature | Status | From tier | Customization | Source |
|---|---|---|---|---|---|
| Guided capture | Capture request from a booking or claim | partial | pov | The reference shape per operator | sow: the upload entry point |
| Guided capture | Guidance on framing, distance and glare | roadmap | pov | Prompts per asset class | research: what the vendors already ship |
| Guided capture | Scale anchor so size can be measured | roadmap | pov | Which anchor a customer can supply | research: the technical screen |
| Guided capture | Both sides captured where the standard requires | roadmap | pov | Per governing standard | research: the US repairability standard, clause 8.1 |
| Quality and integrity gate | Usability check with a reasoned retake | roadmap | pov | Thresholds per asset class | research: what the vendors already ship |
| Quality and integrity gate | Tamper and reuse detection on submitted media | roadmap | pov | Per channel and case history | research: a regulator names fabricated damage images as a fraud route |

### Damage assessment

- **Stage:** Read the damage
- **Customization in this area:** The damage taxonomy and the measured features per asset class and market

| Category | Feature | Status | From tier | Customization | Source |
|---|---|---|---|---|---|
| Asset identification | Identifier read from the media itself | available | pov | Identifier formats per asset class | sow: the identifier detection block |
| Asset identification | Asset record and geometry retrieval | partial | integration | The customer's record system | research: the customer's stated primary source |
| Detection and classification | Damage located and tracked across frames | available | pov | None | research: shipped by the vendor platform |
| Detection and classification | Damage classified against a configurable taxonomy | partial | pov | The taxonomy per asset class | sow: two classes scoped, six required |
| Measurement | Each damage measured, with the basis stated | roadmap | pov | One or two measured features, per market | research: no vendor publishes a measurement claim |
| Measurement | Position mapped to the governing zone | roadmap | pov | Zone geometry per market | research: four different zone constructions |
| Measurement | Post-repair residual predicted where rules require | roadmap | integration | Per market | research: German and Austrian trade bodies judge the residual |
| Measurement | New damage separated from earlier repairs | roadmap | integration | The prior record source | research: sold next door as incremental damage tracking |

### Decision & estimate

- **Stage:** The call
- **Customization in this area:** The rule set per market and contract, and the error trade-off per operator

| Category | Feature | Status | From tier | Customization | Source |
|---|---|---|---|---|---|
| The decision | Repair, replace or refer, with confidence | available | pov | The outcome set per asset class | sow: the recommendation output |
| The decision | Rule, frame and measurement cited on each call | partial | pov | None | sow: cited guidance scoped; the measured value is absent |
| The decision | Tunable threshold between the two kinds of error | partial | pov | Per operator's cost asymmetry | response: a probability-weighted score |
| The decision | Deciding rule type configurable per industry | roadmap | integration | Per industry | research: the rule changes kind across industries |
| Consequence and cost | Follow-on work and safety flags at decision | roadmap | pov | Per asset class | research: no competitor flags it |
| Consequence and cost | Scope priced from a parts and labour source | roadmap | scaling | The source per market | research: the catalogue owners |
| Consequence and cost | Write-off test against a configurable ceiling | roadmap | scaling | The ceiling per jurisdiction | research: absent in glazing, core in three industries |

### Assurance & audit

- **Stage:** Review and hand off
- **Customization in this area:** Reviewer roles, routing thresholds, response times and retention periods

| Category | Feature | Status | From tier | Customization | Source |
|---|---|---|---|---|---|
| Review | Cases routed on confidence, policy and integrity | partial | pov | Routing policy per operator | sow: routing asserted, thresholds unspecified |
| Review | Reviewer workspace with media, reading and rule | partial | pov | Roles and layout | sow: one verification stage named, no design |
| Review | Override with a captured reason | partial | pov | Reason codes per operator | research: no competitor persists the override |
| Review | Override rate tracked in aggregate only | roadmap | pov | None; never per individual reviewer | research: the oversight test four regulators converge on |
| Record and checks | Decision record kept per market retention rules | partial | pov | Export format and retention periods | sow: evidence export |
| Record and checks | Output checked automatically before review | roadmap | integration | Check set per asset class | research: one vendor ships this as its own module |

### Operations & administration

- **Stage:** Review and hand off
- **Customization in this area:** Who authors the rules, across how many markets, and the downstream systems

| Category | Feature | Status | From tier | Customization | Source |
|---|---|---|---|---|---|
| Rules | Rules authored, versioned and deployed per market | roadmap | integration | By SoftServe at proof of value, by the customer later | research: no competitor in this job has it |
| Rules | Rule changes replayed on past cases first | roadmap | scaling | The case history | research: the vendor gap list |
| Handoff and running | Decision handed on with scope resolved | partial | pov | The downstream system | research: the highest-value step the first draft dropped |
| Handoff and running | Write-back to the system of record | partial | integration | Per system | sow: an API exposed for later integration |
| Handoff and running | Accuracy evaluated on an agreed holdout set | partial | pov | The holdout set per customer | response: holdout and shadow comparison committed |
| Handoff and running | Corrections fed back into training | roadmap | integration | Retraining cadence | research: the customer's own requirement |

## Workflow

### Inputs

| System | Data |
|---|---|
| Capture channel | customer or technician media |
| Asset record | identifier, geometry, attributes, prior condition |

### 1. Capture

- **Actor:** human
- **Human in the loop:** no
- **Description:** The capture request reaches whoever holds the asset; media comes back, is checked for usability and for tampering, and a retake is requested when it is not good enough.
- **If it fails:** No scale anchor in the media: no measured decision is possible, so the case is routed to a person

### 2. Read the damage

- **Actor:** ai
- **Human in the loop:** no
- **Description:** The asset is identified from its own markings, each damage instance is located, separated from damage that was already there, classified, and measured against the limit that governs it.
- **If it fails:** Unmeasurable or unclassifiable: routed to a person with the reason stated, never closed silently

### 3. The call

- **Actor:** ai
- **Human in the loop:** no
- **Description:** Repair, replace or refer, with the rule it came from, the measurement it used and a confidence attached — plus any dependent work a replacement triggers.
- **If it fails:** No rule covers the case: routed to a person, never guessed

### 4. Cost it

- **Actor:** ai
- **Human in the loop:** no
- **Description:** Where the industry decides on money rather than on a safety limit, the scope is priced and tested against the local write-off ceiling. Absent in vehicle glazing, which has no economic test at all.
- **If it fails:** Not covered today: no parts and labour source is wired in, so the step is skipped and stated as out of scope

### 5. Confirm or overrule

- **Actor:** human
- **Human in the loop:** yes
- **Description:** The inspector sees the media, the measurement and the cited rule beside the recommended call, and confirms it or overrules it with a reason. The override is kept.
- **If it fails:** Nothing reaches the booking system until a person confirms it; unreviewed cases wait in a visible queue

### 6. Authorised handoff

- **Actor:** system
- **Human in the loop:** no
- **Description:** The confirmed decision is authorised and handed to the booking, dispatch or claims system with its scope resolved — part, skill, slot, dependent work — and the record is retained.
- **If it fails:** Downstream unavailable: the decision is held and re-sent, never dropped

### Outputs

| System | Data |
|---|---|
| the booking, dispatch or claims system | the confirmed decision and its resolved scope |

### Notes

- **Domain steps note:** The twelve-step domain workflow the industries actually share is in the research summary, section "The steps every industry shares". These six are the buyer's checkpoints over it.
- **Not ours:**
  - **Checking whether the customer is covered:** Universal in the domain, but owning it makes this a claims product. Assumed resolved upstream.
- **Integration by tier:**
  - **PoV:** file export and import, plus an exposed API
  - **Integration:** API write-back into the system of record
  - **Scaling:** API, telemetry and multi-market administration

## Architecture

### Inputs

| System | Data |
|---|---|
| Capture channel | customer or technician media |
| Asset record | identifier, geometry, prior condition |

### Stack, top to bottom

| Layer | Vendor | Items | Catalog id |
|---|---|---|---|
| Custom configuration | SoftServe | the rule set per market and contract; the damage taxonomy per asset class; reviewer roles and thresholds |  |
| Accelerator business app | Oracle + SoftServe | guided capture; review; rules; decision record |  |
| Vision and reasoning engine | NVIDIA | VSS and AI-Q | nvidia-ai-enterprise |
| Data platform | Oracle | media; audit; rules | oci-object-storage; oracle-autonomous-ai-database |
| Infrastructure | Oracle | GPU compute; Kubernetes; API gateway; identity; observability | oci-gpu-instances; oci-kubernetes-engine; oci-api-gateway; oci-iam; oci-observability-management |

### Outputs

| System | Data |
|---|---|
| the booking, dispatch or claims system | the confirmed decision and its resolved scope |

### Notes

- **Platform overlap note:** Oracle already ships video search and summarization as a one-click accelerator pack with a front-end, infrastructure-as-code and an evaluation harness. Standing up that platform is not the pack. What it leaves open is measurement from a single uncalibrated camera, the rule layer and its versioning, a record that cites rule, frame and measured value, a persisted override, and the dispatchable consequence.

## Oracle products

| Id | Role | Why | At PoV | At Integration | At Scaling |
|---|---|---|---|---|---|
| oci | required | The tenancy the pack runs in — GPU compute, Kubernetes, object storage, database, API gateway, identity and observability. |  |  |  |
| oracle-autonomous-ai-database | required | Holds the decision record, the audit trail and the versioned rule sets. |  |  |  |
| oracle-integration | optional | Binds the resolved decision into the operator's booking, dispatch or claims system. | file export / import | API write-back | API plus telemetry |
| oci-vision | optional | An Oracle-native route for image detection and classification where the customer prefers it to the NVIDIA stack. |  |  |  |
| oracle-analytics-cloud | optional | Reporting on decision mix, override rate and repeat visits. |  |  |  |
| oci-ai-accelerator-packs | optional | The one-click video platform the pack builds on top of, rather than reimplements. |  |  |  |

## Metrics

- **Kpis note:** CONFIRMED DECISION (user:2026-09-22), carried: the business case stays modelled and per unit, never an absolute annual total; a total computed from the source account's volumes would identify it even with the name removed. Revised 2026-09-29 on the owner's direction to lead with business value: the set states the value of one correct decision first, from published industry figures (the price gap between a replacement and a repair; the cost and delay of a camera recalibration), and keeps one modelled rate per 1,000 cases that counts both error directions, so the improvement reads as a gain and can never be read as "repair more". No figure is measured: no result exists because the engagement had not started; the per-decision figures are industry averages and the rate is modelled from industry assumptions, each labelled with one status word. A seller applies the per-decision values to the prospect's own volumes; when the proof of value produces measured figures they replace these and the status changes. The two technical criteria stay technical and never print on sales material.

### Saving per needless replacement avoided

- **Kind:** business
- **Signed off by:** Head of Claims
- **Chip:** Needless replacements ↓
- **Chip label:** Saved per correct call
- **Label:** saved when a correct call turns a needless replacement into a repair
- **Direction:** up
- **Formula:** The replacement not made, less the repair made instead, for each call corrected from replace to repair where the repair meets the governing limit; it is what moves replacement spend per claim
- **Baseline:** a windscreen replacement about £500 against a £40 repair, UK industry averages
- **Figure:** about £460
- **Figure status:** modeled
- **Show baseline:** no
- **Unit cost:** -
- **Whose metric:** the payer banks it; the operator is measured on the repair rate behind it
- **Attribution:**
  - **Named when allowed:** -
  - **Otherwise:** industry averages for vehicle glazing
- **Caveat:** UK industry averages for vehicle glazing, published 2013 (about $250 in the US); not the prospect's own prices.
- **Note:** UK: a typical replacement screen about £500 against an average repair of £40 (Glass Assist UK, Fleet News, 2013; tier 3, dated). US: an average replacement about $350 against an average crack repair of $99 (NWRD, undated; tier 2). The camera recalibration a replacement can trigger is counted separately under Avoidable recalibrations, never added here. The source engagement's own context-only assumption (repair £100, replacement £300) would give £200; it was not used by that model and is not used here.
- **Source:** research: P3 §2.1 corroboration lines and §4.5 synthesis point 1

### Avoidable recalibrations

- **Kind:** business
- **Signed off by:** Network Operations Director
- **Chip:** Avoidable recalibrations ↓
- **Chip label:** Avoidable recalibrations
- **Label:** for each camera recalibration a needless replacement would have triggered
- **Direction:** down
- **Formula:** Camera recalibrations booked only because a replacement was chosen where a repair would have met the limit, over all recalibrations booked; each counted with its cost and the days it adds
- **Baseline:** about 42 in 100 windscreen replacements also need a camera recalibration, modelled
- **Figure:** $300–400 and 4 days
- **Figure status:** modeled
- **Show baseline:** no
- **Unit cost:** $300–400 and about four days per recalibration, industry figures; the source model valued the operator's slot at about £50, modelled
- **Whose metric:** both: the operator loses the slot and the customer waits; the payer pays the line
- **Attribution:**
  - **Named when allowed:** -
  - **Otherwise:** industry figures from collision repair estimates
- **Caveat:** Industry figures from collision repair estimates, not glass-specific: $300–400 per calibration, and about four more days where a calibration is found after the first estimate; incidence depends on the vehicle mix.
- **Note:** Over half of calibrations surface only after the first estimate (48.5% on initial estimates, 51.5% on supplements); repairs with calibrations run about 17 days keys-to-keys against 13 without (CCC Crash Course Q4 2025, trade press, tier 3). $300–400 per calibration (Opus IVS via AutoBolt report, trade press 2023, tier 3). The 42% incidence is the source model's assumption. Listing the recalibration at decision time is a roadmap feature; at the proof of value the lever is the needless replacements avoided.
- **Source:** research: P3 §2.3 ADAS lines and §4.5 point 4; the value model's recalibration assumption

### Wrong calls per 1,000 cases

- **Kind:** business
- **Signed off by:** Director of Operations
- **Chip:** Repeat visits ↓
- **Chip label:** Repeat visits
- **Label:** cases booked as the wrong job: needless replacements and failed repairs together
- **Direction:** down
- **Formula:** Cases booked as a repair that needed a replacement, or as a replacement a repair would have met, per 1,000 cases decided, over the same window before and after
- **Baseline:** 45 per 1,000
- **Figure:** 36 per 1,000
- **Figure status:** modeled
- **Show baseline:** yes
- **Unit cost:** a needless replacement: about £460 of glass plus any recalibration; a failed repair: the return visit, about £75 of rebooking friction, modelled
- **Whose metric:** the operator owns the booking; the payer counts the rebooks and the days
- **Attribution:**
  - **Named when allowed:** -
  - **Otherwise:** an industry model
- **Caveat:** Modelled, not measured: 30 needless replacements and 15 failed repairs per 1,000 cases today, each reduced by a fifth; apply to the prospect's own volumes.
- **Note:** The same model as before (3.0% → 2.4% needless replacements, 1.5% → 1.2% failed repairs), re-expressed per 1,000 so it reads as a gain and counts both error directions. In money at the sourced per-decision values the modelled gain is about £3,700 per 1,000 cases (six needless replacements about £2,760 of glass, plus recalibrations and repeat visits), about £3.70 per case, close to the market's per-inspection software price; that is why the set leads with the value per correct decision.
- **Source:** research: the value model in the response set, re-expressed per 1,000 cases

### Decision consistency across sites

- **Kind:** technical
- **Signed off by:** Head of Technical Standards
- **Formula:** Share of matched damage cases receiving the same decision across sites in one market
- **Baseline:** not measured anywhere today
- **Figure:** -
- **Whose metric:** the payer audits it; the operator owns it
- **Source:** research: no competitor reports this metric at all

### Reviewer override rate

- **Kind:** technical
- **Signed off by:** Head of Claims
- **Formula:** Decisions changed by the reviewer, over all decisions presented
- **Baseline:** measured per engagement
- **Figure:** -
- **Whose metric:** both — it is the evidence the human review is real
- **Caveat:** An aggregate product metric only. Never used to evaluate individual reviewers.
- **Source:** research: the oversight test four regulators converge on

## Packages

- **Status:** confirmed
- **Value for the client:** Payer: about £460 of glass saved per needless replacement avoided, and a decision that survives audit and dispute. Operator: the job done once, with the right part and any recalibration already booked.
- **Value for Oracle and NVIDIA:** Net-new GPU consumption on OCI, built on VSS, which Oracle already deploys in one click.
- **Source:** user:2026-09-22

### PoV Jumpstart · S

- **Id:** pov
- **Duration:** 6–8 weeks (target 8, hard cap 10)
- **Duration note:** CONFIRMED (user:2026-09-22): a narrower 8-week proof, deliberately not the 12-week engagement. One asset class, one market's rule set, one measured feature set, file-based in and out. Everything else moves to the later packages.
- **Services price:** to be defined
- **What you get:**
  - one market's rule set, versioned
  - measured decisions on one asset class against that rule set
  - a reviewer workspace with override and a decision record
  - an accuracy evaluation against an agreed holdout set, with the measurement basis stated
- **In scope:** guided capture with a scale anchor; detection, classification and measurement; the cited decision; review and override; an evidence export
- **Out of scope:** coverage and entitlement; priced scope and the write-off test; integrity and tamper detection; write-back into the system of record; more than one market's rules

### Integration · M

- **Id:** integration
- **Duration:** 12–20 weeks
- **Services price:** to be defined

### Scaling · L

- **Id:** scaling
- **Duration:** 12–52 weeks
- **Services price:** to be defined

### How each capability area is handled per tier

| Area | PoV | Integration | Scaling |
|---|---|---|---|
| Capture & intake | ◐ One capture channel, one language | ● The operator's own channels and branding | ●● Every market, every language |
| Damage assessment | ◐ One asset class, one taxonomy | ● Additional asset classes | ●● Per-market taxonomies and retraining |
| Decision & estimate | ◐ One market's rule set | ● Multiple markets and contracts | ●● Priced scope and the economic test |
| Assurance & audit | ◐ Review, override and a decision record | ● Integrity checking and machine QA | ●● Override instrumentation and reporting |
| Operations & administration | ◐ Rules authored by SoftServe | ● Rules authored by the customer | ●● Multi-market administration and simulation |

### Why it sells for the partner

- The saving dwarfs the price of deciding: one avoided replacement pays for many software decisions
- Two budgets in one account: the payer saves the replacement, the network saves the repeat visit
- Net-new GPU consumption on OCI: every assessment runs on OCI GPU capacity
- Repeatable across asset classes: vehicles, containers and aircraft on one rule layer

### What each buyer gets

- **Operator:** The job done once, with the right part, skill and slot, any recalibration booked with it, and one answer at every site
- **Payer:** Replacements funded only when the rules require them, the gap between replacing and repairing banked each time, and a decision that survives audit and dispute

## Proof

- **Customer:** (withheld by owner instruction — the account name is not recorded in this file)
- **Delivered:** -
- **Divergence from the pack:** The pack generalizes the rule layer, the measurement and the decision record across five asset classes. The engagement hard-codes one network's guidance, measures nothing dimensionally, and names a single unspecified verification stage. The engagement is also video-first while its own customer's data is photographs; the pack treats media type as an input option, not a premise.
- **Divergence line:** The app measures the damage and versions the rules; the engagement it grows from classifies and cites.

## Open questions

1. Was the tender won, and is the incumbent live in the pathfinder market? Blocks whether this is a pack at all.
2. Is reuse permitted? No document states who owns what is built or whether it may be reused. Blocks the whole pack.
3. The authoritative scope document is cited page-by-page by the customer-facing deck and is not on this machine.
4. No measured result exists. Blocks every metric; artifacts print 'results to follow' until the proof of value runs.
5. The repair rules themselves are undocumented at the source customer, by both sides' admission.
6. Three candidate industries passed on reasoning only; the research ran out of search budget. They stay out of the pack.
7. Freedom to operate: a granted patent covers deciding vehicle damage from video frames with speech corroboration. Our design has no audio, which appears to distinguish it. Do not add audio corroboration.
8. Proof-of-value price is still to be derived from the signed engagement minus the scope removed for the narrower 8-week proof.
9. Both buyers are addressed by decision. Each artifact must be checked that it carries both, not just the operator.

## Settings

### Clearance

| Channel | Customer may be named |
|---|---|
| Internal | no |
| Partner print | no |
| Customer site | no |
| Demo | no |

- **Anonymized descriptor:** a multi-market vehicle services network
- **Descriptor warning:** Any descriptor naming vehicle glass plus multi-market back-solves to one company. External artifacts should rest on the domain and standards evidence and make no source-engagement reference at all.
- **Internal-only facts:** contract value and the add-on phase value; the named account and its pathfinder market; the two-vendor tender situation; team member names; the partner-signature status
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
  - **Name:** Oleksii Orlov
  - **Email:** RnDrequest@softserveinc.com

### Provenance

- **Inputs:**
  - **Path:** Customers/\<account>/UC #8 ... .docx
    - **Kind:** sow
    - **Read:** 2026-09-22
  - **Path:** Customers/\<account>/OneDrive_2026-09-17.zip (40 files)
    - **Kind:** rfi-corpus
    - **Read:** 2026-09-22
  - **Path:** two call recordings in that corpus
    - **Kind:** transcript
    - **Read:** 2026-09-22
- **Research brief:** packs/visual-damage-assessment/research-brief.md
- **Inventory:** inventory/E1-case-and-scope.md; inventory/E2-solution-architecture-value.md; inventory/E3-qa-transcripts-tracker.md
- **Research:**
  - research/P1-domain-workflow.md
  - research/P2-vendor-taxonomy-gaps.md
  - research/P3-competitor-classes.md
  - research/P4-P6-three-move.md
  - research/P7-failure-paths.md
  - research/P10-dach-and-regulatory.md
  - research/P11-technical-coherence.md
