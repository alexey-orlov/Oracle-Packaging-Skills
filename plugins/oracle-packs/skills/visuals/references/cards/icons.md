# The icon for each industry

**What this is.** One icon per entry in `verticals[]`, for the deck's industries slide. Three candidates, one sheet, the owner picks.

    python3 tools/suggest_icons.py "<industry>" --context "<its 'what matters here' line>"
    python3 tools/fetch_icon.py <name> --out <dir> --slot vertical:<i>
    python3 tools/contact_sheet.py <dir> --out <sheet.png>

**The checks**

1. **Judge the three yourself before showing them.** If none of them says the industry, search again *before* asking — a question offering three wrong pictures wastes the owner's turn.
2. **The sheet is open beside the conversation before the question**, and the letters in the question match the letters on the sheet.
3. One widget per industry, titled `Pictures · <n> of <N> · The icon for <the industry>`: options `A` / `B` / `C`, **one plain line each saying what the icon shows** ("a washing machine", "a house with a gear"), plus **"Search again"** as free text, which becomes the next search.
4. **Options are pictures, never actions.** No "keep looking", no "skip for now" as an option label.
5. **One family, one weight** — all from one set, rendered white for the dark panels and ink for light grounds. Four in a row show any mismatch immediately.
6. **No two industries end up with the same icon.** A wrench can be the best candidate for two of them, and two identical pictures in one row read as a mistake: search again for the second rather than shipping the pair.
7. Where the owner does not choose, the slot stays an **explicit empty container** and becomes an open item — never a stand-in, never a number, never an icon in place of a photograph.

Licences and the record: `references/cards/sources.md`.

**Fills:** `verticals[i].icon`, through the record step.
