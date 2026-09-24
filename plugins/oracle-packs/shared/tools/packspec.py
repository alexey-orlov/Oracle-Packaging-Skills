#!/usr/bin/env python3
"""The pack spec: one Markdown file per pack, one loader, one writer.

    from packspec import load, dump, save, SpecError
    data, linemap = load("packs/<slug>/pack-spec.md")
    text = dump(data)                    # the canonical Markdown for that data
    save(path, data)                     # written atomically, only when the round trip is exact
    data_sha(path)                       # what the artifact stamp hashes: the sorted JSON of
                                         # the data, so a re-render never changes it

`data` is exactly the dict `yaml.safe_load` returns for the same spec written in YAML, so no
builder changes; `linemap` maps key paths to the line each was written on, for lint
messages: `linemap[("kpis", 0, "figure")]` is that key's line, `linemap[()]` the spec's first
line, `linemap.starts[path]` where a mapping or list value begins. Every tool reads a spec
through `load`; none keeps its own parser.

The contract
    lossless    load(dump(d)) == d, for every spec
    canonical   dump(load(md)) == md for every file the writer produced; a hand-edited file
                that parses re-renders without changing its data
    strict      a structural slip — a row with a cell too many or too few, an unknown
                section or label, a malformed price — is a SpecError carrying the file's
                line; the loader never guesses
    kept        a key the layout does not know is kept: a table grows a column for it;
                anywhere else it goes to the fenced YAML block under `## Other fields`

The layout (the LAYOUT part of this file is its one declaration)
    front matter   slug, status, spec_version, generated_with, roadmap_item_id, roadmap_block
    # <name>       then the name variants and the name's source, as key lines
    ## sections    One-liner · Problem and solution · Who buys it · Industries · Capabilities ·
                   Workflow · Architecture · Oracle products · Metrics · Packages · Proof ·
                   Next steps · Open questions · Settings · Other fields
    forms          `- **Label:** value` key lines (nested two spaces a level), tables with fixed
                   columns, one `###` heading per record, paragraphs, a fenced YAML block

Values
    text           verbatim. A backslash before punctuation is that character (`\\<`, `\\|`,
                   `\\#`), as on GitHub; a line ending in one backslash ends in a line break.
                   Multi-line text keeps its lines.
    —              null            (none)   an empty list        an empty cell   key absent
    yes / no       a boolean, where the layout types the key as one
    `...`          one code span holding a YAML value — for what a slot's own syntax cannot
                   say: the number 26 in a text field, trailing spaces, a date kept as text
    a; b; c        a short list, on a key line or in a cell; a longer one is nested bullets
    price          €90K · confirmed · <footnote> · €300K–€500K · indicative · to be defined
    duration       6–8 weeks (target 8, hard cap 10) · to be defined

The command line
    packspec.py get <spec> <key.path>             the value, as JSON
    packspec.py set <spec> <key.path> <value> [--source <src>]
                                                  JSON when the value parses as JSON, else a
                                                  string; a typed key (date, price, duration,
                                                  yes/no, list) also takes its own syntax.
                                                  --source sets the key's sibling `source`
                                                  (for meta.name: meta.name_source). The
                                                  first set on a path with no spec creates it
    packspec.py check <spec>                      parses, re-renders, names each line that is
                                                  not canonical and each key the layout does
                                                  not know

    A key path: meta.name · packages.tiers[0].services_price · packages.tiers[pov].name — a
    bracket holds an index, or the id / name / area / layer / n of a list item; quote a key
    with dots in it: kpis["Time to act"].figure

Exit codes: 0 done · 1 a finding (does not parse, not canonical, an unknown key, a round
trip that is not exact, no value at that path) · 2 usage error.

Dependencies: PyYAML.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import decimal
import difflib
import hashlib
import json
import os
import re
import sys
import tempfile

PROG = "packspec"


# ============================================================================ errors, lines
class SpecError(Exception):
    """The spec does not parse, or does not have the pack-spec shape. Carries the line."""

    def __init__(self, message: str, line: int | None = None, source: str | None = None):
        Exception.__init__(self, message)
        self.message = message
        self.line = line
        self.source = source

    def __str__(self) -> str:
        where = self.source or "<spec>"
        if self.line:
            return "%s:%d: %s" % (where, self.line, self.message)
        return "%s: %s" % (where, self.message)


class LineMap(dict):
    """path tuple -> line of that key (or list item); `.starts[path]` -> where a container value begins."""

    def __init__(self, *a, **kw):
        dict.__init__(self, *a, **kw)
        self.starts = {}

    def line(self, path, default: int = 1) -> int:
        """The line of `path`, else of its nearest ancestor that has one."""
        path = tuple(path)
        while True:
            if path in self:
                return self[path]
            if not path:
                return default
            path = path[:-1]


class Misfit(Exception):
    """A value its slot cannot hold. The writer then takes the next form down."""


def _yaml():
    try:
        import yaml  # noqa: F401
    except ImportError:
        raise SpecError("PyYAML is required to read a pack spec — run the tool through "
                        "shared/tools/py, which finds or provisions an interpreter that has it")
    return sys.modules["yaml"]


# ============================================================================ YAML
def loads_yaml(text: str, source: str = "<string>", offset: int = 0):
    """(data, linemap) of YAML text, lines shifted by `offset`. `data` equals yaml.safe_load(text)."""
    yaml = _yaml()

    class _Loader(yaml.SafeLoader):
        pass

    key_lines = {}   # id(container) -> {key or index: line}
    starts = {}      # id(container) -> line where the container node begins

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        out = {}
        starts[id(out)] = node.start_mark.line + 1 + offset
        lines = key_lines.setdefault(id(out), {})
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=True)
            try:
                hash(key)
            except TypeError:
                raise SpecError("a mapping key that is itself a list or a mapping",
                                key_node.start_mark.line + 1 + offset, source)
            out[key] = loader.construct_object(value_node, deep=True)
            lines[key] = key_node.start_mark.line + 1 + offset
        return out

    def construct_sequence(loader, node):
        out = []
        starts[id(out)] = node.start_mark.line + 1 + offset
        lines = key_lines.setdefault(id(out), {})
        for i, child in enumerate(node.value):
            out.append(loader.construct_object(child, deep=True))
            lines[i] = child.start_mark.line + 1 + offset
        return out

    _Loader.add_constructor("tag:yaml.org,2002:map", construct_mapping)
    _Loader.add_constructor("tag:yaml.org,2002:seq", construct_sequence)

    try:
        data = yaml.load(text, Loader=_Loader)
    except SpecError:
        raise
    except yaml.MarkedYAMLError as exc:
        mark = exc.problem_mark or exc.context_mark
        raise SpecError("not readable YAML: %s" % (exc.problem or exc),
                        mark.line + 1 + offset if mark else None, source)
    except yaml.YAMLError as exc:
        raise SpecError("not readable YAML: %s" % exc, None, source)

    linemap = LineMap()
    linemap[()] = starts.get(id(data), 1 + offset)
    linemap.starts[()] = linemap[()]

    def walk(value, path):
        lines = key_lines.get(id(value), {})
        if isinstance(value, dict):
            items = value.items()
        elif isinstance(value, list):
            items = enumerate(value)
        else:
            return
        for k, v in items:
            p = path + (k,)
            linemap[p] = lines.get(k, linemap[path])
            if isinstance(v, (dict, list)):
                linemap.starts[p] = starts.get(id(v), linemap[p])
                walk(v, p)

    walk(data, ())
    return data, linemap


_DUMPER = []


def _dumper():
    """A SafeDumper that never writes an anchor: a value the data holds twice is written twice."""
    if not _DUMPER:
        yaml = _yaml()

        class _NoAliases(yaml.SafeDumper):
            def ignore_aliases(self, data):
                return True

        _DUMPER.append(_NoAliases)
    return _DUMPER[0]


def _flow(value) -> str:
    """One value as single-line YAML flow text."""
    yaml = _yaml()
    text = yaml.dump([value], Dumper=_dumper(), default_flow_style=True, allow_unicode=True,
                     width=float("inf"), sort_keys=False).strip()
    if not (text.startswith("[") and text.endswith("]")) or "\n" in text:
        raise Misfit("no single-line YAML for this value")
    return text[1:-1]


# ============================================================================ key paths
_BARE_SEGMENT = re.compile(r'^[^.\[\]"{}\s](?:[^.\[\]"{}\n]*[^.\[\]"{}\s])?\Z')


def _segment(key) -> str:
    if isinstance(key, str):
        return key if _BARE_SEGMENT.match(key) else json.dumps(key, ensure_ascii=False)
    return "{" + _flow(key) + "}"


def format_path(path, key=None, has_key=False) -> str:
    """("workflow", "steps", 3) + "approve" -> 'workflow.steps[3].approve'. Ints in `path`
    are list positions; `key`, when given, is the last dict key (any type)."""
    out = ""
    for seg in path:
        if isinstance(seg, int) and not isinstance(seg, bool):
            out += "[%d]" % seg
        else:
            out += ("." if out else "") + _segment(seg)
    if has_key:
        out += ("." if out else "") + _segment(key)
    return out


def parse_path(text: str):
    """'packages.tiers[0].name' -> [("key", "packages"), ("key", "tiers"), ("index", 0),
    ("key", "name")]. A non-number bracket is ("select", text); `{…}` is a non-text key."""
    segs, i, n = [], 0, len(text)
    expect_key = True
    while i < n:
        c = text[i]
        if c == ".":
            if expect_key or i + 1 >= n:
                raise ValueError("a key path with an empty segment: %r" % text)
            expect_key = True
            i += 1
            continue
        if c == "[":
            if not segs:
                raise ValueError("a key path starts with a key: %r" % text)
            j = i + 1
            if j < n and text[j] == '"':
                k = j + 1
                while k < n and text[k] != '"':
                    k += 2 if text[k] == "\\" else 1
                sel = json.loads(text[j:k + 1])
                j = k + 1
            else:
                k = text.find("]", j)
                if k < 0:
                    raise ValueError("an unclosed [ in the key path %r" % text)
                sel = text[j:k]
                j = k
            if j >= n or text[j] != "]":
                raise ValueError("an unclosed [ in the key path %r" % text)
            if isinstance(sel, str) and re.fullmatch(r"\d+", sel):
                segs.append(("index", int(sel)))
            else:
                segs.append(("select", sel))
            i = j + 1
            expect_key = False
            continue
        if not expect_key:
            raise ValueError("a key must follow a dot: %r" % text)
        if c == '"':
            k = i + 1
            while k < n and text[k] != '"':
                k += 2 if text[k] == "\\" else 1
            segs.append(("key", json.loads(text[i:k + 1])))
            i = k + 1
        elif c == "{":
            k = text.find("}", i)
            if k < 0:
                raise ValueError("an unclosed { in the key path %r" % text)
            segs.append(("key", _yaml().safe_load(text[i + 1:k])))
            i = k + 1
        else:
            k = i
            while k < n and text[k] not in ".[":
                k += 1
            segs.append(("key", text[i:k]))
            i = k
        expect_key = False
    if expect_key:
        raise ValueError("an empty key path, or one that ends with a dot: %r" % text)
    return segs


# ============================================================================ scalars
DASH = "—"                  # null
NONE = "(none)"             # an empty list
TBD = "to be defined"
PART = " · "                # the parts of a price; a tier's name and size
RANGE = "–"                 # the en dash of a range

_PUNCT = set("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
_HATCH_RE = re.compile(r"^`([^`\n]+)`\Z")
_WORD_RE = re.compile(r"^[a-z][a-z0-9_-]*\Z")
_CONTROL_RE = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")
_THEMATIC_RE = re.compile(r"^[-=*_](?:\s*[-=*_]){2,}\s*$")
_ORDERED_RE = re.compile(r"^(\d+)([.)])(\s|$)")

TEXT, BOOL, INT, NUM, DATE, MONEY, DURATION, LIST, TLIST = (
    "text", "bool", "int", "num", "date", "money", "duration", "list", "tlist")
RECORD, MAP, PAIRS, RECORDS = "record", "map", "pairs", "records"
SCALAR_KINDS = (TEXT, BOOL, INT, NUM, DATE, MONEY, DURATION)


def _is_scalar(v) -> bool:
    return v is None or isinstance(v, (str, bool, int, float, _dt.date))


def _hatch(value) -> str:
    """A scalar as one code span holding its YAML."""
    if not _is_scalar(value) or (isinstance(value, float) and value != value):
        raise Misfit("no code span for this value")
    inner = _flow(value)
    if "`" in inner or not inner.strip() or inner != inner.strip():
        raise Misfit("no code span for this value")
    back = _yaml().safe_load(inner)
    if back != value or type(back) is not type(value):
        raise Misfit("the code span does not read back")
    return "`" + inner + "`"


def _unhatch(inner: str, line, source):
    try:
        value = _yaml().safe_load(inner)
    except Exception as exc:  # yaml.YAMLError and its kin
        raise SpecError("the code span `%s` is not a readable value: %s" % (inner, exc), line, source)
    if not _is_scalar(value):
        raise SpecError("the code span `%s` holds a list or a mapping — write those as bullets, "
                        "or in the Other fields block" % inner, line, source)
    return value


def _esc_inline(s: str, cell: bool = False) -> str:
    """Escape one line of text: a backslash before punctuation, `<`, and `|` in a table cell."""
    out = []
    n = len(s)
    for i, c in enumerate(s):
        if c == "\\":
            nxt = s[i + 1] if i + 1 < n else ""
            if not nxt:
                raise Misfit("a line that ends in a backslash")
            out.append("\\\\" if nxt in _PUNCT else "\\")
        elif c == "<":
            out.append("\\<")
        elif c == "|" and cell:
            out.append("\\|")
        else:
            out.append(c)
    return "".join(out)


def _unesc_inline(s: str) -> str:
    out, i, n = [], 0, len(s)
    while i < n:
        c = s[i]
        if c == "\\" and i + 1 < n and s[i + 1] in _PUNCT:
            out.append(s[i + 1])
            i += 2
        else:
            out.append(c)
            i += 1
    return "".join(out)


def _lead_escape(line: str, item: bool = False) -> str:
    """Escape an (already inline-escaped) line whose start would read as structure."""
    if not line:
        return line
    c = line[0]
    if c in "#>|" or line.startswith(("```", "~~~")) or _THEMATIC_RE.match(line):
        return "\\" + line
    if c in "-*+" and (len(line) == 1 or line[1] in " \t"):
        return "\\" + line
    m = _ORDERED_RE.match(line)
    if m:
        return m.group(1) + "\\" + line[len(m.group(1)):]
    if item and line.startswith("**"):
        return "\\" + line
    return line


def _check_line_text(s: str):
    if s != s.strip() or _CONTROL_RE.search(s):
        raise Misfit("edge spaces or control characters")


def _enc_text_line(s: str, ctx: str) -> str:
    """One text value on one line (ctx: keyval | item | cell | title)."""
    if not isinstance(s, str) or s == "":
        raise Misfit("empty text")
    if "\n" in s or "\r" in s:
        raise Misfit("a line break")
    _check_line_text(s)
    if s == DASH:
        raise Misfit("the null mark as text")
    line = _esc_inline(s, cell=(ctx == "cell"))
    if s == NONE:
        return "\\" + line
    if len(line) >= 2 and line.startswith("`") and line.endswith("`"):
        return "\\" + line
    if ctx == "item":
        return _lead_escape(line, item=True)
    return line


def _enc_text_lines(s: str, ctx: str):
    """A text value as one or more lines (ctx: keyval | item | para). Raises Misfit when it
    cannot be written that way; the caller then uses a code span."""
    if not isinstance(s, str) or s == "":
        raise Misfit("empty text")
    if "\r" in s:
        raise Misfit("a carriage return")
    trailing = s.endswith("\n")
    body = s[:-1] if trailing else s
    if body == "" or body.endswith("\n") or body.startswith("\n"):
        raise Misfit("blank lines at an edge")
    lines = body.split("\n")
    if len(lines) == 1 and not trailing:
        if ctx == "para":
            raw = _enc_text_line(s, "keyval")
            return [raw if raw.startswith("\\") else _lead_escape(raw)]
        return [_enc_text_line(s, ctx)]
    out = []
    for i, ln in enumerate(lines):
        if ln == "":
            out.append("")
            continue
        _check_line_text(ln)
        esc = _esc_inline(ln)
        if i == 0 and ctx == "keyval":
            out.append(esc)
        else:
            out.append(_lead_escape(esc, item=(i == 0 and ctx == "item")))
    if trailing:
        out[-1] += "\\"
    return out


def _has_break_mark(line: str) -> bool:
    return (len(line) - len(line.rstrip("\\"))) % 2 == 1


def _dec_text_lines(lines) -> str:
    """The inverse of _enc_text_lines for two or more lines, or one with a trailing break."""
    lines = list(lines)
    trailing = _has_break_mark(lines[-1])
    if trailing:
        lines[-1] = lines[-1][:-1]
    return "\n".join(_unesc_inline(ln) for ln in lines) + ("\n" if trailing else "")


# -- numbers, prices, durations
def _fmt_num(n) -> str:
    if isinstance(n, bool) or not isinstance(n, (int, float)):
        raise Misfit("not a number")
    if isinstance(n, float):
        text = repr(n)
        if not re.fullmatch(r"-?\d+\.\d+", text):
            raise Misfit("a number this layout does not write plainly")
        return text
    return str(n)


def _parse_num(text: str):
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    if re.fullmatch(r"-?\d+\.\d+", text):
        return float(text)
    return None


_CURRENCY_SYMBOL = {"EUR": "€", "USD": "$", "GBP": "£"}
_SYMBOL_CURRENCY = {v: k for k, v in _CURRENCY_SYMBOL.items()}
_AMOUNT_RE = re.compile(r"^(?:(?P<sym>[€$£])|(?P<code>[A-Z]{3}) )?"
                        r"(?P<num>\d{1,3}(?:,\d{3})+|\d+)(?:\.(?P<frac>\d+))?(?P<mult>[KM])?$")


def _fmt_amount(n, currency) -> str:
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise Misfit("a price that is not a whole, non-negative number")
    if currency is None:
        sym = ""
    elif isinstance(currency, str) and currency in _CURRENCY_SYMBOL:
        sym = _CURRENCY_SYMBOL[currency]
    elif isinstance(currency, str) and re.fullmatch(r"[A-Z]{3}", currency):
        sym = currency + " "
    else:
        raise Misfit("a currency that is not a three-letter code")
    d = decimal.Decimal(n)
    if n >= 1_000_000 and n % 10_000 == 0:
        num = format((d / decimal.Decimal(1_000_000)).normalize(), "f") + "M"
    elif n >= 1000 and n % 100 == 0:
        num = format((d / decimal.Decimal(1000)).normalize(), "f") + "K"
    elif n < 1000:
        num = str(n)
    else:
        num = "{:,}".format(n)
    return sym + num


def _parse_amount(text: str):
    """'€300K' -> (300000, 'EUR'); None when it is not an amount."""
    m = _AMOUNT_RE.match(text)
    if not m:
        return None
    if "," in m.group("num") and (m.group("mult") or m.group("frac")):
        return None
    d = decimal.Decimal(m.group("num").replace(",", "") +
                        ("." + m.group("frac") if m.group("frac") else ""))
    if m.group("mult") == "K":
        d *= 1000
    elif m.group("mult") == "M":
        d *= 1_000_000
    if d != d.to_integral_value():
        return None
    currency = _SYMBOL_CURRENCY.get(m.group("sym")) if m.group("sym") else m.group("code")
    return int(d), currency


_MONEY_KEYS = {"value", "range", "currency", "status", "footnote"}


def _fmt_money(m) -> str:
    if not isinstance(m, dict) or not m or not set(m) <= _MONEY_KEYS:
        raise Misfit("not a price mapping")
    status = m.get("status")
    if "status" in m and not (isinstance(status, str) and _WORD_RE.match(status)):
        raise Misfit("a price status that is not one word")
    foot = ""
    if "footnote" in m:
        foot = PART + _enc_text_line(m["footnote"], "keyval")
    if "value" in m and "range" in m:
        raise Misfit("a price with both a value and a range")
    if "value" not in m and "range" not in m:
        if status != "tbd" or "currency" in m:
            raise Misfit("a price with no amount that is not to be defined")
        return TBD + foot
    if "status" not in m:
        raise Misfit("a price with no status")
    currency = m.get("currency")
    if "currency" in m and currency is None:
        raise Misfit("a null currency")
    if "value" in m:
        amount = _fmt_amount(m["value"], currency)
    else:
        rng = m["range"]
        if not isinstance(rng, list) or len(rng) != 2:
            raise Misfit("a range that is not two numbers")
        amount = _fmt_amount(rng[0], currency) + RANGE + _fmt_amount(rng[1], currency)
    return amount + PART + status + foot


def _parse_money(raw: str):
    """The inverse of _fmt_money; None when the text is not a price."""
    head, sep, rest = raw.partition(PART)
    if head == TBD:
        out = {"status": "tbd"}
        if sep:
            if not rest:
                return None
            out["footnote"] = _unesc_inline(rest)
        return out
    if not sep:
        return None
    status, sep2, footnote = rest.partition(PART)
    if not _WORD_RE.match(status):
        return None
    if RANGE in head:
        lo_text, _, hi_text = head.partition(RANGE)
        lo, hi = _parse_amount(lo_text), _parse_amount(hi_text)
        if lo is None or hi is None or lo[1] != hi[1]:
            return None
        out = {"range": [lo[0], hi[0]]}
        currency = lo[1]
    else:
        amount = _parse_amount(head)
        if amount is None:
            return None
        out = {"value": amount[0]}
        currency = amount[1]
    if currency is not None:
        out["currency"] = currency
    out["status"] = status
    if sep2:
        if not footnote:
            return None
        out["footnote"] = _unesc_inline(footnote)
    return out


_DURATION_KEYS = {"min", "max", "target", "hard_cap", "status", "justification"}
_DURATION_RE = re.compile(r"^(?P<min>-?\d+(?:\.\d+)?)" + RANGE + r"(?P<max>-?\d+(?:\.\d+)?) weeks"
                          r"(?: \((?P<extras>.+)\))?$")


def _fmt_duration(d) -> str:
    if not isinstance(d, dict) or not d or not set(d) <= _DURATION_KEYS:
        raise Misfit("not a duration mapping")
    if set(d) == {"status"} and d["status"] == "tbd":
        return TBD
    if "min" not in d or "max" not in d:
        raise Misfit("a duration without min and max")
    head = "%s%s%s weeks" % (_fmt_num(d["min"]), RANGE, _fmt_num(d["max"]))
    extras = []
    if "target" in d:
        extras.append("target " + _fmt_num(d["target"]))
    if "hard_cap" in d:
        extras.append("hard cap " + _fmt_num(d["hard_cap"]))
    if "status" in d:
        if not (isinstance(d["status"], str) and _WORD_RE.match(d["status"])):
            raise Misfit("a duration status that is not one word")
        extras.append("status " + d["status"])
    if "justification" in d:
        extras.append("justification: " + _enc_text_line(d["justification"], "keyval"))
    return head + (" (" + ", ".join(extras) + ")" if extras else "")


def _parse_duration(raw: str):
    if raw == TBD:
        return {"status": "tbd"}
    m = _DURATION_RE.match(raw)
    if not m:
        return None
    out = {"min": _parse_num(m.group("min")), "max": _parse_num(m.group("max"))}
    rest = m.group("extras") or ""
    while rest:
        if rest.startswith("justification: "):
            text = rest[len("justification: "):]
            if not text:
                return None
            out["justification"] = _unesc_inline(text)
            break
        item, sep, rest = rest.partition(", ")
        if sep and not rest:
            return None
        mt = re.fullmatch(r"(target|hard cap|status) (\S+)", item)
        if not mt:
            return None
        key = {"target": "target", "hard cap": "hard_cap", "status": "status"}[mt.group(1)]
        if key in out:
            return None
        if key == "status":
            if not _WORD_RE.match(mt.group(2)):
                return None
            out[key] = mt.group(2)
        else:
            num = _parse_num(mt.group(2))
            if num is None:
                return None
            out[key] = num
    return out


def _fmt_inline_list(items, ctx: str, limit=None) -> str:
    """`a; b; c`, or Misfit when an item cannot sit on one line between semicolons. `limit`
    caps the summed length of the items (the preview's rule for a short list)."""
    if not isinstance(items, list) or not items:
        raise Misfit("not a non-empty list")
    out = []
    for item in items:
        if not isinstance(item, str) or not item or ";" in item or "\n" in item or "\r" in item:
            raise Misfit("an item that cannot sit on one line")
        _check_line_text(item)
        out.append(_esc_inline(item, cell=(ctx == "cell")))
    if limit is not None and sum(len(x) for x in items) > limit:
        raise Misfit("a list too long for one line")
    text = "; ".join(out)
    if text == DASH:
        raise Misfit("a one-item list that reads as null")
    if text == NONE or _HATCH_RE.match(text):
        text = "\\" + text
    return text


def enc_scalar(value, kind: str, ctx: str) -> str:
    """One value as the single-line text of a slot of `kind` (ctx: keyval | item | cell | title)."""
    if value is None:
        return DASH
    if isinstance(value, list) and not value:
        return NONE
    if kind == LIST:
        if isinstance(value, list):
            return _fmt_inline_list(value, ctx)
        return _hatch(value)
    if kind == MONEY:
        return _fmt_money(value) if isinstance(value, dict) else _hatch(value)
    if kind == DURATION:
        return _fmt_duration(value) if isinstance(value, dict) else _hatch(value)
    if isinstance(value, (list, dict)):
        raise Misfit("a list or a mapping in a one-value slot")
    if kind == BOOL:
        return ("yes" if value else "no") if isinstance(value, bool) else _hatch(value)
    if kind == INT:
        if isinstance(value, int) and not isinstance(value, bool):
            return str(value)
        return _hatch(value)
    if kind == NUM:
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            try:
                return _fmt_num(value)
            except Misfit:
                pass
        return _hatch(value)
    if kind == DATE:
        if isinstance(value, _dt.date) and not isinstance(value, _dt.datetime):
            return value.isoformat()
        return _hatch(value)
    if isinstance(value, str):
        try:
            return _enc_text_line(value, ctx)
        except Misfit:
            return _hatch(value)
    return _hatch(value)


def dec_scalar(raw: str, kind: str, line, source, what: str = "value"):
    """The inverse of enc_scalar."""
    if raw == DASH:
        return None
    if raw == NONE:
        return []
    m = _HATCH_RE.match(raw)
    if m:
        return _unhatch(m.group(1), line, source)
    if kind == LIST:
        return [_unesc_inline(item) for item in raw.split("; ")]
    if kind == BOOL:
        if raw in ("yes", "no"):
            return raw == "yes"
        raise SpecError("%s: `%s` is not yes or no" % (what, raw), line, source)
    if kind == INT:
        if re.fullmatch(r"-?\d+", raw):
            return int(raw)
        raise SpecError("%s: `%s` is not a whole number" % (what, raw), line, source)
    if kind == NUM:
        num = _parse_num(raw)
        if num is None:
            raise SpecError("%s: `%s` is not a number" % (what, raw), line, source)
        return num
    if kind == DATE:
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw):
            try:
                return _dt.date.fromisoformat(raw)
            except ValueError:
                pass
        raise SpecError("%s: `%s` is not a date (YYYY-MM-DD)" % (what, raw), line, source)
    if kind == MONEY:
        out = _parse_money(raw)
        if out is None:
            raise SpecError("%s: `%s` is not a price — write €90K · <status> [· <footnote>], "
                            "€300K–€500K · <status>, or to be defined [· <footnote>]"
                            % (what, raw), line, source)
        return out
    if kind == DURATION:
        out = _parse_duration(raw)
        if out is None:
            raise SpecError("%s: `%s` is not a duration — write 6–8 weeks (target 8, hard cap "
                            "10), or to be defined" % (what, raw), line, source)
        return out
    return _unesc_inline(raw)


# ============================================================================ LAYOUT
class F:
    """One field: a key, its label, and how its value is written."""

    def __init__(self, key, label, kind=TEXT, rec=None, pair=None):
        self.key, self.label, self.kind = key, label, kind
        self.rec = rec          # kind record | records: the nested record type
        self.pair = pair        # kind pairs: (first key, second key)


class Rec:
    """An ordered set of fields, looked up by key or by label."""

    def __init__(self, *fields):
        self.fields = list(fields)
        self.by_key = {f.key: f for f in fields}
        self.by_label = {f.label: f for f in fields}
        assert len(self.by_key) == len(fields) and len(self.by_label) == len(fields), fields

    def keys(self):
        return [f.key for f in self.fields]


def _tiers(prefix=""):
    return Rec(F("pov", prefix + "PoV"), F("integration", prefix + "Integration"),
               F("scaling", prefix + "Scaling"))


BY_TIER = _tiers()
AT_TIER = _tiers("At ")
LEVEL_AT = _tiers("Level at ")
GLYPH_AT = _tiers("Glyph at ")

PICTURE = Rec(F("file", "File"), F("file_white", "File, white"), F("name", "Name"),
              F("source", "Source"), F("creator", "Creator"), F("licence", "Licence"),
              F("source_url", "Source URL"), F("note", "Note"))

FRONT_KEYS = ("slug", "status", "spec_version", "generated_with", "roadmap_item_id",
              "roadmap_block")
NAME_VARIANTS = Rec(F("site", "Site"), F("internal_slide", "Internal slide"),
                    F("external", "External"), F("external_subheading", "External subheading"),
                    F("note", "Note"), F("source", "Source"))
META_H1 = Rec(F("name_source", "Source of the name"), F("eyebrow", "Eyebrow"),
              F("roadmap_note", "Roadmap note"))
SOURCE_ENGAGEMENT = Rec(F("customer", "Customer"), F("context", "Context"),
                        F("delivered", "Delivered"),
                        F("divergence_from_pack", "Divergence from the pack"),
                        F("divergence_line", "Divergence line"), F("source", "Source"))
PROOF_DECK = Rec(F("proof_headline", "Proof headline"), F("vertical_case", "Vertical case"))
PROOF_ONE_PAGER = Rec(F("proof_story", "Proof story"),
                      F("proof_story_anonymized", "Proof story, anonymized"))

ONE_LINER = Rec(F("full", "Full"), F("short", "Short"),
                F("banned_words_checked", "Banned words checked", BOOL),
                F("kpi_chips", "KPI chips", PAIRS, pair=("label", "direction")),
                F("note", "Note"), F("source", "Source"))
PS_PARAGRAPHS = (("problem", "Problem"), ("solution", "Solution"))
PROBLEM_SOLUTION = Rec(F("problem_points", "Problem points", PAIRS, pair=("label", "text")),
                       F("sub_problems", "Sub-problems", PAIRS, pair=("label", "text")),
                       F("outcome_chips", "Outcome chips", LIST), F("outcomes", "Outcomes", LIST),
                       F("reframe", "Reframe"), F("reframe_question", "Reframe question"),
                       F("today", "Today"), F("tomorrow", "Tomorrow"), F("note", "Note"),
                       F("source", "Source"))
ICP = Rec(F("buyer_roles", "Buyer roles", LIST),
          F("buyer_roles_operator", "Buyer roles, operator", LIST),
          F("buyer_roles_payer", "Buyer roles, payer", LIST),
          F("buyer_by_industry", "Buyer by industry", MAP),
          F("qualifying_signals", "Qualifying signals", LIST),
          F("disqualifiers", "Disqualifiers", LIST),
          F("dual_buyer_rule", "Dual-buyer rule"), F("why_both", "Why both"),
          F("note", "Note"), F("source", "Source"))
FRAMING = Rec(F("problem", "Problem"), F("solution", "Solution"), F("entities", "Entities"))
VERTICAL = Rec(F("site_label", "Site label"), F("framing", "Framing", RECORD, rec=FRAMING),
               F("catalog_type", "Catalog type"), F("status", "Status"),
               F("what_matters_here", "What matters here"),
               F("worked_example", "Worked example"),
               F("entities_differ", "How the entities differ"), F("note", "Note"),
               F("scope_note", "Scope note"), F("tier_note", "Tier note"),
               F("icon", "Icon", RECORD, rec=PICTURE), F("source", "Source"))
VERTICAL_TITLES = ("Held out", "Rejected")
HELD_OUT = Rec(F("note", "Note"), F("candidates", "Candidates", LIST))
REJECTED = Rec(F("name", "Name"), F("reason", "Reason"))

AREA = Rec(F("stage", "Stage"),
           F("customization_scope_area", "Customization in this area", TLIST))
FEATURE_COLUMNS = Rec(F("name", "Feature"), F("status", "Status"),
                      F("tier_first_available", "From tier"),
                      F("customization_scope", "Customization"),
                      F("specificity", "Specificity", LIST), F("note", "Note"),
                      F("footnote_marker", "Footnote marker"),
                      F("oracle_product", "Oracle product"), F("source", "Source"))
CATEGORY_COLUMNS = Rec(F("note", "Note"))

IO = Rec(F("system", "System"), F("detail", "Detail"), F("data", "Data"), F("tier", "Tier"),
         F("note", "Note"))
STEP = Rec(F("actor", "Actor"), F("human_in_the_loop", "Human in the loop", BOOL),
           F("covers", "Covers"), F("description", "Description"),
           F("failure_path", "If it fails"),
           F("vertical_differences", "Vertical differences", MAP), F("source", "Source"))
WORKFLOW_TITLES = ("Inputs", "Outputs", "Notes")
WORKFLOW_NOTES = Rec(F("grouping_note", "Grouping note"),
                     F("domain_steps_note", "Domain steps note"),
                     F("not_ours", "Not ours", PAIRS, pair=("step", "reason")),
                     F("integration_tiers", "Integration by tier", RECORD, rec=BY_TIER),
                     F("source", "Source"))
LAYER = Rec(F("layer", "Layer"), F("name", "Name"), F("vendor", "Vendor"),
            F("items", "Items", LIST), F("summary", "Summary"), F("label", "Label"),
            F("catalog_id", "Catalog id", LIST), F("note", "Note"))
STACK_TITLE = "Stack, top to bottom"
ARCH_NOTES = Rec(F("note", "Note"), F("platform_overlap_note", "Platform overlap note"),
                 F("source", "Source"))

PRODUCT = Rec(F("id", "Id"), F("name", "Name"), F("role", "Role"), F("why", "Why"),
              F("integration", "Integration by tier", RECORD, rec=BY_TIER),
              F("note", "Note"), F("name_note", "Name note"), F("catalog_note", "Catalog note"),
              F("inferred", "Inferred", BOOL), F("source", "Source"))

ATTRIBUTION = Rec(F("named_when_allowed", "Named when allowed"), F("otherwise", "Otherwise"))
KPI = Rec(F("kind", "Kind"), F("owner_role", "Signed off by"),
          F("one_pager_label", "One-pager label"), F("chip", "Chip"),
          F("chip_label", "Chip label"), F("label", "Label"), F("direction", "Direction"),
          F("formula", "Formula"), F("baseline", "Baseline"), F("figure", "Figure"),
          F("figure_prefix", "Figure prefix"), F("figure_suffix", "Figure suffix"),
          F("figure_status", "Figure status"), F("show_baseline", "Show baseline", BOOL),
          F("unit_cost", "Unit cost"), F("whose_metric", "Whose metric"),
          F("attribution", "Attribution", RECORD, rec=ATTRIBUTION), F("caveat", "Caveat"),
          F("channels", "Channels", LIST), F("note", "Note"), F("source", "Source"))
METRICS_TOP = Rec(F("kpis_note", "Kpis note"))

PACKAGES_TOP = Rec(F("status", "Status"), F("anchor_line", "Anchor line"),
                   F("tier_vocabulary_note", "Tier vocabulary note"),
                   F("tier_semantics", "Tier semantics"),
                   F("capability_handling_legend", "Legend"),
                   F("value_for_partner", "Value for Oracle and NVIDIA"),
                   F("value_for_client", "Value for the client"),
                   F("target_oci_consumption", "Target OCI consumption"), F("source", "Source"))
TIER = Rec(F("id", "Id"), F("scope_line", "Scope"), F("duration_weeks", "Duration", DURATION),
           F("duration_label", "Duration label"), F("duration_note", "Duration note"),
           F("justification", "Justification"),
           F("duration_justification", "Duration justification"),
           F("services_price", "Services price", MONEY),
           F("infra_price_monthly", "Infrastructure price per month", MONEY),
           F("what_you_get", "What you get", LIST), F("entry_gate", "Entry gate", LIST),
           F("scope_in", "In scope", LIST), F("scope_out", "Out of scope", LIST),
           F("show_size_tag", "Show size tag", BOOL), F("name_note", "Name note"),
           F("source", "Source"))
HANDLING = Rec(F("area", "Area"), F("maps_to_feature_areas", "Feature areas", LIST),
               F("pov", "PoV"), F("integration", "Integration"), F("scaling", "Scaling"),
               F("levels", "Levels", RECORD, rec=BY_TIER),
               F("glyphs", "Glyphs", RECORD, rec=BY_TIER))
PACKAGE_TITLES = {"How each capability area is handled per tier": "capability_handling",
                  "Why it sells for the partner": "why_it_sells_for_the_partner",
                  "What each buyer gets": "what_each_buyer_gets"}
BUYER_GETS = Rec(F("operator", "Operator"), F("payer", "Payer"))
QUESTION = Rec(F("question", "Question"), F("why", "Why"), F("blocks", "Blocks", LIST))

CHANNEL_LABELS = (("internal", "Internal"), ("partner_print", "Partner print"),
                  ("customer_site", "Customer site"), ("demo", "Demo"))
CHANNEL_HEADER = ["Channel", "Customer may be named"]
CLEARANCE = Rec(F("anonymized_descriptor", "Anonymized descriptor"),
                F("descriptor_warning", "Descriptor warning"),
                F("internal_only_facts", "Internal-only facts", LIST),
                F("forbidden_strings", "Forbidden strings", LIST),
                F("disclaimer", "Disclaimer"), F("approvals", "Approvals", LIST),
                F("source", "Source"))
CONTACT = Rec(F("name", "Name"), F("title", "Title"), F("org", "Organization"),
              F("email", "Email"), F("mailbox", "Mailbox"), F("named", "Named"),
              F("status", "Status"), F("note", "Note"))
CONTACTS = Rec(F("partner_print", "Partner print", RECORD, rec=CONTACT),
               F("site", "Site", RECORD, rec=CONTACT),
               F("internal", "Internal", RECORD, rec=CONTACT), F("source", "Source"))
DECK_IMAGES = Rec(F("customer_logo", "Customer logo", RECORD, rec=PICTURE),
                  F("cover", "Cover", RECORD, rec=PICTURE),
                  F("today", "Today", RECORD, rec=PICTURE),
                  F("tomorrow", "Tomorrow", RECORD, rec=PICTURE))
DECK = Rec(F("running_header", "Running header"), F("seller_lead", "Seller lead"),
           F("cta", "Cta"), F("anchor_line", "Anchor line"),
           F("layers_sub", "Layers subtitle"), F("architecture_sub", "Architecture subtitle"),
           F("source", "Source"), F("images", "Images", RECORD, rec=DECK_IMAGES))
ONE_PAGER_CTA = Rec(F("question", "Question"), F("answer", "Answer"))
ONE_PAGER_IMAGES = Rec(F("hero", "Hero", RECORD, rec=PICTURE))
ONE_PAGER = Rec(F("eyebrow", "Eyebrow"), F("reframe", "Reframe"), F("sub", "Sub"),
                F("data_flow_notes", "Data-flow notes", BOOL),
                F("tier_scope", "Tier scope", RECORD, rec=BY_TIER),
                F("cta", "Cta", RECORD, rec=ONE_PAGER_CTA),
                F("kpi_chips", "KPI chips", PAIRS, pair=("label", "direction")),
                F("disclaimer", "Disclaimer"), F("proof_logo", "Proof logo"),
                F("proof_caveat", "Proof caveat"), F("problem_heading", "Problem heading"),
                F("sell_heading", "Sell heading"), F("verticals_label", "Verticals label"),
                F("packages_heading", "Packages heading"),
                F("infra_row_label", "Infrastructure row label"),
                F("services_row_label", "Services row label"),
                F("images", "Images", RECORD, rec=ONE_PAGER_IMAGES), F("source", "Source"))
EXEC_SUMMARY = Rec(F("running_header", "Running header"), F("goal", "Goal"),
                   F("closing_line", "Closing line"), F("source", "Source"))
FEATURE_LIST = Rec(F("title", "Title"), F("intro_label", "Intro label"), F("intro", "Intro"),
                   F("source", "Source"))
# What the owner wants built and who sees the printed documents, settled once in the spec run
# so the build reads them from the spec on any machine (2026-09-24). lint_spec.py (SPEC030)
# holds the values to these two lists.
BUILD_ARTIFACTS = ("feature-list", "deck", "one-pager", "exec-summary", "listing", "demo")
BUILD_AUDIENCES = ("partner_print", "internal")
BUILD = Rec(F("artifacts", "Artifacts", LIST), F("audience", "Audience"), F("source", "Source"))
INPUT = Rec(F("id", "Id"), F("path", "Path"), F("kind", "Kind"), F("read", "Read", DATE),
            F("note", "Note"), F("supplies", "Supplies", LIST))
PROVENANCE = Rec(F("inputs", "Inputs", RECORDS, rec=INPUT),
                 F("research_brief", "Research brief"), F("inventory", "Inventory", LIST),
                 F("research", "Research", LIST), F("source", "Source"))
SETTINGS = (("build", "Build", BUILD), ("contacts", "Contacts", CONTACTS), ("deck", "Deck", DECK),
            ("one_pager", "One-pager", ONE_PAGER),
            ("exec_summary", "Executive summary", EXEC_SUMMARY),
            ("feature_list", "Feature list", FEATURE_LIST),
            ("provenance", "Provenance", PROVENANCE))

TOP_KEYS = ("meta", "one_liner", "problem_solution", "icp", "verticals", "verticals_held_out",
            "verticals_rejected", "capabilities", "workflow", "architecture", "oracle_products",
            "kpis_note", "kpis", "packages", "deck", "one_pager", "exec_summary", "feature_list",
            "clearance", "build", "contacts", "provenance", "open_questions")

SECTIONS = ("One-liner", "Problem and solution", "Who buys it", "Industries", "Capabilities",
            "Workflow", "Architecture", "Oracle products", "Metrics", "Packages", "Proof",
            "Next steps", "Open questions", "Settings", "Other fields")

RECORD_LIMITS = (220, 8, 160)   # a record list with a heading form takes it past: a cell's
                                # length, the number of columns, a list's summed length
INLINE_LIST_LIMIT = 160         # a list on a key line; a longer one is nested bullets


def _fields(*recs, extra=()):
    out = {}
    for rec in recs:
        for f in rec.fields:
            out[f.key] = f
    for key, kind in extra:
        out[key] = F(key, key, kind)
    return out


# Every mapping the layout knows, by path pattern (`[]` for any list position): its keys and
# their kinds. `packspec.py check`, the `set` command and lint_spec's SPEC024 read this.
SCHEMA = {
    "": _fields(extra=[(k, RECORD) for k in TOP_KEYS]),
    "meta": _fields(META_H1, extra=[("slug", TEXT), ("status", TEXT), ("spec_version", INT),
                                    ("generated_with", RECORD), ("roadmap_item_id", TEXT),
                                    ("roadmap_block", TEXT), ("name", TEXT),
                                    ("name_variants", RECORD), ("source_engagement", RECORD)]),
    "meta.generated_with": _fields(extra=[("roadmap_version", DATE), ("catalog_version", DATE)]),
    "meta.name_variants": _fields(NAME_VARIANTS),
    "meta.source_engagement": _fields(SOURCE_ENGAGEMENT),
    "one_liner": _fields(ONE_LINER),
    "one_liner.kpi_chips[]": _fields(extra=[("label", TEXT), ("direction", TEXT)]),
    "problem_solution": _fields(PROBLEM_SOLUTION, extra=[("problem", TEXT), ("solution", TEXT)]),
    "problem_solution.problem_points[]": _fields(extra=[("label", TEXT), ("text", TEXT)]),
    "problem_solution.sub_problems[]": _fields(extra=[("label", TEXT), ("text", TEXT)]),
    "icp": _fields(ICP, extra=[("line", TEXT)]),
    "verticals[]": _fields(VERTICAL, extra=[("name", TEXT)]),
    "verticals[].framing": _fields(FRAMING),
    "verticals[].icon": _fields(PICTURE),
    "verticals_held_out": _fields(HELD_OUT),
    "verticals_rejected[]": _fields(REJECTED),
    "capabilities[]": _fields(AREA, extra=[("area", TEXT), ("categories", RECORDS)]),
    "capabilities[].categories[]": _fields(CATEGORY_COLUMNS, extra=[("name", TEXT),
                                                                     ("features", RECORDS)]),
    "capabilities[].categories[].features[]": _fields(FEATURE_COLUMNS),
    "workflow": _fields(WORKFLOW_NOTES, extra=[("inputs", RECORDS), ("steps", RECORDS),
                                               ("outputs", RECORDS)]),
    "workflow.inputs[]": _fields(IO),
    "workflow.outputs[]": _fields(IO),
    "workflow.steps[]": _fields(STEP, extra=[("n", INT), ("name", TEXT)]),
    "workflow.not_ours[]": _fields(extra=[("step", TEXT), ("reason", TEXT)]),
    "workflow.integration_tiers": _fields(BY_TIER),
    "architecture": _fields(ARCH_NOTES, extra=[("inputs", RECORDS), ("stack", RECORDS),
                                               ("outputs", RECORDS)]),
    "architecture.inputs[]": _fields(IO),
    "architecture.outputs[]": _fields(IO),
    "architecture.stack[]": _fields(LAYER),
    "oracle_products[]": _fields(PRODUCT),
    "oracle_products[].integration": _fields(BY_TIER),
    "kpis[]": _fields(KPI, extra=[("name", TEXT)]),
    "kpis[].attribution": _fields(ATTRIBUTION),
    "packages": _fields(PACKAGES_TOP, extra=[("tiers", RECORDS), ("capability_handling", RECORDS),
                                             ("why_it_sells_for_the_partner", PAIRS),
                                             ("what_each_buyer_gets", RECORD)]),
    "packages.tiers[]": _fields(TIER, extra=[("name", TEXT), ("size_tag", TEXT)]),
    "packages.tiers[].services_price": {k: F(k, k) for k in _MONEY_KEYS},
    "packages.tiers[].infra_price_monthly": {k: F(k, k) for k in _MONEY_KEYS},
    "packages.tiers[].duration_weeks": {k: F(k, k) for k in _DURATION_KEYS},
    "packages.capability_handling[]": _fields(HANDLING),
    "packages.capability_handling[].levels": _fields(BY_TIER),
    "packages.capability_handling[].glyphs": _fields(BY_TIER),
    "packages.why_it_sells_for_the_partner[]": _fields(extra=[("label", TEXT), ("text", TEXT)]),
    "packages.what_each_buyer_gets": _fields(BUYER_GETS),
    "open_questions[]": _fields(QUESTION, extra=[("id", TEXT)]),
    "clearance": _fields(CLEARANCE, extra=[("customer_name_allowed", RECORD)]),
    "clearance.customer_name_allowed": _fields(extra=[(k, BOOL) for k, _ in CHANNEL_LABELS]),
    "contacts": _fields(CONTACTS),
    "contacts.partner_print": _fields(CONTACT),
    "contacts.site": _fields(CONTACT),
    "contacts.internal": _fields(CONTACT),
    "deck": _fields(DECK, PROOF_DECK),
    "deck.images": _fields(DECK_IMAGES),
    "deck.images.customer_logo": _fields(PICTURE),
    "deck.images.cover": _fields(PICTURE),
    "deck.images.today": _fields(PICTURE),
    "deck.images.tomorrow": _fields(PICTURE),
    "one_pager": _fields(ONE_PAGER, PROOF_ONE_PAGER),
    "one_pager.tier_scope": _fields(BY_TIER),
    "one_pager.cta": _fields(ONE_PAGER_CTA),
    "one_pager.kpi_chips[]": _fields(extra=[("label", TEXT), ("direction", TEXT)]),
    "one_pager.images": _fields(ONE_PAGER_IMAGES),
    "one_pager.images.hero": _fields(PICTURE),
    "exec_summary": _fields(EXEC_SUMMARY, extra=[("next_steps", PAIRS)]),
    "exec_summary.next_steps[]": _fields(extra=[("title", TEXT), ("detail", TEXT)]),
    "feature_list": _fields(FEATURE_LIST),
    "build": _fields(BUILD),
    "provenance": _fields(PROVENANCE),
    "provenance.inputs[]": _fields(INPUT),
}

# The record lists and the keys each item may carry — lint_spec's SPEC024.
RECORD_LISTS = {pattern[:-2]: set(fields) for pattern, fields in SCHEMA.items()
                if pattern.endswith("[]")}


def pattern_of(path) -> str:
    """("verticals", 3, "icon") -> 'verticals[].icon'."""
    out = ""
    for seg in path:
        if isinstance(seg, int) and not isinstance(seg, bool):
            out += "[]"
        else:
            out += ("." if out else "") + str(seg)
    return out


def unknown_keys(data):
    """(container path, key) for every key the layout does not know, where it knows the mapping."""
    out = []

    def walk(value, path):
        if isinstance(value, dict):
            fields = SCHEMA.get(pattern_of(path))
            if fields is None:
                return
            for k, v in value.items():
                if k not in fields:
                    out.append((path, k))
                elif isinstance(k, str):
                    walk(v, path + (k,))
        elif isinstance(value, list):
            for i, v in enumerate(value):
                walk(v, path + (i,))

    walk(data, ())
    return out


def field_for(path):
    """The layout's field for a plain key path, or None."""
    if not path or not isinstance(path[-1], str):
        return None
    fields = SCHEMA.get(pattern_of(path[:-1]))
    return fields.get(path[-1]) if fields else None


# ============================================================================ the writer
def _nice_title(value) -> bool:
    return isinstance(value, str) and value != "" and value == value.strip() and "\n" not in value


def _label_ok(text) -> bool:
    return (isinstance(text, str) and text != "" and text == text.strip() and "\n" not in text
            and "*" not in text and ":" not in text and "\\" not in text
            and not _CONTROL_RE.search(text))


def _title_text(value, reserved=()) -> str:
    """A heading's text for a title value. Raises Misfit when no heading can hold it."""
    if isinstance(value, str) and value not in reserved:
        try:
            raw = _enc_text_line(value, "title")
        except Misfit:
            return _hatch(value)
        m = _ORDERED_RE.match(raw)
        if m:
            return m.group(1) + "\\" + raw[len(m.group(1)):]
        return raw
    return _hatch(value)


class _Writer:
    def __init__(self, data: dict):
        self.data = data
        self.lines = []
        self.residuals = []      # (parent path, key, value) for the Other fields block
        self.elsewhere = set()   # (top key, key) written in a section other than its own
        self.seen = {(): 0}      # container path -> the order the document reaches it in

    def see(self, path):
        self.seen.setdefault(tuple(path), len(self.seen))

    # -- plumbing
    def emit(self, *lines):
        self.lines.extend(lines)

    def blank(self):
        if self.lines and self.lines[-1] != "":
            self.lines.append("")

    def heading(self, level: int, text: str):
        self.blank()
        self.lines.append("#" * level + " " + text)
        self.lines.append("")

    def residual(self, path, key, value):
        self.residuals.append((tuple(path), key, value))

    def mark(self):
        return len(self.lines), len(self.residuals)

    def rollback(self, mark):
        del self.lines[mark[0]:]
        del self.residuals[mark[1]:]

    # -- key lines
    def keys_lines(self, rec: Rec, data: dict, path, indent: int, skip=()):
        self.see(path)
        out = []
        for key, value in data.items():
            if key in skip:
                continue
            f = rec.by_key.get(key) if isinstance(key, str) else None
            if f is None:
                self.residual(path, key, value)
                continue
            mark = len(self.residuals)
            try:
                out.extend(self.field_lines(f, value, path + (key,), indent))
            except Misfit:
                del self.residuals[mark:]
                self.residual(path, key, value)
        return out

    def field_lines(self, f: F, value, path, indent: int):
        head = "%s- **%s:**" % (" " * indent, f.label)
        return self.value_lines(head, f, value, path, indent)

    def value_lines(self, head: str, f: F, value, path, indent: int):
        kind = f.kind
        if kind in (RECORD, MAP):
            if isinstance(value, dict):
                if kind == RECORD:
                    return [head] + self.keys_lines(f.rec, value, path, indent + 2)
                return [head] + self.map_lines(value, indent + 2)
            if isinstance(value, list) and value:
                raise Misfit("a list where a mapping goes")
            kind = TEXT
        elif kind in (PAIRS, RECORDS):
            if isinstance(value, list) and value:
                if kind == PAIRS:
                    return [head] + self.pair_lines(value, f.pair, indent + 2)
                return [head] + self.records_lines(f.rec, value, path, indent + 2)
            if isinstance(value, dict):
                raise Misfit("a mapping where a list goes")
            kind = TEXT
        if kind in (TEXT, TLIST) and isinstance(value, str):
            try:
                body = _enc_text_lines(value, "keyval")
            except Misfit:
                return [head + " " + _hatch(value)]
            pad = " " * (indent + 2)
            return [head + " " + body[0]] + [(pad + ln if ln else "") for ln in body[1:]]
        if kind in (LIST, TLIST) and isinstance(value, list) and value:
            if kind == LIST:
                try:
                    return [head + " " + _fmt_inline_list(value, "keyval", INLINE_LIST_LIMIT)]
                except Misfit:
                    pass
            return [head] + self.bullet_lines(value, indent + 2)
        return [head + " " + enc_scalar(value, kind, "keyval")]

    def map_lines(self, data: dict, indent: int):
        out = []
        for key, value in data.items():
            if not _label_ok(key):
                raise Misfit("a key that cannot be a label")
            head = "%s- **%s:**" % (" " * indent, _esc_inline(key))
            out.extend(self.value_lines(head, F(key, key), value, (), indent))
        return out

    def bullet_lines(self, items, indent: int):
        out = []
        pad = " " * indent
        for item in items:
            if isinstance(item, (list, dict)):
                raise Misfit("a list or a mapping inside a list")
            if isinstance(item, str):
                try:
                    body = _enc_text_lines(item, "item")
                except Misfit:
                    body = [_hatch(item)]
            else:
                body = [enc_scalar(item, TEXT, "item")]
            out.append(pad + "- " + body[0])
            out.extend((pad + "  " + ln if ln else "") for ln in body[1:])
        return out

    def pair_lines(self, items, pair, indent: int):
        out = []
        pad = " " * indent
        k1, k2 = pair
        for item in items:
            if isinstance(item, dict):
                if set(item) != {k1, k2} or not _label_ok(item[k1]):
                    raise Misfit("a pair that is not {%s, %s}" % pair)
                head = "%s- **%s:**" % (pad, _esc_inline(item[k1]))
                out.extend(self.value_lines(head, F(k2, k2), item[k2], (), indent))
            else:
                out.extend(self.bullet_lines([item], indent))
        return out

    def records_lines(self, rec: Rec, items, path, indent: int):
        out = []
        pad = " " * indent
        for i, item in enumerate(items):
            ipath = path + (i,)
            if not isinstance(item, dict):
                out.extend(self.bullet_lines([item], indent))
                continue
            self.see(ipath)
            known = [(k, v) for k, v in item.items() if isinstance(k, str) and k in rec.by_key]
            unknown = [(k, v) for k, v in item.items()
                       if not (isinstance(k, str) and k in rec.by_key)]
            # The bullet carries the first field that renders at all, when it fits on the
            # bullet's line; a field that goes to Other fields never decides the form, so the
            # form does not change when that field comes back at the end of the mapping.
            first = None
            for k, v in known:
                mark = len(self.residuals)
                try:
                    probe = self.field_lines(rec.by_key[k], v, ipath + (k,), indent)
                except Misfit:
                    del self.residuals[mark:]
                    continue
                del self.residuals[mark:]
                if len(probe) == 1 and not probe[0].endswith(":**"):
                    first = (k, probe)
                break
            if first:
                out.extend(first[1])
                rest = [(k, v) for k, v in known if k != first[0]]
            else:
                out.append(pad + "-")
                rest = known
            for k, v in rest:
                mark = len(self.residuals)
                try:
                    out.extend(self.field_lines(rec.by_key[k], v, ipath + (k,), indent + 2))
                except Misfit:
                    del self.residuals[mark:]
                    self.residual(ipath, k, v)
            for k, v in unknown:
                self.residual(ipath, k, v)
        return out

    def numbered_lines(self, items, pair=None):
        out = []
        for i, item in enumerate(items, 1):
            marker = "%d. " % i
            pad = " " * len(marker)
            if isinstance(item, dict):
                if pair is None:
                    raise Misfit("a mapping in a numbered list")
                k1, k2 = pair
                if set(item) != {k1, k2} or not _label_ok(item[k1]):
                    raise Misfit("a pair that is not {%s, %s}" % pair)
                head = "%s**%s:**" % (marker, _esc_inline(item[k1]))
                out.extend(self.value_lines(head, F(k2, k2), item[k2], (), len(marker) - 2))
                continue
            if isinstance(item, list):
                raise Misfit("a list in a numbered list")
            if isinstance(item, str):
                try:
                    body = _enc_text_lines(item, "item")
                except Misfit:
                    body = [_hatch(item)]
            else:
                body = [enc_scalar(item, TEXT, "item")]
            out.append(marker + body[0])
            out.extend((pad + ln if ln else "") for ln in body[1:])
        return out

    def paragraph_lines(self, value):
        if isinstance(value, (list, dict)) and value:
            raise Misfit("a list or a mapping where text goes")
        if isinstance(value, str):
            try:
                return _enc_text_lines(value, "para")
            except Misfit:
                return [_hatch(value)]
        return [enc_scalar(value, TEXT, "keyval")]

    # -- tables
    def cell(self, value, kind, fallback, limits):
        if isinstance(value, str) and kind in (TEXT, TLIST):
            try:
                raw = _enc_text_line(value, "cell")
            except Misfit:
                if fallback:
                    raise
                raw = _hatch(value)
        elif kind == LIST and isinstance(value, list) and value:
            raw = _fmt_inline_list(value, "cell", limits[2] if limits else None)
        elif isinstance(value, (list, dict)) and value:
            raise Misfit("a list or a mapping in a cell")
        else:
            raw = enc_scalar(value, kind, "cell")
        if _HATCH_RE.match(raw):
            if "\\|" in raw:
                raise Misfit("a code span that cannot sit in a cell")
            raw = raw.replace("|", "\\|")
        if limits and len(raw) > limits[0]:
            raise Misfit("a cell too long for a table")
        return raw

    def table(self, rec: Rec, rows, path, flatten=(), first=None, fallback=False, limits=None):
        """Rows (mappings) as one table. Declared columns in `rec`'s order, then a column per
        unknown key. `flatten` spreads a nested per-tier mapping over columns; `first` is a
        leading (header, cell texts) column. With `fallback`, a value that is not a plain cell
        raises Misfit (the caller takes the heading form); without it, the value goes to
        Other fields and its cell stays empty."""
        flat = dict(flatten)
        present = set()
        for i, row in enumerate(rows):
            self.see(path + (i,))
            present.update(k for k in row if isinstance(k, str))
        cols = []                               # (header, kind, key | (key, sub) | None)
        if first:
            cols.append((first[0], TEXT, None))
        for f in rec.fields:
            if f.key not in present:
                continue
            if f.key in flat:
                sub = flat[f.key]
                for row in rows:
                    v = row.get(f.key, {})
                    if f.key in row and (not isinstance(v, dict) or not v or not set(v) <= set(sub.by_key)
                                         or not all(_is_scalar(x) for x in v.values())):
                        raise Misfit("a nested value that is not one cell per tier")
                for s in sub.fields:
                    if any(isinstance(r.get(f.key), dict) and s.key in r[f.key] for r in rows):
                        cols.append((s.label, TEXT, (f.key, s.key)))
                continue
            kind = f.kind if (f.kind in SCALAR_KINDS or f.kind == LIST) else TEXT
            cols.append((f.label, kind, f.key))
        headers = {c[0] for c in cols} | set(rec.by_label) | {s.label for sub in flat.values()
                                                                for s in sub.fields}
        unknown = []
        for row in rows:
            for k in row:
                if not (isinstance(k, str) and k in rec.by_key) and k not in unknown:
                    unknown.append(k)
        for k in unknown:
            values = [(i, r[k]) for i, r in enumerate(rows) if k in r]
            ok = (_label_ok(k) and "|" not in k and k not in headers and not _HATCH_RE.match(k)
                  and k not in (DASH, NONE))
            if ok:
                try:
                    for _, v in values:
                        self.cell(v, TEXT, True, limits)
                except Misfit:
                    ok = False
            if ok:
                cols.append((k, TEXT, k))
                headers.add(k)
            else:
                for i, v in values:
                    self.residual(path + (i,), k, v)
        if not cols:
            raise Misfit("a table with no columns")
        if limits and len(cols) > limits[1]:
            raise Misfit("more columns than a table carries")
        body = []
        for i, row in enumerate(rows):
            cells = []
            for header, kind, key in cols:
                if key is None:
                    cells.append(first[1][i])
                    continue
                if isinstance(key, tuple):
                    sub = row.get(key[0])
                    has = isinstance(sub, dict) and key[1] in sub
                    value = sub[key[1]] if has else None
                else:
                    has, value = key in row, row.get(key)
                if not has:
                    cells.append("")
                    continue
                try:
                    cells.append(self.cell(value, kind, fallback, limits))
                except Misfit:
                    if fallback or isinstance(key, tuple):
                        raise
                    self.residual(path + (i,), key, value)
                    cells.append("")
            body.append("| " + " | ".join(cells) + " |")
        self.emit("| " + " | ".join(_esc_inline(c[0], cell=True) for c in cols) + " |",
                  "|" + "---|" * len(cols))
        self.emit(*body)

    def titles(self, rows, key, reserved=()):
        if not isinstance(rows, list):
            return None
        out = []
        for r in rows:
            if not isinstance(r, dict) or not _nice_title(r.get(key)):
                return None
            try:
                out.append(_title_text(r[key], reserved))
            except Misfit:
                return None
        return out

    def records_block(self, rec: Rec, rows, path, level: int, title_key: str, flatten=(),
                      limits=RECORD_LIMITS):
        """A record list as a table; one heading per record when a record does not fit a row;
        bullets for plain items; `(none)` when empty. Raises Misfit when none of these fits."""
        if not isinstance(rows, list):
            raise Misfit("not a list")
        if not rows:
            self.emit(NONE)
            return
        if all(isinstance(r, dict) for r in rows):
            mark = self.mark()
            try:
                self.table(rec, rows, path, flatten=flatten, fallback=True, limits=limits)
                return
            except Misfit:
                self.rollback(mark)
            titles = self.titles(rows, title_key)
            if titles is None:
                raise Misfit("records that fit neither a table nor headings")
            for i, (row, title) in enumerate(zip(rows, titles)):
                self.heading(level, title)
                self.emit(*self.keys_lines(rec, row, path + (i,), 0, skip=(title_key,)))
            return
        if all(not isinstance(r, (dict, list)) for r in rows):
            self.emit(*self.bullet_lines(rows, 0))
            return
        raise Misfit("a list of mixed items")

    # -- the document
    def write(self) -> str:
        data = self.data
        handled = {"meta"}
        if "meta" in data:
            meta = data["meta"]
            if isinstance(meta, dict):
                self.front_matter(meta)
                self.write_h1(meta)
            else:
                self.residual((), "meta", meta)
        writers = (
            ("One-liner", ("one_liner",), self.sec_one_liner),
            ("Problem and solution", ("problem_solution",), self.sec_problem_solution),
            ("Who buys it", ("icp",), self.sec_icp),
            ("Industries", ("verticals", "verticals_held_out", "verticals_rejected"),
             self.sec_industries),
            ("Capabilities", ("capabilities",), self.sec_capabilities),
            ("Workflow", ("workflow",), self.sec_workflow),
            ("Architecture", ("architecture",), self.sec_architecture),
            ("Oracle products", ("oracle_products",), self.sec_products),
            ("Metrics", ("kpis_note", "kpis"), self.sec_metrics),
            ("Packages", ("packages",), self.sec_packages),
            ("Proof", (), self.sec_proof),
            ("Next steps", (), self.sec_next_steps),
            ("Open questions", ("open_questions",), self.sec_open_questions),
            ("Settings", ("clearance", "build", "contacts", "deck", "one_pager", "exec_summary",
                          "feature_list", "provenance"), self.sec_settings),
        )
        for title, keys, fn in writers:
            handled.update(keys)
            start = len(self.lines)
            self.heading(2, title)
            body = len(self.lines)
            if not fn():
                del self.lines[start:]
            elif len(self.lines) == body and self.lines[-1] == "":
                self.lines.pop()
        for key, value in data.items():
            if key not in handled:
                self.residual((), key, value)
        self.write_other_fields()
        while self.lines and self.lines[-1] == "":
            self.lines.pop()
        return "\n".join(self.lines) + "\n"

    def front_matter(self, meta: dict):
        yaml = _yaml()
        self.see(("meta",))
        self.emit("---")
        for key in FRONT_KEYS:
            if key not in meta:
                continue
            value = meta[key]
            try:
                text = _flow(value)
                if isinstance(value, dict) and value and text.startswith("{") and text.endswith("}"):
                    text = "{ " + text[1:-1] + " }"
                back = yaml.safe_load("%s: %s" % (key, text))
                if repr(back) != repr({key: value}):
                    raise Misfit("front matter that does not read back")
            except Misfit:
                self.residual(("meta",), key, value)
                continue
            self.emit("%s: %s" % (key, text))
        self.emit("---")

    def write_h1(self, meta: dict):
        if "name" in meta:
            name = meta["name"]
            try:
                title = _title_text(name) if isinstance(name, str) else enc_scalar(name, TEXT, "title")
            except Misfit:
                title = None
            if title is None:
                self.residual(("meta",), "name", name)
            else:
                self.blank()
                self.emit("# " + title)
        body = []
        if "name_variants" in meta:
            nv = meta["name_variants"]
            done = False
            if isinstance(nv, dict) and nv:
                mark = len(self.residuals)
                lines = self.keys_lines(NAME_VARIANTS, nv, ("meta", "name_variants"), 0)
                if lines:
                    body.extend(lines)
                    done = True
                else:
                    del self.residuals[mark:]
            if not done:
                self.residual(("meta",), "name_variants", nv)
        for key, value in meta.items():
            if key in FRONT_KEYS or key in ("name", "name_variants", "source_engagement"):
                continue
            f = META_H1.by_key.get(key) if isinstance(key, str) else None
            if f is None:
                self.residual(("meta",), key, value)
                continue
            mark = len(self.residuals)
            try:
                body.extend(self.field_lines(f, value, ("meta", key), 0))
            except Misfit:
                del self.residuals[mark:]
                self.residual(("meta",), key, value)
        if body:
            self.blank()
            self.emit(*body)

    def dict_section(self, key: str, rec: Rec, paragraphs=(), lead=None):
        """A section that is one mapping: an optional lead paragraph, optional `###`
        paragraphs, then its key lines."""
        if key not in self.data:
            return False
        value = self.data[key]
        if not isinstance(value, dict):
            self.residual((), key, value)
            return False
        self.see((key,))
        skip = {k for k, _ in paragraphs}
        if lead:
            skip.add(lead)
            if lead in value:
                try:
                    self.emit(*self.paragraph_lines(value[lead]))
                except Misfit:
                    self.residual((key,), lead, value[lead])
        for pkey, title in paragraphs:
            if pkey in value:
                try:
                    lines = self.paragraph_lines(value[pkey])
                except Misfit:
                    self.residual((key,), pkey, value[pkey])
                    continue
                self.heading(3, title)
                self.emit(*lines)
        lines = self.keys_lines(rec, value, (key,), 0, skip=skip)
        if lines:
            self.blank()
            self.emit(*lines)
        return True

    def sec_one_liner(self):
        return self.dict_section("one_liner", ONE_LINER)

    def sec_problem_solution(self):
        return self.dict_section("problem_solution", PROBLEM_SOLUTION, paragraphs=PS_PARAGRAPHS)

    def sec_icp(self):
        return self.dict_section("icp", ICP, lead="line")

    def titled_records(self, rows, rec, path, title_key, level=3):
        titles = self.titles(rows, title_key)
        if titles is None:
            return False
        if not rows:
            self.blank()
            self.emit(NONE)
        for i, (row, title) in enumerate(zip(rows, titles)):
            self.heading(level, title)
            self.emit(*self.keys_lines(rec, row, path + (i,), 0, skip=(title_key,)))
        return True

    def sec_industries(self):
        d = self.data
        wrote = False
        if "verticals" in d:
            rows = d["verticals"]
            titles = self.titles(rows, "name", VERTICAL_TITLES)
            if titles is None:
                self.residual((), "verticals", rows)
            else:
                wrote = True
                if not rows:
                    self.emit(NONE)
                for i, (row, title) in enumerate(zip(rows, titles)):
                    self.heading(3, title)
                    self.emit(*self.keys_lines(VERTICAL, row, ("verticals", i), 0, skip=("name",)))
        if "verticals_held_out" in d:
            v = d["verticals_held_out"]
            if isinstance(v, dict):
                wrote = True
                self.heading(3, "Held out")
                self.emit(*self.keys_lines(HELD_OUT, v, ("verticals_held_out",), 0))
            else:
                self.residual((), "verticals_held_out", v)
        if "verticals_rejected" in d:
            v = d["verticals_rejected"]
            mark = self.mark()
            try:
                self.heading(3, "Rejected")
                self.records_block(REJECTED, v, ("verticals_rejected",), 4, "name")
                wrote = True
            except Misfit:
                self.rollback(mark)
                self.residual((), "verticals_rejected", v)
        return wrote

    @staticmethod
    def area_ok(area) -> bool:
        if not isinstance(area, dict) or not _nice_title(area.get("area")):
            return False
        try:
            _title_text(area["area"])
        except Misfit:
            return False
        if "categories" not in area:
            return True
        cats = area["categories"]
        if not isinstance(cats, list) or not cats:
            return False
        names = set()
        for cat in cats:
            if not isinstance(cat, dict) or not _nice_title(cat.get("name")):
                return False
            try:
                _enc_text_line(cat["name"], "cell")
            except Misfit:
                return False
            if cat["name"] in names:
                return False
            names.add(cat["name"])
            feats = cat.get("features")
            if not isinstance(feats, list) or not feats or not all(isinstance(f, dict) for f in feats):
                return False
        return True

    def sec_capabilities(self):
        if "capabilities" not in self.data:
            return False
        caps = self.data["capabilities"]
        if not isinstance(caps, list) or not all(self.area_ok(a) for a in caps):
            self.residual((), "capabilities", caps)
            return False
        if not caps:
            self.emit(NONE)
        for ai, area in enumerate(caps):
            path = ("capabilities", ai)
            self.heading(3, _title_text(area["area"]))
            self.emit(*self.keys_lines(AREA, area, path, 0, skip=("area", "categories")))
            if "categories" not in area:
                continue
            cats = area["categories"]
            rows, names, fpaths = [], [], []
            for ci, cat in enumerate(cats):
                self.see(path + ("categories", ci))
                for fi, feat in enumerate(cat["features"]):
                    rows.append(feat)
                    names.append(_enc_text_line(cat["name"], "cell"))
                    fpaths.append(path + ("categories", ci, "features", fi))
                    self.see(fpaths[-1])
            self.blank()
            mark = len(self.residuals)
            self.table(FEATURE_COLUMNS, rows, (), first=("Category", names))
            self.residuals[mark:] = [(fpaths[p[0]], k, v) for (p, k, v) in self.residuals[mark:]]
            extra = [(ci, c) for ci, c in enumerate(cats) if set(c) - {"name", "features"}]
            if extra:
                self.blank()
                crows = [{k: v for k, v in c.items() if k not in ("name", "features")}
                         for _, c in extra]
                mark = len(self.residuals)
                self.table(CATEGORY_COLUMNS, crows, (),
                           first=("Category", [_enc_text_line(c["name"], "cell") for _, c in extra]))
                self.residuals[mark:] = [(path + ("categories", extra[p[0]][0]), k, v)
                                         for (p, k, v) in self.residuals[mark:]]
        return True

    def io_block(self, parent, key, title, value):
        mark = self.mark()
        try:
            self.heading(3, title)
            self.records_block(IO, value, (parent, key), 4, "system")
        except Misfit:
            self.rollback(mark)
            self.residual((parent,), key, value)

    def step_titles(self, steps):
        if not isinstance(steps, list) or not steps:
            return None
        out = []
        for s in steps:
            if not isinstance(s, dict):
                return None
            has_n, has_name = "n" in s, "name" in s
            n, name = s.get("n"), s.get("name")
            if has_n and (isinstance(n, bool) or not isinstance(n, int) or n < 0):
                return None
            if (has_name and not _nice_title(name)) or not (has_n or has_name):
                return None
            try:
                if has_n and has_name:
                    try:
                        part = _enc_text_line(name, "title")
                    except Misfit:
                        part = _hatch(name)
                    out.append("%d. %s" % (n, part))
                elif has_n:
                    out.append("%d." % n)
                else:
                    out.append(_title_text(name, WORKFLOW_TITLES))
            except Misfit:
                return None
        return out

    def sec_workflow(self):
        if "workflow" not in self.data:
            return False
        wf = self.data["workflow"]
        if not isinstance(wf, dict):
            self.residual((), "workflow", wf)
            return False
        self.see(("workflow",))
        if "inputs" in wf:
            self.io_block("workflow", "inputs", "Inputs", wf["inputs"])
        if "steps" in wf:
            steps = wf["steps"]
            titles = self.step_titles(steps)
            if titles is None:
                self.residual(("workflow",), "steps", steps)
            else:
                for i, (step, title) in enumerate(zip(steps, titles)):
                    self.heading(3, title)
                    self.emit(*self.keys_lines(STEP, step, ("workflow", "steps", i), 0,
                                               skip=("n", "name")))
        if "outputs" in wf:
            self.io_block("workflow", "outputs", "Outputs", wf["outputs"])
        rest = {k: v for k, v in wf.items() if k not in ("inputs", "steps", "outputs")}
        lines = self.keys_lines(WORKFLOW_NOTES, rest, ("workflow",), 0)
        if lines:
            self.heading(3, "Notes")
            self.emit(*lines)
        return True

    def sec_architecture(self):
        if "architecture" not in self.data:
            return False
        ar = self.data["architecture"]
        if not isinstance(ar, dict):
            self.residual((), "architecture", ar)
            return False
        self.see(("architecture",))
        if "inputs" in ar:
            self.io_block("architecture", "inputs", "Inputs", ar["inputs"])
        if "stack" in ar:
            mark = self.mark()
            try:
                self.heading(3, STACK_TITLE)
                self.records_block(LAYER, ar["stack"], ("architecture", "stack"), 4, "layer")
            except Misfit:
                self.rollback(mark)
                self.residual(("architecture",), "stack", ar["stack"])
        if "outputs" in ar:
            self.io_block("architecture", "outputs", "Outputs", ar["outputs"])
        rest = {k: v for k, v in ar.items() if k not in ("inputs", "stack", "outputs")}
        lines = self.keys_lines(ARCH_NOTES, rest, ("architecture",), 0)
        if lines:
            self.heading(3, "Notes")
            self.emit(*lines)
        return True

    def sec_products(self):
        if "oracle_products" not in self.data:
            return False
        rows = self.data["oracle_products"]
        mark = self.mark()
        try:
            self.records_block(PRODUCT, rows, ("oracle_products",), 3, "id",
                               flatten=(("integration", AT_TIER),), limits=None)
            return True
        except Misfit:
            self.rollback(mark)
            self.residual((), "oracle_products", rows)
            return False

    def sec_metrics(self):
        d = self.data
        wrote = False
        if "kpis_note" in d:
            lines = self.keys_lines(METRICS_TOP, {"kpis_note": d["kpis_note"]}, (), 0)
            if lines:
                self.emit(*lines)
                wrote = True
        if "kpis" in d:
            if self.titled_records(d["kpis"], KPI, ("kpis",), "name"):
                wrote = True
            else:
                self.residual((), "kpis", d["kpis"])
        return wrote

    def tier_titles(self, tiers):
        if not isinstance(tiers, list) or not tiers:
            return None
        out = []
        for t in tiers:
            if not isinstance(t, dict) or not _nice_title(t.get("name")) or "·" in t["name"]:
                return None
            try:
                title = _title_text(t["name"], tuple(PACKAGE_TITLES))
                if "size_tag" in t:
                    tag = t["size_tag"]
                    if not _nice_title(tag) or "·" in tag:
                        return None
                    title += PART + _title_text(tag)
            except Misfit:
                return None
            out.append(title)
        return out

    def sec_packages(self):
        if "packages" not in self.data:
            return False
        pk = self.data["packages"]
        if not isinstance(pk, dict):
            self.residual((), "packages", pk)
            return False
        special = ("tiers",) + tuple(PACKAGE_TITLES.values())
        self.emit(*self.keys_lines(PACKAGES_TOP, pk, ("packages",), 0, skip=special))
        if "tiers" in pk:
            titles = self.tier_titles(pk["tiers"])
            if titles is None:
                self.residual(("packages",), "tiers", pk["tiers"])
            else:
                for i, (tier, title) in enumerate(zip(pk["tiers"], titles)):
                    self.heading(3, title)
                    self.emit(*self.keys_lines(TIER, tier, ("packages", "tiers", i), 0,
                                               skip=("name", "size_tag")))
        for title, key in PACKAGE_TITLES.items():
            if key not in pk:
                continue
            v = pk[key]
            mark = self.mark()
            try:
                self.heading(3, title)
                if key == "capability_handling":
                    self.records_block(HANDLING, v, ("packages", key), 4, "area",
                                       flatten=(("levels", LEVEL_AT), ("glyphs", GLYPH_AT)))
                elif key == "why_it_sells_for_the_partner":
                    if not isinstance(v, list):
                        raise Misfit("not a list")
                    self.emit(*(self.pair_lines(v, ("label", "text"), 0) if v else [NONE]))
                else:
                    if not isinstance(v, dict):
                        raise Misfit("not a mapping")
                    self.emit(*self.keys_lines(BUYER_GETS, v, ("packages", key), 0))
            except Misfit:
                self.rollback(mark)
                self.residual(("packages",), key, v)
        return True

    def sec_proof(self):
        lines = []
        meta = self.data.get("meta")
        if isinstance(meta, dict) and "source_engagement" in meta:
            se = meta["source_engagement"]
            done = False
            if isinstance(se, dict) and se:
                mark = len(self.residuals)
                got = self.keys_lines(SOURCE_ENGAGEMENT, se, ("meta", "source_engagement"), 0)
                if got:
                    lines.extend(got)
                    done = True
                else:
                    del self.residuals[mark:]
            if not done:
                self.residual(("meta",), "source_engagement", se)
        for key, rec in (("deck", PROOF_DECK), ("one_pager", PROOF_ONE_PAGER)):
            v = self.data.get(key)
            if not isinstance(v, dict):
                continue
            for k in rec.keys():
                if k not in v:
                    continue
                mark = len(self.residuals)
                try:
                    lines.extend(self.field_lines(rec.by_key[k], v[k], (key, k), 0))
                    self.elsewhere.add((key, k))
                except Misfit:
                    del self.residuals[mark:]
        self.emit(*lines)
        return bool(lines)

    def sec_next_steps(self):
        ex = self.data.get("exec_summary")
        if not isinstance(ex, dict) or "next_steps" not in ex:
            return False
        steps = ex["next_steps"]
        try:
            if not isinstance(steps, list):
                raise Misfit("not a list")
            lines = self.numbered_lines(steps, ("title", "detail")) if steps else [NONE]
        except Misfit:
            return False
        self.emit(*lines)
        self.elsewhere.add(("exec_summary", "next_steps"))
        return True

    def sec_open_questions(self):
        if "open_questions" not in self.data:
            return False
        qs = self.data["open_questions"]
        mark = self.mark()
        try:
            if not isinstance(qs, list):
                raise Misfit("not a list")
            if not qs:
                self.emit(NONE)
            elif all(isinstance(q, dict) for q in qs):
                if not self.titled_records(qs, QUESTION, ("open_questions",), "id"):
                    raise Misfit("a question with no id")
            else:
                self.emit(*self.numbered_lines(qs))
            return True
        except Misfit:
            self.rollback(mark)
            self.residual((), "open_questions", qs)
            return False

    def channel_rows(self, cna):
        if not isinstance(cna, dict) or not cna:
            raise Misfit("no channels")
        labels = dict(CHANNEL_LABELS)
        seen, out = set(), []
        for ch, ok in cna.items():
            if not isinstance(ch, str):
                raise Misfit("a channel that is not text")
            name = labels.get(ch, ch)
            if ch not in labels and (ch in labels.values() or not _label_ok(ch)):
                raise Misfit("a channel that reads as another")
            if name in seen:
                raise Misfit("a channel twice")
            seen.add(name)
            out.append("| %s | %s |" % (_enc_text_line(name, "cell"),
                                         self.cell(ok, BOOL, False, None)))
        return out

    def sec_settings(self):
        d = self.data
        wrote = False
        if "clearance" in d:
            cl = d["clearance"]
            if isinstance(cl, dict):
                wrote = True
                self.see(("clearance",))
                self.heading(3, "Clearance")
                if "customer_name_allowed" in cl:
                    try:
                        rows = self.channel_rows(cl["customer_name_allowed"])
                        self.emit("| " + " | ".join(CHANNEL_HEADER) + " |", "|---|---|", *rows)
                    except Misfit:
                        self.residual(("clearance",), "customer_name_allowed",
                                      cl["customer_name_allowed"])
                lines = self.keys_lines(CLEARANCE, cl, ("clearance",), 0,
                                        skip=("customer_name_allowed",))
                if lines:
                    self.blank()
                    self.emit(*lines)
            else:
                self.residual((), "clearance", cl)
        for key, title, rec in SETTINGS:
            if key not in d:
                continue
            v = d[key]
            if not isinstance(v, dict):
                self.residual((), key, v)
                continue
            skip = {k for (t, k) in self.elsewhere if t == key}
            if v and all(k in skip for k in v):
                continue
            wrote = True
            self.heading(3, title)
            self.emit(*self.keys_lines(rec, v, (key,), 0, skip=skip))
        return wrote

    def residual_order(self):
        """The Other fields entries in an order that survives the round trip. A key that comes
        back from the block is appended to the end of its mapping, so an order read off the
        data would move; this one places each entry by where its mapping sits among the keys
        that are rendered above (which never move), a mapping's nested entries before its own."""
        own = {}
        for path, key, _ in self.residuals:
            own.setdefault(path, []).append(key)
        late = len(self.seen)

        def sort_key(entry):
            path, key, _ = entry
            cur = self.data
            for seg in path:
                cur = cur[seg]
            mine = own[path]
            rank = [k for k in cur if k in mine].index(key)
            if path in self.seen:
                return (self.seen[path], "", rank)
            return (late, format_path(path), rank)

        return sorted(self.residuals, key=sort_key)

    def write_other_fields(self):
        if not self.residuals:
            return
        mapping = {}
        for path, key, value in self.residual_order():
            if not path and not isinstance(key, str):
                mapping[key] = value
            else:
                mapping[format_path(path, key, has_key=True)] = value
        text = _yaml().dump(mapping, Dumper=_dumper(), allow_unicode=True, sort_keys=False,
                            width=100, default_flow_style=False)
        self.heading(2, "Other fields")
        self.emit("```yaml", *text.rstrip("\n").split("\n"), "```")


def dump(data: dict) -> str:
    """The canonical Markdown of a spec's data."""
    if not isinstance(data, dict):
        raise SpecError("a pack spec is a mapping of components at the top level")
    return _Writer(data).write()


# ============================================================================ the reader
_HEAD_RE = re.compile(r"^(#{1,6}) (.+)$")
_KEY_RE = re.compile(r"^(?P<ind> *)- \*\*(?P<label>(?:[^*\\\n]|\\.)+?):\*\*(?: +(?P<rest>.*))?$")
_PAIR_RE = re.compile(r"^\*\*(?P<label>(?:[^*\\\n]|\\.)+?):\*\*(?: +(?P<rest>.*))?$")
_BULLET_RE = re.compile(r"^(?P<ind> *)-(?: +(?P<rest>.*))?$")
_NUMBERED_RE = re.compile(r"^(?P<num>\d+)\. +(?P<rest>.*)$")
_SEP_RE = re.compile(r"^\|(?:\s*:?-{3,}:?\s*\|)+$")
_FIRST = object()


class _Reader:
    def __init__(self, text: str, source: str):
        self.source = source
        raw = text.split("\n")
        if raw and raw[-1] == "":
            raw.pop()
        self.raw = [ln.rstrip("\r") for ln in raw]
        self.lines = [ln.rstrip() for ln in self.raw]
        self.i = 0
        self.data = {}
        self.lm = LineMap()
        self.lm[()] = 1
        self.lm.starts[()] = 1
        self.overlay = None

    # -- plumbing
    def err(self, message, line=None):
        raise SpecError(message, line if line is not None else self.i + 1, self.source)

    def peek(self):
        return self.lines[self.i] if self.i < len(self.lines) else None

    def skip_blank(self):
        while self.i < len(self.lines) and self.lines[self.i] == "":
            self.i += 1

    def unexpected(self, line):
        shown = line if len(line) <= 72 else line[:69] + "..."
        self.err("this line does not belong here: `%s`" % shown)

    def section_ends(self, line) -> bool:
        return line is None or line.startswith("## ")

    def end_section(self):
        self.skip_blank()
        line = self.peek()
        if not self.section_ends(line):
            self.unexpected(line)

    def put(self, container, key, value, path, line):
        if key in container:
            self.err("`%s` is written twice" % format_path(path[:-1], path[-1], has_key=True), line)
        container[key] = value
        self.lm[path] = line
        if isinstance(value, (dict, list)):
            self.lm.starts[path] = line

    def append(self, items, value, path, line):
        items.append(value)
        p = path + (len(items) - 1,)
        self.lm[p] = line
        if isinstance(value, (dict, list)):
            self.lm.starts[p] = line

    def child(self, container, key, path, line, kind=dict):
        if key in container:
            value = container[key]
            if not isinstance(value, kind):
                self.err("`%s` is written twice" % format_path(path), line)
            return value
        value = kind()
        self.put(container, key, value, path, line)
        return value

    def need_meta(self, line):
        meta = self.data.get("meta")
        if not isinstance(meta, dict):
            self.err("this needs the spec's front matter (--- slug, status … ---) at the top", line)
        return meta

    def heading(self, line):
        m = _HEAD_RE.match(line) if line is not None else None
        return (len(m.group(1)), m.group(2)) if m else None

    def key_match(self, line, indent):
        if line is None:
            return None
        m = _KEY_RE.match(line)
        return m if m and len(m.group("ind")) == indent else None

    def dec_title(self, raw, line):
        return dec_scalar(raw, TEXT, line, self.source, "the heading")

    def dec_cell(self, raw, kind, line, what):
        m = _HATCH_RE.match(raw)
        if m:
            return _unhatch(m.group(1).replace("\\|", "|"), line, self.source)
        return dec_scalar(raw, kind, line, self.source, what)

    # -- values
    def is_continuation(self, line, col) -> bool:
        if line is None or line == "":
            return False
        indent = len(line) - len(line.lstrip(" "))
        if indent < col:
            return False
        content = line.lstrip(" ")
        return not (content == "-" or content.startswith("- "))

    def read_continuation(self, col):
        out = []
        while True:
            line = self.peek()
            if line is None:
                break
            if line == "":
                j = self.i
                while j < len(self.lines) and self.lines[j] == "":
                    j += 1
                if j < len(self.lines) and self.is_continuation(self.lines[j], col):
                    out.extend([""] * (j - self.i))
                    self.i = j
                    continue
                break
            if not self.is_continuation(line, col):
                break
            out.append(line.lstrip(" "))
            self.i += 1
        return out

    def dec_inline(self, lines, f: F, line):
        if len(lines) == 1 and not _has_break_mark(lines[0]):
            kind = f.kind if (f.kind in SCALAR_KINDS or f.kind in (LIST, TLIST)) else TEXT
            return dec_scalar(lines[0], kind, line, self.source, "`%s`" % f.label)
        if f.kind not in (TEXT, TLIST, RECORD, MAP, PAIRS, RECORDS):
            self.err("`%s` takes its value on one line" % f.label, line)
        return _dec_text_lines(lines)

    def dec_item(self, lines, line):
        if len(lines) == 1 and not _has_break_mark(lines[0]):
            return dec_scalar(lines[0], TEXT, line, self.source, "the item")
        return _dec_text_lines(lines)

    def resolver(self, rec: Rec, container, cpath):
        def resolve(label, line):
            f = rec.by_label.get(label)
            if f is None:
                self.err("`%s` is not a field here — the fields are: %s"
                         % (label, ", ".join(rec.by_label)), line)
            return f, container, cpath
        return resolve

    def read_keys(self, resolve, indent):
        while True:
            line = self.peek()
            if line is None:
                return
            if line == "" and indent == 0:
                j = self.i
                while j < len(self.lines) and self.lines[j] == "":
                    j += 1
                if j < len(self.lines) and self.key_match(self.lines[j], 0):
                    self.i = j
                    continue
                return
            m = self.key_match(line, indent)
            if not m:
                return
            ln = self.i + 1
            f, container, cpath = resolve(_unesc_inline(m.group("label")), ln)
            self.i += 1
            path = cpath + (f.key,)
            value = self.read_value(f, m.group("rest"), indent, path, ln)
            self.put(container, f.key, value, path, ln)

    def read_value(self, f: F, rest, indent, path, ln):
        if rest is not None:
            lines = [rest] + self.read_continuation(indent + 2)
            return self.dec_inline(lines, f, ln)
        kind = f.kind
        if kind == RECORD:
            out = {}
            self.read_keys(self.resolver(f.rec, out, path), indent + 2)
            return out
        if kind == MAP:
            out = {}
            self.read_map(out, path, indent + 2)
            return out
        if kind in (LIST, TLIST):
            items = self.read_bullets(indent + 2, path)
        elif kind == PAIRS:
            items = self.read_pairs(indent + 2, f.pair, path)
        elif kind == RECORDS:
            items = self.read_records(indent + 2, f.rec, path)
        else:
            self.err("`%s` has no value" % f.label, ln)
        if not items:
            self.err("`%s` has neither a value nor items under it — an empty list is `(none)`"
                     % f.label, ln)
        return items

    def read_map(self, out, path, indent):
        while True:
            m = self.key_match(self.peek(), indent)
            if not m:
                return
            ln = self.i + 1
            key = _unesc_inline(m.group("label"))
            self.i += 1
            if m.group("rest") is None:
                self.err("`%s` has no value" % key, ln)
            lines = [m.group("rest")] + self.read_continuation(indent + 2)
            self.put(out, key, self.dec_inline(lines, F(key, key), ln), path + (key,), ln)

    def read_plain_item(self, items, path, indent, rest, ln):
        if rest is None:
            self.err("an empty list item", ln)
        lines = [rest] + self.read_continuation(indent + 2)
        self.append(items, self.dec_item(lines, ln), path, ln)

    def read_bullets(self, indent, path):
        items = []
        while True:
            line = self.peek()
            m = _BULLET_RE.match(line) if line is not None else None
            if not m or len(m.group("ind")) != indent:
                return items
            ln = self.i + 1
            self.i += 1
            self.read_plain_item(items, path, indent, m.group("rest"), ln)

    def read_pairs(self, indent, pair, path):
        k1, k2 = pair
        items = []
        while True:
            line = self.peek()
            b = _BULLET_RE.match(line) if line is not None else None
            if not b or len(b.group("ind")) != indent:
                return items
            ln = self.i + 1
            self.i += 1
            m = self.key_match(line, indent)
            if not m:
                self.read_plain_item(items, path, indent, b.group("rest"), ln)
                continue
            label = _unesc_inline(m.group("label"))
            if m.group("rest") is None:
                self.err("`%s` has no text after it" % label, ln)
            lines = [m.group("rest")] + self.read_continuation(indent + 2)
            item = {k1: label, k2: self.dec_inline(lines, F(k2, k2), ln)}
            self.append(items, item, path, ln)
            idx = len(items) - 1
            self.lm[path + (idx, k1)] = ln
            self.lm[path + (idx, k2)] = ln

    def read_records(self, indent, rec, path):
        items = []
        while True:
            line = self.peek()
            b = _BULLET_RE.match(line) if line is not None else None
            if not b or len(b.group("ind")) != indent:
                return items
            ln = self.i + 1
            m = self.key_match(line, indent)
            if not m and b.group("rest") is not None:
                self.i += 1
                self.read_plain_item(items, path, indent, b.group("rest"), ln)
                continue
            item = {}
            self.append(items, item, path, ln)
            ipath = path + (len(items) - 1,)
            self.i += 1
            if m:
                label = _unesc_inline(m.group("label"))
                f = rec.by_label.get(label)
                if f is None:
                    self.err("`%s` is not a field here — the fields are: %s"
                             % (label, ", ".join(rec.by_label)), ln)
                if m.group("rest") is None:
                    self.err("a list item's first field carries its value on the bullet; "
                             "start the item with a bare `-` when that field nests", ln)
                value = self.read_value(f, m.group("rest"), indent, ipath + (f.key,), ln)
                self.put(item, f.key, value, ipath + (f.key,), ln)
            self.read_keys(self.resolver(rec, item, ipath), indent + 2)

    def read_numbered(self, path, pair=None):
        items = []
        while True:
            j = self.i
            while j < len(self.lines) and self.lines[j] == "":
                j += 1
            line = self.lines[j] if j < len(self.lines) else None
            m = _NUMBERED_RE.match(line) if line is not None else None
            if not m:
                return items
            self.i = j + 1
            ln = j + 1
            rest, col = m.group("rest"), len(m.group("num")) + 2
            pm = _PAIR_RE.match(rest) if pair else None
            if pm:
                label = _unesc_inline(pm.group("label"))
                if pm.group("rest") is None:
                    self.err("`%s` has no text after it" % label, ln)
                lines = [pm.group("rest")] + self.read_continuation(col)
                item = {pair[0]: label, pair[1]: self.dec_inline(lines, F(pair[1], pair[1]), ln)}
                self.append(items, item, path, ln)
                self.lm[path + (len(items) - 1, pair[0])] = ln
                self.lm[path + (len(items) - 1, pair[1])] = ln
                continue
            lines = [rest] + self.read_continuation(col)
            self.append(items, self.dec_item(lines, ln), path, ln)

    def read_paragraph(self):
        lines, start = [], self.i + 1
        while True:
            line = self.peek()
            if line is None or _HEAD_RE.match(line) or self.key_match(line, 0) \
                    or line.startswith("|") or line.startswith("```"):
                break
            lines.append(line.lstrip(" "))
            self.i += 1
        while lines and lines[-1] == "":
            lines.pop()
        if not lines:
            return None, None
        if len(lines) == 1 and not _has_break_mark(lines[0]):
            return dec_scalar(lines[0], TEXT, start, self.source, "the text"), start
        return _dec_text_lines(lines), start

    # -- tables
    def split_row(self, line, ln):
        s = line.strip()
        if not s.startswith("|"):
            self.err("a table row starts with `|`", ln)
        cells, cur, i, n, closed = [], [], 1, len(s), False
        while i < n:
            c = s[i]
            if c == "\\" and i + 1 < n:
                cur.append(s[i:i + 2])
                i += 2
                continue
            if c == "|":
                cells.append("".join(cur).strip())
                cur = []
                closed = i == n - 1
                i += 1
                continue
            cur.append(c)
            closed = False
            i += 1
        if not closed:
            self.err("a table row ends with `|`", ln)
        return cells

    def read_table(self):
        hl = self.i + 1
        header = self.split_row(self.peek(), hl)
        self.i += 1
        sep = self.peek()
        if sep is None or not _SEP_RE.match(sep):
            self.err("a table's second line is its separator, `|---|---|`", self.i + 1)
        if len(self.split_row(sep, self.i + 1)) != len(header):
            self.err("the separator has a different number of cells than the header", self.i + 1)
        self.i += 1
        body = []
        while True:
            line = self.peek()
            if line is None or not line.startswith("|"):
                break
            ln = self.i + 1
            cells = self.split_row(line, ln)
            if len(cells) != len(header):
                self.err("this row has %d cells and the header %d — a cell is missing, or a `|` "
                         "inside a cell is not written `\\|`" % (len(cells), len(header)), ln)
            body.append((ln, cells))
            self.i += 1
        return hl, header, body

    def columns(self, header, rec: Rec, flatten, first, hl):
        flat_labels = {}
        for key, sub in flatten:
            for s in sub.fields:
                flat_labels[s.label] = (key, s.key)
        flat_keys = {key for key, _ in flatten}
        cols, seen = [], set()
        for idx, h in enumerate(header):
            text = _unesc_inline(h)
            if first and idx == 0:
                if text != first:
                    self.err("the first column of this table is `%s`" % first, hl)
                cols.append((TEXT, _FIRST, text))
                continue
            if text in flat_labels:
                col = (TEXT, flat_labels[text], text)
            elif text in rec.by_label:
                f = rec.by_label[text]
                if f.key in flat_keys:
                    self.err("`%s` is written as one column per tier here" % text, hl)
                kind = f.kind if (f.kind in SCALAR_KINDS or f.kind == LIST) else TEXT
                col = (kind, f.key, text)
            else:
                if not text:
                    self.err("a column with no header", hl)
                col = (TEXT, text, text)
            if col[1] in seen:
                self.err("the column `%s` appears twice" % text, hl)
            seen.add(col[1])
            cols.append(col)
        return cols

    def fill_row(self, row, cols, cells, rpath, ln):
        for (kind, key, label), raw in zip(cols, cells):
            if key is _FIRST or raw == "":
                continue
            value = self.dec_cell(raw, kind, ln, "`%s`" % label)
            if isinstance(key, tuple):
                sub = self.child(row, key[0], rpath + (key[0],), ln)
                self.put(sub, key[1], value, rpath + key, ln)
            else:
                self.put(row, key, value, rpath + (key,), ln)

    def read_records_block(self, container, key, path, rec, level, title_key, hl, flatten=()):
        self.skip_blank()
        line = self.peek()
        rows = []
        self.put(container, key, rows, path, hl)
        if line == NONE:
            self.i += 1
            return
        if line is not None and line.startswith("|"):
            thl, header, body = self.read_table()
            cols = self.columns(header, rec, flatten, None, thl)
            for ln, cells in body:
                row = {}
                self.append(rows, row, path, ln)
                self.fill_row(row, cols, cells, path + (len(rows) - 1,), ln)
            return
        b = _BULLET_RE.match(line) if line is not None else None
        if b and not b.group("ind"):
            while True:
                line = self.peek()
                b = _BULLET_RE.match(line) if line is not None else None
                if not b or b.group("ind"):
                    return
                ln = self.i + 1
                self.i += 1
                self.read_plain_item(rows, path, 0, b.group("rest"), ln)
        while True:
            self.skip_blank()
            h = self.heading(self.peek())
            if not h or h[0] != level:
                break
            ln = self.i + 1
            self.i += 1
            item = {}
            self.append(rows, item, path, ln)
            ipath = path + (len(rows) - 1,)
            self.put(item, title_key, self.dec_title(h[1], ln), ipath + (title_key,), ln)
            self.skip_blank()
            self.read_keys(self.resolver(rec, item, ipath), 0)
        if not rows:
            self.err("nothing under this heading — write a table, the rows as `%s` headings, or "
                     "`(none)`" % ("#" * level), hl)

    # -- the document
    def parse(self):
        self.skip_blank()
        if self.peek() == "---":
            self.read_front_matter()
        self.skip_blank()
        line = self.peek()
        if line is not None and line.startswith("# "):
            ln = self.i + 1
            meta = self.need_meta(ln)
            self.put(meta, "name", self.dec_title(line[2:], ln), ("meta", "name"), ln)
            self.i += 1
        self.skip_blank()
        if self.key_match(self.peek(), 0):
            meta = self.need_meta(self.i + 1)

            def resolve(label, ln):
                if label in NAME_VARIANTS.by_label:
                    nv = self.child(meta, "name_variants", ("meta", "name_variants"), ln)
                    return NAME_VARIANTS.by_label[label], nv, ("meta", "name_variants")
                if label in META_H1.by_label:
                    return META_H1.by_label[label], meta, ("meta",)
                self.err("`%s` does not belong under the name — it takes %s"
                         % (label, ", ".join(list(NAME_VARIANTS.by_label) + list(META_H1.by_label))), ln)
            self.read_keys(resolve, 0)
        handlers = {
            "One-liner": self.sec_one_liner, "Problem and solution": self.sec_problem_solution,
            "Who buys it": self.sec_icp, "Industries": self.sec_industries,
            "Capabilities": self.sec_capabilities, "Workflow": self.sec_workflow,
            "Architecture": self.sec_architecture, "Oracle products": self.sec_products,
            "Metrics": self.sec_metrics, "Packages": self.sec_packages, "Proof": self.sec_proof,
            "Next steps": self.sec_next_steps, "Open questions": self.sec_open_questions,
            "Settings": self.sec_settings, "Other fields": self.sec_other,
        }
        seen = set()
        while True:
            self.skip_blank()
            line = self.peek()
            if line is None:
                break
            m = re.match(r"^## (.+)$", line)
            if not m:
                self.unexpected(line)
            title = m.group(1)
            if title not in handlers:
                self.err("unknown section `## %s` — the sections are: %s"
                         % (title, ", ".join(SECTIONS)))
            if title in seen:
                self.err("the section `## %s` appears twice" % title)
            seen.add(title)
            ln = self.i + 1
            self.i += 1
            handlers[title](ln)
        self.apply_overlay()
        return self.data, self.lm

    def read_front_matter(self):
        start = self.i + 1
        self.i += 1
        body_start = self.i
        while True:
            line = self.peek()
            if line is None:
                self.err("the front matter opened here is not closed with `---`", start)
            if line == "---":
                break
            self.i += 1
        text = "\n".join(self.raw[body_start:self.i])
        self.i += 1
        fm, lm = loads_yaml(text, self.source, offset=body_start)
        if fm is None:
            fm = {}
        if not isinstance(fm, dict):
            self.err("the front matter is `key: value` lines", start)
        meta = {}
        self.put(self.data, "meta", meta, ("meta",), start)
        for k, v in fm.items():
            kl = lm.get((k,), start)
            if k not in FRONT_KEYS:
                self.err("`%s` does not belong in the front matter — it carries %s"
                         % (k, ", ".join(FRONT_KEYS)), kl)
            self.put(meta, k, v, ("meta", k), kl)
            for p, n in lm.items():
                if len(p) > 1 and p[0] == k:
                    self.lm[("meta",) + p] = n
            for p, n in lm.starts.items():
                if len(p) > 1 and p[0] == k:
                    self.lm.starts[("meta",) + p] = n

    def dict_section(self, key, rec, ln, paragraphs=(), lead=None):
        out = self.child(self.data, key, (key,), ln)
        path = (key,)
        paras = {title: k for k, title in paragraphs}
        first = True
        while True:
            self.skip_blank()
            line = self.peek()
            if self.section_ends(line):
                return
            h = self.heading(line)
            if h and h[0] == 3 and h[1] in paras:
                hl = self.i + 1
                self.i += 1
                self.skip_blank()
                value, pl = self.read_paragraph()
                if pl is None:
                    self.err("`### %s` has no text under it" % h[1], hl)
                self.put(out, paras[h[1]], value, path + (paras[h[1]],), pl)
            elif self.key_match(line, 0):
                self.read_keys(self.resolver(rec, out, path), 0)
            elif lead and first and not h:
                value, pl = self.read_paragraph()
                self.put(out, lead, value, path + (lead,), pl)
            else:
                self.unexpected(line)
            first = False

    def sec_one_liner(self, ln):
        self.dict_section("one_liner", ONE_LINER, ln)

    def sec_problem_solution(self, ln):
        self.dict_section("problem_solution", PROBLEM_SOLUTION, ln, paragraphs=PS_PARAGRAPHS)

    def sec_icp(self, ln):
        self.dict_section("icp", ICP, ln, lead="line")

    def none_list(self, container, key, path):
        """`(none)` at a section's level: an empty list, and nothing else of that list after it."""
        if key in container:
            self.err("`(none)` after items of the same list")
        self.put(container, key, [], path, self.i + 1)
        self.i += 1

    def titled_record(self, container, key, path, rec, title_key, raw, hl, emptied):
        if emptied:
            self.err("a heading after `(none)` — the list is either empty or it has items", hl)
        rows = self.child(container, key, path, hl, list)
        item = {}
        self.append(rows, item, path, hl)
        ipath = path + (len(rows) - 1,)
        self.put(item, title_key, self.dec_title(raw, hl), ipath + (title_key,), hl)
        self.skip_blank()
        self.read_keys(self.resolver(rec, item, ipath), 0)

    def sec_industries(self, ln):
        emptied = False
        while True:
            self.skip_blank()
            line = self.peek()
            if self.section_ends(line):
                return
            if line == NONE:
                self.none_list(self.data, "verticals", ("verticals",))
                emptied = True
                continue
            h = self.heading(line)
            if not h or h[0] != 3:
                self.unexpected(line)
            hl = self.i + 1
            self.i += 1
            if h[1] == "Held out":
                d = self.child(self.data, "verticals_held_out", ("verticals_held_out",), hl)
                self.skip_blank()
                self.read_keys(self.resolver(HELD_OUT, d, ("verticals_held_out",)), 0)
            elif h[1] == "Rejected":
                self.read_records_block(self.data, "verticals_rejected", ("verticals_rejected",),
                                        REJECTED, 4, "name", hl)
            else:
                self.titled_record(self.data, "verticals", ("verticals",), VERTICAL, "name",
                                   h[1], hl, emptied)

    def sec_capabilities(self, ln):
        emptied = False
        path = ("capabilities",)
        while True:
            self.skip_blank()
            line = self.peek()
            if self.section_ends(line):
                return
            if line == NONE:
                self.none_list(self.data, "capabilities", path)
                emptied = True
                continue
            h = self.heading(line)
            if not h or h[0] != 3:
                self.unexpected(line)
            hl = self.i + 1
            self.i += 1
            if emptied:
                self.err("a heading after `(none)` — the list is either empty or it has items", hl)
            areas = self.child(self.data, "capabilities", path, hl, list)
            area = {}
            self.append(areas, area, path, hl)
            apath = path + (len(areas) - 1,)
            self.put(area, "area", self.dec_title(h[1], hl), apath + ("area",), hl)
            self.skip_blank()
            self.read_keys(self.resolver(AREA, area, apath), 0)
            self.skip_blank()
            if (self.peek() or "").startswith("|"):
                self.read_feature_tables(area, apath)

    def read_feature_tables(self, area, apath):
        hl, header, body = self.read_table()
        cols = self.columns(header, FEATURE_COLUMNS, (), "Category", hl)
        cats, index = [], {}
        cpath = apath + ("categories",)
        self.put(area, "categories", cats, cpath, hl)
        current = None
        for ln, cells in body:
            if cells[0] == "":
                self.err("a feature row names its category in the first cell", ln)
            name = self.dec_cell(cells[0], TEXT, ln, "the category")
            if not isinstance(name, str):
                self.err("a category's name is text", ln)
            if current is None or current["name"] != name:
                if name in index:
                    self.err("the category `%s` appears again after another — keep its rows "
                             "together" % name, ln)
                current = {}
                self.append(cats, current, cpath, ln)
                ci = len(cats) - 1
                index[name] = ci
                self.put(current, "name", name, cpath + (ci, "name"), ln)
                self.put(current, "features", [], cpath + (ci, "features"), ln)
            ci = index[name]
            feat = {}
            self.append(current["features"], feat, cpath + (ci, "features"), ln)
            self.fill_row(feat, cols, cells, cpath + (ci, "features", len(current["features"]) - 1), ln)
        self.skip_blank()
        if not (self.peek() or "").startswith("|"):
            return
        hl, header, body = self.read_table()
        cols = self.columns(header, CATEGORY_COLUMNS, (), "Category", hl)
        for ln, cells in body:
            name = self.dec_cell(cells[0], TEXT, ln, "the category") if cells[0] else None
            if name not in index:
                self.err("the category `%s` has no feature rows above" % name, ln)
            self.fill_row(cats[index[name]], cols, cells, cpath + (index[name],), ln)

    def io_or_notes(self, container, cpath, raw, hl, notes_rec, stack):
        """Workflow and Architecture share their subsections."""
        if raw in ("Inputs", "Outputs"):
            key = raw.lower()
            self.read_records_block(container, key, cpath + (key,), IO, 4, "system", hl)
            return True
        if stack and raw == STACK_TITLE:
            self.read_records_block(container, "stack", cpath + ("stack",), LAYER, 4, "layer", hl)
            return True
        if raw == "Notes":
            self.skip_blank()
            self.read_keys(self.resolver(notes_rec, container, cpath), 0)
            return True
        return False

    def sec_workflow(self, ln):
        wf = self.child(self.data, "workflow", ("workflow",), ln)
        path = ("workflow",)
        while True:
            self.skip_blank()
            line = self.peek()
            if self.section_ends(line):
                return
            h = self.heading(line)
            if not h or h[0] != 3:
                self.unexpected(line)
            hl = self.i + 1
            self.i += 1
            if self.io_or_notes(wf, path, h[1], hl, WORKFLOW_NOTES, False):
                continue
            steps = self.child(wf, "steps", path + ("steps",), hl, list)
            step = {}
            self.append(steps, step, path + ("steps",), hl)
            spath = path + ("steps", len(steps) - 1)
            m = re.fullmatch(r"(\d+)\.(?: (.*))?", h[1])
            if m:
                self.put(step, "n", int(m.group(1)), spath + ("n",), hl)
                if m.group(2) is not None:
                    self.put(step, "name", self.dec_title(m.group(2), hl), spath + ("name",), hl)
            else:
                self.put(step, "name", self.dec_title(h[1], hl), spath + ("name",), hl)
            self.skip_blank()
            self.read_keys(self.resolver(STEP, step, spath), 0)

    def sec_architecture(self, ln):
        ar = self.child(self.data, "architecture", ("architecture",), ln)
        while True:
            self.skip_blank()
            line = self.peek()
            if self.section_ends(line):
                return
            h = self.heading(line)
            if not h or h[0] != 3:
                self.unexpected(line)
            hl = self.i + 1
            self.i += 1
            if not self.io_or_notes(ar, ("architecture",), h[1], hl, ARCH_NOTES, True):
                self.err("unknown subsection `### %s` — Architecture has Inputs, %s, Outputs "
                         "and Notes" % (h[1], STACK_TITLE), hl)

    def sec_products(self, ln):
        self.read_records_block(self.data, "oracle_products", ("oracle_products",), PRODUCT, 3,
                                "id", ln, flatten=(("integration", AT_TIER),))
        self.end_section()

    def sec_metrics(self, ln):
        emptied = False
        while True:
            self.skip_blank()
            line = self.peek()
            if self.section_ends(line):
                return
            if self.key_match(line, 0):
                self.read_keys(self.resolver(METRICS_TOP, self.data, ()), 0)
                continue
            if line == NONE:
                self.none_list(self.data, "kpis", ("kpis",))
                emptied = True
                continue
            h = self.heading(line)
            if not h or h[0] != 3:
                self.unexpected(line)
            hl = self.i + 1
            self.i += 1
            self.titled_record(self.data, "kpis", ("kpis",), KPI, "name", h[1], hl, emptied)

    def sec_packages(self, ln):
        pk = self.child(self.data, "packages", ("packages",), ln)
        path = ("packages",)
        while True:
            self.skip_blank()
            line = self.peek()
            if self.section_ends(line):
                return
            if self.key_match(line, 0):
                self.read_keys(self.resolver(PACKAGES_TOP, pk, path), 0)
                continue
            h = self.heading(line)
            if not h or h[0] != 3:
                self.unexpected(line)
            hl = self.i + 1
            self.i += 1
            key = PACKAGE_TITLES.get(h[1])
            if key == "capability_handling":
                self.read_records_block(pk, key, path + (key,), HANDLING, 4, "area", hl,
                                        flatten=(("levels", LEVEL_AT), ("glyphs", GLYPH_AT)))
            elif key == "why_it_sells_for_the_partner":
                self.skip_blank()
                if self.peek() == NONE:
                    self.put(pk, key, [], path + (key,), hl)
                    self.i += 1
                    continue
                items = self.read_pairs(0, ("label", "text"), path + (key,))
                if not items:
                    self.err("nothing under this heading — write the reasons as bullets, or "
                             "`(none)`", hl)
                self.put(pk, key, items, path + (key,), hl)
            elif key == "what_each_buyer_gets":
                d = self.child(pk, key, path + (key,), hl)
                self.skip_blank()
                self.read_keys(self.resolver(BUYER_GETS, d, path + (key,)), 0)
            else:
                tiers = self.child(pk, "tiers", path + ("tiers",), hl, list)
                tier = {}
                self.append(tiers, tier, path + ("tiers",), hl)
                tpath = path + ("tiers", len(tiers) - 1)
                name_raw, sep, tag_raw = h[1].rpartition(PART)
                if sep:
                    self.put(tier, "name", self.dec_title(name_raw, hl), tpath + ("name",), hl)
                    self.put(tier, "size_tag", self.dec_title(tag_raw, hl), tpath + ("size_tag",), hl)
                else:
                    self.put(tier, "name", self.dec_title(h[1], hl), tpath + ("name",), hl)
                self.skip_blank()
                self.read_keys(self.resolver(TIER, tier, tpath), 0)

    def sec_proof(self, ln):
        def resolve(label, line):
            if label in SOURCE_ENGAGEMENT.by_label:
                meta = self.need_meta(line)
                se = self.child(meta, "source_engagement", ("meta", "source_engagement"), line)
                return SOURCE_ENGAGEMENT.by_label[label], se, ("meta", "source_engagement")
            for key, rec in (("deck", PROOF_DECK), ("one_pager", PROOF_ONE_PAGER)):
                if label in rec.by_label:
                    return rec.by_label[label], self.child(self.data, key, (key,), line), (key,)
            self.err("`%s` is not a field of the Proof section — it takes %s"
                     % (label, ", ".join(list(SOURCE_ENGAGEMENT.by_label) + list(PROOF_DECK.by_label)
                                         + list(PROOF_ONE_PAGER.by_label))), line)
        self.skip_blank()
        self.read_keys(resolve, 0)
        self.end_section()

    def sec_next_steps(self, ln):
        ex = self.child(self.data, "exec_summary", ("exec_summary",), ln)
        path = ("exec_summary", "next_steps")
        self.skip_blank()
        if self.peek() == NONE:
            self.put(ex, "next_steps", [], path, self.i + 1)
            self.i += 1
        else:
            items = self.read_numbered(path, ("title", "detail"))
            if not items:
                self.err("Next steps holds a numbered list, or `(none)`", ln)
            self.put(ex, "next_steps", items, path, ln)
        self.end_section()

    def sec_open_questions(self, ln):
        path = ("open_questions",)
        self.skip_blank()
        line = self.peek()
        if line == NONE:
            self.none_list(self.data, "open_questions", path)
        elif line is not None and _NUMBERED_RE.match(line):
            items = self.read_numbered(path)
            self.put(self.data, "open_questions", items, path, ln)
        else:
            while True:
                self.skip_blank()
                h = self.heading(self.peek())
                if not h or h[0] != 3:
                    break
                hl = self.i + 1
                self.i += 1
                self.titled_record(self.data, "open_questions", path, QUESTION, "id", h[1], hl, False)
            if "open_questions" not in self.data:
                self.err("Open questions holds a numbered list, `###` questions, or `(none)`", ln)
        self.end_section()

    def sec_settings(self, ln):
        titles = {title: (key, rec) for key, title, rec in SETTINGS}
        seen = set()
        while True:
            self.skip_blank()
            line = self.peek()
            if self.section_ends(line):
                return
            h = self.heading(line)
            if not h or h[0] != 3:
                self.unexpected(line)
            hl = self.i + 1
            if h[1] in seen:
                self.err("`### %s` appears twice" % h[1], hl)
            seen.add(h[1])
            self.i += 1
            if h[1] == "Clearance":
                self.read_clearance(hl)
            elif h[1] in titles:
                key, rec = titles[h[1]]
                d = self.child(self.data, key, (key,), hl)
                self.skip_blank()
                self.read_keys(self.resolver(rec, d, (key,)), 0)
            else:
                self.err("unknown subsection `### %s` — Settings has Clearance, %s"
                         % (h[1], ", ".join(t for _, t, _ in SETTINGS)), hl)

    def read_clearance(self, hl):
        cl = self.child(self.data, "clearance", ("clearance",), hl)
        self.skip_blank()
        if (self.peek() or "").startswith("|"):
            thl, header, body = self.read_table()
            if [_unesc_inline(h) for h in header] != CHANNEL_HEADER:
                self.err("the clearance table's columns are | %s |" % " | ".join(CHANNEL_HEADER), thl)
            path = ("clearance", "customer_name_allowed")
            cna = {}
            self.put(cl, "customer_name_allowed", cna, path, thl)
            labels = {label: key for key, label in CHANNEL_LABELS}
            for ln, cells in body:
                if not cells[0] or not cells[1]:
                    self.err("a channel row names the channel and says yes or no", ln)
                name = self.dec_cell(cells[0], TEXT, ln, "the channel")
                if not isinstance(name, str):
                    self.err("a channel's name is text", ln)
                key = labels.get(name, name)
                self.put(cna, key, self.dec_cell(cells[1], BOOL, ln, "`Customer may be named`"),
                         path + (key,), ln)
        self.skip_blank()
        self.read_keys(self.resolver(CLEARANCE, cl, ("clearance",)), 0)

    def sec_other(self, ln):
        self.skip_blank()
        if self.peek() != "```yaml":
            self.err("Other fields holds one ```yaml block")
        start = self.i + 1
        self.i += 1
        body_start = self.i
        while True:
            line = self.peek()
            if line is None:
                self.err("the ```yaml block opened here is not closed with ```", start)
            if line == "```":
                break
            self.i += 1
        text = "\n".join(self.raw[body_start:self.i])
        self.i += 1
        data, lm = loads_yaml(text, self.source, offset=body_start)
        if data is None:
            data = {}
        if not isinstance(data, dict):
            self.err("the Other fields block is a mapping of key path: value", start)
        self.overlay = (data, lm, start)
        self.end_section()

    def apply_overlay(self):
        if not self.overlay:
            return
        data, lm, start = self.overlay
        for key, value in data.items():
            ln = lm.get((key,), start)
            if isinstance(key, str):
                try:
                    segs = parse_path(key)
                except ValueError as exc:
                    self.err("Other fields: %s" % exc, ln)
                if any(kind == "select" for kind, _ in segs):
                    self.err("Other fields: `%s` names a list item by position, like [0]" % key, ln)
            else:
                segs = [("key", key)]
            parent, ppath = self.data, ()
            for kind, seg in segs[:-1]:
                if kind == "index":
                    if not isinstance(parent, list) or not 0 <= seg < len(parent):
                        self.err("Other fields: `%s` names a list item the spec does not have" % key, ln)
                elif not isinstance(parent, dict) or seg not in parent:
                    self.err("Other fields: `%s` needs `%s` above it first"
                             % (key, format_path(ppath, seg, has_key=True)), ln)
                parent = parent[seg]
                ppath += (seg,)
            kind, last = segs[-1]
            if kind != "key" or not isinstance(parent, dict):
                self.err("Other fields: `%s` does not name a key of a mapping" % key, ln)
            if last in parent:
                self.err("Other fields: `%s` is also written above" % key, ln)
            parent[last] = value
            path = ppath + (last,)
            self.lm[path] = ln
            for p, n in lm.items():
                if len(p) > 1 and p[0] == key:
                    self.lm[path + p[1:]] = n
            for p, n in lm.starts.items():
                if p and p[0] == key:
                    self.lm.starts[path + p[1:]] = n


def loads_markdown(text: str, source: str = "<string>"):
    """(data, linemap) of Markdown spec text."""
    return _Reader(text, source).parse()


# ============================================================================ the loader
def _check_shape(data, source):
    if data is None or data == {}:
        raise SpecError("the spec is empty", 1, source)
    if not isinstance(data, dict):
        raise SpecError("a pack spec is a mapping of components at the top level", 1, source)


def spec_format(path) -> str:
    """"md", by the file's extension; anything else is not a pack spec."""
    if os.path.splitext(str(path))[1].lower() == ".md":
        return "md"
    raise SpecError("a pack spec is a .md file", None, str(path))


def loads(text: str, source: str = "<string>"):
    """(data, linemap) of a Markdown spec's text."""
    data, linemap = loads_markdown(text, source)
    _check_shape(data, source)
    return data, linemap



def load(path):
    """(data, linemap) of the spec at `path`. Raises SpecError, or OSError when unreadable."""
    path = str(path)
    spec_format(path)
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    return loads(text, source=path)


def canonical_json(data) -> str:
    """The spec's data as sorted JSON: what the artifact stamp hashes."""
    try:
        return json.dumps(data, sort_keys=True, default=str)
    except TypeError:                       # keys of mixed types cannot be sorted
        def textkeys(v):
            if isinstance(v, dict):
                return {repr(k): textkeys(x) for k, x in v.items()}
            if isinstance(v, list):
                return [textkeys(x) for x in v]
            return v
        return json.dumps(textkeys(data), sort_keys=True, default=str)


def data_sha(path) -> str:
    """sha256 of the spec's canonical data, first 12 hex characters — not of its bytes, so a
    re-render or a whitespace edit never changes it."""
    data, _ = load(path)
    return hashlib.sha256(canonical_json(data).encode("utf-8")).hexdigest()[:12]


def differences(a, b, path=(), limit=10):
    """Paths where two specs' data differ (at most `limit`)."""
    out = []

    def walk(x, y, p):
        if len(out) >= limit:
            return
        if isinstance(x, dict) and isinstance(y, dict):
            for k in list(x) + [k for k in y if k not in x]:
                if k not in x or k not in y:
                    out.append(format_path(p, k, has_key=True) + (" (only in the first)" if k in x
                                                                   else " (only in the second)"))
                else:
                    walk(x[k], y[k], p + (k,))
        elif isinstance(x, list) and isinstance(y, list):
            if len(x) != len(y):
                out.append("%s (%d items against %d)" % (format_path(p) or "(top)", len(x), len(y)))
            for i, (u, v) in enumerate(zip(x, y)):
                walk(u, v, p + (i,))
        elif x != y or type(x) is not type(y):
            out.append("%s (%r against %r)" % (format_path(p) or "(top)", x, y))

    walk(a, b, tuple(path))
    return out


def roundtrip_problems(data, source="<spec>"):
    """[] when load(dump(data)) == data and the dump is canonical; else what went wrong."""
    try:
        text = dump(data)
        back, _ = loads(text, source)
    except SpecError as exc:
        return ["the rendered Markdown does not parse: %s" % exc]
    if back != data:
        return ["the round trip changes the data: %s" % "; ".join(differences(data, back))]
    if dump(back) != text:
        return ["the rendered Markdown is not canonical"]
    return []


# ============================================================================ the command line
def _write_atomic(path, text):
    folder = os.path.dirname(os.path.abspath(path)) or "."
    fd, tmp = tempfile.mkstemp(prefix=".packspec-", suffix=".md", dir=folder)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def _select(items, selector):
    for i, item in enumerate(items):
        if isinstance(item, dict):
            for key in ("id", "name", "area", "layer", "n"):
                if key in item and str(item[key]) == str(selector):
                    return i
    return None


def resolve_path(data, segs, create=False):
    """(container, key, plain path) for a parsed key path. With `create`, missing mappings on
    the way are made, and an index one past the end appends a new mapping."""
    parent, plain = data, ()
    for n, (kind, seg) in enumerate(segs):
        last = n == len(segs) - 1
        if kind == "key":
            if not isinstance(parent, dict):
                raise KeyError("%s is not a mapping" % (format_path(plain) or "the spec"))
            key = seg
            if last:
                return parent, key, plain + (key,)
            if key not in parent:
                if not create or segs[n + 1][0] != "key":
                    raise KeyError("the spec has no %s" % format_path(plain, key, has_key=True))
                parent[key] = {}
        else:
            if not isinstance(parent, list):
                raise KeyError("%s is not a list" % (format_path(plain) or "the spec"))
            if kind == "index":
                key = seg
                if key > len(parent) or (key == len(parent) and not create):
                    raise KeyError("%s has %d items" % (format_path(plain), len(parent)))
            else:
                key = _select(parent, seg)
                if key is None:
                    raise KeyError("%s has no item %r" % (format_path(plain), seg))
            if last:
                return parent, key, plain + (key,)
            if key == len(parent):
                parent.append({})
        parent = parent[key]
        plain += (key,)
    raise KeyError("an empty key path")


def _coerce(field, value):
    """A string given on the command line, in the syntax of the key's kind."""
    if field is None or not isinstance(value, str):
        return value
    kind = field.kind
    if kind in (DATE, MONEY, DURATION, BOOL, INT, NUM, LIST):
        return dec_scalar(value, kind, None, "the value", "`%s`" % field.key)
    return value


def _source_path(plain):
    if tuple(plain) == ("meta", "name"):
        return ("meta", "name_source")
    fields = SCHEMA.get(pattern_of(plain[:-1]))
    if fields and "source" in fields and plain[-1] != "source":
        return tuple(plain[:-1]) + ("source",)
    return None


def _say(text):
    sys.stdout.write(text.rstrip("\n") + "\n")


def _usage(message):
    sys.stderr.write("%s: %s\n" % (PROG, message))
    return 2


def cmd_get(args):
    try:
        data, _ = load(args.spec)
        container, key, _plain = resolve_path(data, parse_path(args.path))
        if isinstance(container, dict) and key not in container:
            raise KeyError("the spec has no %s" % args.path)
        value = container[key]
    except (OSError, ValueError) as exc:
        return _usage(str(exc))
    except SpecError as exc:
        _say(str(exc))
        return 1
    except KeyError as exc:
        _say("%s: %s" % (args.spec, exc.args[0]))
        return 1
    indent = 2 if isinstance(value, (dict, list)) else None
    _say(json.dumps(value, ensure_ascii=False, indent=indent, default=str))
    return 0


def save(path, data):
    """Write `data` to `path` as the canonical Markdown spec, atomically, and only when the
    round trip is exact. Raises SpecError naming what would not survive; nothing is written."""
    problems = roundtrip_problems(data, str(path))
    if problems:
        raise SpecError("not written — %s" % problems[0], None, str(path))
    _write_atomic(str(path), dump(data))


def cmd_set(args):
    try:
        spec_format(args.spec)
    except SpecError as exc:
        return _usage(exc.message)
    created = not os.path.exists(args.spec)
    if created:
        # the first value of a new spec: the folder must exist
        if not os.path.isdir(os.path.dirname(os.path.abspath(args.spec))):
            return _usage("no folder for %s — pack_paths.py <slug> --create makes it" % args.spec)
        data = {}
    else:
        try:
            data, _ = load(args.spec)
        except OSError as exc:
            return _usage(str(exc))
        except SpecError as exc:
            _say(str(exc))
            return 1
    try:
        value = json.loads(args.value)
        given_as_json = True
    except ValueError:
        value, given_as_json = args.value, False
    try:
        container, key, plain = resolve_path(data, parse_path(args.path), create=True)
        if not given_as_json:
            value = _coerce(field_for(plain), value)
        if isinstance(container, list) and key == len(container):
            container.append(value)
        else:
            container[key] = value
        if args.source is not None:
            spath = _source_path(plain)
            if spath is None:
                return _usage("no `source` key beside %s" % format_path(plain))
            scontainer, skey, _ = resolve_path(data, [("key", s) for s in spath], create=True)
            scontainer[skey] = args.source
    except ValueError as exc:
        return _usage(str(exc))
    except KeyError as exc:
        _say("%s: %s" % (args.spec, exc.args[0]))
        return 1
    except SpecError as exc:
        _say("%s: %s" % (args.spec, exc.message))
        return 1
    try:
        save(args.spec, data)
    except SpecError as exc:
        _say("%s: %s" % (args.spec, exc.message))
        return 1
    _say("%s: set %s%s" % (args.spec, format_path(plain), " (a new spec)" if created else ""))
    return 0


def check_spec(path):
    """(problems, data): every finding as (line, message)."""
    problems = []
    data, lm = load(path)
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    canon = dump(data)
    if canon != text:
        have, want = text.split("\n"), canon.split("\n")
        matcher = difflib.SequenceMatcher(a=have, b=want, autojunk=False)
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "equal":
                continue
            found = have[i1] if i1 < i2 else "(nothing)"
            expected = want[j1] if j1 < j2 else "(nothing)"
            problems.append((min(i1 + 1, len(have)),
                             "not canonical: `%s` — the writer puts `%s` here"
                             % (found[:80], expected[:80])))
            if len(problems) >= 20:
                break
    else:
        for message in roundtrip_problems(data, path):
            problems.append((1, message))
    for cpath, key in unknown_keys(data):
        where = lm.line(cpath + (key,)) if isinstance(key, (str, int)) else lm.line(cpath)
        problems.append((where, "unknown key `%s` — kept, but the layout does not know it; "
                                "a comma inside an unquoted YAML mapping splits a value into "
                                "keys like this" % format_path(cpath, key, has_key=True)))
    return problems, data


def cmd_check(args):
    try:
        problems, _data = check_spec(args.spec)
    except OSError as exc:
        return _usage(str(exc))
    except SpecError as exc:
        _say(str(exc))
        _say("%s: does not parse" % PROG)
        return 1
    for line, message in sorted(problems, key=lambda p: p[0]):
        _say("%s:%d: %s" % (args.spec, line, message))
    _say("%s: %s" % (PROG, "%d finding(s)" % len(problems) if problems else
                     "clean — parses, canonical, every key known"))
    return 1 if problems else 0



def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="packspec.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("get", help="print a value as JSON")
    g.add_argument("spec")
    g.add_argument("path")
    s = sub.add_parser("set", help="set a value and re-render the spec")
    s.add_argument("spec")
    s.add_argument("path")
    s.add_argument("value")
    s.add_argument("--source", default=None, help="also set the sibling `source` key")
    c = sub.add_parser("check", help="parse, re-render, name non-canonical lines and unknown keys")
    c.add_argument("spec")
    args = ap.parse_args(argv)
    try:
        return {"get": cmd_get, "set": cmd_set, "check": cmd_check}[args.cmd](args)
    except SpecError as exc:
        return _usage(str(exc))


if __name__ == "__main__":
    sys.exit(main())
