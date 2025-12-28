# Phase 04: Refactoring

**Entry Gate:**
```bash
devforgeai-validate phase-check ${STORY_ID} --from=03 --to=04

Examples:
 - Correct: devforgeai-validate phase-init ${STORY_ID} --project-root=.
 - Incorrrect: python -m devforgeai.cli.devforgeai_validate phase-init ${STORY_ID} --project-root=.
# Exit code 0: Transition allowed
# Exit code 1: Phase 03 not complete - HALT
# Exit code 2: Missing subagents from Phase 03 - HALT
```

---

## Phase Workflow

**Purpose:** Improve quality while keeping tests green

**Required Subagents:**
- refactoring-specialist (Code improvement)
- code-reviewer (Quality review)

**Steps:**

1. **Invoke refactoring specialist**
   ```
   Task(
     subagent_type="refactoring-specialist",
     description="Refactor implementation for ${STORY_ID}",
     prompt="""
     Improve code quality while maintaining test success.

     Story: ${STORY_FILE}
     Implementation files: ${IMPL_FILES}

     Requirements:
     1. Reduce cyclomatic complexity if > 10
     2. Extract reusable methods
     3. Improve naming consistency
     4. Apply DRY principle
     5. Ensure all tests still pass after changes
     """
   )
   ```

2. **Verify tests still GREEN**
   ```bash
   ${TEST_COMMAND}
   # Expected: All tests still PASS
   ```

3. **Invoke code reviewer**
   ```
   Task(
     subagent_type="code-reviewer",
     description="Review code for ${STORY_ID}",
     prompt="""
     Review implementation quality and security.

     Files: ${IMPL_FILES}

     Check:
     1. Code quality and maintainability
     2. Security vulnerabilities
     3. Pattern compliance
     4. Standards adherence
     """
   )
   ```

4. **Anti-Gaming Validation** [NEW - BLOCKING]
   - Check for skip decorators
   - Check for empty tests
   - Check for excessive mocking (>2x assertions)
   - HALT if gaming patterns detected

5. **Light QA validation** [MANDATORY]
   ```
   Skill(command="qa --mode=light --story=${STORY_ID}")
   ```

6. **Update AC Checklist (quality items)**
   ```
   Edit(
     file_path="${STORY_FILE}",
     old_string="- [ ] Quality item",
     new_string="- [x] Quality item"
   )
   ```

**Reference:** `references/tdd-refactor-phase.md` for complete workflow

---

## Validation Checkpoint

**Before proceeding to Phase 05, verify:**

- [ ] refactoring-specialist invoked
- [ ] code-reviewer invoked
- [ ] Anti-gaming validation passed
- [ ] Light QA validation passed
- [ ] AC Checklist (quality items) updated

**IF any checkbox UNCHECKED:** HALT workflow

---

**Exit Gate:**
```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=04 --checkpoint-passed
# Exit code 0: Phase complete, proceed to Phase 05
# Exit code 1: Cannot complete - quality issues detected
```
