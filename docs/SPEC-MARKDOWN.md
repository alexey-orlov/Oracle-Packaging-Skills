# The pack spec in Markdown — design

**Decision (Alex, 2026-09-24).** One file per pack, `packs/<slug>/pack-spec.md`, read by people and by every builder. It replaces `pack-spec.yaml`. The alternatives weighed and set aside: YAML plus a generated Markdown view (two files, and people edit the one that gets regenerated), and YAML only (nobody reads 700 lines of YAML, so mistakes surface only in the artifacts).

## Why, measured on the three real specs

- **The spec is a document.** In the Account Insights spec, 496 of its 515 values are text, 192 of them full sentences; 19 are numbers or yes/no switches; 47 are source notes. Across the three real specs: 8 null values, 19 empty lists, 16 multi-line texts, no pipe characters.
- **Twelve tools open the YAML themselves**, each with its own `yaml.safe_load`; one tool writes it (`apply_choice.py`); the model writes it by hand during the spec stage.
- **The one data failure so far was YAML reading wrong data without complaint**: in a Belron draft, ten feature names written as unquoted flow mappings were split at their commas into bogus keys. Only a later lint rule (SPEC024) caught it. Protection comes from one strict loader and a linter, whatever the format; Markdown adds readability and direct editing on top.

## The contract

1. **One loader**, `shared/tools/packspec.py`: `load(path) -> (data, linemap)`. `data` is exactly the dict `yaml.safe_load` returns for the same spec today, so no builder changes; `linemap` maps key paths to line numbers for lint messages.
2. **Lossless.** `load(dump(d)) == d` for the three real specs and the two fixtures, before any builder reads Markdown.
3. **Canonical.** `dump(load(md)) == md` for every file the writer produced. A write normalizes a hand-edited file without changing its data.
4. **Strict.** A structural slip is a lint finding with the file's line number; the loader never guesses. A key the layout does not know is kept in a fenced YAML block under "Other fields", never dropped, and the linter names it.
5. **Writes go through the writer**: `packspec.py get | set | check | convert`. `set <spec> <key.path> <value> [--source <src>]` re-renders the canonical file. The spec skill and the visuals tool never hand-edit tables. People may edit the file directly; the next load validates it and names the line of any slip.
6. **The artifact stamp hashes the canonical data** (sorted JSON of `data`), not the file's bytes, so a re-render or a whitespace edit never marks built artifacts stale.

## The layout

Front matter carries identity only: `slug`, `status`, `spec_version: 2`, `generated_with`, the roadmap ids. The body follows the order in which the owner reviews a pack:

1. `# <name>`, then the name variants as a key list
2. One-liner
3. Problem and solution
4. Who buys it
5. Industries — one `###` per industry, as a key list
6. Capabilities — one `###` per area with its customization line, then one table per area: Category · Feature · Status · From tier · Customization · Note · Source
7. Workflow — the inputs table, one `###` per step, the outputs table
8. Architecture — the inputs, stack and outputs as tables
9. Oracle products — one table: Product · Role · Why · PoV · Integration · Scaling
10. Metrics — one `###` per metric, as a key list
11. Packages — one `###` per tier as a key list, then the capability-handling table and the partner's case
12. Proof — the delivered engagement's context, the delivered line, the divergence line, the proof headline, the vertical case
13. Next steps
14. Open questions
15. Settings — clearance per channel as a table, contacts, pictures, per-artifact overrides, provenance; a nested object with no readable form is a fenced YAML block

The forms are declared per key path in one layout table in code: `paragraph`, `keys` (`- **Label:** value`), `table` (records with fixed columns, one row per line), `sections` (one `###` per record) and `yaml` (a fenced block). A key the layout does not declare falls to `yaml`.

## Scalars

- **Types come from the layout, never from how the text looks.** "2026" in a name stays text.
- **Text is verbatim.** A value that would read as structure (a line starting with `#`, `- **`, `|` or `---`) is written with a leading backslash, removed on read. In a table cell `|` is written `\|`. A value holding a line break never goes in a cell; that record renders as `sections` instead.
- **Lists of short strings** in a cell or key line are `; `-separated. A list whose items contain `;` renders as nested bullets.
- **Booleans** are `yes` / `no`. An empty cell means the key is absent, `—` means null, `(none)` means an empty list.
- **Money:** `€90K`, `€300K–€500K`, `~€25K / month`, then ` · <status>`, then optionally ` · <footnote>`; `to be defined` for status `tbd`. Read back into `{value | range, currency, status, footnote}`.
- **Durations:** `6–8 weeks (target 8, hard cap 10)`, or `to be defined`.
- **Multi-line text** keeps its line breaks in `paragraph` form.

## An excerpt, from the real Account Insights values

```markdown
---
slug: account-insights
status: confirmed
spec_version: 2
---

# Account Insights

- **Site:** Account Insights
- **Internal slide:** Account Insights App
- **External:** Account insights
- **External subheading:** Accelerator App by SoftServe
- **Source:** user:2026-09-22

## One-liner

- **Full:** More opportunities from the companies you already track: the news, filings and updates on them become a named next move for each — scored, cited and reviewed before anything reaches your systems.
- **Short:** More opportunities from the companies you already track — found in the news, filings and updates on them.

## Problem and solution

### Problem

An account manager, a partnerships lead or a portfolio manager each covers dozens of companies and cannot keep up with the news, filings and updates landing on all of them.

### Solution

Each morning they see the handful of changes that matter across the companies they cover, what each one means and what to do about it, and review that list instead of assembling it.

## Capabilities

### Account universe & grounding

In-scope account list definition · System-of-record field mapping and account-framing extraction · Per-client catalog-of-moves capture · Signal-source selection and licensing review

| Category | Feature | Status | From tier | Note | Source |
|---|---|---|---|---|---|
| The account universe | Account universe — the in-scope companies, their tiering, the relationship framing from the system of record | partial | PoV | Extract at PoV Jumpstart; API at Integration | one-pager-2026-09-10, reviewer-ui-2026-09-11 |

## Packages

### PoV Jumpstart · S

- **Scope:** One signal set, one segment, files in and out: prove the reviewer agrees.
- **Duration:** 6–8 weeks (target 8, hard cap 10)
- **Services price:** to be defined
```

## Migration, each step green before the next

1. **One loader.** All twelve read sites and the linter load through `packspec.load`, still on YAML. The suite passes unchanged.
2. **The codec and the layout**, with round-trip tests on the five specs and strictness tests.
3. **Convert** the five specs to `pack-spec.md`. `.gitignore` whitelists `pack-spec.md`. The loader keeps reading `.yaml` for one release and says in one line that the file should be converted.
4. **The skills.** The spec skill writes through `packspec.py set` and opens `pack-spec.md` beside the conversation at the brief; `shared/schema/pack-spec.md` becomes the Markdown template; cards say `pack-spec.md`; `apply_choice.py` writes through the writer; the stamp hashes the canonical data.
5. **Remove** the YAML files.

## Acceptance

- The round trip is exact on all five specs.
- Every builder produces the same output from the `.md` as from the `.yaml`, compared on the fixture builds after stripping timestamps and stamps.
- A table row with a missing cell, an unknown heading and an unescaped pipe each fail with the right line number.
- The Account Insights spec renders on GitHub as a readable brief, checked once by eye.
