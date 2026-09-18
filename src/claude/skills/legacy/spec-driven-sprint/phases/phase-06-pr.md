# Phase 06: Commit / Push / PR

## Entry Gate

```bash
devforgeai-validate phase-check ${ISSUE_ID} --workflow=spec-sprint --from=05 --to=06 --project-root=${PROJECT_ROOT}
# Exit 0: proceed | Exit != 0: Phase 05 incomplete → HALT
```

## Contract

PURPOSE: Push the Phase 04 custody commits, open the PR, and triage CI until all terminal non-skipped checks are in an acceptable state (`SUCCESS`, `NEUTRAL`, `SKIPPING`, or `SKIPPED`).
DELEGATES TO: none mandatory; OPTIONAL `documentation-writer` (if public API/docs changed).
GATE: `gh pr create` is hook-gated (`spec-sprint-completion-gate.sh` block point C) — it is blocked unless phase 05 is `completed` with `checkpoint_passed=true`. `phase-complete --phase=06` is hook-gated (block point D) — it is blocked while any terminal non-skipped CI check on the PR head is in a failing state.

---

## Mandatory Steps

### Step 1: Verify custody commits are ready (NEVER --no-verify)

EXECUTE: If the committed diff touches a source-tree drift trigger path
(`src/claude/{hooks,scripts,agents,commands,skills}/**`,
`.claude/{hooks,agents,commands,skills}/**`, or `devforgeai/specs/**`),
regenerate the source-tree artifact into the sprint worktree before opening or updating the PR.
The default `--output-dir` resolves relative to the process CWD (the main checkout for
spec-sprint phase gates), not to `--root`, so `--output-dir` MUST be passed explicitly for a
worktree sprint:
```bash
devforgeai-validate generate-source-tree --root ${WORKTREE_PATH} --output-dir ${WORKTREE_PATH}/devforgeai/specs/context/source-tree
cd ${WORKTREE_PATH} && devforgeai-validate validate-source-tree --root . --artifact-dir devforgeai/specs/context/source-tree
```
The validation command runs from `${WORKTREE_PATH}` because CWD must equal the tree root to
match CI-style source-tree validation.
Verify `tmp/${ISSUE_ID}/phase-04-commits.json` names the local commits created during Phase 04. If there are no new source/spec files left unstaged, do not create another implementation commit here; Phase 06 pushes the custody commits. If source-tree regeneration produced additional generated files, stage only those explicit paths and commit them with a conventional message that references the issue. Commit the materialized HTML spec in the PR when `$SPEC_OUTPUT_LOCATION` is the worktree. The gate CLI calls (`phase-record`/`phase-complete`) keep `--project-root=${PROJECT_ROOT}` with main-checkout CWD per the `worktree-identity-guard.sh` contract.
VERIFY: `git -C ${WORKTREE_PATH} status --porcelain` is empty before push. If pre-commit fails → fix the validation; **never** `--no-verify` (HALT trigger).

### Step 2: Push + open the PR

EXECUTE: `git -C ${WORKTREE_PATH} push origin <branch>`; `PR_URL=$(gh pr create --body-file tmp/${ISSUE_ID}/pr-body.md)` (body written to a project-scoped tmp file, not inline). Link the issue (`Fixes #${ISSUE_NUMBER}` where appropriate). After `gh pr create` succeeds, extract the PR number and write it to `tmp/${ISSUE_ID}/pr-number.txt`: `echo "$PR_URL" | grep -oE '[0-9]+$' > tmp/${ISSUE_ID}/pr-number.txt`. This file is read by `spec-sprint-completion-gate.sh` Block point D at `phase-complete --phase=06` to assert all non-skipped CI checks are in an acceptable state.
- **DevForgeAI addendum** (when `$DEVFORGEAI_SENTINELS`): keep `STORY-`/`ISSUE-` ids out of the PR **title** (qa-validation quality-gate); dual-path mirror clean (`diff -rq`); CLI-reference drift regenerated if a flag changed; conviction-gate-safe command strings. See `references/devforgeai-addendum.md`.
VERIFY: `gh pr create` succeeded. If the completion-gate (block point C) blocks it → phase 05 is not truly complete; return to Phase 05.
- **Claim release** (if `tmp/${ISSUE_ID}/claim.json` exists and has `"released": false`): write `/release — PR #<pr_number> open` to `tmp/${ISSUE_ID}/release-comment.md` and post via `gh issue comment ${ISSUE_NUMBER} --body-file tmp/${ISSUE_ID}/release-comment.md`. Update `claim.json.released = true`. See `references/claim-protocol.md`. Skip silently if `claim.json` is absent or `{"skipped":"gh-unavailable"}`.

### Step 3: Triage CI

EXECUTE: Poll `gh pr checks --json name,state`. For every check whose terminal `state` is outside `SUCCESS`, `NEUTRAL`, `SKIPPING`, or `SKIPPED` — read the failing job, fix the cause, re-push. This is part of Phase 06, not a new phase. **Never bypass or `--no-verify`.** Continue polling until all non-skipped checks are terminal and acceptable. `IN_PROGRESS`, `PENDING`, `QUEUED`, and null states are not failures; re-poll until they resolve. This applies to ALL non-skipped checks, not only `$REQUIRED_CHECK` — a failing non-required check (e.g. `test-installer`) is triage-required and blocks Phase-06 completion identical to a failing required check.
**Base-branch advanced mid-sprint:** when the base branch advances after the PR was opened (e.g., a CI-fixing commit merged to the default branch) and the failing check is caused by a stale base, run `gh pr update-branch <pr-number>` to take the base in server-side — do **not** run `git merge origin/<default>` inside the sandbox (see `operational-safety.md` Rule 4: it can exit non-zero on read-only `.claude/` paths and leave a partial working tree requiring `git checkout -- <paths>` to restore).
VERIFY: All terminal non-skipped CI checks on the PR head are in state `SUCCESS`, `NEUTRAL`, `SKIPPING`, or `SKIPPED`. Any other terminal state is triage-required. The `phase-complete --phase=06` gate (Block point D in `spec-sprint-completion-gate.sh`) enforces this deterministically — it reads `tmp/${ISSUE_ID}/pr-number.txt`, calls `gh pr checks --json name,state`, and blocks advancement while any non-skipped check is in a failing state.

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${ISSUE_ID} --workflow=spec-sprint --phase=06 --checkpoint-passed --project-root=${PROJECT_ROOT}
# Exit 0: proceed to Phase 07 | Exit != 0: HALT
```
