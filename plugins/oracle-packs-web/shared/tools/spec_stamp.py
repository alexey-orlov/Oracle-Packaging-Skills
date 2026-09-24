#!/usr/bin/env python3
"""Which spec an artifact was built from: the stamp every builder writes into its file.

    stamp(spec_path)          "pack-spec sha256:<12 hex> commit:<short hash|uncommitted|none>"
    read_stamp(artifact)      that string, or None when the file carries no stamp

    shared/tools/py shared/tools/spec_stamp.py <artifact>...    each file's stamp
    shared/tools/py shared/tools/spec_stamp.py --spec <spec>     the stamp a build writes now

The spec lives in the packaging-skills repo and the artifacts on the machine that built them
(pack_paths.py), so every artifact says which spec it reflects. The sha is the spec file's
own bytes. The commit is the last commit touching the spec, `uncommitted` when git reports it
modified or untracked, `none` outside a git checkout (pack_paths.spec_git_state). A file
built before 2026-09-24, or by hand, carries no stamp.

Where the stamp lives
    .docx .pptx   dc:identifier in docProps/core.xml — core_properties.identifier in
                  python-docx and python-pptx
    .html         <meta name="pack-spec" content="...">
    .pdf          the document-information key /PackSpec, read with pypdf (None without it)

check_consistency.py compares an artifact's sha with the current spec's: CON006 when they
differ (built from an earlier version of the spec), CON007 when a stampable file has none.

Exit codes (the command line): 0 printed · 2 usage error (no such file, no arguments).
"""

from __future__ import annotations

import argparse
import html
import os
import re
import sys
import zipfile
from xml.etree import ElementTree as ET

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.append(_HERE)

import pack_paths  # noqa: E402

PREFIX = "pack-spec"
STAMP_RE = re.compile(r"^pack-spec\s+sha256:([0-9a-f]{12})(?![0-9a-f])")
DC_IDENTIFIER = "{http://purl.org/dc/elements/1.1/}identifier"
PDF_KEY = "/PackSpec"
HTML_META = "pack-spec"
META_TAG = re.compile(r"<meta\b[^>]*>", re.IGNORECASE)
ATTR = re.compile(r"""([\w:-]+)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'>]+))""")

# The formats the builders stamp; any other file carries no stamp by design.
STAMPED = (".docx", ".pptx", ".html", ".htm", ".pdf")


def spec_sha(spec_path) -> str:
    """sha256 of the spec's bytes, first 12 hex characters."""
    return pack_paths.spec_sha(str(spec_path))


def stamp(spec_path) -> str:
    """The stamp a build of this spec writes: its sha and its commit, or `uncommitted`."""
    path = str(spec_path)
    commit, dirty = pack_paths.spec_git_state(path)
    return "%s sha256:%s commit:%s" % (PREFIX, spec_sha(path), "uncommitted" if dirty else commit)


def stamp_sha(value):
    """The 12-hex sha inside a stamp, or None."""
    m = STAMP_RE.match((value or "").strip())
    return m.group(1) if m else None


def stampable(path) -> bool:
    """True for the formats the builders stamp (.docx, .pptx, .html, .pdf)."""
    return str(path).lower().endswith(STAMPED)


def readable(path) -> bool:
    """False only for a .pdf on an interpreter without pypdf: its stamp cannot be read here."""
    if not str(path).lower().endswith(".pdf"):
        return True
    try:
        import pypdf  # noqa: F401
    except ImportError:
        return False
    return True


def _ours(value):
    value = (value or "").strip()
    return value if value.startswith(PREFIX + " ") else None


def _office(path):
    try:
        with zipfile.ZipFile(path) as zf:
            blob = zf.read("docProps/core.xml")
    except (KeyError, zipfile.BadZipFile, OSError):
        return None
    try:
        node = ET.fromstring(blob).find(DC_IDENTIFIER)
    except ET.ParseError:
        return None
    return _ours(node.text if node is not None else None)


def _html(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError:
        return None
    end = text.lower().find("</head>")
    for tag in META_TAG.findall(text if end < 0 else text[:end]):
        attrs = {}
        for m in ATTR.finditer(tag):
            value = next(g for g in m.groups()[1:] if g is not None)
            attrs[m.group(1).lower()] = html.unescape(value)
        if attrs.get("name", "").strip().lower() == HTML_META:
            return _ours(attrs.get("content"))
    return None


def _pdf(path):
    try:
        from pypdf import PdfReader
    except ImportError:
        return None
    try:
        info = PdfReader(path).metadata
        value = info.get(PDF_KEY) if info else None
    except Exception:                       # noqa: BLE001 - an unreadable PDF has no readable stamp
        return None
    return _ours(str(value)) if value is not None else None


def read_stamp(artifact_path):
    """The stamp a built file carries, or None (no stamp, or not a stamped format)."""
    path = str(artifact_path)
    low = path.lower()
    if low.endswith((".docx", ".pptx")):
        return _office(path)
    if low.endswith((".html", ".htm")):
        return _html(path)
    if low.endswith(".pdf"):
        return _pdf(path)
    return None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="spec_stamp.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("artifacts", nargs="*", help="built files whose stamp to print")
    ap.add_argument("--spec", help="print the stamp a build of this spec writes now")
    args = ap.parse_args(argv)
    if not args.spec and not args.artifacts:
        ap.print_usage(sys.stderr)
        sys.stderr.write("spec_stamp: give --spec <pack-spec.yaml>, or one or more built files\n")
        return 2
    for path in ([args.spec] if args.spec else []) + args.artifacts:
        if not os.path.isfile(path):
            sys.stderr.write("spec_stamp: no such file: %s\n" % path)
            return 2
    if args.spec:
        print(stamp(args.spec))
    for path in args.artifacts:
        if not readable(path):
            print("%s: not read here — pypdf is not installed" % path)
            continue
        print("%s: %s" % (path, read_stamp(path) or "no stamp"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
