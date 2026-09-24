# Roadmap extract — what these files are and how to use them

**generated: 2026-09-22** · regenerate with `python3 shared/tools/regen_roadmap.py`

Packs are mapped to items on SoftServe's Oracle AI use-case roadmap. The join
in the source material is free text with drift and no ids. `roadmap-items.csv`
is the minimal versioned extract that gives a packaging skill a **stable id per
roadmap item**, so it can (a) look up the roadmap item a pack maps to and
(b) place a new pack on the map. The spec's `roadmap_item_id` must be an id in
it (`lint_spec.py`, SPEC005).

No customer name appears in any file here. Nothing outside this directory is
written by the regeneration script.

---

## The files

| File | Rows | Columns | What it is |
|---|---|---|---|
| `roadmap-items.csv` | 91 | `id,block,item,status,l1_pattern,l2_pattern` | The whole roadmap, one row per use case, with a minted stable id and the workflow-pattern taxonomy it sits under. All 91 items carry an L1/L2. `block` holds the current six-block grouping plus the two unpackaged families — see "The blocks" below. |

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

## The blocks

Since 2026-09-22 the map is grouped into **six blocks**, chosen so that each cuts
on a single axis and no use case is a judgement call between two of them:

| Block | Items | What puts a use case here |
|---|---|---|
| Enterprise knowledge & analytics | 18 | Someone asks; the agent answers from governed documents or a governed schema. Nothing written back. |
| Deep research & investigation | 18 | A question too big for one answer — the agent plans, gathers across sources, returns an evidence set a person signs off. |
| Transaction & process execution | 15 | The agent changes something in a system of record: a transaction, a queue item, a multi-week process. |
| Document processing | 14 | An item arrives and is worked one by one — read, classified, checked against a reference, transformed at volume. |
| Forecasting & optimization | 9 | The answer is computed, not retrieved: a score, a forecast, the next period's plan under constraints. |
| Video & image intelligence | 4 | The input is pixels. |

All 3 Available and all 6 WinP items sit inside these six. The remaining **13
items carry a family name instead of a block** — real demand with no packaged
offering behind it, kept on the map so nothing is silently dropped:
`Content generation` (7) and `Monitoring & incident response` (6). A skill that
renders "the blocks" should render the six and treat those two as a remainder,
not as blocks seven and eight.

The two are out on purpose. Content generation is a different business
(marketing and enablement, not operations); monitoring splits across the blocks
above by its own nature — the watching is analytics, the fixing is execution —
and forcing it into one reintroduces exactly the boundary overlap the six-block
cut removed.

## Volatility — what to trust

- **Durable: the 91 items and their statuses.** Every competing re-grouping of
  the map opens with "same 91 items and statuses"; the item vocabulary survived
  a red-team pass and three slide variants.
- **Settling, not settled: the block names and their membership.** The six
  above replaced seven different ones on 2026-09-22 and are the first grouping
  the owner converged on rather than commissioned — but the seven they replaced
  had themselves survived three slide variants, six competing 8-block
  taxonomies were written within six minutes on 2026-09-17, and the mini-site
  still uses its own category labels. Assume the names move again.
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
Roadmap extract: 2026-09-22 (91 items) · source: AI use case roadmap 2026-09-22.md
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
| `Use case maps/AI use case roadmap 2026-09-22.md` | 2026-09-22 23:00 | `roadmap-items.csv` (block, item, status) |
| `Use case maps/AI workflow patterns - AIDP-NVIDIA-OracleAI mapping.xlsx` | 2026-09-17 13:34 | `roadmap-items.csv` (l1/l2, via the `Card labels v2` tab) |

The roadmap markdown is the **primary** source: it is the already-cleaned
version of the map and carries no customer names. It is dated per re-grouping,
so `DEFAULT_ROADMAP` in the regeneration script moves with it; earlier dated
files stay on the drive as the record of what a past artifact cited. Its use-case
table is read by its `| Block | Item | Status |` header, and a run stops if the
file has no such table or more than one — the file's other tables (block counts,
the unpackaged remainder) are narrative and must not be parsed as use cases. The workbook is read for the
taxonomy only — the fit glyphs, the examples, the NVIDIA/Oracle service
columns, the red-team tab and both legend tabs are internal qualification IP
and are deliberately not extracted.

---

## The join, and where it drifts

The source join is a free-text item name with a different vocabulary at every
hop. The aliases live in `CARD_TO_ITEM_ALIASES` in the regeneration script.

Four card labels differ from their roadmap item and are aliased explicitly:

| Card label (tag stripped) | Roadmap item |
|---|---|
| `Account insight briefings` | `Account insights` |
| `Technician shift scheduling` | `Workforce optimization` |
| `Contract metadata extraction` | `Large document extraction & validation` |
| `Warehouse pick-path optimisation` | `Warehouse pick-path optimization` |

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
python3 shared/tools/regen_roadmap.py             # write roadmap-items.csv
```

Standard library only; `openpyxl` is used when importable and the `.xlsx` is
read directly from its OOXML otherwise. Source paths resolve under
`$ORACLE_PACKS_DIR` (the folder in the table above) and can be overridden with
`--roadmap`, `--mapping` and `--out`. With neither the variable nor
the flags the run stops and says so; it never writes an empty CSV.

Exit codes: `0` written · `1` a source is missing · `2` a published id would
change (diff printed, nothing written) · `3` a clearance or integrity check
failed.

After a successful run, update the `generated:` date and the source mtimes in
this file so an artifact citing the extract names the right version.

This file is rewritten to current truth on every change. Do not stack dated
"UPDATE" sections onto it.
