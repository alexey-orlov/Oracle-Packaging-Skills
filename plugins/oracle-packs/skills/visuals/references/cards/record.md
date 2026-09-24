# Recording a choice

**What this is.** One command per chosen picture. It copies the file into the repo's `packs/<slug>/visuals/`, writes the slot's key into the pack brief with the picture's source, creator, licence and page, and logs the decision in the local work folder — all three, or none.

    shared/tools/py tools/apply_choice.py <spec> --slot <slot> --file <the chosen file> \
        [--note "<the owner's reason, in their words>"] [--add-to-library]

**The checks**

1. Every chosen file goes through this command. Nothing is copied into the pack or written into the brief by hand; the brief's entry is the picture's only record in the repo.
2. `--note` carries the owner's reason in the owner's own words, whenever they gave one.
3. `--add-to-library` only for an icon worth reusing on other packs. It never overwrites: a name already in the library stays exactly as it is, and a new icon is a new name.
4. The brief still passes its checks afterwards: `shared/tools/py shared/tools/lint_spec.py <spec>`.
5. Only a file the owner actually chose is recorded — nothing invented, nothing substituted, nothing "close enough".
6. The brief is edited in place as text and re-verified by the tool; if anything but the slot's own key moved, nothing is saved. Do not hand-edit the brief to work around that.

**Fills:** the slot's key — `verticals[i].icon`, `deck.images.today`, `deck.images.tomorrow`, and the rest of the slot list the tool holds. **Writes:** in the repo, the picture in `packs/<slug>/visuals/`; locally, `<work>/decisions.md`.
