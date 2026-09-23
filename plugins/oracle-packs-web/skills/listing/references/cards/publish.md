# Publishing

**What this is.** Putting the changed site live — **only when the owner asks**, and only with the three gates green. The target is the owner's input, never assumed: publishing without it creates a *second* page and the link already shared goes stale.

**The checks**

1. **Strip the wrapper by exact line, never by prefix.** A hosted preview supplies its own skeleton, so the copy handed over carries only the body content plus the site's own `<title>`. `grep -v -x -F -e '<!DOCTYPE html>' …` into a git-ignored `.work/publish/`, then `diff`: exactly those lines differ. A prefix strip on `<head` once removed `<header class="masthead">`; keeping the meta lines shipped them twice inside `<body>`.
2. **Read the live page once in the session before the first publish**, or the publish is refused as not built on the newer version.
3. **Root plus a files map**: root at the publish root, the map published path → source path, for **every changed or added file**. Files not passed are kept; **new images must be passed explicitly**. Publish the **full tree** when another session may have touched renderer files.
4. **On a refusal**, read the live copies of the files you changed, diff them against local, treat the working tree as the merge, and publish again. **Never force past a conflict.**
5. **Confirm what is live** with the platform's file listing: every new file is live, **and nothing is live that should not be**. The second is the one that matters — it is how three customer logo files were found on a link-shared page, downloadable by path, long after the data layer stopped referencing them.
6. **A walkthrough is its own page**: publish it standalone, put that URL in `demoPreviewUrl`, leave `demoUrl` canonical, and open it in a new tab.
