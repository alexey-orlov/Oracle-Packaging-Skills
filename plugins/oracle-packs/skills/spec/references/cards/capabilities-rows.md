# How the capability rows are written

**What this is.** The rules for each row of the tree, beside card `capabilities`: where rows come from, how they are named, and what a status may claim.

**Checks the draft must pass**

1. **Rows come from the real workflow.** Map the tree against the delivered flow, screen by screen, and order the rows in flow order; a tree nobody mapped is out of step with the product by default.
2. **Each block's core job gets a plain-language row first**, before its quality rows: "find the fields a document carries" comes before confidence scoring or coverage.
3. **Task altitude.** A feature is named for the task, not for the component ("classifier") and not for the pilot customer's case ("contract header extraction"); never for the model, which is not a property of the feature.
4. **Status comes from the delivered system**, at the granularity the source supports. A cell nobody verified carries a flag in the brief and an open item, never a mark.
5. **The constraints the delivery silently assumed** (one document type, one language, one catalogue of items, one integration target) are each a variability axis, and the rows cover them or name them as scope.

**Good.** "Field recognition: find the fields a document carries, in any layout", ahead of "confidence scoring".
**Bad.** "Contract header extraction (GPT-4)": the pilot's document and the model in the name.

**Fills:** `capabilities[].categories[].features[]` (`name`, `status`, `note`).
