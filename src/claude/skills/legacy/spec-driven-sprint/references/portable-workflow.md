# Portable Workflow Core (consumer-safe)

The generic, runtime-detected rules that apply in **any** repository the
spec-driven-sprint skill runs in. Nothing here is specific to one host project:
every value is either generic or detected at runtime (default branch, required
check, test runner). Host-specific mechanics live in `devforgeai-addendum.md`,
applied **only** when the Phase 00 sentinels are present.

---

## Git & worktree pre-flight (ordered)

Run BEFORE creating the worktree (Phase 00 → Phase 03):

1. **Connectivity + auth** — confirm the git remote is reachable; if a PR will be
   opened, the host CLI (`gh`/`glab`/equivalent) is authenticated. HALT →
   AskUserQuestion if not.
2. **Fetch** — `git fetch origin --prune` so the remote tip is current and stale
   remote-tracking refs are cleared.
3. **Fast-forward the local default (FF-ONLY)** — sync local `<default>` to
   `origin/<default>`. Fast-forward only — never force, never clobber. If it
   cannot fast-forward (local diverged) → HALT (do not reset).
4. **Working-tree sanity** — abort if a merge/rebase/cherry-pick is in progress;
   stage with explicit paths, **NEVER `git add -A`** (it sweeps machine-local
   files and reverts others' state).
5. **Worktree hygiene + resume** — `git worktree prune`; if a worktree/branch
   already exists for THIS issue → RESUME it (idempotent).
6. **Branch off the REMOTE tip** — create the worktree off `origin/<default>`
   with branch `<type>/<issue-slug>` (`feat`/`fix`/`chore`), NOT off local
   default (defense in depth).
7. **Resolve deps in the worktree** — symlink or install so tooling resolves.

### The 4 pristine-main rules

1. **Branch off the remote default tip** (`origin/<default>`), never stale local default.
2. **Fetch before branching** so the remote tip is current.
3. **Fast-forward only** when syncing the local default — never force/clobber a diverged local.
4. **If `origin/<default>` advances DURING the work, merge `origin/<default>` INTO the branch** (not rebase onto the moved tip — merge protects already-merged sibling PRs from an auto-merge-race revert). For JS/TS repos, `node -e "require('./<file>')"` each merged file to catch duplicate-`const` fatals (language-gated).

### Lock-file recovery

On `Unable to create '…/.git/*.lock'`:
- **Active lock** (a live git process holds it): wait ~3s and retry — **never `rm`** an actively-held lock.
- **Stale lock** (lock file exists, `ps aux | grep -v grep | grep git` returns empty): `rm -f .git/index.lock`, then log a warning before retrying. A stale lock is safe to remove; an active lock is not.

For full recovery steps and WSL2-specific guidance, see
`.claude/skills/spec-driven-dev/references/git-workflow-conventions.md` (§ Lock File Recovery).

---

## Commit / push / PR

- **Land the complete reviewed change in one push** — some hosts auto-merge a PR
  the instant the required check goes green, so a "push commit 1 → review → push
  commit 2" plan can lose commit 2. Land it all at once.
- **Conventional commit; pre-commit must run** — `--no-verify` is forbidden. Fix
  the validation, do not bypass it.
- **Merge on the green required check** — detect the repo's required check(s) at
  runtime via the host CLI (e.g. `gh pr checks` / branch-protection API); do not
  assume a check name. Never merge red.
- **PR body via a file** — write the body to a project-scoped `tmp/<id>/` file and
  pass it with `--body-file`, avoiding inline-string quoting pitfalls.
- **CI triage** — if the required check fails after push, read the failing job,
  fix the cause, re-push. Never bypass.

---

## Dogfood-first

The first real run of a freshly built skill IS the smoke test. Plan the first
invocation as the proof: a concrete corpus issue, a watch-list of what to verify,
and an explicit fix-vs-defer policy for whatever the run surfaces.

---

## Provenance

Distilled from cross-session workflow lessons (remote-tip branching, one-push
auto-merge race, ff-only sync, merge-into-branch reconciliation, lock-file
recovery, dogfood-first). Host-specific enforcement is intentionally excluded —
see the sentinel-gated `devforgeai-addendum.md`.
