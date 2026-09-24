#!/usr/bin/env python3
"""Every card is loaded by some skill.

    python3 tests/check_orphans.py <plugin shared/tools dir> <plugin dir>

A card no SKILL.md names on a Card, Start-up or Agents-read line is read by no step:
either a stub left behind by a restructure or a rule that stopped reaching the model.
Both are how the plugin grew second homes for its rules (2026-09-24), so an orphan
fails the suite. The files each SKILL.md names are resolved by context_budget.py, the
same parser the budget check uses.

Exit 0 every card is loaded · 1 an orphan card · 2 usage error.
"""

import sys
from pathlib import Path


def main(argv):
    if len(argv) != 3:
        sys.stderr.write(__doc__)
        return 2
    tools, plugin = Path(argv[1]), Path(argv[2])
    sys.path.insert(0, str(tools))
    import context_budget

    loaded = set()
    skills = sorted(plugin.glob("skills/*/SKILL.md"))
    if not skills:
        sys.stderr.write("check_orphans: no SKILL.md under %s\n" % plugin)
        return 2
    for skill in skills:
        start_up, steps = context_budget.skill_steps(str(skill))
        for _name, path in start_up + [f for s in steps for f in s["session"] + s["agents"]]:
            loaded.add(Path(path).resolve())

    cards = sorted(plugin.glob("skills/*/references/cards/*.md")) + sorted(plugin.glob("shared/cards/*.md"))
    orphans = [c for c in cards if c.resolve() not in loaded]
    for c in orphans:
        print("orphan card: %s — no SKILL.md loads it" % c.relative_to(plugin))
    print("check_orphans: %d cards, %d loaded by a skill, %d orphan(s)"
          % (len(cards), len(cards) - len(orphans), len(orphans)))
    return 1 if orphans else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
