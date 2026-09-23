# Delivery and the closing message

**What this is.** Copying the approved files where the owner keeps the pack, logging what was decided, and closing the run in one message.

**Where.** Ask once for the delivery folder; the owner's convention is the pack's own folder on the practice's shared drive, next to the earlier artifacts. Copy the approved files there, keeping the pack's file-name pattern: `<Pack name> - <Artifact> - Oracle.<ext>`.

**The log.** Append one line per artifact to `packs/<slug>/decisions.md`: the date, the channel, the file, and what changed on review.

**The closing message**, in the owner's words: the files and where they are; what was decided differently from the pack brief and why; and the open items the owner still holds — named as parts of the pack, not as keys or steps.

**Checks**

1. Every delivered file follows `<Pack name> - <Artifact> - Oracle.<ext>`.
2. Only approved artifacts are copied; anything stopped or unapproved is named as not delivered.
3. `decisions.md` carries one line per delivered artifact, with what changed on review.
4. The closing message names the open items as parts of the pack — never spec keys, file names, step names or the channel words.
5. The delivery folder was asked for once, not once per artifact.

**Good.** `Damage assessment - Feature list - Oracle.docx`
**Bad.** `damage-assessment_feature-list_internal_v3.docx`

**Reads:** the approved files and the channel settled at the map. **Writes:** `packs/<slug>/decisions.md`, and the delivery folder.
