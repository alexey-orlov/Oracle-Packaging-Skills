# The customer's logo

**What this is.** The delivered customer's own mark, for the deck's proof slide (and the today → tomorrow slide). The one picture in the pack that is not found but given. Ask for it only where the pack brief clears the customer's name for some audience; where clearance is false everywhere, the slot does not exist and nothing is asked.

**How to ask.** One question, with two ways out: the owner gives a file path, or skips. Say why it is worth finding: with the logo the proof slide is the delivered case with the customer's mark on it, which is the strongest slide in the deck; without it the slide still builds, and the logo is an open item. Then record it:

    python3 tools/apply_choice.py <spec> --slot customer_logo --file <their file>

**The checks**

1. Asked only when `clearance.customer_name_allowed` is true for at least one audience — never otherwise, and never re-asked once the brief has a file.
2. **Never searched for on the web.** A company's mark is a trademark, not an openly licensed picture, and a copy off a search result carries no right to use it. The only file this step accepts is one the owner hands over from the engagement materials.
3. No stand-in, no lookalike, no redrawn version. Skipped is skipped: the slot goes to the closing message as open, with what would unblock it.
4. Recorded through `apply_choice.py` like every other picture, so the file, the brief key and the credits row move together. Its record says it was supplied by the owner and is used under the customer's clearance in the brief — there is no licence to look up.
5. The brief still passes `python3 shared/tools/lint_spec.py <spec>` afterwards.

**Fills:** `deck.images.customer_logo`. **Writes:** `packs/<slug>/visuals/`, `credits.md`, `decisions.md`.
