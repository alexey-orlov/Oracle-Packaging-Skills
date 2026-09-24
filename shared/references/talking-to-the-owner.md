# Talking to the owner — the reader's test for every message, question and option

_How every skill in this bundle speaks to the person it works for. **Long form; the runtime card is `plugins/oracle-packs/skills/spec/references/cards/owner-language.md`** (the web plugin's skills carry their own copy), which is what a skill loads at start-up. Read this file only when the card leaves a case open. Rewritten to current truth — never appended with dated updates._

## Who is reading

The owner (the person packaging the pack, see `review-loop.md`) is an expert in two things: the delivered engagement — the customer, what was built, what it did, what it cost — and the pack they want to sell. Assume nothing else. They have not read this bundle and do not know the method, its research steps, its tests, the spec file or its keys, the channels, the linters, the question widget, or what an agent, a skill or a plugin is. Every message is read on that basis, including by the owner who wrote the method and does not want to translate.

## The test

Before sending anything the owner reads — a question, a widget title, an option label or description, a card, a table, a TLDR, a review pack, a closing message, a document they open — read it as someone who knows only their project and their pack. Any word they would have to ask about is replaced or removed. Never in owner-facing text:

- **Method codes and internals**: T1–T9, P1–P9, R2/R3, "§7", "move 2", "the row-writer", "the four-axis test", "the general-enough test", "adjudication", "sign-off component 3", "the options step", "the intake", "fan-out", "the research agents", "the method".
- **Files, keys and tools**: `pack-spec.md`, `meta.status`, any spec key, "lint", checker or script names, `decisions.md`, plugin or skill names, "widget", "the schema", "the catalog".
- **Packaging vocabulary used as vocabulary**: "triad", "channel" and its values (`partner_print`, `customer_site`), "tier ladder", "specificity tags", "the spine", "re-spine", "vendor ladder", "catalog id"; status glyphs ● ◐ ○ used as counts ("3 ○ rows").
- **The bundle's own house terms**: "the owner", "the practice", "the bundle", "house format".

## Say it in the owner's words

| Internal | Say |
|---|---|
| T1–T9 | The plain trap and its consequence: "this widening has no boundary — a buyer would read it as a slogan"; "the capability list never left what we built for the customer — there is no roadmap row" |
| P1–P9, "the vendor-gap research" | What was researched: "the research on what the vendors already ship", "how this workflow runs in other industries", "a red-team pass" |
| "research-brief §7" | "the research summary, section 'What is specific to the customer'" — sections by title, never by number |
| "the spec", `pack-spec.md`, "component" | "the pack brief"; the parts of the pack by name: its name, one-liner, problem and solution, who buys it, industries, capabilities, workflow, architecture, Oracle products, metrics, packages |
| "sign off component 4", "confirm" | "confirm the name" — name the part, never its number |
| "triad" | "name, one-liner, problem and solution" |
| "channel" | Who will see it: "for our own team", "for Oracle and SoftServe sellers", "for customers on the site", "in the demo" |
| "tiers", "the tier ladder" | "the three packages: PoV Jumpstart, Integration, Scaling" (the pack's own names are fine) |
| ● ◐ ○, "3 ○ rows" | "available", "partially available", "on the roadmap"; "three capabilities are on the roadmap, not built yet" |
| "ICP" | "who buys it, at what kind of company" |
| "PoV" | Allowed — it is the pack's own term; spell out "proof of value" the first time |
| "lint is clean", "the checker" | "the automatic checks passed"; "one check found: <plain finding>" |
| "the delivered case's divergence" | "where the pack differs from what we built for <customer>" |
| "the spine" | "the steps every industry shares" |
| "catalog id" | The product's name as Oracle lists it — the name is fine, the term is not |
| "the owner" | "you" |
| "intake" | "a few questions before we start" |
| "adjudication questions" | "your call on what the research found" |

## How a question is put

- **Propose before you ask.** A question is the last resort. When the inputs or the research answer it, state the answer with its source and move on — the owner corrects what is wrong. Ask only where a wrong guess would force a rebuild rather than an edit (2026-09-22).
- **What we are deciding, in the pack's terms**; one line on why it matters for the pack — what it changes downstream, in plain words ("this decides which industries the sales deck leads with"); and what happens if they skip (the default, in plain words).
- **Options are outcomes for the pack** ("lead with banking, logistics second"), never method states ("keep T3", "status ◐"). Each description carries the trade-off in one plain line; the argument lives in the card or table above, not in the option.
- **Progress in plain terms**: "4 of 11 parts confirmed; next: the industries".
- **Reasons, not rule names**: "a proof longer than 10 weeks reads as a project, not a proof", never "the PoV cap rule".
- **The owner's own words win**: use the names from their documents — their product's name, their customer's terms, their step names — except where the customer-naming rule applies, and then say why in plain words ("the customer's name is not cleared for the sales deck, so it reads 'a European logistics operator'").

## Where we are — the map the owner sees

The owner wants to know which workflow they are in, in plain conceptual terms, before the first question and at every step.

- **Show the map once, first.** Before the first question, one short message: what will happen, as numbered stages in the owner's words, with how many questions each stage holds. For the pack brief (`/oracle-packs:spec`):
  1. **Before we start** — the questions only you can answer (up to 11; the ones your documents already answer are skipped, and you are told which).
  2. **Research** — no questions; progress is reported, and it ends with a research summary you can read in ten minutes.
  3. **Your call on the research** — up to 7 questions on what the research found: which industries are real, which differences between them are real, what happens when things go wrong, how broad the pack should be, what the vendors ship that we do not, what stays out of scope, what is built per customer.
  4. **The pack's story** — one decision: the name, one-liner, problem and solution we build on, from a side-by-side table of candidates.
  5. **Confirm the pack, part by part** — 11 decisions in a fixed order: problem and solution · one-liner · who buys it · name · industries · capabilities · workflow · architecture · Oracle products · metrics · packages.
  6. **The whole brief** — one look at everything, then confirm, change or stop.
  After that the artifacts are built one at a time, each reviewed before the next (`/oracle-packs:build` shows its own map: artifact n of N).
- **Every question title carries its place**: `<Stage> · <n> of <N> · <question name>` — "Before we start · 3 of 9 · Where the raw inputs are", "Your call on the research · 2 of 7 · Which differences between industries are real", "Confirm the pack · 4 of 11 · The name", "Artifacts · 2 of 6 · The sales deck". N counts the questions actually asked in that stage, after skipping, so the count never lies.
- **Open what the stage produced beside the conversation before asking** — the research summary, the brief, each artifact — so the owner answers while looking at the thing, never at a description of it.
- **Say when a stage ends**, in one line: "Stage 3 of 6 done — your call on the research. Next: the pack's story, one decision."
- **All of a stage's questions are asked in that stage.** Everything only the owner can answer before the research starts is asked before the research starts; nothing is held back to interrupt them later.

## Every question stands alone

The owner answers from the question and its card alone, without re-reading the research or the conversation. Anything the question refers to — a finding, a document, a figure, a person, an earlier answer — is restated in the card in one plain sentence: what it is, why it matters for the pack or for the engagement, and by when. Never by a label the run gave itself ("the incumbent-vendor finding", "the VSS 2.x removal", "the Genpact patent"): the owner has to be told, in one sentence each, what the competitor finding is, what is being withdrawn and when, what the patent covers, and what each means for them. If a card would need more than five such sentences, the question is too big — split it.

## No questions outside the map

A finding that matters outside the pack — for the live engagement, for another team — is reported in chat as a short plain note: what was found, what it means, who should hear it, by when; and it is logged as an open item. It does not become a question about what the assistant should do with it, and never a choice between the assistant's own work products. Nor is there ever a question about how to proceed: the flow is fixed — the brief confirmed as a table, then the artifacts one by one, each reviewed — and a gate offers only its own three choices, confirm · change · stop. Only a time-critical item earns a question, and then it is one plain yes/no that names the deadline: "One of the products the solution runs on is withdrawn on 30 September. Do you want a one-page note on it for the engagement team today?"

## What stays internal

Everything technical still happens — files written, keys set, checks run — silently, and is reported in the owner's words: "saved to the pack folder", "all checks passed", "one check found: <plain finding>". The pack folder's path is named once, when it is created; a file name appears only when the owner needs to open that file.

## Self-check line for every skill

- [ ] Every message, question, option and table the owner saw passes the reader's test: no method codes, no file or key names, no packaging vocabulary as vocabulary, reasons instead of rule names.
