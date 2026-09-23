# The diagram reviewer — slide 8

**What this is.** The architecture slide has been wrong more often than any other, and the builder is the worst judge of its own diagram. A **fresh-context subagent**, model `opus`, reviews it.

**What the reviewer is given, and nothing else**

- The render of slide 8.
- The spec's `architecture` component.
- `shared/references/architecture-diagram.md`.

No build conversation, no rationale, not this card. It returns that file's nine-point checklist with pass or fail and a one-line reason each.

**Checks this step must pass**

1. The reviewer's context is fresh — not me re-reading my own build.
2. Every fail is fixed and the slide re-rendered. Stop when it passes, or after three rounds.
3. Anything still failing after three rounds goes to the owner in plain words, as what is wrong in the picture — never as a checklist or a rule number.
4. The builder's plain-sentence summary of the diagram — the boxes, then the arrows — goes into the review pack, so the owner can check the naming and the direction without opening the slide.

**Bad.** "Point 4 failed: unlabelled edge." **Good.** "The line from the dispatch system doesn't say what it sends; I've labelled it 'job status every 5 minutes' — tell me if that's wrong."

Derivation rules a fix has to respect: `references/cards/slides-6-10.md`, slide 8.

**Reads:** `architecture.{inputs[], stack[], outputs[]}`. **Writes:** nothing directly; fixes land in the pack brief or the build.
