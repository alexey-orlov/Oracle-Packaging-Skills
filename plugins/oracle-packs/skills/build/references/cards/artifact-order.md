# The artifacts, in order

**What this is.** The fixed build order and the skill that produces each artifact. The order is not a preference: the one-pager is condensed from the approved deck, and the pictures are chosen before the deck that places them.

1. **Feature list** → `/oracle-packs:feature-list`
   ↳ then **Pictures** → `/oracle-packs:visuals` — before the deck: the icon for each industry, the cover photograph, and the two photos for today → tomorrow, proposed from openly licensed sources and chosen by the owner (the sheet opens in the side panel, then one widget per slot); a slot left unchosen stays an explicit empty container. It has its own place in the map, under "Pictures", right before the sales deck.
2. **Sales deck** → `/oracle-packs:deck`
3. **Sales one-pager** → `/oracle-packs:one-pager` — condensed from the deck, built after it on purpose
4. **Executive summary** → `/oracle-packs:exec-summary`
5. **Mini-site listing** → `/oracle-packs-web:listing` — the web plugin; tell the user to run it if the plugin is not installed
6. **Interactive demo** → `/oracle-packs-web:demo` — asks for its sources first

**Checks**

1. The pictures are chosen before the deck is built, and appear in the owner's map under their own name.
2. The one-pager is built after the deck has been approved, never beside it.
3. Nothing starts before the previous artifact is approved (card: `per-artifact-review`) — the owner's feedback on the deck changes the one-pager.
4. The map lists artifacts by name and format only, never by the skill or plugin that builds them.
5. Artifacts the owner dropped are skipped, and what the owner sees is renumbered over what remains.

**Reads:** the artifact set settled in `packs/<slug>/intake.md` or by the opening question (card: `plan-and-ask`).
