#!/usr/bin/env python3
"""derive-stage-view.py — build the listing's `technology.capabilities[]` stage
view from a pack spec's `capabilities[]`.

    python3 derive-stage-view.py packs/<slug>/pack-spec.md
    python3 derive-stage-view.py pack-spec.md --map "Allocation rules=Plan,Review=Approve" --out caps.js
    python3 derive-stage-view.py pack-spec.json --format json

WHY THIS IS A DERIVATION, NOT A COPY
    The spec owns capabilities as **Area > Category > Feature**, which is how a
    feature list and a capability matrix are read: by subject.
    The listing's Technology tab owns them as **four workflow stages**, which is
    how a buyer reads them: in the order the work happens, and in the same order
    the product page's How-it-works stepper already walks.
    They are two views of one set. The mapping between them is a per-pack
    decision — the same capability sits at a different stage in a document
    pipeline and in an optimizer — so it lives in the spec, as `stage` on each
    `capabilities[]` area, and this script only applies it.

    Nothing is invented here. Every feature in the spec lands in exactly one
    stage; a feature with no home is reported, never dropped.

WHERE THE STAGE COMES FROM, in order
    1. `capabilities[].stage` in the spec        (the intended home)
    2. --map "Area=Stage,Area=Stage"             (a one-off override)
    3. an interactive prompt, area by area       (a TTY only)
    Option 3 refuses to run without a terminal rather than guessing: exit 4 and
    the message names the areas still unmapped. An environment that cannot ask
    is a deferred answer, never a made-up one.

WHAT IT ENFORCES (the listing's own invariants, so the checker will pass)
    - exactly 4 stages, unique, and emitted IN WORKFLOW ORDER: a stage named
      after a `workflow.steps[]` entry is sorted by that step, because the
      capability areas are ordered by subject and the listing reads in the order
      the work happens;
    - at least 3 items per stage;
    - `state` only where the spec states one, mapped available→(omitted),
      partial→"partial", roadmap→"roadmap". The listing omits `state` where no
      shipped capability matrix states one: a guessed tag is worse than none.
      Pass --state-all to emit "supported" for available features too, only when
      the pack has a real matrix behind it.

EXIT CODES
    0 written · 2 input not found or malformed · 3 PyYAML missing (an
    environment problem, not a data problem — retry, do not record a result)
    · 4 stages unresolved and no terminal to ask.
"""

import argparse
import json
import os
import sys

SITE_STATES = {"available": None, "partial": "partial", "roadmap": "roadmap"}
STAGE_TARGET = 4
MIN_ITEMS = 3


def _packspec():
    """The one spec loader, shared/tools/packspec.py: the plugin's own."""
    here = os.path.dirname(os.path.abspath(__file__))
    parents = [here]
    while os.path.dirname(parents[-1]) != parents[-1]:
        parents.append(os.path.dirname(parents[-1]))
    for up in range(3, 7):                  # tools/ -> skill/ -> skills/ -> plugin/ (and the bundle)
        if len(parents) <= up:
            break
        shared = os.path.join(parents[up], "shared", "tools")
        if os.path.isfile(os.path.join(shared, "packspec.py")):
            if shared not in sys.path:
                sys.path.insert(0, shared)
            break
    import packspec
    return packspec


def load_spec(path):
    if not os.path.exists(path):
        print("derive-stage-view: not found: %s" % path, file=sys.stderr)
        raise SystemExit(2)
    if path.endswith((".json", ".jsn")):
        return json.loads(open(path, "r", encoding="utf-8").read())
    try:
        import yaml  # type: ignore  # noqa: F401  (the spec loader needs it)
    except ImportError:
        print(
            "derive-stage-view: PyYAML is not installed in this interpreter.\n"
            "  This is an environment condition, not a result: install it\n"
            "  (python3 -m pip install pyyaml) or convert the spec to JSON and\n"
            "  pass the .json file. Nothing was derived.",
            file=sys.stderr,
        )
        raise SystemExit(3)
    packspec = _packspec()
    try:
        return packspec.load(path)[0]
    except packspec.SpecError as err:
        print("derive-stage-view: the spec does not parse: %s" % err, file=sys.stderr)
        raise SystemExit(2)


def features_of(area):
    """Flatten one spec area into (feature name, status) pairs, in spec order."""
    out = []
    for cat in area.get("categories") or []:
        for feat in cat.get("features") or []:
            name = (feat.get("name") or "").strip()
            if not name:
                continue
            out.append((name, (feat.get("status") or "").strip().lower()))
    return out


def resolve_stages(areas, cli_map, interactive):
    """Return {area name: stage}, asking only for what the spec left open."""
    mapping, unmapped = {}, []
    for area in areas:
        name = (area.get("area") or "").strip()
        stage = (area.get("stage") or "").strip()
        if not stage and name in cli_map:
            stage = cli_map[name]
        if stage:
            mapping[name] = stage
        else:
            unmapped.append(name)

    if not unmapped:
        return mapping

    if not interactive:
        print(
            "derive-stage-view: no stage for %s.\n"
            "  Add `stage:` to those areas in the pack spec (that is where the\n"
            "  decision belongs), or pass --map \"Area=Stage,...\". Nothing derived."
            % ", ".join('"%s"' % a for a in unmapped),
            file=sys.stderr,
        )
        raise SystemExit(4)

    known = sorted({s for s in mapping.values()})
    print("The listing groups capabilities into exactly four workflow stages,")
    print("named in the product's own vocabulary and in the order the work happens.")
    if known:
        print("Stages used so far: %s" % ", ".join(known))
    print("")
    for name in unmapped:
        preview = ", ".join(n for n, _ in features_of(next(a for a in areas if (a.get("area") or "").strip() == name))[:3])
        while True:
            print('Area "%s"  (%s…)' % (name, preview))
            got = input("  stage: ").strip()
            if got:
                mapping[name] = got
                break
            print("  A stage is required — the feature cannot be dropped.")
    return mapping


def build(spec, mapping, state_all):
    areas = spec.get("capabilities") or []
    groups, order, notes = {}, [], []
    for area in areas:
        name = (area.get("area") or "").strip()
        stage = mapping.get(name, "")
        feats = features_of(area)
        if not feats:
            notes.append('area "%s" carries no features — nothing to place' % name)
            continue
        if stage not in groups:
            groups[stage] = []
            order.append(stage)
        for fname, status in feats:
            item = {"name": fname}
            if status in SITE_STATES:
                mapped = SITE_STATES[status]
                if mapped:
                    item["state"] = mapped
                elif state_all:
                    item["state"] = "supported"
            elif status:
                notes.append('feature "%s" has status "%s", which is not available/partial/roadmap — state omitted' % (fname, status))
            groups[stage].append(item)
    return [{"stage": s, "items": groups[s]} for s in order], notes


def in_workflow_order(spec, view):
    """Stages render in the order the work happens, not in spec order.

    The listing invariant is that `technology.capabilities[]` walks the same four
    stages as `overview.steps`, in the same order. Capability AREAS are ordered by
    subject (the feature list's order), so a stage named after a workflow step is
    sorted by that step's position; a stage that matches no step keeps its
    relative position at the end.
    """
    steps = [str(st.get("name") or "").strip().lower()
             for st in (spec.get("workflow") or {}).get("steps") or []
             if isinstance(st, dict)]
    if not steps:
        return view, ""
    def key(item):
        name = str(item["stage"]).strip().lower()
        return (steps.index(name), 0) if name in steps else (len(steps), view.index(item))
    ordered = sorted(view, key=key)
    if [g["stage"] for g in ordered] == [g["stage"] for g in view]:
        return view, ""
    unmatched = [g["stage"] for g in ordered
                 if str(g["stage"]).strip().lower() not in steps]
    note = "stages reordered to the workflow order the listing walks"
    if unmatched:
        note += " (no workflow step matches %s — left at the end)" % ", ".join(
            '"%s"' % u for u in unmatched)
    return ordered, note


def as_js(view):
    lines = ["      capabilities: ["]
    for i, g in enumerate(view):
        lines.append("        {")
        lines.append('          stage: %s,' % json.dumps(g["stage"], ensure_ascii=False))
        lines.append("          items: [")
        for j, it in enumerate(g["items"]):
            body = 'name: %s' % json.dumps(it["name"], ensure_ascii=False)
            if "state" in it:
                body += ', state: %s' % json.dumps(it["state"])
            lines.append("            { %s }%s" % (body, "" if j == len(g["items"]) - 1 else ","))
        lines.append("          ]")
        lines.append("        }%s" % ("" if i == len(view) - 1 else ","))
    lines.append("      ]")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(add_help=True, description="Derive the listing stage view from a pack spec.")
    ap.add_argument("spec", help="packs/<slug>/pack-spec.md (or .json)")
    ap.add_argument("--map", default="", help='one-off stage mapping: "Area=Stage,Area=Stage"')
    ap.add_argument("--out", default="", help="write here instead of stdout")
    ap.add_argument("--format", choices=["js", "json"], default="js", help="js (a content.js fragment) or json")
    ap.add_argument("--state-all", action="store_true", help='also emit state:"supported" for available features (only with a real capability matrix behind the pack)')
    ap.add_argument("--no-prompt", action="store_true", help="never ask; exit 4 on an unmapped area")
    args = ap.parse_args()

    spec = load_spec(args.spec)
    if not isinstance(spec, dict) or not spec.get("capabilities"):
        print("derive-stage-view: the spec has no `capabilities[]` — run the spec skill first.", file=sys.stderr)
        raise SystemExit(2)

    cli_map = {}
    for pair in filter(None, [p.strip() for p in args.map.split(",")]):
        if "=" not in pair:
            print('derive-stage-view: --map entry "%s" is not Area=Stage' % pair, file=sys.stderr)
            raise SystemExit(2)
        k, v = pair.split("=", 1)
        cli_map[k.strip()] = v.strip()

    interactive = sys.stdin.isatty() and not args.no_prompt
    mapping = resolve_stages(spec["capabilities"], cli_map, interactive)
    view, notes = build(spec, mapping, args.state_all)
    view, order_note = in_workflow_order(spec, view)
    if order_note:
        notes.append(order_note)

    problems = []
    if len(view) != STAGE_TARGET:
        problems.append(
            "%d stages, the listing needs exactly %d — merge or split the mapping "
            "(the four stages are the same four the How-it-works stepper walks)"
            % (len(view), STAGE_TARGET)
        )
    for g in view:
        if len(g["items"]) < MIN_ITEMS:
            problems.append('stage "%s" has %d capabilities, the listing needs at least %d' % (g["stage"], len(g["items"]), MIN_ITEMS))

    text = json.dumps(view, indent=2, ensure_ascii=False) if args.format == "json" else as_js(view)
    if args.out:
        open(args.out, "w", encoding="utf-8").write(text + "\n")
        print("derive-stage-view: wrote %s" % args.out, file=sys.stderr)
    else:
        print(text)

    total = sum(len(g["items"]) for g in view)
    print("\nderive-stage-view: %d capabilities across %d stages (%s)" % (total, len(view), " · ".join(g["stage"] for g in view)), file=sys.stderr)
    for n in notes:
        print("  ! %s" % n, file=sys.stderr)
    for p in problems:
        print("  x %s" % p, file=sys.stderr)
    if problems:
        print("  The output above is written as derived — fix the mapping in the spec, not the output.", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
