# Git Validator - Additional Invocation Examples

Reference examples showing git-validator invocation from different parent skills.

---

## Examples

### Example 1: Git Validator Invocation from spec-driven-dev

**Scenario:** spec-driven-dev skill needs to determine workflow mode before proceeding

```
Task(
  subagent_type="git-validator",
  description="Validate Git repository status at project start",
  prompt="Validate the Git repository status and provide workflow strategy.

  Determine:
  1. Is Git installed and accessible?
  2. Is this a Git repository?
  3. How many commits exist?
  4. What is the current branch?
  5. Are there uncommitted changes?

  Categorize any uncommitted files to help the user understand what would be affected by stash/reset operations. Highlight story files if present.

  Return a JSON object with:
  - git_status: Installation, repo initialization, commit count, current branch, changes
  - file_analysis: Count and categorization of uncommitted files
  - assessment: Status (READY/UNCOMMITTED/INIT_REQUIRED/NOT_INITIALIZED/GIT_MISSING), workflow mode (full/partial/fallback), can_commit/can_push flags
  - recommendations: Primary action, specific commands, fallback strategy

  CRITICAL: Always provide a fallback workflow strategy. DevForgeAI must not fail due to missing Git."
)
```

**Expected Response:** Valid JSON with git_status, assessment.status = "READY", workflow_mode = "full" (if Git available and repo initialized)

---

### Example 2: Git Validator Invocation from spec-driven-release (Pre-Deployment Check)

**Scenario:** Before releasing/deploying, verify repository is in clean state

```
Task(
  subagent_type="git-validator",
  description="Verify clean Git state before deployment",
  prompt="Perform a pre-deployment Git validation.

  Validate:
  1. Git is installed
  2. Repository is initialized with commits
  3. No uncommitted changes (working directory clean)
  4. Not in detached HEAD state
  5. On a main release branch (if applicable)

  Return JSON with assessment status and explicit can_push flag.

  If uncommitted changes detected, include detailed file breakdown in file_analysis to show what would need to be committed.

  CRITICAL: Deployment should not proceed if assessment.can_commit = false or uncommitted_changes > 0."
)
```

**Expected Response:** Valid JSON with assessment.status = "READY", can_commit = true, can_push = true, uncommitted_changes = 0
