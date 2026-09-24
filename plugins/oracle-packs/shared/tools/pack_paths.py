#!/usr/bin/env python3
"""Where a pack's files go: the spec in the packaging-skills repo, the work on this machine.

    shared/tools/py shared/tools/pack_paths.py <slug> [--repo <dir>] [--create] [--json]

The owner's layout (2026-09-24). The spec lives in the packaging-skills repo, so every
colleague builds from the same one; everything a run produces, and everything it reads out
of the customer's documents, stays on the machine of the person running the skills:

    <repo>/packs/<slug>/     committed and shared: pack-spec.yaml, architecture.json (the
                             architecture model) and visuals/ (the pictures the spec names,
                             with their provenance .json files and credits.md)
    <work>/                  $ORACLE_PACKS_OUT/<slug>, else ~/oracle-packs/<slug>: artifacts/
                             (every built file), intake.md, inventory.md, inventory/ (extracts
                             of customer documents), sources/, research-brief.md, research/,
                             decisions.md, any scratch. Never in the repo: these files quote
                             the customer's own documents and carry internal figures.

The repo is `--repo`, else $ORACLE_PACKS_ROOT, else the working directory or its nearest
ancestor that is a checkout of this repo: a folder holding .claude-plugin/marketplace.json
whose "name" is "oracle-packaging-skills".

Output, as key=value lines or, with --json, one JSON object:
    slug, repo, spec_dir, spec, work, artifacts, spec_exists
    and, when the spec exists:
    spec_sha      sha256 of the spec's bytes, first 12 hex characters
    spec_commit   short hash of the last commit touching the spec, or `none`
    spec_dirty    true when git reports the spec modified, staged or untracked

--create makes spec_dir, work and artifacts, and nothing else in the repo.

Exit codes
    0   printed (and created, with --create)
    2   usage error, one line on stderr: a bad slug, no checkout found, a --repo or
        $ORACLE_PACKS_ROOT that is not a checkout of this repo, a folder that cannot be made

Standard library only. Also a library: spec_stamp.py reuses spec_sha() and spec_git_state().
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

PROG = "pack_paths"
REPO_NAME = "oracle-packaging-skills"
MARKETPLACE = os.path.join(".claude-plugin", "marketplace.json")
SPEC_NAME = "pack-spec.yaml"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

NOT_FOUND = ("no checkout of the packaging-skills repo found: clone it and set "
             "ORACLE_PACKS_ROOT, or pass --repo")


class PathsError(Exception):
    """A usage error: one line on stderr, exit 2."""


# ---------------------------------------------------------------------------- the repo
def is_checkout(path: str) -> bool:
    """True when `path` holds .claude-plugin/marketplace.json named oracle-packaging-skills."""
    try:
        with open(os.path.join(path, MARKETPLACE), encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return False
    return isinstance(data, dict) and data.get("name") == REPO_NAME


def find_checkout(start: str):
    """`start` or its nearest ancestor that is a checkout of this repo, else None."""
    here = os.path.abspath(start)
    while True:
        if is_checkout(here):
            return here
        parent = os.path.dirname(here)
        if parent == here:
            return None
        here = parent


def resolve_repo(repo=None, environ=None, cwd=None) -> str:
    """--repo, else $ORACLE_PACKS_ROOT, else found from the working directory."""
    env = os.environ if environ is None else environ
    for given, label in ((repo, "--repo "), (env.get("ORACLE_PACKS_ROOT"), "ORACLE_PACKS_ROOT=")):
        if given:
            path = os.path.abspath(os.path.expanduser(given))
            if not is_checkout(path):
                raise PathsError("%s%s is not a checkout of the packaging-skills repo: it holds no "
                                 ".claude-plugin/marketplace.json named \"%s\""
                                 % (label, given, REPO_NAME))
            return path
    found = find_checkout(cwd or os.getcwd())
    if not found:
        raise PathsError(NOT_FOUND)
    return found


# ------------------------------------------------------------------------ the work folder
def work_root(environ=None) -> str:
    """$ORACLE_PACKS_OUT, else ~/oracle-packs (%USERPROFILE%\\oracle-packs on Windows)."""
    env = os.environ if environ is None else environ
    out = env.get("ORACLE_PACKS_OUT")
    if out:
        return os.path.abspath(os.path.expanduser(out))
    return os.path.join(os.path.expanduser("~"), "oracle-packs")


def work_dir(slug: str, environ=None) -> str:
    return os.path.join(work_root(environ), slug)


def check_slug(slug: str) -> str:
    if not SLUG_RE.match(slug or ""):
        raise PathsError("%r is not a pack slug: lowercase letters and digits in hyphenated "
                         "words, like account-insights" % (slug,))
    return slug


# ------------------------------------------------------------------------------ the spec
def spec_sha(spec_path: str) -> str:
    """sha256 of the spec's bytes, first 12 hex characters."""
    digest = hashlib.sha256()
    with open(spec_path, "rb") as fh:
        for block in iter(lambda: fh.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()[:12]


def _git(args, where):
    """git's stdout, or None when git is missing, fails or `where` is no checkout."""
    try:
        proc = subprocess.run(["git", "-C", where] + list(args), stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, universal_newlines=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    return proc.stdout if proc.returncode == 0 else None


def spec_git_state(spec_path: str, repo=None):
    """(commit, dirty) for the spec.

    commit: the short hash of the last commit touching it (`git log -1 --format=%h`), or
    "none". dirty: `git status --porcelain` names it — modified, staged or untracked. Outside
    a git checkout, or on a machine without git, ("none", False).
    """
    spec_abs = os.path.abspath(spec_path)
    base = os.path.abspath(repo) if repo else os.path.dirname(spec_abs)
    rel = os.path.relpath(spec_abs, base).replace(os.sep, "/")
    commit = (_git(["log", "-1", "--format=%h", "--", rel], base) or "").strip() or "none"
    dirty = bool((_git(["status", "--porcelain", "--", rel], base) or "").strip())
    return commit, dirty


# ------------------------------------------------------------------------------- paths
def layout(slug: str, repo: str, environ=None) -> dict:
    """The folders and the spec's path, without looking at the spec."""
    spec_dir = os.path.join(repo, "packs", slug)
    work = work_dir(slug, environ)
    return {"slug": slug, "repo": repo, "spec_dir": spec_dir,
            "spec": os.path.join(spec_dir, SPEC_NAME), "work": work,
            "artifacts": os.path.join(work, "artifacts")}


def paths(slug: str, repo: str, environ=None) -> dict:
    """layout(), plus whether the spec exists and, when it does, its sha and git state."""
    out = layout(slug, repo, environ)
    out["spec_exists"] = os.path.isfile(out["spec"])
    if out["spec_exists"]:
        commit, dirty = spec_git_state(out["spec"], repo)
        out.update(spec_sha=spec_sha(out["spec"]), spec_commit=commit, spec_dirty=dirty)
    return out


def create(found: dict) -> None:
    """spec_dir, work and artifacts — nothing else in the repo."""
    for key in ("spec_dir", "work", "artifacts"):
        try:
            os.makedirs(found[key], exist_ok=True)
        except OSError as exc:
            raise PathsError("cannot make %s: %s" % (found[key], exc.strerror or exc))


def render(found: dict, as_json: bool) -> str:
    if as_json:
        return json.dumps(found, indent=2)
    lines = []
    for key, value in found.items():
        if isinstance(value, bool):
            value = "true" if value else "false"
        lines.append("%s=%s" % (key, value))
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="pack_paths.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug", help="the pack's slug, e.g. account-insights")
    ap.add_argument("--repo", help="the packaging-skills checkout (default: $ORACLE_PACKS_ROOT, "
                                   "else found from the working directory)")
    ap.add_argument("--create", action="store_true",
                    help="make spec_dir, work and artifacts")
    ap.add_argument("--json", action="store_true", help="one JSON object instead of key=value lines")
    args = ap.parse_args(argv)

    try:
        slug = check_slug(args.slug)
        repo = resolve_repo(args.repo)
        if args.create:
            create(layout(slug, repo))
        found = paths(slug, repo)
    except PathsError as exc:
        sys.stderr.write("%s: %s\n" % (PROG, exc))
        return 2
    print(render(found, args.json))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
