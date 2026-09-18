# Phase 08: Git Workflow & Commit

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --from=07 --to=08
# Exit 0: proceed | Exit 1: Phase 07 incomplete (DoD not validated) | Exit 2: DoD validation failed
```

## Contract

PURPOSE: Stage files, create a properly formatted git commit, and verify commit success.
REQUIRED SUBAGENTS: None (git operations only)
REQUIRED ARTIFACTS: None
STEP COUNT: 6 mandatory steps

**GIT POLICY:** See `.claude/rules/core/git-operations.md` for safe vs approval-required operations.

## Reference Loading [MANDATORY]

```
# No required references for this phase. Self-contained — git workflow
# operations only; error-recovery Read of
# .claude/rules/workflow/commit-failure-recovery.md sits outside the 4
# declared categories (skill ref / context file / memory / story).
```

---

## Mandatory Steps

### Step 1: Budget Enforcement Check

EXECUTE: Check deferral budget for this story via CLI.
```bash
devforgeai-validate check-deferral-budget --story-file=${STORY_FILE} --project-root=${PROJECT_ROOT}
```
VERIFY: Exit code 0 = within budget.
```
IF exit code == 1: HALT — "Deferral budget exceeded."
IF new incomplete items detected: Return to Phase 06.
```

### Step 2: Stage Files for Commit

EXECUTE: Stage all relevant files.

**Stale Lock Pre-Flight (run before every `git add`):** If `.git/index.lock` is present, follow the Lock File Recovery procedure in `.claude/skills/spec-driven-dev/references/git-workflow-conventions.md` (§ Lock File Recovery, lines 266-295). Summary:
1. `ps aux | grep -v grep | grep git` — if any live git process found: **HALT** with message "A live git process holds `.git/index.lock` — wait for it to finish before re-running Phase 08."
2. If no live process (stale lock): `rm -f .git/index.lock` and log a warning:
   ```bash
   echo "$(date -Iseconds) WARN: stale .git/index.lock cleared before Phase 08 git add" >> devforgeai/logs/git-operations.log
   ```
3. Proceed to `git add`.
VERIFY: `.git/index.lock` absent before the first `git add`.

```bash
git add ${STORY_FILE}
git add ${IMPL_FILES}    # Implementation files created/modified
git add ${TEST_FILES}    # Test files from Phase 02
```
VERIFY: Files staged successfully.
```bash
git status --porcelain
# Verify expected files appear with 'A' or 'M' status
```

### Step 3: Create Git Commit

EXECUTE: Create commit with conventional commit format.
```bash
git commit -m "feat(${STORY_ID}): ${STORY_TITLE}

- Implemented ${FEATURE_DESCRIPTION}
- Tests passing (${PASS_COUNT}/${TOTAL_COUNT})
- Coverage: ${COVERAGE}%

Refs: ${STORY_ID}"
```
**Commit types:** feat, fix, refactor, test, docs
VERIFY: Commit succeeds (exit code 0).
```
IF exit code != 0:
  # Pre-commit hook blocked. `--no-verify` is hook-blocked by `pre-commit-no-verify-guard.sh` (exit 2).
  Read(file_path=".claude/rules/workflow/commit-failure-recovery.md")
  # Follow recovery workflow.
```

### Step 4: Verify Commit Success

EXECUTE: Confirm the commit was created.
```bash
git log -1 --format="%H %s"
```
VERIFY: Output shows new commit hash and message matching the story.
```
IF no new commit: HALT — "Git commit did not succeed."
```

### Step 4.5: Push branch + open PR [CONDITIONAL: branch field set in story front-matter]

EXECUTE: Read `branch` and `pr_base` from story front-matter.
- If `branch` is null → SKIP (no worktree branch set; legacy path or #725 not yet applied).
- If `pr_base` is null → AskUserQuestion: "No sprint branch set in pr_base. Push PR to 'main' or enter the sprint branch name?" Resolve `pr_base` from the story's `sprint` front-matter field (`sprint/<slug>`) if non-empty/non-Backlog; else use the user's response.

```bash
git push -u origin story/${STORY_ID}
```
```bash
gh pr create --base ${pr_base} --head story/${STORY_ID} --title "feat(${STORY_ID}): ${STORY_TITLE}" --body-file tmp/${STORY_ID}/pr-body.md
```
VERIFY: `gh pr view --json number,url` returns non-empty `number` and `url` fields.
Write `pr_number` and `pr_url` to story front-matter:
```bash
devforgeai-validate update-story-frontmatter ${STORY_FILE} --field pr_number --value ${pr_number} --project-root=${PROJECT_ROOT}
devforgeai-validate update-story-frontmatter ${STORY_FILE} --field pr_url --value ${pr_url} --project-root=${PROJECT_ROOT}
```

### Step 5: Update AC Checklist (Deployment Items) [CONDITIONAL: ac_checklist_updates_enabled]

CONDITIONAL: If `ac_checklist_updates_enabled` is false, SKIP this step. Rely on Phase 07 DoD tracking instead. Default: true.

EXECUTE: Mark git/deployment-related acceptance criteria as completed.
```bash
devforgeai-validate update-ac-checklist --story-file=${STORY_FILE} --category=deployment
```
VERIFY: Exit code 0 = items updated. Command displays progress summary.

### Step 6: Capture Observations

EXECUTE: Write observation file for this phase via CLI.
```bash
devforgeai-validate write-observation --story=${STORY_ID} --phase=08 --observations='${OBS_JSON}' --project-root=${PROJECT_ROOT}
```
OBS_JSON must be a JSON array. Each object requires 7 fields: `id` (obs-STORY-NNN-08-001), `phase` (08), `source` (agent name), `category` (friction|success|pattern|gap|idea|bug), `note` (description), `severity` (low|medium|high), `timestamp` (ISO 8601).
VERIFY: Exit code 0 = observation file written. Non-blocking on failure.

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=08 --checkpoint-passed
# Exit 0: proceed to Phase 09 | Exit 1: commit failed
```
