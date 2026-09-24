# The pack's story — one decision

**What this is.** Name, one-liner, problem, solution and who buys it, settled **together** as 2–3 complete candidates: one table, one widget, one pick. The rules for the one-liner, the buyer and the name: card `story-parts`.

**The table.** A column per candidate, headed `<letter> · <Name>`. Rows: **Name, One-liner, Problem, Solution, Who buys it, Sells best in, Bets on, Leaves out, Risk**. Rows, not paragraphs; every option the widget offers is a column, a blend included. Under it: the recommendation and its reason, and the likeliest alternative. The widget carries only the pick: the column labels, one line each, recommended first, plus free text and "research further".

**Checks every candidate's problem and solution must pass**

1. **Tangible:** the problem names a role and a situation with the nouns on that person's desk; they could say it about their week. "Commercial teams work out what a development means for their accounts" fails; "Account managers can't keep up with the market signals, insights and updates in their accounts" passes.
2. **Zero context:** an Oracle or SoftServe seller outside the industry can restate it — the business named, literal words, everything introduced, ≤ 30 words. If the pain is insider-only, one clause first says it exists and why it hurts.
3. **The solution is what the person now does** ("review the plan, not build it"), never the machinery ("resolved, reasoned, scored").
4. Two to four sub-problems, each a label plus one clause, none restating the headline, none owned by nobody ("data silos", "lack of visibility").
5. Nothing opens on the vendor or the engine.

**Fills:** `problem_solution` (`problem`, `solution`, `problem_points[]`, `today`, `tomorrow`), each `source: user:<date>`.
