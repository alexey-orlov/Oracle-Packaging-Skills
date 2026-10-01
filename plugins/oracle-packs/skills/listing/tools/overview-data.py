#!/usr/bin/env python3
"""overview-data.py — the Overview parts that come from data, never from copy: the KPI band
(`overview.metrics[]`) from the spec's framed metrics, and each step's `shot` from the site's
frame capture.

    shared/tools/py tools/overview-data.py packs/<slug>/pack-spec.md
    shared/tools/py tools/overview-data.py <spec> --only <key>,<key>[,<key>]
    shared/tools/py tools/overview-data.py <spec> --shots <capture out>/shots.json

It prints one JSON object, `{"metrics": [...]}`, plus `"steps": [{"n", "shot"}, ...]` with
--shots. Paste each part into the entry as printed — the band and the shots are never retyped,
because a tile's numbers are the spec's claims and a region is a measurement.

THE BAND (site contract round 20). A tile is `{key, title, kind, owner, figure, visual, line}`,
read from one spec metric through shared/tools/kpichart.py, the reader lint_spec.py uses:
`name` → title, `evidence` → kind, `owner_role` → owner, `figure_prefix` + `figure` (+ suffix)
→ figure, `chart` + `direction` → visual, `label` → line; the key is the name, slugged. A
metric goes on the band when it is a business metric with a figure, cleared for the customer
site (`channels`), and framed (`evidence` and `chart`, the spec skill's `metrics-shown` card).
Every other metric is named on stderr with why it stays off. The band holds two or three: with
more framed, --only picks them, in the order given. Nothing here writes a footnote, a method
or a source: where a figure comes from stays in the spec and in the site's round record.

THE SHOTS. --shots reads the `shots.json` the site's own capture writes (its docs.assets §1:
one `{n, region, anchor, alt}` per step, region and anchor measured at capture) and returns
each step's `shot`, its two paths fixed by the slug and the step number.

EXIT CODES
    0 printed · 1 refused: a framed metric that breaks its tile, fewer than two tiles, more
    than three without --only, an --only key not on offer, or a shots file that does not
    read — each named, with the spec key to fix, and nothing printed on stdout · 2 input not
    found or malformed · 3 PyYAML missing (an environment condition, not a result: retry).
"""

import argparse
import json
import os
import sys

CHANNEL = "customer_site"
ANCHORS = ("tl", "tr", "bl", "br")
STEPS_MIN, STEPS_MAX = 3, 5


def _shared_tools():
    """The plugin's shared/tools/ (the spec loader and the frame reader live there)."""
    here = os.path.dirname(os.path.abspath(__file__))
    parents = [here]
    while os.path.dirname(parents[-1]) != parents[-1]:
        parents.append(os.path.dirname(parents[-1]))
    for up in range(3, 7):                  # tools/ -> skill/ -> skills/ -> plugin/ (and the bundle)
        if len(parents) <= up:
            break
        shared = os.path.join(parents[up], "shared", "tools")
        if os.path.isfile(os.path.join(shared, "kpichart.py")):
            if shared not in sys.path:
                sys.path.insert(0, shared)
            return shared
    print("overview-data: shared/tools/kpichart.py not found above %s" % here, file=sys.stderr)
    raise SystemExit(2)


def load_spec(path):
    if not os.path.exists(path):
        print("overview-data: not found: %s" % path, file=sys.stderr)
        raise SystemExit(2)
    if path.endswith(".json"):
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    try:
        import yaml  # type: ignore  # noqa: F401  (the spec loader needs it)
    except ImportError:
        print("overview-data: PyYAML is not installed in this interpreter — an environment "
              "condition, not a result. Run through shared/tools/py, or install it; nothing was "
              "read.", file=sys.stderr)
        raise SystemExit(3)
    import packspec
    try:
        return packspec.load(path)[0]
    except packspec.SpecError as err:
        print("overview-data: the spec does not parse: %s" % err, file=sys.stderr)
        raise SystemExit(2)


def band(spec, only):
    """(tiles, refusals, notes)."""
    import kpichart as K
    kpis = spec.get("kpis") if isinstance(spec, dict) else None
    tiles, refusals, notes = [], [], []
    for kpi in kpis if isinstance(kpis, list) else []:
        if not isinstance(kpi, dict):
            continue
        name = K.text(kpi.get("name")) or "(unnamed)"
        where = 'kpis["%s"]' % name
        if K.kind(kpi) != "business":
            notes.append("off the band: %s — a %s metric; tiles are business metrics"
                         % (name, K.kind(kpi)))
            continue
        if not K.has_figure(kpi):
            notes.append("off the band: %s — no figure; a metric with no defensible number is "
                         "never a tile" % name)
            continue
        if not K.cleared_for(kpi, CHANNEL):
            notes.append("off the band: %s — its channels do not include %s" % (name, CHANNEL))
            continue
        if not K.is_framed(kpi):
            notes.append("off the band: %s — no evidence or no chart in the spec (the spec "
                         "skill's metrics-shown card)" % name)
            continue
        tile, probs = K.tile(kpi)
        if probs:
            refusals += ["%s.%s %s" % (where, key, msg) for key, msg in probs]
            continue
        tiles.append(tile)
    keys = [t["key"] for t in tiles]
    dupes = sorted({k for k in keys if keys.count(k) > 1})
    if dupes:
        refusals.append("two metrics slug to the same key (%s) — rename one in the spec"
                        % ", ".join(dupes))
    if refusals:
        return [], refusals, notes
    if only:
        by_key = {t["key"]: t for t in tiles}
        missing = [k for k in only if k not in by_key]
        if missing:
            return [], ["--only names %s, not a framed metric on offer (%s)"
                        % (", ".join(missing), ", ".join(keys) or "none")], notes
        tiles = [by_key[k] for k in only]
    if len(tiles) < K.BAND_MIN:
        return [], ["%d framed metric(s) on offer — the KPI band shows %d or %d. Frame more in "
                    "the spec (evidence and chart, the spec skill's metrics-shown card); never "
                    "fill the band with a figure-less tile" % (len(tiles), K.BAND_MIN, K.BAND_MAX)], notes
    if len(tiles) > K.BAND_MAX:
        return [], ["%d framed metrics on offer — the band takes %d or %d: pass --only with the "
                    "keys to show, in order (%s)" % (len(tiles), K.BAND_MIN, K.BAND_MAX,
                                                     ", ".join(t["key"] for t in tiles))], notes
    limit = K.FIGURE_MAX[len(tiles)]
    long = ['%s figure "%s" is %d characters — %d tiles set at most %d'
            % (t["key"], t["figure"]["text"], len(t["figure"]["text"]), len(tiles), limit)
            for t in tiles if len(t["figure"]["text"]) > limit]
    if long:
        return [], long, notes
    return tiles, [], notes


def shots(path, slug):
    """(steps, refusals): `[{"n", "shot"}]` from the site capture's shots.json."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            rows = json.load(fh)
    except FileNotFoundError:
        print("overview-data: not found: %s" % path, file=sys.stderr)
        raise SystemExit(2)
    except ValueError as err:
        print("overview-data: %s is not JSON: %s" % (path, err), file=sys.stderr)
        raise SystemExit(2)
    if not isinstance(rows, list):
        return [], ["%s is not a list of {n, region, anchor, alt}" % path]
    out, refusals = [], []
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("n"), int):
            refusals.append("a row with no step number n: %s" % json.dumps(row)[:80])
            continue
        n, region = row["n"], row.get("region")
        if not (isinstance(region, list) and len(region) == 4
                and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in region)):
            refusals.append("step %d: region is not four numbers [x, y, w, h]" % n)
        elif (not all(0 <= v <= 100 for v in region) or not (region[2] > 0 and region[3] > 0)
              or region[0] + region[2] > 100 or region[1] + region[3] > 100):
            refusals.append("step %d: region %s is not inside the frame — percent of it, 0–100, "
                            "with an area" % (n, region))
        if row.get("anchor") not in ANCHORS:
            refusals.append("step %d: anchor %r is not %s" % (n, row.get("anchor"), " / ".join(ANCHORS)))
        if not str(row.get("alt") or "").strip():
            refusals.append("step %d: no alt — what the screen shows" % n)
        stem = "assets/img/steps/%s-%d" % (slug, n)
        out.append({"n": n, "shot": {"full": stem + ".jpg", "zoom": stem + "-zoom.jpg",
                                     "region": region, "anchor": row.get("anchor"),
                                     "alt": str(row.get("alt") or "").strip()}})
    numbers = sorted(s["n"] for s in out)
    if numbers != list(range(1, len(numbers) + 1)):
        refusals.append("the steps are numbered %s — they run 1, 2, 3 … with none skipped"
                        % numbers)
    if not STEPS_MIN <= len(out) <= STEPS_MAX:
        refusals.append("%d steps captured — How it works shows %d to %d"
                        % (len(out), STEPS_MIN, STEPS_MAX))
    return sorted(out, key=lambda s: s["n"]), refusals


def main():
    ap = argparse.ArgumentParser(prog="overview-data.py", description=__doc__.split("\n\n")[0])
    ap.add_argument("spec", help="packs/<slug>/pack-spec.md")
    ap.add_argument("--only", default="", help="the band's keys, comma-separated, in order")
    ap.add_argument("--shots", default="", help="the site capture's shots.json")
    ap.add_argument("--slug", default="", help="the product slug (default: the spec's slug)")
    args = ap.parse_args()

    _shared_tools()
    spec = load_spec(args.spec)
    slug = args.slug or str(((spec or {}).get("meta") or {}).get("slug") or "").strip()
    only = [k.strip() for k in args.only.split(",") if k.strip()]

    tiles, refusals, notes = band(spec, only)
    out = {"metrics": tiles}
    if args.shots:
        if not slug:
            print("overview-data: no slug — the spec has no meta.slug; pass --slug", file=sys.stderr)
            raise SystemExit(2)
        steps, shot_refusals = shots(args.shots, slug)
        refusals += shot_refusals
        out["steps"] = steps
    for line in notes:
        print("overview-data: " + line, file=sys.stderr)
    if refusals:
        for line in refusals:
            print("overview-data: refused — " + line, file=sys.stderr)
        print("overview-data: nothing printed; fix the spec through the spec skill (or re-capture "
              "the frames), then run this again", file=sys.stderr)
        raise SystemExit(1)
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
