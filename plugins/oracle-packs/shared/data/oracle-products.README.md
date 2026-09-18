# `oracle-products.yaml` — the shared Oracle + NVIDIA product catalog

**Version `2026-09-18` · 55 entries · names fetched from the vendors' own pages on 2026-09-18.**

One distilled catalog with canonical names, from which every accelerator pack picks its products —
so the same product is named and aggregated identically across packs, artifacts and channels.

---

## What it is for

Every pack declares its Oracle and NVIDIA products by `id` from this file, with a per-item
`required` / `optional` flag inside its architecture stack:

- **Required** — the pack is built on it, or fully relies on it.
- **Optional** — could logically be used with it, as an additional data source or destination system.

"Oracle products" here means the whole surface a pack can touch: OCI products (compute and GPU
shapes, Object Storage, networking, databases, the data platform, AI services), Oracle Fusion Cloud
applications (ERP, SCM, HCM, CX, Field Service, Procurement, EPM), the Oracle AI for Fusion
Applications / AI Agent Studio surfaces, and the NVIDIA components that run on OCI as part of the
packs (AI-Q, NeMo Agent Toolkit, cuOpt, VSS, NVIDIA AI Enterprise, NIM, Nemotron).

Picking by `id` is the point. Free-text product names drift between artifacts — the same product is
already written three ways across the current pack set (see *Naming conflicts found*, below) — and a
required/optional roll-up across packs is only meaningful if the names aggregate.

## The record

| Field | Meaning |
|---|---|
| `id` | kebab-case, stable. **Never renamed** — packs reference it. A superseded product gets a new id, not an edited one. |
| `name` | Canonical, as the vendor writes it today. The string that goes in an artifact. |
| `short` | ≤ 3 words, for chips, stack rows and table cells. |
| `vendor` | `Oracle` or `NVIDIA`. There is no joint brand — see the naming rules. |
| `family` | `oci-compute` · `oci-storage` · `oci-network` · `oci-database` · `data-platform` · `ai-platform` · `ai-services` · `fusion-apps` · `industry-apps` · `nvidia-stack` · `other` |
| `layer` | `infrastructure` · `platform` · `engine` · `application` · `data-source-destination` |
| `what_it_is` | ≤ 25 words, vendor-accurate, drawn from the vendor's own page. |
| `typical_role_in_a_pack` | `runs-the-engine` · `hosts-the-app` · `stores-data` · `source-system` · `destination-system` · `model-service` · `agent-runtime` · `analytics` · `integration` · `governance` |
| `aliases` | Old or informal names to map **from** when reading an existing artifact (`AIDP`, `OFS`, `cuOpt on OCI`). |
| `not_this` | Wrong spellings to **reject** when writing. An alias can appear in both lists: fine to read, never to write. |
| `url` | The vendor page the name and definition were verified against. |
| `verified` | `true` = the `name` matches that page's own H1 or `<title>`. `false` = could not be confirmed; see below. |
| `notes` | Optional. Pack-specific facts, disambiguation traps, product-state caveats. |

`industry-apps` is declared but currently unused — no pack touches an Oracle industry application yet.
`layer: data-source-destination` is likewise unused: every product catalogued so far has a real
position in the stack, and its source/destination role is carried by `typical_role_in_a_pack`
(`source-system` / `destination-system`) instead.

## Adding or changing an entry

1. **Fetch the vendor's own product page and read the H1.** That string is the `name`. Do not take a
   name from a slide, a blog post, a partner deck, or from memory — Oracle is mid-rebrand and page
   names move. `oracle.com` returns **403 to WebFetch**; it serves fine to `curl` with a browser
   User-Agent, which is how every name in this file was verified.
2. Write `what_it_is` from that page, ≤ 25 words, in the vendor's own terms. No marketing adjectives.
3. Add every way the product is already written in our artifacts to `aliases`, and every plausible
   wrong spelling to `not_this`. Search the existing pack artifacts before assuming there is only one.
4. Set `verified: true` only if step 1 actually landed on a live page whose H1 or title carries the
   name. Otherwise `verified: false` plus a `notes` line saying what failed. **Never invent a name.**
5. Bump the top-level `version` (and `fetched`, if you re-verified) in the same commit.
6. If the change affects how a product must be written, add or sharpen a line in `naming_rules` —
   don't leave the rule implicit in a single entry's `not_this`.

## Unverified entries

One, as of `2026-09-18`:

- **`oracle-analytics-cloud`** — `verified: false`. Oracle's product-specific pages for Analytics
  Cloud (`/analytics/analytics-cloud/`, `/business-analytics/analytics-cloud/`) both return 404.
  The live page at `/business-analytics/analytics-platform/` leads with the umbrella H1
  **"Oracle Analytics"**. If you need a name you can point a reader at a live page for, write
  *Oracle Analytics*. No pack currently requires it — it appears only as a downstream BI destination.

Every other entry's name was confirmed against the vendor's own live page. No fetch failed silently;
the pages that 404'd or redirected were chased to the URL that resolves, and that URL is what the
entry carries (e.g. `developer.nvidia.com/nemo-agent-toolkit` 301s to the NeMo docs; the Fusion AI
Agent Studio page is an anchor section of `/applications/fusion-ai/`, not its own page).

## Catalog change requests

Ids a pack needed and the catalog does not carry. A pack **never** invents an entry: it uses the
closest catalogued product, records the substitution in its own spec (`catalog_note`), and files the
request here. The catalog owner decides — a new entry needs the vendor's own page under step 1 of
*Adding or changing an entry*, which is why none of these was added on the spot.

| Requested by | The id the pack wanted | What it stands for | Resolved with | The question for the catalog owner |
|---|---|---|---|---|
| Workforce Optimization (worked example, 2026-09-18) | `oci-compute-gpu` | The GPU capacity a customer-run solver consumes: "OCI dedicated AI cluster, 4–8 NVIDIA A100" on the artifacts | `oci-dedicated-ai-cluster` | Two entries can answer this — `oci-dedicated-ai-cluster` (managed, reserved capacity inside OCI Enterprise AI) and `oci-gpu-instances` (raw GPU shapes). The packs say "dedicated AI cluster" and mean reserved capacity, so that is the id in use. If a pack ever sizes bare shapes, it should say `oci-gpu-instances` and the two must not be mixed in one roll-up. |
| Workforce Optimization (worked example, 2026-09-18) | `oci-networking` | The landing zone's networking | `oci-vcn` | The catalog names the product (Virtual Cloud Network); the packs write "networking". Alias only, or does a "landing zone" entry belong in the catalog as a bundle? |
| Workforce Optimization (worked example, 2026-09-18) | `oracle-fusion-inventory-management`, `oracle-fusion-demand-management` | Spare-parts availability and demand forecast as optional source systems | one `oracle-fusion-cloud-scm` entry covering both | Both are modules of Fusion SCM, so two pack entries collapsed into one and the pack lost the distinction between "inventory source" and "forecast source". Split the modules out (as the HCM entry's note already contemplates for Workforce Management), or keep the suite-level id and carry the module in the `why`? |

## Naming conflicts found between our docs and the vendor pages

These were live disagreements at the time of the fetch. The catalog resolves each in favour of the
vendor page; they are recorded here so the resolution can be argued with rather than silently inherited.

1. **Oracle Fusion Field Service vs Oracle Field Service.** Our artifacts split: the July-17 sales
   one-pager says *"Oracle Fusion Field Service"*, while the sales deck, the feature list and the
   mini-site all say *"Oracle Field Service"*. Oracle's own page H1 is
   **"Oracle Fusion Field Service"**. Catalogued as the Fusion form; the short form is an alias to
   read from and a `not_this` to write.
2. **Oracle AI Agent Studio vs Oracle AI Agent Studio for Fusion Applications.** Our naming table
   uses the long form. Oracle's current Fusion AI page uses the short form
   (`"name": "Oracle AI Agent Studio"`, section heading *"Discover AI Agent Studio"*). Catalogued as
   the **long** form anyway, because the AI Data Platform Workbench has its own, unrelated
   "Agent Studio" — the Fusion qualifier is what keeps the two apart in a stack row.
3. **OCI Generative AI Agents no longer exists as a brand.** Our offerings doc refers to
   *"Enterprise AI Agents in OCI Generative AI"*; `oracle.com/artificial-intelligence/generative-ai/agents/`
   now serves the **OCI Enterprise AI** page. Meanwhile **OCI Generative AI is still the service name
   in the OCI docs** and in Oracle's own blog headlines. Both are catalogued, with the agent brand as
   an alias of `oci-enterprise-ai`.
4. **OCI Document Understanding vs Oracle Document Understanding.** The mini-site writes the second;
   Oracle's own page description writes *"with OCI Document Understanding"*. Catalogued with the OCI
   prefix. The same rule applies to Vision, Speech and Language, whose page H1s drop the prefix
   ("AI Vision", "AI Language") while the service name keeps it.
5. **Oracle's own Autonomous AI Lakehouse page is half-rebranded.** Its H1 reads
   *"Oracle Autonomous AI Lakehouse"*, but its meta description still reads
   *"Oracle Autonomous Data Warehouse is a data and analytics platform…"*. Trust the H1; this is why
   the naming rule exists at all.
6. **Oracle Integration vs Oracle Integration Cloud (OIC).** H1 is *"Oracle Integration"*; the page
   `<title>` still carries *"Oracle Integration Cloud (OIC)"*, and its own meta description contains
   the typo *"Oracle Integration Cloud (OCI)"*. Catalogued as the H1 form.
7. **OCI API Gateway.** `oracle.com`'s page for this area is titled *"API Management"* and describes
   the older Oracle API Platform Cloud Service. The OCI service is **API Gateway** — verified against
   the OCI service docs, which is the `url` the entry carries.
8. **Two near-identical names that are different products:** *NVIDIA AI Enterprise* (NVIDIA's
   commercial software suite, sold on Oracle Marketplace) and *OCI Enterprise AI* (Oracle's agent
   platform). Both are catalogued with a `notes` warning; do not let one stand in for the other.

## Re-check cadence

Oracle's post–AI World 2025 rebrand is still landing (Autonomous Database → Autonomous AI Database,
Autonomous Data Warehouse → Autonomous AI Lakehouse, 23ai → 26ai, the GenAI pages consolidating under
OCI Enterprise AI). Treat the `fetched` date as an expiry hint: **re-verify every `name` before a
pack artifact goes to a customer or to Oracle**, and at minimum re-run the whole file quarterly.
The `verified` flag records that a name was right once — not that it still is.
