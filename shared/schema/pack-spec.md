# Pack spec — schema and template

One Markdown file per pack, at `packs/<slug>/pack-spec.md` in the packaging-skills repo — committed and shared, so every colleague builds from the same spec; `shared/tools/pack_paths.py <slug>` finds the checkout (`--repo`, else `$ORACLE_PACKS_ROOT`, else the working directory). Beside it live only the architecture model (`architecture.json`) and the pictures the spec names (`visuals/`). Everything else a pack produces — the artifacts, the intake, the inventory and its extracts, the sources, the research, the decisions log — lives in the local work folder, `$ORACLE_PACKS_OUT/<slug>/`, else `~/oracle-packs/<slug>/`, and never enters the repo. The spec is the single source of truth: every artifact skill reads its values from here and never re-derives them. Values are confirmed by the user through `/oracle-packs:spec`; a build skill that finds a required key missing stops and sends the user back to the spec skill instead of filling the gap itself.

Conventions: every fact carries a `source` (file, call, URL, or `user:<date>` for something the user typed) so the linter can trace it. The four first-order components carry theirs on a fixed key — `problem_solution.source`, `one_liner.source`, `icp.source` and, because the name lives inside `meta`, `meta.name_source` — and the linter reads exactly those. Money in the currency written on the source artifact. Durations in weeks. `status` values are the ones listed; free text goes in `note`.

## Reading and writing the file

- **One loader.** Every tool reads the spec through `shared/tools/packspec.py`: `load(path)` returns the spec's data — the key paths on this page are what the builders and the linter read — and the line each key was written on, for findings.
- **Writes go through the writer.** `shared/tools/py shared/tools/packspec.py set <spec> <key.path> <value> [--source <src>]` sets one value and re-renders the whole file in its canonical form; the first `set` on a path where no spec exists yet creates it. The value is JSON when it parses as JSON (a list, a record, a number), else text; a typed key also takes its own syntax (`€95K · indicative`, `6–8 weeks (target 8, hard cap 10)`, `yes`, `2026-09-24`, `a; b; c`). `--source` sets the key's sibling `source` (for `meta.name`, `meta.name_source`). `get <spec> <key.path>` prints a value as JSON; `check <spec>` names each line that does not parse or is not canonical, and each key the layout does not know; `convert <in.yaml> --out <out.md>` writes the Markdown only when the round trip is exact. The spec skill and the visuals tool never hand-edit the file.
- **People may edit it directly.** The next load validates the file and names the line of any slip — a row with a cell too many or too few, an unknown section or label, a `|` in a cell not written `\|`, a price that does not read. The next `set` re-renders it without changing its data.
- **Key paths.** `meta.name` · `packages.tiers[0].services_price` · `packages.tiers[pov].name` — a bracket holds an index, or the `id`, `name`, `area`, `layer` or `n` of a list item; a key with dots in it is quoted: `kpis["Time to act"].figure`.
- **The stamp.** Every built artifact carries `pack-spec sha256:<12 hex> commit:<short hash|uncommitted|none>` (`shared/tools/spec_stamp.py`). The sha is of the spec's canonical data — its values as sorted JSON — not of the file's bytes, so a re-render, a whitespace edit or the conversion from YAML never marks a built artifact stale; a changed value does.

## Values

| In the file | Means |
|---|---|
| text | verbatim. A backslash before punctuation is that character, as on GitHub: a `<` is always written `\<`, a `\|` sits inside a table cell, and a line that would read as structure starts with one (`\#`, `\-`). A line ending in one backslash ends in a line break. Multi-line text keeps its lines |
| `—` | null |
| `(none)` | an empty list |
| an empty cell | the key is absent |
| `yes` · `no` | a boolean, where the layout types the key as one |
| `` `…` `` | one code span holding a YAML value — for what a slot's own syntax cannot say: the number 26 in a text field, trailing spaces, a date kept as text |
| `a; b; c` | a short list, on a key line or in a cell; a longer one is nested bullets |
| `€90K · indicative · <footnote>` | a price, `{value, currency, status, footnote}`; `€300K–€500K · indicative` is a range (`range: [300000, 500000]`); `to be defined [· <footnote>]` is status `tbd` |
| `6–8 weeks (target 8, hard cap 10)` | a duration, `{min, max, target, hard_cap, status, justification}`; `to be defined` is status `tbd` |
| `2026-09-24` | a date, where the layout types the key as one |

A list of records is a table while every record fits one row — at most 8 columns, a cell up to 220 characters, a list in a cell up to 160 — and one heading per record, its keys as a list, when one does not. The Oracle products and the features are always one table. A key the layout does not know is kept: a table grows a column for it; anywhere else it goes to the fenced YAML block under `## Other fields`, and `packspec.py check` and the linter (SPEC024) name it.

## The template

Every section in its canonical place and every key the layout knows, with `<placeholders>`. In a real file the writer puts a backslash before each `<` (`\<practice-drive>`); the template leaves it out for reading. Where a record type repeats — a picture, a contact, an input or output row, a price — each of its keys appears in one of its places. A key is written only when it has a value, and a section with nothing in it is left out.

```markdown
---
slug: <slug>
status: draft
spec_version: 1
generated_with: { roadmap_version: 2026-09-24, catalog_version: 2026-09-24 }
roadmap_item_id: <roadmap item id>
roadmap_block: <roadmap block>
---

# <Pack name>

- **Site:** <name on the site>
- **Internal slide:** <name on internal slides>
- **External:** <name on the one-pager and the deck>
- **External subheading:** <subheading under it>
- **Note:** <note>
- **Source:** <source>
- **Source of the name:** user:<date>
- **Eyebrow:** Oracle AI & Data Solutions
- **Roadmap note:** <note on the roadmap mapping>

## One-liner

- **Full:** <the job and the outcome, in the buyer's words>
- **Short:** <the same, rep-sayable in one breath>
- **Banned words checked:** yes
- **KPI chips:**
  - **<metric>:** ↑
- **Note:** <note>
- **Source:** user:<date>

## Problem and solution

### Problem

<a named role, and the situation they would describe in their own words>

### Solution

<what that person does instead, with the pack>

- **Problem points:**
  - **<short label>:** <one sub-problem>
- **Sub-problems:**
  - **<short label>:** <one sub-problem, longer>
- **Outcome chips:** <outcome> ↑; <outcome> ↓
- **Outcomes:** <outcome>; <outcome>
- **Reframe:** <the job reframe, used as a headline>
- **Reframe question:** <the reframe as a question>
- **Today:** <how the work is done today>
- **Tomorrow:** <how it is done with the pack>
- **Note:** <note>
- **Source:** user:<date>

## Who buys it

<who buys it, in one line>

- **Buyer roles:** <role>; <role>
- **Buyer roles, operator:** <role that runs it>
- **Buyer roles, payer:** <role that pays>
- **Buyer by industry:**
  - **<industry>:** <buyer there>
- **Qualifying signals:** <signal>; <signal>
- **Disqualifiers:** <disqualifier>
- **Dual-buyer rule:** <when two buyers are needed>
- **Why both:** <why both>
- **Note:** <note>
- **Source:** user:<date>

## Industries

### <Industry>

- **Site label:** <short label on the site>
- **Framing:**
  - **Problem:** <the problem in this industry>
  - **Solution:** <the solution in this industry>
  - **Entities:** <the things the pack works on here>
- **Catalog type:** <offering | lever>
- **Status:** proven | plausible | roadmap
- **What matters here:** <what matters here>
- **Worked example:** <a worked example>
- **How the entities differ:** <how the entities differ from the delivered case>
- **Note:** <note>
- **Scope note:** <scope note>
- **Tier note:** <tier note>
- **Icon:**
  - **File:** visuals/<icon>-ink.png
  - **File, white:** visuals/<icon>-white.png
  - **Name:** <icon name>
  - **Source:** <library>
  - **Licence:** <licence>
- **Source:** <source>

### Held out

- **Note:** <why these wait>
- **Candidates:** <industry>; <industry>

### Rejected

| Name | Reason |
|---|---|
| <industry> | <why not> |

## Capabilities

### <Capability area>

- **Stage:** <stage on the site>
- **Customization in this area:** <how the area is customized per customer>

| Category | Feature | Status | From tier | Customization | Specificity | Note | Footnote marker | Oracle product | Source |
|---|---|---|---|---|---|---|---|---|---|
| <Category> | <Feature> | available | pov | <customization> | customer; engine | <caveat, becomes a footnote> | 1 | <catalog id> | <source> |
| <Another category> | <Feature> | roadmap | integration |  |  |  |  |  | <source> |

| Category | Note |
|---|---|
| <Category> | <note on the category> |

## Workflow

### Inputs

| System | Detail | Data | Tier | Note |
|---|---|---|---|---|
| <system> | <qualifier> | <what it carries> | <how, per tier> | <note> |

### 1. <Step name>

- **Actor:** system | human | ai
- **Human in the loop:** no
- **Covers:** <the mechanics inside this step>
- **Description:** <what happens>
- **If it fails:** <what happens when it fails>
- **Vertical differences:**
  - **<Industry>:** <how this step differs there>
- **Source:** <source>

### Outputs

| System | Data |
|---|---|
| <system> | <what it receives> |

### Notes

- **Grouping note:** <why the steps are grouped this way>
- **Domain steps note:** <note>
- **Not ours:**
  - **<step>:** <why it is not the pack's>
- **Integration by tier:**
  - **PoV:** <files>
  - **Integration:** <API>
  - **Scaling:** <live>
- **Source:** <source>

## Architecture

### Inputs

| System | Data |
|---|---|
| <source system> | <what it carries> |

### Stack, top to bottom

| Layer | Name | Vendor | Items | Summary | Label | Catalog id | Note |
|---|---|---|---|---|---|---|---|
| <Layer> | <box name> | <vendor> | <item>; <item> | <one line> | <label> | <catalog id> | <note> |

### Outputs

| System | Data |
|---|---|
| <destination system> | <what it receives> |

### Notes

- **Note:** <note>
- **Platform overlap note:** <note>
- **Source:** <source>

## Oracle products

| Id | Name | Role | Why | At PoV | At Integration | At Scaling | Note | Name note | Catalog note | Inferred | Source |
|---|---|---|---|---|---|---|---|---|---|---|---|
| <catalog id> | <name> | required | <why the pack needs it> | <files> | <API> | <live> | <note> | <note> | <note> | no | <source> |

## Metrics

- **Kpis note:** <note on the metric set>

### <Metric>

- **Kind:** business | leading | technical
- **Signed off by:** <buyer-side role who signs it off>
- **One-pager label:** <label on the one-pager>
- **Chip:** <chip text>
- **Chip label:** <chip label>
- **Label:** <label>
- **Direction:** ↑
- **Formula:** <how it is measured>
- **Baseline:** <today's value>
- **Figure:** <the cleared figure, or ->
- **Figure prefix:** <prefix>
- **Figure suffix:** <suffix>
- **Figure status:** pov_result | delivered_result | target | modeled
- **Show baseline:** yes
- **Unit cost:** <unit cost>
- **Whose metric:** <whose>
- **Attribution:**
  - **Named when allowed:** <with the customer's name>
  - **Otherwise:** <with the anonymized descriptor>
- **Caveat:** <caveat>
- **Channels:** internal; partner_print
- **Note:** <note>
- **Source:** <source>

## Packages

- **Status:** <status>
- **Anchor line:** <the Oracle anchor, in one line>
- **Tier vocabulary note:** <note>
- **Tier semantics:** <note>
- **Legend:** ◐ partial · ● included · ●● advanced · — not included
- **Value for Oracle and NVIDIA:** <the proof slide's VALUE FOR ORACLE + NVIDIA>
- **Value for the client:** <the proof slide's VALUE FOR CLIENT>
- **Target OCI consumption:** <the OCI consumption the pack drives>
- **Source:** <source>

### PoV Jumpstart · S

- **Id:** pov
- **Scope:** <the tier in one line>
- **Duration:** 4–8 weeks (target 6, hard cap 10)
- **Duration label:** <label>
- **Duration note:** <note>
- **Services price:** €90K · indicative · <footnote>
- **Infrastructure price per month:** €2K · indicative
- **What you get:** <deliverable>; <deliverable>
- **Entry gate:** <what the customer brings>
- **In scope:** <in scope>
- **Out of scope:** <out of scope>
- **Show size tag:** no
- **Name note:** <note>
- **Source:** <source>

### Integration · M

- **Id:** integration
- **Duration:** 12–20 weeks
- **Services price:** €300K–€500K · indicative

### Scaling · L

- **Id:** scaling
- **Duration:** to be defined
- **Services price:** to be defined · <footnote>

### How each capability area is handled per tier

| Area | Feature areas | PoV | Integration | Scaling | Level at PoV | Level at Integration | Level at Scaling |
|---|---|---|---|---|---|---|---|
| <Commercial row> | <Capability area> | <at PoV> | <at Integration> | <at Scaling> | partial | included | advanced |

### Why it sells for the partner

- <reason>
- **<label>:** <reason>

### What each buyer gets

- **Operator:** <what the operator gets>
- **Payer:** <what the payer gets>

## Proof

- **Customer:** <the delivery customer's name>
- **Context:** <{Customer}'s situation before the engagement>
- **Delivered:** <what was delivered at {customer}, on what data, when>
- **Divergence from the pack:** <how the pack differs from the delivery — internal>
- **Divergence line:** <the same, in one print-ready sentence>
- **Source:** <source>
- **Proof headline:** <proof headline, {customer} where the name goes>
- **Vertical case:** <the vertical case>
- **Proof story:** <the proof story, {Customer} where the name goes>
- **Proof story, anonymized:** <the same, anonymized>

## Next steps

1. **<next step>:** <detail>
2. <next step>

## Open questions

### <id>

- **Question:** <the question>
- **Why:** <why it matters>
- **Blocks:** <what it blocks>

## Settings

### Clearance

| Channel | Customer may be named |
|---|---|
| Internal | yes |
| Partner print | no |
| Customer site | no |
| Demo | no |

- **Anonymized descriptor:** <a global home-appliance manufacturer>
- **Descriptor warning:** <warning>
- **Internal-only facts:** <fact>; <fact>
- **Forbidden strings:** <string>
- **Disclaimer:** <disclaimer>
- **Approvals:** <who approved what, when>
- **Source:** <source>

### Contacts

- **Partner print:**
  - **Name:** <alliances contact>
  - **Title:** <their title>
  - **Organization:** <organization>
  - **Email:** <address>
- **Site:**
  - **Mailbox:** <practice mailbox>
  - **Named:** <alliances contact>
- **Internal:**
  - **Name:** <person doing the packaging>
  - **Email:** <address>
  - **Status:** <status>
  - **Note:** <note>
- **Source:** <source>

### Deck

- **Running header:** Oracle AI & Data Solutions
- **Seller lead:** <seller lead>
- **Cta:** <call to action>
- **Anchor line:** <anchor line>
- **Layers subtitle:** <subtitle of the layers slide>
- **Architecture subtitle:** <subtitle of the architecture slide>
- **Source:** <source>
- **Images:**
  - **Customer logo:**
    - **File:** visuals/<logo>.png
    - **Source:** <where the owner's file came from>
    - **Note:** <note>
  - **Cover:**
    - **File:** visuals/<file>.jpg
    - **Source:** <library>
    - **Creator:** <creator>
    - **Licence:** <licence>
    - **Source URL:** <page URL>
  - **Today:**
    - **File:** visuals/<file>.jpg
    - **Source:** <library>
    - **Creator:** <creator>
    - **Licence:** <licence>
    - **Source URL:** <page URL>
  - **Tomorrow:**
    - **File:** visuals/<file>.jpg
    - **Source:** <library>
    - **Creator:** <creator>
    - **Licence:** <licence>
    - **Source URL:** <page URL>

### One-pager

- **Eyebrow:** Oracle AI & Data Solutions
- **Reframe:** <reframe>
- **Sub:** short
- **Data-flow notes:** no
- **Tier scope:**
  - **PoV:** <scope line>
  - **Integration:** <scope line>
  - **Scaling:** <scope line>
- **Cta:**
  - **Question:** <question>
  - **Answer:** <answer>
- **KPI chips:**
  - **<metric>:** ↓
- **Disclaimer:** <disclaimer>
- **Proof logo:** <logo file>
- **Proof caveat:** <caveat>
- **Problem heading:** <heading>
- **Sell heading:** <heading>
- **Verticals label:** <label>
- **Packages heading:** <heading>
- **Infrastructure row label:** <label>
- **Services row label:** <label>
- **Images:**
  - **Hero:**
    - **File:** visuals/<file>.jpg
    - **Source:** <library>
    - **Creator:** <creator>
    - **Licence:** <licence>
    - **Source URL:** <page URL>
- **Source:** <source>

### Executive summary

- **Running header:** Oracle AI & Data Solutions
- **Goal:** <goal>
- **Closing line:** <closing line>
- **Source:** <source>

### Feature list

- **Title:** <title>
- **Intro label:** <label>
- **Intro:** <intro>
- **Source:** <source>

### Provenance

- **Inputs:**
  - **Id:** <source id>
    - **Path:** <where the input sits>
    - **Kind:** sow | deck | video | transcript | feature-list | call-note
    - **Read:** 2026-09-24
    - **Note:** <note>
    - **Supplies:** <component>
- **Research brief:** research-brief.md
- **Inventory:** inventory/<extract>.md
- **Research:** research/<topic>.md
- **Source:** <source>
```

## The contract, key by key

Each key is written as the label in the second column. A key not listed is not part of the layout: it is kept, and named (SPEC024).

### Front matter and the name

| Key | In the file | Contract |
|---|---|---|
| `meta.slug` | `slug:` | stable id; the folder, the listing slug and the file names |
| `meta.status` | `status:` | `draft` · `research` · `options` · `signing-off` · `confirmed` · `built` |
| `meta.spec_version` | `spec_version:` | a whole number; the feature list writes it into its file properties |
| `meta.generated_with.roadmap_version`, `.catalog_version` | `generated_with:` | the dates of the roadmap extract and the product catalog (the `generated:` / `version:` lines of `shared/data/`) the spec was checked against |
| `meta.roadmap_item_id` | `roadmap_item_id:` | from `shared/data/roadmap-items.csv`; never the row number |
| `meta.roadmap_block` | `roadmap_block:` | label only; blocks are renamed often |
| `meta.name` | `# <name>` | component 4 — one plain name |
| `meta.name_variants.site`, `.internal_slide`, `.external`, `.external_subheading` | `Site`, `Internal slide`, `External`, `External subheading` | derived by the spec skill (rule from Alex, 2026-09-18): the site's name, the internal slide's, the one-pager's and the deck's with an optional subheading |
| `meta.name_variants.note`, `.source` | `Note`, `Source` | about the variants |
| `meta.name_source` | `Source of the name` | component 4's source — `user:<date>` before `status: confirmed` |
| `meta.eyebrow` | `Eyebrow` | the family name, **Oracle AI & Data Solutions** |
| `meta.roadmap_note` | `Roadmap note` | how the pack maps onto its roadmap item when that is not one to one |

### One-liner — component 2

| Key | In the file | Contract |
|---|---|---|
| `one_liner.full` | `Full` | states the job and the outcome; never packaging vocabulary |
| `one_liner.short` | `Short` | rep-sayable in one breath |
| `one_liner.banned_words_checked` | `Banned words checked` | yes / no |
| `one_liner.kpi_chips[]` — `label`, `direction` | `KPI chips`, a `**<label>:** <direction>` line each | optional chips beside the one-liner |
| `one_liner.note`, `.source` | `Note`, `Source` | `source` is `user:<date>` before confirmation |

### Problem and solution — component 1

| Key | In the file | Contract |
|---|---|---|
| `problem_solution.problem` | the paragraph under `### Problem` | a named role and a situation they would describe in their own words |
| `problem_solution.solution` | the paragraph under `### Solution` | what that person does instead |
| `problem_solution.problem_points[]`, `.sub_problems[]` — `label`, `text` | `Problem points`, `Sub-problems` | the sub-problems the print artifacts bullet |
| `problem_solution.outcome_chips`, `.outcomes` | `Outcome chips`, `Outcomes` | lists |
| `problem_solution.reframe` | `Reframe` | the job reframe used as a headline |
| `problem_solution.reframe_question` | `Reframe question` | the reframe as a question, on the deck |
| `problem_solution.today`, `.tomorrow` | `Today`, `Tomorrow` | the work before and after |
| `problem_solution.note`, `.source` | `Note`, `Source` | `source` is `user:<date>` before confirmation |

### Who buys it — component 3

| Key | In the file | Contract |
|---|---|---|
| `icp.line` | the paragraph under `## Who buys it` | who buys it, in one line |
| `icp.buyer_roles`, `.buyer_roles_operator`, `.buyer_roles_payer` | `Buyer roles`, `Buyer roles, operator`, `Buyer roles, payer` | lists |
| `icp.buyer_by_industry` | `Buyer by industry`, a `**<industry>:** <buyer>` line each | |
| `icp.qualifying_signals`, `.disqualifiers` | `Qualifying signals`, `Disqualifiers` | lists |
| `icp.dual_buyer_rule`, `.why_both` | `Dual-buyer rule`, `Why both` | when an operator and a payer both have to buy |
| `icp.note`, `.source` | `Note`, `Source` | `source` is `user:<date>` before confirmation |

### Industries — component 5

| Key | In the file | Contract |
|---|---|---|
| `verticals[]` — `name` | `### <name>`, one per industry | |
| `site_label` | `Site label` | the short label on the site |
| `framing.problem`, `.solution`, `.entities` | `Framing` | the problem and the solution in this industry's words, and the things the pack works on there |
| `catalog_type` | `Catalog type` | what a move maps to here: `offering` · `lever` |
| `status` | `Status` | `proven` · `plausible` · `roadmap` |
| `what_matters_here`, `worked_example`, `entities_differ` | `What matters here`, `Worked example`, `How the entities differ` | |
| `note`, `scope_note`, `tier_note`, `source` | `Note`, `Scope note`, `Tier note`, `Source` | |
| `icon` — `file`, `file_white`, `name`, `source`, `licence` | `Icon` | written by `/oracle-packs:visuals` when the user picks one; paths relative to the spec's folder (`visuals/…`); absent = the deck draws an empty container |
| `verticals_held_out` — `note`, `candidates` | `### Held out` | industries considered and held for later |
| `verticals_rejected[]` — `name`, `reason` | `### Rejected` | industries considered and ruled out |

### Capabilities — component 6, area › category › feature

| Key | In the file | Contract |
|---|---|---|
| `capabilities[]` — `area` | `### <area>`, one per area | |
| `stage` | `Stage` | the area's stage on the site's stage view |
| `customization_scope_area` | `Customization in this area` | how the area is customized per customer — the packages table's summary; text, or a list |
| `categories[]` — `name`, `features[]` | the table, one row per feature, its category first | |
| feature `name` | `Feature` | |
| feature `status` | `Status` | `available` ● · `partial` ◐ · `roadmap` ○ |
| feature `tier_first_available` | `From tier` | `pov` · `integration` · `scaling` |
| feature `customization_scope` | `Customization` | |
| feature `specificity` | `Specificity` | the four-axis tag: `customer`, `engine`, `use_case`, `industry`; empty = generic |
| feature `note`, `footnote_marker` | `Note`, `Footnote marker` | a note becomes a footnote on the feature list |
| feature `oracle_product`, `source` | `Oracle product`, `Source` | a catalog id |
| `categories[].note` | the `Category · Note` table under the features | a note on a category |

### Workflow — component 7

| Key | In the file | Contract |
|---|---|---|
| `workflow.inputs[]`, `workflow.outputs[]` — `system`, `detail`, `data`, `tier`, `note` | `### Inputs`, `### Outputs` | a system, a qualifier, what it carries, how per tier |
| `workflow.steps[]` — `n`, `name` | `### <n>. <name>`, one per step | 5–7 steps (hard cap 7, min 3), grouped at the buyer's checkpoints; mechanics live inside a step (`covers`, `description`), never as steps (SPEC019) |
| step `actor` | `Actor` | `system` · `human` · `ai` |
| step `human_in_the_loop` | `Human in the loop` | yes / no |
| step `covers`, `description`, `failure_path` | `Covers`, `Description`, `If it fails` | |
| step `vertical_differences` | `Vertical differences`, a `**<industry>:** <difference>` line each | |
| step `source` | `Source` | |
| `workflow.grouping_note`, `.domain_steps_note` | `Grouping note`, `Domain steps note` under `### Notes` | |
| `workflow.not_ours[]` — `step`, `reason` | `Not ours` | steps the buyer runs, not the pack |
| `workflow.integration_tiers` — `pov`, `integration`, `scaling` | `Integration by tier` | |
| `workflow.source` | `Source` | |

### Architecture — component 8

| Key | In the file | Contract |
|---|---|---|
| `architecture.inputs[]`, `architecture.outputs[]` | `### Inputs`, `### Outputs` | the same shape as the workflow's |
| `architecture.stack[]` — `layer`, `name`, `vendor`, `items`, `summary`, `label`, `catalog_id`, `note` | `### Stack, top to bottom` — a table, or `#### <layer>` per layer | the vendor ladder, top to bottom. `catalog_id` is one id or a list: every NVIDIA component, and the platform's services, by catalog id; the platform itself is one entry in `oracle_products` (`oci`) |
| `architecture.note`, `.platform_overlap_note`, `.source` | under `### Notes` | |

### Oracle products — components 9 and 10

`oracle_products[]` holds Oracle-vendor entries only — the products an Oracle seller can put on a deal. NVIDIA components (cuOpt, NeMo, NIM, AI-Q, VSS, NVIDIA AI Enterprise) are in the catalog too, but they belong in `architecture.stack[].catalog_id`: a required / optional roll-up across packs is an Oracle-consumption question. Both places take catalog ids only, and the linter resolves both against `shared/data/oracle-products.yaml`.

| Key | In the file | Contract |
|---|---|---|
| `oracle_products[]` — `id` | `Id` | a catalog id; the catalog's canonical name (`oracle-fusion-field-service`, not "Oracle Field Service") |
| `name` | `Name` | |
| `role` | `Role` | `required` = only what the pack cannot run without (typically 1–3: the platform as one entry plus what the core executes on); `optional` = only what a buyer would plausibly connect (2–4); never a catalog sweep |
| `why` | `Why` | |
| `integration` — `pov`, `integration`, `scaling` | `At PoV`, `At Integration`, `At Scaling` | what happens with the product at each tier |
| `note`, `name_note`, `catalog_note`, `inferred`, `source` | `Note`, `Name note`, `Catalog note`, `Inferred` (yes / no), `Source` | |

### Metrics — component 11

`kind` decides where a metric may be printed, and is `business` when absent:

- **business** — what the buyer's business already tracks: money, time, volume, risk, quality, in their own words ("cost per claim", "planning cycle time"). The ONLY kind sales artifacts print on their tiles and chips: deck stat tiles and KPI chips, the one-pager's proof strip and chips, the executive summary's proof strip, the site's metrics.
- **leading** — the proxy that moves first and predicts the business metric. May print as a second line under its business metric where the layout has one; never as a tile of its own.
- **technical** — a proof-of-value acceptance criterion (precision, recall, reviewer agreement, coverage, latency). NEVER on a sales artifact. The builders route it to the PoV package's success line — "Proof accepted when: …" on the deck's packages slide, the one-pager's packages table and the executive summary's tier strip.

A metric defined and measured per engagement but with no cleared headline number has the figure `-`; it then carries no `figure_status`, `caveat` or `attribution` — there is nothing to qualify — and artifacts print "results to follow" for it.

| Key | In the file | Contract |
|---|---|---|
| `kpis_note` | `Kpis note`, above the metrics | |
| `kpis[]` — `name` | `### <name>`, one per metric | ONE metric set per pack |
| `kind` | `Kind` | `business` · `leading` · `technical` |
| `owner_role` | `Signed off by` | the buyer-side role who signs the number off; required on a business metric — the test that the metric is the business's, not ours |
| `formula`, `baseline`, `figure` | `Formula`, `Baseline`, `Figure` | |
| `figure_status` | `Figure status` | `pov_result` · `delivered_result` · `target` · `modeled` |
| `attribution` — `named_when_allowed`, `otherwise` | `Attribution` | how the figure is attributed where the customer may be named, and elsewhere |
| `caveat` | `Caveat` | |
| `one_pager_label`, `chip`, `chip_label`, `label`, `direction`, `figure_prefix`, `figure_suffix`, `show_baseline`, `unit_cost`, `whose_metric`, `channels` | `One-pager label`, `Chip`, `Chip label`, `Label`, `Direction`, `Figure prefix`, `Figure suffix`, `Show baseline` (yes / no), `Unit cost`, `Whose metric`, `Channels` | how each artifact prints it |
| `note`, `source` | `Note`, `Source` | |

### Packages — component 12

| Key | In the file | Contract |
|---|---|---|
| `packages.tiers[]` — `name`, `size_tag` | `### <name> · <size tag>`, one per tier | PoV Jumpstart / Integration / Scaling; S / M / L are size tags only |
| tier `id` | `Id` | `pov` · `integration` · `scaling` |
| tier `scope_line` | `Scope` | the tier in one line |
| tier `duration_weeks` | `Duration` | `{min, max, target, hard_cap, status, justification}`; the skill pushes back above 10 weeks with reasons |
| tier `justification`, `duration_justification` | `Justification`, `Duration justification` | older places for the PoV's reason to run past 8 weeks; the linter reads any of the three |
| tier `duration_label`, `duration_note` | `Duration label`, `Duration note` | |
| tier `services_price`, `infra_price_monthly` | `Services price`, `Infrastructure price per month` | a price; status `confirmed` · `indicative` · `tbd` |
| tier `what_you_get`, `entry_gate`, `scope_in`, `scope_out` | `What you get`, `Entry gate`, `In scope`, `Out of scope` | lists |
| tier `show_size_tag`, `name_note`, `source` | `Show size tag` (yes / no), `Name note`, `Source` | |
| `packages.capability_handling[]` — `area`, `maps_to_feature_areas`, `pov`, `integration`, `scaling` | `### How each capability area is handled per tier`: `Area`, `Feature areas`, `PoV`, `Integration`, `Scaling` | per commercial row × tier, the ◐ ● ●● cells; `Feature areas` is the bridge to the capability areas |
| `capability_handling[].levels`, `.glyphs` — `pov`, `integration`, `scaling` | `Level at …`, `Glyph at …` | the one-pager's matrix level per tier (`none` · `partial` · `included` · `advanced`), and a glyph that overrides one |
| `packages.why_it_sells_for_the_partner[]` | `### Why it sells for the partner` | the seller block on partner-facing artifacts; text, or `label` and `text` |
| `packages.what_each_buyer_gets` — `operator`, `payer` | `### What each buyer gets` | |
| `packages.anchor_line` | `Anchor line` | the Oracle anchor in one line |
| `packages.value_for_partner` | `Value for Oracle and NVIDIA` | the proof slide's VALUE FOR ORACLE + NVIDIA block; falls back to `anchor_line` |
| `packages.value_for_client` | `Value for the client` | the proof slide's VALUE FOR CLIENT block; falls back to `problem_solution.solution` |
| `packages.target_oci_consumption` | `Target OCI consumption` | per tier when known |
| `packages.capability_handling_legend` | `Legend` | |
| `packages.status`, `.tier_vocabulary_note`, `.tier_semantics`, `.source` | `Status`, `Tier vocabulary note`, `Tier semantics`, `Source` | |

### Proof, next steps, open questions

| Key | In the file | Contract |
|---|---|---|
| `meta.source_engagement.customer` | `Customer` under `## Proof` | internal-only unless `clearance.customer_name_allowed` says otherwise |
| `meta.source_engagement.context` | `Context` | optional; the proof slide's CONTEXT block |
| `meta.source_engagement.delivered` | `Delivered` | what was delivered, where, when |
| `meta.source_engagement.divergence_from_pack` | `Divergence from the pack` | the internal statement; may run to a paragraph |
| `meta.source_engagement.divergence_line` | `Divergence line` | ONE print-ready sentence — what a deck or executive-summary footnote prints. Without it the builders fall back to the long one and the fit report reports the overflow: the honest failure, not a silent truncation |
| `meta.source_engagement.source` | `Source` | |
| `deck.proof_headline`, `deck.vertical_case` | `Proof headline`, `Vertical case` | the deck's proof slide |
| `one_pager.proof_story`, `.proof_story_anonymized` | `Proof story`, `Proof story, anonymized` | the one-pager's proof strip, named and anonymized |
| `exec_summary.next_steps[]` — `title`, `detail` | `## Next steps`, numbered: `**<title>:** <detail>`, or plain text | the executive summary's next steps |
| `open_questions[]` | `## Open questions`: a bullet each, or `### <id>` each with `question`, `why`, `blocks` (`Question`, `Why`, `Blocks`); `(none)` when there is none | anything the user deferred; artifacts print nothing that depends on an open question |

`context`, `delivered`, `deck.proof_headline` and `deck.vertical_case` may carry `{customer}` / `{Customer}`: the deck fills it with what the channel may call the customer — the name where `clearance.customer_name_allowed` is yes, `clearance.anonymized_descriptor` elsewhere.

### Settings

| Key | In the file | Contract |
|---|---|---|
| `clearance.customer_name_allowed` — `internal`, `partner_print`, `customer_site`, `demo` | the `Channel · Customer may be named` table | per channel, yes / no; default no. The builders never read the customer name unless the channel allows it |
| `clearance.anonymized_descriptor` | `Anonymized descriptor` | what the customer is called where it may not be named |
| `clearance.descriptor_warning`, `.internal_only_facts`, `.forbidden_strings`, `.disclaimer` | `Descriptor warning`, `Internal-only facts`, `Forbidden strings`, `Disclaimer` | |
| `clearance.approvals`, `.source` | `Approvals`, `Source` | who approved what, when |
| `contacts.partner_print`, `.site`, `.internal` — `name`, `title`, `org`, `email`, `mailbox`, `named`, `status`, `note` | `### Contacts`: `Partner print`, `Site`, `Internal` — `Name`, `Title`, `Organization`, `Email`, `Mailbox`, `Named`, `Status`, `Note` | the three addresses: `naming-and-clearance.md` §3, "Contacts by channel" |
| `contacts.source` | `Source` | |
| `deck.running_header`, `.seller_lead`, `.cta`, `.anchor_line`, `.layers_sub`, `.architecture_sub`, `.source` | `### Deck`: `Running header`, `Seller lead`, `Cta`, `Anchor line`, `Layers subtitle`, `Architecture subtitle`, `Source` | the deck's own wording, where it differs from the defaults |
| `deck.images.customer_logo`, `.cover`, `.today`, `.tomorrow` — `file`, `file_white`, `name`, `source`, `creator`, `licence`, `source_url`, `note` | `Images`: `Customer logo`, `Cover`, `Today`, `Tomorrow` — `File`, `File, white`, `Name`, `Source`, `Creator`, `Licence`, `Source URL`, `Note` | written by `/oracle-packs:visuals`; `file` relative to the spec's folder (`visuals/…`, in the repo). A slot absent = the deck draws an empty container, never a stand-in |
| `one_pager.eyebrow`, `.reframe`, `.sub`, `.data_flow_notes`, `.disclaimer`, `.proof_logo`, `.proof_caveat` | `### One-pager`: `Eyebrow`, `Reframe`, `Sub`, `Data-flow notes` (yes / no), `Disclaimer`, `Proof logo`, `Proof caveat` | the one-pager's own wording |
| `one_pager.problem_heading`, `.sell_heading`, `.verticals_label`, `.packages_heading`, `.infra_row_label`, `.services_row_label` | `Problem heading`, `Sell heading`, `Verticals label`, `Packages heading`, `Infrastructure row label`, `Services row label` | heading overrides |
| `one_pager.tier_scope` — `pov`, `integration`, `scaling` | `Tier scope` | a scope line per tier |
| `one_pager.cta` — `question`, `answer` | `Cta` | |
| `one_pager.kpi_chips[]` — `label`, `direction` | `KPI chips` | |
| `one_pager.images.hero`, `one_pager.source` | `Images` › `Hero`, `Source` | a picture, as the deck's |
| `exec_summary.running_header`, `.goal`, `.closing_line`, `.source` | `### Executive summary`: `Running header`, `Goal`, `Closing line`, `Source` | |
| `feature_list.title`, `.intro_label`, `.intro`, `.source` | `### Feature list`: `Title`, `Intro label`, `Intro`, `Source` | |
| `provenance.inputs[]` — `id`, `path`, `kind`, `read`, `note`, `supplies` | `### Provenance` › `Inputs`: `Id`, `Path`, `Kind`, `Read` (a date), `Note`, `Supplies` | where each raw input sits (the shared drive, the work folder's `sources/`); `kind`: `sow` · `deck` · `video` · `transcript` · `feature-list` · `call-note`; the ids are the source tokens every `Source` line uses |
| `provenance.research_brief`, `.inventory`, `.research`, `.source` | `Research brief`, `Inventory`, `Research`, `Source` | relative to the pack's work folder, `$ORACLE_PACKS_OUT/<slug>/` (else `~/oracle-packs/<slug>/`); the spec lives in the repo, the files named here never enter it |

## Rules the schema enforces (checked by `shared/tools/lint_spec.py`)

- Every component key present and confirmed before `status: confirmed`; the four first-order components carry a `user:<date>` source on `problem_solution.source`, `one_liner.source`, `icp.source` and `meta.name_source`.
- `oracle_products[].id` and every `architecture.stack[].catalog_id` must exist in the catalog; a product missing from the catalog is a catalog change request, not a free-text entry.
- `oracle_products[]` is Oracle-vendor only. A catalog entry whose `vendor` is NVIDIA belongs in `architecture.stack[].catalog_id`.
- `packages.tiers[pov].duration_weeks.max` ≤ 8 by default; anything above 8 needs a `justification`; above 10 is rejected.
- `kpis` is one set; the same metric may not appear twice with different figures. A figure of `-` means "measured per engagement, no cleared number" and is read as absent.
- `kpis[].kind` is `business`, `leading` or `technical` (`business` when absent). A set with no business metric, and a metric whose name reads as a proof criterion or a vanity count without `kind: technical`, are warnings (SPEC025, SPEC026); a business metric with no `owner_role` is a warning too (SPEC027). Sales artifacts print `kind != technical`; technical criteria are routed to the PoV package's success line.
- No retired family name — "OCI AI Accelerator(s)", "OCI accelerator(s)" — in `meta.eyebrow`, `deck.running_header`, `exec_summary.running_header` or `one_pager.eyebrow`. The family name on every print artifact is **Oracle AI & Data Solutions** (SPEC028).
- `clearance.customer_name_allowed` decides attribution per channel; the builders never read the customer name unless the channel allows it.
- No customer name inside `one_liner`, `problem_solution`, `verticals`, or `name`.
- A key the layout does not know, in any record list, is a warning naming it (SPEC024); a spec that does not parse is a finding on its line (SPEC029).
