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

---

## Mandatory Steps

### Step 1: Budget Enforcement Check

EXECUTE: Check deferral budget for this story.
```
Read(file_path=".claude/skills/implementing-stories/references/deferral-budget-enforcement.md")
# Parse budget limits, check against deferred items from Phase 06
```
VERIFY: Budget within limits.
```
IF budget exceeded: HALT — "Deferral budget exceeded."
IF new incomplete items detected: Return to Phase 06.
```

### Step 2: Stage Files for Commit

EXECUTE: Stage all relevant files.
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
  # Pre-commit hook may have blocked — read error output
  # Common: DoD validation failure → See .claude/rules/workflow/commit-failure-recovery.md
  Read(file_path=".claude/rules/workflow/commit-failure-recovery.md")
  # Follow recovery workflow. NEVER use --no-verify.
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

### Step 5: Update AC Checklist (Deployment Items)

EXECUTE: Mark git/deployment-related acceptance criteria as completed.
```
Edit(file_path="${STORY_FILE}", old_string="- [ ] <git item>", new_string="- [x] <git item>")
```
VERIFY: Grep confirms git items are checked.
```
Grep(pattern="- \\[x\\].*[Gg]it|[Cc]ommit|[Dd]eploy", path="${STORY_FILE}")
```

### Step 6: Capture Observations

EXECUTE: Write observation file for this phase.
```
Write(file_path="devforgeai/feedback/ai-analysis/${STORY_ID}/phase-08-observations.json",
  content=<JSON with phase, category, note, files, severity>)
```
VERIFY: Observation file exists.
```
Glob(pattern="devforgeai/feedback/ai-analysis/${STORY_ID}/phase-08-observations.json")
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=08 --checkpoint-passed
# Exit 0: proceed to Phase 09 | Exit 1: commit failed
```
