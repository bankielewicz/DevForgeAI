# Sync, retire branches and prune

## Contents

- sync: states
- sync: per-path reconciliation
- sync: afterwards
- Retiring a merged branch
- prune: inventory and removal

## sync: states

1. `git fetch --prune origin`, then the state report.
2. Record a backup ref for the local default branch before moving it:
   `git update-ref refs/devforgeai-backup/<default>/<UTC yyyymmddThhmmssZ> refs/heads/<default>`
   (for example `date -u +%Y%m%dT%H%M%SZ`).
3. Act on `default_branch.state`:

| State | Action |
|---|---|
| `up_to_date` | Nothing to do: `no_change` |
| `behind` | Fast-forward: `git merge --ff-only origin/<default>` in the checkout that has the branch checked out (`checked_out_at`); `git fetch origin <default>:<default>` when no checkout has it. Reconcile first (below) |
| `ahead` or `diverged` | ERR-11: don't move it |
| `unrelated` | Don't move it: stop as for ERR-04 (preflight-and-connect.md) and report `awaiting_approval` |
| `no_remote` or `empty_remote` | Nothing to sync from; say so (`no_change`). Pushing to an empty remote is `connect`'s bootstrap |
| `unknown` | Fetch, or pass `--default-branch`, and read the report again |

**ERR-11.** List the local-only commits (`git log --oneline origin/<default>..<default>`: SHA and
subject) and offer to move them onto a new branch for a PR (recommended), or leave the branch as it
is. Resetting the default branch afterwards needs its own confirmation and a backup ref. Report
`awaiting_approval`.

Never run `git pull` without `--ff-only`, `git reset --hard`, `git clean`, or `git checkout --` /
`git restore` on a path not proven identical.

## sync: per-path reconciliation

When the checkout holding the default branch has uncommitted changes or untracked files, look at
each path's `incoming` value in the report (computed against the fetched `origin/<default>`):

| `incoming` | Meaning | Action |
|---|---|---|
| `untouched` | The incoming commits don't change the path | Leave it as it is: the fast-forward keeps it |
| `identical` | Its content and mode equal the incoming version (or both are absent) | The local change is already upstream, so restoring or removing it loses nothing: `git checkout HEAD -- <path>` for a tracked path (it resets the index too, where `git checkout -- <path>` would restore a staged copy), `rm -- <path>` for an untracked one. The fast-forward then writes the same content |
| `differs` | The local version differs from what the fast-forward would write | ERR-12 |

Confirm `identical` yourself before discarding anything:
`git hash-object <path>` equals `git rev-parse origin/<default>:<path>` and the modes match
(`git ls-tree origin/<default> -- <path>`), or both are absent.

**ERR-12.** Keep every differing path byte-identical and don't move the branch; don't reconcile the
other paths either. List the differing paths and offer:
(a) carry the changes to a new branch and worktree (preflight-and-connect.md, recommended);
(b) a named stash, after a confirmation: `git stash push -u -m "devforgeai-sync <UTC>" -- <paths>`;
(c) leave the branch unsynced.
Report `awaiting_approval`.

When the main checkout is on a feature branch whose PR has merged, switch it to the default branch
only when it is clean, or reconciled as above.

## sync: afterwards

Run the repository's post-merge steps (for example a redeploy), or report them as the user's step
when the session can't run them. Then report the new SHA of the default branch and the backup ref.

Local branches whose work is now merged (a merged PR's branch, the feature branch the main checkout
just left) are retired as below, which removes their worktrees first and asks before any deletion.

## Retiring a merged branch

Only when that loses nothing, and only after removing its worktree (git refuses to delete a branch a
worktree has checked out). Deleting a local branch is destructive: ask once, naming each branch.
- `git branch -d <branch>` when the branch is an ancestor of `origin/<default>`.
- Squash- or rebase-merged PR (`git branch -d` refuses): `git branch -D <branch>` only after
  `gh pr view <branch> --json state,headRefOid` shows `MERGED` with a `headRefOid` equal to the local
  tip, and after a confirmation naming the branch.
- Keep and report a branch with commits beyond the PR's head, or with no merged PR.
- Delete backup refs only when the user asks.

## prune: inventory and removal

1. Inventory the linked worktrees from `git worktree list --porcelain` and the report's
   `worktrees[]`: branch, last activity and size, uncommitted or untracked files, ignored files,
   unpushed commits, lock, whether it is the session's current directory, and whether its branch
   merged (`merged_by_ancestry`, or with `gh`, a `MERGED` PR whose head equals the tip) or its PR
   closed. Without `gh`, judge by ancestry only and say so. Never touch the main checkout.
2. **Removable** only when all hold: merged or closed; no uncommitted or untracked files
   (`uncommitted` 0); nothing unpushed (`unpushed` 0); not locked; not current. Age never makes a
   worktree removable, and a removable one needs no minimum age.
3. **ERR-13.** Keep every other worktree and its branch, and list it with the reason it was kept
   (uncommitted or untracked files, unpushed commits, locked, current, not merged), its disk size
   (`size_bytes`, in MB) and its activity: `idle` when the last activity is at least 14 days old,
   `stale` at 30 days (the `prune` argument may change both; pass `--idle-days`/`--stale-days` to
   the report). **A locked worktree is reported as locked, never as idle or stale:** a lock is how a
   user keeps one on purpose.
4. **Ignored files.** `git worktree remove` deletes ignored files without warning. List each
   removable worktree's `ignored` entries and ask about any that isn't regenerable output (such as
   `.env`, local settings or data); keep the worktree unless the user clears them.
5. Flag removable worktrees with `modified_within_hour`: another session may be working there.
6. **Confirm once**, listing each removable worktree and its branch. With no answer possible,
   remove nothing and report `awaiting_approval`. Otherwise remove each with
   `git worktree remove <path>`, never `--force`, never `rm`; then retire its branch as above,
   keeping the branch of a closed, unmerged PR.
7. Administrative entries whose directory is gone (`prunable: true`): show
   `git worktree prune --dry-run -v`, then run `git worktree prune`.
