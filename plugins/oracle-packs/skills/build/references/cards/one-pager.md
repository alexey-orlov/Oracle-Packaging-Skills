# The sales one-pager — one A4 page

**What this is.** The approved deck condensed onto one A4 page, rendered from the spec as HTML and printed to PDF; never a second source of truth.

**The page, in order.** Hero: the family name as eyebrow, the external name variant, the full one-liner, the approved photograph faded behind the right 46%; pitch, two columns: the problem (a lead and three bullets), the solution (the reframe, three outcome chips, the mechanism in two sentences) and the architecture strip; beside it, "Why it sells: for <partner> account teams" and a "Where it applies" chip row; the proof strip; the packages table: three tiers, prices, timeline, capability rows as glyphs, the legend and the price footnote; the closing question, the offer and the named contact. No technology-stack section, no full feature matrix.

    shared/tools/py one-pager/tools/build_one_pager.py <spec> --out <dir> --channel <channel> [--hero <image>]

Exit 0 one page, 1 spec error, 2 a name this channel may not carry, 3 over one page (card `one-pager-overflow`), 4 no Chrome, nothing verified.

**Checks**

1. A block with nothing in the spec renders as nothing, never an empty heading or a "not available" line.
2. Every capability row carries a level per tier; prose with no level is fixed in the spec, never guessed.
3. `--hero` is an image the owner approved, embedded at build time, never fetched from the web; no hero is a supported state.
4. The strip draws the pack's one reviewed model with every system and label the deck carries.
5. Look at the render: the contact block fully on the page, no scope line orphaning a word, capability marks rising left to right, every figure footnoted.

**Reads:** `meta.name_variants`, `one_liner`, `problem_solution`, `verticals[]`, `kpis[]`, `packages.*`, `architecture`, `contacts.<channel>`, `clearance.*`, `one_pager:`.
