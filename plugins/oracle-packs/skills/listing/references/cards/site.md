# The site

**What this is.** How the skill finds the mini-site and learns its current rules before touching it. The site describes itself in `site.manifest.json` at its root; this skill never restates what the site owns, and where the two differ the site wins.

**Find it**, in this order: `--site <path>`; else `$ORACLE_SITE_ROOT`; else the session's own folder, when it holds `site.manifest.json`; else ask the owner. Never guess and never search the disk. A folder without `site.manifest.json` is not a site root, including the site's retired home inside a personal repository.

**Read it before any change**

1. `git -C <site> status --short`, then `git -C <site> pull --ff-only`. A dirty tree means another session is mid-round: say so and ask before writing. A pull the environment cannot make is deferred and retried, never skipped silently.
2. Read `<site>/site.manifest.json` whole. Its `paths` say where the entry, the switch block, the figure and a walkthrough go. Its `checker` is the gate. Its `publish` block is the only source for the target, the artifacts never to publish to, the wrapper lines and the file types.
3. Compare its `contract.round` with this skill's, written against **site round 14**. When the site is newer, tell the owner in one line, then have a fresh-context agent read the site's `startHere` §3–§4 against these cards and return only the differences. Follow the site on each; its checker decides.
4. Run `node tools/refresh-exemplar.mjs --site <site> --check`. On drift, regenerate the exemplar in the same pass: the same command without `--check`.

**Record where the site keeps its records.** A round goes into the site's `docs.provenance`, a contract change into its `docs.schema` or `docs.config`, and `contract.round` moves in the same commit.

**Reads:** `<site>/site.manifest.json`. The site's START-HERE is read only through an agent, and only when the site is newer.
