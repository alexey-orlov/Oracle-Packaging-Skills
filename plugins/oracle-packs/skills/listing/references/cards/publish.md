# Publishing

**What this is.** Putting the changed site live, **only when the owner asks**, with the three gates green. Every value comes from the site manifest's `publish` block, never from memory: the target is `publish.target`; `publish.neverPublishTo` is refused; any other target makes a *second* page.

**The checks**

1. **Strip the wrapper by exact line, never by prefix.** Remove `publish.wrapper.stripExactLines` from `wrapper.from` into `wrapper.to` with `grep -v -x -F`, then `diff`: exactly those lines differ (a prefix strip on `<head` once removed the masthead).
2. **Publish from where the tool can read**: the Artifact tool reads only the session's folder and its scratchpad. With the site root outside it, copy the wrapper and every published file under a copy of the publish root in the scratchpad, and publish from there.
3. **Read the live page once per session before publishing**, or it is refused.
4. **Root plus a files map**: root at the publish root, and published path → source path for **every changed or added file**, fonts typed per `publish.contentTypes`. Files not passed are kept, so **new images go in explicitly**. A full-tree publish follows `publish.fullTree`: never the whole folder, and never a path in `publish.neverInArtifact`.
5. **On a refusal**, diff the live copies of your files against local; the working tree is the merge; publish again. **Never force past a conflict.**
6. **Confirm what is live** with the platform's file listing: every new file is live, **and nothing that should not be** (it once found three customer logos on a link-shared page).
7. **A walkthrough is its own page.** Publish it standalone, record its URL in `links.json` (`interactiveDemoArtifact`) and run `paths.syncLinks`. `data/links.js` is never a file under the publish root: the publish builds it (`paths.buildSiteLinks` into `paths.siteLinks`) and maps it. Open the walkthrough in a new tab.
