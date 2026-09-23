# The research, and the summary it produces

**What this is.** How this job is done outside the one delivered case. No questions here — progress is reported; it ends with a summary the owner reads in ten minutes.

**What the fan-out produces.** Five agents, at most four at once, each writing `packs/<slug>/research/<topic>.md` and reading its own prompt from `references/generalization-method.md` §4 — the method never enters this conversation.

1. **How the job runs across industries** — canonical steps, where industries differ, how the delivered case differs.
2. **What other vendors ship** — 3–5: direct competitors, substitutes (a team doing it by hand counts), same-vendor overlaps; which steps we miss or over-split.
3. **The industries** — three or more, every step, a "what matters here" line; widened deliberately; the owner rules on it next.
4. **What happens when things go wrong** — a failure path per step; "not covered" is a required answer, not a blank.
5. **What is specific to the customer** — each feature tagged customer / engine / use case / industry, reusable or built per engagement.

Yourself: the delivered case in three lenses (what the vendor pack gave, what we built, what stays custom), the roadmap item, candidate Oracle products and metrics, a red team.

**Checks the summary must pass**

1. The sections of `../research-brief-format.md` (read as you start writing), in order, nothing renumbered.
2. Every non-trivial claim labeled; "—" where nothing supports it; no force-filled grid.
3. The "general enough, but not too general" test passes, or you name what fails and the research that would fix it.
4. Under about 1,600 words, open beside the conversation before the next question.
5. No agent is silent: check each output file's modification time; take over when nothing moves.

**Fills:** `provenance.research_brief`, and the evidence every later part cites.
