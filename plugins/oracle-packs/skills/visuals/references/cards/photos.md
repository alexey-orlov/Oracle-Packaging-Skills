# The photographs — today and tomorrow

**What this is.** The pair on the deck's before-and-after slide. Search terms come from the pack's own words, not the industry name.

    python3 tools/search_photos.py "<terms>" --out <dir> --slot today --n 3
    python3 tools/contact_sheet.py <dir> --out <sheet.png>

- **today** — the pain in the way the work is done now, from `problem_solution.problem` and `problem_solution.today`: the desk, the paperwork, the manual step. **Never a picture of the software.**
- **tomorrow** — the person using the solution, from `problem_solution.solution` and `problem_solution.tomorrow`: the plan reviewed, the decision made.
- **cover** — **not a standard slot**: the deck's cover carries the family's shared picture. Offer one only when the owner asks for this pack's own: the industry at work, wide, no text.

**The checks**

1. **Landscape, at least 1600 px wide, no text or watermark in the picture.** The frames are wide: a portrait crops to nothing, and baked-in text cannot be corrected.
2. **The two read as one pair** — same era, same register, both landscape. An archive photograph opposite a modern one reads as a joke. Check the pair on the sheet before asking.
3. **People are a decision, not a detail.** Prefer pictures where no face reads as an endorsement and where clothing, screens and equipment do not date the picture. Say so plainly rather than letting it reach the deck.
4. The sheet is open beside the conversation before the question, and each option's line says **what is in the picture, who took it and where it is from**, plus **"Search again"** as free text — the question's shape is on `icons.md`.
5. Openverse's search is strict — every word must appear, so search one to three broad words.

Licences and the record: `references/cards/sources.md`.

**Fills:** `deck.images.{cover, today, tomorrow}`, through the record step.
