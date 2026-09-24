#!/usr/bin/env python3
"""Clearance and naming linter for everything a pack skill produces.

    python3 shared/tools/lint_artifact.py out/one-pager.html --channel partner_print
    python3 shared/tools/lint_artifact.py out/ --channel customer_site --spec packs/x/pack-spec.md

It reads .docx (word/document.xml, plus headers, footers and notes), .pptx
(ppt/slides/*.xml and the speaker notes), .html, .js, .md, .txt, .yaml and .pdf
(through `pdftotext`, skipped with a warning when poppler is not installed), then
runs the rules of shared/references/naming-and-clearance.md §1-§4 over the text.
A skill is not done until this is green on every file it wrote.

Findings print as `file:line: CODE message`; for .docx/.pptx/.pdf the line is the
extracted paragraph and the message names the slide or part. Repeats of one
finding in one file collapse into a single line with an occurrence count. A
check that could not run is listed as "not evaluated" — it is not a check that
passed.

Exit codes
    0   clean
    1   findings
    2   usage or dependency error (bad channel, unreadable file, no PyYAML)

Channels
    internal        the deny-list is not enforced; prices and figures may be named
    partner_print   one-pager and deck for Oracle sellers  (customer-facing copy)
    customer_site   the mini-site listing                  (customer-facing copy)
    demo            the interactive walkthrough            (customer-facing copy)

Rule codes
  clearance (§3)
    ART001  a deny-listed customer name appears on a channel that does not allow it
    ART002  a deny-listed mark appears in an asset path, file name or embedded media
    ART003  an Oracle partner-standing claim (tier, award, "preferred partner")
  naming (§1, §2)
    ART101  a catalog `not_this` spelling of a vendor product
    ART102  "AIDP" outside the internal channel — write Oracle AI Data Platform
    ART103  a vendor product name close to, but not, the catalog's `name`/`short`
    ART104  the pack name is not the channel's variant from meta.name_variants
    ART105  a retired family name ("OCI AI Accelerators", "OCI accelerator")
            appears in the artifact's text — on EVERY channel. The family name
            is "Oracle AI & Data Solutions", the mini-site's own lockup; the
            old one still sits in the reference deck and in older briefs, so it
            travels into a new artifact unless it is caught here (2026-09-23)
  vocabulary, customer-facing channels only (§4)
    ART201  a count, total, denominator or ceiling ("seven products", "5 of 7")
    ART202  a negation or absence ("so far", "yet", "not seeing")
    ART203  packaging vocabulary ("packaged", "ready-to-run", "accelerator pack")
    ART204  operating-model vocabulary ("pods", "hardening", "productization")
    ART205  internal taxonomy ("workflow pattern", "L1 / L2", "use-case map")
    ART206  packaging vocabulary inside the pack's own one-liner — on EVERY
            channel, internal included: a one-liner states the job and the
            outcome, never how we package it (§4), and the internal cut of it
            is the line that travels into every other artifact (needs --spec)
  prices (§3)
    ART301  a EUR figure with no disclaimer or footnote marker within 200 characters
    ART302  a non-PoV price on the customer site (needs --spec)
    ART303  a price inside a demo — a walkthrough carries none
  figures and tiers (§3)
    ART401  "proven" with no delivered_result figure beside it (needs --spec)
    ART402  a tier named anything but PoV Jumpstart / Integration / Scaling
    ART403  an S / M / L size tag on a customer-facing channel
  warnings
    ART900  a file was skipped (unsupported format, or pdftotext missing)
    ART901  a check could not run because --spec or --catalog was not supplied

Rule text and rationale: shared/references/naming-and-clearance.md.
Deny-list: shared/tools/denylist.txt (internal to SoftServe; see its header).
"""

from __future__ import annotations

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import packlint as PL  # noqa: E402

PROG = "lint_artifact"

CUSTOMER_FACING = ("partner_print", "customer_site", "demo")
CHANNEL_VARIANT = {"internal": "internal_slide", "partner_print": "external",
                   "customer_site": "site", "demo": "site"}

# Deny-list entries that have a rule of their own, so they are not double-reported.
DEDICATED_DENY = {"AIDP"}

PARTNER_STANDING = re.compile(
    r"\bOracle\s+(?:Platinum|Gold|Silver|Premier|Elite|Preferred)\b"
    r"|\bpreferred\s+partner\b|\bpartner\s+of\s+the\s+year\b"
    r"|\bpartner\s+tier\b|\b(?:Platinum|Gold)\s+partner\b", re.IGNORECASE)

NUM = r"(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)"

VOCAB_RULES = [
    ("ART201", re.compile(r"\b%s\s+of\s+%s\b" % (NUM, NUM), re.IGNORECASE),
     "a ceiling — a reader who is told the denominator counts what is missing"),
    ("ART201", re.compile(r"\b%s\s+(?:products|packs|packages|accelerators|agents|solutions|"
                          r"apps|offerings)\b" % NUM, re.IGNORECASE),
     "states the size of the catalog — say what the reader gets, not how many there are"),
    # A duration or a price IS the reader's own information, so "only 6 weeks" stands.
    ("ART201", re.compile(r"\b(?:all|only|just)\s+%s\b(?!\s*(?:weeks?|days?|months?|hours?"
                          r"|hrs?|min(?:utes)?|%%|€|EUR))" % NUM, re.IGNORECASE),
     "a total — a number is a headline only when it is the reader's own information "
     "(a price, a duration)"),
    ("ART202", re.compile(r"\bso far\b|\bnot yet\b|\byet\b|\bnot seeing\b|\bcoming soon\b"
                          r"|\bno pack (?:for|covers)\b", re.IGNORECASE),
     "names a gap — the copy says what is here, never what is not"),
    ("ART203", re.compile(r"\bpackaged\b|\bready[- ]to[- ]run\b|\baccelerator pack\b"
                          r"|\bevaluation[- ]first\b|\bproductiz(?:ed|ation)\b", re.IGNORECASE),
     "packaging vocabulary — the reader hears a product they cannot buy; state the job "
     "and the outcome"),
    ("ART203", re.compile(r"\bscoped\b(?!\s+per\s+engagement)", re.IGNORECASE),
     "packaging vocabulary (\"scoped per engagement\" on a price is the one cleared use)"),
    ("ART204", re.compile(r"\bpods?\b|\bdelivery pod\b|\bpractice unit\b|\bCOE build[- ]out\b"
                          r"|\bhardening\b|\bproductisation\b", re.IGNORECASE),
     "operating-model vocabulary — it describes our org, not the reader's job"),
    ("ART205", re.compile(r"\bworkflow pattern\b|\buse[- ]case map\b|\bL1\s*/\s*L2\b"
                          r"|\bL[12]\s+(?:pattern|block|category)\b", re.IGNORECASE),
     "internal taxonomy — it exists for our roadmap, not for the reader"),
]

# The ART203 patterns again, applied to the one-liner on every channel (ART206).
PACKAGING_PATTERNS = [(pattern, message) for code, pattern, message in VOCAB_RULES
                      if code == "ART203"]

TIER_RULES = [
    ("ART402", re.compile(r"(?<!PoV )\bJumpstart\b"),
     "the tier is `PoV Jumpstart` — one tier vocabulary everywhere"),
    ("ART402", re.compile(r"\bScale\b(?=[^.\n]{0,40}\b(?:tier|package|phase)\b)"
                          r"|\b(?:Integration)\s*(?:and|&|/|,)\s*Scale\b"),
     "the tier is `Scaling`, not `Scale`"),
    ("ART402", re.compile(r"\bQuick ?Start\b|\bPoC package\b|\bProof of Concept package\b",
                          re.IGNORECASE),
     "a retired tier name — the three tiers are PoV Jumpstart / Integration / Scaling"),
]

SIZE_TAG = re.compile(r"\bS\s*/\s*M\s*/\s*L\b|\b(?:size|tier)\s+tags?\s*[:=]\s*[SML]\b")

# The retired family name, caught the way the retired tier names are (ART402):
# one pattern over the extracted text, on every channel. "Oracle AI & Data
# Solutions" is the lockup the mini-site ships and the only family name.
#
# The lookahead spares Oracle's own catalog entry `OCI AI Accelerator Packs`
# (oci-ai-accelerator-packs), which is a real product an artifact may name. The
# retired lockup never carries "Pack(s)" after it, so the two do not collide.
HEADER_BRAND = "Oracle AI & Data Solutions"
RETIRED_HEADER = re.compile(r"OCI\s+(?:AI\s+)?[Aa]ccelerators?\b(?!\s+[Pp]acks?\b)",
                            re.IGNORECASE)

# A vendor phrase runs on while the next token is capitalized or a connector.
# No punctuation inside a token, so a sentence-ending "Service." stops it.
#
# Two variants, because "one line" means different things per format. In a text
# source (.md, .html, .js, .yaml) a name really can wrap across two source lines,
# so whitespace including the newline joins the phrase. In an EXTRACTED document
# (.pdf, .docx, .pptx) a line is a paragraph or a layout row, and crossing it
# invents names: `pdftotext -layout` puts two columns on one line, so a left
# column ending "…Oracle Fusion Field" followed by a right column starting
# "Planning cycle" was read as "Oracle Fusion Field Planning".
VENDOR_PHRASE = re.compile(
    r"\b(?:Oracle|NVIDIA)(?:\s+(?:for|and|of|the|[A-Z][A-Za-z0-9\-]*))+")
VENDOR_PHRASE_ONE_LINE = re.compile(
    r"\b(?:Oracle|NVIDIA)(?:[ \t]+(?:for|and|of|the|[A-Z][A-Za-z0-9\-]*))+")
STOP_TOKENS = {"oracle", "nvidia", "oci", "the", "for", "and", "of", "a", "an", "by", "on", "in"}
GENERIC_VENDOR_PHRASES = {
    "oracle cloud infrastructure", "oracle cloud", "nvidia ai enterprise", "nvidia nemo",
    "nvidia nemo agent toolkit", "nvidia ai-q", "nvidia cuopt", "nvidia vss",
    "oracle ai & data", "oracle ai and data", "oracle fusion applications",
    "oracle marketplace", "oci marketplace",
}


def split_vendor_phrase(raw: str):
    """[(offset, phrase)] — one entry per vendor name inside a matched run.

    "Oracle Cloud Infrastructure and Oracle Autonomous AI Lakehouse" is two
    correct names joined by "and", not one wrong one, so a new Oracle/NVIDIA
    token starts a new phrase and trailing connectors are dropped.
    """
    starts = [sm.start() for sm in re.finditer(r"\b(?:Oracle|NVIDIA)\b", raw)]
    if not starts:
        return []
    bounds = starts + [len(raw)]
    out = []
    for i in range(len(starts)):
        piece = raw[bounds[i]:bounds[i + 1]]
        phrase = PL.norm_ws(piece).rstrip(".,;:")
        while phrase.split() and phrase.split()[-1].lower() in ("for", "and", "of", "the"):
            phrase = phrase.rsplit(" ", 1)[0]
        if phrase:
            out.append((bounds[i], phrase))
    return out


def covered_by_good_name(text, match, names):
    """True when this `not_this` match sits inside an accepted catalog name.

    Two catalog habits land here. Some entries mark the bare form `not_this`
    because the vendor prefix is mandatory ("cuOpt" → "NVIDIA cuOpt"); some mark a
    spelling that differs from the accepted one only in case ("NVIDIA Nemo"
    against the catalog's own "NVIDIA NeMo", "Nemo" against "NeMo"). Both are the
    same test — an accepted name occupies the match — and the relative length of
    the two strings has nothing to do with it:

    * a name that spans MORE than the match covers it whatever its case;
    * a name that spans exactly the match has to match it letter for letter,
      because the case IS the whole difference between the two spellings.
    """
    if not names:
        return False
    start = max(0, match.start() - 80)
    window = text[start:match.end() + 80]
    for name in names:
        for gm in re.finditer(re.escape(name), window, re.IGNORECASE):
            gs, ge = start + gm.start(), start + gm.end()
            if gs > match.start() or ge < match.end():
                continue
            if gs == match.start() and ge == match.end():
                if text[gs:ge] == name:        # written exactly as the catalog spells it
                    return True
                continue                        # same span, wrong case: a finding
            return True
    return False


class ArtifactLint:
    def __init__(self, channel, spec, catalog, deny, rep):
        self.channel = channel
        self.spec = spec
        self.catalog = catalog
        self.deny = deny
        self.rep = rep
        self.hits = {}          # (path, code, key) -> [line, label, message, count]
        self.customer_facing = channel in CUSTOMER_FACING
        self.deny_enforced = channel != "internal" and not self._cleared()
        self.pov_prices, self.other_prices = self._prices()
        self.delivered_figures = self._delivered_figures()
        self.one_liners = self._one_liners()

    # -- spec-derived state -------------------------------------------------
    def _cleared(self):
        if not self.spec:
            return False
        allowed = PL.dig(self.spec, "clearance", "customer_name_allowed", default={})
        return bool(isinstance(allowed, dict) and allowed.get(self.channel) is True)

    def _prices(self):
        pov, other = set(), set()
        tiers = PL.dig(self.spec or {}, "packages", "tiers", default=[])
        if not isinstance(tiers, list):
            return pov, other
        for tier in tiers:
            if not isinstance(tier, dict):
                continue
            bucket = pov if str(tier.get("id") or "").strip() == "pov" else other
            for key in ("services_price", "infra_price_monthly"):
                price = tier.get(key)
                if not isinstance(price, dict):
                    continue
                if price.get("value") is not None:
                    bucket.add(float(price["value"]))
                for end in (price.get("range") or []):
                    try:
                        bucket.add(float(end))
                    except (TypeError, ValueError):
                        pass
        return pov, other

    def _one_liners(self):
        """The spec's one-liner, normalized, so it can be recognized in an artifact."""
        out = []
        for key in ("full", "short"):
            value = PL.dig(self.spec or {}, "one_liner", key)
            if PL.is_filled(value):
                flat = PL.norm_loose(str(value))
                if len(flat) > 20:          # too short to identify a line by
                    out.append(flat)
        return out

    def _delivered_figures(self):
        out = []
        kpis = (self.spec or {}).get("kpis")
        if isinstance(kpis, list):
            for kpi in kpis:
                if isinstance(kpi, dict) and kpi.get("figure_status") == "delivered_result":
                    if PL.is_filled(kpi.get("figure")):
                        out.append(PL.norm_loose(str(kpi["figure"])))
        return out

    # -- finding plumbing ---------------------------------------------------
    def hit(self, doc, code, start, end, message, key=None):
        line, label = doc.where(start)
        key = (doc.path, code, (key or doc.text[start:end]).lower())
        if key in self.hits:
            self.hits[key][3] += 1
            return
        self.hits[key] = [line, label, message, 1]

    def flush(self):
        for (path, code, _), (line, label, message, count) in self.hits.items():
            suffix = label
            if count > 1:
                suffix += " (%d occurrences)" % count
            self.rep.fail(path, line, code, message + suffix)

    # -- the rules ----------------------------------------------------------
    def run(self, doc):
        self.check_denylist(doc)
        self.check_assets(doc)
        self.check_partner_standing(doc)
        self.check_naming(doc)
        self.check_retired_header(doc)
        self.check_vocabulary(doc)
        self.check_one_liner(doc)
        self.check_prices(doc)
        self.check_proven(doc)
        self.check_tiers(doc)
        self.check_name_variant(doc)

    def check_denylist(self, doc):
        if not self.deny_enforced:
            return
        for entry in self.deny:
            if entry.term in DEDICATED_DENY or entry.is_path:
                continue
            for m in entry.regex.finditer(doc.text):
                self.hit(doc, "ART001", m.start(), m.end(),
                         "names `%s`, which is on the deny-list — describe the customer by "
                         "industry and scale (clearance.anonymized_descriptor), or record the "
                         "approval in clearance.customer_name_allowed.%s"
                         % (entry.term, self.channel),
                         key=entry.term)
        if self.channel != "internal":
            for m in re.finditer(r"\bAIDP\b", doc.text):
                self.hit(doc, "ART102", m.start(), m.end(),
                         "\"AIDP\" is internal shorthand — write Oracle AI Data Platform; "
                         "Oracle never uses the abbreviation in copy anyone else reads",
                         key="AIDP")

    def check_assets(self, doc):
        """Asset paths, file names and media embedded in a .docx/.pptx container.

        One finding per asset, naming the first deny-list entry it carries, so a
        path that matches both a customer name and `logos/` is reported once.
        """
        if not self.deny_enforced:
            return
        tokens = set(re.findall(r"[\w./\\-]+\.(?:svg|png|jpe?g|webp|gif|pdf|emf|wmf)", doc.text))
        tokens.update(doc.assets)
        covered = []
        for token in sorted(tokens):
            slugs = PL.asset_slug_candidates(token)
            entry = next((e for e in self.deny if e.slug and e.slug in slugs), None)
            if entry is None:
                continue
            where = doc.text.find(token)
            covered.append(token)
            self.hit(doc, "ART002", max(where, 0), max(where, 0) + len(token),
                     "asset `%s` carries the deny-listed mark `%s` — a mark that is merely "
                     "unreferenced is still shipped; keep it outside the publishable root"
                     % (token, entry.term), key=token)
        for entry in self.deny:
            if not entry.is_path:
                continue
            for m in entry.regex.finditer(doc.text):
                if any(entry.term.lower() in t.lower() for t in covered
                       if t in doc.text[max(0, m.start() - 200):m.end() + 200]):
                    continue
                self.hit(doc, "ART002", m.start(), m.end(),
                         "references `%s` — no cleared logo file exists; ship the wordmark "
                         "as text" % entry.term, key=entry.term)

    def check_partner_standing(self, doc):
        for m in PARTNER_STANDING.finditer(doc.text):
            self.hit(doc, "ART003", m.start(), m.end(),
                     "`%s` is a partner-standing claim — never on any channel; what may be "
                     "said is joint delivery with Oracle's AI & Data organization"
                     % PL.norm_ws(m.group(0)))

    def check_naming(self, doc):
        if not self.catalog:
            return
        known, entries = set(), self.catalog["entries"]
        wrong_spellings = set()
        # Every string the catalog accepts, raw, for the containment test below.
        good_names = [v for e in entries for v in ([e["name"], e["short"]] + e["aliases"]) if v]
        for entry in entries:
            for value in [entry["name"], entry["short"]] + entry["aliases"]:
                if value:
                    known.add(PL.norm_loose(value))
            for wrong in entry["not_this"]:
                if wrong in DEDICATED_DENY:      # AIDP has its own rule (ART102)
                    continue
                wrong_spellings.add(PL.norm_loose(wrong))
                # "cuOpt" is `not_this` because the vendor prefix is required, and it
                # is also the tail of the correct "NVIDIA cuOpt"; "NVIDIA Nemo" is
                # `not_this` for a capital letter the catalog's own "NVIDIA NeMo"
                # has. A wrong spelling that sits inside an occurrence of an accepted
                # name is not a finding, whichever of the two strings is longer.
                containing = [g for g in good_names if wrong.lower() in g.lower()]
                for m in re.finditer(r"(?<![\w-])%s(?![\w-])" % re.escape(wrong), doc.text,
                                     re.IGNORECASE):
                    if covered_by_good_name(doc.text, m, containing):
                        continue
                    self.hit(doc, "ART101", m.start(), m.end(),
                             "`%s` is the spelling the catalog marks `not_this` — write `%s`"
                             % (wrong, entry["name"] or entry["id"]), key=wrong.lower())
        known |= GENERIC_VENDOR_PHRASES
        catalog_tokens = [(e, {t for t in PL.norm_loose(e["name"]).split() if t not in STOP_TOKENS})
                          for e in entries if e["name"]]
        phrase_re = VENDOR_PHRASE if doc.kind == "text" else VENDOR_PHRASE_ONE_LINE
        for m in phrase_re.finditer(doc.text):
            for offset, phrase in split_vendor_phrase(m.group(0)):
                start = m.start() + offset
                flat = PL.norm_loose(phrase)
                if not flat or flat in known or flat in wrong_spellings:
                    continue                      # a not_this spelling is already ART101
                tokens = {t for t in flat.split() if t not in STOP_TOKENS}
                if not tokens:
                    continue
                best, overlap = None, 0
                for entry, cat_tokens in catalog_tokens:
                    shared = len(tokens & cat_tokens)
                    if shared > overlap:
                        best, overlap = entry, shared
                if best and overlap >= 2 and flat != PL.norm_loose(best["name"]):
                    # The phrase pattern stops at a parenthesis: "Oracle Customer
                    # Experience (CX)" on the page is caught as "Oracle Customer
                    # Experience". When the text right after the phrase completes the
                    # canonical name, the artifact spells it in full (2026-09-23).
                    canon = PL.norm_loose(best["name"])
                    tail = doc.text[start + len(phrase):start + len(phrase) + 40]
                    if canon.startswith(flat + " ") and PL.norm_loose(phrase + tail).startswith(canon):
                        continue   # a whole-word prefix completed by what follows — not "Field Services" for "Field Service"
                    # In an extracted document a rendered line break cuts a name in
                    # two ("Oracle Fusion Field" / "Service customer …"), and the cut
                    # is the extractor's, not the artifact's. A phrase that is a
                    # prefix of the canonical name is that case, not a misspelling.
                    if (doc.kind != "text"
                            and PL.norm_loose(best["name"]).startswith(flat + " ")):
                        continue
                    self.hit(doc, "ART103", start, start + len(phrase),
                             "`%s` is not how the catalog spells it — write `%s` (vendor names "
                             "are volatile; re-verify against the vendor's own page before "
                             "shipping)" % (phrase, best["name"]), key=flat)

    def check_retired_header(self, doc):
        """ART105 — the retired family name, on every channel."""
        for m in RETIRED_HEADER.finditer(doc.text):
            self.hit(doc, "ART105", m.start(), m.end(),
                     "`%s` is the retired family name — every print artifact carries `%s`, the "
                     "mini-site's own lockup; fix it in the brief's header key, not in the "
                     "artifact" % (PL.norm_ws(m.group(0)), HEADER_BRAND),
                     key=PL.norm_ws(m.group(0)).lower())

    def check_vocabulary(self, doc):
        if not self.customer_facing:
            return
        for code, pattern, message in VOCAB_RULES:
            for m in pattern.finditer(doc.text):
                self.hit(doc, code, m.start(), m.end(),
                         "`%s` — %s" % (PL.norm_ws(m.group(0)), message))

    def check_one_liner(self, doc):
        """Packaging vocabulary inside the pack's one-liner, on every channel.

        §4: a one-liner states the job and the outcome, never how we package it.
        The rule is not channel-scoped the way the rest of §4 is — the internal
        cut of the one-liner is the string every other artifact inherits, so a
        feature list on the `internal` channel is where "packaged" has to be
        caught, not three artifacts later.
        """
        if not self.one_liners:
            return
        seen = set()            # the 1-3 line windows overlap; count a match once
        offset = 0
        for i, line in enumerate(doc.lines):
            # a one-liner may be wrapped over two or three source lines; "\n" and
            # " " are both one character, so offsets inside the window still map
            # onto doc.text unchanged.
            for width in (1, 2, 3):
                chunk = " ".join(doc.lines[i:i + width])
                flat = PL.norm_loose(chunk)
                if not flat or not any(one in flat or flat in one for one in self.one_liners):
                    continue
                for pattern, message in PACKAGING_PATTERNS:
                    for m in pattern.finditer(chunk):
                        if (offset + m.start()) in seen:
                            continue
                        seen.add(offset + m.start())
                        self.hit(doc, "ART206", offset + m.start(), offset + m.end(),
                                 "`%s` sits in the pack's one-liner — %s. The one-liner is the "
                                 "one string every artifact inherits, so this is a finding on "
                                 "every channel; fix it in the spec, not in the artifact"
                                 % (PL.norm_ws(m.group(0)), message),
                                 key="one-liner:%s" % PL.norm_ws(m.group(0)).lower())
            offset += len(line) + 1

    def check_prices(self, doc):
        for m in PL.MONEY_RE.finditer(doc.text):
            token = PL.norm_ws(m.group(0))
            value = PL.money_value(token)
            ctx = PL.context(doc.text, m.start(), m.end(), 200)
            if not PL.DISCLAIMER_RE.search(ctx):
                self.hit(doc, "ART301", m.start(), m.end(),
                         "`%s` carries no disclaimer within 200 characters — a price never "
                         "ships without its footnote, and the footnote travels in the same "
                         "block" % token, key=token)
            if self.channel == "demo":
                self.hit(doc, "ART303", m.start(), m.end(),
                         "`%s` — a demo carries no prices; every figure inside a walkthrough "
                         "is synthetic" % token, key=token)
            elif self.channel == "customer_site":
                if not self.spec:
                    continue
                if value is not None and self.other_prices and value in self.other_prices:
                    self.hit(doc, "ART302", m.start(), m.end(),
                             "`%s` is not the PoV price — the customer site publishes the PoV "
                             "price only; other tiers read \"scoped per engagement\"" % token,
                             key=token)
                elif value is not None and self.pov_prices and value not in self.pov_prices:
                    self.hit(doc, "ART302", m.start(), m.end(),
                             "`%s` is not a price the spec carries for the PoV tier — the "
                             "customer site publishes the PoV price only" % token, key=token)

    def check_proven(self, doc):
        if not self.spec:
            return
        for m in re.finditer(r"\bproven\b", doc.text, re.IGNORECASE):
            ctx = PL.norm_loose(PL.context(doc.text, m.start(), m.end(), 200))
            if not any(fig and fig in ctx for fig in self.delivered_figures):
                self.hit(doc, "ART401", m.start(), m.end(),
                         "\"proven\" with no delivered_result figure beside it — say `proven` "
                         "only for a delivered, accepted result; a PoV result is a proof of "
                         "value and carries its caveat", key="proven")

    def check_tiers(self, doc):
        for code, pattern, message in TIER_RULES:
            for m in pattern.finditer(doc.text):
                self.hit(doc, code, m.start(), m.end(),
                         "`%s` — %s" % (PL.norm_ws(m.group(0)), message))
        if self.customer_facing:
            for m in SIZE_TAG.finditer(doc.text):
                self.hit(doc, "ART403", m.start(), m.end(),
                         "`%s` — S/M/L survive only as size tags in internal tables"
                         % PL.norm_ws(m.group(0)))

    def check_name_variant(self, doc):
        if not self.spec:
            return
        name = PL.dig(self.spec, "meta", "name")
        variants = PL.dig(self.spec, "meta", "name_variants", default={})
        if not PL.is_filled(name) or not isinstance(variants, dict):
            return
        expected = variants.get(CHANNEL_VARIANT[self.channel])
        if not PL.is_filled(expected):
            return
        expected = PL.norm_ws(str(expected))
        plain = PL.norm_ws(str(name).strip())
        pattern = re.compile(r"%s(\s+App\b)?" % re.escape(str(name).strip()), re.IGNORECASE)
        for m in pattern.finditer(doc.text):
            got = PL.norm_ws(m.group(0))
            if got == expected:
                continue
            # Internal copy may write the plain name or the "<name> App" form: the
            # App suffix is the executive-slide convention (§2), not a requirement
            # on every internal sentence. What internal may NOT do is drift in case.
            if self.channel == "internal" and got.lower() in (plain.lower(),
                                                              expected.lower()):
                continue
            self.hit(doc, "ART104", m.start(), m.end(),
                     "the pack is written `%s`; on `%s` the name is `%s` "
                     "(meta.name_variants.%s)"
                     % (got, self.channel, expected, CHANNEL_VARIANT[self.channel]),
                     key=got)


def main() -> int:
    ap = argparse.ArgumentParser(prog=PROG, description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", help="a produced artifact, or a directory of them")
    ap.add_argument("--channel", required=True,
                    choices=["internal", "partner_print", "customer_site", "demo"],
                    help="who reads this artifact; sets which rules apply")
    ap.add_argument("--spec", help="packs/<slug>/pack-spec.md — enables the clearance "
                                   "switch, the price, name-variant and `proven` checks")
    ap.add_argument("--denylist", "--deny-list", dest="denylist", default=PL.DEFAULT_DENYLIST,
                    help="deny-list file (default: shared/tools/denylist.txt)")
    ap.add_argument("--catalog", default=PL.DEFAULT_CATALOG,
                    help="Oracle product catalog (default: shared/data/oracle-products.yaml)")
    args = ap.parse_args()

    rep = PL.Report(PROG)
    files = PL.collect_files(args.target, PROG)
    deny = PL.load_denylist(args.denylist, PROG)

    spec = None
    if args.spec:
        if not os.path.isfile(args.spec):
            PL.die_usage(PROG, "no such spec file: %s" % args.spec)
        spec = PL.load_spec_or_die(args.spec, PROG)
        if not isinstance(spec, dict):
            PL.die_usage(PROG, "%s is not a pack spec" % args.spec)
    else:
        rep.warn(args.target, 1, "ART901",
                 "no --spec: clearance switch, price, name-variant and `proven` checks fall "
                 "back to defaults")
        rep.cannot_check("prices against the spec, the channel name variant, and \"proven\" "
                         "against figure_status (pass --spec)")

    catalog = None
    if os.path.isfile(args.catalog):
        catalog = PL.load_catalog(args.catalog, PROG)
    else:
        rep.warn(args.target, 1, "ART901",
                 "catalog not found at %s — vendor product spellings not checked" % args.catalog)
        rep.cannot_check("vendor product names against the catalog (%s)" % args.catalog)

    lint = ArtifactLint(args.channel, spec, catalog, deny, rep)
    read = 0
    for path in files:
        doc, reason = PL.extract(path)
        if doc is None:
            rep.warn(path, 1, "ART900", reason)
            rep.cannot_check(reason)
            continue
        read += 1
        lint.run(doc)
    lint.flush()

    if lint.deny_enforced is False and args.channel != "internal":
        rep.warn(args.target, 1, "ART901",
                 "clearance.customer_name_allowed.%s is true in the spec — the deny-list is "
                 "not enforced on this run" % args.channel)
    return rep.render("%d file(s), channel %s" % (read, args.channel))


if __name__ == "__main__":
    raise SystemExit(main())
