# Phase 05: Integration & Validation

**Entry Gate:**
```bash
devforgeai-validate phase-check ${STORY_ID} --from=04 --to=05

Examples:
 - Correct: devforgeai-validate phase-init ${STORY_ID} --project-root=.
 - Incorrrect: python -m devforgeai.cli.devforgeai_validate phase-init ${STORY_ID} --project-root=.
# Exit code 0: Transition allowed
# Exit code 1: Phase 04 not complete - HALT
# Exit code 2: Missing subagents from Phase 04 - HALT
```

---

## Phase Workflow

**Purpose:** Cross-component testing and coverage validation

**Required Subagents:**
- integration-tester (Integration tests)

**Steps:**

0. **Anti-Gaming Validation** [MANDATORY - RUN FIRST]
   - Check for skip decorators
   - Check for assertion-less tests
   - Check for excessive mocking
   - HALT if gaming patterns detected (coverage scores would be invalid)

1. **Invoke integration tester**
   ```
   Task(
     subagent_type="integration-tester",
     description="Run integration tests for ${STORY_ID}",
     prompt="""
     Validate cross-component interactions.

     Story: ${STORY_FILE}
     Implementation: ${IMPL_FILES}

     Requirements:
     1. Test API contracts if applicable
     2. Test database transactions if applicable
     3. Test message flows if applicable
     4. Verify coverage thresholds met
        - Business logic: 95%
        - Application layer: 85%
        - Infrastructure: 80%
     """
   )
   ```

2. **Validate coverage thresholds**
   ```bash
   # Run coverage analysis
   ${COVERAGE_COMMAND}
   # Verify: 95%/85%/80% thresholds met
   ```

3. **Update AC Checklist (integration items)**
   ```
   Edit(
     file_path="${STORY_FILE}",
     old_string="- [ ] Integration item",
     new_string="- [x] Integration item"
   )
   ```

**Reference:** `references/integration-testing.md` for complete workflow

---

## Validation Checkpoint

**Before proceeding to Phase 06, verify:**

- [ ] Anti-gaming validation PASSED
- [ ] integration-tester subagent invoked
- [ ] Coverage thresholds validated (95%/85%/80%)
- [ ] AC Checklist (integration items) updated

**IF Anti-Gaming validation FAILED:**
- HALT immediately
- Test gaming detected, coverage scores INVALID
- Fix: Remove skip decorators, add assertions, reduce mocking

**IF any other checkbox UNCHECKED:** HALT workflow

---

**Exit Gate:**
```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=05 --checkpoint-passed
# Exit code 0: Phase complete, proceed to Phase 06
# Exit code 1: Cannot complete - coverage thresholds not met
```
