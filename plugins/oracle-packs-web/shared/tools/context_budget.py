#!/usr/bin/env python3
"""Check a skill's per-step reading budget against its cards manifest.

    python3 shared/tools/context_budget.py <manifest.yaml>
    python3 shared/tools/context_budget.py <manifest.yaml> --quiet

A skill used to read everything it might ever need before its first question.
The manifest says instead which files enter the conversation at which step, and
this tool holds that honest: it counts the words of every listed file, converts
them to tokens, and fails when a step reads more than its share.

What counts
    `session` files enter the conversation at that step and are charged to it.
    `agents` files are read by a subagent in its own fresh context; they are
    listed and sized in the report but charged to no step — a subagent's prompt
    costs the session nothing.

Budgets (overridable per manifest under `budget:`)
    tokens_per_word   1.35
    start_up_tokens   6000   the step marked `start_up: true`
    step_tokens       2000   every other step

Paths
    Relative to the manifest's own `root:` (itself relative to the manifest's
    directory). A path beginning `shared/` resolves against the nearest parent
    directory that contains one — the bundle's shared folder in the repo, the
    plugin's synced copy in an install.

Exit codes
    0   every step is within budget (the per-step table is printed)
    1   a step is over budget, or a listed file is missing
    2   usage or dependency error (bad arguments, unreadable manifest, no PyYAML)
"""

import os
import sys

USAGE = "usage: context_budget.py <manifest.yaml> [--quiet]"

DEFAULTS = {"tokens_per_word": 1.35, "start_up_tokens": 6000, "step_tokens": 2000}


def die(msg, code=2):
    sys.stderr.write("context_budget: %s\n" % msg)
    sys.exit(code)


def words_in(path):
    """Word count the way `wc -w` does it — whitespace-separated runs."""
    with open(path, encoding="utf-8", errors="replace") as fh:
        return len(fh.read().split())


def resolve(spec_path, root, manifest_dir):
    """Resolve one manifest entry to an absolute path."""
    if spec_path.startswith("shared/"):
        here = root
        while True:
            candidate = os.path.join(here, spec_path)
            if os.path.exists(candidate):
                return candidate
            parent = os.path.dirname(here)
            if parent == here:
                return os.path.join(root, spec_path)   # report it as missing where it was looked for
            here = parent
    return os.path.normpath(os.path.join(root, spec_path))


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("-")]
    flags = [a for a in argv[1:] if a.startswith("-")]
    for f in flags:
        if f not in ("--quiet", "-q"):
            die("unknown option %s\n%s" % (f, USAGE))
    if len(args) != 1:
        die(USAGE)
    quiet = bool(flags)

    manifest_path = args[0]
    if not os.path.isfile(manifest_path):
        die("no such manifest: %s" % manifest_path)

    try:
        import yaml
    except ImportError:
        die("PyYAML is not installed for this interpreter; "
            "pip install -r plugins/oracle-packs/requirements.txt")

    try:
        with open(manifest_path, encoding="utf-8") as fh:
            manifest = yaml.safe_load(fh)
    except Exception as exc:                                  # noqa: BLE001
        die("could not read %s: %s" % (manifest_path, exc))
    if not isinstance(manifest, dict) or not manifest.get("steps"):
        die("%s has no `steps:` list" % manifest_path)

    budget = dict(DEFAULTS)
    budget.update(manifest.get("budget") or {})
    per_word = float(budget["tokens_per_word"])
    start_cap = int(budget["start_up_tokens"])
    step_cap = int(budget["step_tokens"])

    manifest_dir = os.path.dirname(os.path.abspath(manifest_path)) or "."
    root = os.path.normpath(os.path.join(manifest_dir, manifest.get("root", ".")))

    rows, findings, missing = [], [], []
    total_session_words = 0

    for step in manifest["steps"]:
        step_id = step.get("id") or "(unnamed step)"
        is_start = bool(step.get("start_up"))
        cap = start_cap if is_start else step_cap

        session_words, files = 0, []
        for entry in step.get("session") or []:
            path = resolve(entry, root, manifest_dir)
            if not os.path.isfile(path):
                missing.append((step_id, entry))
                continue
            w = words_in(path)
            session_words += w
            files.append((entry, w))

        agent_words, agent_files = 0, []
        for entry in step.get("agents") or []:
            path = resolve(entry, root, manifest_dir)
            if not os.path.isfile(path):
                missing.append((step_id, entry))
                continue
            w = words_in(path)
            agent_words += w
            agent_files.append((entry, w))

        tokens = int(round(session_words * per_word))
        total_session_words += session_words
        rows.append((step_id, files, session_words, tokens, cap, is_start,
                     agent_files, agent_words))
        if tokens > cap:
            findings.append((step_id, tokens, cap, files))

    out = sys.stdout
    if not quiet:
        out.write("%s\n" % manifest_path)
        out.write("  tokens ~= words x %.2f; start-up cap %d, per-step cap %d\n\n"
                  % (per_word, start_cap, step_cap))
        out.write("  %-26s %7s %8s %8s\n" % ("step", "words", "tokens", "cap"))
        for (step_id, files, w, t, cap, is_start, agent_files, aw) in rows:
            flag = "  OVER" if t > cap else ""
            out.write("  %-26s %7d %8d %8d%s\n" % (step_id, w, t, cap, flag))
            for name, fw in files:
                out.write("      %-40s %5d w\n" % (name, fw))
            for name, fw in agent_files:
                out.write("      %-40s %5d w  (subagent, not charged)\n" % (name, fw))
        out.write("\n  session words across all steps: %d (~%d tokens)\n"
                  % (total_session_words, int(round(total_session_words * per_word))))

    for step_id, entry in missing:
        out.write("  MISSING %s: %s\n" % (step_id, entry))
    for step_id, tokens, cap, files in findings:
        out.write("  OVER BUDGET %s: %d tokens against a cap of %d\n"
                  % (step_id, tokens, cap))
        for name, fw in sorted(files, key=lambda p: -p[1]):
            out.write("      %-40s %5d w (~%d tokens)\n"
                      % (name, fw, int(round(fw * per_word))))

    if missing or findings:
        out.write("\ncontext_budget: %d over budget, %d missing\n"
                  % (len(findings), len(missing)))
        return 1
    if not quiet:
        out.write("\ncontext_budget: %d steps, all within budget\n" % len(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
