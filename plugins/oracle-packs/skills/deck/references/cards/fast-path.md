# The rebuild round

**What this is.** One rebuild round after the owner's corrections. The builder writes the whole deck from the spec every time — there is no per-slide flag — so a change to one slide is a change to one line of the pack brief.

**How a change lands**

1. Make the change in the pack brief through the spec skill's fast path, never in the .pptx by hand: a hand-edited file is overwritten by the next build and the brief stops being the truth.
2. Run the same build call: `python3 tools/build_deck_v2.py <spec> --out <dir> --channel <channel> --fit-report`.
3. Re-review only the changed slide — but the deck linter, the clearance linter and the consistency check run on the whole file again.
4. A change to the architecture goes back through the fresh-context reviewer (`references/cards/diagram-reviewer.md`).
5. A fit-report overflow is answered by shorter wording in the brief, never by smaller type.

**Checks before closing**

- Fit report, deck linter, clearance and consistency all clean on the rebuilt file.
- The corrected slide was actually looked at, not assumed.
- The approval is recorded in `packs/<slug>/decisions.md`, and the file is delivered as `<Pack name> - Sales deck - Oracle.pptx`.

**Reads / writes:** the pack brief, through the spec skill's fast path; the rebuilt .pptx.
