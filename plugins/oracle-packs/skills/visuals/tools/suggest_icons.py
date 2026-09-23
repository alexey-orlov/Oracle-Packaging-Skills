#!/usr/bin/env python3
"""Turn an industry name into candidate icon names worth proposing.

    suggest_icons.py "<vertical name>" [--context "<what matters here>"] [--n 3]
                     [--describe] [--json] [--set tabler]

Matches the name (and any `--context` line) against `references/icon-keywords.yaml` and prints the
best candidates, best first, with the industry row each came from. `--describe` also fetches each
icon's own tag list from the set, which helps when writing the one plain line the owner reads
("a factory building", "a delivery truck"); it is the picture on the contact sheet, not this list,
that the line should actually describe.

Nothing is downloaded or written without `--describe`; this tool only proposes names. Exit codes:
0 candidates printed · 1 usage error · 3 the set could not be reached while describing.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from visuals_common import (  # noqa: E402
    EXIT_DEFERRED, EXIT_OK, EXIT_USAGE, Deferred, ICON_SETS, eprint, http_get,
)

KEYWORDS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "references", "icon-keywords.yaml")


def load_table(path: str) -> dict:
    import yaml
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def score_row(row: dict, haystack: str) -> tuple[int, str]:
    """Best (score, matched phrase) for one industry row. A multi-word phrase beats a single word;
    a word on its own beats the same letters inside another word."""
    best = (0, "")
    for phrase in row.get("match", []):
        p = phrase.lower().strip()
        if not p or p not in haystack:
            continue
        words = len(p.split())
        whole = re.search(rf"(?<![a-z]){re.escape(p)}(?![a-z])", haystack) is not None
        s = words * 10 + (5 if whole else 0) + min(len(p), 20) // 5
        if s > best[0]:
            best = (s, phrase)
    return best


NAME_WEIGHT = 2      # the industry's own name decides; the context line only breaks ties


def suggest(name: str, context: str, table: dict, n: int) -> tuple[list[dict], list[str]]:
    hay_name, hay_ctx = name.lower(), (context or "").lower()
    hits = []
    for row in table.get("industries", []):
        sn, pn = score_row(row, hay_name)
        sc, pc = score_row(row, hay_ctx)
        s, phrase = max((sn * NAME_WEIGHT, pn), (sc, pc))
        if s:
            hits.append((s, phrase, row))
    hits.sort(key=lambda t: -t[0])

    out, seen, rows = [], set(), []
    for s, phrase, row in hits:
        rows.append(f"{row['id']} (matched “{phrase}”)")
        for icon in row["icons"]:
            if icon in seen:
                continue
            seen.add(icon)
            out.append({"icon": icon, "industry": row["id"], "matched": phrase})
            if len(out) >= n:
                return out, rows
    if not out:
        for icon in table.get("fallback", {}).get("icons", []):
            out.append({"icon": icon, "industry": "fallback", "matched": "-"})
    return out[:n], rows


def describe(icon: str, icon_set: str) -> str:
    """Tabler and Lucide both carry a `tags:` comment at the top of the SVG."""
    svg = http_get(ICON_SETS[icon_set]["svg"].format(name=icon)).decode("utf-8", "replace")
    m = re.search(r"tags:\s*\[([^\]]*)\]", svg)
    cat = re.search(r"category:\s*(.+)", svg)
    bits = []
    if cat:
        bits.append(cat.group(1).strip())
    if m:
        bits.append(", ".join(t.strip() for t in m.group(1).split(",")[:6]))
    return " · ".join(bits) or "-"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("vertical", help="the industry's name, as the pack writes it")
    ap.add_argument("--context", default="", help="the vertical's 'what matters here' line, to sharpen the match")
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--describe", action="store_true", help="also fetch each icon's own tag list")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--set", dest="icon_set", default="tabler", choices=sorted(ICON_SETS))
    ap.add_argument("--keywords", default=KEYWORDS)
    args = ap.parse_args(argv)

    if not os.path.exists(args.keywords):
        eprint(f"no keyword table at {args.keywords}")
        return EXIT_USAGE
    table = load_table(args.keywords)
    picks, rows = suggest(args.vertical, args.context, table, args.n)

    if args.describe:
        for p in picks:
            try:
                p["shows"] = describe(p["icon"], args.icon_set)
            except Deferred as exc:
                eprint(f"deferred — {exc}")
                return EXIT_DEFERRED
            except FileNotFoundError:
                p["shows"] = "MISSING FROM THE SET — fix the keyword table"

    if args.json:
        print(json.dumps({"vertical": args.vertical, "matched_rows": rows, "candidates": picks},
                         indent=2, ensure_ascii=False))
        return EXIT_OK

    print(f"{args.vertical}")
    print("  matched: " + ("; ".join(rows) if rows else "nothing — using the generic fallback"))
    for i, p in enumerate(picks):
        line = f"  {'ABC'[i] if i < 3 else i}  {p['icon']}   ({p['industry']})"
        if p.get("shows"):
            line += f"\n       shows: {p['shows']}"
        print(line)
    print("\n  fetch them:  fetch_icon.py <name> --out <dir> --slot <slot>")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
