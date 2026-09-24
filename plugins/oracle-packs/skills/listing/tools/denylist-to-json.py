#!/usr/bin/env python3
"""denylist-to-json.py — shared deny-list -> the listing checker's JSON input.

    python3 denylist-to-json.py                      # writes ./deny-list.json
    python3 denylist-to-json.py --out <site>/tools/deny-list.json
    python3 denylist-to-json.py --denylist <path> --print

WHY THIS EXISTS
    `shared/tools/denylist.txt` is the one list of customer names the practice
    keeps, and the site's `tools/check-grammar.js` needs the same names as JSON
    (`{"customerNames": [...], "bannedStrings": [[str, why], ...]}`). Kept by
    hand, the two drift, and the failure is silent in the worst direction: the
    checker prints a warning and passes, so an unconfigured deny-list is how a
    customer name reaches a published page. One converter, run before the gate,
    is the fix.

WHAT IT CONVERTS
    plain entry          -> customerNames  (whole-word match in the checker)
    ~entry               -> customerNames  (the checker matches case-insensitively)
    entry containing "/" -> bannedStrings  (a path fragment: substring match)
    `#` comments and blank lines are dropped.

    Entries that have a rule of their own in the JS checker (AIDP) are still
    emitted: a second assertion on the same string costs nothing and the two
    lists are maintained separately.

EXIT CODES
    0 written (or printed) · 2 the deny-list is missing, unreadable or empty
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# skills/listing/tools -> the plugin's shared/tools/denylist.txt.
DEFAULTS = [
    os.path.normpath(os.path.join(HERE, "..", "..", "..", "shared", "tools", "denylist.txt")),
]

WHY_PATH = "asset path carrying a customer or vendor mark (shared deny-list)"


def find_default():
    for path in DEFAULTS:
        if os.path.isfile(path):
            return path
    return DEFAULTS[0]


def convert(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            raw = fh.read()
    except OSError as exc:
        print("denylist-to-json: cannot read %s: %s" % (path, exc), file=sys.stderr)
        raise SystemExit(2)
    names, banned = [], []
    for line in raw.splitlines():
        entry = line.split("#", 1)[0].strip()
        if not entry:
            continue
        if entry.startswith("~"):
            entry = entry[1:].strip()
        if not entry:
            continue
        if "/" in entry:
            banned.append([entry, WHY_PATH])
        elif entry not in names:
            names.append(entry)
    if not names and not banned:
        print("denylist-to-json: %s holds no entries" % path, file=sys.stderr)
        raise SystemExit(2)
    return {
        "_README": [
            "GENERATED from shared/tools/denylist.txt by",
            "plugins/oracle-packs/skills/listing/tools/denylist-to-json.py.",
            "Do not hand-edit: add the name to the shared deny-list and re-run.",
            "INTERNAL — it carries the customer names it exists to keep out of a build,",
            "so it lives beside the site, never inside a published root.",
        ],
        "customerNames": names,
        "bannedStrings": banned,
    }


def main():
    ap = argparse.ArgumentParser(description="Convert the shared deny-list to the "
                                             "listing checker's JSON input.")
    ap.add_argument("--denylist", default=find_default(),
                    help="shared/tools/denylist.txt (default: the plugin's copy)")
    ap.add_argument("--out", default="deny-list.json",
                    help="where to write (default: ./deny-list.json); "
                         "the checker reads <site-root>/tools/deny-list.json or --deny-list")
    ap.add_argument("--print", dest="to_stdout", action="store_true",
                    help="print the JSON instead of writing it")
    args = ap.parse_args()

    if not os.path.isfile(args.denylist):
        print("denylist-to-json: no deny-list at %s — pass --denylist" % args.denylist,
              file=sys.stderr)
        raise SystemExit(2)
    data = convert(args.denylist)
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if args.to_stdout:
        sys.stdout.write(text)
    else:
        directory = os.path.dirname(os.path.abspath(args.out))
        if directory and not os.path.isdir(directory):
            print("denylist-to-json: no such directory: %s" % directory, file=sys.stderr)
            raise SystemExit(2)
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("denylist-to-json: wrote %s (%d names, %d path fragments) from %s"
              % (args.out, len(data["customerNames"]), len(data["bannedStrings"]),
                 args.denylist), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
