# Phase 05: Integration & Validation

**Entry Gate:**
```bash
devforgeai-validate phase-check ${STORY_ID} --from=4.5 --to=05

Examples (--project-root applies to phase-* commands only, not check-hooks/invoke-hooks):
 - Correct: devforgeai-validate phase-init ${STORY_ID} --project-root=.
 - Incorrect: python -m devforgeai.cli.devforgeai_validate phase-init ${STORY_ID} --project-root=.
# Exit code 0: Transition allowed
# Exit code 1: Phase 4.5 not complete - HALT
# Exit code 2: Missing subagents from Phase 4.5 - HALT
```

---

## Mandatory Steps

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

     **Response Constraints:**
     - Limit response to 500 words maximum
     - Use bullet points, not paragraphs
     - Only include actionable findings
     - No code snippets unless essential
     """
   )
   ```

1.5. **Diagnostic Hook: Diagnostic-Analyst on Integration Test Failure** (STORY-496)
   ```
   # BR-001: Only fires on failure path (zero overhead on success)
   IF integration tests fail AND NOT diagnosis_invoked:
       # BR-002: Single-invocation guard - once per phase cycle
       SET diagnosis_invoked = true

       Display: "Integration tests failed - invoking diagnostic-analyst"

       # BR-003: Graceful skip when diagnostic-analyst subagent unavailable
       TRY:
           Task(
             subagent_type="diagnostic-analyst",
             description="Diagnose integration test failure for ${STORY_ID}",
             prompt="""
             Investigate integration test failure.

             Story: ${STORY_ID}
             Phase: 05 (Integration)
             Integration test failure output: ${INTEGRATION_TEST_OUTPUT}
             Implementation files: ${IMPL_FILES}

             Analyze failure against context files and provide root cause diagnosis.
             """
           )
           # AC#2: Integration failure invokes diagnostic-analyst with test output (not empty/generic)
           # AC#5: Failure context includes specific data (integration_test_output, story_id, impl_files)
           SET retry_context = diagnosis_output
       CATCH:
           Display: "⚠️ diagnostic-analyst unavailable - proceeding without diagnosis"
           # Graceful degradation - continue with normal failure handling

   ELIF integration tests fail AND diagnosis_invoked:
       Display: "Integration tests still failing after diagnosis - escalating"
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
    Read(file_path="references/integration-testing.md")

---

## Validation Checkpoint

**Before proceeding to Phase 06, verify:**

- [ ] Anti-gaming validation PASSED
- [ ] integration-tester subagent invoked (check for Task() call in conversation)
- [ ] Coverage thresholds validated (95%/85%/80%)
- [ ] AC Checklist (integration items) updated ([ ] → [x])

### AC Checklist Update Verification (RCA-003)

After Step 3 completes, verify AC Checklist was actually updated:
```
Grep(pattern="- \\[x\\].*[Ii]ntegration", path="${STORY_FILE}")
# Should find checked integration-related items
# If no matches found: AC Checklist update was skipped - HALT
```

**IF Anti-Gaming validation FAILED:**
- HALT immediately
- Test gaming detected, coverage scores INVALID
- Fix: Remove skip decorators, add assertions, reduce mocking

**IF any other checkbox UNCHECKED:** HALT workflow

### Subagent Invocation Verification

FOR required_subagent in [integration-tester]:
  IF conversation contains Task(subagent_type="{required_subagent}"):
    mark_verified(required_subagent)
  ELSE:
    add_to_missing(required_subagent)

IF any check fails:
  Display: "Phase 05 incomplete: {missing items}"
  HALT (do not proceed to Phase 06)
  Prompt: "Complete missing items before proceeding"

IF all checks pass:
  Display: "Phase 05 validation passed - all mandatory steps completed"
  Proceed to Phase 06

---

## Pre-Exit Checklist

**Before calling `phase-complete`, verify ALL items:**

- [ ] Anti-gaming validation passed
- [ ] integration-tester subagent invoked
- [ ] Coverage thresholds validated (95%/85%/80%)
- [ ] AC checklist updated (integration items)
- [ ] Observation capture executed

**IF any item UNCHECKED and no N/A justification:** HALT — do not call exit gate.

---

## Optional Captures

### Observation Capture (EPIC-051)

Before exiting this phase, capture observations from subagent outputs:

1. **Collect Explicit Observations:**
   IF integration-tester returned `observations[]` in output:
   - Extract each observation object
   - Set source: "explicit"

   IF ac-compliance-verifier returned `observations[]` in output:
   - Extract each observation object
   - Set source: "explicit"

2. **Invoke Observation Extractor:**
   ```
   Task(subagent_type="observation-extractor",
        description="Extract observations from Phase 05 subagent outputs",
        prompt="Extract implicit observations from integration-tester and ac-compliance-verifier outputs including integration test results, coverage gaps, and AC compliance issues.")
   ```
   - Set source: "extracted" for returned observations

3. **Append to Phase State:**
   FOR each observation (explicit OR extracted):
   - Generate ID: "OBS-05-{timestamp}" (ISO8601 milliseconds)
   - Set fields: id, phase ("05"), category, note, severity, files[], source, timestamp
   - Append to phase-state.json observations[] array
   - Ensure no duplicate observations (skip if same finding in explicit and extracted)

**Error Handling:** If observation capture fails, log warning and continue phase completion (non-blocking per BR-001).

### Session Memory Update (STORY-341)

Before exiting this phase, append observations to the session memory file:

```
# Append Phase 05 observations to session memory
session_path = ".claude/memory/sessions/${STORY_ID}-session.md"

Edit(
  file_path=session_path,
  old_string="## Observations",
  new_string="## Observations\n\n### Phase 05 (Integration)\n${OBSERVATIONS_LIST}"
)

# Update last_updated timestamp
Edit(
  file_path=session_path,
  old_string="last_updated: ${OLD_TIMESTAMP}",
  new_string="last_updated: ${CURRENT_TIMESTAMP}"
)
```

**Reference:** EPIC-052 Session Memory Layer specification

---

## Exit Gate
```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=05 --checkpoint-passed
# Exit code 0: Phase complete, proceed to Phase 5.5
# Exit code 1: Cannot complete - coverage thresholds not met
```
