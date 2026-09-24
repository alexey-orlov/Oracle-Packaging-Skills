# The artifacts, in order

**What this is.** The build order and the skill that produces each artifact. It is not a preference: the one-pager is condensed from the approved deck, and the pictures are chosen before the deck that places them.

1. **Feature list** → `/oracle-packs:feature-list`
   ↳ then **Pictures** → `/oracle-packs:visuals` — before the deck: the icon per industry, the cover photograph and the two photos for today → tomorrow, from openly licensed sources, chosen by the owner (the sheet opens in the side panel, one widget per slot); an unchosen slot stays an explicit empty container. Its own place in the map.
2. **The architecture picture** → `shared/tools/build_diagram.py` (card: `architecture-picture`) — built and reviewed ONCE, before the deck; the three artifacts are levels of detail on that one model.
3. **Sales deck** → `/oracle-packs:deck`
4. **Sales one-pager** → `/oracle-packs:one-pager` — condensed from the deck, built after it
5. **Executive summary** → `/oracle-packs:exec-summary`
6. **Mini-site listing** → `/oracle-packs-web:listing` — the web plugin; tell the user to run it if it is not installed
7. **Interactive demo** → `/oracle-packs-web:demo` — asks for its sources first

**Checks**

1. The pictures are chosen before the deck is built, and appear in the map under their own name.
2. The one-pager is built after the deck is approved, never beside it.
3. The architecture picture is reviewed once, in its own step — never again inside the three artifact skills.
4. Nothing starts before the previous artifact is approved (card: `per-artifact-review`) — deck feedback changes the one-pager.
5. The map lists artifacts by name and format only, never by the skill that builds them.
6. Artifacts the owner dropped are skipped, and what the owner sees is renumbered.

**Reads:** the artifact set settled in `<work>/intake.md` or by the opening question (card: `plan-and-ask`).
