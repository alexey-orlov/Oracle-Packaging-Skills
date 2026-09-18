/* exemplar-product-entry.js — the worked example a listing entry is calibrated to.
 *
 * WHAT THIS IS
 *   One entry of `window.SITE_CONTENT.products[]`, copied verbatim from a shipped
 *   practice site, plus the two things that travel with it: its `window.SITE_CONFIG.products[<slug>]`
 *   switch block and its `window.SITE_DIAGRAMS[<slug>]` architecture figure.
 *
 * HOW TO USE IT
 *   This file is the SPEC, not a template to paraphrase. Per the exemplar rule: when you
 *   fill a structure that already carries an exemplar, match the exemplar's altitude, length
 *   and phrasing — the existing cells are the specification, the source documents are not.
 *   Read `../references/listing-schema.md` for the key-by-key contract and the invariants,
 *   and `../references/listing-rules.md` for the content and messaging rules each string obeys.
 *
 * WHAT WAS CHANGED FROM THE SOURCE
 *   - `config.demoPreviewUrl` is blanked: the live value was an account-bound artifact URL.
 *     It is a per-runner input, never a shipped constant.
 *   - Nothing else. No customer name, geography or identifier appears in the source entry
 *     (verified by deny-list grep); the case study identifies its customer by an anonymized
 *     descriptor and an industry medallion, which is the required shape.
 *
 * NOTE ON THE FILE EXTENSION
 *   `.js` so an editor highlights it. It is a fragment, not a loadable module: the entry is a
 *   single array element and the three blocks below belong to three different files.
 */

/* =========================================================================
 * 1 · window.SITE_CONTENT.products[] — one entry
 * Insert before the closing `]` of `products: [` in site/data/content.js.
 * ========================================================================= */
    {
      slug: "workforce-optimization",
      name: "Workforce optimization",
      headline: { accent: "WORKFORCE", rest: "OPTIMIZATION" },
      category: "data-analysis",
      categoryChip: "Data analysis & optimization",
      facet: "oci-nvidia",
      oneLiner: "Optimizes field-service work zones and schedules with NVIDIA cuOpt — a region’s four-week plan built in minutes, approved by dispatchers, exported to Oracle Field Service.",
      shortLine: "A region’s four-week field plan, optimized in minutes and approved by dispatchers.",
      heroCaption: "What if dispatchers reviewed the plan, not built it?",
      tags: ["Data analysis & optimization", "OCI + NVIDIA"],
      hero: {
        image: {
          file: "assets/img/heroes/workforce-optimization.jpg",
          alt: "An overhead field of interlocking hexagonal plates, with loose ones still settling into the pattern from above",
          focal: "50% 55%"
        }
      },
      tile: {
        outcomes: [
          "A region’s four-week plan optimized and approved in ~30 minutes, down from ~2 days",
          "Dispatchers review the plan instead of building it — then export it straight to Oracle Field Service",
          "Native Oracle Field Service integration: known endpoints, no requirement engineering"
        ]
      },
      overview: {
        problemSolution: {
          problem: {
            title: "THE PROBLEM",
            text: "Field-service operators plan their mobile workforce by hand: work zones, technician assignments, dozens of rules and constraints. Workloads come out uneven, wait times long, and new zones launch slowly.",
            icon: "alert"
          },
          solution: {
            title: "THE SOLUTION: REVIEW THE PLAN, NOT BUILD IT",
            text: "NVIDIA cuOpt ingests demand, availability, skills and constraints and computes the best technician-to-zone-to-job plan in minutes. Dispatchers review it on a live map, re-optimize, and write the approved plan back to Oracle Field Service.",
            icon: "spark"
          }
        },
        metrics: [
          { value: "~30 min", label: "To optimize and approve a region’s four-week plan", qualifier: "Down from ~2 days", icon: "clock" }
        ],
        metricsNote: "Each KPI is computed identically for the current plan and the optimized one, on the customer’s historical proof-of-value data — modeled against that baseline, not measured in production; figures are illustrative, not contractual.",
        roi: {
          icon: "roi",
          text: "The gain lands in the field: the same technicians complete more jobs per day, with less travel and less waiting. A single-digit percentage runs across every region."
        },
        features: [
          "Work-zone and availability rules, with skill-based allocation",
          "Planned-vacation reallocation and same-day sickness handling",
          "Default, neighboring and cross-zone allocation",
          "Forecast-based allocation against a demand forecast you supply",
          "Commitment rules: non-movable appointments and SLA types per appointment *",
          "Multi-objective optimization with hard and soft rule weighting",
          "Dispatcher review UI: map and table views, approve, reject, re-run",
          "KPIs and analytics: productivity, utilization, travel, workload balance"
        ],
        featuresNote: "* Commitment-rule coverage is partial out of the box; the exact constraint set is confirmed in scoping.",
        featuresDetail: [
          { title: "Work-zone and availability rules", body: "Skill-based allocation, maximum load per day, planned-vacation reallocation, same-day sickness handling, default and neighboring work zones, cross-zone allocation." },
          { title: "Forecast-based allocation", body: "Allocate against a demand forecast you supply." },
          { title: "Commitment rules", body: "Non-movable appointments and different SLA types per appointment.*" },
          { title: "Multi-objective optimization", body: "Productivity, waiting time and workload balance, with hard/soft rule weighting and minimal disruption of the current allocation." },
          { title: "Dispatcher review UI", body: "Map and table views, approve or reject, with model-decision explanations and recommendations." },
          { title: "KPIs and analytics", body: "Productivity, capacity utilization, travel reduction and workload balance." }
        ],
        industriesNote: "Any mobile field force planned against skills, availability and geography.",
        steps: [
          {
            n: 1,
            title: "Load the period's data",
            text: "Demand, technician availability, skills, work zones and the period's bookings come in from Oracle Field Service.",
            image: "assets/img/steps/workforce-optimization-1.jpg",
            features: [
              "Work-zone and availability rules, with skill-based allocation",
              "Planned-vacation reallocation and same-day sickness handling"
            ]
          },
          {
            n: 2,
            title: "Set the rules",
            text: "Zone, forecast and commitment rules are configured, then weighted as hard or soft constraints against the objectives that matter.",
            image: "assets/img/steps/workforce-optimization-2.jpg",
            features: [
              "Default, neighboring and cross-zone allocation",
              "Forecast-based allocation against a demand forecast you supply",
              "Commitment rules: non-movable appointments and SLA types per appointment *"
            ]
          },
          {
            n: 3,
            title: "Solve the plan",
            text: "cuOpt computes the technician-to-zone-to-job plan against every constraint at once, in minutes rather than days.",
            image: "assets/img/steps/workforce-optimization-3.jpg",
            features: ["Multi-objective optimization with hard and soft rule weighting"]
          },
          {
            n: 4,
            title: "Review, approve, measure",
            text: "The dispatcher compares plans on a live map, approves or re-runs, and the KPI readout shows what changed.",
            image: "assets/img/steps/workforce-optimization-4.jpg",
            features: [
              "Dispatcher review UI: map and table views, approve, reject, re-run",
              "KPIs and analytics: productivity, utilization, travel, workload balance"
            ]
          }
        ],
        industryCases: [
          {
            industry: "manufacturing",
            label: "Manufacturing",
            image: "assets/img/industries/manufacturing.jpg",
            problem: "In-home repair of manufactured goods is planned by hand: work zones and technician allocations, region by region, juggling skills, spare parts, travel and absences. Urgent call-outs and no-shows mean re-planning the day.",
            solution: "The solver plans the whole region against skills, parts, travel and existing bookings at once, and the dispatcher reviews and approves the result. Rules that differ by market — working time, holidays, service commitments — are configuration, so setting up a new region is a configuration job."
          },
          {
            industry: "utilities",
            label: "Utilities",
            image: "assets/img/industries/utilities.jpg",
            problem: "Water, gas and electric crews are scheduled across service territories against SLAs, crew certifications and outage spikes. Planned and emergency work compete for the same capacity, and the balance is struck manually by a handful of senior dispatchers.",
            solution: "Territories, certifications and SLA commitments become weighted constraints, and the plan is re-solved as the day's demand changes. Planned and emergency work are balanced against the objectives you weight, and no allocation reaches a crew until a dispatcher approves it."
          },
          {
            industry: "telecom",
            label: "Telecom & cable",
            image: "assets/img/industries/telecom.jpg",
            problem: "Install-and-repair technicians have to be routed to tight appointment windows across regions, matched to line skills. Missed windows cost customer satisfaction directly, and launching a new service zone depends on scarce planning expertise.",
            solution: "Appointment windows and line skills are modeled as commitment and skill rules, and the solver routes against them while minimizing travel. Launching a new zone comes down to a configuration change."
          },
          {
            industry: "healthcare",
            label: "Healthcare",
            image: "assets/img/industries/healthcare.jpg",
            problem: "Medical-device and equipment service engineers are allocated to contracted assets by skill, SLA and location. Uptime on high-value machines is contractual, and the allocation is worked out by hand against a rising number of installed assets.",
            solution: "Contracted SLAs, engineer certifications and asset locations become the constraint set the solver works against, with uptime-critical commitments weighted as hard rules. The KPI readout compares the current and the optimized plan on identical definitions."
          }
        ],
        scope: {
          in: [
            "Foundational allocation with the recurring, most-typical constraints — zones, skills, planned absences",
            "Core KPIs predicted at scheduling and measured against the signed benchmark",
            "The dispatcher review UI, with approve, reject and re-run",
            "Sandboxed deployment on your own tenancy",
            "A before/after KPI readout computed identically on both plans"
          ],
          out: [
            "Oracle Field Service integration — delivered after the Jumpstart",
            "Additional data sources and BI integration — delivered after the Jumpstart",
            "The re-optimization feedback loop — delivered after the Jumpstart",
            "Live-traffic travel rules, within-day reassignment, spare-parts and crew-based assignment — on the roadmap"
          ]
        },
        moreDetail: [
          { title: "Today", body: "Dispatchers maintain work zones and technician allocations by hand, region by region, juggling postcode coverage, skills, working days and absences, with little room to optimize." },
          { title: "Tomorrow", body: "The dispatcher uploads the period’s data, runs cuOpt on OCI, and reviews the optimized allocation on a live map — comparing, approving or re-running before export to Oracle Field Service. The solver returns the schedule that scores best against the weighted objectives." },
          { title: "Suboptimal efficiency", body: "Uneven workloads and under-used capacity." },
          { title: "Lower customer satisfaction", body: "Longer wait times from suboptimal allocations." },
          { title: "Poor scalability", body: "Planning hinges on scarce senior dispatchers; new zones launch slowly." },
          { title: "How the KPIs are defined", body: "Time to plan: how long to optimize and approve a region’s four-week plan. Productivity: jobs per technician per working day. Capacity utilization: booked activity time against available capacity. Customer wait time: calendar days between booking and appointment. Each is computed identically for the current plan and the optimized plan." },
          { title: "Delivered after the Jumpstart", body: "Oracle Field Service integration — staff, availability and booking data in; optimized allocations (zones, visits) out; factual durations and times back. The architecture is native to Oracle Field Service; the integration itself comes after the Jumpstart, not inside it. Also after the Jumpstart: additional data sources and BI integration (up to five typical integrations — booking, inventory for parts availability, HR/WFM for people availability, demand forecasting, BI), and the re-optimization feedback loop." },
          { title: "On the roadmap, not in the pack today", body: "Distance and travel-time rules with live traffic · within-day dynamic reassignment and urgent-request handling · spare-parts and crew-based assignment · the human-feedback learning loop." }
        ],
        caseStudy: {
          descriptor: "A global home-appliance manufacturer",
          area: "Field-service operations across three countries",
          industry: "manufacturing",
          status: "modeled",
          metrics: [
            { value: "+4.5%", label: "median gain in jobs per technician per day, optimized against the current plan" },
            { value: "~5x", label: "return within three years on the modeled rollout" }
          ],
          story: "Dispatchers planned a residential appliance-repair field force by hand — postcode-based work zones and technician allocations, region by region. NVIDIA cuOpt on Oracle Cloud Infrastructure was run against the customer’s own historical operations data with dispatcher approval in the loop: 83% of the 12 modeled simulations came out positive, and dispatcher productivity improved 15–20% during the pilot. Figures are forecast from those simulations against the customer’s own historical baseline; illustrative, not contractual.",
          scope: [
            { label: "Duration", value: "Three months" },
            { label: "Data footprint", value: "Historical operations data" },
            { label: "Constraints modeled", value: "Around thirty" }
          ],
          ndaLine: "Customer under NDA · reference call available on request",
          downloadLabel: "Download the case summary"
        }
      },
      technology: {
        narrative: "Oracle Field Service is both the source and the destination. NVIDIA cuOpt computes the allocation on a dedicated AI cluster on Oracle Cloud Infrastructure, and the approved plan is written back — nothing reaches the field until a dispatcher approves it.",
        stack: [
          {
            key: "application",
            label: "Application / accelerator",
            summary: "The SoftServe pack: the dispatcher UI, the approval workflow, the re-solve loop and the KPI layer.",
            vendors: ["softserve"],
            items: [
              { name: "Dispatcher review UI and approval workflow", required: true },
              { name: "Re-solve loop", required: true },
              { name: "KPI and analytics layer — productivity, utilization, travel, workload balance", required: true },
              { name: "Write-back to Oracle Field Service", required: false, note: "After the Jumpstart" }
            ]
          },
          {
            key: "ai-engine",
            label: "AI engine",
            summary: "NVIDIA cuOpt solves the technician-to-zone-to-job plan on GPUs.",
            vendors: ["nvidia"],
            items: [
              { name: "NVIDIA cuOpt, the GPU-accelerated optimization solver", required: true }
            ]
          },
          {
            key: "data-platform",
            label: "Data & platform",
            summary: "Oracle Field Service is both the source and the destination; storage holds the period's data.",
            vendors: ["oracle"],
            items: [
              { name: "Oracle Field Service, as source and destination", required: true },
              { name: "OCI Object Storage for the period's data", required: true }
            ]
          },
          {
            key: "infrastructure",
            label: "Infrastructure",
            summary: "A dedicated GPU cluster in your own tenancy, with its networking and IAM.",
            vendors: ["oracle"],
            items: [
              { name: "A dedicated AI cluster (4–8 NVIDIA A100 GPUs)", required: true },
              { name: "Object storage, networking and IAM", required: true }
            ]
          },
          {
            key: "custom",
            label: "Configuration & integrations",
            summary: "Client rules, constraints, KPI definitions and the data integrations.",
            vendors: ["softserve"],
            items: [
              { name: "From Oracle Field Service: staff, availability and booking data", required: true, direction: "inbound" },
              { name: "Back from Oracle Field Service: factual durations and times", required: false, direction: "inbound" },
              { name: "To Oracle Field Service: optimized allocations — zones and visits", required: true, direction: "outbound", note: "After the Jumpstart" },
              { name: "Up to five further integrations — booking, inventory, HR/WFM, demand forecasting, BI", required: false, direction: "inbound", note: "After the Jumpstart" },
              { name: "Client rules, constraints and KPI definitions", required: true }
            ]
          }
        ],
        capabilities: [
          {
            stage: "Load the period's data",
            items: [
              { name: "Oracle Field Service as the source for demand, availability, skills and bookings — delivered after the Jumpstart" },
              { name: "Demand forecasting, booking, inventory, HR/WFM and BI sources — delivered after the Jumpstart" },
              { name: "Skill-based allocation", state: "supported" },
              { name: "Maximum load per day", state: "supported" },
              { name: "Planned-vacation reallocation and same-day sickness handling", state: "supported" }
            ]
          },
          {
            stage: "Set the rules",
            items: [
              { name: "Default work zones per technician, and work-zone-level demand", state: "supported" },
              { name: "Neighboring work zones and cross-zone allocation", state: "supported" },
              { name: "Forecast-based allocation against a demand forecast you supply", state: "supported" },
              { name: "Non-movable appointments and SLA types per appointment", state: "partial" },
              { name: "Client rules, constraints and KPI definitions, configured per engagement" },
              { name: "Distance and travel-time rules with live traffic data", state: "roadmap" },
              { name: "Spare-parts availability and crew-based assignment", state: "roadmap" }
            ]
          },
          {
            stage: "Solve the plan",
            items: [
              { name: "Multi-objective optimization with hard and soft rule weighting", state: "supported" },
              { name: "Minimal disruption of the current allocation", state: "supported" },
              { name: "A region's four-week plan solved on GPU-accelerated cuOpt, in minutes" },
              { name: "Within-day job reassignment and urgent-request handling", state: "roadmap" }
            ]
          },
          {
            stage: "Review, approve, measure",
            items: [
              { name: "Dispatcher UI with map and table views", state: "supported" },
              { name: "Dispatcher approval or rejection before anything reaches the field", state: "supported" },
              { name: "Model-decision explanations and recommendations", state: "supported" },
              { name: "KPI readout: jobs per technician per working day, capacity utilization, travel reduction, workload balance", state: "supported" },
              { name: "The current plan against the optimized plan, computed on identical definitions" },
              { name: "The approved plan written back to Oracle Field Service — delivered after the Jumpstart" },
              { name: "Iterative feedback-based re-optimization", state: "roadmap" },
              { name: "Human-feedback-driven tuning and what-if alternatives", state: "roadmap" }
            ]
          }
        ]
      },
      jumpstart: {
        title: "Jumpstart Proof-of-Value",
        promise: "Pilot workforce optimization on your own historical data in 4–8 weeks, at a fixed price, and take away a before/after KPI readout your dispatchers have signed off.",
        durationShort: "4–8 weeks",
        pillars: [
          { key: "fast", title: "Fast", text: "4–8 weeks from kickoff to a before/after KPI readout on a real region of your own." },
          { key: "low-risk", title: "Low-risk", text: "Fixed scope at a fixed price: manual data import, the recurring constraints, a sandboxed environment on your own tenancy. A dispatcher approves every plan before anything reaches the field." },
          { key: "tangible", title: "Tangible", text: "An optimized four-week plan for one region, measured against your current plan on identical KPI definitions." }
        ],
        outcomes: [
          "An optimized four-week plan for one real region, computed on your own historical data.",
          "A before/after KPI readout — productivity, capacity utilization and wait time — computed identically on the current and the optimized plan.",
          "The dispatcher review UI running in a sandboxed environment on your tenancy.",
          "A costed plan for the next step: integration scope, additional sources, timeline."
        ],
        timeline: [
          { label: "Week 0 · Gate", text: "Sponsor named, two to three success metrics signed, the baseline and source access approved in writing." },
          { label: "Weeks 1–4 · Build", text: "The period’s data imported; zones, skills, absences and commitment rules configured and weighted against your objectives." },
          { label: "Weeks 5–7 · Review", text: "Dispatchers compare the current and the optimized plan on a live map, approve or re-run." },
          { label: "Week 8 · Decision", text: "Before/after KPI readout against the signed benchmark, and a costed proposal for the next step." }
        ],
        needs: [
          "One real region and a period of historical planning data — demand, availability, skills, work zones and bookings",
          "The allocation rules that actually apply: zones, skills, absences, service commitments",
          "A dispatcher and a business owner who will review the plan and sign the baseline"
        ],
        investment: {
          price: "€90K services · €4K/mo infrastructure",
          duration: "4–8 weeks",
          includes: [
            "Foundational allocation with the recurring, most-typical constraints — zones, skills, planned absences",
            "Core KPIs predicted at scheduling and measured against the signed benchmark",
            "The dispatcher review UI, with approve, reject and re-run",
            "Sandboxed deployment on your own tenancy"
          ],
          footnote: "Figures are illustrative and confirmed in scoping."
        },
        next: [
          { tier: "Integration", text: "Full setup and integration, live at one location: Oracle Field Service integration, additional data sources and BI, the re-optimization feedback loop, on a dedicated landing zone with IAM and observability.", duration: "3–5 months", price: "€300–500K services · ~€25K/mo infrastructure, depending on usage and rule complexity" },
          { tier: "Scale", text: "Across locations, with per-region rule sets and data workflows, deployed multi-zone.", duration: "3–12 months", price: "Scoped per engagement" }
        ],
        cta: { label: "Start a Jumpstart conversation", route: "#/products/workforce-optimization/contacts" }
      },
      sellers: {
        materials: [
          { key: "sales-deck", title: "Sales deck — service packages", description: "10 slides: verticals, today/tomorrow, proof of value, solution layers, reference architecture, the three packages and the capability-by-tier matrix.", state: "link-pending" },
          { key: "one-pager", title: "Sales overview (one-pager)", description: "Problem, solution, architecture, proof strip, the three packages with pricing, CTA.", state: "link-pending" },
          { key: "feature-list", title: "Accelerator pack one-pager (feature list)", description: "The full capability matrix: what is out of the box, what is roadmap, and the standard customization scope per area.", state: "link-pending" },
          { key: "demo-video", title: "Demo video", description: "A recorded walkthrough of the dispatcher review UI.", state: "coming-soon" },
          { key: "marketplace-package", title: "Oracle Marketplace package", description: "The listing package for the product’s Oracle Marketplace entry.", state: "planned" }
        ]
      }
    },

/* =========================================================================
 * 2 · window.SITE_CONFIG.products["<slug>"] — the per-slug switch block
 * Insert into the `products: { … }` map in site/data/config.js.
 * Every key must exist; an empty string means "do not render that control".
 * `demoPreviewUrl` is the standalone demo artifact's own URL — an input the
 * runner supplies after publishing the demo, never a value carried in a repo.
 * ========================================================================= */
    "workforce-optimization": {
      marketplace: true,
      marketplaceUrl: "",
      demoUrl: "demo/workforce-optimization/index.html",
      demoPreviewUrl: "",
      video: true,
      videoUrl: "",
      videoPoster: "assets/img/posters/workforce-optimization.jpg",
      successStoryUrl: "",
      materials: {
        "sales-deck": "",
        "one-pager": "",
        "feature-list": "",
        "demo-video": "",
        "marketplace-package": ""
      }
    },

/* =========================================================================
 * 3 · window.SITE_DIAGRAMS["<slug>"] — the architecture figure
 * Insert into site/data/diagrams.js. `layout` is "flow" (sources → an OCI
 * group → a human approval target) or "hub" (a platform hub with items).
 * The figure is drawn from the spec's `architecture.stack[]` vendor ladder;
 * the `target` is always the human gate, and `loop` / `note` states the
 * one invariant that keeps the workflow honest.
 * ========================================================================= */
  "workforce-optimization": {
    layout: "flow",
    sources: [
      { title: ["Oracle Field", "Service"], sub: ["Staff, availability,", "bookings"] }
    ],
    group: {
      label: ["Oracle Cloud Infrastructure", "dedicated AI cluster"],
      nodes: [
        { title: ["Workforce app"], sub: ["Dispatcher map,", "re-solve, approve"] },
        { title: ["NVIDIA cuOpt"], sub: ["GPU-accelerated solver"] }
      ]
    },
    target: { title: ["Dispatcher", "approves"], sub: ["No allocation reaches", "the field unreviewed"], accent: true },
    loop: "Approved plan written back to Oracle Field Service"
  },
