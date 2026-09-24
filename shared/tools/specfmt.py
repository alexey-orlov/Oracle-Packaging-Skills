"""How a spec value prints on an artifact — one home for every builder.

A price in the spec is a block `{value | range, currency, status, footnote}`. Every
artifact prints its amount the same way, in the delivered artifacts' own style:

    money_text({"value": 90000, "currency": "EUR"})               -> "€90K"
    money_text({"value": 2000000, "currency": "EUR"})             -> "€2M"
    money_text({"range": [300000, 500000], "currency": "EUR"})    -> "€300–500K"
    money_text({"range": [300000, 1500000], "currency": "EUR"})   -> "€300K–€1.5M"

What each artifact adds around the amount (a footnote mark, "~" for an indicative
figure, its own "to be defined" line) stays with that artifact's builder.
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
