# Building the feature list

**What this is.** The pack's spine document, built by a tool from the spec: one A4 page of Area > Category > Feature with a status per feature and the standard customization scope per area. Every other artifact condenses it. Section order, columns and legend: `shared/references/anatomy/artifact-feature-list.md`.

**Read the spec, not the delivered artifacts.** The title and the two intro lines come from the keys the anatomy names; `feature_list.intro` overrides `one_liner.full` where the pack needs a longer definition. Missing `icp.line` → go back to `/oracle-packs:spec` for it rather than inventing one; otherwise the build prints the one-liner alone and warns. Rows = `capabilities[]` in spec order. Cut the footnotes first (card: `footnotes`).

**Build:** `python3 tools/build_feature_list.py <spec> --out <dir>` (resolve paths via `${CLAUDE_PLUGIN_ROOT}`). The customization-scope column stays last; Area and Category cells merge down. The build walks a fit ladder — a row per feature at 7.5pt, then 7pt, then compact mode (a row per category, features inline, the status and tier columns dropped) at 7.5 and 7pt — and where Pages is installed verifies the real page count. `--fit none` allows several pages, only when the long form was asked for; `--no-check-pages` skips verification. Exit 3 → card: `does-not-fit`.

**Checks**

1. Type never drops below 7pt to buy space: one page is a requirement, and the lever is the tree, not the size.
2. `icp.line` was present or fetched from the spec skill — never invented.
3. The rung the build printed is carried into the review; needing compact mode means the tree is too fine.
4. The spec version and build date went into the file's properties, and nothing onto the page.
5. Rows follow the spec's order and the spec's wording (card: `statuses-and-wording`).

**Reads:** `meta.name`, `one_liner.full` / `feature_list.intro`, `icp.line`, `capabilities[]`.
