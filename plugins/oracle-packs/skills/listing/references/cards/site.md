# The site

**What this is.** How the skill finds the mini-site and learns its current rules before touching it. The site describes itself (`site.manifest.json` at its root, the docs it names, its checker), and this skill restates none of it: where a card and the site differ, the site wins.

**Find it**, in this order: `--site <path>`; else `$ORACLE_SITE_ROOT`; else the session's own folder, when it holds `site.manifest.json`; else ask the owner. Never guess and never search the disk. A folder without `site.manifest.json` is not a site root.

**Read it before any change**

1. `git -C <site> status --short`, then `git -C <site> pull --ff-only`. A dirty tree means another session is mid-round: say so and ask before writing. A pull the environment cannot make is deferred and retried, never skipped silently.
2. Read `site.manifest.json` whole. `paths` says where the entry, the switch block, the figure, the kit links and a walkthrough go; `checker` is the gate; `preview` and `publish` hold every value those steps use.
3. These cards were written against **site round 15**. When `contract.round` is newer, say so in one line, then have a fresh-context agent read the site's `startHere` against these cards and return only the differences; follow the site on each.
4. The keys of the switch block and of the kit links are the site's `docs.config` and `docs.schema`: read the part you are filling.
5. Extract the exemplar from the live site: `node tools/exemplar.mjs --site <site> --out <work>/.scratch/exemplar.js`.

**Record where the site keeps its records.** A round goes into its `docs.provenance`, a contract change into `docs.schema` or `docs.config`, with `contract.round` moved in the same commit.

**Reads:** `<site>/site.manifest.json`; the site's docs, a part at a time.
