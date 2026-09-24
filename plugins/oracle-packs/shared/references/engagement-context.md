# Engagement context — Oracle + NVIDIA accelerator packs

_The minimum an artifact builder must know about the engagement before writing a word. Distilled from the practice's Oracle wiki and pack pages, the June 2026 approach and packaging briefs, the 2026-06-26 Oracle packaging session, and the owner's decisions of 2026-09-18. Rewritten to current truth — never appended with dated updates._

Rows marked **⚠** are volatile. Each carries its own re-check line; do not copy a ⚠ row into an artifact without confirming it first.

## 1. Who Oracle is to us

NVIDIA builds the accelerator packs (AI-Q, cuOpt, VSS). They run on Oracle Cloud Infrastructure. SoftServe verticalizes a pack, extends it into a real business application, and delivers it to the end customer.

- **⚠ SoftServe is one of several integrators** Oracle works with, and Oracle runs more than one partner in parallel on some projects. There are **no shared KPIs and no shared due dates** with Oracle. *Re-check before use: the competitor set and SoftServe's standing move with each Oracle reorganisation.*
- **The delivery bar is dual:** a C-level narrative **and** tangible operational proof. An artifact that carries only one of the two fails with this audience.
- **⚠ Oracle-side ownership of the packs changes often** — product, presales, value-realization and compute organisations have each held a piece. *Re-check before use, and prefer not to name an individual owner in any artifact at all.*

## 2. Why we package at all

Oracle's GTM teams want to expand enterprise accounts into OCI-based, AI-powered use cases. Three gaps stop them:

- **Platform capability.** Oracle's own enterprise-AI and Fusion surfaces are outmatched by NVIDIA in vision, GPU-accelerated optimization and agent orchestration — and NVIDIA is Oracle's strategic partner.
- **Business-application coverage.** The existing accelerator packs tailor the platform to a handful of use cases; the live customer pipeline exposes many that no pack covers.
- **Delivery predictability.** There is no predictable, transparent, value-driven framework for delivering these applications, which reduces GTM-team engagement and customer conversions.

The answer is three classes of deliverable. Every artifact these skills build serves one of them:

1. **Packaged apps** — business-application-specific packs, prioritized off the real pipeline, used for trials, self-testing and demos, self-service provisioned in the OCI portal.
2. **Packaged services** — standardized delivery packages with framed scope and timing, for phased rollout and later expansion.
3. **GTM enablement** — material that shortens the sales cycle: feature list, sales deck, sales one-pager, executive summary, mini-site listing, interactive demo.

## 3. What Oracle gets

- **OCI consumption is the driver.** Accelerator projects tend to land as dedicated AI clusters — client-committed, client-paid GPU capacity. The pack is the on-ramp; the compute commitment is the revenue. That is why the demand side pushes low-friction pilots so hard.
- **Anchor a pack to Oracle Fusion applications** wherever the use case allows: the workflow API endpoints are known by definition (no requirements engineering), Fusion reps have a warm path to the application owner, and those reps are compensated on OCI consumption.
- So every partner-facing artifact carries a **"why it sells" block** for the Oracle seller: the Fusion cross-sell, net-new OCI and GPU consumption on top of the SaaS seat, repeatability across comparable accounts.

## 4. Who reads what

Priority order is fixed. When two readers want different things, the higher row wins.

| # | Reader | What they need | What they do not need |
|---|---|---|---|
| 1 | **Oracle sellers and partners** | The "why it sells" block, the vertical framings, one price band, a duration, a named contact to hand off to | Architecture depth, feature glyph matrices, our internal delivery model |
| 1b | Oracle **presales** — same audience, deeper | Reference architecture and the layer cake (OCI + GPU → NVIDIA stack → accelerator pack → tailored SoftServe layer), the feature matrix with ● ◐ ○, integration scope per tier | Commercial framing they cannot quote |
| 2 | **SoftServe sellers** | The internal executive-summary slide: what the pack is, who it is for, what it costs, what is reusable versus custom | Customer-facing polish |
| 3 | **End customers** | The mini-site: the job and the outcome in their own words, the workflow, the verticals, the PoV price and duration, one way to get in touch | Customer names, prices beyond the PoV, internal taxonomy, anything about how we build it |

## 5. Pack anatomy

A pack is described once, in one signed-off spec, by twelve components — problem ↔ solution, one-liner, target ICP, name, verticals, capabilities and features, workflow architecture, high-level architecture, required Oracle products, optional Oracle products, key performance metrics, and the service packages table — plus cross-cutting clearance, figures, contacts and provenance. Every artifact reads its values from that spec; none re-derives them. The component definitions, the per-artifact map, and the nine solution layers a packaged app is built from (UI · backend logic · analytics · AI pipeline · integrations · access rights · app configuration · observability · infrastructure and platform wiring) live in `shared/references/pack-anatomy.md`; the machine-readable shape is `shared/schema/pack-spec.md`.

## 6. The service-package model

One vocabulary everywhere: **PoV Jumpstart · Integration · Scaling**. S/M/L survive only as size tags in internal tables. Print artifacts still carrying older tier names are relabelled at their next rebuild.

| Tier | What it is | Scope |
|---|---|---|
| **PoV Jumpstart** (S) | "Proving AI value" | You give us data, we prove value on your data. **Zero integration**, separate or test environment, possibly test data. Fixed scope per use case. |
| **Integration** (M) | "Delivering real business impact" | A live, fully integrated MVP. One to two API integrations for data exchange, optional customer auth and security. One to two key markets. |
| **Scaling** (L) | "Scaling the impact" | Many markets, market-local rules and customizations, advanced AI telemetry, org-wide rollout. |

Rules that hold for every pack:

- **The sizing axis is integration depth, not feature count.**
- **PoV duration is set per pack, ideally 4–8 weeks. Ten weeks is a hard cap** — a longer PoV must be argued, and the spec skill pushes back and explains why.
- **PoV Jumpstart and Scaling are optional.** A customer already bought into the use case starts at Integration; a customer with one uniform global process may never need Scaling.
- **"Integration" means background data exchange through existing product APIs**, not native UI inside the vendor's own application.
- **Production hardening lives in Scaling and is never labelled "hardening".**
- **State the tier next to every integration claim.** The same pack can truthfully say "file export and import" at PoV and "API write-back" at Integration; unqualified, one of the two is wrong.
- **⚠ Prices and durations live in the pack spec, per pack — never in this document.** Every price carries its disclaimer. *Re-check before use: price sets change per pack and per quarter, and several superseded sets are still in circulation in old files.*

## 7. Naming

⚠ Vendor product names are in a heavy rebranding wave: the discipline is durable, the strings are not. **Re-verify each against the vendor's own live product page before shipping**, and take product ids from `shared/data/oracle-products.yaml`.

| Write this | Not this |
|---|---|
| Oracle Autonomous AI Lakehouse | "Oracle AI Lakehouse" |
| Oracle AI Data Platform | "AIDP" in anything a customer or partner reads |
| Oracle AI for Fusion Applications (umbrella) · Oracle AI Agent Studio for Fusion Applications (the build surface) | "Oracle Fusion AI" |
| NVIDIA NeMo Agent Toolkit | "NVIDIA NeMo Agents" |
| OCI · NVIDIA AI-Q · cuOpt · VSS | — |

There is **no joint OCI + NVIDIA product brand**; an artifact naming one thing has to pick a side. Full table, evidence, channel-by-channel pack naming and the clearance rules: `shared/references/naming-and-clearance.md`.

## 8. Clearance, in brief

A customer's name or logo appears only where the pack's clearance allows it for that audience: the spec run always asks, proposing yes for our own team and for Oracle and SoftServe sellers; without a yes, the case ships as an anonymized descriptor (industry and scale, nothing that back-solves). No Oracle partner-standing claim of any kind; the permitted phrasing is joint delivery with Oracle's AI & Data organisation. Never "AIDP" externally. Every price carries its disclaimer, and only the PoV price is published on the customer site. One metric set per pack, attribution varying by channel. Inside a demo the rule inverts: vendor product names and interfaces are expected and correct, only customer marks are banned — and since no vendor logo file is cleared, a wordmark ships as text. **The pack owner clears everything.** Operative rules per channel, the banned-vocabulary list and the linter contract: `shared/references/naming-and-clearance.md`.

## 9. What to re-check before you use this page

Confirm the ⚠ rows before an artifact goes out: the integrator picture and who owns the packs on the Oracle side (§1), every vendor product name against its live product page (§7), and every price, duration and figure against the pack spec rather than against this page or an older artifact (§6). Re-confirm clearance each round — it is revocable and has been withdrawn after being granted. People, prices and product names are the three things this page deliberately does not try to hold.
