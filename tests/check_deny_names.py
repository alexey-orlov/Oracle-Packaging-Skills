#!/usr/bin/env python3
"""No deny-list entry under plugins/ except in the deny-list itself.

    python3 tests/check_deny_names.py <plugin shared/tools dir> <dir to search>

The repo's rule: no customer name anywhere under plugins/ except the linter's deny-list,
which exists to catch them. The linters read specs and artifacts, never the plugin's own
comments and cards, and names reached those as the source of a lesson ("the <customer>
one-pager, 2026-09-23") until they were found by hand (2026-09-29), so a test holds the rule.

Every entry of <tools>/denylist.txt is searched for in each text file under the directory
and in the file's path: case-insensitively, on word boundaries (grep -iw). That is stricter
than the linter, because a slug or a file name carries a name in lower case. Entries
holding a `/` are asset-path fragments and are skipped. So are the entries lint_artifact.py
gives a rule of their own (DEDICATED_DENY: "AIDP", ART102), whose rule, references and
catalog must spell them. Binary files (the pictures, the reference decks) are not read.

In a git checkout the files are the ones a commit would carry: tracked, and untracked but
not ignored. Anywhere else, every file outside the folders the repo's .gitignore keeps out.

A hit prints its path, its line and the line of denylist.txt it matches, never the name;
a path that holds a name prints with the name masked.

Exit 0 no entry found · 1 an entry found · 2 usage error.
"""

import re
import subprocess
import sys
from pathlib import Path

# The folders the repo's .gitignore keeps out, for a tree that is not a git checkout.
IGNORED_DIRS = {".git", ".venv", ".work", "__pycache__", "node_modules"}
MASK = "<name>"


def name_entries(denylist, dedicated):
    """(denylist.txt line, regex) per name entry: `#` comments and a leading `~` stripped,
    path fragments and the entries with a rule of their own skipped."""
    found = []
    for n, line in enumerate(denylist.read_text(encoding="utf-8").splitlines(), 1):
        term = line.split("#", 1)[0].strip()
        term = term[1:].strip() if term.startswith("~") else term
        if term and "/" not in term and term not in dedicated:
            found.append((n, re.compile(r"(?<!\w)%s(?!\w)" % re.escape(term), re.IGNORECASE)))
    return found


def files(root):
    """The files under root a commit would carry; outside a git checkout, every file
    outside the ignored folders."""
    try:
        listed = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "--cached", "--others",
                                 "--exclude-standard"], capture_output=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return sorted(p for p in root.rglob("*")
                      if p.is_file() and not IGNORED_DIRS & set(p.relative_to(root).parts))
    return sorted({root / p for p in listed.decode("utf-8").split("\0") if p})


def main(argv):
    if len(argv) != 3:
        sys.stderr.write(__doc__)
        return 2
    tools, root = Path(argv[1]), Path(argv[2])
    denylist = tools / "denylist.txt"
    for need, ok in ((denylist, denylist.is_file()), (root, root.is_dir())):
        if not ok:
            sys.stderr.write("check_deny_names: %s not found\n" % need)
            return 2
    sys.path.insert(0, str(tools))
    from lint_artifact import DEDICATED_DENY

    names = name_entries(denylist, DEDICATED_DENY)
    if not names:
        sys.stderr.write("check_deny_names: %s holds no name entry\n" % denylist)
        return 2

    own = denylist.resolve()
    hits, read = [], 0
    for path in files(root):
        if not path.is_file() or path.resolve() == own:
            continue
        rel = path.relative_to(root).as_posix()
        shown = root.name + "/" + rel
        for _n, rx in names:
            shown = rx.sub(MASK, shown)
        for n, rx in names:
            if rx.search(rel):
                hits.append("%s: its path holds the deny-list entry on line %d of denylist.txt"
                            % (shown, n))
        data = path.read_bytes()
        if b"\0" in data[:8000]:                     # binary: a picture, a deck
            continue
        read += 1
        for i, line in enumerate(data.decode("utf-8", "replace").split("\n"), 1):
            for n, rx in names:
                if rx.search(line):
                    hits.append("%s:%d: the deny-list entry on line %d of denylist.txt"
                                % (shown, i, n))
    for hit in hits:
        print(hit)
    print("check_deny_names: %d text files under %s/, %d name entries, %d hit(s)%s"
          % (read, root.name, len(names), len(hits),
             " — describe the customer instead (industry and scale); never trim denylist.txt"
             if hits else ""))
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
