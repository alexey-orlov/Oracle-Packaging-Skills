# Delivery and the closing message

**What this is.** Copying the approved files where the owner keeps the pack, logging what was decided, and closing the run in one message.

**Where.** The finals go to the pack's folder in the practice OneDrive, `Oracle AI & Data Solutions/<Pack name>/`: the files the mini-site's sales-kit email links to. Drafts and working files never go there; they stay in `<work>/`. Where that folder is not synced on this machine, ask once where it is. Copy the approved files from `<work>/artifacts/`, keeping the pack's file-name pattern: `<Pack name> - <Artifact> - Oracle.<ext>`.

**The log.** Append one line per artifact to `<work>/decisions.md`: the date, the channel, the file, its spec stamp (`shared/tools/py shared/tools/spec_stamp.py <file>`), and what changed on review.

**The closing message**, in the owner's words: the files and where they are; what was decided differently from the pack brief and why; and the open items the owner still holds — named as parts of the pack, not as keys or steps.

**Checks**

1. Every delivered file follows `<Pack name> - <Artifact> - Oracle.<ext>`.
2. Only approved artifacts are copied; anything stopped or unapproved is named as not delivered.
3. `decisions.md` carries one line per delivered artifact, with its spec stamp and what changed on review.
4. The closing message names the open items as parts of the pack — never spec keys, file names, step names or the channel words.
5. The delivery folder was asked for at most once, never once per artifact.

**Good.** `Damage assessment - Feature list - Oracle.docx`
**Bad.** `damage-assessment_feature-list_internal_v3.docx`

**Reads:** the approved files in `<work>/artifacts/` and the channel settled at the map. **Writes:** `<work>/decisions.md`, and the delivery folder.
