#!/usr/bin/env python3
"""Check every produced artifact against the pack spec it was built from.

    python3 shared/tools/check_consistency.py packs/<slug>/pack-spec.md \
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
    CON003  a duration in weeks matches no tier's duration_weeks in the spec. Not a
            tier duration, so not checked: a figure inside one of the spec's own
            exec_summary.next_steps, and the source engagement's own length (a
            duration meta.source_engagement states) in a sentence about the
            engagement — unless that sentence names a tier
    CON004  a EUR figure matches no price the spec carries
    CON005  a KPI figure differs from the spec's figure for that KPI
    CON006  the artifact's spec stamp names another version of the spec: built from an
            earlier version — rebuild before sending (warning)
    CON007  a .docx, .pptx, .html or .pdf with no spec stamp: built before 2026-09-24 or
            by hand, so which spec it reflects is unknown (warning). Other formats carry
            no stamp by design and are not reported
    CON900  a file was skipped (unsupported format, or pdftotext missing) — warning

The stamp is the line every builder writes into its file (shared/tools/spec_stamp.py):
`pack-spec sha256:<12 hex> commit:<...>`. Only the sha is compared, against the sha of the
spec given here. Warnings never change the exit code.

Matrix legend
    ✓   present and identical to the spec
    ✗   present and differs (a finding)
    –   absent (by design; nothing to check)
    The last column, "spec", is the stamp: ✓ built from this spec · ✗ from an earlier
    version (CON006) · – no stamp

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
import spec_stamp  # noqa: E402

PROG = "check_consistency"

COMPONENTS = [("one_liner", "one-liner"), ("tiers", "tier names"),
              ("duration", "PoV duration"), ("prices", "prices"), ("kpis", "KPI figures")]

# The matrix's last column: the spec stamp, not a component (CON006 / CON007).
STAMP_COLUMN = ("spec", "spec")

CON006_TEXT = "built from an earlier version of the spec — rebuild before sending"
CON007_TEXT = ("no spec stamp: built before 2026-09-24 or by hand; which spec it reflects "
               "is unknown")

LEGACY_TIER = re.compile(r"(?<!PoV )\bJumpstart\b|\bQuick ?Start\b|\bPoC package\b"
                         r"|\b(?:Integration)\s*(?:and|&|/)\s*Scale\b"
                         r"|\bScale\b(?=[^.\n]{0,40}\b(?:tier|package|phase)\b)")

WEEKS = re.compile(r"\b(\d{1,2})\s*(?:[-–—]|to)\s*(\d{1,2})\s*weeks?\b"
                   r"|\b(\d{1,2})\s*weeks?\b", re.IGNORECASE)

# The spec states the engagement's own length in any form, "a 12-week proof of value"
# included — so the compound adjective counts when reading the spec.
SPEC_WEEKS = re.compile(r"\b(\d{1,2})\s*(?:[-–—]|to)\s*(\d{1,2})[\s-]*weeks?\b"
                        r"|\b(\d{1,2})[\s-]*weeks?\b", re.IGNORECASE)

# What makes a sentence about the source engagement rather than about a tier.
ENGAGEMENT_WORDS = (r"\bengagements?\b", r"\bcontracted\b", r"\bdeliver(?:ed|y)\b",
                    r"\bpilot\b", r"\bproof of concept\b", r"\bPoC\b")

SENTENCE_END = re.compile(r"[.!?](?=\s|$)")

FIGURE = re.compile(r"[~≈<>]?\s?\d+(?:[.,]\d+)?\s*(?:%|×|x\b|pp\b|bps\b|h\b|hrs?\b|hours?\b"
                    r"|min(?:utes)?\b|days?\b|weeks?\b|months?\b|FTE\b)", re.IGNORECASE)

PRESENT, DIFFERS, ABSENT = "✓", "✗", "–"


def statement(doc, start, end):
    """The statement a match belongs to: its paragraph where the extractor gives one per
    line (.pptx, .docx, .pdf), else its sentence, which may wrap across source lines."""
    text = doc.text
    if doc.kind != "text":
        s = text.rfind("\n", 0, start) + 1
        e = text.find("\n", end)
        return text[s:len(text) if e < 0 else e]
    s = text.rfind("\n\n", 0, start)
    s = 0 if s < 0 else s + 2
    e = text.find("\n\n", end)
    e = len(text) if e < 0 else e
    ends = [m.end() for m in SENTENCE_END.finditer(text, s, start)]
    if ends:
        s = ends[-1]
    m = SENTENCE_END.search(text, end, e)
    return text[s:m.end() if m else e]


def _strings(node):
    if isinstance(node, dict):
        for value in node.values():
            yield from _strings(value)
    elif isinstance(node, list):
        for value in node:
            yield from _strings(value)
    elif isinstance(node, str):
        yield node


class Consistency:
    def __init__(self, spec, spec_path, rep):
        self.spec = spec
        self.spec_path = spec_path
        self.rep = rep
        self.matrix = []                     # (artifact, {component: state})
        self.spec_sha = spec_stamp.spec_sha(spec_path)
        self.one_liners = [str(v) for v in
                           (PL.dig(spec, "one_liner", "full"), PL.dig(spec, "one_liner", "short"))
                           if PL.is_filled(v)]
        self.tiers = self._tiers()
        self.prices = self._prices()
        self.kpis = self._kpis()
        # CON003 reads a week figure as a tier duration. Two kinds are not one: the
        # spec's own planned next steps, and the source engagement's own length in a
        # sentence about the engagement. The next step "12 weeks" on a logistics
        # customer's executive summary failed the check although no tier claimed it
        # (2026-09-23).
        self.engagement_weeks = self._engagement_weeks()
        self.next_steps = self._next_steps()
        self.engagement_marker = self._engagement_marker()
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

    def _engagement_weeks(self):
        """Every duration meta.source_engagement states, as (lo, hi) in weeks."""
        out = set()
        for text in _strings(PL.dig(self.spec, "meta", "source_engagement", default={})):
            for m in SPEC_WEEKS.finditer(text):
                lo, hi = m.group(1) or m.group(3), m.group(2) or m.group(3)
                out.add((float(lo), float(hi)))
        return out

    def _next_steps(self):
        """One pattern per planned next step as the spec writes it (title, detail or line)."""
        out = []
        steps = PL.dig(self.spec, "exec_summary", "next_steps", default=[])
        for step in steps if isinstance(steps, list) else []:
            parts = [step.get("title"), step.get("detail")] if isinstance(step, dict) else [step]
            for part in parts:
                words = PL.norm_ws(str(part or "")).split()
                if words:
                    out.append(re.compile(r"\s+".join(re.escape(w) for w in words),
                                          re.IGNORECASE))
        return out

    def _engagement_marker(self):
        names = [PL.dig(self.spec, "meta", "source_engagement", "customer"),
                 PL.dig(self.spec, "clearance", "anonymized_descriptor")]
        alts = list(ENGAGEMENT_WORDS) + [re.escape(PL.norm_ws(str(n)))
                                         for n in names if PL.is_filled(n)]
        return re.compile("|".join(alts), re.IGNORECASE)

    def not_a_tier_duration(self, doc, m, lo, hi, step_spans):
        """A week figure that belongs to a planned next step or to the source engagement.

        Never when its statement names a tier: "PoV Jumpstart runs 12 weeks" is a tier
        claim even where 12 weeks is the engagement's length — the very drift CON003 is
        for. Otherwise: inside one of the spec's own next steps, or the engagement's own
        length in a statement that speaks of the engagement.
        """
        unit = statement(doc, m.start(), m.end())
        if any(re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(t["name"]), unit)
               for t in self.tiers if t["name"]):
            return False
        if any(s <= m.start() and m.end() <= e for s, e in step_spans):
            return True
        return (lo, hi) in self.engagement_weeks and bool(self.engagement_marker.search(unit))

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
    def run(self, doc, stamp_state=ABSENT):
        states = {
            "one_liner": self.check_one_liner(doc),
            "tiers": self.check_tiers(doc),
            "duration": self.check_duration(doc),
            "prices": self.check_prices(doc),
            "kpis": self.check_kpis(doc),
            "spec": stamp_state,
        }
        self.matrix.append((doc.path, states))

    def check_stamp(self, path):
        """Which spec the file was built from, by the stamp its builder wrote into it.

        ✓ this spec · ✗ an earlier version (CON006) · – no stamp (CON007, for the formats
        the builders stamp). Both are warnings: the text checks still run, and the fix is a
        rebuild, which the skill decides — the exit code stays theirs.
        """
        if not spec_stamp.readable(path):
            self.rep.cannot_check("the spec stamp of %s: pypdf is not installed" % path)
            return ABSENT
        found = spec_stamp.read_stamp(path)
        sha = spec_stamp.stamp_sha(found)
        if sha is None:
            if spec_stamp.stampable(path):
                self.rep.warn(path, 1, "CON007", CON007_TEXT)
            return ABSENT
        if sha != self.spec_sha:
            self.rep.warn(path, 1, "CON006", "%s (stamped sha256:%s, the spec is sha256:%s)"
                          % (CON006_TEXT, sha, self.spec_sha))
            return DIFFERS
        return PRESENT

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
        step_spans = [(s.start(), s.end()) for rx in self.next_steps
                      for s in rx.finditer(doc.text)]
        state = ABSENT
        for m in WEEKS.finditer(doc.text):
            lo = m.group(1) or m.group(3)
            hi = m.group(2) or m.group(3)
            try:
                lo, hi = float(lo), float(hi)
            except (TypeError, ValueError):
                continue
            if self.not_a_tier_duration(doc, m, lo, hi, step_spans):
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
        columns = COMPONENTS + [STAMP_COLUMN]
        labels = [label for _, label in columns]
        width = max([len(os.path.basename(p)) for p, _ in self.matrix] + [8]) + 2
        out = ["", "artifact × component  (✓ identical to the spec · ✗ differs · – absent; "
                   "spec: ✓ built from this spec · ✗ from an earlier version · – no stamp)"]
        out.append("  %-*s %s" % (width, "artifact", "  ".join("%-*s" % (len(l), l) for l in labels)))
        for path, states in self.matrix:
            cells = []
            for key, label in columns:
                cells.append("%-*s" % (len(label), states[key].center(len(label))))
            out.append("  %-*s %s" % (width, os.path.basename(path), "  ".join(cells)))
        out.append("")
        return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(prog=PROG, description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", help="packs/<slug>/pack-spec.md")
    ap.add_argument("artifacts", nargs="+", help="the produced artifacts (files or directories)")
    args = ap.parse_args()

    if not os.path.isfile(args.spec):
        PL.die_usage(PROG, "no such spec file: %s" % args.spec)
    spec = PL.load_spec_or_die(args.spec, PROG)
    if not isinstance(spec, dict):
        PL.die_usage(PROG, "%s is not a pack spec" % args.spec)

    rep = PL.Report(PROG)
    checker = Consistency(spec, args.spec, rep)

    files = []
    for target in args.artifacts:
        files.extend(PL.collect_files(target, PROG))

    read = 0
    for path in files:
        # The stamp does not depend on the text: a .pdf skipped for want of pdftotext still
        # says which spec it was built from.
        stamp_state = checker.check_stamp(path)
        doc, reason = PL.extract(path)
        if doc is None:
            rep.warn(path, 1, "CON900", reason)
            rep.cannot_check(reason)
            continue
        read += 1
        checker.run(doc, stamp_state)

    return rep.render("%d artifact(s) against %s" % (read, os.path.basename(args.spec)),
                      tail=checker.render_matrix())


if __name__ == "__main__":
    raise SystemExit(main())
