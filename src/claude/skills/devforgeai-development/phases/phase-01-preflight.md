# Phase 01: Pre-Flight Validation

**Entry Gate:**
```bash
devforgeai-validate phase-init ${STORY_ID} --project-root=.

Examples:
 - Correct: devforgeai-validate phase-init ${STORY_ID} --project-root=.
 - Incorrrect: python -m devforgeai.cli.devforgeai_validate phase-init ${STORY_ID} --project-root=.
# Exit code 0: State file created, proceed
# Exit code 1: State file exists (resume scenario)
# Exit code 2: Invalid story ID - HALT
```

---

## Phase Workflow

**Purpose:** 11-step validation before TDD begins

**Required Subagents:**
- git-validator (Git availability check)
- tech-stack-detector (Technology detection)

**Steps:**

1. **Validate Git status** (git-validator subagent)
   ```
   Task(
     subagent_type="git-validator",
     description="Validate Git repository status",
     prompt="Check Git availability and repository status for workflow strategy"
   )
   ```

1.5. **User consent for git operations** (if uncommitted changes >10)
   - Use AskUserQuestion if uncommitted changes detected
   - Option: Stash, Continue, Abort

1.6. **Stash warning and confirmation** (if user chooses to stash)

1.7. **Check for existing plan file**
   ```
   Glob(".claude/plans/*.md")
   Grep(pattern="${STORY_ID}", path="{plan_file}")
   ```
   - If match found, offer to resume via AskUserQuestion

2. **Git Worktree Auto-Management** (git-worktree-manager subagent)
   ```
   Task(
     subagent_type="git-worktree-manager",
     description="Manage Git worktree for ${STORY_ID}",
     prompt="Create/manage worktree for parallel development"
   )
   ```

3. **Adapt workflow** (Git vs file-based)

4. **File-based tracking setup** (if no Git)

5. **Validate 6 context files exist**
   ```
   Read(file_path="devforgeai/specs/context/tech-stack.md")
   Read(file_path="devforgeai/specs/context/source-tree.md")
   Read(file_path="devforgeai/specs/context/dependencies.md")
   Read(file_path="devforgeai/specs/context/coding-standards.md")
   Read(file_path="devforgeai/specs/context/architecture-constraints.md")
   Read(file_path="devforgeai/specs/context/anti-patterns.md")
   ```

6. **Load story specification**
   ```
   Read(file_path="${STORY_FILE}")
   ```

7. **Validate spec vs context conflicts**

8. **Detect tech stack** (tech-stack-detector subagent)
   ```
   Task(
     subagent_type="tech-stack-detector",
     description="Detect technology stack for ${STORY_ID}",
     prompt="Auto-detect project technologies, validate against tech-stack.md"
   )
   ```

9. **Detect QA failures** (recovery mode check)

9.5. **Load structured gap data** (if gaps.json exists)
   ```
   IF Glob("tests/results/${STORY_ID}/gaps.json"):
     Read(file_path="tests/results/${STORY_ID}/gaps.json")
     SET $REMEDIATION_MODE = true
   ```

**Reference:** `references/preflight-validation.md` for complete workflow

---

## Validation Checkpoint

**Before proceeding to Phase 02, verify:**

- [ ] git-validator subagent invoked
- [ ] Context files validated (6 files)
- [ ] Story specification loaded
- [ ] tech-stack-detector subagent invoked

**IF any checkbox UNCHECKED:** HALT workflow

---

**Exit Gate:**
```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=01 --checkpoint-passed
# Exit code 0: Phase complete, proceed to Phase 02
# Exit code 1: Cannot complete - validation failed
```

---

**Record Subagents:**
```bash
# Record after each subagent invocation:
# (Called automatically by orchestrator)
# devforgeai-validate phase-record ${STORY_ID} --phase=01 --subagent=git-validator
# devforgeai-validate phase-record ${STORY_ID} --phase=01 --subagent=tech-stack-detector
```
