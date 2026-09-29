#!/usr/bin/env python3
"""How a shown metric is drawn: its one-word kind, its figure and a small chart, read once.

A pack spec carries the frame on every metric it shows — `kpis[].evidence` and `kpis[].chart`
beside `name`, `owner_role`, `label`, `direction`, `figure`, `figure_prefix` and
`figure_status`. The rule and its checks are the spec skill's `metrics-shown` card.
lint_spec.py (SPEC032-SPEC035) and the listing's tools/overview-data.py both read the frame
through this module, so a chart the linter passes is the chart the site's KPI band draws.

The chart's own syntax, one text value per key:

    form      compression · dumbbell · range · baseline
    unit      what the scale counts ("minutes to an approved plan")
    direction up or down, only where the chart counts another quantity than the metric's
              name (a saving drawn as the cost it cuts); else the metric's own `direction`
    scale     <min>–<max>                    0–2880
    before  <value> · <label>               2880 · ~2 days before
    after   <value> · <label>               30 · ~30 min after     (compression, dumbbell)
    range   <lo>–<hi> · <label>             4–10 · +4% to +10%     (range)

Values are plain magnitudes on the scale: no sign, no thousands separator; an en dash, a
hyphen or "to" between two of them. The label carries the sign and the words; `direction`
(up or down, the way the number improves) carries which way is better. Where a label is a
word ("a quarter", "hours"), its value only sets the mark's length and prints nowhere.

Dependency-free, so any interpreter the plugin resolves can import it.
"""

from __future__ import annotations

import re

EVIDENCE = ("proven", "forecast", "estimated")

# The figure_status each kind may stand on (the card's first check). Proven: measured end to
# end on the customer's own data, in a completed proof of value or in delivery. Forecast:
# modeled on the customer's own history. Estimated: set against a published rate or the way
# the work is done today (`benchmark`), or modeled on industry assumptions. A target is a
# promise, not evidence, and is never shown.
EVIDENCE_STATUS = {
    "proven": ("pov_result", "delivered_result"),
    "forecast": ("modeled",),
    "estimated": ("modeled", "benchmark"),
}

FORMS = ("compression", "dumbbell", "range", "baseline")

# The tile's shape on the site's KPI band (site contract round 20; the card's shape check).
TITLE_MAX = 40
OWNER_MAX = 40
LINE_WORDS = 14
PREFIX_MAX = 6
FIGURE_MAX = {2: 20, 3: 14}         # characters, by the number of tiles on the band
BAND_MIN, BAND_MAX = 2, 3

EMPTY = {"", "-", "--", "—", "–", "n/a"}

_NUM = r"\d+(?:\.\d+)?"
_SEP = r"\s*(?:–|—|-|\bto\b)\s*"
_PAIR = re.compile(r"^\s*(%s)%s(%s)\s*$" % (_NUM, _SEP, _NUM))
_MARK = re.compile(r"^\s*(%s)\s*·\s*(\S.*?)\s*$" % _NUM)
_BAND = re.compile(r"^\s*(%s)%s(%s)\s*·\s*(\S.*?)\s*$" % (_NUM, _SEP, _NUM))

_UP = {"↑", "up", "higher", "increase", "increases", "rise", "rises"}
_DOWN = {"↓", "down", "lower", "decrease", "decreases", "fall", "falls"}


def text(value) -> str:
    """The value as stripped text, or "" for absent and for the `-` that means empty."""
    if value is None or isinstance(value, (dict, list)):
        return ""
    out = str(value).strip()
    return "" if out.lower() in EMPTY else out


def _number(raw: str):
    return float(raw) if "." in raw else int(raw)


def words(value: str) -> int:
    """Whitespace-separated words, as the site's checker counts them."""
    return len(value.split())


def _way(raw) -> str:
    raw = text(raw).lower()
    if raw in _UP:
        return "up"
    if raw in _DOWN:
        return "down"
    return ""


def direction(kpi: dict) -> str:
    """`up` or `down`, the way the chart's number improves: the chart's own `direction` where it
    counts another quantity than the metric's name, else the metric's (↑ / ↓ / up / down …)."""
    chart = kpi.get("chart")
    if isinstance(chart, dict) and text(chart.get("direction")):
        return _way(chart.get("direction"))
    return _way(kpi.get("direction"))


def kind(kpi: dict) -> str:
    """business | leading | technical; absent means business (shared/schema/pack-spec.md)."""
    return text(kpi.get("kind")).lower() or "business"


def evidence(kpi: dict) -> str:
    return text(kpi.get("evidence")).lower()


def has_figure(kpi: dict) -> bool:
    return bool(text(kpi.get("figure")))


def is_framed(kpi: dict) -> bool:
    """The metric declares how it is shown: a kind word and a chart record."""
    return bool(evidence(kpi)) and isinstance(kpi.get("chart"), dict)


def cleared_for(kpi: dict, channel: str) -> bool:
    """A metric with a `channels` list is cleared for those channels only."""
    chans = kpi.get("channels")
    if isinstance(chans, list) and chans:
        return channel in [str(c).strip() for c in chans]
    return True


def slug(name: str) -> str:
    out = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return out or "metric"


def evidence_problems(kpi: dict) -> list[tuple[str, str]]:
    """(key, message) for a kind word that is unknown or that the figure cannot stand on."""
    ev = evidence(kpi)
    if not ev:
        return []
    if ev not in EVIDENCE:
        return [("evidence", "`%s` is not one of %s" % (kpi.get("evidence"), " | ".join(EVIDENCE)))]
    if not has_figure(kpi):
        return [("evidence", "`%s` on a metric with no figure: a kind word qualifies a number, "
                             "and a metric with none is not shown" % ev)]
    status = text(kpi.get("figure_status"))
    allowed = EVIDENCE_STATUS[ev]
    if status and status not in allowed:
        return [("evidence", "`%s` needs figure_status %s, not `%s` — %s"
                 % (ev, " or ".join(allowed), status, {
                     "proven": "proven is measured end to end on the customer's own data, in a "
                               "completed proof of value or in delivery",
                     "forecast": "a forecast is modeled on the customer's own history",
                     "estimated": "an estimate is set against a published rate or today's way "
                                  "of working, or modeled on industry assumptions; a target is a "
                                  "promise and is never shown",
                 }[ev]))]
    return []


def read(kpi: dict):
    """(visual, problems): the site's `visual` for this metric's chart, or None, and a list of
    (key, message) naming each part of the chart that does not read or does not draw its own
    numbers."""
    chart = kpi.get("chart")
    if not isinstance(chart, dict):
        return None, [("chart", "no chart record")]
    probs = []
    form = text(chart.get("form")).lower()
    if form not in FORMS:
        return None, [("chart.form", "`%s` is not one of %s" % (chart.get("form"), " | ".join(FORMS)))]
    unit = text(chart.get("unit"))
    if not unit:
        probs.append(("chart.unit", "missing — name what the scale counts"))
    way = direction(kpi)
    if not way:
        own = text(chart.get("direction"))
        probs.append(("chart.direction" if own else "direction",
                      "`%s` does not say which way the number improves — up or down (↑ / ↓)"
                      % (own or kpi.get("direction") or "")))

    lo = hi = None
    m = _PAIR.match(text(chart.get("scale")))
    if not m:
        probs.append(("chart.scale", "`%s` is not <min>–<max>, two plain numbers"
                      % (chart.get("scale") or "")))
    else:
        lo, hi = _number(m.group(1)), _number(m.group(2))
        if not hi > lo:
            probs.append(("chart.scale", "`%s` — its max must be above its min" % chart.get("scale")))
            lo = hi = None

    def on_scale(v):
        return lo is None or (lo <= v <= hi)

    def mark(key):
        raw = text(chart.get(key))
        if not raw:
            probs.append(("chart." + key, "missing — a %s chart draws its %s mark, with its label"
                          % (form, key)))
            return None
        mm = _MARK.match(raw)
        if not mm:
            probs.append(("chart." + key, "`%s` is not <value> · <label>" % raw))
            return None
        value = _number(mm.group(1))
        if not on_scale(value):
            probs.append(("chart." + key, "%s is off the scale %s–%s" % (mm.group(1), lo, hi)))
        return {"value": value, "label": mm.group(2)}

    before = mark("before")
    after = band = None
    if form in ("compression", "dumbbell"):
        after = mark("after")
        if form == "compression" and before and not before["value"] > 0:
            probs.append(("chart.before", "a compression's before must be above 0 — the after "
                                          "bar is drawn as its share of it"))
        elif form == "compression" and before and after and not after["value"] < before["value"]:
            probs.append(("chart.after", "%s is not below the before (%s) — a compression draws "
                                         "the after as a share of the before"
                          % (after["value"], before["value"])))
    elif text(chart.get("after")):
        probs.append(("chart.after", "a %s draws no after mark — only compression and dumbbell do"
                      % form))
    if form == "range":
        raw = text(chart.get("range"))
        mb = _BAND.match(raw)
        if not mb:
            probs.append(("chart.range", ("`%s` is not <lo>–<hi> · <label>" % raw) if raw
                          else "missing — a range chart draws the band, with its label"))
        else:
            blo, bhi = _number(mb.group(1)), _number(mb.group(2))
            if not bhi > blo:
                probs.append(("chart.range", "its hi must be above its lo"))
            elif not (on_scale(blo) and on_scale(bhi)):
                probs.append(("chart.range", "%s–%s is off the scale %s–%s"
                              % (mb.group(1), mb.group(2), lo, hi)))
            band = {"lo": blo, "hi": bhi, "label": mb.group(3)}
    elif text(chart.get("range")):
        probs.append(("chart.range", "a %s draws no band — only range does" % form))
    if form == "baseline" and before and lo is not None and way and (
            (way == "down" and before["value"] >= hi) or (way == "up" and before["value"] <= lo)):
        probs.append(("chart.scale", "ends at today's value, so the baseline draws a full bar with "
                                     "nowhere to go — run the scale past it (about 1.5 × the value)"))
    if probs:
        return None, probs
    visual = {"form": form, "unit": unit, "direction": way,
              "scale": {"min": lo, "max": hi}, "before": before}
    if after:
        visual["after"] = after
    if band:
        visual["range"] = band
    return visual, []


def figure(kpi: dict) -> dict:
    """The tile's `figure`: the prefix set small, then the figure and any suffix."""
    out = {}
    prefix = text(kpi.get("figure_prefix"))
    if prefix:
        out["prefix"] = prefix
    body = text(kpi.get("figure"))
    suffix = text(kpi.get("figure_suffix"))
    out["text"] = (body + " " + suffix).strip() if suffix else body
    return out


def shape_problems(kpi: dict) -> list[tuple[str, str]]:
    """(key, message) where a shown metric breaks the tile's shape."""
    probs = []
    fig = figure(kpi)
    if fig["text"] and not re.search(r"\d", fig["text"]) and fig.get("prefix", "").lower() != "from":
        probs.append(("figure", "`%s` is a bare word — a figure is a measured before → after, a "
                                "range, or a from-X baseline (figure_prefix `from`), never a word "
                                "that reads as a promise" % fig["text"]))
    chart = kpi.get("chart") if isinstance(kpi.get("chart"), dict) else {}
    after = _MARK.match(text(chart.get("after")))
    if (evidence(kpi) in ("forecast", "estimated") and text(chart.get("form")).lower() == "compression"
            and after and fig["text"] and fig["text"].lower() in after.group(2).lower()):
        probs.append(("figure", "`%s` prints the modeled after alone — an estimate shows its baseline "
                                "(figure_prefix `from` and the before), or the gap it closes"
                      % fig["text"]))
    if len(fig.get("prefix", "")) > PREFIX_MAX:
        probs.append(("figure_prefix", "`%s` is over %d characters — it sets small beside the figure"
                      % (fig["prefix"], PREFIX_MAX)))
    if len(fig["text"]) > FIGURE_MAX[BAND_MIN]:
        probs.append(("figure", "`%s` is %d characters — the band sets at most %d (%d with three tiles)"
                      % (fig["text"], len(fig["text"]), FIGURE_MAX[2], FIGURE_MAX[3])))
    name = text(kpi.get("name"))
    if len(name) > TITLE_MAX:
        probs.append(("name", "is %d characters — the tile's title takes %d" % (len(name), TITLE_MAX)))
    owner = text(kpi.get("owner_role"))
    if not owner:
        probs.append(("owner_role", "missing — the tile prints the buyer-side role who tracks it"))
    elif len(owner) > OWNER_MAX:
        probs.append(("owner_role", "is %d characters — the tile takes %d" % (len(owner), OWNER_MAX)))
    line = text(kpi.get("label"))
    if not line:
        probs.append(("label", "missing — the tile's one line: what the figure counts"))
    elif words(line) > LINE_WORDS:
        probs.append(("label", "is %d words — the tile's one line takes %d" % (words(line), LINE_WORDS)))
    return probs


_SMALL = {"a", "an", "and", "as", "at", "by", "for", "in", "of", "on", "or", "per", "the", "to", "with"}


def sentence_case(value: str) -> str:
    """"Head of Claims" -> "Head of claims": the site sets every string in sentence case. Only a
    Title Case string is changed, every word but the small ones capitalized, so a sentence-case
    one keeps its proper nouns ("Head of Oracle operations"); a word with a capital after its
    first letter or a digit (VP, COO, FP&A, 3PL) is kept as written. A proper noun inside a
    Title Case string is lowered with the rest: the owner reads the entry before it ships."""
    words_ = value.split(" ")
    titled = [w for w in words_[1:] if w[:1].isalpha() and w.lower() not in _SMALL]
    if not titled or not all(w[:1].isupper() for w in titled):
        return value
    out = []
    for i, w in enumerate(words_):
        keep = i == 0 or any(ch.isupper() for ch in w[1:]) or any(ch.isdigit() for ch in w)
        out.append(w if keep else w[:1].lower() + w[1:])
    return " ".join(out)


def sentence(value: str) -> str:
    """A label written to follow a figure ("saved when a correct call …") as the line under a
    chart: its first letter capital, a full stop at its end."""
    value = value.strip()
    if not value:
        return value
    value = value[0].upper() + value[1:]
    return value if value[-1] in ".!?" else value + "."


def tile(kpi: dict):
    """(tile, problems): the site's `overview.metrics[]` entry for one shown metric, or None."""
    probs = evidence_problems(kpi) + shape_problems(kpi)
    if not evidence(kpi):
        probs.append(("evidence", "missing — the one-word kind: proven, forecast or estimated"))
    visual, chart_probs = read(kpi)
    probs += chart_probs
    if probs:
        return None, probs
    name = text(kpi.get("name"))
    return {
        "key": slug(name),
        "title": sentence_case(name),
        "kind": evidence(kpi),
        "owner": sentence_case(text(kpi.get("owner_role"))),
        "figure": figure(kpi),
        "visual": visual,
        "line": sentence(text(kpi.get("label"))),
    }, []
