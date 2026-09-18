#!/usr/bin/env python3
"""Shared helpers for the pack linters (not a command-line tool).

`lint_spec.py`, `lint_artifact.py` and `check_consistency.py` import this module
from their own directory. Keep the four files together when a skill copies them.

What lives here:
  * the PyYAML guard (every tool exits 2 with an install line when it is absent)
  * a line-preserving YAML loader, so a finding can name the line it came from
  * the finding/report plumbing behind `file:line: CODE message` + one summary line
  * the deny-list reader (shared/tools/denylist.txt)
  * text extraction for .docx, .pptx, .pdf, .html, .js, .md, .txt, .yaml

Rules these encode live in shared/references/naming-and-clearance.md; when a rule
moves, that file is rewritten first and the linters follow in the same pass.

Dependencies: standard library, plus PyYAML for the YAML paths only.
"""

from __future__ import annotations

import html
import os
import re
import subprocess
import sys
import zipfile
from xml.etree import ElementTree as ET

# Into a virtualenv, never into system Python (plugins/oracle-packs/requirements.txt).
PYYAML_HINT = (
    "PyYAML is required and is not installed.\n"
    "  python3 -m venv .venv \\\n"
    "    && .venv/bin/pip install -r plugins/oracle-packs/requirements.txt\n"
    "  then run this tool with .venv/bin/python (or just: .venv/bin/pip install pyyaml)"
)

EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_USAGE = 2

TEXT_EXT = {".md", ".txt", ".html", ".htm", ".js", ".json", ".yaml", ".yml", ".csv"}
BINARY_EXT = {".docx", ".pptx", ".pdf"}
SUPPORTED_EXT = TEXT_EXT | BINARY_EXT

# The three tier names, everywhere, in this spelling (decisions 2026-09-18).
TIER_IDS = ("pov", "integration", "scaling")
TIER_NAMES = {"pov": "PoV Jumpstart", "integration": "Integration", "scaling": "Scaling"}

# The four clearance channels of clearance.customer_name_allowed.
CHANNELS = ("internal", "partner_print", "customer_site", "demo")


def die_usage(prog: str, message: str) -> "NoReturn":  # noqa: F821
    """Exit 2 — usage or dependency error, never a finding."""
    sys.stderr.write("%s: %s\n" % (prog, message))
    raise SystemExit(EXIT_USAGE)


def require_yaml(prog: str):
    """Import PyYAML or exit 2 with the install line."""
    try:
        import yaml  # noqa: F401
    except ImportError:
        die_usage(prog, PYYAML_HINT)
    return sys.modules["yaml"]


# --------------------------------------------------------------------------
# Line-preserving YAML
# --------------------------------------------------------------------------


class LineDict(dict):
    """A mapping that remembers the line each of its keys was written on."""

    def __init__(self, *a, **kw):
        dict.__init__(self, *a, **kw)
        self.line = 0
        self.key_lines = {}


class LineList(list):
    """A sequence that remembers the line each of its items starts on."""

    def __init__(self, *a, **kw):
        list.__init__(self, *a, **kw)
        self.line = 0
        self.item_lines = []


def load_yaml(path: str, prog: str):
    """Parse `path`, returning LineDict/LineList nodes. Exits 2 on a parse error."""
    yaml = require_yaml(prog)

    class LineLoader(yaml.SafeLoader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        out = LineDict()
        out.line = node.start_mark.line + 1
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=True)
            value = loader.construct_object(value_node, deep=True)
            out[key] = value
            out.key_lines[key] = key_node.start_mark.line + 1
        return out

    def construct_sequence(loader, node):
        out = LineList()
        out.line = node.start_mark.line + 1
        for child in node.value:
            out.append(loader.construct_object(child, deep=True))
            out.item_lines.append(child.start_mark.line + 1)
        return out

    LineLoader.add_constructor("tag:yaml.org,2002:map", construct_mapping)
    LineLoader.add_constructor("tag:yaml.org,2002:seq", construct_sequence)

    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = yaml.load(fh, Loader=LineLoader)
    except FileNotFoundError:
        die_usage(prog, "file not found: %s" % path)
    except IsADirectoryError:
        die_usage(prog, "expected a YAML file, got a directory: %s" % path)
    except Exception as exc:  # yaml.YAMLError and friends
        die_usage(prog, "cannot parse %s: %s" % (path, exc))
    if data is None:
        die_usage(prog, "%s is empty" % path)
    return data


def lineno(node, key=None, default=1) -> int:
    """Line of `key` inside `node`, or of `node` itself."""
    if isinstance(node, LineDict):
        if key is not None and key in node.key_lines:
            return node.key_lines[key]
        return node.line or default
    if isinstance(node, LineList):
        if isinstance(key, int) and 0 <= key < len(node.item_lines):
            return node.item_lines[key]
        return node.line or default
    return default


def dig(node, *path, default=None):
    """node['a']['b'] without raising on a missing or wrongly typed level."""
    cur = node
    for step in path:
        if isinstance(cur, dict) and step in cur:
            cur = cur[step]
        elif isinstance(cur, list) and isinstance(step, int) and 0 <= step < len(cur):
            cur = cur[step]
        else:
            return default
    return cur


def is_filled(value) -> bool:
    """True when a key carries a real value (an empty list is a filled `open_questions`)."""
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    return True


# --------------------------------------------------------------------------
# Findings
# --------------------------------------------------------------------------


class Report:
    """Collects findings, prints `file:line: CODE message` and one summary line."""

    def __init__(self, prog: str):
        self.prog = prog
        self.findings = []       # (file, line, code, message)
        self.warnings = []       # (file, line, code, message)
        self.unchecked = []      # str — a check that could not run (§5, honesty rule)

    def fail(self, path: str, line, code: str, message: str) -> None:
        self.findings.append((path, int(line or 1), code, message))

    def warn(self, path: str, line, code: str, message: str) -> None:
        self.warnings.append((path, int(line or 1), code, message))

    def cannot_check(self, what: str) -> None:
        if what not in self.unchecked:
            self.unchecked.append(what)

    def render(self, summary_extra: str = "", tail: str = "") -> int:
        for path, line, code, message in sorted(self.warnings, key=lambda f: (f[0], f[1], f[2])):
            sys.stdout.write("%s:%d: %s %s\n" % (path, line, code, message))
        for path, line, code, message in sorted(self.findings, key=lambda f: (f[0], f[1], f[2])):
            sys.stdout.write("%s:%d: %s %s\n" % (path, line, code, message))
        if self.unchecked:
            for item in self.unchecked:
                sys.stdout.write("  not evaluated: %s\n" % item)
        if tail:
            sys.stdout.write(tail.rstrip("\n") + "\n")
        bits = ["%d finding(s)" % len(self.findings), "%d warning(s)" % len(self.warnings)]
        if self.unchecked:
            bits.append("%d check(s) not evaluated" % len(self.unchecked))
        if summary_extra:
            bits.append(summary_extra)
        sys.stdout.write("%s: %s\n" % (self.prog, " · ".join(bits)))
        return EXIT_FINDINGS if self.findings else EXIT_CLEAN


# --------------------------------------------------------------------------
# Deny-list
# --------------------------------------------------------------------------


class DenyEntry:
    """One deny-list line: a customer name, a mark, or a path fragment."""

    def __init__(self, raw: str):
        self.raw = raw.strip()
        self.ci = self.raw.startswith("~")           # ~Foo — match case-insensitively
        self.term = self.raw[1:].strip() if self.ci else self.raw
        self.is_path = "/" in self.term
        flags = re.IGNORECASE if (self.ci or self.is_path) else 0
        if self.is_path:
            self.regex = re.compile(re.escape(self.term), flags)
        else:
            self.regex = re.compile(r"(?<![\w-])%s(?![\w-])" % re.escape(self.term), flags)
        # a name → "name", "name-", "name_" inside an asset path or file name
        self.slug = re.sub(r"[^a-z0-9]+", "", self.term.lower())

    def __str__(self):
        return self.term


DEFAULT_DENYLIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "denylist.txt")


def load_denylist(path: str, prog: str):
    """Read denylist.txt: one entry per line, `#` comments, blank lines ignored."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            raw = fh.read()
    except OSError as exc:
        die_usage(prog, "cannot read deny-list %s: %s" % (path, exc))
    entries = []
    for line in raw.splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            entries.append(DenyEntry(line))
    if not entries:
        die_usage(prog, "deny-list %s holds no entries" % path)
    return entries


# --------------------------------------------------------------------------
# Text extraction
# --------------------------------------------------------------------------

W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
A_NS = "{http://schemas.openxmlformats.org/drawingml/2006/main}"


class Doc:
    """Extracted text of one artifact, with a line number for every offset.

    `lines` are source lines for text formats, and one paragraph per line for
    .docx / .pptx / .pdf. `labels` names the origin of a line where the format
    has one worth printing ("slide 3", "slide 3 notes", "notes").
    `assets` holds file names carried inside the container (media, rels), which
    the logo check reads.
    """

    def __init__(self, path: str, lines, labels=None, assets=None, kind="text"):
        self.path = path
        self.lines = list(lines)
        self.labels = labels or {}
        self.assets = assets or []
        self.kind = kind
        self.text = "\n".join(self.lines)
        self._starts = []
        pos = 0
        for line in self.lines:
            self._starts.append(pos)
            pos += len(line) + 1

    def line_of(self, offset: int) -> int:
        lo, hi = 0, len(self._starts) - 1
        if hi < 0:
            return 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if self._starts[mid] <= offset:
                lo = mid
            else:
                hi = mid - 1
        return lo + 1

    def label(self, line: int) -> str:
        return self.labels.get(line, "")

    def where(self, offset: int):
        """(line, ' [slide 3]') for a match offset."""
        line = self.line_of(offset)
        label = self.label(line)
        return line, (" [%s]" % label if label else "")


# Markup carries the reader's characters as entities: a one-pager writes
# `&euro;90K` and a listing writes `&#x27;`. Unescaping per line keeps every line
# number valid and is what makes the price, name and copy checks see the same
# string the reader does — without it they silently skip the escaped half.
ENTITY_EXT = {".html", ".htm", ".js", ".json", ".md"}


def _read_text_file(path: str) -> Doc:
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        lines = fh.read().splitlines()
    if os.path.splitext(path)[1].lower() in ENTITY_EXT:
        lines = [html.unescape(line) for line in lines]
    return Doc(path, lines, kind="text")


def _xml_paragraphs(blob: bytes, para_tag: str, run_tag: str, break_tag=None):
    try:
        root = ET.fromstring(blob)
    except ET.ParseError:
        return []
    out = []
    for para in root.iter(para_tag):
        chunks = []
        for node in para.iter():
            if node.tag == run_tag and node.text:
                chunks.append(node.text)
            elif break_tag and node.tag == break_tag:
                chunks.append(" ")
        text = "".join(chunks).strip()
        if text:
            out.append(text)
    return out


def _read_docx(path: str) -> Doc:
    lines, labels, assets = [], {}, []
    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        assets = [n for n in names if "/media/" in n or n.endswith(".rels")]
        for name in names:
            if name.endswith(".rels"):
                try:
                    assets.extend(re.findall(r'Target="([^"]+)"', zf.read(name).decode("utf-8", "replace")))
                except KeyError:
                    pass
        parts = ["word/document.xml"]
        parts += sorted(n for n in names if re.match(r"word/(header|footer|footnotes|endnotes)\d*\.xml$", n))
        for part in parts:
            if part not in names:
                continue
            label = "document" if part == "word/document.xml" else os.path.basename(part)[:-4]
            for para in _xml_paragraphs(zf.read(part), W_NS + "p", W_NS + "t", W_NS + "br"):
                lines.append(para)
                if label != "document":
                    labels[len(lines)] = label
    return Doc(path, lines, labels, assets, kind="docx")


def _slide_no(name: str) -> int:
    m = re.search(r"(\d+)", os.path.basename(name))
    return int(m.group(1)) if m else 0


def _read_pptx(path: str) -> Doc:
    lines, labels, assets = [], {}, []
    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        assets = [n for n in names if "/media/" in n]
        for name in names:
            if name.endswith(".rels"):
                try:
                    assets.extend(re.findall(r'Target="([^"]+)"', zf.read(name).decode("utf-8", "replace")))
                except KeyError:
                    pass
        slides = sorted((n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n)), key=_slide_no)
        notes = {_slide_no(n): n for n in names if re.match(r"ppt/notesSlides/notesSlide\d+\.xml$", n)}
        for slide in slides:
            n = _slide_no(slide)
            for para in _xml_paragraphs(zf.read(slide), A_NS + "p", A_NS + "t", A_NS + "br"):
                lines.append(para)
                labels[len(lines)] = "slide %d" % n
            if n in notes:
                for para in _xml_paragraphs(zf.read(notes[n]), A_NS + "p", A_NS + "t", A_NS + "br"):
                    lines.append(para)
                    labels[len(lines)] = "slide %d notes" % n
    return Doc(path, lines, labels, assets, kind="pptx")


def _read_pdf(path: str):
    """(Doc, None) or (None, reason) when pdftotext is not installed."""
    try:
        proc = subprocess.run(["pdftotext", "-layout", path, "-"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except (FileNotFoundError, OSError):
        return None, "pdftotext is not installed — install poppler (brew install poppler) to lint .pdf"
    if proc.returncode != 0:
        return None, "pdftotext failed on %s: %s" % (path, proc.stderr.decode("utf-8", "replace").strip())
    text = proc.stdout.decode("utf-8", "replace")
    return Doc(path, text.splitlines(), kind="pdf"), None


def extract(path: str):
    """(Doc, None) on success, (None, reason) when the file cannot be read as text."""
    ext = os.path.splitext(path)[1].lower()
    if ext in TEXT_EXT:
        try:
            return _read_text_file(path), None
        except OSError as exc:
            return None, "cannot read %s: %s" % (path, exc)
    if ext == ".docx":
        try:
            return _read_docx(path), None
        except (zipfile.BadZipFile, OSError) as exc:
            return None, "cannot read %s as .docx: %s" % (path, exc)
    if ext == ".pptx":
        try:
            return _read_pptx(path), None
        except (zipfile.BadZipFile, OSError) as exc:
            return None, "cannot read %s as .pptx: %s" % (path, exc)
    if ext == ".pdf":
        return _read_pdf(path)
    return None, "%s: unsupported extension %s (text, .docx, .pptx, .pdf only)" % (path, ext or "(none)")


SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", ".work", "dist", "build"}


def collect_files(target: str, prog: str):
    """A file, or every supported file under a directory (sorted, hidden dirs skipped)."""
    if os.path.isfile(target):
        return [target]
    if not os.path.isdir(target):
        die_usage(prog, "no such file or directory: %s" % target)
    out = []
    for root, dirs, files in os.walk(target):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))
        for name in sorted(files):
            if name.startswith("~$") or name.startswith("."):
                continue
            if os.path.splitext(name)[1].lower() in SUPPORTED_EXT:
                out.append(os.path.join(root, name))
    if not out:
        die_usage(prog, "no lintable files under %s" % target)
    return out


# --------------------------------------------------------------------------
# Shared data files: the Oracle product catalog and the roadmap extract
# --------------------------------------------------------------------------


def _repo_data(name: str) -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(here, "..", "data", name))


DEFAULT_CATALOG = _repo_data("oracle-products.yaml")
DEFAULT_ROADMAP = _repo_data("roadmap-items.csv")


def load_catalog(path: str, prog: str):
    """Read shared/data/oracle-products.yaml.

    Tolerant of the three shapes the catalog may take — a bare list, a mapping
    with a `products:` list, or an id → entry mapping — because the catalog is
    owned elsewhere. Returns {"ids": set, "entries": [dict]}; entry keys read
    here are id, name, short, aliases, not_this.
    """
    data = load_yaml(path, prog)
    if isinstance(data, dict) and isinstance(data.get("products"), list):
        rows = data["products"]
    elif isinstance(data, list):
        rows = data
    elif isinstance(data, dict):
        rows = []
        for key, value in data.items():
            if isinstance(value, dict):
                row = dict(value)
                row.setdefault("id", key)
                rows.append(row)
    else:
        die_usage(prog, "catalog %s is not a list or mapping of products" % path)
        rows = []
    entries, ids = [], set()
    for row in rows:
        if not isinstance(row, dict) or not row.get("id"):
            continue
        entry = {
            "id": str(row["id"]),
            "name": str(row.get("name") or "").strip(),
            "short": str(row.get("short") or "").strip(),
            "aliases": [str(a) for a in (row.get("aliases") or []) if str(a).strip()],
            "not_this": [str(a) for a in (row.get("not_this") or []) if str(a).strip()],
            "vendor": str(row.get("vendor") or "").strip(),
        }
        entries.append(entry)
        ids.add(entry["id"])
    return {"ids": ids, "entries": entries}


def load_roadmap_ids(path: str, prog: str):
    """Read the `id` column of shared/data/roadmap-items.csv."""
    import csv
    try:
        with open(path, "r", encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            if not reader.fieldnames or "id" not in reader.fieldnames:
                die_usage(prog, "%s has no `id` column" % path)
            return {(row.get("id") or "").strip() for row in reader if (row.get("id") or "").strip()}
    except OSError as exc:
        die_usage(prog, "cannot read roadmap extract %s: %s" % (path, exc))


# --------------------------------------------------------------------------
# Small text utilities shared by the artifact linter and the consistency check
# --------------------------------------------------------------------------

# "€90,000", "€90K", "EUR 90 000", "90,000 EUR", "€300K–€500K". The digit run may
# only cross a space into a full group of three, so a price never swallows the
# number on the next line.
_NUMBER = r"\d[\d.,]*(?:[  ]\d{3})*"
MONEY_RE = re.compile(
    r"(?:€|\bEUR\b)[  ]?" + _NUMBER + r"[  ]?[KkMm]?\b"
    r"|\b" + _NUMBER + r"[  ]?[KkMm]?[  ]?(?:€|\bEUR\b)")

# What counts as a disclaimer beside a price. Deliberately excludes the word
# "footnote" itself: copy that merely talks about footnotes is not a disclaimer.
DISCLAIMER_RE = re.compile(
    r"\*|†|‡|\bindicative\b|\billustrative\b|\bto be confirmed\b|\bTBC\b|\bnot contractual\b"
    r"|\bexcl\.|\bexcluding\b|\bestimate[sd]?\b|\bscoped per engagement\b",
    re.IGNORECASE)


def money_value(token: str):
    """'€90K' → 90000.0; '€300,000' → 300000.0; None when it will not parse."""
    t = token.replace("€", " ").replace("EUR", " ")
    m = re.search(r"\d[\d.,\s]*", t)
    if not m:
        return None
    digits = m.group(0)
    suffix = t[m.end():].strip()[:1].lower()
    # 90,000 / 90 000 → 90000 ; 1.5 → 1.5 (a lone dot with 1-2 decimals is a decimal point)
    if re.search(r"\.\d{1,2}$", digits.strip()) and "," not in digits:
        num = digits.strip()
    else:
        num = re.sub(r"[.,\s]", "", digits)
    try:
        value = float(num)
    except ValueError:
        return None
    if suffix == "k":
        value *= 1000
    elif suffix == "m":
        value *= 1000000
    return value


def asset_slug_candidates(token: str, max_join: int = 4):
    """Every word-boundary-respecting slug inside a file name or asset path.

    "assets/img/logos/acme-logo.svg" → {..., "logos", "acme", "acmelogo", ...}
    Matching a deny-list slug against THESE, rather than against the whole
    flattened string, is what stops a file like "media/logos-mark.png" from
    reading as a three-letter customer acronym hiding inside "mark".
    """
    spaced = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", token)
    segs = [s.lower() for s in re.findall(r"[A-Za-z]+|\d+", spaced)]
    out = set()
    for i in range(len(segs)):
        for j in range(i + 1, min(i + max_join, len(segs)) + 1):
            out.add("".join(segs[i:j]))
    return out


def norm_ws(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").replace(" ", " ")).strip()


def norm_loose(text: str) -> str:
    """Compare copy across formats: fold case, dashes, quotes, entities, whitespace.

    HTML and .js artifacts carry `&#x27;` where the spec carries `\u2019`; without
    unescaping, every one-liner in a listing or a one-pager reads as different.
    """
    t = html.unescape(norm_ws(text)).lower()
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    t = re.sub(r"[‐-―]", "-", t)
    return re.sub(r"[^\w%€$.,:/'\"-]+", " ", t).strip()


def context(text: str, start: int, end: int, radius: int = 200) -> str:
    return text[max(0, start - radius):min(len(text), end + radius)]
