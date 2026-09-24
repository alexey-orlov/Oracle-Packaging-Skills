#!/usr/bin/env python3
"""Validate a pack spec against shared/schema/pack-spec.md.

    python3 shared/tools/lint_spec.py packs/<slug>/pack-spec.md
    python3 shared/tools/lint_spec.py packs/<slug>/pack-spec.md --strict
    python3 shared/tools/lint_spec.py packs/<slug>/pack-spec.md --strict --signoff
    python3 shared/tools/lint_spec.py <spec> --catalog shared/data/oracle-products.yaml \
                                             --roadmap shared/data/roadmap-items.csv

The spec is the single source of truth for every artifact, so this runs before
any build skill reads it, and again before a pack is called done. Findings print
as `file:line: CODE message`, followed by a per-component completeness table and
one summary line.

Exit codes
    0   clean
    1   findings
    2   usage or dependency error (bad arguments, unreadable spec, no PyYAML)

Rule codes
    SPEC001  a component key is missing from the spec
    SPEC002  a required key inside a component is missing or empty
    SPEC003  a first-order component (problem_solution, one_liner, icp, name)
             carries no `source: user:<date>` while meta.status is confirmed
    SPEC004  oracle_products[].id or architecture.stack[].catalog_id is not in
             the product catalog (a product missing from the catalog is a
             catalog change request, never a free-text entry —
             naming-and-clearance.md §1)
    SPEC005  meta.roadmap_item_id is not in the roadmap extract
    SPEC006  PoV duration_weeks.max is above 8 weeks with no `justification`
    SPEC007  PoV duration_weeks.max is above the 10-week hard cap
    SPEC008  two metric sets — a KPI name appears twice with different figures
    SPEC009  the tier set or a tier name is not exactly
             PoV Jumpstart / Integration / Scaling
    SPEC010  a deny-listed customer name sits in customer-facing spec copy
             (name, one_liner, problem_solution, icp, verticals, kpis
             attribution.otherwise) — naming-and-clearance.md §3
    SPEC011  a kpis[].figure carries no figure_status
    SPEC012  a kpis[].figure carries no caveat
    SPEC013  clearance.customer_name_allowed is missing a channel, or the value
             is not a boolean (internal, partner_print, customer_site, demo)
    SPEC014  open_questions is absent (it may be an empty list, never missing)
    SPEC015  meta.status is not one of the documented status values
    SPEC016  oracle_products[].role is not `required` or `optional`
    SPEC017  a meta.name_variants entry does not follow the channel rule
             (naming-and-clearance.md §2) — warning unless --strict
    SPEC018  oracle_products[] carries a non-Oracle catalog entry — NVIDIA
             components belong in architecture.stack[].catalog_id, because the
             required/optional roll-up across packs is an Oracle question
    SPEC900  the Oracle product catalog was not found — ids not checked
    SPEC901  the roadmap extract was not found — roadmap id not checked
    SPEC902  a recommended key is missing (--strict only)
    SPEC019  workflow has more than 7 steps (5-7, grouped at the buyer's checkpoints)
    SPEC020  workflow has fewer than 3 steps (warning)
    SPEC021  more than 3 required Oracle products (warning)
    SPEC022  more than 4 optional Oracle products (warning)
    SPEC023  the capability tree is too fine for a one-page feature list
             (warning): more than 6 areas, 14 categories or 40 features
    SPEC024  a record in a list the spec layout knows carries a key the layout
             does not define (workflow and architecture inputs, outputs and
             steps, the stack, industries, capability areas, categories and
             features, Oracle products, metrics, tiers, capability handling,
             open questions, provenance inputs — packspec.RECORD_LISTS), or a
             capability feature has no status (warning). An unknown key is
             almost always an unquoted YAML inline mapping whose value held a
             comma: `{ name: Repair, replace or refer, status: ... }` parses as
             name="Repair" plus junk keys, so the row silently loses everything
             after the comma. Valid YAML, wrong data. A spec converted to Markdown
             keeps such keys — an extra table column, or an entry under Other
             fields — so they stay visible until the value is set back whole.
    SPEC025  the metric set carries no business metric (warning): every metric
             is marked `kind: technical`, or `kind` itself is not one of
             business | leading | technical. Sales artifacts print business
             metrics; a set with none leaves the deck's tiles, the one-pager's
             proof strip and the site's metrics with nothing to say
    SPEC026  a metric whose name reads as a proof criterion or a vanity count is
             not marked `kind: technical` (warning) — "reviewer agreement",
             "coverage", precision / recall / accuracy / latency, "documents
             processed". Technical criteria belong to the PoV package's success
             line, never to a sales tile
    SPEC027  a `business` metric carries no `owner_role` (warning) — the
             buyer-side role who would sign the number off is the test that the
             metric is the business's rather than ours
    SPEC028  a retired family name ("OCI AI Accelerator(s)", "OCI accelerator")
             sits in meta.eyebrow, deck.running_header,
             exec_summary.running_header or one_pager.eyebrow — the family name
             on every print artifact is "Oracle AI & Data Solutions"
    SPEC029  the spec does not parse — a structural slip, named on its own line;
             nothing else is checked until it does

--strict    promotes SPEC900/901/902 and SPEC017 to findings: the completeness
            check, usable on a spec at any status. A `draft` stays clean under
            it as long as every component it does carry is complete.
--signoff   additionally applies the first-order `user:` source rule whatever
            meta.status says — "would this pass as confirmed?". The rule is on
            by itself once meta.status is `confirmed` or `built`, so this flag
            is for asking the question early, on a draft.

The rules and their wording come from shared/references/naming-and-clearance.md
and shared/schema/pack-spec.md; when a rule moves, those are rewritten first.
"""

from __future__ import annotations

import argparse
import collections
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import packlint as PL  # noqa: E402

PROG = "lint_spec"

STATUS_VALUES = ("draft", "research", "options", "signing-off", "confirmed", "built")
CONFIRMED_STATUSES = ("confirmed", "built")
FIGURE_STATUSES = ("pov_result", "delivered_result", "target", "modeled")

# `kind` decides where a metric may be printed (shared/schema/pack-spec.md).
# Absent means `business`: the default has to be the one sales artifacts print,
# or a brief written before this key existed would silently lose its tiles.
KPI_KINDS = ("business", "leading", "technical")
DEFAULT_KPI_KIND = "business"

# Names that read as a proof-of-value acceptance criterion or a vanity count
# rather than as something the business is willing to improve. A match is not a
# verdict — it asks for `kind: technical`, which is where such a metric belongs.
TECHNICAL_NAME_RE = re.compile(
    r"\bagreement\b|\bprecision\b|\brecall\b|\baccurac(?:y|ies)\b|\blatenc(?:y|ies)\b"
    r"|\bcoverage\b|\bconfidence\b|\bcalibrat|\bcitation|\bF1\b|\bthroughput\b"
    r"|\bprocessed\b|\bingested\b|\bonboarded\b|\bsurfaced\b|\bsignals?\b"
    r"|\bdocuments?\b|\btokens?\b|\buptime\b", re.IGNORECASE)

# The family name retired on 2026-09-23; the mini-site lockup is the only one.
HEADER_BRAND = PL.HEADER_BRAND
RETIRED_HEADER_RE = PL.RETIRED_HEADER_RE
HEADER_KEYS = (("meta", "eyebrow"), ("deck", "running_header"),
               ("exec_summary", "running_header"), ("one_pager", "eyebrow"))

# The repo's written convention for an empty cell (`-`). A metric that is defined
# and measured per engagement but carries no cleared headline figure says so with
# `figure: "-"`, and then has no figure_status, caveat or attribution to give.
EMPTY_MARKERS = {"-", "--", "—", "–", "n/a"}


def has_value(value) -> bool:
    """Filled, and not the `-` that means 'deliberately empty'."""
    return PL.is_filled(value) and str(value).strip().lower() not in EMPTY_MARKERS

# component label → (spec key, required sub-keys)
REQUIRED_KEYS = {
    "meta": ["slug", "name", "name_variants", "roadmap_item_id", "status"],
    "clearance": ["customer_name_allowed", "anonymized_descriptor"],
    "problem_solution": ["problem", "solution"],
    "one_liner": ["full", "short"],
    "icp": ["line", "buyer_roles"],
    "workflow": ["inputs", "steps", "outputs"],
    "architecture": ["inputs", "stack", "outputs"],
    "packages": ["tiers", "capability_handling", "why_it_sells_for_the_partner"],
    "contacts": ["partner_print", "site", "internal"],
    "provenance": ["inputs"],
}

# list components → required keys on each item
LIST_ITEM_KEYS = {
    "verticals": ["name", "framing", "status"],
    "capabilities": ["area", "categories"],
    "oracle_products": ["id", "role", "why"],
    # `attribution` is asserted in check_kpis, and only for a metric that carries a
    # real figure: there is nothing to attribute when the figure is `-`.
    "kpis": ["name", "formula", "figure"],
}

RECOMMENDED = [
    ("meta", "source_engagement"), ("meta", "spec_version"),
    ("clearance", "internal_only_facts"),
    ("problem_solution", "reframe"), ("one_liner", "banned_words_checked"),
    ("icp", "qualifying_signals"), ("icp", "disqualifiers"),
    ("packages", "target_oci_consumption"),
]

# The 12 components in sign-off order, plus the cross-cutting keys.
COMPONENT_ROWS = [
    ("1", "problem <-> solution", "problem_solution"),
    ("2", "one-liner", "one_liner"),
    ("3", "target ICP", "icp"),
    ("4", "name", "meta.name"),
    ("5", "verticals", "verticals"),
    ("6", "capabilities", "capabilities"),
    ("7", "workflow architecture", "workflow"),
    ("8", "high-level architecture", "architecture"),
    ("9", "required Oracle products", "oracle_products:required"),
    ("10", "optional Oracle products", "oracle_products:optional"),
    ("11", "key performance metrics", "kpis"),
    ("12", "service packages", "packages"),
    ("-", "meta", "meta"),
    ("-", "clearance", "clearance"),
    ("-", "contacts", "contacts"),
    ("-", "provenance", "provenance"),
    ("-", "open questions", "open_questions"),
]

FIRST_ORDER = {
    "problem_solution": ("problem_solution", "source"),
    "one_liner": ("one_liner", "source"),
    "icp": ("icp", "source"),
    "meta.name": ("meta", "name_source"),
}

# Spec copy a customer name may never appear in (naming-and-clearance.md §3).
DENY_SCAN = ["one_liner", "problem_solution", "icp", "verticals"]


class SpecLint:
    def __init__(self, path, spec, rep, strict, signoff=False):
        self.path = path
        self.spec = spec
        self.rep = rep
        self.strict = strict
        self.signoff = signoff
        self.per_component = collections.Counter()

    # -- finding helpers ----------------------------------------------------
    def fail(self, component, line, code, message):
        self.per_component[component] += 1
        self.rep.fail(self.path, line, code, message)

    def soft(self, component, line, code, message):
        """A warning, or a finding under --strict."""
        if self.strict:
            self.fail(component, line, code, message)
        else:
            self.rep.warn(self.path, line, code, message)

    # -- checks -------------------------------------------------------------
    def check_present(self):
        spec = self.spec
        reported = set()
        for row in COMPONENT_ROWS:
            key = row[2].split(":")[0].split(".")[0]
            if key in ("open_questions",) or key in reported or key in spec:
                continue
            reported.add(key)
            self.fail(row[2], PL.lineno(spec), "SPEC001",
                      "component `%s` is missing — the spec is the only source an "
                      "artifact builder may read" % key)
        if "open_questions" not in spec:
            self.fail("open_questions", PL.lineno(spec), "SPEC014",
                      "`open_questions` is absent — it may be an empty list, never missing; "
                      "artifacts print nothing that depends on an open question")

    def check_required_keys(self):
        for key, needed in REQUIRED_KEYS.items():
            node = self.spec.get(key)
            if not isinstance(node, dict):
                continue
            for sub in needed:
                if not PL.is_filled(node.get(sub)):
                    self.fail(key, PL.lineno(node, sub), "SPEC002",
                              "%s.%s is missing or empty" % (key, sub))
        variants = PL.dig(self.spec, "meta", "name_variants")
        if isinstance(variants, dict):
            for sub in ("site", "internal_slide", "external"):
                if not PL.is_filled(variants.get(sub)):
                    self.fail("meta", PL.lineno(variants, sub), "SPEC002",
                              "meta.name_variants.%s is missing — every channel renders "
                              "its own form of the one plain name" % sub)
        for key, item_keys in LIST_ITEM_KEYS.items():
            node = self.spec.get(key)
            if node is None:
                continue
            if not isinstance(node, list):
                self.fail(key, PL.lineno(self.spec, key), "SPEC002",
                          "`%s` must be a list" % key)
                continue
            if not node:
                self.fail(key, PL.lineno(self.spec, key), "SPEC002",
                          "`%s` is empty" % key)
                continue
            for i, item in enumerate(node):
                where = PL.lineno(node, i)
                if not isinstance(item, dict):
                    self.fail(key, where, "SPEC002", "%s[%d] is not a mapping" % (key, i))
                    continue
                for sub in item_keys:
                    if not PL.is_filled(item.get(sub)):
                        self.fail(key, PL.lineno(item, sub, where), "SPEC002",
                                  "%s[%d].%s is missing or empty" % (key, i, sub))
        if self.strict:
            for key, sub in RECOMMENDED:
                node = self.spec.get(key)
                if isinstance(node, dict) and not PL.is_filled(node.get(sub)):
                    self.soft(key, PL.lineno(node), "SPEC902",
                              "%s.%s is not filled in" % (key, sub))

    def check_status_and_sources(self):
        status = PL.dig(self.spec, "meta", "status")
        meta = self.spec.get("meta")
        if status is not None and status not in STATUS_VALUES:
            self.fail("meta", PL.lineno(meta, "status"), "SPEC015",
                      "meta.status `%s` is not one of %s" % (status, " | ".join(STATUS_VALUES)))
        enforce = self.signoff or status in CONFIRMED_STATUSES
        for component, (key, sub) in FIRST_ORDER.items():
            node = self.spec.get(key)
            value = node.get(sub) if isinstance(node, dict) else None
            if value is None and key == "meta":
                value = PL.dig(self.spec, "meta", "sources", "name")
            if not enforce:
                continue
            line = PL.lineno(node, sub) if isinstance(node, dict) else PL.lineno(self.spec, key)
            if not PL.is_filled(value):
                self.fail(component, line, "SPEC003",
                          "%s.%s is missing — a confirmed spec records the four first-order "
                          "components as `user:<date>`" % (key, sub))
            elif not re.match(r"^user:\d{4}-\d{2}-\d{2}$", str(value).strip()):
                self.fail(component, line, "SPEC003",
                          "%s.%s is `%s` — a first-order component is confirmed by the user, "
                          "so the source reads `user:<YYYY-MM-DD>`" % (key, sub, value))

    def check_clearance(self):
        clearance = self.spec.get("clearance")
        if not isinstance(clearance, dict):
            return
        allowed = clearance.get("customer_name_allowed")
        if not isinstance(allowed, dict):
            self.fail("clearance", PL.lineno(clearance, "customer_name_allowed"), "SPEC013",
                      "clearance.customer_name_allowed must name all four channels: %s"
                      % ", ".join(PL.CHANNELS))
            return
        for channel in PL.CHANNELS:
            if channel not in allowed:
                self.fail("clearance", PL.lineno(allowed), "SPEC013",
                          "clearance.customer_name_allowed.%s is absent — clearance is per "
                          "channel and defaults to false, but it is recorded, not assumed"
                          % channel)
            elif not isinstance(allowed[channel], bool):
                self.fail("clearance", PL.lineno(allowed, channel), "SPEC013",
                          "clearance.customer_name_allowed.%s is `%s` — it is true or false, "
                          "set by a recorded approval" % (channel, allowed[channel]))
        for channel in allowed:
            if channel not in PL.CHANNELS:
                self.fail("clearance", PL.lineno(allowed, channel), "SPEC013",
                          "clearance.customer_name_allowed.%s is not a channel (%s)"
                          % (channel, ", ".join(PL.CHANNELS)))

    def check_build(self):
        """SPEC030 — the build settings hold only the values the build knows."""
        build = self.spec.get("build")
        if build is None:
            return
        ps = PL._packspec()
        if not isinstance(build, dict):
            self.fail("build", PL.lineno(self.spec, "build"), "SPEC030",
                      "build is a record: artifacts and audience")
            return
        artifacts = build.get("artifacts")
        if artifacts is not None:
            items = artifacts if isinstance(artifacts, list) else [artifacts]
            for item in items:
                if item not in ps.BUILD_ARTIFACTS:
                    self.fail("build", PL.lineno(build, "artifacts"), "SPEC030",
                              "build.artifacts has `%s` — the artifacts are %s"
                              % (item, ", ".join(ps.BUILD_ARTIFACTS)))
        audience = build.get("audience")
        if audience is not None and audience not in ps.BUILD_AUDIENCES:
            self.fail("build", PL.lineno(build, "audience"), "SPEC030",
                      "build.audience is `%s` — it is %s"
                      % (audience, " or ".join(ps.BUILD_AUDIENCES)))

    def check_products(self, catalog):
        products = self.spec.get("oracle_products")
        if not isinstance(products, list):
            return
        for i, item in enumerate(products):
            if not isinstance(item, dict):
                continue
            line = PL.lineno(products, i)
            role = item.get("role")
            if role is not None and role not in ("required", "optional"):
                self.fail("oracle_products:%s" % role, PL.lineno(item, "role", line), "SPEC016",
                          "oracle_products[%d].role is `%s` — required (built on it or fully "
                          "relies on it) or optional (a possible source or destination)"
                          % (i, role))
            pid = item.get("id")
            if catalog is None or not PL.is_filled(pid):
                continue
            if str(pid) not in catalog["ids"]:
                self.fail("oracle_products:%s" % (role or "required"),
                          PL.lineno(item, "id", line), "SPEC004",
                          "oracle_products[%d].id `%s` is not in the catalog — add it to "
                          "shared/data/oracle-products.yaml as a catalog change, never as "
                          "free text here" % (i, pid))
                continue
            vendor = catalog_vendor(catalog, str(pid))
            if vendor and vendor.lower() != "oracle":
                self.fail("oracle_products:%s" % (role or "required"),
                          PL.lineno(item, "id", line), "SPEC018",
                          "oracle_products[%d].id `%s` is a %s product — this list is Oracle "
                          "only; carry it in architecture.stack[].catalog_id, where the pack's "
                          "engine layer belongs" % (i, pid, vendor))

    def check_stack_catalog_ids(self, catalog):
        """architecture.stack[].catalog_id resolves to the same catalog."""
        if catalog is None:
            return
        stack = PL.dig(self.spec, "architecture", "stack")
        if not isinstance(stack, list):
            return
        for i, layer in enumerate(stack):
            if not isinstance(layer, dict):
                continue
            line = PL.lineno(stack, i)
            ids = layer.get("catalog_id")
            if ids is None:
                continue
            values = ids if isinstance(ids, list) else [ids]
            for pid in values:
                if not PL.is_filled(pid):
                    continue
                if str(pid) not in catalog["ids"]:
                    self.fail("architecture", PL.lineno(layer, "catalog_id", line), "SPEC004",
                              "architecture.stack[%d].catalog_id `%s` is not in the catalog — "
                              "every vendor component of the stack is named by a catalog id, "
                              "Oracle and NVIDIA alike" % (i, pid))

    def check_roadmap(self, roadmap_ids):
        if roadmap_ids is None:
            return
        meta = self.spec.get("meta")
        item_id = PL.dig(self.spec, "meta", "roadmap_item_id")
        if not PL.is_filled(item_id):
            return
        if str(item_id) not in roadmap_ids:
            self.fail("meta", PL.lineno(meta, "roadmap_item_id"), "SPEC005",
                      "meta.roadmap_item_id `%s` is not in the roadmap extract — use the "
                      "stable id from shared/data/roadmap-items.csv, never a row number"
                      % item_id)

    def check_packages(self):
        packages = self.spec.get("packages")
        if not isinstance(packages, dict):
            return
        tiers = packages.get("tiers")
        if not isinstance(tiers, list) or not tiers:
            return
        seen = []
        for i, tier in enumerate(tiers):
            if not isinstance(tier, dict):
                continue
            line = PL.lineno(tiers, i)
            tid = str(tier.get("id") or "").strip()
            name = tier.get("name")
            seen.append(tid)
            if tid not in PL.TIER_IDS:
                self.fail("packages", PL.lineno(tier, "id", line), "SPEC009",
                          "packages.tiers[%d].id `%s` is not one of %s"
                          % (i, tid or "(none)", " / ".join(PL.TIER_IDS)))
            else:
                want = PL.TIER_NAMES[tid]
                if name != want:
                    self.fail("packages", PL.lineno(tier, "name", line), "SPEC009",
                              "packages.tiers[%d].name is `%s` — one tier vocabulary "
                              "everywhere: `%s` (S/M/L survive only as size tags in internal "
                              "tables)" % (i, name, want))
            if not PL.is_filled(tier.get("services_price")):
                self.fail("packages", PL.lineno(tier, "services_price", line), "SPEC002",
                          "packages.tiers[%d].services_price is missing — a tier states a "
                          "price or says `status: tbd`" % i)
        missing = [t for t in PL.TIER_IDS if t not in seen]
        if missing:
            self.fail("packages", PL.lineno(packages, "tiers"), "SPEC009",
                      "packages.tiers is missing %s — every pack carries the same three tiers"
                      % ", ".join("`%s`" % PL.TIER_NAMES[m] for m in missing))
        elif seen[:3] != list(PL.TIER_IDS):
            self.soft("packages", PL.lineno(packages, "tiers"), "SPEC009",
                      "packages.tiers is ordered %s — artifacts render PoV Jumpstart, "
                      "Integration, Scaling in that order" % " / ".join(seen))
        self.check_pov_duration(tiers)

    def check_pov_duration(self, tiers):
        pov = None
        for i, tier in enumerate(tiers):
            if isinstance(tier, dict) and str(tier.get("id") or "").strip() == "pov":
                pov, idx = tier, i
                break
        if pov is None:
            return
        line = PL.lineno(tiers, idx)
        weeks = pov.get("duration_weeks")
        if not isinstance(weeks, dict):
            self.fail("packages", PL.lineno(pov, "duration_weeks", line), "SPEC002",
                      "packages.tiers[pov].duration_weeks is missing — a PoV states its "
                      "length; 4-8 weeks, 10 the hard cap")
            return
        top = weeks.get("max")
        if top is None:
            self.fail("packages", PL.lineno(weeks), "SPEC002",
                      "packages.tiers[pov].duration_weeks.max is missing")
            return
        try:
            top = float(top)
        except (TypeError, ValueError):
            self.fail("packages", PL.lineno(weeks, "max"), "SPEC002",
                      "packages.tiers[pov].duration_weeks.max `%s` is not a number" % top)
            return
        justification = (weeks.get("justification") or pov.get("justification")
                         or pov.get("duration_justification"))
        if top > 10:
            self.fail("packages", PL.lineno(weeks, "max"), "SPEC007",
                      "PoV runs up to %g weeks — 10 weeks is the hard cap; a longer proof of "
                      "value stops being a proof of value" % top)
        elif top > 8 and not PL.is_filled(justification):
            self.fail("packages", PL.lineno(weeks, "max"), "SPEC006",
                      "PoV runs up to %g weeks with no `justification` — the target band is "
                      "4-8 weeks; state why this one is longer or cut the scope" % top)

    def check_workflow_steps(self):
        workflow = self.spec.get("workflow")
        if not isinstance(workflow, dict):
            return
        steps = workflow.get("steps")
        if not isinstance(steps, list):
            return
        n = len(steps)
        line = PL.lineno(workflow, "steps")
        if n > 7:
            self.fail("workflow", line, "SPEC019",
                      "workflow has %d steps — the pack's workflow is 5-7 steps grouped at the "
                      "buyer's checkpoints (where a human decides, an output appears or data "
                      "changes hands); mechanics such as normalization, dedup, entity resolution "
                      "or routing belong inside a step's description, not as steps" % n)
        elif 0 < n < 3:
            self.soft("workflow", line, "SPEC020",
                      "workflow has %d step(s) — fewer than 3 hides the work; the target is "
                      "5-7 steps" % n)

    def check_record_keys(self):
        """SPEC024 (warning) — every record in a list the layout knows carries only the keys
        the layout defines for it, and every capability feature has a status.

        The lists and their keys are the spec layout's own (packspec.RECORD_LISTS): workflow
        and architecture inputs, outputs and steps, the stack, industries, capability areas,
        categories and features, Oracle products, metrics, tiers, capability handling, open
        questions, provenance inputs, and the label/text lists. A warning, not a finding: the
        damage is often in a record's provenance rather than in what the artifacts print, and
        a stale key must not stop a build. It is still said out loud, because the same slip
        can truncate a value and nothing else notices — an unquoted `{ … }` mapping in YAML
        splits a value at its commas into bogus keys (`data: work orders, technicians, zones`
        reads as data "work orders" plus two empty keys), which the Markdown spec then shows as
        extra columns or under Other fields.
        """
        for pattern, keys in sorted(PL.record_lists().items()):
            for path, items, n, item in PL.iter_records(self.spec, pattern):
                if not isinstance(item, dict):
                    continue
                extra = [k for k in item if k not in keys]
                if extra:
                    self.rep.warn(self.path, PL.lineno(item, extra[0], PL.lineno(items, n)),
                                  "SPEC024",
                                  "%s carries key(s) the spec layout does not define: %s — "
                                  "usually a value YAML split at its commas (an unquoted "
                                  "`{ … }` mapping); set the whole text back on its key "
                                  "(`packspec.py set`), or move it to a key the layout knows "
                                  "(`note`)"
                                  % (PL.format_path(path), ", ".join("`%s`" % k for k in extra)))
        for path, items, n, feat in PL.iter_records(self.spec, "capabilities[].categories[].features"):
            if isinstance(feat, dict) and not feat.get("status"):
                self.rep.warn(self.path, PL.lineno(items, n), "SPEC024",
                              "capability %r has no status — the feature list will not build "
                              "until it does" % (feat.get("name") or "(unnamed)"))

    def check_product_counts(self):
        products = self.spec.get("oracle_products")
        if not isinstance(products, list):
            return
        roles = collections.Counter(str(p.get("role") or "required")
                                    for p in products if isinstance(p, dict))
        line = PL.lineno(self.spec, "oracle_products")
        if roles["required"] > 3:
            self.rep.warn(self.path, line, "SPEC021",
                          "%d required Oracle products — required is only what the pack cannot "
                          "run without: the platform as one entry (OCI, its `why` naming the "
                          "services it uses) plus the one or two products the core executes on; "
                          "systems the pack reads from or writes to are optional"
                          % roles["required"])
        if roles["optional"] > 4:
            self.rep.warn(self.path, line, "SPEC022",
                          "%d optional Oracle products — optional holds only what a typical "
                          "buyer would plausibly connect as a source or destination, each with a "
                          "concrete `why`; a catalog sweep is cut" % roles["optional"])

    def check_capability_size(self):
        """SPEC023 — the capability tree is sized for a feature list that fits one A4 page."""
        caps = self.spec.get("capabilities")
        if not isinstance(caps, list) or not caps:
            return
        areas = categories = features = 0
        for area in caps:
            if not isinstance(area, dict):
                continue
            areas += 1
            for cat in area.get("categories") or []:
                if not isinstance(cat, dict):
                    continue
                categories += 1
                features += len(cat.get("features") or [])
        over = []
        if areas > 6:
            over.append("%d areas (6 is the ceiling)" % areas)
        if categories > 14:
            over.append("%d categories (about 12)" % categories)
        if features > 40:
            over.append("%d features (about 30-35)" % features)
        if over:
            self.rep.warn(self.path, PL.lineno(self.spec, "capabilities"), "SPEC023",
                          "the capability tree carries %s — the feature list is one A4 page, and "
                          "a tree this fine will not fit it even with one row per category. Group "
                          "at sign-off, not at build time: merge sibling features into one, fold "
                          "a small category into its neighbour, shorten names"
                          % ", ".join(over))

    def check_kpis(self):
        kpis = self.spec.get("kpis")
        if not isinstance(kpis, list):
            return
        by_name = collections.defaultdict(list)
        for i, kpi in enumerate(kpis):
            if not isinstance(kpi, dict):
                continue
            line = PL.lineno(kpis, i)
            name = PL.norm_loose(str(kpi.get("name") or ""))
            figure = kpi.get("figure")
            if has_value(figure):
                status = kpi.get("figure_status")
                if not has_value(status):
                    self.fail("kpis", PL.lineno(kpi, "figure", line), "SPEC011",
                              "kpis[%d].figure `%s` carries no figure_status — one plain word: "
                              "%s" % (i, figure, " | ".join(FIGURE_STATUSES)))
                elif str(status) not in FIGURE_STATUSES:
                    self.fail("kpis", PL.lineno(kpi, "figure_status", line), "SPEC011",
                              "kpis[%d].figure_status `%s` is not one of %s"
                              % (i, status, " | ".join(FIGURE_STATUSES)))
                if not has_value(kpi.get("caveat")):
                    self.fail("kpis", PL.lineno(kpi, "figure", line), "SPEC012",
                              "kpis[%d].figure `%s` carries no caveat — a figure never travels "
                              "without one (illustrative, not contractual)" % (i, figure))
                if not PL.is_filled(kpi.get("attribution")):
                    self.fail("kpis", PL.lineno(kpi, "figure", line), "SPEC002",
                              "kpis[%d].attribution is missing — a figure states who it belongs "
                              "to, named where the channel allows and anonymized otherwise" % i)
            elif has_value(kpi.get("figure_status")):
                self.fail("kpis", PL.lineno(kpi, "figure_status", line), "SPEC011",
                          "kpis[%d].figure_status is `%s` but the figure is `-` — a metric with "
                          "no cleared figure carries no status either"
                          % (i, kpi.get("figure_status")))
            if name:
                by_name[name].append((i, line, PL.norm_loose(str(figure or ""))))
        for name, rows in by_name.items():
            figures = {r[2] for r in rows}
            if len(rows) > 1 and len(figures) > 1:
                line = rows[-1][1]
                self.fail("kpis", line, "SPEC008",
                          "`%s` appears %d times with different figures (%s) — one metric set "
                          "per pack; if a second set exists, one of them is wrong and the spec "
                          "decides which"
                          % (name, len(rows), ", ".join(sorted(f or "(empty)" for f in figures))))
        figures_block = self.spec.get("figures")
        if isinstance(figures_block, list):
            for i, row in enumerate(figures_block):
                if not isinstance(row, dict):
                    continue
                name = PL.norm_loose(str(row.get("name") or ""))
                value = PL.norm_loose(str(row.get("figure") or ""))
                if name in by_name and value and value not in {r[2] for r in by_name[name]}:
                    self.fail("kpis", PL.lineno(figures_block, i), "SPEC008",
                              "figures[%d] `%s` = %s contradicts kpis — one metric set per pack"
                              % (i, name, value))

    def check_kpi_kinds(self):
        """SPEC025-027 — the business-metric rule (warnings).

        Warnings, not findings: the call on what the business is willing to improve is
        the owner's, and a brief that has not had that conversation yet must still be
        able to build. What the checks do is make the conversation unavoidable.
        """
        kpis = self.spec.get("kpis")
        if not isinstance(kpis, list) or not kpis:
            return
        kinds, business_like = [], []
        for i, kpi in enumerate(kpis):
            if not isinstance(kpi, dict):
                continue
            line = PL.lineno(kpis, i)
            name = str(kpi.get("name") or "").strip()
            raw = kpi.get("kind")
            kind = str(raw).strip().lower() if PL.is_filled(raw) else DEFAULT_KPI_KIND
            if kind not in KPI_KINDS:
                self.rep.warn(self.path, PL.lineno(kpi, "kind", line), "SPEC025",
                              "kpis[%d].kind is `%s` — one of %s (absent means `%s`)"
                              % (i, raw, " | ".join(KPI_KINDS), DEFAULT_KPI_KIND))
                kind = DEFAULT_KPI_KIND
            kinds.append(kind)
            if kind == "business" and not TECHNICAL_NAME_RE.search(name):
                business_like.append(name)
            if kind != "technical" and TECHNICAL_NAME_RE.search(name):
                self.rep.warn(self.path, PL.lineno(kpi, "name", line), "SPEC026",
                              "kpis[%d] `%s` reads as a proof-of-value acceptance criterion, "
                              "not as a business metric — mark it `kind: technical` (it then "
                              "rides the PoV package's \"Proof accepted when …\" line and never "
                              "a sales tile), or name the business outcome it serves instead: "
                              "money, time, volume, risk or quality in the buyer's words"
                              % (i, name or "(unnamed)"))
            if kind == "business" and not PL.is_filled(kpi.get("owner_role")):
                self.rep.warn(self.path, PL.lineno(kpi, "name", line), "SPEC027",
                              "kpis[%d] `%s` has no owner_role — name the buyer-side role who "
                              "would sign this number off (\"Head of claims\", \"COO\"); a "
                              "metric nobody on their side owns is not a business metric"
                              % (i, name or "(unnamed)"))
        # "No business metric" covers both shapes: every metric marked `technical`, and
        # every metric unmarked but reading as a proof criterion. The second is the one
        # that shipped (the DHL one-pager, 2026-09-23) — nothing was marked at all.
        if kinds and not business_like:
            self.rep.warn(self.path, PL.lineno(self.spec, "kpis"), "SPEC025",
                          "no business metric in the set (%d metric(s), kinds: %s) — every one "
                          "is a technical criterion or reads as one. Sales artifacts print "
                          "business metrics only, so the deck's stat tiles, the one-pager's "
                          "proof strip and the site's metrics would have nothing to show. "
                          "Derive the business outcomes these criteria serve — money, time, "
                          "volume, risk or quality in the buyer's words — and put that set to "
                          "the owner" % (len(kinds), ", ".join(sorted(set(kinds)))))

    def check_retired_header(self):
        """SPEC028 — the retired family name in a header the artifacts print."""
        for key, sub in HEADER_KEYS:
            node = self.spec.get(key)
            if not isinstance(node, dict):
                continue
            value = node.get(sub)
            if not PL.is_filled(value):
                continue
            m = RETIRED_HEADER_RE.search(str(value))
            if not m:
                continue
            self.fail(key if key != "meta" else "meta", PL.lineno(node, sub), "SPEC028",
                      "%s.%s is `%s` — `%s` is retired; the family name on every print artifact "
                      "is \"%s\" (the mini-site lockup)"
                      % (key, sub, value, m.group(0), HEADER_BRAND))

    def check_customer_names(self, deny):
        spec = self.spec
        targets = []
        meta = spec.get("meta")
        if isinstance(meta, dict):
            for key in ("name", "name_variants"):
                if key in meta:
                    targets.append(("meta.%s" % key, meta[key], PL.lineno(meta, key)))
        for key in DENY_SCAN:
            if key in spec:
                targets.append((key, spec[key], PL.lineno(spec, key)))
        kpis = spec.get("kpis")
        if isinstance(kpis, list):
            for i, kpi in enumerate(kpis):
                otherwise = PL.dig(kpi, "attribution", "otherwise")
                if isinstance(otherwise, str):
                    targets.append(("kpis[%d].attribution.otherwise" % i, otherwise,
                                    PL.lineno(PL.dig(kpi, "attribution") or kpi, "otherwise",
                                              PL.lineno(kpis, i))))
        for label, node, base in targets:
            for text, line in walk_strings(node, base):
                for entry in deny:
                    if entry.regex.search(text):
                        component = label.split("[")[0].split(".")[0]
                        self.fail(component, line, "SPEC010",
                                  "%s names `%s`, which is on the deny-list — customer-facing "
                                  "copy uses clearance.anonymized_descriptor instead"
                                  % (label, entry.term))
                        break

    def check_name_variants(self):
        meta = self.spec.get("meta")
        if not isinstance(meta, dict):
            return
        name = meta.get("name")
        variants = meta.get("name_variants")
        if not PL.is_filled(name) or not isinstance(variants, dict):
            return
        name = str(name).strip()
        want = {
            "site": name,
            "internal_slide": "%s App" % name,
            "external": name[:1].upper() + name[1:].lower() if name else name,
        }
        for key, expected in want.items():
            got = variants.get(key)
            if not PL.is_filled(got):
                continue
            if str(got).strip() != expected:
                self.soft("meta", PL.lineno(variants, key), "SPEC017",
                          "meta.name_variants.%s is `%s`; the channel rule derives `%s` from "
                          "meta.name (naming-and-clearance.md §2)" % (key, got, expected))

    # -- completeness table -------------------------------------------------
    def table(self):
        rows = []
        for num, label, key in COMPONENT_ROWS:
            state, detail = self.state_of(key)
            rows.append((num, label, key.split(":")[0], state, detail))
        width = max(len(r[1]) for r in rows) + 2
        out = ["", "component completeness"]
        out.append("  %-3s %-*s %-26s %-9s %s" % ("#", width, "component", "spec key",
                                                  "state", "note"))
        for num, label, key, state, detail in rows:
            out.append("  %-3s %-*s %-26s %-9s %s" % (num, width, label, key, state, detail))
        done = sum(1 for r in rows if r[3] == "complete")
        out.append("")
        return "\n".join(out), done, len(rows)

    def state_of(self, key):
        base = key.split(":")[0].split(".")[0]
        node = self.spec.get(base)
        findings = self.per_component.get(key, 0)
        if key == "meta.name":
            present = PL.is_filled(PL.dig(self.spec, "meta", "name"))
        elif ":" in key:
            role = key.split(":")[1]
            present = isinstance(node, list) and any(
                isinstance(p, dict) and p.get("role") == role for p in node)
            if not present and role == "optional":
                return "-", "no optional product (legitimate)"
        elif key == "open_questions":
            present = "open_questions" in self.spec
        else:
            present = PL.is_filled(node)
        if not present:
            return "missing", "not in the spec"
        detail = ""
        if key in FIRST_ORDER:
            detail = str(PL.dig(self.spec, *FIRST_ORDER[key]) or "")
        elif ":" in key:
            role = key.split(":")[1]
            detail = "%d %s" % (sum(1 for p in node
                                    if isinstance(p, dict) and p.get("role") == role), role)
        elif isinstance(node, list):
            detail = "%d item(s)" % len(node)
        if findings:
            return "partial", "%d finding(s)" % findings
        return "complete", detail


def catalog_vendor(catalog, pid):
    """The catalog `vendor` of one id, or "" when the entry does not name one."""
    for entry in catalog["entries"]:
        if entry["id"] == pid:
            return entry.get("vendor") or ""
    return ""


def walk_strings(node, base_line):
    """(text, line) for every string in a subtree, keyed to the line it sits on."""
    if isinstance(node, str):
        yield node, base_line
    elif isinstance(node, dict):
        for key, value in node.items():
            yield from walk_strings(value, PL.lineno(node, key, base_line))
    elif isinstance(node, list):
        for i, item in enumerate(node):
            yield from walk_strings(item, PL.lineno(node, i, base_line))


def main() -> int:
    ap = argparse.ArgumentParser(prog=PROG, description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", help="path to packs/<slug>/pack-spec.md")
    ap.add_argument("--catalog", default=PL.DEFAULT_CATALOG,
                    help="Oracle product catalog (default: shared/data/oracle-products.yaml)")
    ap.add_argument("--roadmap", default=PL.DEFAULT_ROADMAP,
                    help="roadmap extract (default: shared/data/roadmap-items.csv)")
    ap.add_argument("--denylist", "--deny-list", dest="denylist", default=PL.DEFAULT_DENYLIST,
                    help="deny-list file (default: shared/tools/denylist.txt)")
    ap.add_argument("--strict", action="store_true",
                    help="promote SPEC900/901/902/017 to findings — the completeness "
                         "check, usable at any meta.status")
    ap.add_argument("--signoff", action="store_true",
                    help="also require the four first-order `user:<date>` sources whatever "
                         "meta.status says (it is required anyway once the spec is confirmed)")
    args = ap.parse_args()

    spec_path = args.spec
    if not os.path.isfile(spec_path):
        PL.die_usage(PROG, "no such spec file: %s" % spec_path)
    rep = PL.Report(PROG)
    try:
        spec = PL.load_spec(spec_path, PROG)
    except PL.spec_error_type() as exc:
        # A structural slip is a finding on its own line; nothing else can be checked.
        rep.fail(spec_path, exc.line or 1, "SPEC029", "the spec does not parse: %s" % exc.message)
        return rep.render("0 of %d components checked" % len(COMPONENT_ROWS))
    if not isinstance(spec, dict):
        PL.die_usage(PROG, "%s is not a mapping — expected the pack-spec shape" % spec_path)

    lint = SpecLint(spec_path, spec, rep, args.strict, args.signoff)

    catalog = None
    if os.path.isfile(args.catalog):
        catalog = PL.load_catalog(args.catalog, PROG)
    else:
        lint.soft("oracle_products:required", PL.lineno(spec), "SPEC900",
                  "catalog not found at %s — product ids not checked" % args.catalog)
        rep.cannot_check("oracle_products[].id and architecture.stack[].catalog_id against the "
                         "catalog (%s)" % args.catalog)

    roadmap_ids = None
    if os.path.isfile(args.roadmap):
        roadmap_ids = PL.load_roadmap_ids(args.roadmap, PROG)
    else:
        lint.soft("meta", PL.lineno(spec), "SPEC901",
                  "roadmap extract not found at %s — meta.roadmap_item_id not checked"
                  % args.roadmap)
        rep.cannot_check("meta.roadmap_item_id against the roadmap extract (%s)" % args.roadmap)

    deny = PL.load_denylist(args.denylist, PROG)

    lint.check_present()
    lint.check_required_keys()
    lint.check_status_and_sources()
    lint.check_clearance()
    lint.check_build()
    lint.check_products(catalog)
    lint.check_stack_catalog_ids(catalog)
    lint.check_roadmap(roadmap_ids)
    lint.check_packages()
    lint.check_kpis()
    lint.check_kpi_kinds()
    lint.check_retired_header()
    lint.check_workflow_steps()
    lint.check_record_keys()
    lint.check_product_counts()
    lint.check_capability_size()
    lint.check_customer_names(deny)
    lint.check_name_variants()

    table, done, total = lint.table()
    return rep.render("%d of %d components complete" % (done, total), tail=table)


if __name__ == "__main__":
    raise SystemExit(main())
