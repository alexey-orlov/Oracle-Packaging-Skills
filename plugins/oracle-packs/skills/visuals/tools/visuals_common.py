"""Shared plumbing for the visuals tools: the slot list, licence gates, provenance sidecars.

Every tool in this folder imports from here so that the slot list, the allowed licences and the
shape of a provenance record exist in exactly one place. The prose form of all three lives in
`shared/references/visual-assets.md`; when one changes, change both.

Exit codes are the same across every tool in this folder:

    0  did what was asked
    1  usage or input error (bad slot, missing spec key, unknown icon name)
    2  the result was refused on licence grounds (a licence outside the allow-list)
    3  a source could not be reached — DEFERRED, never "nothing found". A network failure is an
       environment limitation, not a fact about the world, and reporting it as "not found" closes
       the item forever on the strength of a timeout.
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

# --------------------------------------------------------------------------------------- exits

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_LICENCE = 2
EXIT_DEFERRED = 3

USER_AGENT = "oracle-packs-visuals/1.0 (+SoftServe accelerator packaging; contact via the pack owner)"
NET_TIMEOUT = 25


class Deferred(Exception):
    """A source could not be reached. Carries the plain sentence the owner should be told."""


class Refused(Exception):
    """A candidate was refused on licence grounds."""


# ---------------------------------------------------------------------------------- the slots

# The pack's picture slots, in the order the skill walks them. `spec_path` is where the choice is
# written in the pack spec; `{i}` is the vertical's zero-based index. Adding a slot is adding a row
# here plus a line in `shared/references/visual-assets.md` — nothing else in the tools is per-slot.
#
# kind:     icon | photo | supplied
#           `supplied` is a file only the owner can give us. It is never searched for and never
#           licence-checked: the right to use it does not come from an open licence at all, it
#           comes from the customer's clearance recorded in the pack brief.
# artifact: which artifact consumes it (for the closing message, and so a future skill can ask for
#           only the slots it needs)
SLOT_KINDS = {
    "vertical": {
        "kind": "icon",
        "spec_path": "verticals[{i}].icon",
        "artifact": "sales deck (the industries slide), later the site",
        "repeats": "one per vertical in the spec",
    },
    "cover": {
        "kind": "photo",
        "spec_path": "deck.images.cover",
        "artifact": "sales deck (the title slide, right half)",
        "repeats": "one",
    },
    "today": {
        "kind": "photo",
        "spec_path": "deck.images.today",
        "artifact": "sales deck (today → tomorrow, left)",
        "repeats": "one",
    },
    "tomorrow": {
        "kind": "photo",
        "spec_path": "deck.images.tomorrow",
        "artifact": "sales deck (today → tomorrow, right)",
        "repeats": "one",
    },
    # The delivered customer's own logo. Owner-supplied, never searched: a company's mark is a
    # trademark, not an openly licensed picture, and the only copy we may use is the one that came
    # with the engagement materials. Asked for only where the pack brief clears the customer's name
    # for some audience; the deck drops the slot on every channel where it does not.
    "customer_logo": {
        "kind": "supplied",
        "spec_path": "deck.images.customer_logo",
        "artifact": "sales deck (the proof slide, and today → tomorrow)",
        "repeats": "one",
    },
    # Reserved, not yet asked for by any builder. Keeping it here means the one-pager step is a
    # spec key away rather than a change to every tool.
    "hero": {
        "kind": "photo",
        "spec_path": "one_pager.images.hero",
        "artifact": "sales one-pager (the banner)",
        "repeats": "one",
    },
}

SLOT_RE = re.compile(r"^(?P<base>[a-z_]+)(?::(?P<index>\d+))?$")


def parse_slot(slot: str) -> tuple[str, int | None]:
    """'vertical:2' -> ('vertical', 2); 'today' -> ('today', None). Raises ValueError on junk."""
    m = SLOT_RE.match(slot or "")
    if not m or m.group("base") not in SLOT_KINDS:
        raise ValueError(
            f"unknown slot {slot!r}. Known slots: "
            + ", ".join(sorted(SLOT_KINDS)) + " (verticals are numbered: vertical:0, vertical:1 ...)"
        )
    base = m.group("base")
    idx = int(m.group("index")) if m.group("index") is not None else None
    if base == "vertical" and idx is None:
        raise ValueError("a vertical slot needs its number, e.g. vertical:0 for the first industry")
    if base != "vertical" and idx is not None:
        raise ValueError(f"slot {base!r} is not numbered")
    return base, idx


def slot_kind(slot: str) -> str:
    base, _ = parse_slot(slot)
    return SLOT_KINDS[base]["kind"]


def slot_spec_path(slot: str) -> str:
    base, idx = parse_slot(slot)
    return SLOT_KINDS[base]["spec_path"].replace("{i}", str(idx))


# ------------------------------------------------------------------------------------- licences

# Photos: only licences that permit commercial use without attribution, and only where the licence
# and the creator are recorded per file. Everything else is refused, including CC-BY: a CC-BY photo
# obliges the artifact to print a credit line, and a sales deck will not carry one.
PHOTO_LICENCES = {
    "cc0": {
        "name": "CC0 1.0",
        "url": "https://creativecommons.org/publicdomain/zero/1.0/",
        "attribution_required": False,
    },
    "pdm": {
        "name": "Public Domain Mark",
        "url": "https://creativecommons.org/publicdomain/mark/1.0/",
        "attribution_required": False,
    },
    "pexels": {
        "name": "Pexels License",
        "url": "https://www.pexels.com/license/",
        "attribution_required": False,
    },
    "unsplash": {
        "name": "Unsplash License",
        "url": "https://unsplash.com/license",
        "attribution_required": False,
    },
}

# Icons: permissive open-source sets only. No CC-BY sets (they would put an attribution line on the
# slide) and never a vendor's logo used as an icon.
ICON_LICENCES = {
    "mit": {"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    "isc": {"name": "ISC", "url": "https://opensource.org/licenses/ISC"},
}

ICON_SETS = {
    "tabler": {
        "licence": "mit",
        "png": "https://cdn.jsdelivr.net/npm/@tabler/icons-png/icons/outline/{name}.png",
        "svg": "https://raw.githubusercontent.com/tabler/tabler-icons/main/icons/outline/{name}.svg",
        "page": "https://tabler.io/icons/icon/{name}",
        "credit": "Tabler Icons",
    },
    "lucide": {
        "licence": "isc",
        "png": None,
        "svg": "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/{name}.svg",
        "page": "https://lucide.dev/icons/{name}",
        "credit": "Lucide",
    },
}


# A `supplied` file has no licence to look up. What stands in its record instead: where it came
# from, and the thing that actually permits the use — the customer's clearance in the pack brief.
SUPPLIED_SOURCE = "supplied by the owner from the engagement materials"
SUPPLIED_TERMS = "used under the customer's clearance recorded in the pack brief"


def check_photo_licence(code: str) -> dict:
    code = (code or "").strip().lower()
    if code not in PHOTO_LICENCES:
        raise Refused(
            f"licence {code!r} is not one this bundle may use. Allowed: "
            + ", ".join(sorted(PHOTO_LICENCES))
            + " — every other licence either forbids commercial use or obliges the artifact to "
              "print a credit line."
        )
    return PHOTO_LICENCES[code]


# ---------------------------------------------------------------------------------- provenance

def provenance_record(**kw) -> dict:
    """The sidecar every downloaded candidate carries. Missing values are '-' so a credits line is
    never silently short."""
    rec = {
        "slot": kw.get("slot") or "-",
        "kind": kw.get("kind") or "-",
        "file": kw.get("file") or "-",
        "title": kw.get("title") or "-",
        "creator": kw.get("creator") or "-",
        "creator_url": kw.get("creator_url") or "-",
        "source": kw.get("source") or "-",
        "source_url": kw.get("source_url") or "-",      # the page a human can open
        "download_url": kw.get("download_url") or "-",  # the bytes we fetched
        "licence": kw.get("licence") or "-",
        "licence_name": kw.get("licence_name") or "-",
        "licence_url": kw.get("licence_url") or "-",
        "attribution_required": bool(kw.get("attribution_required", False)),
        "terms": kw.get("terms") or "-",
        "width": kw.get("width") or 0,
        "height": kw.get("height") or 0,
        "fetched": kw.get("fetched") or _dt.date.today().isoformat(),
        "note": kw.get("note") or "",
    }
    return rec


def write_sidecar(image_path: str, rec: dict) -> str:
    side = os.path.splitext(image_path)[0] + ".json"
    with open(side, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return side


def read_sidecar(path: str) -> dict:
    """Accepts either the .json sidecar or the image beside it."""
    if path.lower().endswith(".json"):
        side = path
    else:
        side = os.path.splitext(path)[0] + ".json"
    if not os.path.exists(side):
        raise FileNotFoundError(
            f"no provenance beside {path} — every picture this bundle uses carries a recorded "
            "licence; a file with none cannot be applied."
        )
    with open(side, encoding="utf-8") as fh:
        return json.load(fh)


def credits_line(rec: dict) -> str:
    """One markdown row for packs/<slug>/visuals/credits.md."""
    lic = rec.get("licence_name") or rec.get("licence") or "-"
    return "| `{file}` | {slot} | {source} | {creator} | {lic} | {url} | {date} |".format(
        file=os.path.basename(rec.get("file", "-")),
        slot=rec.get("slot", "-"),
        source=rec.get("source", "-"),
        creator=rec.get("creator", "-"),
        lic=lic,
        url=rec.get("source_url", "-"),
        date=rec.get("fetched", "-"),
    )


CREDITS_HEADER = (
    "# Picture credits\n"
    "\n"
    "Every picture in this pack, where it came from and under what licence. Written by the\n"
    "`/oracle-packs:visuals` step, one row per chosen file. Kept even where the licence asks for no\n"
    "attribution: the record is what lets anyone re-check the right to use a file later.\n"
    "\n"
    "| File | Slot | Source | Creator | Licence | Page | Chosen |\n"
    "|---|---|---|---|---|---|---|\n"
)


# ------------------------------------------------------------------------------------- network

def http_get(url: str, headers: dict | None = None, timeout: int = NET_TIMEOUT) -> bytes:
    """GET with the bundle's user agent. Raises Deferred on anything that is the network's fault."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            raise Deferred(f"{url} refused the request ({exc.code}) — it needs a key we do not have here.")
        if exc.code == 404:
            raise FileNotFoundError(f"{url} — not there (404).")
        if exc.code == 429:
            raise Deferred(f"{url} rate-limited us (429). Try again in a few minutes.")
        raise Deferred(f"{url} answered {exc.code}.")
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise Deferred(f"could not reach {urllib.parse.urlparse(url).netloc}: {exc}")


def http_json(url: str, headers: dict | None = None) -> dict:
    raw = http_get(url, headers=headers)
    try:
        return json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as exc:
        raise Deferred(f"{urllib.parse.urlparse(url).netloc} did not answer with JSON: {exc}")


def keychain(service: str) -> str | None:
    """A key by name: the environment variable of that name when it is set and non-empty, else —
    on macOS only — the Keychain entry of that name (`security find-generic-password -s <name>`).
    Returns None when neither has it — never raises, and never prints the value."""
    value = (os.environ.get(service) or "").strip()
    if value:
        return value
    if sys.platform != "darwin":
        return None
    try:
        out = subprocess.run(
            ["security", "find-generic-password", "-s", service, "-w"],
            capture_output=True, text=True, timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    key = out.stdout.strip()
    return key or None


# --------------------------------------------------------------------------------------- misc

def slugify(text: str, limit: int = 48) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return (s[:limit].rstrip("-")) or "untitled"


def eprint(*a) -> None:
    print(*a, file=sys.stderr)


def die(msg: str, code: int = EXIT_USAGE) -> None:
    eprint(msg)
    sys.exit(code)


def packspec_module():
    """The one spec loader, shared/tools/packspec.py: the plugin's own.

    Imported here, on first use, so the tools that do not read a spec need no PyYAML."""
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


def load_spec(path: str) -> dict:
    """The spec's data, read through packspec.py. A spec that does not parse exits 1 with its line."""
    packspec = packspec_module()
    try:
        data, _lines = packspec.load(path)
    except packspec.SpecError as err:
        die("the spec does not parse: %s" % err)
    return data


def pack_dir(spec_path: str) -> str:
    """The pack folder is the spec's own folder — packs/<slug>/pack-spec.md."""
    return os.path.dirname(os.path.abspath(spec_path))
