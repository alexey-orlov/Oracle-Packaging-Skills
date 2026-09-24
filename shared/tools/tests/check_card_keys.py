"""Every spec key a card names on its Fills / Reads / Writes line exists in packspec's layout.

    python3 check_card_keys.py <shared/tools> <repo root>

The spec skill writes the brief through `packspec.py set <key.path>`, so a card that names a
key the layout does not know (`hitl` for `human_in_the_loop`, `packages[]` for
`packages.tiers[]`) sends the model to write a field no builder reads. Keys are checked
against packspec.SCHEMA; the listing's and the demo's site keys (`tile.*`, `shared.*`) are
not the spec's and are skipped. Exit 0 clean, 1 with one line per unknown key.
"""
import pathlib, re, sys
tools, root = sys.argv[1], pathlib.Path(sys.argv[2])
sys.path.insert(0, tools)
import packspec
SCHEMA = packspec.SCHEMA
TOPS = set(packspec.TOP_KEYS)

def valid(path: str) -> bool:
    path = re.sub(r"\[[^\]]*\]", "[]", path)          # tiers[pov] is a selector: tiers[]
    prefix = ""
    segs = path.split(".")
    for i, seg in enumerate(segs):
        if seg in ("*", "") or seg.startswith("<"):
            return True
        is_list = seg.endswith("[]")
        key = seg[:-2] if is_list else seg
        fields = SCHEMA.get(prefix)
        if fields is None:                       # below a map or a scalar the layout does not describe
            return True
        if key not in fields:
            return False
        prefix = (prefix + "." if prefix else "") + key + ("[]" if is_list else "")
        other = prefix[:-2] if is_list else prefix + "[]"
        navigated = is_list or i < len(segs) - 1           # the path's shape matters only where it is walked
        if navigated and prefix not in SCHEMA and other in SCHEMA:   # a record walked as a list, or the reverse
            return False
    return True

def expand(token: str):
    m = re.search(r"\{([^}]*)\}", token)
    if not m:
        return [token]
    head, tail = token[:m.start()], token[m.end():]
    return [x for part in m.group(1).split(",") for x in expand(head + part.strip() + tail)]

def looks_like_path(tok: str) -> bool:
    head = re.split(r"[.\[]", tok, 1)[0]
    return head in TOPS                                  # the site's own keys (tile.*, shared.*) are not the spec's

bad = []
cards = sorted(root.glob("plugins/*/skills/*/references/cards/*.md")) + sorted(root.glob("shared/references/anatomy/*.md"))
for card in cards:
    for line in card.read_text(encoding="utf-8").splitlines():
        if not re.search(r"\*\*(Fills|Reads|Writes|Fills / reads|Reads / fills)\b", line):
            continue
        last = None
        for tok in re.findall(r"`([^`]+)`", line):
            tok = tok.strip()
            if "/" in tok or ":" in tok or " " in tok.replace(", ", ",") or tok[:1].isupper() or re.search(r"\.(md|json|yaml|py|js|pptx|docx|html|pdf)$", tok):
                continue
            if looks_like_path(tok):
                for p in expand(tok):
                    if not valid(p):
                        bad.append(f"{card.relative_to(root)}: `{p}`")
                last = tok.rstrip(".*").rstrip(".")
            elif last and re.match(r"^[a-z_]+(\[\])?$", tok) and "/listing/" not in str(card) and "/demo/" not in str(card):
                p = f"{last}.{tok}"
                if not valid(p):
                    bad.append(f"{card.relative_to(root)}: `{tok}` under `{last}`")
print("\n".join(bad) or "every key a card names is in the layout")
sys.exit(1 if bad else 0)
