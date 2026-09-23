#!/usr/bin/env python3
"""Build the one-slide executive summary for an accelerator pack.

    build_exec_summary.py <pack-spec.yaml> --out <dir>
                          [--host-deck <pptx>] [--with-closing]
                          [--fit-report] [--allow-overflow]

Six blocks on the section-slides grid: one-liner, problem -> solution,
solution-layers ladder, proof strip with caveat, tiers strip, planned next
steps — and speaker notes that say which cut the slide is. With --host-deck the
slide is built on that deck's own master, so it pastes into the host unchanged;
without it, on the shipped SoftServe base.

Dependencies: pyyaml, python-pptx, Pillow  (see plugins/oracle-packs/requirements.txt)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
for _cand in (_HERE, _HERE.parents[1] / "deck" / "tools"):
    if (_cand / "deckkit.py").exists():
        sys.path.insert(0, str(_cand))
        break

from pptx import Presentation                                 # noqa: E402

from deckkit import (                                         # noqa: E402
    C, FitLog, TITLE_BOX, copy_slide_number, Spec, SpecError, autofit_paras, autofit_pt, fmt_duration,
    fmt_price, log_box, new_slide, open_base, panel, pick_layout, rect,
    stacked_height, strip_slides, textbox,
)

BASE_DEFAULT = (_HERE.parents[1] / "deck" / "assets" / "softserve-deck-base.pptx")

# The family name on every print artifact, as the mini-site's lockup carries it.
# "OCI AI Accelerators" is retired (2026-09-23): a brief that still holds it is
# rewritten here rather than printed, and the run says so.
HEADER_BRAND = "Oracle AI & Data Solutions"
RETIRED_HEADER = re.compile(r"OCI\s+AI\s+Accelerators?|OCI\s+accelerators?", re.IGNORECASE)

# The section-slides grid, measured from the Sep-11 deck and the Jul-17
# executive summary (inches).
COL = [(0.42, 4.62), (5.22, 3.78), (9.18, 3.75)]
LABEL_Y_TOP, PANEL_Y_TOP, PANEL_H_TOP = 2.12, 2.41, 1.86
LABEL_Y_BOT, PANEL_Y_BOT, PANEL_H_BOT = 4.43, 4.72, 1.92
SUBTITLE_Y, FOOTNOTE_Y = 1.70, 6.80

VENDOR_TINTS = [
    ("softserve", (C["orange_tint"], C["orange"])),
    ("oracle + softserve", ("D2E7F6", C["blue"])),
    ("softserve + oracle", ("D2E7F6", C["blue"])),
    ("nvidia", (C["blue_tint"], C["blue_light"])),
    ("oracle", ("EEF1F3", "6B7680")),
]

# The ladder starts at the application layer, as the sales deck's does
# (deck/tools/build_deck_v2.py, `layers`): a layer the spec places above it — the
# client's own configuration — is the deck's "Tailored solution" card, never a rung.
# Same words and the same fallback as the deck, so the two ladders cannot disagree.
APP_LAYER_WORDS = ("app", "business", "by softserve")

# The in-panel label (the VERTICALS label): a name that stands where a figure would,
# so that nobody reads it as a number (2026-09-23).
LABEL = {"sz": 8, "b": True, "color": C["blue"]}
# The anatomy's idiom for absence: one grey line, label-sized, saying what is missing.
ABSENT = {"sz": 8, "color": C["muted_light"], "align": "r"}

FIGURELESS_CAVEAT = "To be measured in the proof of value; results to follow."

# Who may be named where, in the words the notes use.
CHANNEL_WORDS = (("internal", "the internal cut"), ("partner_print", "partner print"),
                 ("customer_site", "the customer site"), ("demo", "the demo"))


def tints(vendor: str, i: int):
    v = (vendor or "").strip().lower()
    for key, cols in VENDOR_TINTS:
        if key == v:
            return cols
    for key, cols in VENDOR_TINTS:
        if key in v:
            return cols
    return [(C["blue_tint"], C["blue"]), ("EEF1F3", "6B7680")][i % 2]


def sec_label(slide, col, y, text, color=C["blue"], right=None):
    x, w = col
    textbox(slide, x, y, w, 0.24, [{"t": text, "sz": 10.5, "b": True, "color": color}])
    if right:
        textbox(slide, x, y, w, 0.24,
                [{"t": right, "sz": 7.5, "color": C["muted"], "align": "r"}])


# ---------------------------------------------------------------------------
# blocks
# ---------------------------------------------------------------------------

def block_use_case(s, spec: Spec, fit: FitLog):
    col = COL[0]
    x, w = col
    sec_label(s, col, LABEL_Y_TOP, "USE CASE")
    panel(s, x, PANEL_Y_TOP, w, PANEL_H_TOP, fill=C["blue_tint"], accent=C["blue"],
          line=C["hairline"])
    ps = spec.get("problem_solution", {}) or {}
    verticals = [str(v.get("name", "")) for v in (spec.get("verticals") or [])]
    paras = [
        {"t": [("PROBLEM:  ", {"b": True}), (str(ps.get("problem", "")), {})],
         "sz": 9.5, "color": C["ink"], "space_after": 5},
        {"t": [("SOLUTION:  ", {"b": True}), (str(ps.get("solution", "")), {})],
         "sz": 9.5, "color": C["ink"], "space_after": 5},
    ]
    if verticals:
        paras += [
            {"t": "VERTICALS", "sz": 8, "b": True, "color": C["blue"], "space_after": 1},
            {"t": " · ".join(verticals), "sz": 8.5, "color": C["muted"]},
        ]
    bx, bw, bh = x + 0.20, w - 0.40, PANEL_H_TOP - 0.24
    paras = autofit_paras(paras, bw, bh, min_scale=0.70, default_sz=9.5)
    textbox(s, bx, PANEL_Y_TOP + 0.12, bw, bh, paras)
    log_box(fit, 1, "use case", bx, PANEL_Y_TOP + 0.12, bw, bh, paras, 9.5)


def ladder(stack: list) -> tuple[list, list]:
    """(rungs, above): the stack from the application layer down, and what sits above it."""
    names = [re.sub(r"\s+", " ", str((l or {}).get("layer") or "")).strip().lower()
             for l in stack]
    app = next((i for i, n in enumerate(names) if any(w in n for w in APP_LAYER_WORDS)), 0)
    return stack[app:], stack[:app]


def block_layers(s, spec: Spec, fit: FitLog):
    col = COL[1]
    x, w = col
    sec_label(s, col, LABEL_Y_TOP, "SOLUTION LAYERS", right="▲ business value")
    stack = spec.get("architecture.stack") or []
    if not stack:
        raise SpecError("pack spec has no `architecture.stack` — the "
                        "high-level architecture component is not signed off")
    stack, above = ladder(stack)
    for layer in above:
        fit.note(f"solution layers: `{layer.get('layer')}` sits above the application layer — "
                 f"not a rung, as on the deck's ladder")
    n = len(stack)
    gap = 0.06
    rh = (PANEL_H_TOP - gap * (n - 1)) / n
    for i, layer in enumerate(stack):
        y = PANEL_Y_TOP + i * (rh + gap)
        tint, bar = tints(str(layer.get("vendor", "")), i)
        panel(s, x, y, w, rh, fill=tint, accent=bar, line=C["hairline"])
        name = str(layer.get("layer", ""))
        pt = autofit_pt(name, w - 1.10, rh, 10, 7.5, bold=True, max_lines=2)
        textbox(s, x + 0.20, y, w - 1.10, rh,
                [{"t": name, "sz": pt, "b": True, "color": C["ink"]}], anchor="m")
        fit.add(1, f"layer {i+1}", name, pt, w - 1.10, rh, bold=True, max_lines=2)
        vend = str(layer.get("vendor", ""))
        textbox(s, x + 0.20, y, w - 0.34, rh,
                [{"t": vend, "sz": 7.5, "color": C["muted"], "align": "r"}], anchor="m")
        fit.add(1, f"layer {i+1} vendor", vend, 7.5, 1.00, rh, max_lines=1)


def block_proof(s, spec: Spec, fit: FitLog):
    col = COL[2]
    x, w = col
    # Business metrics only (`kind != technical`): the strip is what the slide claims
    # about the buyer's business, and a proof criterion reads as such a claim here.
    kpis = spec.figured_kpis()
    sales = spec.sales_kpis()
    blocked = [k for k in sales
               if k.get("channels") and spec.channel not in k["channels"]]
    if spec.technical_kpis():
        print("build_exec_summary: %d technical criterion(s) are kept off the proof strip — "
              "they print on the PoV tier as the \"Proof accepted when …\" line."
              % len(spec.technical_kpis()), file=sys.stderr)
    customer = str(spec.get("meta.source_engagement.customer") or "").strip()
    named = spec.customer_name_allowed() and bool(customer)
    label = f"PROOF OF VALUE · {customer}" if named else "PROOF OF VALUE"
    sec_label(s, col, LABEL_Y_TOP, label.upper(), color=C["orange"])
    panel(s, x, PANEL_Y_TOP, w, PANEL_H_TOP, fill=C["panel_grey"],
          accent=C["orange"], line=C["hairline"])
    if blocked or not sales:
        # Peer claims are all-or-none (slide-design rule 11): show the empty
        # instance of the container, never a partly-filled proof block. This is
        # the CLEARANCE state only — a metric set with no figure yet is a
        # different thing and is drawn below (2026-09-23).
        textbox(s, x + 0.20, PANEL_Y_TOP, w - 0.40, PANEL_H_TOP,
                [{"t": "Metric set not cleared for this channel.", "sz": 9,
                  "color": C["muted_light"], "align": "c"}], anchor="m")
        fit.note("proof block left empty — the metric set is not cleared here")
        return
    # The header already names a cleared customer; a line under it saying "proof of
    # value at <Customer>" is the same attribution twice (the DHL slide, 2026-09-23).
    # Only a header that cannot name the customer keeps the attribution line.
    top = PANEL_Y_TOP + 0.12
    if not named:
        attribution = spec.kpi_attribution()
        textbox(s, x + 0.20, PANEL_Y_TOP + 0.10, w - 0.40, 0.24,
                [{"t": attribution, "sz": 8, "color": C["muted"]}])
        fit.add(1, "proof attribution", attribution, 8, w - 0.40, 0.24, max_lines=1)
        top = PANEL_Y_TOP + 0.40
    # No cleared figure yet: each tile names its metric where the figure will stand,
    # as the deck and the one-pager do — in the label style, never in figure type where
    # a reader looks for a number — and one line underneath says the figures are coming.
    rows = (kpis or sales)[:3]
    caveat_h = 0.0 if kpis else 0.20
    rh = (PANEL_Y_TOP + PANEL_H_TOP - 0.04 - caveat_h - top) / max(1, len(rows))
    for i, k in enumerate(rows):
        y = top + i * rh
        caption = str(k.get("label") or k.get("name") or "").strip()
        if spec.has_figure(k):
            fig = str(k.get("figure", ""))
            base = k.get("baseline")
            shown = f"{base} → {fig}" if base and k.get("show_baseline") else fig
            fpt = autofit_pt(shown, w - 0.40, 0.24, 12.5, 9, bold=True, max_lines=1)
            head = {"t": shown, "sz": fpt, "b": True, "color": C["blue"]}
        else:   # the metric's name stands where its figure will
            shown = str(k.get("chip") or k.get("name") or "").strip().rstrip("↑↓→ ")
            fpt = LABEL["sz"]
            head = {"t": shown, **LABEL, "space_after": 1}
        paras = [head]
        if caption and caption.lower() != shown.lower():
            paras.append({"t": caption, "sz": 7.5, "color": C["muted"]})
        paras = autofit_paras(paras, w - 0.40, rh - 0.04, min_scale=0.75, default_sz=fpt)
        textbox(s, x + 0.20, y, w - 0.40, rh - 0.04, paras)
        log_box(fit, 1, f"proof stat {i+1}", x + 0.20, y, w - 0.40, rh - 0.04, paras, fpt)
    if caveat_h:
        textbox(s, x + 0.20, PANEL_Y_TOP + PANEL_H_TOP - caveat_h, w - 0.40, caveat_h,
                [{"t": FIGURELESS_CAVEAT, "sz": 7, "color": C["muted_light"]}])
        fit.add(1, "proof caveat", FIGURELESS_CAVEAT, 7, w - 0.40, caveat_h, max_lines=1)
        fit.note("proof strip names the metrics being measured — no cleared figure yet")


def absent_line(s, fit: FitLog, x, y, w, text: str, label: str) -> None:
    """One grey label-sized line saying what is missing — never the value's own type."""
    textbox(s, x, y, w, 0.18, [{"t": text, **ABSENT}])
    fit.add(1, label, text, ABSENT["sz"], w, 0.18, max_lines=1)


def block_packages(s, spec: Spec, fit: FitLog) -> tuple[bool, bool]:
    """Draw the tier rows; returns (an indicative price needs the footnote, a price is shown)."""
    col = COL[0]
    x, w = col
    sec_label(s, col, LABEL_Y_BOT, "SERVICE PACKAGES")
    tiers = spec.tiers()
    n = max(1, len(tiers))
    gap = 0.09
    rh = (PANEL_H_BOT - gap * (n - 1)) / n
    price_w, text_w = 1.55, w - 1.55 - 0.40
    star = shown = False
    for i, t in enumerate(tiers):
        y = PANEL_Y_BOT + i * (rh + gap)
        shade = [C["blue"], C["blue_light"], C["hairline_alt"]][min(i, 2)]
        panel(s, x, y, w, rh, fill=C["blue_tint"], accent=shade, line=C["hairline"])
        label = spec.tier_label(t)
        textbox(s, x + 0.20, y + 0.07, text_w, 0.20,
                [{"t": label, "sz": 10, "b": True, "color": C["ink"]}])
        fit.add(1, f"tier {i+1} name", label, 10, text_w, 0.20, bold=True, max_lines=1)
        scope = str(t.get("scope_line") or "")
        # The technical criteria ride the PoV tier's own scope — the one place on this
        # slide where "when is the proof done?" is the reader's question.
        success = spec.pov_success_line()
        if success and str(t.get("id") or "").strip() == "pov":
            scope = (scope.rstrip(". ") + ". " + success).strip() if scope else success
        sh = rh - 0.28
        spt = autofit_pt(scope, text_w, sh, 8, 6, max_lines=3)
        textbox(s, x + 0.20, y + 0.26, text_w, sh,
                [{"t": scope, "sz": spt, "color": C["muted"]}])
        fit.add(1, f"tier {i+1} scope", scope, spt, text_w, sh, max_lines=3)
        # The price and the duration where the brief states them. A missing one is one
        # grey line naming what is missing: "To be defined" set in blue price type read
        # as a price, and stacked twice in one cell it read as two (2026-09-23).
        px = x + w - price_w - 0.18
        price, foot = fmt_price(t.get("services_price"), tbd="")
        if price:
            shown = True
            star = star or foot
            textbox(s, px, y + 0.07, price_w, 0.24,
                    [{"t": price + ("*" if foot else ""), "sz": 12, "b": True,
                      "color": C["blue"], "align": "r"}])
            fit.add(1, f"tier {i+1} price", price, 12, price_w, 0.24, bold=True, max_lines=1)
        else:
            absent_line(s, fit, px, y + 0.09, price_w, "Services price: to be defined",
                        f"tier {i+1} price")
        duration = fmt_duration(t.get("duration_weeks"), tbd="")
        if duration:
            textbox(s, px, y + 0.32, price_w, 0.18,
                    [{"t": duration, "sz": 8.5, "color": C["muted"], "align": "r"}])
            fit.add(1, f"tier {i+1} duration", duration, 8.5, price_w, 0.18, max_lines=1)
        else:
            absent_line(s, fit, px, y + 0.32, price_w, "Duration: to be defined",
                        f"tier {i+1} duration")
    return star, shown


def block_capabilities(s, spec: Spec, fit: FitLog):
    col = COL[1]
    x, w = col
    sec_label(s, col, LABEL_Y_BOT, "CAPABILITIES")
    areas = spec.get("capabilities") or []
    rows = []
    for a in areas:
        cats = [str(c.get("name", "")) for c in (a.get("categories") or [])] or [""]
        rows.append((str(a.get("area", "")), cats))
    total = sum(max(1, len(c)) for _, c in rows) or 1
    rh = min(0.20, PANEL_H_BOT / total)
    aw = 1.40
    y = PANEL_Y_BOT
    sz = 7.5 if rh >= 0.15 else 6.5
    for area, cats in rows:
        ah = rh * max(1, len(cats))
        rect(s, x, y, aw, ah - 0.02, fill=C["panel_grey"], line=C["hairline"],
             line_pt=0.5)
        apt = autofit_pt(area, aw - 0.16, ah - 0.04, sz, 5.5, bold=True, max_lines=3)
        textbox(s, x + 0.08, y, aw - 0.16, ah - 0.02,
                [{"t": area, "sz": apt, "b": True, "color": C["ink"]}], anchor="m")
        fit.add(1, f"cap area {area[:18]}", area, apt, aw - 0.16, ah - 0.04,
                bold=True, max_lines=3)
        for j, cat in enumerate(cats):
            cy = y + j * rh
            rect(s, x + aw + 0.02, cy, w - aw - 0.02, rh - 0.02, fill=C["white"],
                 line=C["hairline"], line_pt=0.5)
            cpt = autofit_pt(cat, w - aw - 0.18, rh - 0.04, sz, 5.5, max_lines=1)
            textbox(s, x + aw + 0.10, cy, w - aw - 0.18, rh - 0.02,
                    [{"t": cat, "sz": cpt, "color": C["ink"]}], anchor="m")
            fit.add(1, f"cap {cat[:20]}", cat, cpt, w - aw - 0.18, rh - 0.04,
                    max_lines=1)
        y += ah
    if y > PANEL_Y_BOT + PANEL_H_BOT + 0.02:
        fit.note(f"capability tree needs {y - PANEL_Y_BOT:.2f} in of "
                 f"{PANEL_H_BOT:.2f} in — trim areas or categories for this slide")


def block_next_steps(s, spec: Spec, fit: FitLog):
    col = COL[2]
    x, w = col
    steps = spec.get("exec_summary.next_steps") or []
    sec_label(s, col, LABEL_Y_BOT, "PLANNED NEXT STEPS", color=C["orange"])
    panel(s, x, PANEL_Y_BOT, w, PANEL_H_BOT, fill=C["orange_tint"],
          accent=C["orange"], line=C["hairline"])
    if not steps:
        textbox(s, x + 0.20, PANEL_Y_BOT, w - 0.40, PANEL_H_BOT,
                [{"t": "To be confirmed with the pack owner.", "sz": 9,
                  "color": C["muted_light"], "align": "c"}], anchor="m")
        fit.note("no exec_summary.next_steps in the spec — empty instance drawn")
        return
    n = min(len(steps), 4)
    rh = PANEL_H_BOT / n
    for i in range(n):
        st = steps[i]
        y = PANEL_Y_BOT + i * rh
        rect(s, x + 0.22, y + 0.16, 0.26, 0.26, fill=C["white"], line=C["orange"],
             line_pt=1.25, rounded=True, adj=0.5)
        textbox(s, x + 0.22, y + 0.16, 0.26, 0.26,
                [{"t": str(i + 1), "sz": 9.5, "b": True, "color": C["orange"],
                  "align": "c"}], anchor="m")
        title = str(st.get("title", st) if isinstance(st, dict) else st)
        detail = str(st.get("detail", "")) if isinstance(st, dict) else ""
        paras = [{"t": title, "sz": 10, "b": True, "color": C["ink"]}]
        if detail:
            paras.append({"t": detail, "sz": 8.5, "color": C["muted"]})
        bw = w - 0.84
        paras = autofit_paras(paras, bw, rh - 0.22, min_scale=0.7, default_sz=10)
        textbox(s, x + 0.62, y + 0.14, bw, rh - 0.22, paras)
        log_box(fit, 1, f"next step {i+1}", x + 0.62, y + 0.14, bw, rh - 0.22, paras, 10)


# ---------------------------------------------------------------------------

def _and(items: list[str]) -> str:
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def notes_body(prs, slide):
    """The notes text frame, created when the master gives the notes page none.

    The shipped base's notes master carries no placeholders, so python-pptx makes a
    notes page with nothing to write into. The standard body placeholder is added with
    its own geometry (the default notes-page layout, scaled to this deck's notes size),
    so PowerPoint shows the text in the notes pane.
    """
    notes = slide.notes_slide
    if notes.notes_text_frame is not None:
        return notes.notes_text_frame
    from pptx.oxml import parse_xml
    from pptx.oxml.ns import nsdecls
    size = prs.part._element.find(
        "{http://schemas.openxmlformats.org/presentationml/2006/main}notesSz")
    cx = int(size.get("cx")) if size is not None else 6858000
    cy = int(size.get("cy")) if size is not None else 9144000
    sp = parse_xml(
        f'<p:sp {nsdecls("p", "a")}><p:nvSpPr>'
        f'<p:cNvPr id="{notes.shapes._next_shape_id}" name="Notes Placeholder"/>'
        f'<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr><p:ph type="body" idx="1"/></p:nvPr>'
        f'</p:nvSpPr><p:spPr><a:xfrm><a:off x="{cx // 10}" y="{int(cy * 0.48)}"/>'
        f'<a:ext cx="{cx * 8 // 10}" cy="{int(cy * 0.39)}"/></a:xfrm></p:spPr>'
        f'<p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody></p:sp>')
    notes.shapes._spTree.append(sp)
    return notes.notes_text_frame


def speaker_notes(prs, slide, spec: Spec, prices_shown: bool, fit: FitLog) -> str:
    """Say which cut this is, in the notes, so the slide cannot travel as the wrong one.

    Internal: the internal cut; tier prices, where the slide shows any, come off before
    external use; where the customer may be named. Otherwise the shorter external note.
    Every clause is derived from what this build printed and from the clearance, so the
    note cannot claim a price or a name the slide does not carry.
    """
    descriptor = str(spec.get("clearance.anonymized_descriptor") or "an enterprise customer")
    customer = str(spec.get("meta.source_engagement.customer") or "").strip()
    cleared = [words for ch, words in CHANNEL_WORDS
               if customer and bool(spec.get(f"clearance.customer_name_allowed.{ch}", False))]
    if spec.channel == "internal":
        lines = ["Internal cut, for the internal solutions review."]
        if prices_shown:
            lines.append("The tier prices on this slide come off before any external use.")
        lines.append(f"The customer is named on {_and(cleared)} only; everywhere else it "
                     f"appears as \"{descriptor}\"." if cleared else
                     f"The customer is not cleared to be named on any channel; it appears "
                     f"as \"{descriptor}\".")
    else:
        prices = "tier prices included" if prices_shown else "no prices"
        here = ("as it is here" if spec.customer_name_allowed() and customer
                else f"so here it appears as \"{descriptor}\"")
        lines = [f"External cut: {prices}; the customer is named only where cleared, {here}."]
    text = "\n".join(lines)
    notes_body(prs, slide).text = text
    fit.note("speaker notes: " + " ".join(lines))
    return text


def build_slide(prs, layout, spec: Spec, fit: FitLog, title: str | None):
    header = str(spec.get("exec_summary.running_header") or "").strip()
    if header:
        m = RETIRED_HEADER.search(header)
        if m:
            header = RETIRED_HEADER.sub(HEADER_BRAND, header)
            print("build_exec_summary: the brief's running header still carries the retired "
                  "'%s' lockup — rewritten to '%s'." % (m.group(0), HEADER_BRAND),
                  file=sys.stderr)
    else:
        header = f"{HEADER_BRAND} — {spec.name()}"
    s = new_slide(prs, layout, title=title or spec.name(), header=header,
              title_pt=28, title_min_pt=16, title_box=TITLE_BOX)
    copy_slide_number(s, layout)

    goal = spec.get("exec_summary.goal")
    one = spec.get("one_liner.short") or spec.get("one_liner.full") or ""
    parts = []
    if goal:
        parts.append(("GOAL   ", {"b": True, "color": C["orange"], "sz": 11}))
        parts.append((goal + "   ", {"color": C["ink"], "sz": 12.5}))
    parts.append((one, {"color": C["ink"], "sz": 12.5}))
    full = "".join(t for t, _ in parts)
    pt = autofit_pt(full, 12.50, 0.30, 12.5, 8.5, max_lines=1)
    scale = pt / 12.5
    parts = [(t, {**o, "sz": round(o.get("sz", 12.5) * scale, 2)}) for t, o in parts]
    textbox(s, 0.42, SUBTITLE_Y, 12.50, 0.30, [{"t": parts}])
    fit.add(1, "one-liner", full, pt, 12.50, 0.30, max_lines=1)

    block_use_case(s, spec, fit)
    block_layers(s, spec, fit)
    block_proof(s, spec, fit)
    star, prices_shown = block_packages(s, spec, fit)
    block_capabilities(s, spec, fit)
    block_next_steps(s, spec, fit)
    speaker_notes(prs, s, spec, prices_shown, fit)

    # The caveat travels with the figures: with none printed there is nothing to
    # qualify, and "figures are illustrative" under a strip of metric names reads as
    # a hedge on claims the slide never made (2026-09-23).
    bits = [spec.kpi_caveat()] if spec.figured_kpis() else []
    if star:
        bits.append("* Indicative; depends on usage and rule-set complexity.")
    # the print-ready sentence first; the long internal statement only as a fallback
    div = spec.get("meta.source_engagement.divergence_line")   # the one print-ready sentence; the internal note never prints
    if not div and spec.get("meta.source_engagement.divergence_from_pack"):
        print("build_exec_summary: no meta.source_engagement.divergence_line in the brief — the "
              "divergence footnote is omitted (the internal note is never printed); add the line "
              "through the spec skill's proof card", file=sys.stderr)
    if div:
        # A divergence line written as a full sentence stands alone; the run-in prefix
        # is for a fragment. "…engagement: Not the first client's results" read as a
        # sentence cut in half (2026-09-23).
        line = str(div).strip()
        standalone = bool(line) and line[:1].isupper() and line.endswith((".", "!", "?"))
        bits.append(line if standalone
                    else f"Pack scope differs from the delivered engagement: {line}")
    tail = " ".join(b for b in bits if b)
    textbox(s, 0.42, FOOTNOTE_Y, 12.50, 0.30,
            [{"t": tail, "sz": 8, "color": C["muted_light"]}])
    fit.add(1, "footnote", tail, 8, 12.50, 0.30, max_lines=2)
    return s


def add_closing(prs, fit: FitLog, line: str | None = None):
    names = [l.name for m in prs.slide_masters for l in m.slide_layouts]
    match = next((n for n in names if n.lower().startswith("close")), None)
    if not match:
        fit.note("--with-closing ignored: the host has no Close layout "
                 f"(layouts: {', '.join(names) or 'none'})")
        return None
    layout = pick_layout(prs, match)
    slide = prs.slides.add_slide(layout)
    line = None
    for ph in slide.placeholders:
        if ph.placeholder_format.idx in (0, 1, 2, 3) and ph.has_text_frame:
            line = line or "We look forward to continuing the conversation."
            ph.text_frame.text = line
            break
    return slide


def build(spec: Spec, base: Path, out_dir: Path, fit: FitLog,
          host: Path | None, with_closing: bool, title: str | None) -> Path:
    if host:
        prs = Presentation(str(host))
        strip_slides(prs)
        fit.note(f"built on the host deck's master: {host.name}")
    else:
        prs = open_base(base)
    layout = pick_layout(prs, "Title-1Column", "1_1-Title", "ShortTitle-Empty")
    fit.note(f"layout: {layout.name!r}")
    build_slide(prs, layout, spec, fit, title)
    if with_closing:
        add_closing(prs, fit, spec.get("exec_summary.closing_line"))
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = spec.get("meta.slug", "pack")
    out = out_dir / f"{slug}-exec-summary.pptx"
    prs.save(str(out))
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Build the one-slide executive summary for an accelerator pack.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Done means: fit report clean, render reviewed (see the deck "
               "skill's tools/render_probe.sh), linter clean.")
    ap.add_argument("spec", help="path to pack-spec.yaml")
    ap.add_argument("--out", required=True, help="output directory")
    ap.add_argument("--channel", choices=["internal", "partner_print"], default="internal",
                    help="who the slide is for: internal (default — the solutions-review deck, "
                         "the `<name> App` variant, internal clearance) or partner_print (a "
                         "partner deck: the external name variant and the partner contact)")
    ap.add_argument("--host-deck", default=None,
                    help="build on this deck's master so the slide pastes in unchanged")
    ap.add_argument("--with-closing", action="store_true",
                    help="append the host's closing slide when it has a Close layout")
    ap.add_argument("--base", default=str(BASE_DEFAULT),
                    help="SoftServe deck base .pptx used when --host-deck is absent")
    ap.add_argument("--title", default=None,
                    help="slide title (default: the spec's internal_slide name variant)")
    ap.add_argument("--fit-report", action="store_true",
                    help="print the per-box text-fit estimate for every box")
    ap.add_argument("--allow-overflow", action="store_true",
                    help="exit 0 even when boxes overflow (review builds only)")
    args = ap.parse_args(argv)

    try:
        # The executive summary is the internal artifact by default: internal naming
        # and internal clearance (2026-09-18 naming decision). `--channel partner_print`
        # cuts the same slide for a partner deck, where the external name variant and
        # the partner clearance apply.
        spec = Spec.load(args.spec, channel=args.channel)
    except SpecError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    fit = FitLog()
    try:
        out = build(spec, Path(args.base), Path(args.out), fit,
                    Path(args.host_deck) if args.host_deck else None,
                    args.with_closing, args.title)
    except SpecError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(f"built {out}")
    print(fit.report(verbose=args.fit_report))
    if fit.problems() and not args.allow_overflow:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
