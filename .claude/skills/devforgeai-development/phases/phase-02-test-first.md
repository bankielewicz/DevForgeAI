# Phase 02: Test-First Design (TDD Red)

**Entry Gate:**
```bash
devforgeai-validate phase-check ${STORY_ID} --from=01 --to=02
# Exit code 0: Transition allowed
# Exit code 1: Phase 01 not complete - HALT
# Exit code 2: Missing subagents from Phase 01 - HALT
```

---

## Phase Workflow

**Purpose:** Write failing tests from acceptance criteria

**Required Subagents:**
- test-automator (Test generation)

**Steps:**

1. **Generate failing tests from AC**
   ```
   Task(
     subagent_type="test-automator",
     description="Generate failing tests for ${STORY_ID}",
     prompt="""
     Generate failing tests from acceptance criteria.

     Story: ${STORY_FILE}

     Requirements:
     1. Read story file acceptance criteria
     2. Generate tests that will FAIL initially
     3. Follow test naming: test_<function>_<scenario>_<expected>
     4. Use project's test framework (from tech-stack.md)
     5. Return test files and run command
     """
   )
   ```

2. **Run tests - verify RED state**
   ```bash
   # Run generated tests
   ${TEST_COMMAND}
   # Expected: All tests FAIL (red phase)
   ```

3. **Verify tests fail for expected reasons**
   - Not import errors
   - Not configuration errors
   - Failures are business logic (expected)

4. **Tech Spec Coverage Validation**
   - Verify all technical spec sections have tests
   - User approval if gaps detected

5. **Update AC Checklist (test items)**
   ```
   Edit(
     file_path="${STORY_FILE}",
     old_string="- [ ] Test item",
     new_string="- [x] Test item"
   )
   ```

**Reference:** `references/tdd-red-phase.md` for complete workflow

---

## Validation Checkpoint

**Before proceeding to Phase 03, verify:**

- [ ] test-automator subagent invoked
- [ ] Tech Spec Coverage Validation completed
- [ ] AC Checklist (test items) updated

**IF any checkbox UNCHECKED:** HALT workflow

---

**Exit Gate:**
```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=02 --checkpoint-passed
# Exit code 0: Phase complete, proceed to Phase 03
# Exit code 1: Cannot complete - tests not in RED state
```
