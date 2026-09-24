# Building the page

**What this is.** The sales one-pager: the deck condensed onto one A4 page, rendered from the confirmed spec as HTML and printed to PDF. Section order and what each block carries: `shared/references/anatomy/artifact-one-pager.md`.

```
shared/tools/py tools/build_one_pager.py <spec> --out <dir> --channel partner_print|internal [--hero <image>]
```

Exit 0 one A4 page · 1 spec error · 2 a name this channel may not carry reached the page · 3 more than one page (card `overflow`) · 4 no Chrome, so nothing was verified. Needs `pyyaml`, `pypdf` and Chrome or Chromium (`CHROME_BIN`, then the macOS default, then PATH). Name what is missing; never degrade silently.

**Checks the build must pass**

1. The channel is settled before building: `partner_print` (default) or `internal`, which carries prices in full and named accounts. Store both values; show neither.
2. Cut by design, not by accident: no technology-stack section and no full feature matrix. The capability rows in the packages table are the whole capability summary.
3. A block with no content in the spec renders as nothing at all — never a heading with an empty body, never a "not available" sentence.
4. Every capability entry carries a level per tier (the `Level at …` columns, `levels.pov` and so on, or a glyph-prefixed string). Prose with no level is an error the tool names by entry: fix the spec, never guess a level.
5. `--hero` is an approved image the owner supplies, embedded into the file at build time. Never fetch imagery from the web. No hero is a supported state, not a degraded one.
6. The data-flow strip reuses the reviewed architecture and its naming (`shared/references/architecture-diagram.md`); it invents no new boxes.

**Reads:** `meta.name_variants`, `one_liner`, `problem_solution`, `verticals[]`, `kpis[]`, `packages.*`, `architecture`, `contacts.<channel>`, `clearance.*`, and the `one_pager:` overrides.
