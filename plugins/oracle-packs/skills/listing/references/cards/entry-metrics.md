# The KPI band

**What this is.** `overview.metrics[]`: two or three tiles, each one business metric shown as its kind chip, one figure, one small chart, one line and its owner. Printed from the spec by `shared/tools/py tools/overview-data.py <spec>` and pasted as printed, never written by hand.

**The checks**

1. **One tile, one framed spec metric**: `name` → `title` (≤ 40 characters), `evidence` → `kind` (`proven`, `forecast` or `estimated`), `owner_role` → `owner` (≤ 40), `figure_prefix` + `figure` → `figure` (≤ 20 characters with two tiles, 14 with three), `chart` → `visual`, `label` → `line` (≤ 14 words).
2. **Two or three tiles**, no two sharing a claim shape. More on offer: the owner picks, `--only`. Fewer: the spec frames more (its `metrics-shown` card); never a figure-less, qualitative or placeholder tile.
3. **The frame is the honesty**: a proven tile prints its measured after (*~30 min*), an estimated one its *from X* baseline, its range or the gap it closes, never a modeled after. No footnote, method note, ROI paragraph, apology or pointer to another tab, and no `sources` key; where a figure comes from goes in the site's round record.
4. A metric the tool leaves off stays off, and the tool says why: a technical criterion (it rides the Jumpstart scope), no figure, not cleared for the site (`channels`), or no frame.
5. `value`, `label`, `qualifier` and `icon` are the retired rail tile and fail by name.

**Good.** *Time to plan a region's four weeks* · Proven · *~30 min*, its bars *~2 days before* and *~30 min after* · Owner · VP of field service. **Bad.** *Hours* over a method footnote.

**Fills / reads:** `kpis[]` — `name`, `evidence`, `owner_role`, `figure`, `figure_prefix`, `chart`, `label`, `channels`.
