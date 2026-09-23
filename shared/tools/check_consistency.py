#!/usr/bin/env python3
"""Check every produced artifact against the pack spec it was built from.

    python3 shared/tools/check_consistency.py packs/<slug>/pack-spec.yaml \
            out/one-pager.html out/deck.pptx out/feature-list.docx

The linters ask whether an artifact is allowed to say what it says; this asks
whether the artifacts say the SAME thing. Artifacts omit components by design —
a one-pager carries no capability matrix — so an absent component is reported for
information, never as a finding. A component that is present and differs from the
spec is a finding: two artifacts of one pack may not carry two one-liners, two
tier vocabularies, two durations, two price sets or two figures.

Findings print as `file:line: CODE message`, then an artifact x component matrix,
then one summary line.

Exit codes
    0   every component that appears is identical to the spec
    1   at least one component appears and differs
    2   usage or dependency error (unreadable spec or artifact, no PyYAML)

Rule codes
    CON001  the one-liner differs from spec one_liner.full / .short
    CON002  a tier is named something other than PoV Jumpstart / Integration / Scaling
    CON003  a duration in weeks matches no tier's duration_weeks in the spec
    CON004  a EUR figure matches no price the spec carries
    CON005  a KPI figure differs from the spec's figure for that KPI
    CON900  a file was skipped (unsupported format, or pdftotext missing) — warning

Matrix legend
    ✓   present and identical to the spec
    ✗   present and differs (a finding)
    –   absent (by design; nothing to check)

Rule text: shared/references/naming-and-clearance.md §3 (one metric set, one
tier vocabulary, prices with their disclaimers) and shared/schema/pack-spec.md.
"""

from __future__ import annotations

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import packlint as PL  # noqa: E402

PROG = "check_consistency"

COMPONENTS = [("one_liner", "one-liner"), ("tiers", "tier names"),
              ("duration", "PoV duration"), ("prices", "prices"), ("kpis", "KPI figures")]

LEGACY_TIER = re.compile(r"(?<!PoV )\bJumpstart\b|\bQuick ?Start\b|\bPoC package\b"
                         r"|\b(?:Integration)\s*(?:and|&|/)\s*Scale\b"
                         r"|\bScale\b(?=[^.\n]{0,40}\b(?:tier|package|phase)\b)")

WEEKS = re.compile(r"\b(\d{1,2})\s*(?:[-–—]|to)\s*(\d{1,2})\s*weeks?\b"
                   r"|\b(\d{1,2})\s*weeks?\b", re.IGNORECASE)

FIGURE = re.compile(r"[~≈<>]?\s?\d+(?:[.,]\d+)?\s*(?:%|×|x\b|pp\b|bps\b|h\b|hrs?\b|hours?\b"
                    r"|min(?:utes)?\b|days?\b|weeks?\b|months?\b|FTE\b)", re.IGNORECASE)

PRESENT, DIFFERS, ABSENT = "✓", "✗", "–"


class Consistency:
    def __init__(self, spec, spec_path, rep):
        self.spec = spec
        self.spec_path = spec_path
        self.rep = rep
        self.matrix = []                     # (artifact, {component: state})
        self.one_liners = [str(v) for v in
                           (PL.dig(spec, "one_liner", "full"), PL.dig(spec, "one_liner", "short"))
                           if PL.is_filled(v)]
        self.tiers = self._tiers()
        self.prices = self._prices()
        self.kpis = self._kpis()
        # A KPI figure can be money ("€190K / month"). It is a figure, not a price:
        # CON005 owns it, and CON004 must not read it as a tier price the spec lost.
        self.figure_values = set()
        for kpi in self.kpis:
            value = PL.money_value(kpi["figure"]) if "€" in kpi["figure"] or "EUR" in kpi["figure"] else None
            if value is not None:
                self.figure_values.add(value)

    def _tiers(self):
        out = []
        tiers = PL.dig(self.spec, "packages", "tiers", default=[])
        if isinstance(tiers, list):
            for tier in tiers:
                if not isinstance(tier, dict):
                    continue
                weeks = tier.get("duration_weeks") if isinstance(tier.get("duration_weeks"), dict) else {}
                span = []
                for key in ("min", "target", "max"):
                    try:
                        span.append(float(weeks.get(key)))
                    except (TypeError, ValueError):
                        pass
                out.append({
                    "id": str(tier.get("id") or "").strip(),
                    "name": str(tier.get("name") or "").strip(),
                    "lo": min(span) if span else None,
                    "hi": max(span) if span else None,
                })
        return out

    def _prices(self):
        values = set()
        tiers = PL.dig(self.spec, "packages", "tiers", default=[])
        if isinstance(tiers, list):
            for tier in tiers:
                if not isinstance(tier, dict):
                    continue
                for key in ("services_price", "infra_price_monthly"):
                    price = tier.get(key)
                    if not isinstance(price, dict):
                        continue
                    if price.get("value") is not None:
                        try:
                            values.add(float(price["value"]))
                        except (TypeError, ValueError):
                            pass
                    for end in (price.get("range") or []):
                        try:
                            values.add(float(end))
                        except (TypeError, ValueError):
                            pass
        return values

    def _kpis(self):
        out = []
        kpis = self.spec.get("kpis")
        if isinstance(kpis, list):
            for kpi in kpis:
                if isinstance(kpi, dict) and PL.is_filled(kpi.get("name")):
                    out.append({"name": str(kpi["name"]).strip(),
                                "figure": PL.norm_ws(str(kpi.get("figure") or "")),
                                "baseline": PL.norm_ws(str(kpi.get("baseline") or ""))})
        return out

    # -- per-artifact -------------------------------------------------------
    def run(self, doc):
        states = {
            "one_liner": self.check_one_liner(doc),
            "tiers": self.check_tiers(doc),
            "duration": self.check_duration(doc),
            "prices": self.check_prices(doc),
            "kpis": self.check_kpis(doc),
        }
        self.matrix.append((doc.path, states))

    def check_one_liner(self, doc):
        """The full or the short variant, verbatim, is the spec's one-liner.

        Every place the one-liner opens is checked against BOTH variants before
        anything is reported: a cover that prints the short line is right, and
        the window is cut for the longest variant so the full line fits it too.
        """
        variants = [v for v in self.one_liners if len(PL.norm_loose(v).split()) >= 4]
        if not variants:
            return ABSENT
        span = int(max(len(v) for v in variants) * 1.6) + 40
        seen, differs, present = set(), [], False
        for text in variants:
            words = PL.norm_loose(text).split()
            anchor = re.compile(r"\s+".join(re.escape(w) for w in words[:4]), re.IGNORECASE)
            for m in anchor.finditer(doc.text):
                if m.start() in seen:
                    continue
                seen.add(m.start())
                window = doc.text[m.start():m.start() + span]
                if any(PL.norm_loose(window).startswith(PL.norm_loose(v)) for v in variants):
                    present = True
                else:
                    differs.append((m.start(), window))
        for start, window in differs:
            line, label = doc.where(start)
            got = PL.norm_ws(window)
            if len(got) > 120:
                got = got[:117] + "..."
            self.rep.fail(doc.path, line, "CON001",
                          "the one-liner reads `%s`; the spec says `%s`%s"
                          % (got, " / ".join(PL.norm_ws(v) for v in variants), label))
        return DIFFERS if differs else (PRESENT if present else ABSENT)

    def check_tiers(self, doc):
        state = ABSENT
        for m in LEGACY_TIER.finditer(doc.text):
            line, label = doc.where(m.start())
            self.rep.fail(doc.path, line, "CON002",
                          "`%s` is not a tier name in the spec — the tiers are %s%s"
                          % (PL.norm_ws(m.group(0)),
                             " / ".join(t["name"] or t["id"] for t in self.tiers) or
                             "PoV Jumpstart / Integration / Scaling", label))
            state = DIFFERS
        for tier in self.tiers:
            if tier["name"] and re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(tier["name"]),
                                          doc.text):
                if state != DIFFERS:
                    state = PRESENT
        return state

    def check_duration(self, doc):
        if not any(t["lo"] is not None for t in self.tiers):
            return ABSENT
        state = ABSENT
        for m in WEEKS.finditer(doc.text):
            lo = m.group(1) or m.group(3)
            hi = m.group(2) or m.group(3)
            try:
                lo, hi = float(lo), float(hi)
            except (TypeError, ValueError):
                continue
            ctx = PL.context(doc.text, m.start(), m.end(), 120).lower()
            pov_context = "pov" in ctx or "jumpstart" in ctx or "proof of value" in ctx
            candidates = [t for t in self.tiers if t["lo"] is not None]
            if pov_context:
                candidates = [t for t in candidates if t["id"] == "pov"] or candidates
            ok = any(t["lo"] <= lo and hi <= t["hi"] for t in candidates)
            if ok:
                if state != DIFFERS:
                    state = PRESENT
            else:
                line, label = doc.where(m.start())
                self.rep.fail(doc.path, line, "CON003",
                              "`%s` matches no tier's duration_weeks in the spec (%s)%s"
                              % (PL.norm_ws(m.group(0)),
                                 "; ".join("%s %g-%g weeks" % (t["name"] or t["id"], t["lo"], t["hi"])
                                           for t in candidates), label))
                state = DIFFERS
        return state

    def check_prices(self, doc):
        state = ABSENT
        for m in PL.MONEY_RE.finditer(doc.text):
            token = PL.norm_ws(m.group(0))
            value = PL.money_value(token)
            if value is None:
                continue
            if any(abs(value - f) < 0.5 for f in self.figure_values):
                continue                     # a KPI figure: CON005's business
            if not self.prices:
                state = PRESENT if state != DIFFERS else state
                continue
            # "~€300-500K" is one range; the regex stops at the dash, so the low end
            # arrives as "€300" and carries the second half's K/M multiplier.
            candidates = [value]
            tail = doc.text[m.end():m.end() + 12]
            unit = re.match(r"\s*[-\u2010-\u2015]\s*(?:€|EUR)?\s*\d[\d.,]*\s*([KkMm])", tail)
            if unit and not re.search(r"[KkMm]\s*$", token):
                candidates.append(value * (1000 if unit.group(1).lower() == "k" else 1000000))
            if any(abs(v - p) < 0.5 for v in candidates for p in self.prices):
                if state != DIFFERS:
                    state = PRESENT
            else:
                line, label = doc.where(m.start())
                self.rep.fail(doc.path, line, "CON004",
                              "`%s` matches no price in the spec (%s) — one price set per pack%s"
                              % (token, ", ".join("%g" % p for p in sorted(self.prices)), label))
                state = DIFFERS
        return state

    def check_kpis(self, doc):
        state = ABSENT
        flat = PL.norm_loose(doc.text)
        for kpi in self.kpis:
            name = PL.norm_loose(kpi["name"])
            if not name or name not in flat:
                continue
            pattern = re.compile(r"\s+".join(re.escape(w) for w in kpi["name"].split()),
                                 re.IGNORECASE)
            m = pattern.search(doc.text)
            if not m:
                continue
            ctx = PL.context(doc.text, m.start(), m.end(), 200)
            want = PL.norm_loose(kpi["figure"])
            seen = [PL.norm_ws(f.group(0)) for f in FIGURE.finditer(ctx)]
            if want and want in PL.norm_loose(ctx):
                if state != DIFFERS:
                    state = PRESENT
            elif seen and want:
                line, label = doc.where(m.start())
                self.rep.fail(doc.path, line, "CON005",
                              "`%s` is printed with %s; the spec's figure is `%s` — the numbers "
                              "do not vary by channel, only the attribution does%s"
                              % (kpi["name"], " / ".join("`%s`" % s for s in seen[:3]),
                                 kpi["figure"], label))
                state = DIFFERS
            elif want:
                if state != DIFFERS:
                    state = PRESENT if want in PL.norm_loose(ctx) else state
        return state

    # -- matrix -------------------------------------------------------------
    def render_matrix(self):
        if not self.matrix:
            return ""
        labels = [label for _, label in COMPONENTS]
        width = max([len(os.path.basename(p)) for p, _ in self.matrix] + [8]) + 2
        out = ["", "artifact × component  (✓ identical to the spec · ✗ differs · – absent)"]
        out.append("  %-*s %s" % (width, "artifact", "  ".join("%-*s" % (len(l), l) for l in labels)))
        for path, states in self.matrix:
            cells = []
            for key, label in COMPONENTS:
                cells.append("%-*s" % (len(label), states[key].center(len(label))))
            out.append("  %-*s %s" % (width, os.path.basename(path), "  ".join(cells)))
        out.append("")
        return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(prog=PROG, description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", help="packs/<slug>/pack-spec.yaml")
    ap.add_argument("artifacts", nargs="+", help="the produced artifacts (files or directories)")
    args = ap.parse_args()

    if not os.path.isfile(args.spec):
        PL.die_usage(PROG, "no such spec file: %s" % args.spec)
    spec = PL.load_yaml(args.spec, PROG)
    if not isinstance(spec, dict):
        PL.die_usage(PROG, "%s is not a pack spec" % args.spec)

    rep = PL.Report(PROG)
    checker = Consistency(spec, args.spec, rep)

    files = []
    for target in args.artifacts:
        files.extend(PL.collect_files(target, PROG))

    read = 0
    for path in files:
        doc, reason = PL.extract(path)
        if doc is None:
            rep.warn(path, 1, "CON900", reason)
            rep.cannot_check(reason)
            continue
        read += 1
        checker.run(doc)

    return rep.render("%d artifact(s) against %s" % (read, os.path.basename(args.spec)),
                      tail=checker.render_matrix())


if __name__ == "__main__":
    raise SystemExit(main())
