"""How a spec value prints on an artifact — one home for every builder.

A price in the spec is a block `{value | range, currency, status, footnote}`. Every
artifact prints its amount the same way, in the delivered artifacts' own style:

    money_text({"value": 90000, "currency": "EUR"})               -> "€90K"
    money_text({"value": 2000000, "currency": "EUR"})             -> "€2M"
    money_text({"range": [300000, 500000], "currency": "EUR"})    -> "€300–500K"
    money_text({"range": [300000, 1500000], "currency": "EUR"})   -> "€300K–€1.5M"

A package's duration prints its `duration_label` when the spec sets one, else weeks:

    duration_text({"duration_weeks": {"min": 4, "max": 8}})       -> "4–8 weeks"
    duration_text({"duration_label": "6 weeks, then monthly"})    -> "6 weeks, then monthly"

A metric with no cleared figure says FIGURELESS_PHRASE on the deck's tile and
FIGURELESS_CAVEAT under the one-pager's strip and the executive summary's proof block,
so the artifacts of one pack never disagree on tense (2026-09-23).

What each artifact adds around a value (a footnote mark, "~" for an indicative figure,
its own "to be defined" line, HTML escaping) stays with that artifact's builder.
"""
from __future__ import annotations

CURRENCY_SYMBOL = {"EUR": "€", "USD": "$", "GBP": "£"}


def currency_symbol(currency: str | None) -> str:
    code = (currency or "EUR").upper()
    return CURRENCY_SYMBOL.get(code, code + " ")


def short_amount(value) -> tuple[str, str]:
    """2000000 -> ("2", "M"); 1500000 -> ("1.5", "M"); 90000 -> ("90", "K"); 950 -> ("950", "")."""
    value = float(value)
    for div, unit in ((1_000_000, "M"), (1_000, "K")):
        if value >= div:
            scaled = value / div
            text = f"{scaled:.0f}" if abs(scaled - round(scaled)) < 1e-9 else f"{scaled:g}"
            return text, unit
    return f"{value:.0f}", ""


def money_text(block) -> str | None:
    """The amount of a price block as printed text, or None when it has no value or range."""
    if not isinstance(block, dict):
        return None
    sym = currency_symbol(block.get("currency"))
    if block.get("range"):
        low, high = block["range"]
        lo_n, lo_u = short_amount(low)
        hi_n, hi_u = short_amount(high)
        if lo_u == hi_u:
            return f"{sym}{lo_n}–{hi_n}{hi_u}"
        return f"{sym}{lo_n}{lo_u}–{sym}{hi_n}{hi_u}"
    if block.get("value") is not None:
        num, unit = short_amount(block["value"])
        return f"{sym}{num}{unit}"
    return None


FIGURELESS_PHRASE = "to be measured in the proof of value"
FIGURELESS_CAVEAT = "To be measured in the proof of value; results to follow."


def duration_text(tier) -> str | None:
    """How a package's duration prints, or None when the spec has none: `duration_label`
    as written, else `duration_weeks` — a {min, max, target} block or a bare number."""
    if not isinstance(tier, dict):
        return None
    if tier.get("duration_label"):
        return str(tier["duration_label"])
    weeks = tier.get("duration_weeks")
    if weeks in (None, "", {}):
        return None
    if not isinstance(weeks, dict):
        return f"{weeks} weeks"
    lo, hi, target = weeks.get("min"), weeks.get("max"), weeks.get("target")
    if lo and hi and lo != hi:
        return f"{lo}–{hi} weeks"
    single = target or lo or hi
    return f"{single} weeks" if single else None
