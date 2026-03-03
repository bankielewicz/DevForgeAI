# Phase 02: Test-First Design (TDD Red)

---

## Memory Context

**Purpose:** Surface relevant TDD patterns from long-term memory before writing tests.

**Step 0.1: Load TDD Patterns from Long-Term Memory**
```
result = Glob(pattern=".claude/memory/learning/tdd-patterns.md")
IF result is not empty:
    Read(file_path=".claude/memory/learning/tdd-patterns.md")
ELSE:
    Display: "No TDD patterns in long-term memory yet. Proceeding without memory context."
```

**Step 0.2: Pattern Matching**
```
FOR each pattern in tdd_patterns:
  # Only surface confident patterns (confidence >= low, i.e., 3+ occurrences)
  IF pattern.confidence != "emerging" AND pattern.occurrences >= 3:
    # Match story keywords against pattern triggers
    IF keyword_match(story.acceptance_criteria, pattern.when_to_apply):
      matched_patterns.append(pattern)

# Limit to top 3 most relevant patterns
surfaced_patterns = matched_patterns[:3]
```

**Step 0.3: Display Relevant Patterns (if any)**
```
IF surfaced_patterns:
  Display:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Relevant TDD Patterns (from long-term memory)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pattern: {pattern_name} ({occurrences} occurrences, {confidence} confidence)
  → This story involves {story_context}
  → Recommendation: {when_to_apply}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Reference:** EPIC-052 Memory Surfacing specification

---

**Entry Gate:**
```bash
devforgeai-validate phase-check ${STORY_ID} --from=01 --to=02

Examples (--project-root applies to phase-* commands only, not check-hooks/invoke-hooks):
 - Correct: devforgeai-validate phase-init ${STORY_ID} --project-root=.
 - Incorrect: python -m devforgeai.cli.devforgeai_validate phase-init ${STORY_ID} --project-root=.
# Exit code 0: Transition allowed
# Exit code 1: Phase 01 not complete - HALT
# Exit code 2: Missing subagents from Phase 01 - HALT
```

---

## Mandatory Steps

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

     **Response Constraints:**
     - Limit response to 500 words maximum
     - Use bullet points, not paragraphs
     - Only include actionable findings
     - No code snippets unless essential
     """
   )
   ```

1.5. **Distinguish Test Output Based on Implementation Type**
   ```
   # Determine output type based on story implementation
   IF story modifies Slash Command (.md files):
       output_type = "Test Specification Document"
       Display: "Test Specification Generated for Slash Command"
       # Note: Specification validates structure, not executable

   ELIF story modifies Code (Python/JS/C#/etc):
       output_type = "Executable unit tests"
       Display: "Executable Tests Generated for Code implementation"
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
    Read(file_path="references/tdd-red-phase.md")

### Test Integrity Snapshot [MANDATORY] (STORY-502)

After tests verified RED, create test integrity snapshot:
```
Read(file_path="references/test-integrity-snapshot.md")
```
Execute snapshot creation per the reference.

### Snapshot File Existence Verification [MANDATORY] (STORY-514)

After snapshot creation, verify the file was actually written to disk:
```
Glob(pattern="devforgeai/qa/snapshots/${STORY_ID}/red-phase-checksums.json")
IF not found: HALT "Snapshot file not created — cannot complete Phase 02"
```

**Note:** `${STORY_ID}` is a runtime template variable — do NOT replace it with an actual story ID.

### AC Checklist Update Verification [MANDATORY] (RCA-003)

After Step 5 completes, verify AC Checklist was actually updated:
```
Grep(pattern="- \\[x\\].*test", path="${STORY_FILE}")
# Should find checked test-related items
# If no matches found: AC Checklist update was skipped - HALT
```

---

## Validation Checkpoint

**Before proceeding to Phase 03, verify:**

- [ ] test-automator subagent invoked
- [ ] Tech Spec Coverage Validation completed
- [ ] AC Checklist (test items) updated ([ ] → [x])
- [ ] Test integrity snapshot created (STORY-502)

**IF any checkbox UNCHECKED:** HALT workflow

---

## Pre-Exit Checklist

**Before calling `phase-complete`, verify ALL items:**

- [ ] Memory context loaded (TDD patterns)
- [ ] test-automator invoked
- [ ] RED state verified (all tests fail)
- [ ] Test integrity snapshot created
- [ ] Snapshot verified via Glob
- [ ] AC checklist updated (test items)
- [ ] Observation capture executed

**IF any item UNCHECKED and no N/A justification:** HALT — do not call exit gate.

---

## Optional Captures

### Observation Capture (EPIC-051)

Before exiting this phase, capture observations from subagent outputs:

1. **Collect Explicit Observations:**
   IF test-automator returned `observations[]` in output:
   - Extract each observation object
   - Set source: "explicit"

2. **Invoke Observation Extractor:**
   ```
   Task(subagent_type="observation-extractor",
        description="Extract observations from Phase 02 subagent outputs",
        prompt="Extract implicit observations from test-automator output including coverage gaps, test patterns, and potential issues.")
   ```
   - Set source: "extracted" for returned observations

3. **Append to Phase State:**
   FOR each observation (explicit OR extracted):
   - Generate ID: "OBS-02-{timestamp}" (ISO8601 milliseconds)
   - Set fields: id, phase ("02"), category, note, severity, files[], source, timestamp
   - Append to phase-state.json observations[] array
   - Ensure no duplicate observations (skip if same finding in explicit and extracted)

**Error Handling:** If observation capture fails, log warning and continue phase completion (non-blocking per BR-001).

### Session Memory Update (STORY-341)

Before exiting this phase, append observations to the session memory file:

```
# Append Phase 02 observations to session memory
session_path = ".claude/memory/sessions/${STORY_ID}-session.md"

Edit(
  file_path=session_path,
  old_string="## Observations\n\n(Observations from phases 02-08 will be appended here)",
  new_string="## Observations\n\n### Phase 02 (Test-First)\n${OBSERVATIONS_LIST}\n"
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
  "id": "obs-02-{seq}",
  "phase": "02",
  "category": "{friction|success|pattern|gap|idea|bug}",
  "note": "{1-2 sentence description}",
  "files": ["{relevant files}"],
  "severity": "{low|medium|high}"
}
```

**Reference:** `references/observation-capture.md`
    Read(file_path="references/observation-capture.md")

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=02 --checkpoint-passed
# Exit code 0: Phase complete, proceed to Phase 03
# Exit code 1: Cannot complete - tests not in RED state
```
