# Intake — the predefined question list

Asked at the start of `/oracle-packs:spec`, one widget at a time, in this order. To the owner this is stage 1 of the map, "Before we start" — never "the intake"; all three blocks are asked here, before any research runs, and each widget is titled `Before we start · n of N · <question name>`, N being the questions actually asked after skipping (decide the skips first, then number). The question texts below are what they read: keep their meaning, and keep them in the plain words of `shared/references/talking-to-the-owner.md`. **Skip a question when the answer is already in the context** (the user's message, an existing `pack-spec.yaml`, the input folder's documents, or `packs/<slug>/intake.md` from an earlier run) — state the answer you found and where, and move on. Never ask a question whose answer you could read from the inputs. Record every answer with `source: user:<date>` in the spec.

## Block A — locate the raw inputs (always first)

| # | Question | Why it matters | If the user has nothing |
|---|---|---|---|
| A1 | Where are the raw inputs? A folder path, or individual files: the delivered engagement's SoW or scope doc, the PoC or final deck, the demo recording, feature lists or backlog, call transcripts, existing pack artifacts from a sibling pack. | Nothing in the pack gets invented — every line in it has to come from something you give us or from research we can cite. | Proceed with research only, and mark every fact `source: research` — the brief will say the pack has no delivered-case evidence. |
| A2 | Which of these is the delivered case the pack starts from (customer, what was delivered, when, on which Oracle/NVIDIA components)? | Everything we widen is measured against it, and every sales document says in one line where the pack differs from what was delivered. | Ask whether the pack is meant for a product with no delivered engagement behind it (allowed; the site has one) and set `meta.source_engagement: none`. |
| A3 | Is there an existing pack brief, feature table or earlier packaging attempt for this case? | So we build on it instead of starting over — two competing capability tables for one pack is the failure we see most often. | Continue. |

## Block B — the pack's frame (asked only if not answered by the inputs)

| # | Question | Default when unanswered |
|---|---|---|
| B1 | Which item on the practice roadmap is this pack? (offer the closest matches by name from `shared/data/roadmap-items.csv`) | Propose the top three; if none fits, propose a new item and flag it for the roadmap owner. |
| B2 | Which industries do you expect to sell it in — first and second? | Three are proposed from the research on how this job is done across industries. |
| B3 | Which of these do you want at the end? Six choices, so this is **its own widget call with two multi-select questions** — never one question with the artifacts bundled into four options. Question 1, titled "Documents": Feature list (.docx) · Sales deck (.pptx) · Sales one-pager (.pdf) · Executive summary (.pptx). Question 2, titled "For the mini-site": Mini-site listing (a product page) · Interactive demo (a clickable walkthrough). One artifact per option, every label in exactly this `<Artifact> (<format>)` form, each with a one-line description of what it is and who reads it. Which plugin builds which is your business, not a question title. | All six, in that order (the user skips, or ticks everything). The build takes this answer from `intake.md` and does not ask again. |
| B4 | Who is the contact for this pack inside SoftServe (the person doing the packaging)? | Ask; never default to a name. Emails per channel come from `shared/references/naming-and-clearance.md`. |

## Block C — what may be named, and which numbers are cleared (asked in stage 1 with A and B, before the research; the anonymous customer description and the proof length are proposed later, when their parts are confirmed)

| # | Question | Default when unanswered |
|---|---|---|
| C1 | May the customer's name and logo be used, and who may see them — our own team · Oracle and SoftServe sellers · customers on the site · the demo? | Our own team only; everywhere else the pack uses an anonymous description of the customer, proposed from the research. |
| C2 | Which figures from the delivered engagement are cleared to use, and what is each one — a delivered result · a proof-of-value result · a target · a modelled figure? | Nothing cleared; every document prints "results to follow" rather than a number. |
| C3 | The proof of value — how long, and at what price? Do you have a target, a contract value, or a constraint? (Say why with the question: a proof longer than 10 weeks reads as a project, not a proof; 4–8 weeks is where these land.) | The length is proposed from the scope; the price is left out and marked "to be confirmed", never invented. |
| C4 | Is anything here for our own team only — contract values, named accounts, how many people we can staff? | Everything from the statement of work stays internal until you say otherwise. |

## Block D — before the demo skill runs (asked by `/oracle-packs-web:demo`, not here)

Sources for the walkthrough: a video, screenshots, a written overview, or a detailed description of how the real product is used, screen by screen. The demo skill refuses to start without at least one — a walkthrough invented from the brief alone would not match the product.

## Rules for asking

- One widget per question; two to four concrete options plus the free-text "Other"; when you have a recommendation, put it first and label it.
- **One option = one choice, never a bundle.** The widget caps a question at four options. When a question has more than four concrete choices (B3 has six), split it into two or more questions in the same widget call, along a real boundary (which plugin builds it: documents vs web), all of them multi-select, with uniform option labels (`<Artifact> (<format>)`). Merging several choices into one option to fit the cap is a defect: the user can no longer take one of them without the others.
- **Every question and every option passes the reader's test** in `shared/references/talking-to-the-owner.md`: the owner knows their engagement and their pack and nothing about how this works. No step names, no file or key names, no packaging vocabulary; the question is the decision in their words, and each option is an outcome for the pack, not a state of the method.
- Every question carries one line of "why this matters" — what it changes about the pack, in plain words — so the user can answer fast, and says what happens if they skip it.
- When an answer contradicts the inputs (a price, a date, a count), say so before moving on; the user decides which is right.
- When something essential is missing and no default is safe, stop and ask; never fill the gap with an invention.
- Write the answers to `packs/<slug>/intake.md` as you go, so a rerun skips them.
