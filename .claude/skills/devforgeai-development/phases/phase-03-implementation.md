# Phase 03: Implementation (TDD Green)

**Entry Gate:**
```bash
devforgeai-validate phase-check ${STORY_ID} --from=02 --to=03
# Exit code 0: Transition allowed
# Exit code 1: Phase 02 not complete - HALT
# Exit code 2: Missing subagents from Phase 02 - HALT
```

---

## Phase Workflow

**Purpose:** Minimal code to pass tests (Tests GREEN)

**Required Subagents:**
- backend-architect OR frontend-developer (Implementation)
- context-validator (Constraint validation)

**Steps:**

1. **Determine implementation subagent**
   - If backend story → backend-architect
   - If frontend story → frontend-developer
   - If full-stack → invoke both sequentially

2. **Implement minimal code to pass tests**
   ```
   Task(
     subagent_type="backend-architect",  # or frontend-developer
     description="Implement code for ${STORY_ID}",
     prompt="""
     Write minimal implementation to pass tests.

     Story: ${STORY_FILE}
     Test files: ${TEST_FILES}

     Requirements:
     1. Implement ONLY what tests require
     2. Follow tech-stack.md constraints
     3. Follow coding-standards.md patterns
     4. Follow source-tree.md for file placement
     5. No premature optimization
     """
   )
   ```

3. **Run tests - verify GREEN state**
   ```bash
   ${TEST_COMMAND}
   # Expected: All tests PASS (green phase)
   ```

4. **Validate context constraints**
   ```
   Task(
     subagent_type="context-validator",
     description="Validate constraints for ${STORY_ID}",
     prompt="Validate implementation against all 6 context files"
   )
   ```

5. **Update AC Checklist (implementation items)**
   ```
   Edit(
     file_path="${STORY_FILE}",
     old_string="- [ ] Implementation item",
     new_string="- [x] Implementation item"
   )
   ```

**Reference:** `references/tdd-green-phase.md` for complete workflow

---

## Validation Checkpoint

**Before proceeding to Phase 04, verify:**

- [ ] backend-architect OR frontend-developer invoked
- [ ] All tests GREEN (passing)
- [ ] context-validator invoked
- [ ] AC Checklist (implementation items) updated

**IF any checkbox UNCHECKED:** HALT workflow

---

**Exit Gate:**
```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=03 --checkpoint-passed
# Exit code 0: Phase complete, proceed to Phase 04
# Exit code 1: Cannot complete - tests not GREEN
```
