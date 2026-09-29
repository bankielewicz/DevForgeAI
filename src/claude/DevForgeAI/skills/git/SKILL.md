---
name: git
description: Takes work in a git repository from changed files to merged, synced and cleaned up. It connects a repository to its remote, starts a branch and worktree for the work, classifies changes before staging, scans for secrets, runs the repository's checks, commits, pushes, opens or updates a GitHub pull request, merges only a PR that QA labeled merge-approved and the user confirms, fast-forwards the default branch without losing local edits, and prunes merged worktrees. Use when the user asks to initialize a repository or connect it to a remote, commit changes, commit and push, push a branch, open, update or merge a PR, start a branch or worktree for a task, sync or pull main, check the repository's git or PR status, or clean up old worktrees and branches, even when they don't name the skill. Not for explaining git concepts or commands.
argument-hint: "[status|connect|start|commit|push|pr|merge|sync|prune] [details]"
metadata:
  devforgeai-id: "SKL-006"
  devforgeai-version: "1"
---

# Git

Deliver work in the user's repository: connect it to its remote, isolate the work in a branch and
worktree, decide what belongs in each commit, commit, push, open a pull request, merge it when QA
approved it and the user authorizes the merge, bring the local default branch up to date, and
prune worktrees that are no longer needed. Every phase starts from the repository's real state and
ends with the completion response.

Three rules shape everything below:
- **No data loss.** Never overwrite, reset, clean or remove a path whose content isn't proven to
  exist elsewhere (in a commit, a branch or the incoming version).
- **Nothing outward-facing or destructive without authorization** (the gates below).
- **The repository's rules win.** Its instructions and ADRs override this skill's defaults (worktree
  location, branch names, commit format, checks, merge method, post-merge steps), except the two
  rules above.

## Inputs

- `$ARGUMENTS`, optional: a phase (`status`, `connect`, `start`, `commit`, `push`, `pr`, `merge`,
  `sync`, `prune`), then free text: a remote URL for `connect`, a branch or task for `start`, a PR
  number for `merge`, idle and stale ages in days for `prune` (defaults 14 and 30). With no phase,
  infer the phases from the request and the state report.
- The repository: its git state, its remote, PR data from `gh`, and its instructions (`CLAUDE.md`,
  `AGENTS.md`, `CONTRIBUTING*`, and ADRs or runbooks about branches, worktrees, commits, PRs, merges
  or deploys).
- The conversation: the task, the files this session edited, and authorizations already given in it.

**Tools.** Bash for `git`, `gh` and the scripts; Read, Glob and Grep; Edit and Write only for ignore
files; AskUserQuestion for gates; EnterWorktree with `path`, to move the session into a worktree
this skill created; Skill, only to run documents-updater after the user says yes (step 6). Run
every command from the checkout it targets, with the working directory at that checkout's root.
Never install anything. Never run a `devforgeai` command: that CLI doesn't exist.

Scripts, run with `python3`, all read-only and offline:
- `${CLAUDE_SKILL_DIR}/scripts/repo_state.py [--default-branch NAME]`: the state report (JSON).
- `${CLAUDE_SKILL_DIR}/scripts/scan_staged.py`: the pre-publish scan of the staged content.
- `${CLAUDE_SKILL_DIR}/scripts/qa_state.py`: the PR's QA state, from `gh pr view` JSON on stdin.

Read their JSON; never paste it into the reply.

## Gates: what may run

Every action has a class. Check it before running anything.

| Class | Examples | Allowed when |
|---|---|---|
| Read-only | status, log, diff, fetch, ls-remote, `gh pr view`, `gh pr checks`, the scripts | Always |
| Local, reversible | `git init`, adding a remote, a branch or worktree, staging, a commit, an ignore-file edit, a fast-forward | The request asks for the phase that does it |
| Outward-facing | push, creating or editing a PR, merging, deleting a remote branch | The request names that action ("commit this and open a PR" authorizes the commit, the push and the PR), or the user confirms it in this run |
| Destructive | removing a worktree, deleting a local branch, `git rm --cached`, discarding working-tree content, dropping a stash, rewriting pushed commits | A confirmation naming each target, every time |

- **Merge is never authorized in advance.** It needs QA's approval (step 7) and a confirmation the
  user gives after this run's readiness report.
- Authorization doesn't carry over to a later run. Phases inferred from the request (step 2) count as
  asked for; an outward-facing action still has to be named in the request or confirmed.
- **Asking.** Ask one question per phase, listing the exact commands and targets, with the
  recommended option first. Use AskUserQuestion when it is available and continue once it is
  answered; otherwise ask in plain text and end the turn. **When no answer can arrive** (no user
  is present, or AskUserQuestion isn't available and the run must end), do nothing that needs the
  answer, finish what doesn't, and report `awaiting_approval` with the question in Action required.

**Never run these without a confirmation naming the exact target:** `push --force-with-lease`,
`reset --hard`, `clean`, `checkout --` or `restore` over content not proven identical, `branch -D`,
`stash drop` or `stash clear`, a rebase or amend of pushed commits, `git rm --cached`, deleting a
remote branch, merging unrelated histories.

**Never run these at all:** `push --force` or `-f`, any forced push to the default branch,
`gh pr merge --admin` or `--auto`, any command that adds, removes or creates a QA label or posts a
QA verdict, `--no-verify`, `filter-branch` or `filter-repo`, `worktree remove --force`, and changes
to git configuration outside the repository (`--global`, `--system`). Never stage with
`git add -A`, `git add .`, `git add -u` or `git commit -a`. Never run `git pull` without
`--ff-only`.

Before a step that moves a branch or rewrites commits, record how to undo it: a backup ref
`refs/devforgeai-backup/<branch>/<UTC yyyymmddThhmmssZ>` (local, never pushed), the previous SHA,
or a stash ref. When a step fails midway, stop, leave the state as it is, and give the exact
commands that restore the previous state.

## Decisions that belong to the user

- Every confirmation the gates require, and the merge method (among those the repository allows).
- Which paths are part of the task when the request, the session's edits and the diff don't settle
  it: an uncertain path is never staged, only named.
- Whether to commit despite a failed check or a scan warning. A blocked scan finding is never
  committed, even when the user asks.
- Changing `origin`, merging unrelated histories, renumbering a colliding document ID, removing
  ignored files that aren't regenerable, and deleting backup refs.
- Whether to run documents-updater before a PR.
- QA verdicts and labels belong to an independent QA session or the human, never to this skill,
  even when asked (step 7).

## Workflow

Copy this checklist into your response, and tick each step or mark it `(skipped: <reason>)`:

```
- [ ] 1. Preflight and state report
- [ ] 2. Choose the phases
- [ ] 3. connect
- [ ] 4. start
- [ ] 5. commit
- [ ] 6. push / pr
- [ ] 7. merge
- [ ] 8. sync
- [ ] 9. prune
- [ ] 10. Report
```

### 1. Preflight and state report

Follow [references/preflight-and-connect.md](references/preflight-and-connect.md). With read-only
commands: confirm the repository root and whether this is the main checkout or a linked worktree;
read the repository's instructions; check that git runs, that `user.name` and `user.email`
resolve, whether HEAD is detached and whether an operation is in progress. For phases that use the
remote, check it is reachable (`git ls-remote`) and read its default branch with
`git ls-remote --symref origin HEAD`; never assume `main`. Check `gh` (installed, `gh auth status`)
only before a step that needs it. Fetch, then run `repo_state.py` and base every decision on it.

Stop with ERR-01 when git is missing or this isn't a repository and nobody asked to create one,
and with ERR-05 when an operation is in progress or HEAD is detached and the phase needs a branch.
When the report shows `sandbox.git_config_write_masked`, plan every phase without `.git/config`
writes (`--no-track`, a push without `-u`) and report what still can't run (ERR-16).

### 2. Choose the phases

Take the phase from the first argument, or infer the phases from the request and the report: "open
a PR for my changes" with uncommitted work runs start, commit and pr. Order: connect, start,
commit, push, pr, merge, sync, prune. Skip what the request doesn't need, and stop at the first
gate that needs an answer. When `start` carries uncommitted work, it makes that work's first commit
(applying step 5's rules first); `commit` is for later commits in the worktree. `status` runs step 1, reports the changes, the default branch's
ahead/behind state, the worktrees and the PR's QA state, and changes nothing. Before each phase,
check whether its result already exists (origin set, branch or worktree present, change committed,
branch pushed, PR open, PR merged, default branch up to date), and report it rather than repeat it.
Nothing to deliver (no task changes, no commits beyond the base) is ERR-14: create nothing and
report `no_change`. A request for a commit message only drafts it.

### 3. connect

[references/preflight-and-connect.md](references/preflight-and-connect.md): `git init` when asked,
`origin` from the given URL, a fetch, and adopting or bootstrapping the remote's history. Never
replace a different existing `origin` (ERR-03) or push over unrelated history (ERR-04). A push to an
empty remote is outward-facing: offer the bootstrap commit unless the request names the push.

### 4. start

[references/preflight-and-connect.md](references/preflight-and-connect.md): the branch name and the
worktree under `.claude/worktrees/<name>` (unless the repository sets another place), kept out of
git by `.git/info/exclude`.
- **No uncommitted work to carry:** create the branch and worktree together from the fetched
  `origin/<default>`.
- **Uncommitted work to carry:** classify, stage, scan and check it (step 5), then `git switch -c
  <branch>` at the current HEAD, commit, verify each carried path by hash, switch back, and only then
  add the worktree on that branch. Never move work with stash, copies or patches. The rebase onto
  `origin/<default>` comes before the push (step 6).

Then enter the worktree with EnterWorktree (`path`) when available, or tell the user how to open it.

### 5. commit

Follow [references/classify-and-commit.md](references/classify-and-commit.md):
1. **Classify** every change as `task`, `unrelated`, `local` or `blocked`; an uncertain path isn't
   staged. Stage task paths only, by explicit path (`git add -- <paths>`). Propose ignore patterns
   for local paths in the reply; write them only when asked or confirmed.
2. **Scan**: run `scan_staged.py`. A blocked finding stops the commit (ERR-06); a warning needs the
   user's yes. Name file and line, never a secret's value.
3. **Check**: run the checks the repository's instructions require, as they say, and report each
   as passed, failed or not run. A failed check stops the commit (ERR-07) unless the user confirms.
4. **Commit** in the repository's message convention, one commit per logical change, letting hooks
   and signing run.

### 6. push / pr

Follow [references/publish-and-merge.md](references/publish-and-merge.md), in this order:
1. **`pr` only:** when the branch changes neither README nor CHANGELOG, recommend
   `/devforgeai:documents-updater` and ask whether to run it first. Run it only on the user's yes;
   with a no, or no answer possible, continue and list "documentation not reviewed".
2. Fetch, and run the state report in the branch's checkout. **`pr` only:** stop on a colliding
   document ID (ERR-15), before any rebase.
3. When the base moved and the branch's commits are unpushed, rebase them onto `origin/<default>`;
   on a conflict run `git rebase --abort` and stop (ERR-08). Push the branch.
4. **`pr` only:** now check `gh` and a GitHub remote (ERR-02), then reuse the branch's open PR or
   create one. Name the next step: an independent QA session reviews the PR.

### 7. merge

Follow [references/publish-and-merge.md](references/publish-and-merge.md). Derive the QA state with
`gh pr view <n> --json labels,comments,headRefOid | python3 ${CLAUDE_SKILL_DIR}/scripts/qa_state.py`.
Give the readiness report. Offer the merge only when the QA state is `approved` and nothing else
blocks it (ERR-10). Merge only after the user confirms, with the method they choose and
`--match-head-commit <head SHA>`. A `failed` state sends the PR back to development: report QA's
findings as the work to do. Never add, remove or create a QA label, and never post a verdict.

### 8. sync

Follow [references/sync-and-prune.md](references/sync-and-prune.md). `git fetch --prune`, record a
backup ref for the local default branch, then act on its state: fast-forward only when it is
behind; stop when it is ahead or diverged (ERR-11). Before a fast-forward that would overwrite local
edits, reconcile each path: restore or remove it only when its content and mode equal the incoming
version; otherwise keep it byte-identical and stop (ERR-12). Then run or report the repository's
post-merge steps.

### 9. prune

Follow [references/sync-and-prune.md](references/sync-and-prune.md). Inventory the linked
worktrees from the state report. A worktree is removable only when it is merged or closed, clean,
fully pushed, not locked and not current; age never makes one removable. Report every other
worktree with its reason, disk size and activity (idle at 14 days, stale at 30; a locked one is
reported as locked). Remove removable ones only after one confirmation listing them, with
`git worktree remove` (never `--force`, never `rm`), then retire their branches safely.

### 10. Report

Read [references/output-rules.md](references/output-rules.md) and check its self-check list. End
the reply with the completion response, and put nothing after it.

## Output contract

The last thing in the reply, with empty fields omitted:

```text
Result: done | partial | blocked | awaiting_approval | no_change
Phases: <phases run, in order>
Branch: <branch> → <base>
PR: <URL, state>
Checks: <each check: passed, failed or not run>
Changes: <committed, left unstaged, proposed for ignoring, blocked>
Action required: <approval needed, conflict, recovery command, the user's own step>
```

`done`: every requested phase finished. `partial`: some finished and an issue remains. `blocked`:
nothing could proceed. `awaiting_approval`: a gate needs an answer. `no_change`: everything
requested was already done. Show the ticked checklist once, before this block.

## Examples

**Deliver uncommitted work.** "Commit my --json change on branch feat/json-output and push it; notes/todo.md
is other work." The skill classifies `app.py` and its test as task, `notes/todo.md` as unrelated,
`__pycache__/` as local. It stages the task paths, scans, runs the required tests, creates
`feat/json-output` at HEAD, commits, verifies the carried paths, switches back, and adds the worktree.
Inside it, it rebases onto the fetched `origin/main`, reruns the tests and pushes. It proposes
ignore patterns for the local paths and reports `Result: done`.

**Merge.** "Merge PR 42." The QA state is `stale`: QA's passing verdict names an older commit. The
skill gives the readiness report, doesn't offer the merge, and reports `Result: blocked`: an
independent QA session must review the new head.

**Sync.** "Sync main with origin." Main is two commits behind, and an uncommitted edit to
`config.yaml` differs from the incoming version. The skill keeps the edit byte-identical, doesn't
move main, and offers to carry the edit to a branch or stash it by name.

## References

- [references/preflight-and-connect.md](references/preflight-and-connect.md): steps 1, 3 and 4.
  Preflight, the sandbox, connect, branch and worktree naming, carrying pending work.
- [references/classify-and-commit.md](references/classify-and-commit.md): step 5. Change classes,
  ignore rules, the scan, checks and commit messages.
- [references/publish-and-merge.md](references/publish-and-merge.md): steps 6 and 7. Rebase, push,
  documentation, the PR, QA and the merge.
- [references/sync-and-prune.md](references/sync-and-prune.md): steps 8 and 9. Sync states,
  per-path reconciliation, retiring branches, prune.
- [references/output-rules.md](references/output-rules.md): step 10. The completion response, the
  forbidden commands and the self-check list.
