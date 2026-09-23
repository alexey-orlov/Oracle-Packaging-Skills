# Publishing

**What this is.** Putting the changed site live, **only when the owner asks**, with the three gates green. Every value below comes from the site manifest's `publish` block, never from memory. The target is `publish.target`, and anything in `publish.neverPublishTo` is refused. Any other target makes a *second* page.

**The checks**

1. **Strip the wrapper by exact line, never by prefix.** Remove `publish.wrapper.stripExactLines` from `wrapper.from` into `wrapper.to` with `grep -v -x -F`, then `diff`: exactly those lines differ. A prefix strip on `<head` once removed the masthead.
2. **Publish from where the tool can read.** The Artifact tool reads only the session's working folder and its scratchpad. When the site root is outside it, copy the wrapper and every file you publish into the scratchpad, under a copy of the publish root, and publish from there.
3. **Read the live page once per session before the first publish**, or it is refused.
4. **Root plus a files map**: root at the publish root, and published path → source path for **every changed or added file**, fonts typed per `publish.contentTypes`. Files not passed are kept, so **new images go in explicitly**. A full-tree publish follows `publish.fullTree`: never the whole folder, and never a path in `publish.neverInArtifact`.
5. **On a refusal**, diff the live copies of your files against local. The working tree is the merge; publish again. **Never force past a conflict.**
6. **Confirm what is live** with the platform's file listing: every new file is live, **and nothing is live that should not be**. That check once found three customer logos on a link-shared page.
7. **A walkthrough is its own page.** Publish it standalone, record its URL where `publish.demoTargets` says (`links.json`, `interactiveDemoArtifact`), run `paths.syncLinks`, include `data/links.js` in the publish (`publish.fullTree`), and open it in a new tab.
