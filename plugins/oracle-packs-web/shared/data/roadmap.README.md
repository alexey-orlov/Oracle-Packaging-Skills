# Roadmap extract — what these files are and how to use them

**generated: 2026-09-18** · regenerate with `python3 shared/tools/regen_roadmap.py`

Packs are mapped to items on SoftServe's Oracle AI use-case roadmap. The join
in the source material is free text with drift and no ids. These files are the
minimal versioned extract that gives a packaging skill a **stable id per
roadmap item**, so it can (a) look up the roadmap item a pack maps to and
(b) place a new pack on the map.

No customer name appears in any file here. Nothing outside this directory is
written by the regeneration script.

---

## The files

| File | Rows | Columns | What it is |
|---|---|---|---|
| `roadmap-items.csv` | 91 | `id,block,item,status,l1_pattern,l2_pattern` | The whole roadmap, one row per use case, with a minted stable id and the workflow-pattern taxonomy it sits under. All 91 items carry an L1/L2. |
| `roadmap-l2-patterns.csv` | 26 | `l1,l2,definition` | The 26 workflow sub-patterns and their definitions, verbatim from the source sheet. Definition shape: `<trigger> → <input> → <output>; human gate: …; agent acts: …`. |
| `pack-crosswalk.csv` | 9 | `pack_slug,pack_name_current,roadmap_item_id,site_slug,tracker_name,older_names` | The curated pack ↔ roadmap join, resolving the name drift between the tracker, the mini-site and the map. |
| `pack-tracker.csv` | 18 | `pack,artifact,status,due_date` | The per-pack artifact checklist as it stands in the tracker. Three packs × six artifacts. People columns are dropped on purpose. |

`status` on the roadmap is one of **Available** (packaged offering available),
**WinP** (WinP package), **Roadmap**. Today: 3 Available · 6 WinP · 82 Roadmap.

---

## The id rule

`id` is a kebab-case slug minted **deterministically from the item name**, never
from a row number — positional numbering breaks on any row insert, and the map
is re-grouped often.

1. Unicode NFKD normalise, drop combining marks, keep ASCII.
2. Lowercase and trim.
3. `" & "` (ampersand fenced by whitespace) becomes `" and "`.
4. Any remaining `&` and every apostrophe are deleted with **no** separator, so
   `Q&A` → `qa` and `customer's` → `customers`.
5. Every remaining run of non-`[a-z0-9]` collapses to a single `-`.
6. Leading and trailing `-` are stripped.

Worked examples:

| Item | id |
|---|---|
| `Large document extraction & validation` | `large-document-extraction-and-validation` |
| `Cross-system ERP Q&A` | `cross-system-erp-qa` |
| `Plan-vs-actual investigation` | `plan-vs-actual-investigation` |
| `Warehouse pick-path optimization` | `warehouse-pick-path-optimization` |

**Ids are a published contract.** Once an id is in `roadmap-items.csv`, the
regeneration script refuses to overwrite the file if a re-run would change it —
it prints the diff and exits 2. Changing one anyway needs
`--accept-id-changes`, and the change must be recorded here, in a
`## Id changes` section, with the date and why.

`pack_slug` follows the same shape rule but is **not** re-minted from the
current pack name: it reuses the mini-site slug where a listing exists, because
that string is already the handle for demo URLs, assets and step frames. For a
pack with no listing, mint it with the rule above and then leave it alone.

---

## Volatility — what to trust

- **Durable: the 91 items and their statuses.** Every competing re-grouping of
  the map opens with "same 91 items and statuses"; the item vocabulary survived
  a red-team pass and three slide variants.
- **Volatile: the 7 block names and their membership.** Six competing 8-block
  taxonomies were written within six minutes on 2026-09-17, each renaming or
  dissolving several current blocks; the mini-site already refuses two of the
  present names and uses its own category labels.
- **Volatile: `status`.** It moves week to week as packages land.
- **Cadence:** roughly weekly structural churn, daily during an active round.

**So: key on `id`. Treat `block` as a replaceable display label and never
hard-code a block name in a skill.** If a skill needs grouping, read `block`
from this file at run time; if it needs a durable grouping, use
`l1_pattern`/`l2_pattern`, which are the more stable taxonomy.

---

## Stating the version in an artifact

The map churns faster than any artifact built from it. **Every artifact a skill
produces that cites the roadmap must state which extract it used**, so a reader
can tell whether it is current. One line, in the artifact's own provenance or
footer:

```
Roadmap extract: 2026-09-18 (91 items) · source: AI use case roadmap 2026-09-17.md
```

Take the date from the `generated:` line at the top of this file and the row
count from `roadmap-items.csv`. If a skill cannot read this file, it must say
so and stop, not guess an item name — an unmapped use case is an abort, not an
invention.

---

## Sources

Read-only, on the practice's shared drive under `Projects/Oracle/Packs/` — point the
regenerator at it with `ORACLE_PACKS_DIR`. Their state when this extract was generated:

| Source | mtime at generation | Feeds |
|---|---|---|
| `Use case maps/AI use case roadmap 2026-09-17.md` | 2026-09-17 17:38 | `roadmap-items.csv` (block, item, status) |
| `Use case maps/AI workflow patterns - AIDP-NVIDIA-OracleAI mapping.xlsx` | 2026-09-17 13:34 | `roadmap-items.csv` (l1/l2, via the `Card labels v2` tab) and `roadmap-l2-patterns.csv` (via `Patterns v2 (red-team 2026-09)`, column "L2 definition") |
| `Oracle packages.xlsx` | 2026-09-15 18:55 | `pack-tracker.csv` (the `Packaging activities` tab only) |

The roadmap markdown is the **primary** source: it is the already-cleaned
version of the map and carries no customer names. The workbook is read for the
taxonomy only — the fit glyphs, the examples, the NVIDIA/Oracle service
columns, the red-team tab and both legend tabs are internal qualification IP
and are deliberately not extracted. The tracker's `GTM` tab and its hidden
`Sheet1` are never read.

---

## The join, and where it drifts

The source join is a free-text item name with a different vocabulary at every
hop. `pack-crosswalk.csv` is the curated resolution of that drift; the aliases
live in `CROSSWALK` and `CARD_TO_ITEM_ALIASES` in the regeneration script.

Four card labels differ from their roadmap item and are aliased explicitly:

| Card label (tag stripped) | Roadmap item |
|---|---|
| `Account insight briefings` | `Account insights` |
| `Technician shift scheduling` | `Workforce optimization` |
| `Contract metadata extraction` | `Large document extraction & validation` |
| `Warehouse pick-path optimisation` | `Warehouse pick-path optimization` |

`older_names` in the crosswalk is a `;`-separated list of every other string
this use case has gone by across the estate (tracker, mini-site, card labels,
work-split sheet). It exists so a free-text lookup has something to hit; it is
not a history.

Rows 4–9 of the crosswalk are the committed items (Available + WinP) that have
no pack in the tracker yet. Rows with an empty `pack_slug` and a `site_slug`
have a mini-site listing but no packaging effort; rows with both empty are WinP
items with neither. They are listed so "place a new pack on the map" has a
single file to read.

**Do not extend the crosswalk by guessing.** A new row needs a verified name
link, not a plausible one — the weakest join in the estate is a pack name with
zero textual overlap with its roadmap item.

---

## Customer-tag clearance

The card-label tab tags items with customer names in parentheses. Two
mechanisms keep them out of these files, and **neither writes the names down**
— a list of customer names in a shared repo is itself the disclosure the rule
exists to prevent:

1. **Strip by shape.** In the `Card labels v2` Card 1–5 columns every
   parenthetical is a customer tag, so all of them are removed. Parentheticals
   in the L1/L2 and definition columns are vocabulary
   (`Ambient scribe (meetings, clinical)`) and are left alone.
2. **Sweep by shape.** Every output cell is checked for a residual
   proper-noun-shaped parenthetical — all words capitalised, no comma, three
   words or fewer, not one of a small allow-list of technical acronyms. A hit
   fails the run with exit 3.

An exact-name second gate is available for a run that wants one:
`--deny-list FILE` (one lowercase name per line) or the
`ORACLE_PACK_DENYLIST` environment variable. **Keep that file outside this
repo and never commit it.**

If a card label ever gains a legitimate parenthetical, stripping it will break
that item's match and the run will report it as unmatched rather than guess.
Fix the alias table; do not relax the strip.

---

## Regenerating

```bash
python3 shared/tools/regen_roadmap.py --check     # parse and validate, write nothing
python3 shared/tools/regen_roadmap.py             # write the four CSVs
```

Standard library only; `openpyxl` is used when importable and the `.xlsx` is
read directly from its OOXML otherwise. Source paths resolve under
`$ORACLE_PACKS_DIR` (the folder in the table above) and can be overridden with
`--roadmap`, `--mapping`, `--tracker` and `--out`. With neither the variable nor
the flags the run stops and says so; it never writes an empty CSV.

Exit codes: `0` written · `1` a source is missing · `2` a published id would
change (diff printed, nothing written) · `3` a clearance or integrity check
failed.

After a successful run, update the `generated:` date and the source mtimes in
this file so an artifact citing the extract names the right version.

This file is rewritten to current truth on every change. Do not stack dated
"UPDATE" sections onto it.
