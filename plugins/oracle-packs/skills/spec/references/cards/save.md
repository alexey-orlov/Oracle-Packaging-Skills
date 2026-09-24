# Saving the pack to the shared repo

**What this is.** How a change to the pack's shared files reaches the packaging-skills repo, so a colleague builds from the same spec. Shared means `packs/<slug>/`: the spec and its pictures. Run it when the spec is confirmed, after any change to a confirmed spec and after pictures are recorded.

**The calls** — three, each its own, never chained; `<repo>` is the checkout `pack_paths.py` printed:

    git -C <repo> add packs/<slug>
    git -C <repo> commit -m "spec(<slug>): <what>" -- packs/<slug>
    git -C <repo> push

`<what>` is `confirmed` on confirmation, else the change in a few words: `pictures`, `architecture`, `PoV price`.

**Checks**

1. Only `packs/<slug>` is added and committed — anything else staged in the checkout stays out of the commit. The work folder — artifacts, intake, inventory, research, decisions — never enters the repo.
2. A push the remote rejects is reported in one plain line and left for the owner: never forced, never overwritten.
3. A commit or push the environment cannot make — no network, no credentials — is reported as not saved yet and retried before the run closes, never skipped silently.
4. Nothing to commit is not an error: say nothing.
5. The owner hears one plain line at most: saved to the shared repo, or what stopped it.

**Good.** "Saved to the shared repo, so a colleague builds from the same brief."
**Bad.** "`git push` exited 1: non-fast-forward; retrying with --force."
