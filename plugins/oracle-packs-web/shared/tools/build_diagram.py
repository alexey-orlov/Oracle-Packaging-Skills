#!/usr/bin/env python3
"""Build the pack's ONE architecture model — the picture the three artifacts share.

    python3 shared/tools/build_diagram.py <pack-spec.md> --out packs/<slug>/architecture.json
    python3 shared/tools/build_diagram.py <pack-spec.md> --check        # rules only, writes nothing

Also a library:

    from build_diagram import build_model, DiagramError
    model = build_model(spec_dict, channel="partner_print")

The deck, the one-pager and the mini-site used to derive a picture each from the
same spec, and drifted. They now render THIS model: it is built once, reviewed
once, and detailed to each artifact's own level.

Levels of detail — the contract every renderer obeys
    name      prints everywhere (deck, one-pager, site)
    line      the deck and the one-pager (<= 8 words)
    detail    the mini-site only (<= 25 words)

Shape
    {slug, pack, channel,
     sources:      [{name, data, detail}],          data = the label on the arrow IN
     platform:     {label, services: [...]},
     app:          {name, line, detail},            name = "<pack> by SoftServe"
     engine:       {name, line, detail},            name = catalog names joined by " · "
     destinations: [{name, data, writeback}],       data = the label on the arrow OUT
     gate:         {name, line} | null,             the workflow's human step
     note:         "..."}                           the one invariant

Everything traces to a spec entry: `architecture.inputs[]`, `architecture.stack[]`,
`architecture.outputs[]`, `oracle_products[]`, the catalog (shared/data/oracle-products.yaml),
`meta.name` with the channel's variant, and `workflow.steps[].human_in_the_loop`.

Exit codes
    0   the model is valid (and was written, unless --check)
    1   a rule failed — a source with no edge, an output with no destination,
        an unnamed engine, an app box without the pack's name
    2   usage or dependency error (unreadable spec, no PyYAML)

Rules: shared/references/architecture-diagram.md.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

PROG = "build_diagram"

LINE_WORDS = 8          # what the deck and the one-pager print under a box
DETAIL_WORDS = 25       # what the mini-site prints under a box

# A layer is the app layer / the infrastructure layer when its name says so.
APP_WORDS = ("app", "business", "by softserve", "application")
INFRA_WORDS = ("infra", "infrastructure", "platform")
ENGINE_WORDS = ("engine", "optimiz", "model", "agent", "retriev", "solver")

# The verb the gate's name carries, from what the human step is called.
GATE_VERBS = ((("approve", "sign-off", "sign off", "signoff"), "approves"),
              (("review", "check", "inspect"), "reviews"),
              (("confirm", "accept", "validate"), "confirms"))


class DiagramError(RuntimeError):
    """A rule of shared/references/architecture-diagram.md the spec breaks."""


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------

def clean(value) -> str:
    return re.sub(r"\s+", " ", str(value if value is not None else "")).strip()


def dig(data, path, default=None):
    node = data
    for part in path.split("."):
        if not isinstance(node, dict) or part not in node:
            return default
        node = node[part]
    return node if node is not None else default


def split_lead(text: str) -> tuple[str, str]:
    """"Any CRM — Oracle CX included" -> ("Any CRM", "Oracle CX included")."""
    for sep in (" — ", " – ", " - "):
        if sep in text:
            head, _, tail = text.partition(sep)
            return clean(head), clean(tail)
    return clean(text), ""


def clip_words(text: str, limit: int) -> str:
    """At most `limit` words, cut at a clause boundary rather than mid-thought."""
    text = clean(text)
    if not text or len(text.split()) <= limit:
        return text
    for sep in (" — ", "; ", ", "):
        head = text.split(sep)[0]
        if head and len(head.split()) <= limit:
            return clean(head)
    return " ".join(text.split()[:limit])


def join_items(items) -> str:
    return ", ".join(clean(x) for x in (items or []) if clean(x))


# ---------------------------------------------------------------------------
# the product catalog — the engine's names come from it, never from an id
# ---------------------------------------------------------------------------

_CATALOG = None


def catalog_paths() -> list[Path]:
    here = Path(__file__).resolve().parent
    out = [here.parent / "data" / "oracle-products.yaml"]
    for up in range(1, 6):
        if len(here.parents) > up:
            out.append(here.parents[up] / "shared" / "data" / "oracle-products.yaml")
    env = os.environ.get("ORACLE_PRODUCT_CATALOG")
    if env:
        out.insert(0, Path(env))
    return out


def catalog() -> dict:
    """{id: name} — empty when no catalog is reachable (the spec's own names then win)."""
    global _CATALOG
    if _CATALOG is None:
        _CATALOG = {}
        import yaml
        for path in catalog_paths():
            if not path.is_file():
                continue
            try:
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
            except Exception:               # a broken catalog is not a crash
                continue
            rows = data.get("products") if isinstance(data, dict) else data
            for row in rows or []:
                if isinstance(row, dict) and row.get("id"):
                    _CATALOG[str(row["id"])] = clean(row.get("name")) or str(row["id"])
            break
    return _CATALOG


def product_name(key: str) -> str:
    return catalog().get(clean(key), "") or catalog().get(clean(key).lower().replace(" ", "-"), "")


# ---------------------------------------------------------------------------
# the model
# ---------------------------------------------------------------------------

def pack_name(spec: dict, channel: str) -> str:
    """The pack's name in this channel's variant (the deck's own rule)."""
    variants = dig(spec, "meta.name_variants", {}) or {}
    base = clean(dig(spec, "meta.name", ""))
    if channel == "internal":
        return clean(variants.get("internal_slide") or variants.get("site") or base)
    if channel == "site":
        return clean(variants.get("site") or variants.get("external") or base)
    return clean(variants.get("external") or variants.get("site") or base)


def layers(spec: dict) -> list:
    return [layer for layer in (dig(spec, "architecture.stack", []) or [])
            if isinstance(layer, dict)]


def layer_like(spec: dict, words, default_index=None) -> dict:
    stack = layers(spec)
    for layer in stack:
        if any(w in clean(layer.get("layer")).lower() for w in words):
            return layer
    if default_index is not None and stack:
        return stack[max(-len(stack), min(default_index, len(stack) - 1))]
    return {}


def engine_layer(spec: dict) -> dict:
    for layer in layers(spec):
        if layer.get("catalog_id") and not any(
                w in clean(layer.get("layer")).lower() for w in INFRA_WORDS):
            return layer
    return layer_like(spec, ENGINE_WORDS)


def engine_names(layer: dict, notes: list) -> list:
    """Catalog names for the engine layer — never a bare id on a slide."""
    names: list[str] = []
    cid = layer.get("catalog_id")
    for one in (cid if isinstance(cid, list) else ([cid] if cid else [])):
        names.append(product_name(str(one)) or clean(one))
    for item in layer.get("items") or []:
        key = clean(item)
        resolved = product_name(key)
        if resolved:
            name = resolved
        elif re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)+", key):
            notes.append(f"`{key}` is not in the product catalog — left off the engine "
                         f"box rather than printed as an id")
            continue
        else:
            name = key
        if name and name not in names:
            names.append(name)
    return [n for n in names if n]


def system_role(spec: dict, system: str) -> str:
    """What the spec says this system IS — from `oracle_products[].why`."""
    hay = clean(system).lower()
    if not hay:
        return ""
    for row in (spec.get("oracle_products") or []):
        if not isinstance(row, dict):
            continue
        name = clean(row.get("name") or product_name(str(row.get("id") or ""))).lower()
        if name and (name in hay or hay in name):
            return clean(row.get("why"))
    return ""


def gate_from_workflow(spec: dict) -> tuple[dict | None, str]:
    """The workflow's human step, and the invariant it enforces.

    The gate is the LAST step the spec marks `human_in_the_loop: true` — the one
    standing between the machine's output and the system of record. Its name is the
    role and the verb ("Reviewer approves"); its line is the step's own name.
    """
    steps = [s for s in (dig(spec, "workflow.steps", []) or []) if isinstance(s, dict)]
    human = [s for s in steps if s.get("human_in_the_loop")]
    if not human:
        note = ""
        for step in reversed(steps):
            if clean(step.get("failure_path")):
                note = clean(step.get("failure_path"))
                break
        return None, note
    step = human[-1]
    label = clean(step.get("name"))
    verb = "approves"
    for words, spelling in GATE_VERBS:
        if any(w in label.lower() for w in words):
            verb = spelling
            break
    role = clean(step.get("role") or step.get("actor_role")) or "Reviewer"
    gate = {"name": f"{role[0].upper()}{role[1:]} {verb}", "line": clip_words(label, LINE_WORDS)}
    note = clean(step.get("failure_path"))
    if not note:
        for other in reversed(steps):
            if clean(other.get("failure_path")):
                note = clean(other.get("failure_path"))
                break
    return gate, note


def build_model(spec: dict, channel: str = "partner_print") -> dict:
    """The one model. Raises DiagramError when a diagram rule cannot be met."""
    spec = spec or {}
    notes: list[str] = []
    name = pack_name(spec, channel)
    if not name:
        raise DiagramError("the pack brief has no `meta.name`, so the app box cannot "
                           "carry the pack's name")

    # -- sources: one box per input, the data on its arrow
    sources, problems = [], []
    for index, row in enumerate(dig(spec, "architecture.inputs", []) or []):
        row = row if isinstance(row, dict) else {"system": row}
        sys_name, qualifier = split_lead(clean(row.get("system")))
        data = clean(row.get("data"))
        if not sys_name:
            problems.append(f"input {index + 1} names no system — a box with no name "
                            f"cannot go on the diagram")
            continue
        if not data:
            problems.append(f"the source \"{sys_name}\" has no edge: "
                            f"`architecture.inputs[{index}].data` says what it sends")
        detail = qualifier or system_role(spec, sys_name) or data
        sources.append({"name": sys_name, "data": data,
                        "detail": clip_words(detail, DETAIL_WORDS)})
    if not sources:
        problems.append("the pack brief names no `architecture.inputs[]` — the diagram "
                        "has nothing flowing in")

    # -- destinations: one per output; a system that is also a source is a write-back
    source_names = {s["name"].lower() for s in sources}
    destinations = []
    for index, row in enumerate(dig(spec, "architecture.outputs", []) or []):
        row = row if isinstance(row, dict) else {"system": row}
        sys_name, _ = split_lead(clean(row.get("system")))
        data = clean(row.get("data"))
        if not sys_name:
            problems.append(f"output {index + 1} has no destination — "
                            f"`architecture.outputs[{index}].system` names the system "
                            f"the result lands in")
            continue
        if not data:
            problems.append(f"the output to \"{sys_name}\" has no edge: "
                            f"`architecture.outputs[{index}].data` says what comes back")
        destinations.append({"name": sys_name, "data": data,
                             "writeback": sys_name.lower() in source_names})
    if not destinations:
        problems.append("the pack brief names no `architecture.outputs[]` — nothing "
                        "leaves the app, so no destination can be drawn")

    # -- the platform: one line, the services the spec actually lists
    infra = layer_like(spec, INFRA_WORDS, default_index=-1)
    vendor = clean(infra.get("vendor")) or "Oracle"
    label = ("Oracle Cloud Infrastructure" if vendor.lower().startswith("oracle")
             else f"{vendor} infrastructure")
    services = [clean(x) for x in (infra.get("items") or []) if clean(x)]
    if not services:
        cid = infra.get("catalog_id")
        services = [product_name(str(c)) or clean(c)
                    for c in (cid if isinstance(cid, list) else ([cid] if cid else []))]
    if not services and clean(infra.get("summary")):
        services = [clean(infra.get("summary"))]

    # -- the app: the pack's own name, never a generic role
    app_layer = layer_like(spec, APP_WORDS, default_index=1)
    app_detail = clean(app_layer.get("summary"))
    items = join_items(app_layer.get("items"))
    if items and items.lower() not in app_detail.lower():
        app_detail = f"{app_detail} — {items}" if app_detail else items
    app = {"name": f"{name} by SoftServe",
           "line": clip_words(app_layer.get("summary") or items, LINE_WORDS),
           "detail": clip_words(app_detail, DETAIL_WORDS)}
    if not clean(app["line"]):
        notes.append("the app layer has no `summary` — the app box carries its name only")

    # -- the engine: the vendor products, by their catalog names
    eng_layer = engine_layer(spec)
    products = engine_names(eng_layer, notes)
    eng_detail = clean(eng_layer.get("summary")) or clean(eng_layer.get("layer"))
    engine = {"name": " · ".join(products),
              "line": clip_words(eng_detail, LINE_WORDS),
              "detail": clip_words(eng_detail, DETAIL_WORDS)}
    if not engine["name"]:
        problems.append("the engine box would be unnamed: no `catalog_id` and no catalog "
                        "product among the engine layer's `items` — an unnamed engine "
                        "tells the seller nothing")

    if name.lower() not in app["name"].lower():
        problems.append(f"the app box says \"{app['name']}\" and does not carry the pack's "
                        f"name (\"{name}\")")

    gate, note = gate_from_workflow(spec)
    if not note:
        notes.append("no `workflow.steps[].failure_path` to state the invariant — the "
                     "mini-site's figure will carry no note")

    if problems:
        raise DiagramError("\n".join(problems))

    return {
        "slug": clean(dig(spec, "meta.slug", "")) or "pack",
        "pack": name,
        "channel": channel,
        "sources": sources,
        "platform": {"label": label, "services": services},
        "app": app,
        "engine": engine,
        "destinations": destinations,
        "gate": gate,
        "note": note,
        "warnings": notes,
    }


def model_path(spec_path) -> Path:
    """packs/<slug>/architecture.json — beside the pack brief it was built from."""
    return Path(spec_path).resolve().parent / "architecture.json"


def load_or_build(spec: dict, spec_path, channel: str = "partner_print",
                  write: bool = True) -> dict:
    """The reviewed model when the pack has one, otherwise build it and write it.

    The renderers call this: the picture is derived once, and a rebuild of a single
    artifact never redraws it.
    """
    path = model_path(spec_path)
    if path.is_file():
        try:
            model = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(model, dict) and model.get("app"):
                return model
        except (OSError, ValueError):
            pass                            # unreadable: rebuild rather than fail
    model = build_model(spec, channel)
    if write:
        try:
            write_model(model, path)
        except OSError:
            pass                            # a read-only pack folder is not a build failure
    return model


def write_model(model: dict, path) -> Path:
    """Write the model — the documented shape only.

    `warnings` is advice to this build (a layer with no summary, an item that is not
    in the catalog), not part of the contract the renderers read, so it stays out of
    the file rather than becoming an undocumented field three tools have to know.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    stored = {k: v for k, v in model.items() if k != "warnings"}
    path.write_text(json.dumps(stored, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def describe(model: dict) -> str:
    """The diagram in plain sentences — for the review pack and the fit report."""
    out = [f"  box  {model['app']['name']}  (app)",
           f"  box  {model['engine']['name']}  (engine)",
           f"  line {model['platform']['label']}: " + ", ".join(model["platform"]["services"])]
    writeback = {d["name"].lower() for d in model["destinations"] if d["writeback"]}
    for src in model["sources"]:
        mark = "  (write-back)" if src["name"].lower() in writeback else ""
        out.append(f"  box  {src['name']}{mark}")
        out.append(f"  arrow → app  {src['name']}: {src['data']}")
    for dest in model["destinations"]:
        if not dest["writeback"]:
            out.append(f"  box  {dest['name']}  (destination)")
        out.append(f"  arrow app →  {dest['name']}: {dest['data']}")
    if model.get("gate"):
        out.append(f"  gate {model['gate']['name']} — {model['gate']['line']}")
    if model.get("note"):
        out.append(f"  note {model['note']}")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog=PROG, description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", help="packs/<slug>/pack-spec.md")
    ap.add_argument("--out", default=None,
                    help="where to write the model (default: architecture.json beside the spec)")
    ap.add_argument("--channel", default="partner_print",
                    choices=("partner_print", "internal", "site"),
                    help="which name variant the app box carries (default: partner_print)")
    ap.add_argument("--check", action="store_true",
                    help="apply the diagram rules and print the model; write nothing")
    args = ap.parse_args(argv)

    try:
        import yaml  # noqa: F401  (the spec loader needs it)
    except ImportError:
        sys.stderr.write(f"{PROG}: pyyaml is required — "
                         f"pip install -r plugins/oracle-packs/requirements.txt\n")
        return 2
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import packspec  # the one spec loader, beside this file
    try:
        spec, _lines = packspec.load(args.spec)
    except OSError as err:
        sys.stderr.write(f"{PROG}: cannot read {args.spec}: {err}\n")
        return 2
    except packspec.SpecError as err:
        sys.stderr.write(f"{PROG}: the spec does not parse: {err}\n")
        return 2

    try:
        model = build_model(spec, args.channel)
    except DiagramError as err:
        sys.stderr.write(f"{PROG}: the architecture picture cannot be drawn as the "
                         f"pack brief stands:\n")
        for line in str(err).splitlines():
            sys.stderr.write(f"  - {line}\n")
        return 1

    for warning in model.get("warnings") or []:
        print(f"note: {warning}")
    print(describe(model))
    if args.check:
        print(f"{PROG}: the model is valid ({len(model['sources'])} source(s), "
              f"{len(model['destinations'])} destination(s), "
              f"gate: {model['gate']['name'] if model['gate'] else 'none'})")
        return 0
    out = Path(args.out) if args.out else model_path(args.spec)
    write_model(model, out)
    print(f"MODEL {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
