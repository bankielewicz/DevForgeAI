# Phase 03: Implementation (TDD Green)

---

## Friction Awareness

**Purpose:** Surface relevant friction warnings from long-term memory before implementing.

**Step 0.1: Load Friction Catalog from Long-Term Memory**
```
result = Glob(pattern=".claude/memory/learning/friction-catalog.md")
IF result is not empty:
    Read(file_path=".claude/memory/learning/friction-catalog.md")
ELSE:
    Display: "No friction patterns in long-term memory yet. Proceeding without friction context."
```

**Step 0.2: Friction Matching**
```
FOR each friction in friction_catalog:
  # Only surface confident frictions (confidence >= low, i.e., 3+ occurrences)
  IF friction.confidence != "emerging" AND friction.occurrences >= 3:
    # Match story characteristics against friction triggers
    IF keyword_match(story.technical_specification, friction.root_cause):
      matched_frictions.append(friction)

# Limit to top 3 most relevant frictions
surfaced_frictions = matched_frictions[:3]
```

**Step 0.3: Display Friction Warnings (if any)**
```
IF surfaced_frictions:
  Display:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Friction Warning (from long-term memory)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Friction: {friction_id} ({occurrences} occurrences)
  → {root_cause}
  → Prevention: {solution}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Reference:** EPIC-052 Memory Surfacing specification

---

**Entry Gate:**
```bash
devforgeai-validate phase-check ${STORY_ID} --from=02 --to=03

Examples (--project-root applies to phase-* commands only, not check-hooks/invoke-hooks):
 - Correct: devforgeai-validate phase-init ${STORY_ID} --project-root=.
 - Incorrect: python -m devforgeai.cli.devforgeai_validate phase-init ${STORY_ID} --project-root=.
# Exit code 0: Transition allowed
# Exit code 1: Phase 02 not complete - HALT
# Exit code 2: Missing subagents from Phase 02 - HALT
```

---

## Mandatory Steps

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

     **Response Constraints:**
     - Limit response to 500 words maximum
     - Use bullet points, not paragraphs
     - Only include actionable findings
     - No code snippets unless essential
     """
   )
   ```

3. **Run tests - verify GREEN state**
   ```bash
   ${TEST_COMMAND}
   # Expected: All tests PASS (green phase)
   ```

3.5. **Diagnostic Hook: Root-Cause Diagnosis on Test Failure** (STORY-496)
   ```
   # BR-001: Only fires on failure path (zero overhead on success)
   IF tests fail (exit code != 0) AND NOT diagnosis_invoked:
       # BR-002: Single-invocation guard - maximum one diagnosis per phase cycle
       SET diagnosis_invoked = true

       Display: "Tests failed - invoking root-cause-diagnosis before retry"

       Skill("root-cause-diagnosis", args="--story=${STORY_ID} --phase=03 --test_output=${TEST_OUTPUT} --files=${IMPL_FILES}")
       # AC#1: Test failure invokes root-cause-diagnosis before retrying backend-architect
       # AC#5: Failure context includes specific data (test_output, story_id, file_paths)

       # Attach diagnosis to retry context for backend-architect
       SET retry_context = diagnosis_output

       # BR-003: Graceful degradation if skill unavailable
       IF skill invocation fails:
           Display: "⚠️ root-cause-diagnosis unavailable - proceeding with standard retry"
           # Continue with normal failure handling

   ELIF tests fail AND diagnosis_invoked:
       # Already diagnosed this cycle - escalate via existing path
       Display: "Tests still failing after diagnosis-informed retry - escalating"
   ```

4. **Validate context constraints**
   ```
   Task(
     subagent_type="context-validator",
     description="Validate constraints for ${STORY_ID}",
     prompt="""
     Validate implementation against all 6 context files.

     **Response Constraints:**
     - Limit response to 500 words maximum
     - Use bullet points, not paragraphs
     - Only include actionable findings
     - No code snippets unless essential
     """
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
    Read(file_path="references/tdd-green-phase.md")

### AC Checklist Update Verification (RCA-003)

After Step 5 completes, verify AC Checklist was actually updated:
```
Grep(pattern="- \\[x\\].*[Ii]mplementation", path="${STORY_FILE}")
# Should find checked implementation-related items
# If no matches found: AC Checklist update was skipped - HALT
```

### Subagent Invocation Verification

FOR required_subagent in [backend-architect OR frontend-developer, context-validator]:
  IF conversation contains Task(subagent_type="{required_subagent}"):
    mark_verified(required_subagent)
  ELSE:
    add_to_missing(required_subagent)

IF any check fails:
  Display: "Phase 03 incomplete: {missing items}"
  HALT (do not proceed to Phase 04)
  Prompt: "Complete missing items before proceeding"

IF all checks pass:
  Display: "Phase 03 validation passed - all mandatory steps completed"
  Proceed to Phase 04

---

## Validation Checkpoint

**Before proceeding to Phase 04, verify:**

- [ ] backend-architect OR frontend-developer invoked (check for Task() call in conversation)
- [ ] All tests GREEN (passing)
- [ ] context-validator invoked (check for Task() call in conversation)
- [ ] AC Checklist (implementation items) updated ([ ] → [x])

**IF any checkbox UNCHECKED:** HALT workflow

---

## Pre-Exit Checklist

**Before calling `phase-complete`, verify ALL items:**

- [ ] Friction awareness loaded (friction catalog)
- [ ] backend-architect OR frontend-developer subagent invoked
- [ ] All tests GREEN (passing)
- [ ] context-validator subagent invoked
- [ ] AC checklist updated (implementation items)
- [ ] Observation capture executed

**IF any item UNCHECKED and no N/A justification:** HALT — do not call exit gate.

---

## Optional Captures

### Observation Capture (EPIC-051)

Before exiting this phase:

1. **Collect Explicit Observations:**
   IF any subagent returned `observations[]` in output:
   - Extract each observation object
   - Set source: "explicit"

2. **Invoke Observation Extractor:**
   ```
   Task(subagent_type="observation-extractor",
        prompt="Extract observations from Phase 03 backend-architect and code-reviewer outputs",
        context="{subagent_outputs}")
   ```
   - Set source: "extracted" for returned observations

3. **Append to Phase State:**
   FOR each observation:
   - Generate ID: "OBS-03-{timestamp}" (ISO8601 milliseconds)
   - Append to phase-state.json observations[]

4. **Error Handling:**
   If observation capture fails, log warning and continue phase completion (non-blocking per BR-001).

### Session Memory Update (STORY-341)

Before exiting this phase, append observations to the session memory file:

```
# Append Phase 03 observations to session memory
session_path = ".claude/memory/sessions/${STORY_ID}-session.md"

Edit(
  file_path=session_path,
  old_string="## Observations",
  new_string="## Observations\n\n### Phase 03 (Implementation)\n${OBSERVATIONS_LIST}"
)

# Update last_updated timestamp
Edit(
  file_path=session_path,
  old_string="last_updated: ${OLD_TIMESTAMP}",
  new_string="last_updated: ${CURRENT_TIMESTAMP}"
)
```

**Reference:** EPIC-052 Session Memory Layer specification

### Reflection

**Before exiting this phase, reflect:**
1. Did I encounter any friction? (unclear docs, missing tools, workarounds)
2. Did anything work particularly well? (constraints that helped, patterns that fit)
3. Did I notice any repeated patterns?
4. Are there gaps in tooling/docs?
5. Did I discover any bugs?

**If YES to any:** Append to phase-state.json `observations` array:
```json
{
  "id": "obs-03-{seq}",
  "phase": "03",
  "category": "{friction|success|pattern|gap|idea|bug}",
  "note": "{1-2 sentence description}",
  "files": ["{relevant files}"],
  "severity": "{low|medium|high}"
}
```

**Reference:** `references/observation-capture.md`
    Read(file_path="references/observation-capture.md")

### Phase Completion Display

**Before marking Phase 03 complete, display:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 03/10: Implementation - Mandatory Steps Completed
  TDD Iteration: X/5 | Observations: N captured
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ backend-architect invoked (lines XXX-YYY)
✓ context-validator invoked (lines XXX-YYY)
✓ AC Checklist items updated (implementation items)
✓ All tests GREEN (passing)

All Phase 03 mandatory steps completed. Proceeding to Phase 04...
```

**Iteration counter display:**
- IF iteration_count >= 4: Display "TDD Iteration: X/5 ⚠️ Approaching limit"
- IF iteration_count >= max_iterations (5): HALT with "Maximum iterations reached"

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=03 --checkpoint-passed
# Exit code 0: Phase complete, proceed to Phase 04
# Exit code 1: Cannot complete - tests not GREEN
```
