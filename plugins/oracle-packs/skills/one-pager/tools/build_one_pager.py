#!/usr/bin/env python3
"""Build the Oracle accelerator-pack sales one-pager: pack spec -> HTML -> one A4 PDF.

Reads a signed-off pack spec (shared/schema/pack-spec.md), renders
assets/one-pager-template.html, then prints the page to PDF with headless Chrome
and asserts the result is exactly one A4 page. More than one page is a failure,
not a warning: the one-pager is always one A4 page (Alex, 2026-09-18), so the
tool exits non-zero and names the blocks that are over their word budget, for the
skill to propose cuts.

Usage
    build_one_pager.py <pack-spec.yaml> --out <dir> [--channel partner_print|internal]
                       [--hero <image>] [--no-pdf]

Exit codes
    0  one A4 page, clearance clean
    1  usage / spec error (missing required key, unresolvable capability level)
    2  clearance violation (a name this channel may not carry reached the page)
    3  the PDF is longer than one page  -> cut content, see the listed blocks
    4  no Chrome/Chromium found; the HTML was written but nothing was verified

Dependencies: pyyaml, pypdf (see plugins/oracle-packs/requirements.txt).
"""

from __future__ import annotations

import argparse
import base64
import html
import mimetypes
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("build_one_pager: pyyaml is required -- pip install -r plugins/oracle-packs/requirements.txt")

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "assets" / "one-pager-template.html"

CHANNELS = ("partner_print", "internal")

# ---------------------------------------------------------------------------
# Word budgets, measured block by block on the Workforce Optimization reference
# one-pager (2026-07-17). The reference count is in references/one-pager-anatomy.md;
# the budget here is that count plus a little headroom. Whole page: 450 words.
# ---------------------------------------------------------------------------
BUDGETS = {
    "hero.h1": 4,
    "hero.h1-sub": 5,
    "hero.sub": 20,
    "problem.para": 22,
    "problem.bullets": 34,
    "solution.heading": 10,
    "solution.para": 38,
    "solution.chips": 12,
    "data-flow": 40,
    "sell.bullets": 54,
    "sell.chips": 22,
    "proof.story": 48,
    "proof.stats": 50,
    "proof.caveat": 14,
    "packages.table": 95,
    "packages.notes": 16,
    "disclaimer": 16,
    "cta.q": 10,
    "cta.a": 18,
    "PAGE TOTAL": 470,
}

GLYPH = {
    "none": ('&mdash;', "dot none"),
    "partial": ('&#9680;', "dot"),          # ◐
    "included": ('&#9679;', "dot"),         # ●
    "advanced": ('&#9679;&#9679;', "dot"),  # ●●
}
GLYPH_BY_CHAR = {"—": "none", "-": "none", "–": "none", "○": "none",
                 "◐": "partial", "●●": "advanced", "●": "included"}
LEGEND = "&#9680; partial &nbsp;&nbsp; &#9679; included &nbsp;&nbsp; &#9679;&#9679; multi-region / advanced"
CURRENCY = {"EUR": "&euro;", "USD": "$", "GBP": "&pound;"}
TIER_TH_CLASS = ["t-s", "t-m", "t-l"]


class SpecError(Exception):
    """A required value is missing or unusable -- send the user back to /oracle-packs:spec."""


# ---------------------------------------------------------------------------
# Template renderer: {{ x }} escaped, {{& x }} raw, {{# x }}..{{/ x }} section,
# {{^ x }}..{{/ x }} inverted section, {{ . }} the current scalar item.
# ---------------------------------------------------------------------------
TOKEN = re.compile(r"\{\{\s*([#^/&]?)\s*([\w.]+|\.)\s*\}\}")


def _truthy(value):
    if value is None or value is False:
        return False
    if isinstance(value, (list, tuple, dict, str)):
        return len(value) > 0
    return True


def _lookup(stack, path):
    if path == ".":
        return stack[-1].get(".") if isinstance(stack[-1], dict) else stack[-1]
    head, _, rest = path.partition(".")
    for frame in reversed(stack):
        if isinstance(frame, dict) and head in frame:
            value = frame[head]
            for part in (rest.split(".") if rest else []):
                if not isinstance(value, dict) or part not in value:
                    return None
                value = value[part]
            return value
    return None


def _section_body(template, start, path):
    """Return (body, index after the matching {{/path}}), honouring nested sections."""
    depth, pos = 1, start
    while True:
        match = TOKEN.search(template, pos)
        if match is None:
            raise SpecError(f"template: unclosed section {{{{#{path}}}}}")
        kind = match.group(1)
        if kind in ("#", "^"):
            depth += 1
        elif kind == "/":
            depth -= 1
            if depth == 0:
                if match.group(2) != path:
                    raise SpecError(f"template: {{{{/{match.group(2)}}}}} closes {{{{#{path}}}}}")
                return template[start:match.start()], match.end()
        pos = match.end()


def render(template: str, context: dict) -> str:
    """Mustache-lite: {{ x }} escaped, {{& x }} raw, {{# x }}..{{/ x }}, {{^ x }}..{{/ x }}, {{ . }}."""
    return _render(template, [context])


def _render(template, stack):
    out, pos = [], 0
    while True:
        match = TOKEN.search(template, pos)
        if match is None:
            out.append(template[pos:])
            return "".join(out)
        out.append(template[pos:match.start()])
        kind, path = match.group(1), match.group(2)
        if kind in ("#", "^"):
            body, pos = _section_body(template, match.end(), path)
            value = _lookup(stack, path)
            if kind == "^":
                if not _truthy(value):
                    out.append(_render(body, stack))
            elif _truthy(value):
                for item in (value if isinstance(value, list) else [value]):
                    stack.append(item if isinstance(item, dict) else {".": item})
                    out.append(_render(body, stack))
                    stack.pop()
            continue
        if kind == "/":
            raise SpecError(f"template: stray {{{{/{path}}}}}")
        value = _lookup(stack, path)
        if value not in (None, False):
            text = str(value)
            out.append(text if kind == "&" else html.escape(text, quote=True))
        pos = match.end()


# ---------------------------------------------------------------------------
# Spec helpers
# ---------------------------------------------------------------------------
def dig(spec, path, default=None):
    node = spec
    for part in path.split("."):
        if not isinstance(node, dict) or part not in node:
            return default
        node = node[part]
    return node if node is not None else default


def need(spec, path):
    value = dig(spec, path)
    if value in (None, "", [], {}):
        raise SpecError(f"pack spec is missing `{path}` -- confirm it in /oracle-packs:spec before building")
    return value


def as_points(raw):
    """Accept a list of strings ('Label: text') or of {label, text} mappings."""
    points = []
    for item in raw or []:
        if isinstance(item, dict):
            points.append({"label": item.get("label"), "text": item.get("text") or item.get("body") or ""})
        else:
            label, sep, text = str(item).partition(":")
            points.append({"label": label.strip(), "text": text.strip()} if sep else {"label": None, "text": str(item)})
    return points


def money(block, footnote_mark="*"):
    """{value|range, currency, status, footnote} -> '~&euro;2K*' / '&euro;300&ndash;500K' / 'to be defined'."""
    if not isinstance(block, dict):
        return html.escape(str(block)) if block else ""
    status = (block.get("status") or "").lower()
    if status == "tbd" or ("value" not in block and "range" not in block):
        return "to be defined"
    sym = CURRENCY.get((block.get("currency") or "EUR").upper(), (block.get("currency") or "") + "&nbsp;")
    approx = "~" if status in ("indicative", "estimate") else ""
    mark = f'<sup class="fnmark">{footnote_mark}</sup>' if block.get("footnote") or status in ("indicative", "estimate") else ""
    if "range" in block:
        low, high = block["range"]
        lo_n, lo_u = _short(low)
        hi_n, hi_u = _short(high)
        body = f"{sym}{lo_n}&ndash;{hi_n}{hi_u}" if lo_u == hi_u else f"{sym}{lo_n}{lo_u}&ndash;{sym}{hi_n}{hi_u}"
    else:
        num, unit = _short(block["value"])
        body = f"{sym}{num}{unit}"
    return f"{approx}{body}{mark}"


def _short(value):
    value = float(value)
    for div, unit in ((1_000_000, "M"), (1_000, "K")):
        if value >= div:
            scaled = value / div
            return (f"{scaled:.0f}" if abs(scaled - round(scaled)) < 1e-9 else f"{scaled:g}"), unit
    return f"{value:.0f}", ""


def duration(tier):
    if tier.get("duration_label"):
        return html.escape(str(tier["duration_label"]))
    weeks = tier.get("duration_weeks") or {}
    if not isinstance(weeks, dict):
        return f"{weeks} weeks"
    low, high, target = weeks.get("min"), weeks.get("max"), weeks.get("target")
    if low and high and low != high:
        return f"{low}&ndash;{high} weeks"
    single = target or low or high
    return f"{single} weeks" if single else "to be defined"


def level_for(entry, tier_id, label):
    """Resolve the ◐ ● ●● cell for one capability area x tier."""
    levels = entry.get("levels") or {}
    if tier_id in levels:
        return _normalise_level(levels[tier_id], label, tier_id)
    value = entry.get(tier_id)
    if isinstance(value, dict) and "level" in value:
        return _normalise_level(value["level"], label, tier_id)
    if isinstance(value, str):
        stripped = value.strip()
        for chars in ("●●", "◐", "●", "○", "—", "–"):
            if stripped.startswith(chars):
                return GLYPH_BY_CHAR[chars]
        first = stripped.split()[0].lower().strip(".,:;") if stripped else ""
        if first in GLYPH:
            return first
    if value in (None, "", False):
        return "none"
    raise SpecError(
        f"packages.capability_handling[{label!r}].{tier_id} does not say which cell to draw. "
        f"Give it a glyph prefix (◐ / ● / ●●), or add `levels: {{{tier_id}: partial|included|advanced|none}}`."
    )


def _normalise_level(value, label, tier_id):
    key = str(value).strip().lower()
    key = {"full": "included", "yes": "included", "no": "none", "multi-region": "advanced"}.get(key, key)
    if key not in GLYPH:
        raise SpecError(f"packages.capability_handling[{label!r}].{tier_id}: unknown level {value!r} "
                        f"(use none | partial | included | advanced)")
    return key


def data_uri(path: Path) -> str:
    kind = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{kind};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


# ---------------------------------------------------------------------------
# Spec -> template context
# ---------------------------------------------------------------------------
def build_context(spec: dict, channel: str, hero: Path | None) -> tuple[dict, list[str]]:
    """Return (context, forbidden_strings) for this channel."""
    name_allowed = bool(dig(spec, f"clearance.customer_name_allowed.{channel}", False))
    customer = dig(spec, "meta.source_engagement.customer")
    descriptor = dig(spec, "clearance.anonymized_descriptor", "the delivery customer")

    variants = dig(spec, "meta.name_variants", {}) or {}
    if channel == "internal":
        name = variants.get("internal_slide") or need(spec, "meta.name")
        subheading = None
    else:
        name = variants.get("external") or need(spec, "meta.name")
        subheading = variants.get("external_subheading")

    op = dig(spec, "one_pager", {}) or {}          # optional per-artifact overrides
    ps = need(spec, "problem_solution")
    reframe = ps.get("reframe")

    # --- solution chips: explicit, else the KPI names with a direction arrow
    chips = []
    for chip in op.get("kpi_chips") or dig(spec, "one_liner.kpi_chips") or []:
        if isinstance(chip, dict):
            chips.append({"label": chip.get("label", ""), "arrow": _arrow(chip.get("direction", "up"))})
        else:
            text = str(chip)
            arrow = _arrow("down" if text.rstrip().endswith(("down", "↓")) else "up")
            chips.append({"label": re.sub(r"\s*(up|down|↑|↓)\s*$", "", text), "arrow": arrow})
    if not chips:
        for kpi in (dig(spec, "kpis") or [])[:3]:
            chips.append({"label": kpi.get("chip_label") or kpi.get("name", ""), "arrow": _arrow(kpi.get("direction", "up"))})

    # --- data-flow line: explicit block, else derived from architecture
    flow = op.get("data_flow") or _flow_from_architecture(spec)
    if flow:
        for index, box in enumerate(flow.get("platform", {}).get("boxes", [])):
            box["sep"] = index > 0

    # --- proof strip: one metric set, attribution by channel
    kpis = dig(spec, "kpis") or []
    stats, caveats = [], []
    for kpi in kpis:
        if not has_figure(kpi):
            continue
        stats.append({
            "figure": str(kpi["figure"]),
            "prefix": kpi.get("figure_prefix"),
            "suffix": kpi.get("figure_suffix"),
            "label": kpi.get("one_pager_label") or kpi.get("label") or kpi.get("name", ""),
        })
        if kpi.get("caveat"):
            caveats.append(kpi["caveat"])
    attribution = ""
    for kpi in kpis:
        attr = kpi.get("attribution") or {}
        attribution = (attr.get("named_when_allowed") if name_allowed else attr.get("otherwise")) or attribution
        if attribution:
            break
    story = op.get("proof_story") if name_allowed else (op.get("proof_story_anonymized") or op.get("proof_story"))
    if not story:
        delivered = dig(spec, "meta.source_engagement.delivered", "")
        who = customer if name_allowed and customer else descriptor
        story = f"Delivered with {who}: {delivered}" if delivered else ""
    logo = op.get("proof_logo") if name_allowed else None

    # --- packages table
    tiers_raw = need(spec, "packages.tiers")
    tiers, tier_ids = [], []
    for index, tier in enumerate(tiers_raw):
        tier_ids.append(tier.get("id") or f"tier{index}")
        tiers.append({
            "name": tier.get("name") or tier.get("id", ""),
            "size_tag": tier.get("size_tag") if channel == "internal" or tier.get("show_size_tag", True) else None,
            "scope_line": tier.get("scope_line") or (tier.get("what_you_get") or [None])[0],
            "th_class": TIER_TH_CLASS[index] if index < len(TIER_TH_CLASS) else TIER_TH_CLASS[-1],
        })

    rows, footnote = [], None
    if any(t.get("infra_price_monthly") for t in tiers_raw):
        rows.append({"label": op.get("infra_row_label", "Infrastructure price (monthly, consumption&#8209;based)"),
                     "blk_top": False,
                     "cells": [{"css": "val price", "text": money(t.get("infra_price_monthly"))} for t in tiers_raw]})
    if any(t.get("services_price") for t in tiers_raw):
        rows.append({"label": op.get("services_row_label", "Services price (one-time)"),
                     "blk_top": bool(rows),
                     "cells": [{"css": "val price", "text": money(t.get("services_price"))} for t in tiers_raw]})
    rows.append({"label": "Timeline", "blk_top": not rows,
                 "cells": [{"css": "val", "text": duration(t)} for t in tiers_raw]})
    for tier in tiers_raw:
        for block in (tier.get("infra_price_monthly"), tier.get("services_price")):
            if isinstance(block, dict) and block.get("footnote"):
                footnote = "* " + str(block["footnote"]).lstrip("* ")
    if footnote is None and any(
        isinstance(t.get(k), dict) and (t[k].get("status") or "").lower() in ("indicative", "estimate")
        for t in tiers_raw for k in ("infra_price_monthly", "services_price")
    ):
        footnote = "* Indicative; depends on usage and configuration complexity"

    handling = dig(spec, "packages.capability_handling") or []
    for index, entry in enumerate(handling):
        label = entry.get("label") or entry.get("area") or f"capability {index + 1}"
        cells = []
        for tier_id in tier_ids:
            glyph, css = GLYPH[level_for(entry, tier_id, label)]
            cells.append({"css": css, "text": glyph})
        rows.append({"label": html.escape(label), "blk_top": index == 0, "cells": cells})

    contact = dig(spec, f"contacts.{channel}", {}) or {}
    if not contact:
        raise SpecError(f"pack spec is missing `contacts.{channel}` -- the CTA needs a named owner for this channel")
    cta = op.get("cta") or {}

    verticals = []
    for vertical in dig(spec, "verticals") or []:
        verticals.append({"name": vertical.get("name", ""), "line": vertical.get("one_pager_line")})

    context = {
        "doc_title": f"{name} - Sales one-pager - Oracle",
        "hero_image": data_uri(hero) if hero else None,
        "hero": {"eyebrow": op.get("eyebrow", dig(spec, "meta.eyebrow", "OCI AI Accelerators")),
                 "name": name, "subheading": subheading,
                 "one_liner": need(spec, "one_liner.full")},
        "problem": {"heading": op.get("problem_heading", "The problem"),
                    "text": ps.get("problem", ""),
                    "points": as_points(ps.get("problem_points")),
                    "has_points": bool(ps.get("problem_points"))},
        "solution": {"heading": f"The solution: {reframe}" if reframe else "The solution",
                     "text": ps.get("solution", ""),
                     "chips": chips, "has_chips": bool(chips)},
        "data_flow": flow,
        "sell": {"heading": op.get("sell_heading", "Why it sells: for Oracle account teams"),
                 "points": as_points(dig(spec, "packages.why_it_sells_for_the_partner")),
                 "has_points": bool(dig(spec, "packages.why_it_sells_for_the_partner"))},
        "verticals": {"label": op.get("verticals_label", "Where it applies"),
                      "items": verticals, "show": bool(verticals),
                      "as_chips": not any(v["line"] for v in verticals)},
        # the attribution is printed as a run-in prefix only when neither the logo nor the story
        # already carries it -- printing it twice costs words the page does not have
        "proof": {"show": bool(stats), "story": story, "logo": data_uri(Path(logo)) if logo else None,
                  "attribution": attribution,
                  "attribution_inline": bool(attribution) and not logo
                  and str(customer if name_allowed and customer else descriptor).lower() not in (story or "").lower(),
                  "stats": stats, "stat_columns": max(1, len(stats)),
                  "caveat": op.get("proof_caveat") or (caveats[0] if caveats else None)},
        "packages": {"heading": op.get("packages_heading", "Service packages"),
                     "tiers": tiers, "rows": rows, "legend": LEGEND, "footnote": footnote},
        "disclaimer": op.get("disclaimer") or dig(spec, "clearance.disclaimer"),
        "cta": {"question": cta.get("question", "See the fit in one of your accounts?"),
                "answer": cta.get("answer", ""),
                "contact": {"name": contact.get("name", ""),
                            "org": ", ".join(x for x in (contact.get("title"), contact.get("org", "SoftServe")) if x),
                            "email": contact.get("email") or contact.get("mailbox", "")}},
    }

    forbidden = [] if name_allowed else [s for s in ([customer] + (dig(spec, "clearance.forbidden_strings") or [])) if s]
    return context, forbidden


def _arrow(direction):
    return "&#8595;" if str(direction).lower() in ("down", "lower", "reduce", "↓") else "&#8593;"



# The spec writes `-` for "defined and measured per engagement, no cleared number"
# (shared/schema/pack-spec.md). A `-` stat tile is an empty container reading as
# content, so such a metric is simply not printed.
EMPTY_FIGURES = {"-", "--", "\u2014", "\u2013", "n/a"}


def has_figure(kpi) -> bool:
    fig = str((kpi or {}).get("figure") or "").strip()
    return bool(fig) and fig.lower() not in EMPTY_FIGURES

def _flow_from_architecture(spec):
    """inputs -> [source] --data--> [platform boxes] --result--> per architecture.stack."""
    arch = dig(spec, "architecture") or {}
    inputs, outputs, stack = arch.get("inputs") or [], arch.get("outputs") or [], arch.get("stack") or []
    if not inputs or not stack:
        return None
    first = inputs[0] if isinstance(inputs[0], dict) else {"system": str(inputs[0])}
    source = {"name": first.get("system", ""), "note": first.get("note")}
    boxes, platform_label = [], None
    for layer in stack:
        role = (layer.get("layer") or "").lower()
        if "infrastructure" in role:
            parts = [layer.get("vendor"), ", ".join(layer.get("items") or [])]
            platform_label = layer.get("label") or "<br>".join(html.escape(p) for p in parts if p)
        elif any(word in role for word in ("app", "engine")):
            boxes.append({"name": layer.get("name") or (layer.get("items") or [layer.get("layer", "")])[0],
                          "note": layer.get("note") or layer.get("summary")})
    if not boxes:
        return None
    out_first = outputs[0] if outputs and isinstance(outputs[0], dict) else {}
    return {
        "source": source,
        "to_platform_label": first.get("data") or "source data",
        "from_platform_label": out_first.get("data") or "results",
        "platform": {"label": platform_label, "boxes": boxes[:2]},
    }


# ---------------------------------------------------------------------------
# Render QA: word budgets, PDF, page count
# ---------------------------------------------------------------------------
# Measurement is region-scoped: first cut the page into its five regions, then match blocks
# inside one region only. A page-wide regex leaks across regions (the pitch column's bullet
# pattern also matches the sell card's) and reports counts nobody can act on.
REGIONS = {
    "pitch-left": r'<div class="pitch-left">(.*?)</div>\s*</section>|<div class="pitch-left">(.*?)<aside',
    "sell": r'<aside class="sell-card">(.*?)</aside>',
    "hero": r'<header class="hero">(.*?)</header>',
    "proof": r'<section class="proof">(.*?)</section>',
    "packages": r'<section class="packages">(.*?)</section>',
    "cta": r'<footer class="cta">(.*?)</footer>',
}

BLOCK_PATTERNS = [
    ("hero.h1", "hero", r"<h1>(.*?)</h1>"),
    ("hero.h1-sub", "hero", r'<div class="h1-sub">(.*?)</div>'),
    ("hero.sub", "hero", r'<p class="sub">(.*?)</p>'),
    ("problem.para", "pitch-left", r'<h2 class="sec">[^<]*</h2>\s*<p>(.*?)</p>'),
    ("problem.bullets", "pitch-left", r'<ul class="dash">(.*?)</ul>'),
    ("solution.heading", "pitch-left", r'<h2 class="sec">(The solution.*?)</h2>'),
    ("solution.chips", "pitch-left", r'<div class="kpis">(.*?)</div>\s*<p>'),
    ("solution.para", "pitch-left", r'<div class="kpis">.*?</div>\s*<p>(.*?)</p>'),
    ("data-flow", "pitch-left", r'<div class="arch">(.*)'),
    ("sell.bullets", "sell", r'<ul class="dash">(.*?)</ul>'),
    ("sell.chips", "sell", r'<div class="(?:chips|vert-lines)">(.*)'),
    ("proof.story", "proof", r'<div class="proof-head">.*?<p>(.*?)</p>'),
    ("proof.stats", "proof", r'<div class="stats">(.*?)<p class="caveat">|<div class="stats">(.*)'),
    ("proof.caveat", "proof", r'<p class="caveat">(.*?)</p>'),
    ("packages.table", "packages", r'(<table class="pk">.*?</table>)'),
    ("packages.notes", "packages", r'<div class="pk-notes">(.*?)</div>'),
    ("disclaimer", "disclaimer", r'<p class="disclaimer">(.*?)</p>'),
    ("cta.q", "cta", r'<div class="q">(.*?)</div>'),
    ("cta.a", "cta", r'<div class="a">(.*?)</div>'),
]


def _words(fragment: str) -> int:
    text = html.unescape(re.sub(r"<[^>]+>", " ", fragment or ""))
    return len([w for w in text.split() if re.search(r"[\w€$£%+~]", w)])


def _first(pattern: str, text: str) -> str:
    match = re.search(pattern, text, re.S)
    return next((g for g in match.groups() if g), "") if match else ""


def measure(rendered: str) -> list[tuple[str, int, int]]:
    body = re.sub(r"<svg.*?</svg>", "", rendered.split("<body>", 1)[-1], flags=re.S)
    regions = {name: _first(pattern, body) for name, pattern in REGIONS.items()}
    # the pitch column ends where the sell card starts
    regions["pitch-left"] = regions["pitch-left"].split("<aside")[0]
    # the disclaimer sits inside .pk-notes; measure it once, as itself, not again as part of the row
    regions["disclaimer"] = regions["packages"]
    regions["packages"] = re.sub(r'<p class="disclaimer">.*?</p>', "", regions["packages"], flags=re.S)
    measured, total = [], 0
    for name, region, pattern in BLOCK_PATTERNS:
        count = sum(_words(m if isinstance(m, str) else next((g for g in m if g), ""))
                    for m in re.findall(pattern, regions.get(region, ""), re.S))
        total += count
        measured.append((name, count, BUDGETS.get(name, 0)))
    measured.append(("PAGE TOTAL", total, BUDGETS["PAGE TOTAL"]))
    return measured


def find_chrome() -> str | None:
    """CHROME_BIN, then the macOS default path, then PATH. A CHROME_BIN that is not runnable
    falls through with a warning rather than failing the build with a FileNotFoundError."""
    override = os.environ.get("CHROME_BIN")
    if override:
        if os.access(override, os.X_OK):
            return override
        print(f"build_one_pager: CHROME_BIN={override} is not executable; looking elsewhere", file=sys.stderr)
    mac_default = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if Path(mac_default).exists():
        return mac_default
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        found = shutil.which(name)
        if found:
            return found
    for extra in ("/Applications/Chromium.app/Contents/MacOS/Chromium",
                  "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"):
        if Path(extra).exists():
            return extra
    return None


def print_pdf(chrome: str, html_path: Path, pdf_path: Path, timeout: int = 90) -> None:
    """Print the page with headless Chrome.

    Chrome writes the PDF and then, on macOS, often lingers instead of exiting. So poll for the
    file to appear and stop growing, then stop the process -- waiting on exit can hang for minutes.
    """
    if pdf_path.exists():
        pdf_path.unlink()
    with tempfile.TemporaryDirectory(prefix="one-pager-chrome-") as profile:
        cmd = [chrome, "--headless", f"--print-to-pdf={pdf_path}", "--no-pdf-header-footer",
               "--disable-gpu", "--no-sandbox", "--no-first-run", "--no-default-browser-check",
               "--disable-extensions", "--disable-sync", f"--user-data-dir={profile}",
               "--run-all-compositor-stages-before-draw", "--virtual-time-budget=6000",
               html_path.as_uri()]
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except OSError as err:
            raise SpecError(f"could not run {chrome}: {err}") from err
        deadline, last_size = time.monotonic() + timeout, -1
        try:
            while time.monotonic() < deadline:
                if proc.poll() is not None:
                    break
                size = pdf_path.stat().st_size if pdf_path.exists() else -1
                if size > 0 and size == last_size:
                    break                       # written and stable -> done
                last_size = size
                time.sleep(0.4)
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    proc.kill()
            stderr = (proc.stderr.read() if proc.stderr else "") or ""
    if not pdf_path.exists() or pdf_path.stat().st_size == 0:
        raise SpecError("headless Chrome produced no PDF:\n" + (stderr.strip()[-1200:] or "no output"))


def page_report(pdf_path: Path):
    try:
        from pypdf import PdfReader
    except ImportError:
        return None, None
    reader = PdfReader(str(pdf_path))
    box = reader.pages[0].mediabox
    return len(reader.pages), (round(float(box.width), 2), round(float(box.height), 2))


# ---------------------------------------------------------------------------
def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="build_one_pager.py",
        description="Build the sales one-pager (HTML -> one A4 PDF) from a pack spec.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Exit codes: 0 ok | 1 spec error | 2 clearance violation | 3 more than one page | 4 no Chrome.",
    )
    parser.add_argument("spec", type=Path, help="path to packs/<slug>/pack-spec.yaml")
    parser.add_argument("--out", type=Path, required=True, help="output directory (created if missing)")
    parser.add_argument("--channel", choices=CHANNELS, default="partner_print",
                        help="naming, attribution and contact rules to apply (default: partner_print)")
    parser.add_argument("--hero", type=Path, default=None,
                        help="hero image; embedded as a data: URI. Omitted -> the hero renders without a photo.")
    parser.add_argument("--template", type=Path, default=TEMPLATE, help="override the HTML template")
    parser.add_argument("--no-pdf", action="store_true", help="write the HTML only; skip Chrome and the page check")
    args = parser.parse_args(argv)

    if not args.spec.exists():
        print(f"build_one_pager: no such spec: {args.spec}", file=sys.stderr)
        return 1
    if args.hero and not args.hero.exists():
        print(f"build_one_pager: no such hero image: {args.hero}", file=sys.stderr)
        return 1

    spec = yaml.safe_load(args.spec.read_text(encoding="utf-8")) or {}
    try:
        context, forbidden = build_context(spec, args.channel, args.hero)
        rendered = render(args.template.read_text(encoding="utf-8"), context)
    except SpecError as err:
        print(f"build_one_pager: {err}", file=sys.stderr)
        return 1

    args.out.mkdir(parents=True, exist_ok=True)
    slug = dig(spec, "meta.slug", "pack")
    stem = f"{slug}-one-pager-{args.channel}"
    html_path = args.out / f"{stem}.html"
    html_path.write_text(rendered, encoding="utf-8")
    print(f"HTML  {html_path}  ({len(rendered) // 1024} KB)")

    # clearance guard: a name this channel may not carry must not reach the page
    visible = html.unescape(re.sub(r"<[^>]+>", " ", rendered))
    leaked = [s for s in forbidden if re.search(rf"\b{re.escape(str(s))}\b", visible, re.I)]
    if leaked:
        print(f"build_one_pager: CLEARANCE -- {', '.join(leaked)} appears on the page, but "
              f"clearance.customer_name_allowed.{args.channel} is false. Use the anonymized descriptor "
              f"({dig(spec, 'clearance.anonymized_descriptor', '-')}) in one_pager.proof_story_anonymized "
              f"and in kpis[].attribution.otherwise.", file=sys.stderr)
        return 2

    measured = measure(rendered)
    over = [(n, c, b) for n, c, b in measured if b and c > b and n != "PAGE TOTAL"]

    if args.no_pdf:
        _print_budget(measured)
        return 0

    chrome = find_chrome()
    if not chrome:
        print("build_one_pager: no Chrome/Chromium found -- set CHROME_BIN, or install Google Chrome. "
              "The HTML is written but the one-page rule was NOT verified.", file=sys.stderr)
        return 4

    pdf_path = args.out / f"{stem}.pdf"
    try:
        print_pdf(chrome, html_path, pdf_path)
    except SpecError as err:
        print(f"build_one_pager: {err}", file=sys.stderr)
        return 1

    pages, size = page_report(pdf_path)
    if pages is None:
        print(f"PDF   {pdf_path}  (pypdf not installed -- page count NOT verified)", file=sys.stderr)
        return 4
    print(f"PDF   {pdf_path}  ({pages} page{'s' if pages != 1 else ''}, {size[0]} x {size[1]} pt)")

    if pages > 1:
        print(f"\nbuild_one_pager: the one-pager must be ONE A4 page; this render is {pages}. "
              f"Cut content and rebuild -- longest blocks first:", file=sys.stderr)
        # blocks over their budget first, then simply the biggest blocks -- when nothing is over
        # budget the page is over for layout reasons, and the cut has to come from the long blocks
        ranked = sorted([m for m in measured if m[0] != "PAGE TOTAL"],
                        key=lambda m: (max(0, m[1] - m[2]), m[1]), reverse=True)
        for name, count, budget in ranked[:8]:
            flag = "OVER" if budget and count > budget else "    "
            print(f"  {flag}  {name:<18} {count:>4} words   budget {budget}", file=sys.stderr)
        total = next(m for m in measured if m[0] == "PAGE TOTAL")
        print(f"        {'PAGE TOTAL':<18} {total[1]:>4} words   budget {total[2]} "
              f"(reference one-pager: 450)", file=sys.stderr)
        print("  Propose the cuts to the owner rather than shrinking type: the type scale is the brand.",
              file=sys.stderr)
        return 3

    if over:
        print("\nOne page, but these blocks are over their reference budget -- tighten on the next pass:")
        for name, count, budget in over:
            print(f"  {name:<18} {count:>4} words   budget {budget}")
    _print_budget(measured, only_total=True)
    return 0


def _print_budget(measured, only_total=False):
    rows = [m for m in measured if m[0] == "PAGE TOTAL"] if only_total else measured
    for name, count, budget in rows:
        mark = "OVER" if budget and count > budget else "ok"
        print(f"  {name:<18} {count:>4} words   budget {budget:>4}   {mark}")


if __name__ == "__main__":
    sys.exit(main())
