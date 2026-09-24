# The three gates

**What this is.** The checks between a written entry and a published one. **All three must be green — nothing publishes on two out of three.** The owner hears one line: the checks passed, or what one found, in plain words.

**The order, and why**

1. **Generate the deny-list first**, never by hand: `shared/tools/py tools/denylist-to-json.py --out <site>/<paths.denyList>` converts the practice's one list, so names cannot diverge. **The customer-name gate fails open**: with no list configured the checker warns and exits 0. Treat that warning as a **failed gate** — the one failure mode that ships a name.
2. **Gate 1 — the site's checker.** `node --check` on every changed `.js`, then the manifest's `checker.run`, from the site root, prints `checker.pass`. This skill keeps no copy: a port once lagged the site's gate.
3. **Gate 2 — the console**, clean on **every route**, not only the one you changed. A renderer that throws on an unopened tab is still broken.
4. **Gate 3 — the deny-list sweep**, a grep over the publish root with the practice deny-list plus the manifest's `neverShip.sweep` patterns, independent of the checker: it catches files the data layer never mentions. Quote the globs; patterns need word boundaries.
5. Then, all under `shared/tools/` and all clean: `lint_artifact.py <entry file> --channel customer_site --spec <spec>`, `check_consistency.py <spec> <entry file>`, and `check_diagram.py <repo>/packs/<slug>/architecture.json --site <diagrams.js> --slug <slug>` (`pack_paths.py`) — the figure still draws the pack's model. Drift is fixed by regenerating it.
6. **Turn every new owner rule into a checker assertion in the same pass** — a rule that lives only in prose is one the next rebuild loses — and update the site's schema, config and grammar docs wherever the contract moved, with `contract.round` bumped.

**Reads:** the inserted entry, the spec, the practice deny-list.
