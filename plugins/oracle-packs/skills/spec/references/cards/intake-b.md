# Before we start · the pack's frame

**What this is.** Four decisions that fix what is built and who owns it. Same stage as the inputs and the clearance, before any research. Skip any the inputs answer.

**Ask:**

- **Which item on the practice roadmap this pack is.** Offer the closest matches from the roadmap extract. *Unanswered:* propose the top three; if none fits, propose a new item and flag it for the roadmap owner.
- **Which industries you expect to sell it in — first and second.** *Why it matters:* it decides which industries the sales deck and the site lead with. *Unanswered:* three are proposed from the research on how this job runs across industries.
- **Which of these you want at the end.** Six choices, so this is **one call with two multi-select questions**, never one question with the artifacts bundled into four options. "Documents": Feature list (.docx), Sales deck (.pptx), Sales one-pager (.pdf), Executive summary (.pptx). "For the mini-site": Mini-site listing (a product page), Interactive demo (a clickable walkthrough). Labels in exactly that `<Artifact> (<format>)` form, each with one line on what it is and who reads it. *Unanswered:* all six, in that order.
- **Who owns this pack inside SoftServe.** *Unanswered:* ask — never default to a name.

**Checks this stage must pass**

1. The roadmap item is an id that exists in the extract, or an explicit new-item flag.
2. The artifact question is two multi-selects, one artifact per option — merging choices to fit the four-option cap is a defect.
3. No option names a plugin, a skill, or which tool builds what.
4. The answer is recorded once; the build reads it and never asks again.

**Fills:** `meta.roadmap_item_id`, the priority order of `verticals[]`, the artifact set for the build, `contacts`.
