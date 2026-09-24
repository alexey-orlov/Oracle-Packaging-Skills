# Running agents — how a skill's subagents are written and watched

_Read once, when a skill writes a subagent's prompt: the four rules every subagent in the plugin follows. Rewritten to current truth — never appended with dated updates._

1. **Model routing.** Mechanical work runs on Opus: searches, extraction, lookups, builds from a settled design, rendering QA, captures. The strongest available model is spent only on the judgement passes a skill names as such — the editorial pass, the design decisions, the final synthesis. Say which step used which.

2. **Tools, spelled out in every agent's prompt.** Read with Read or Grep and edit with Edit or Write — never through the shell. Bash only for allow-listed commands, one command per call, with absolute paths; never `cd … && …`, never any `&&` or `;` chain. No permission rule can match a chain, and an unattended agent that meets a permission prompt does not fail — it hangs.

3. **Progress that can be checked.** A long-running agent writes its progress log early, one line per unit of work — per file, per screen, per source — never one per stage, which cannot tell a long stage from a hang. The session checks the log's modification time at the cadence the work should keep. When the log has stopped, check the agent's own transcript as well; if that has stopped too, stop the agent and take over from what it already wrote. Never resume it blindly, and never wait on a completion notice.

4. **Agents report; the session rewrites.** A subagent never appends to or edits a reference document — anything under `shared/references/`, a card, a README. It reports what it found wrong, and the main session rewrites the file to current truth.
