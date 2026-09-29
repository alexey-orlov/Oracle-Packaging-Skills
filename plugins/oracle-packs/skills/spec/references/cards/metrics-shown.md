# How a metric is shown

**What this is.** What lets every artifact show a metric as a visual instead of explaining it.

**The checks**

1. **One kind word** (`evidence`): `proven`, measured end to end on the customer's own data, in a completed proof of value or delivery (`pov_result`, `delivered_result`); `forecast`, modeled on the customer's own history (`modeled`); `estimated`, set against a published rate or today's way of working (`benchmark`), or modeled on industry figures. The word is the disclaimer.
2. **A frame, never a promise.** The figure is a measured before → after (proven prints its after, *~30 min*), a range, a dumbbell's two ends (*3.0 → 2.4%*) or a *from X* baseline (`figure_prefix` `from`); an estimate never prints a modeled after alone. Never a bare word (*Hours*), a target, a delivery time, a feature.
3. **A chart that prints its own numbers** (`chart`): `form` (`compression`, `dumbbell`, `range` or `baseline`), `unit`, `scale` as `min–max`, `before`, then `after` or `range`, each `<value> · <label>` on the scale; `direction` only where it counts another quantity (a saving drawn as its cost). A baseline's scale runs past X (about 1.5 × X); a word label takes a value that only sets its bar.
4. **Shown, not explained.** Title ≤ 40 characters (`name`), owner ≤ 40 (`owner_role`), one line ≤ 14 words (`label`), figure ≤ 20. No footnote, method note or pointer to another page.
5. **Sourced, not printed.** A range or a baseline rests on the pack's figure or a page that was read, named in `source`.
6. **Two or three shown.** No defensible number: `-`, off the tiles.

**Good.** *Planning time* · proven · *~30 min*, from `2880 · ~2 days before` to `30 · ~30 min after`. **Bad.** *Hours* over a method footnote.

**Fills:** `kpis[].evidence`, `kpis[].chart`, `kpis[].figure_prefix`, `kpis[].label`.
