# The `products[]` entry — schema, invariants, and where each key comes from

_Long form; the runtime cards are `references/cards/entry-identity.md`, `entry-overview.md`, `entry-case-study.md`, `entry-technology.md`, `entry-jumpstart.md`, `insert.md` and `switches.md`._

> **Case.** Every string below is stored in **sentence case**. The site's live
> theme (2026-09-18 rebrand) sets display type in sentence case and uppercases
> only micro-type slots (`.eyebrow`, `.hero-badges li`, chips, buttons) in CSS,
> so a stored capital is a shout that cannot be undone. `site/data/content-case.js`
> exists only to re-case strings written *before* that rebrand — never add to it.

The listing skill writes **one entry** of `window.SITE_CONTENT.products[]` in a
practice site's `site/data/content.js`, plus the two things that travel with it:
a `window.SITE_CONFIG.products["<slug>"]` switch block in `site/data/config.js`
and a `window.SITE_DIAGRAMS["<slug>"]` figure in `site/data/diagrams.js`.

It touches nothing else. `site`, `media`, `disclaimers`, `shared`, `overview`
(the home page), `productsPage`, `facets`, `services`, `forms` and `salesKit`
are site-level and belong to whoever owns the site.

Read this with `assets/exemplar-product-entry.js` open. **The exemplar is the
spec**: when a cell already carries an example, match its altitude, length and
phrasing. The source documents are the evidence, not the template.

Every string obeys `listing-rules.md`. `tools/check-grammar.js` is the gate.

---

## 1 · Identity and tile

| Key | Type | Contract |
|---|---|---|
| `slug` | string | Route `#/products/<slug>`, and the key into `SITE_CONFIG.products`. Lowercase, hyphenated, stable forever: it is in URLs, image paths and the demo path. |
| `name` | string | The pack's one plain name. |
| `headline` | `{ accent, rest }` | The product H1, split so `accent` renders in the accent colour. Two to four words total. |
| `category` | string | One `facets.categories[].id` — the workflow pattern. |
| `categoryChip` | string | That category's display label, denormalised. Must equal `tags[0]`. |
| `facet` | string | One `facets.technology[].id` — the platform the pack runs on. |
| `oneLiner` | string | The tile description **and** the hero lead — one string on both surfaces. A product statement: what it does, for whom, with what outcome. No packaging vocabulary (the checker fails a list of phrases). Every clause traceable to a signed-off source; an unsupported clause is **dropped**, never swapped for a new claim. |
| `shortLine` | string | ≤ 12 words, ends in a period, different from `oneLiner`. The one line under the name in a catalog row. |
| `statusNote?` | string | One muted line under the hero one-liner, **only** where the pack has no package yet. One sentence. Where it is absent the availability badges say what there is, which is the correct rendering. |
| `heroLine?` / `heroCaption?` | string | One or the other, never both — a short slogan or a short line above the name, in the same slot and treatment. |
| `subLine?` | string | A second hero line where the one-liner is very short. Usually absent. |
| `badges?` | `[string]` | Small uppercase hero badges. |
| `hero.image` | `{ file, alt, focal }` | `assets/img/heroes/<name>.<jpg\|png\|webp>`. All three non-empty. |
| `tags` | `[string]` | **Exactly two, in order:** `categoryChip`, then the facet's canonical label. Facts, not toggles. A third entry is a build failure — engine specifics (a solver, a retrieval engine) read as part of the platform name and belong on the Technology tab. No availability string here. |
| `tile.outcomes` | `[string]` | Exactly three outcome bullets. |

**One hero shape on every product.** Slots render in a fixed order; an unset one
does not render: breadcrumb → `heroLine`/`heroCaption` → `headline` → chip row
(pattern and platform chips left, availability badges right) → `oneLiner` →
`statusNote` → `subLine` → `badges` → CTA row. **The CTA row is always last.**

---

## 2 · `overview`

The tab is two columns on desktop (MAIN + a side rail) and one on mobile.
**Every product fills every slot**; none of these keys is optional. A slot with
no fact behind it is filled with a *qualitative* instance — a `null`-valued
metric tile, a `cross-industry` chip, a `Scoped per engagement` price. It is
never left out and it never renders an apology.

| Key | Type | Contract |
|---|---|---|
| `problemSolution` | `{ problem: {title,text,icon}, solution: {title,text,icon} }` | The paired two-panel strip, first block on the tab. `text` 1–2 sentences per panel. `icon` is an icon-registry key. |
| `metrics` | `[{ value, label, qualifier, icon }]` | 1–4 stat tiles; four is the designed shape. `value` is a string ≤ 20 chars **or `null`** — a `null` is a qualitative tile that keeps the row level. `qualifier` is the baseline or caveat, ≤ 14 words. |
| `metricsNote` | string | **Mandatory.** One footnote under the metric row, carrying the disclaimer that travels with the figures. Where nothing is published it says **what the proof of value measures**, leading with the measure. A note opening on an absence is a build failure. |
| `roi` | `{ icon, text }` | One callout band, 1–2 sentences. |
| `features` | `[string]` | 6–8 items, each ≤ 12 words. Not a block of their own: each belongs to exactly one `steps[]` entry. |
| `featuresNote?` | string | One asterisked caveat, rendered at the end of the disclosure. Use it for partial coverage. |
| `featuresDetail` | `[{ title, body }]` | ≥ 6. The long-form feature list, inside the More-detail disclosure, so no fact is lost. |
| `industriesNote` | string | One line closing the industry tabs: who this is for, beyond the tabs. |
| `scope` | `{ in: [string], out: [string] }` | ≥ 4 items each, ≤ 14 words each. The customization boundary. |
| `steps` | `[{ n, title, text, image, features }]` | **3–5**, the How-it-works stepper. `n === index + 1`. `text` ≤ 30 words. `image` is `assets/img/steps/<slug>-<n>.<ext>`. `features` holds the **exact strings** from `overview.features` belonging to this step: the union across steps must equal `features`, no bullet twice, none missing. |
| `industryCases` | `[{ industry, label, image, problem, solution }]` | **3–6**, the industry tab component. `industry` is one of the fixed 16 keys (§5) and unique. `label` must equal `shared.industryLabels[industry]`. `image` is `assets/img/industries/<key>.<ext>` — shared across products. `problem` and `solution` are 2–3 sentences each, specific to that industry **and** this pack; a paragraph that would read the same under any tab is the failure mode. |
| `moreDetail` | `[{ title, body }]` | ≥ 3. The collapsible disclosure: today/tomorrow, the pattern, scope boundaries, roadmap notes, evaluation disclaimers. An entry repeating a vertical the tabs already cover does not belong — one telling per vertical. |
| `caseStudy` | object **or `null`** | See §3. The key is always present; `null` renders nothing. There is no empty state. |

**Absent by construction** — the checker fails if any returns:
`overview.sideFacts`, `overview.industries`, `overview.successStory`, and a
top-level `pov`.

**The metrics heading follows the data.** With at least one `value`, the block
is headed "metrics improved"; with every tile qualitative it is headed "what the
proof of value measures" instead. A heading asserting improvement over four
numberless tiles contradicts itself two lines later.

---

## 3 · `overview.caseStudy`

No customer is named and no logo is rendered. Each case identifies its customer
by an **anonymized descriptor** — industry and scale — and an **industry
medallion** where a logo would be.

| Key | Contract |
|---|---|
| `descriptor` | Industry and scale, no name, no country, nothing that narrows to one company. The callout's title. |
| `area` | The operational area, one short line. |
| `industry` | One of the fixed 16 keys; picks the medallion. |
| `status` | `measured` \| `modeled` \| `in-preparation` → the chip. **The only place the status word is set.** |
| `metrics` | **1–2** big figures, `value` ≤ 20 chars. Where no figure is published, a short qualitative **outcome** statement — never an invented number and never a restatement of the mechanic. Neither may repeat a side-rail tile. |
| `story` | 2–3 sentences: what was done, on what data, with which stack, **closing with the caveat that qualifies the figures**. The checker fails a story with no caveat clause. The caveat agrees with the status in the chip's own plain words, and never states the negation. |
| `scope` | **Exactly 3** `{ label, value }` facts the rest of the card does not carry. **No contract value, no contract duration, no headcount, no money figure.** |
| `ndaLine` | The footer line. A case in preparation does not offer a reference call about results that do not exist yet. |
| `downloadLabel` | Renders only when `SITE_CONFIG.products[slug].successStoryUrl` is non-empty. |

`customer`, `logo`, `logoStacked`, `image` and `metricsEyebrow` are **removed**
and are build failures if they return.

---

## 4 · `technology`

**Exactly two blocks:** `narrative` + `stack` under *Architecture*, then
`capabilities` under *Capabilities*. Architecture and capability are different
objects and never share a container; "how it runs" never gets a block of its own.

| Key | Contract |
|---|---|
| `narrative` | Two short sentences, ~40 words max, at the head of the Architecture block. |
| `stack` | **4–5 layers**, top → bottom, keys a subsequence of `application` → `ai-engine` → `data-platform` → `infrastructure` → `custom`. `application`, `data-platform`, `infrastructure` and `custom` are always present; a layer may be omitted but never re-ordered. `summary` is **one sentence** (the collapsed row). `vendors` is a non-empty array of the vendor ids and picks the wordmarks. `items` is `[{ name, required, note?, direction? }]`; `required` is a real boolean rendering as **Required / Optional**, and every layer carries ≥ 1 `required: true`. `note` is a short second chip, never package-ladder vocabulary. `direction` (`inbound`/`outbound`/`both`) is legal **only** on `custom`, and that layer always names at least one of each. |
| `governance?` | `{ title, body }` — one band below the accordion, where the platform needs one. |
| `capabilities` | **Exactly four** `{ stage, items: [{ name, state? }] }` groups, stages unique, in workflow order, named in the pack's own vocabulary — **the same four stages `overview.steps` walks**. ≥ 3 items each. Together they must cover every feature the page claims anywhere. `state` is `supported` / `partial` / `roadmap` and is **omitted** unless a real capability matrix states one: a guessed tag is worse than no tag. |

`groups`, `layers`, `integration`, `notUsed`, `flow` and `security` are gone and
are build failures if they return.

---

## 5 · `jumpstart`

One screen, identical shape on every product: fast · low-risk · tangible.
**The block sells one idea** — pilot this pack fast, at low risk, with tangible
output — and every element serves it.

| Key | Contract |
|---|---|
| `title` | Always `Jumpstart Proof-of-Value`. |
| `promise` | One line: pilot *this pack* on your own data, in *this* duration, at *this* price, and take away *this* result. Only a duration or price the evidence supports; otherwise the sentence says the scope is agreed at scoping. The product noun is lowercase mid-sentence. **The closing clause is written per pack** — a catalog of lines ending on the same six words is the template tell a seller sees the moment they flip between two tabs live. |
| `durationShort?` | The proof-of-value duration, stated identically everywhere on the site; the checker fails any other duration anywhere in the data. |
| `pillars` | **Exactly 3, in order:** `fast` (kickoff to result), `low-risk` (fixed scope and price, your tenancy, no production change — only the claims the evidence supports), `tangible` (the headline outcome). |
| `outcomes` | 3–4 **customer outcomes**, not deliverables: "an optimized four-week plan for one region, measured against your current plan", not "a plan document". |
| `timeline` | 3–4 `{ label, text }` week-by-week nodes. Node 1 is the pre-flight gate where the pack has one. |
| `needs` | **Exactly 3** short asks — data access, a business owner, sample material. |
| `investment` | `{ price, duration, includes ≥ 3, footnote }`. `price` and `duration` are each a string **or `null`**. Where **both** are null the card prints one scoped-in-scoping line and no footnote; where one is known it prints what it has. `footnote` is **one line**, never a stack of disclaimers. |
| `next` | **Exactly 2**, `Integration` then `Scale`, one line each, with duration and price where a signed-off source states them and `Scoped per engagement` where it does not. |
| `cta` | `{ label, route }` routed at `#/products/<slug>/contacts`. |

Packaging-internal disclaimers ("framed scope", "flexible add-ons", "beyond the
frame", "set by specific constraints") describe how a quote is built, not what a
customer gets. The checker fails them.

---

## 6 · `sellers`

Not rendered — this block is the **kit manifest**: what whoever sends the kit
puts in it. `materials` is `[{ key, title, description, state }]`, one row per
asset; `key` is the lookup into `SITE_CONFIG.products[slug].materials`.

Anything in `content.js` is one view-source away from a customer. No seller
notes, no internal file names, no internal paths.

---

## 7 · The `config.js` switch block

`SITE_CONFIG.products["<slug>"]` — every key must exist; an **empty string means
the control does not render**, which is how absence stays an empty container
rather than a dead button.

| Key | Contract |
|---|---|
| `marketplace` | Real boolean. Drives the availability badge. |
| `marketplaceUrl` | The listing URL. A URL set while `marketplace` is `false` is a build failure. |
| `demoUrl` | The canonical relative path to the walkthrough, e.g. `demo/<slug>/index.html`. Keep it canonical for the real deployment even while previewing. |
| `demoPreviewUrl` | Where the demo actually opens **while previewing**. A hosted-preview platform that serves a page as a supporting file cannot open it as a top-level page, so the demo is published standalone and linked by its own URL. **A runner input, never a repo constant.** |
| `video` / `videoUrl` / `videoPoster` | The demo-video switches; `videoPoster` must exist as a key even when empty. |
| `successStoryUrl` | Gates the case-study download link. |
| `materials` | `{ <key>: <url> }` for each `sellers.materials[].key`. |

Site-level in the same file: `productOrder` — catalog order is **owner-controlled
data, never derived**. A new slug joins the end; the owner moves it.

---

## 8 · The `diagrams.js` figure

`SITE_DIAGRAMS["<slug>"]` — the architecture figure on the Technology tab.
Two layouts:

- `layout: "flow"` — `sources[]` → a `group` (the compute boundary, with `nodes[]`) → a `target`, plus `note` or `loop`.
- `layout: "hub"` — a `hub` with `title` and `items[]`, fed by `sources[]`.

Titles and subs are **arrays of lines**, because the renderer sets each entry as
its own line rather than wrapping. The `target` is always the human gate; `note`
or `loop` states the one invariant that keeps the workflow honest.

---

## 9 · Invariants a renderer relies on

These hold for every entry, and `tools/check-grammar.js` asserts them.

- Every `slug` has a matching key in `SITE_CONFIG.products`.
- `facet` is one of the site's technology facet ids; `category` one of its category ids.
- `tags.length === 2`, `tags[0] === categoryChip`, `tags[1] ===` the facet's label. **No surface names a platform in any other words.**
- `tile.outcomes.length === 3`.
- 1–4 `metrics` **plus** `metricsNote`; 6–8 `features`; 3–5 `steps` covering every feature exactly once; 3–6 `industryCases`; `scope.in`/`.out` ≥ 4; `moreDetail` ≥ 3; `featuresDetail` ≥ 6.
- `caseStudy` present as an object or `null`.
- `stack` 4–5 layers, each with ≥ 1 required item; `capabilities` exactly 4 stages, ≥ 3 items each.
- `jumpstart.pillars` is `fast` → `low-risk` → `tangible`; `jumpstart.next.length === 2`, Integration → Scale.
- `oneLiner` carries no packaging phrase; `shortLine` ≤ 12 words, ends in a period, differs from `oneLiner`.
- **No customer name anywhere in the file**, and no reference to a logo path.
- **No surface states a total, a denominator or a gap** — never the size of the catalog, never what is missing.
- A missing **image file** is a warning, not a failure: copy and imagery ship on separate tracks.

---

## 10 · Where each key comes from — the pack-spec map

The spec (`shared/schema/pack-spec.md`) is the single source. A builder that
finds a required key missing **stops and sends the user back to the spec skill**
rather than filling the gap itself.

| Listing key | Spec source | Component | How |
|---|---|---|---|
| `slug` | `meta.slug` | 4 | verbatim |
| `name`, `headline` | `meta.name_variants.site` | 4 | split into `{accent, rest}` |
| `oneLiner` / `shortLine` | `one_liner.full` / `one_liner.short` | 2 | verbatim; re-checked against the packaging deny-list |
| `category`, `categoryChip` | `meta.roadmap_block` + the workflow pattern | — | **choice**: map the pack's pattern onto the site's own category taxonomy |
| `facet`, `tags[1]` | `oracle_products[]` where `role: required` | 9 | the platform those required products belong to, named in the vendor's own words |
| `hero.image` | — | — | **an input**, not a derivation: imagery comes from the company's own corpus, never the web |
| `tile.outcomes[3]` | `kpis[]` + `problem_solution.solution` | 11, 1 | three outcomes in the reader's words |
| `overview.problemSolution` | `problem_solution` | 1 | `reframe` heads the solution panel |
| `overview.metrics` + `metricsNote` | `kpis[]`, `figures` | 11 | `value` ← `figure`; `qualifier` ← `baseline`; `metricsNote` ← `caveat` + the channel's attribution rule. `figure_status` decides whether a figure may appear at all |
| `overview.roi` | `kpis[]` + `problem_solution` | 11, 1 | one band, no new claim |
| `overview.features` / `featuresDetail` / `featuresNote` | `capabilities[].categories[].features[]` | 6 | short form ≤ 12 words; long form verbatim; `status: partial` becomes the asterisked caveat |
| `overview.steps` | `workflow.steps[]` | 7 | 3–5 steps; the human-in-the-loop step is never merged away; `image` ← a demo capture frame |
| `overview.industryCases` | `verticals[]` | 5 | `problem`/`solution` ← `verticals[].framing`; `industry` mapped onto the fixed 16-key set |
| `overview.industriesNote` | `icp.line` | 3 | **the only place ICP reaches the listing today** — see §11 |
| `overview.scope.in/.out` | `capabilities[].customization_scope_area` + the PoV tier's `scope_in`/`scope_out` | 6, 12 | the customization boundary |
| `overview.moreDetail` | `verticals[].what_matters_here`, `meta.source_engagement.divergence_from_pack` | 5, — | say where the pack differs from the delivered scope |
| `overview.caseStudy` | `meta.source_engagement` + `clearance` + `kpis[]` | — | `descriptor` ← `clearance.anonymized_descriptor`; `status` ← `kpis[].figure_status`; the card renders **only** if `clearance.customer_name_allowed.customer_site` logic permits an anonymized telling, else `null` |
| `technology.narrative` | `architecture` | 8 | two sentences |
| `technology.stack[]` | `architecture.stack[]` | 8 | the vendor ladder, top to bottom |
| `stack[].items[].required` | `oracle_products[].role` | 9, 10 | `required` / `optional` as a per-item boolean inside one accordion |
| `technology.capabilities[]` | `capabilities[]` | 6 | **a derived view** — see §12 |
| `jumpstart.promise` / `pillars` / `outcomes` / `timeline` / `needs` | `packages.tiers[pov]` | 12 | outcomes, not deliverables |
| `jumpstart.investment` | `packages.tiers[pov].services_price` + `duration_weeks` | 12 | **only the PoV price ships** |
| `jumpstart.next[]` | `packages.tiers[integration]`, `[scaling]` | 12 | text only; `Scoped per engagement` where no price is published |
| `jumpstart.durationShort` | `packages.tiers[pov].duration_weeks` | 12 | one duration, everywhere |
| `sellers.materials[]` | the pack's artifact set | — | the manifest, never rendered as a list to a reader |
| `SITE_DIAGRAMS[slug]` | `architecture` | 8 | inputs → compute boundary → human gate |
| `config.*` | — | — | **runner inputs**: URLs, posters, kit links |

**Deliberately omitted from the listing**, relative to the full spec: customer
names and logos; prices beyond the PoV; the per-capability S/M/L handling matrix
(`packages.capability_handling`); counts and denominators; roadmap and gap
statements; internal taxonomy names; uncleared time-to-deliver claims; the
materials inventory (requested, never listed); `contacts.partner_print` and
`contacts.internal`; `provenance`; `open_questions`.

---

## 11 · Proposal: an `icp` key — **needs a checker assertion**

**The gap.** The pack spec makes target ICP a first-order component (3), signed
off before the name. The listing has **no dedicated field for it**. Today it is
approximated by `overview.industriesNote`, a one-line closer under the industry
tabs — which answers "who else is this for" but not "who is this for".

**Proposal.**

```js
icp: {
  line: "Field-service operations leaders at companies running <platform> with 200+ technicians",
  buyerRoles: ["VP Field Service", "COO"]   // optional, ≤ 3
}
```

- `icp.line` — one sentence: who, at what kind of company, with what pain. ≤ 25 words. No counts of the catalog, no packaging vocabulary, no customer name.
- Renders in the Overview side rail above the metrics, or as the lead of the industry tab block; **the site owner decides where**, because a new rendered slot is a design decision, not a schema one.
- `industriesNote` stays: it closes the tabs. `icp.line` opens the question.

**Checker assertions to add with it** (none exist yet — this proposal is not
enforced until they do):

1. `icp` present on every product, `icp.line` a non-empty string ≤ 25 words, one sentence.
2. `icp.line` carries no packaging phrase (reuse the `oneLiner` deny-list) and no customer name (reuse the deny-list).
3. `icp.line !== oneLiner` and `icp.line !== industriesNote` — three fields saying one thing is three places to drift.
4. `icp.buyerRoles`, where present, is 1–3 non-empty strings.

**Until those assertions exist, treat this section as a proposal**: write
`icp.line` into the spec, carry it into `industriesNote` on the listing, and
raise the new key with the site owner rather than shipping an unenforced field.

---

## 12 · The derived-view rule (the one real transformation)

`technology.capabilities[]` is **not a copy** of the spec's `capabilities[]`.

- The spec owns capabilities as **Area > Category > Feature** — how a feature list and a capability matrix are read: by subject.
- The listing owns them as **four workflow stages** — how a buyer reads them: in the order the work happens, and the same order the How-it-works stepper walks.

They are two views of one set, joined by a **per-pack mapping**: `stage` on each
`capabilities[]` area in the spec. The same capability sits at a different stage
in a document pipeline and in an optimizer, so the mapping is a pack decision
and lives in the spec, not in the tool.

`tools/derive-stage-view.py` applies it: every feature lands in exactly one
stage, a feature with no home is **reported, never dropped**, and the four-stage
and three-item-minimum invariants are checked before the output is used. Where
an area has no `stage`, the tool asks — and refuses to guess when there is no
terminal to ask in.

Status mapping, spec → listing: `available` → no `state` key · `partial` →
`state: "partial"` · `roadmap` → `state: "roadmap"`. `supported` is emitted only
where a real capability matrix backs it.

---

## 13 · The fixed industry set

Sixteen keys; **no product may invent a seventeenth**. A new industry is added
to the site's own set, with its icon, before any product references it.

`manufacturing` · `logistics` · `utilities` · `telecom` · `healthcare` ·
`financial-services` · `insurance` · `retail` · `energy` · `public-sector` ·
`automotive` · `life-sciences` · `professional-services` · `construction` ·
`travel-transport` · `cross-industry`

`cross-industry` is reserved: it means "no vertical list exists because the
constraint is the system landscape, not the sector", and it always ships with an
`industriesNote` that says so.
