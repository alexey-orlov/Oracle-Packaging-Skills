#!/usr/bin/env python3
"""Turn the pack's architecture model into the mini-site's `SITE_DIAGRAMS` figure.

    python3 tools/diagram_to_site.py <repo>/packs/<slug>/pack-spec.md --slug <slug>

The model is built from the spec with the site's name variant, by the function the deck
and the one-pager also call (shared/tools/build_diagram.py); a model file written by
`build_diagram.py --out` is read as it is.

Prints one JavaScript entry, ready to paste into `site/data/diagrams.js` between the
other packs' figures. The figure is NEVER written by hand: the deck, the one-pager and
this figure are three levels of detail on one model (shared/references/architecture-diagram.md),
and a hand-drawn site figure is how the three pictures drifted apart in the first place.

What the site gets that the printed artifacts do not: the `detail` level. Titles are the
model's names, split into at most two lines and never shortened — the consistency check
matches them character for character. Subs come from `detail` and are clipped to the box,
with a note on stderr saying what was clipped, so the fix is a shorter `detail` in the
model rather than a silently half-told box.

Exit codes
    0   the figure was printed
    1   the model cannot be drawn as a site figure (no sources, no app, no engine)
    2   usage error (unreadable spec or model file)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PROG = "diagram_to_site"
HERE = Path(__file__).resolve().parent
for _up in range(2, 6):                     # the model builder: the plugin's shared/tools
    _shared = HERE.parents[_up] / "shared" / "tools" if len(HERE.parents) > _up else None
    if _shared is not None and (_shared / "build_diagram.py").is_file():
        sys.path.insert(0, str(_shared))
        break

# Characters that fit one line of each box, measured on the renderer's own geometry
# (diagrams.js: source 236 px, group node 312 px, target 248 px, at 27/21 px type).
FIT = {"source": (20, 22), "node": (22, 26), "target": (14, 22), "label": (28, 28)}
MAX_LINES = 2
MAX_SOURCES = 2          # `flow` draws sources[0] and sources[1]; a third would not render


def wrap(text: str, width: int, lines: int = MAX_LINES) -> list[str]:
    """Split into at most `lines` BALANCED lines — a one-word first line reads as a typo.

    Two lines is what the site's boxes take, so the split point is the one that makes
    the longer line as short as possible; a dash never starts a line.
    """
    words = str(text or "").split()
    if not words:
        return []
    whole = " ".join(words)
    if lines <= 1 or len(words) == 1 or len(whole) <= width:
        return [whole]                       # one line that fits is never split in two
    best, best_cost = None, None
    for cut in range(1, len(words)):
        head, tail = " ".join(words[:cut]), " ".join(words[cut:])
        if tail.lstrip().startswith(("—", "-", "–")):
            continue                         # a continuation line never opens on a dash
        if lines > 2:
            rest = wrap(tail, width, lines - 1)
            longest = max([len(head)] + [len(r) for r in rest])
            candidate = [head] + rest
        else:
            longest = max(len(head), len(tail))
            candidate = [head, tail]
        cost = (max(longest - width, 0), longest)
        if best_cost is None or cost < best_cost:
            best, best_cost = candidate, cost
    return best or [" ".join(words)]


# A clipped line must not end mid-thought: these are dropped off the tail.
DANGLING = {"and", "or", "with", "plus", "the", "a", "an", "of", "for", "to", "in", "on"}


def clip(text: str, width: int, where: str, warnings: list,
         lines: int = MAX_LINES) -> list[str]:
    """Wrap, then drop whole trailing words that would not fit the box."""
    words = str(text or "").split()
    if not words:
        return []
    kept = list(words)
    while kept:
        while kept and (kept[-1].lower().strip(".,;:—-") in DANGLING
                        or kept[-1] in {"—", "-", ",", ";"}
                        or kept[-1].count("(") > kept[-1].count(")")):
            kept.pop()                       # never end on "and", a comma, a dash or "(4–8"
        if not kept:
            break
        kept[-1] = kept[-1].rstrip(",;:—- ")
        wrapped = wrap(" ".join(kept), width, lines)
        if len(wrapped) <= lines and all(len(line) <= width + 2 for line in wrapped):
            if len(kept) < len(words):
                warnings.append(f"{where}: clipped to \"{' '.join(kept)}\" — shorten its "
                                f"`detail` in the model so the box says the whole thing")
            return wrapped
        kept.pop()
    return wrap(words[0], width, lines)


def js(value) -> str:
    return json.dumps(value, ensure_ascii=False)


def node(title: str, detail: str, kind: str, warnings: list, accent: bool = False,
         sub_lines: list | None = None) -> str:
    title_lines = wrap(title, FIT[kind][0])          # a name is never shortened
    if len(title_lines) > MAX_LINES:
        warnings.append(f"{title!r} needs more than two lines in the {kind} box — "
                        f"it will render tight")
    if sub_lines is None:
        sub_lines = clip(detail, FIT[kind][1], f"{kind} \"{title}\"", warnings)
    out = f"{{ title: {js(title_lines)}"
    if sub_lines:
        out += f", sub: {js(sub_lines)}"
    if accent:
        out += ", accent: true"
    return out + " }"


def figure(model: dict, slug: str, warnings: list) -> str:
    sources = model.get("sources") or []
    destinations = model.get("destinations") or []
    if not sources or not model.get("app") or not model.get("engine"):
        raise SystemExit(f"{PROG}: the model has no sources, app or engine — "
                         f"rebuild it with shared/tools/build_diagram.py")
    if len(sources) > MAX_SOURCES:
        warnings.append(f"the model has {len(sources)} sources and the site's flow figure "
                        f"draws two — the others are left off; say so to the owner")

    src = ",\n".join("      " + node(s["name"], s.get("detail", ""), "source", warnings)
                     for s in sources[:MAX_SOURCES])
    label = wrap(model["platform"]["label"], FIT["label"][0], 1) + \
        clip(", ".join(model["platform"]["services"]), FIT["label"][1],
             "the platform label", warnings, lines=1)

    # The target box is the only slot this figure has for what happens on the right,
    # so the destinations are named on its second line: the site names the same
    # systems as the deck and the one-pager, at its own level of detail.
    gate = model.get("gate")
    width = FIT["target"][1]
    if gate:
        first = clip(gate.get("line") or "", width, f"the gate \"{gate['name']}\"",
                     warnings, lines=1)
        lines = list(first)
        if destinations:
            lines.append("into " + " · ".join(d["name"] for d in destinations))
        target = node(gate["name"], "", "target", warnings, accent=True,
                      sub_lines=lines[:MAX_LINES])
    elif destinations:
        first = clip(destinations[0].get("data") or "", width,
                     f"the destination \"{destinations[0]['name']}\"", warnings, lines=1)
        lines = list(first)
        others = [d["name"] for d in destinations[1:]]
        if others:
            lines.append("also " + " · ".join(others))
        target = node(destinations[0]["name"], "", "target", warnings, accent=True,
                      sub_lines=lines[:MAX_LINES])
    else:
        raise SystemExit(f"{PROG}: the model has neither a human gate nor a destination — "
                         f"the figure has nothing to point at")
    for line in re.findall(r'"((?:[^"\\]|\\.)*)"', target):
        if len(line) > width + 2 and (line.startswith("into ") or line.startswith("also ")):
            warnings.append(f'the target\'s "{line}" is longer than the box\'s line — '
                            f"a destination name is never shortened, so it will render "
                            f"tight; shorten the system's name in the pack brief if that matters")

    out = [f'  {js(slug)}: {{',
           '    layout: "flow",',
           '    sources: [', src, '    ],',
           '    group: {',
           f'      label: {js(label)},',
           '      nodes: [',
           "        " + node(model["app"]["name"], model["app"].get("detail", ""),
                             "node", warnings) + ",",
           "        " + node(model["engine"]["name"], model["engine"].get("detail", ""),
                             "node", warnings),
           '      ]',
           '    },',
           f'    target: {target},']
    note = str(model.get("note") or "").strip()
    if note:
        out.append(f'    note: {js(note.rstrip("."))}')
    else:
        out[-1] = out[-1].rstrip(",")
        warnings.append("the model carries no invariant — the figure prints no note line")
    out.append("  },")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog=PROG, description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("model", help="packs/<slug>/pack-spec.md (or a model file from build_diagram.py --out)")
    ap.add_argument("--slug", default=None,
                    help="the site's product slug (default: the model's own `slug`)")
    args = ap.parse_args(argv)

    import build_diagram
    try:
        model = build_diagram.load_model(args.model, channel="site")
    except build_diagram.DiagramError as err:
        sys.stderr.write(f"{PROG}: the architecture picture cannot be drawn: {err}\n")
        return 1
    except Exception as err:            # unreadable file, or a spec that does not parse
        sys.stderr.write(f"{PROG}: cannot read {args.model}: {err}\n")
        return 2

    warnings: list[str] = []
    slug = args.slug or model.get("slug") or "pack"
    try:
        print(figure(model, slug, warnings))
    except SystemExit as err:
        sys.stderr.write(f"{err}\n")
        return 1
    for warning in warnings:
        sys.stderr.write(f"note: {warning}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
