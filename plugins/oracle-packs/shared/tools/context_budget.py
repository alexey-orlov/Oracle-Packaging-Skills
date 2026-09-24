#!/usr/bin/env python3
"""Check a skill's per-step reading budget against the cards its SKILL.md names.

    python3 shared/tools/context_budget.py <SKILL.md or skill folder> [...] [--quiet]
    python3 shared/tools/context_budget.py <SKILL.md> --list     # every file the skill loads

A skill reads only the files its current step needs. The SKILL.md says which, and
this tool holds that honest: it counts the words of every file a step loads,
converts them to tokens, and fails when a step reads more than its share or a
file grows past its own word cap.

How a SKILL.md names what a step loads (the only grammar this tool reads)
    `Card: \`x\``, `Cards: \`x\`, \`y\``   one step that loads those files together.
        The label may carry a few words before its colon ("Card for the summary:");
        the list ends at the sentence's full stop.
    `Cards, one per part: \`x\`, \`y\``  one step per file ("one per" or "one at a
        time" before the colon).
    `Start-up: \`x\``                    files read with SKILL.md before the first
        message; they form the start-up step.
    `Agents read: \`x\``                 files a subagent reads in its own context:
        listed and sized, charged to no step.
    A bare name is the skill's own card, `references/cards/<name>.md`. A name with a
    slash is a path from the skill's folder; one beginning `shared/` is the plugin's
    shared folder. Labels are case-sensitive, so "(card: `x`)" in running prose is a
    pointer, not a step. Nothing inside a fenced code block counts.

Budgets
    tokens_per_word   1.35
    start-up          6000 tokens   SKILL.md plus its Start-up files
    every other step  2000 tokens

Word caps per file (docs/CONTEXT-BUDGET.md; not overridable)
    a card              300 words   every `.md` a step loads whose path has a
                                    `cards/` or `anatomy/` folder in it
    owner-language.md   400 words   the reader's test, the one wider card
    SKILL.md          1,200 words
    A file over its cap is reported once, even with --quiet, and fails the run like
    a step over budget: the fix is to tighten the file, never to raise the cap.

Exit codes
    0   every step within budget and every capped file within its cap
    1   a step over budget, a file over its cap, or a named file missing
    2   usage error
"""

import os
import re
import sys

USAGE = "usage: context_budget.py <SKILL.md or skill folder> [...] [--quiet | --list]"

TOKENS_PER_WORD = 1.35
START_UP_TOKENS = 6000
STEP_TOKENS = 2000

CARD_WORDS = 300
OWNER_LANGUAGE_WORDS = 400
SKILL_WORDS = 1200

LABEL = re.compile(r"(?<![\w`])(?P<label>Start-up|Cards?|Agents read)\b(?P<qual>[^:`\n]{0,100}):")


def word_cap(path):
    """The per-file word cap for `path`, as (cap, kind), or (None, None)."""
    norm = path.replace(os.sep, "/")
    name = norm.rsplit("/", 1)[-1]
    if name == "SKILL.md":
        return SKILL_WORDS, "SKILL.md"
    if name == "owner-language.md":
        return OWNER_LANGUAGE_WORDS, "card"
    if name.endswith(".md") and ("/cards/" in norm or "/anatomy/" in norm):
        return CARD_WORDS, "card"
    return None, None


def words_in(path):
    """Word count the way `wc -w` does it — whitespace-separated runs."""
    with open(path, encoding="utf-8", errors="replace") as fh:
        return len(fh.read().split())


def _names_after(line, start):
    """The backticked names from `start` to the end of the sentence."""
    names, i, inside, buf = [], start, False, []
    while i < len(line):
        ch = line[i]
        if ch == "`":
            if inside:
                names.append("".join(buf))
                buf = []
            inside = not inside
        elif inside:
            buf.append(ch)
        elif ch in ".;" and (i + 1 == len(line) or line[i + 1] in " *_)"):
            break
        i += 1
    return [n.strip() for n in names if n.strip() and " " not in n.strip()]


def _shared_root(skill_dir):
    here = os.path.abspath(skill_dir)
    while True:
        if os.path.isdir(os.path.join(here, "shared")):
            return here
        parent = os.path.dirname(here)
        if parent == here:
            return os.path.abspath(skill_dir)
        here = parent


def resolve(name, skill_dir):
    """A name from a SKILL.md, as an absolute path."""
    if name.startswith("shared/"):
        return os.path.normpath(os.path.join(_shared_root(skill_dir), name))
    if "/" in name:
        return os.path.normpath(os.path.join(skill_dir, name))
    base = name[:-3] if name.endswith(".md") else name
    return os.path.normpath(os.path.join(skill_dir, "references", "cards", base + ".md"))


def skill_steps(skill_md):
    """Parse a SKILL.md: (start_up_files, steps), where each step is a dict with
    `id`, `session` and `agents` lists of (name, absolute path)."""
    skill_dir = os.path.dirname(os.path.abspath(skill_md))
    with open(skill_md, encoding="utf-8") as fh:
        text = fh.read()
    if text.startswith("---"):
        end = text.find("\n---", 3)
        text = text[end + 4:] if end != -1 else text
    start_up, steps = [], []
    section, fenced, count = "top", False, {}
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if line.startswith("## "):
            section = re.sub(r"[^a-z0-9]+", "-", line[3:].lower()).strip("-") or "section"
            continue
        for m in LABEL.finditer(line):
            names = _names_after(line, m.end())
            if not names:
                continue
            files = [(n, resolve(n, skill_dir)) for n in names]
            label, qual = m.group("label"), m.group("qual").lower()
            if label == "Start-up":
                start_up.extend(files)
            elif label == "Agents read":
                if steps and steps[-1]["section"] == section:
                    steps[-1]["agents"].extend(files)
                else:
                    steps.append({"id": section, "section": section, "session": [], "agents": files})
            elif "one per" in qual or "one at a time" in qual:
                for f in files:
                    steps.append({"id": "%s/%s" % (section, os.path.basename(f[1])[:-3]),
                                  "section": section, "session": [f], "agents": []})
            else:
                title = re.match(r"\s*(?:\d+\.\s*)?\*\*([^*]+)\*\*", line)
                if title:
                    sid = re.sub(r"[^a-z0-9]+", "-", title.group(1).lower()).strip("-")
                else:
                    count[section] = count.get(section, 0) + 1
                    sid = section if count[section] == 1 else "%s-%d" % (section, count[section])
                steps.append({"id": sid, "section": section, "session": files, "agents": []})
    return start_up, steps


def check(skill_md, quiet, out):
    """Report one skill; return the number of problems found."""
    start_up, steps = skill_steps(skill_md)
    rows, findings, missing, over_cap = [], [], [], {}
    total = 0

    def capped(name, path, w):
        cap, kind = word_cap(path)
        if cap is None or w <= cap:
            return ""
        over_cap.setdefault(path, (name, w, cap, kind))
        return "  OVER the %d-word %s cap" % (cap, kind)

    everything = [{"id": "start-up", "session": [("SKILL.md", os.path.abspath(skill_md))] + start_up,
                   "agents": [], "start": True}] + steps
    for step in everything:
        cap = START_UP_TOKENS if step.get("start") else STEP_TOKENS
        words, files = 0, []
        for name, path in step["session"]:
            if not os.path.isfile(path):
                missing.append((step["id"], name))
                continue
            w = words_in(path)
            words += w
            files.append((name, w, capped(name, path, w)))
        agent_files = []
        for name, path in step["agents"]:
            if not os.path.isfile(path):
                missing.append((step["id"], name))
                continue
            w = words_in(path)
            agent_files.append((name, w, capped(name, path, w)))
        tokens = int(round(words * TOKENS_PER_WORD))
        total += words
        rows.append((step["id"], files, words, tokens, cap, agent_files))
        if tokens > cap:
            findings.append((step["id"], tokens, cap))

    if not quiet:
        out.write("%s\n  tokens ~= words x %.2f; start-up cap %d, per-step cap %d\n\n"
                  % (skill_md, TOKENS_PER_WORD, START_UP_TOKENS, STEP_TOKENS))
        out.write("  %-34s %7s %8s %8s\n" % ("step", "words", "tokens", "cap"))
        for step_id, files, w, t, cap, agent_files in rows:
            out.write("  %-34s %7d %8d %8d%s\n" % (step_id, w, t, cap, "  OVER" if t > cap else ""))
            for name, fw, over in files:
                out.write("      %-44s %5d w%s\n" % (name, fw, over))
            for name, fw, over in agent_files:
                out.write("      %-44s %5d w  (subagent, not charged)%s\n" % (name, fw, over))
        out.write("\n  session words across all steps: %d (~%d tokens)\n"
                  % (total, int(round(total * TOKENS_PER_WORD))))
    for step_id, name in missing:
        out.write("  MISSING %s: %s (%s)\n" % (step_id, name, skill_md))
    for step_id, tokens, cap in findings:
        out.write("  OVER BUDGET %s: %d tokens against a cap of %d (%s)\n" % (step_id, tokens, cap, skill_md))
    for name, w, cap, kind in over_cap.values():
        out.write("  %s over %d words: %s (%d)\n" % (kind, cap, name, w))
    if not steps:
        out.write("  NO STEPS: %s names no card on a Card line\n" % skill_md)
    problems = len(missing) + len(findings) + len(over_cap) + (0 if steps else 1)
    if not quiet and not problems:
        out.write("\ncontext_budget: %d steps, all within budget; every card within its cap\n"
                  % len(rows))
    return problems


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("-")]
    flags = [a for a in argv[1:] if a.startswith("-")]
    for f in flags:
        if f not in ("--quiet", "-q", "--list"):
            sys.stderr.write("context_budget: unknown option %s\n%s\n" % (f, USAGE))
            return 2
    if not args:
        sys.stderr.write("%s\n" % USAGE)
        return 2
    paths = []
    for a in args:
        p = os.path.join(a, "SKILL.md") if os.path.isdir(a) else a
        if not os.path.isfile(p):
            sys.stderr.write("context_budget: no such SKILL.md: %s\n" % a)
            return 2
        paths.append(p)
    if "--list" in flags:
        for p in paths:
            start_up, steps = skill_steps(p)
            seen = []
            for _name, path in start_up + [f for s in steps for f in s["session"] + s["agents"]]:
                if path not in seen:
                    seen.append(path)
                    print(path)
        return 0
    quiet = "--quiet" in flags or "-q" in flags
    problems = sum(check(p, quiet, sys.stdout) for p in paths)
    if problems:
        sys.stdout.write("\ncontext_budget: %d problem(s)\n" % problems)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
