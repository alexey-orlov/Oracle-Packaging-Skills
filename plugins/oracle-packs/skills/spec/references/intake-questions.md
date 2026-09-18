# Intake — the predefined question list

Asked at the start of `/oracle-packs:spec`, one widget at a time, in this order. **Skip a question when the answer is already in the context** (the user's message, an existing `pack-spec.yaml`, the input folder's documents, or `packs/<slug>/intake.md` from an earlier run) — state the answer you found and where, and move on. Never ask a question whose answer you could read from the inputs. Record every answer with `source: user:<date>` in the spec.

## Block A — locate the raw inputs (always first)

| # | Question | Why it matters | If the user has nothing |
|---|---|---|---|
| A1 | Where are the raw inputs? A folder path, or individual files: the delivered engagement's SoW or scope doc, the PoC or final deck, the demo recording, feature lists or backlog, call transcripts, existing pack artifacts from a sibling pack. | Everything downstream is evidence-bound; the inventory is step 1 of the method. | Proceed with research only, and mark every fact `source: research` — the brief will say the pack has no delivered-case evidence. |
| A2 | Which of these is the delivered case the pack starts from (customer, what was delivered, when, on which Oracle/NVIDIA components)? | The generalization is measured against it; the divergence gets stated in every sales artifact. | Ask whether the pack is meant for a product with no delivered engagement behind it (allowed; the site has one) and set `meta.source_engagement: none`. |
| A3 | Is there an existing pack spec, feature table or earlier packaging attempt for this case? | Reuse and reconcile instead of restarting; two competing tables are the WfO estate's main defect. | Continue. |

## Block B — the pack's frame (asked only if not answered by the inputs)

| # | Question | Default when unanswered |
|---|---|---|
| B1 | Which roadmap item does this pack map to? (offer the closest matches from `shared/data/roadmap-items.csv` by name similarity) | Propose the top three; if none fits, propose a new item and flag it for the roadmap owner. |
| B2 | Which verticals do you expect to sell it in, first and second? | Research proposes three from the domain study. |
| B3 | Which artifacts do you want at the end? (feature list · sales deck · sales one-pager · executive summary · mini-site listing · interactive demo) | All six, in that order. |
| B4 | Who is the internal contact for this pack (the person doing the packaging)? | Ask; never default to a name. Emails per channel come from `shared/references/naming-and-clearance.md`. |

## Block C — clearance and numbers (asked before the options step)

| # | Question | Default when unanswered |
|---|---|---|
| C1 | May the customer's name and logo be used, and where: internal · partner-facing print · customer-facing site · demo? | All false except internal; the anonymized descriptor is proposed by the research step. |
| C2 | Which figures from the delivered case are cleared to use, and as what: delivered result · PoV result · target · modeled? | Nothing cleared; artifacts print "results to follow" rather than a number. |
| C3 | PoV duration and price: do you have a target, a SoW value, or a constraint? (Reminder shown: PoV 4–8 weeks ideal, 10 weeks hard cap.) | Duration proposed from the scope; price left `tbd` with a footnote, never invented. |
| C4 | Are any facts internal-only (contract values, named accounts, capacity numbers)? | Everything from a SoW is internal-only unless the user clears it. |

## Block D — before the demo skill runs (asked by `/oracle-packs-web:demo`, not here)

Sources for the walkthrough: a video, screenshots, a written overview, or a detailed brief of the real product's flow. The demo skill refuses to start without at least one.

## Rules for asking

- One widget per question; two to four concrete options plus the free-text "Other"; when you have a recommendation, put it first and label it.
- Every question carries one line of "why this matters" so the user can answer fast.
- When an answer contradicts the inputs (a price, a date, a count), say so before moving on; the user decides which is right.
- When something essential is missing and no default is safe, stop and ask; never fill the gap with an invention.
- Write the answers to `packs/<slug>/intake.md` as you go, so a rerun skips them.
