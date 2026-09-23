# Brand fonts — shipped privately, for practice members only

The four faces every print artifact is set in, so a build on any practice member's machine fits and renders as it does on the owner's:

| File | Face | Used by |
|---|---|---|
| `Azurio-Regular.otf`, `Azurio-Semibold.otf` | Azurio (display) | the feature list's title; deck and one-pager display type |
| `ReplicaLLTT-Regular.ttf`, `ReplicaLLTT-Bold.ttf` | Replica LL TT (text) | everything else: body, tables, labels, legends |

**Licence.** These are SoftServe's licensed brand fonts, distributed to practice members through the company's managed font set. They sit in this private repository so that the packaging tools work on a colleague's machine; they are not redistributable. Never copy them into a public repository, an artifact, a mini-site bundle or a customer deliverable. The `.docx` and `.pptx` builders reference the faces by name and never embed the files.

**Where the files come from.** The owner's Mac holds them in `/Library/Fonts/Managed/` (the managed set) with a numeric suffix on each name. They go here without the suffix, exactly as named above.

**Install.** `shared/tools/py shared/tools/install_fonts.py` copies them into the current user's font folder (macOS `~/Library/Fonts`; Windows the per-user fonts folder plus its registry entries; Linux `~/.local/share/fonts`). A machine that already has them through the managed set needs nothing.

**Fit without installing.** The builders' text-fit estimate reads these files straight from this folder when they are present, so fit reports are exact on every machine; installing matters only for what a render shows. When the folder holds no files the builders fall back to Helvetica-metric stand-ins with headroom, as before.
