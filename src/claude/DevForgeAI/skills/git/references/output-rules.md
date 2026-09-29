# Output rules

## Contents

- The completion response
- Reporting rules
- Forbidden commands
- Self-check list

## The completion response

The last thing in the reply, after the ticked checklist, with empty fields omitted and nothing after
it:

```text
Result: done | partial | blocked | awaiting_approval | no_change
Phases: <phases run, in order>
Branch: <branch> → <base>
PR: <URL, state>
Checks: <each check: passed, failed or not run>
Changes: <committed, left unstaged, proposed for ignoring, blocked>
Action required: <approval needed, conflict, recovery command, the user's own step>
```

| Result | When |
|---|---|
| `done` | Every requested phase finished |
| `partial` | Some requested phases finished and an issue remains (a check failed, `gh` missing for the PR, a sandbox block) |
| `blocked` | Nothing could proceed (not a repository, an operation in progress, a blocked scan finding, a rebase conflict, QA not approved) |
| `awaiting_approval` | A gate needs the user's answer: the question goes in Action required |
| `no_change` | Everything requested was already done, or there was nothing to deliver |

- **Checks:** each check with its command and result, for example
  `python3 -m unittest: passed (12 tests)`, `git diff --cached --check: passed`. `not run` says why.
- **Changes:** name paths or short groups: committed (with the commit's subject), left unstaged
  (unrelated, uncertain), proposed for ignoring (with the pattern and the file it belongs in),
  blocked (file and line, never a value).
- **Action required:** anything the user must do: approve (the exact question), resolve a conflict
  (the paths), run a command the session can't (the command and why), an independent QA review,
  the repository's post-merge step, a recovery command after a failure.

## Reporting rules

- Report the state after the run, from git itself (`git log -1`, `git status`), not from memory.
- Never paste the state report, the scan JSON or full command output; quote only the lines that
  matter (a conflict path, a hook's error, a remote's rejection).
- Never print a secret's value, even partly.
- Say what was verified and what wasn't: a check not run, documentation not reviewed, PR state not
  read without `gh`.
- When the remote is public or its visibility is unknown and something was pushed, say it is
  published.
- In `status`, report: the branch and checkout, the default branch's state with ahead/behind counts,
  the changes grouped by class, the worktrees (branch, activity, lock, merged), and the PR's QA state
  when `gh` can read it.

## Forbidden commands

Never run without a confirmation naming the exact target, given in this run:

| Command | Why |
|---|---|
| `git push --force-with-lease=<branch>:<sha>` | Replaces remote commits |
| `git reset --hard` | Discards working-tree and index content |
| `git clean` | Deletes untracked files |
| `git checkout -- <path>` / `git restore <path>` over content not proven identical to what replaces it | Discards edits |
| `git branch -D` | Deletes a branch git considers unmerged |
| `git stash drop` / `git stash clear` | Deletes stashed work |
| Rebase or amend of pushed commits | Rewrites published history |
| `git rm --cached` | Deletes the file for everyone once merged |
| `git push origin --delete <branch>` | Deletes a remote branch |
| `git merge --allow-unrelated-histories` | Joins unrelated histories |

Never run at all:
- `git push --force`, `git push -f`, a `+<refspec>` push, or any forced push to the default branch;
- `gh pr merge --admin` or `--auto`, and `gh pr merge --delete-branch`;
- any command that adds, removes or creates a QA label (`gh pr edit --add-label`/`--remove-label`
  with a QA label, `gh label create`) or posts a QA verdict;
- `--no-verify`, `--no-gpg-sign`, or a `-c` override of hooks or signing;
- `git filter-branch`, `git filter-repo`;
- `git worktree remove --force`, or `rm` on a worktree;
- `git config --global` or `--system`, and any other change to git configuration outside the
  repository;
- `git add -A`, `git add --all`, `git add .`, `git add -u`, `git commit -a`;
- `git pull` without `--ff-only`;
- changes to Claude Code's sandbox or permission settings.

## Self-check list

Before the completion response, confirm each item:

1. Every decision came from the state report run after the fetch, and the default branch came from
   the remote, not an assumption.
2. No forbidden command ran; every confirmation-only command ran after a confirmation naming its
   target, given in this run.
3. Only task paths were staged, by explicit path. Unrelated, local, uncertain and blocked paths are
   unstaged and named; sandbox write masks were never staged.
4. The scan ran on the staged content before every commit, and no blocked finding was committed.
5. Each required check is reported with its command as passed, failed or not run.
6. Carried work was verified by hash before switching back (when it applied).
7. Every branch move or rewrite has a backup ref or a recorded SHA, and a failed step's recovery
   commands are in Action required.
8. Nothing was pushed, and no PR was created or edited, unless the request named it or the user
   confirmed it in this run.
9. No merge happened without the `approved` QA state and a confirmation given after this run's
   readiness report, with `--match-head-commit`. No QA label was touched and no verdict posted.
10. No worktree, branch or file was removed without proof that its content exists elsewhere and a
    confirmation naming it. A locked worktree is reported as locked.
11. A differing local edit is byte-identical to how it started.
12. The reply never says the session is working in a worktree unless EnterWorktree moved it there (a
    Bash `cd` doesn't); otherwise it gives `claude --worktree <name>` to open it.
13. The reply ends with the completion response, and its Result matches the definitions above.
