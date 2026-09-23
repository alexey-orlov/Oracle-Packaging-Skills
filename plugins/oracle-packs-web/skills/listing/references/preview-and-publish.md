# Preview, QA and publish a listing

_Long form; the runtime cards are `references/cards/site.md`, `preview.md`, `gates.md` and `publish.md`._

Written generically: no location or URL is a constant in this bundle. The site
supplies its own in `site.manifest.json` at its root, and the runner supplies
only the root.

| Input | What it is | Where it comes from |
|---|---|---|
| **site root** | The repo that contains `site/` and `site.manifest.json` | `--site`, else `ORACLE_SITE_ROOT`, else a session opened in the site repo |
| **publish root** | The tree that actually goes live | manifest `paths.publishRoot` |
| **preview target** | Where the site is previewed | manifest `publish.target` |
| **demo preview target** | Where a standalone walkthrough is previewed (its own URL) | manifest `publish.demoTargets` |
| **Node** | Any version for the checker; ≥ 22 for the capture script | `NODE_BIN` |

**Preflight, before any work:** print `node --version`, resolve the site
root and read its manifest (card `site`). State the requirement and what is missing rather than starting and failing
halfway. A source the environment cannot reach is **deferred and retried** — it
is never recorded as "not found", because that closes the item forever on the
strength of a network failure.

On a machine other than the one that last worked on the site: `git pull` first,
and commit explicitly. Do not assume an autosync daemon is running.

---

## 1 · Run it locally

```sh
cd "$ORACLE_SITE_ROOT/site"
python3 -m http.server 8765 --bind 127.0.0.1
```

Then browse **`http://127.0.0.1:8765`** — **not `localhost`**, whose cache goes
stale and quietly serves the previous build.

If the editor's own preview launcher is available, point it at the same origin
rather than starting a second server. A QA subagent can kill a shared server;
restart it before blaming the page.

**Fresh assets.** The preview caches hard. Before measuring any CSS or data
change, either confirm the new rule is in `document.styleSheets`, or re-point
the stylesheet link with a `?v=<something>` query from the console, or
`fetch('<file>', {cache: 'reload'})` each changed file — then navigate.

---

## 2 · QA widths

Look at **every changed screen** at:

**1440 · 1280 · 1024 · 768 · 375**, and the **H1 at 320**.

- Check **horizontal overflow at every width**.
- Headings are display lines: count them **on the rendered page**, not in the file. No lone short word on a line at 375.
- Screenshots taken after scrolling can come back black. Take each shot at scroll 0: hide the other sections from the console and force the reveal class on the block you are shooting, or resize the viewport tall.
- A component moved to a new page **takes its wrapper, its modifier classes, the container width it was sized for and its breakpoints with it.** Moving a component breaks it quietly — a shipped hero once lost its wrapper and rendered an 84 px H1.

Tab-by-tab for a new product: every tab its page renders (the site's
START-HERE §3 names them) — plus the catalog tile and the facet rail with this
product's platform selected.

---

## 3 · The three gates

All three must be green. Nothing publishes on two out of three.

**Gate 1 — the site's own checker** (the manifest's `checker.run`; this skill
keeps no copy).

```sh
"$NODE_BIN" --check <each changed .js>
"$NODE_BIN" "$ORACLE_SITE_ROOT/tools/check-grammar.js"
# → check-grammar: OK — N products, every grammar slot filled, …
```

Generate the deny-list before the gate, never by hand:

```sh
python3 tools/denylist-to-json.py --out "$ORACLE_SITE_ROOT/tools/deny-list.json"
```

It converts `shared/tools/denylist.txt` — the one list the practice keeps — into the
checker's JSON, so the names cannot diverge between the Python linters and this
checker. Pass `--deny-list <file>` if it lives elsewhere. The checker only *warns*
while the customer-name list is empty, and an unconfigured deny-list is the one
failure mode that ships a name: treat that warning as a failed gate.

**Gate 2 — the console.** Clean on **every route**, not just the one you
changed. A renderer that throws on a tab you did not open is still a broken tab.

**Gate 3 — the deny-list sweep.** A belt-and-braces grep over the publish root,
independent of the checker, because it catches files the data layer never
mentions:

```sh
grep -ri "<name1>\|<name2>\|<banned-path>/" "$ORACLE_SITE_ROOT/site" \
  --include='*.js' --include='*.css' --include='*.html'
```

Quote the globs — unquoted, zsh aborts with `no matches found` before grep
runs. If an alternative grep hits a complexity limit, use `/usr/bin/grep`.
Deny-list regexes need **word boundaries**: an unbounded "2 months" once matched
"3–12 months".

---

## 4 · Publish

Generic procedure. It has three parts: strip the wrapper, pass a files map,
then confirm what is actually live.

### 4a · Strip the wrapper

A hosted-preview platform wraps the page in its own document skeleton, so the
copy you hand it must carry **only** the body content plus the site's own
`<title>`. Strip **by exact line, never by prefix** — a prefix strip on `<head`
once removed `<header class="masthead">` and shipped a site with no sticky nav:

```sh
mkdir -p "$ORACLE_SITE_ROOT/.work/publish"
grep -v -x -F \
  -e '<!DOCTYPE html>' \
  -e '<html lang="en" data-theme="light" data-brand="ss26">' \
  -e '<head>' -e '</head>' -e '<body>' -e '</body>' -e '</html>' \
  -e '<meta charset="utf-8">' \
  -e '<meta name="viewport" content="width=device-width, initial-scale=1">' \
  "$ORACLE_SITE_ROOT/site/index.html" > "$ORACLE_SITE_ROOT/.work/publish/index.html"

diff "$ORACLE_SITE_ROOT/site/index.html" "$ORACLE_SITE_ROOT/.work/publish/index.html"
# exactly those lines should differ — no more, no fewer
```

The `-e` list is the manifest's `publish.wrapper.stripExactLines`, never this
copy of it: the rule is "the document skeleton and the two meta lines the host
already provides". Keeping the meta lines once shipped them twice inside `<body>`.

Where the wrapper goes depends on where the session runs. The Artifact tool
reads sources only from the session's working folder and its scratchpad. In a
session opened in the site repo, write it to the git-ignored `.work/publish/`.
From any other folder, copy the wrapper and every file you publish into the
scratchpad, keeping their paths under a copy of the publish root, and publish
from that copy.

### 4b · Publish with a files map

- **Target:** the manifest's `publish.target`, so the same URL updates; never one in `publish.neverPublishTo`. Publishing without it creates a *second* page and the link you already shared goes stale.
- **Read before you write.** Read the live page once in the session before the first publish, or the publish is refused as "not built on the newer version".
- **Root + files map:** root at the publish root; the map is published path → source path, for **every changed or added file**. Files not passed are kept; **new images must be passed explicitly**.
- **Publish the full tree when another session may have changed renderer files.** A partial publish once shipped a new data file against an old renderer and broke the home page. The full tree is the manifest's `publish.fullTree`: what the target already lists plus the new files, never the whole folder, and never a path in `publish.neverInArtifact`. Fonts carry the types in `publish.contentTypes`.
- **On a refusal:** read the live copies of the files you changed, diff them against local, treat the working tree as the merge, then publish again. Never force past a conflict.

### 4c · Confirm what is live

Run the platform's **file listing** on the target and check **two** things:

1. every new file is live, and
2. **nothing is published that should not be.**

That second check is the one that matters: it is how three customer logo files
were found sitting on a link-shared page, downloadable by path, long after the
data layer had stopped referencing them.

### 4d · A walkthrough is its own page

A demo that lives inside the site tree at `site/demo/<slug>/` cannot be opened
as a top-level page when the site is served as a single preview artifact — a
supporting file is not a document. So:

- publish the walkthrough **standalone**, as its own preview target, and put that URL in `config.products[<slug>].demoPreviewUrl`;
- keep `demoUrl` as the **canonical relative path** for the real deployment, unchanged;
- the listing's secondary CTA opens the demo **in a new tab**.

---

## 5 · Record and report

- Append a round record where the site keeps them: the asks, the decisions, a before/after table, the checks run, and **Open for the owner**.
- Update the site's own schema/config/grammar docs wherever the contract moved.
- **Turn every new owner rule into a checker assertion** in the same pass.
- Report: what changed · what was decided differently and why · what is still open.

Two things that bite when sessions overlap: another session may be publishing
the same target (expect refusals — re-read, merge, republish), and record
section numbers collide (read the last heading before numbering).

---

## 6 · One-screen checklist

```
[ ] node --version printed; site root resolved; manifest read; git pull done
[ ] node --check on every changed .js
[ ] denylist-to-json.py → <root>/tools/deny-list.json written
[ ] the site's own checker → OK, and no deny-list warning
[ ] console clean on every route
[ ] deny-list sweep over the publish root → nothing
[ ] every changed screen at 1440/1280/1024/768/375; H1 at 320; no h-overflow
[ ] wrapper stripped by exact line; diff shows only the skeleton lines
[ ] read the live target, then publish with root + files map
[ ] file listing: new files live, nothing live that should not be
[ ] demo published standalone; demoPreviewUrl set; demoUrl left canonical
[ ] round recorded; new rules turned into checker assertions
[ ] report: changed / decided differently / still open
```
