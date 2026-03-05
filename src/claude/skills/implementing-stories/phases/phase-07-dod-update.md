# Phase 07: DoD Update Workflow

**Entry Gate:**
```bash
devforgeai-validate phase-check ${STORY_ID} --from=06 --to=07

Examples (--project-root applies to phase-* commands only, not check-hooks/invoke-hooks):
 - Correct: devforgeai-validate phase-init ${STORY_ID} --project-root=.
 - Incorrect: python -m devforgeai.cli.devforgeai_validate phase-init ${STORY_ID} --project-root=.
# Exit code 0: Transition allowed
# Exit code 1: Phase 06 not complete - HALT
# Exit code 2: Missing subagents from Phase 06 - HALT
```

---

## Progressive Task Disclosure

Read and follow `references/progressive-task-disclosure.md` (substitute PHASE_ID = "07").

---

## Mandatory Steps

**Purpose:** Update DoD format for git commit - prepare documentation

**Required Subagents:** None (file operations only)

**Pre-Check: Implementation Notes Section**
```
Grep(pattern="^## Implementation Notes", path="${STORY_FILE}")

IF NOT found:
  # Auto-create section before Workflow Status
  Edit(
    file_path="${STORY_FILE}",
    old_string="## Workflow Status",
    new_string="## Implementation Notes\n\n**Developer:** DevForgeAI AI Agent\n**Implemented:** ${CURRENT_DATE}\n\n## Workflow Status"
  )
```

**Steps:**

1. **Mark completed items [x] in Definition of Done section**
   ```
   Edit(
     file_path="${STORY_FILE}",
     old_string="- [ ] {completed_item}",
     new_string="- [x] {completed_item}"
   )
   ```

2. **Add DoD items to Implementation Notes**
   - CRITICAL: Use FLAT LIST format
   - NO ### subsections under Implementation Notes
   ```
   Edit(
     file_path="${STORY_FILE}",
     old_string="## Implementation Notes\n\n**Developer:**",
     new_string="## Implementation Notes\n\n- [x] DoD item 1 completed\n- [x] DoD item 2 completed\n- [ ] DoD item 3 (DEFERRED: reason)\n\n**Developer:**"
   )
   ```

3. **Validate DoD format**
   ```bash
   devforgeai validate-dod ${STORY_FILE}
   # Exit code 0: Format valid
   # Exit code 1: Format invalid - fix and retry
   ```

4. **Update Workflow Status section**
   ```
   Edit(
     file_path="${STORY_FILE}",
     old_string="status: In Development",
     new_string="status: Dev Complete"
   )
   ```

4.5. **Populate TDD Workflow Summary and Files tables**
   ```
   # Read phase state for phase list and status
   Read(file_path="devforgeai/workflows/${STORY_ID}-phase-state.json")

   # Skip guard: Only populate empty tables (no rows after header separator)
   # IF Edit fails (old_string not found), tables are already populated — skip

   # Edit TDD Workflow Summary table (empty → populated)
   Edit(
     file_path="${STORY_FILE}",
     old_string="| Phase | Status | Details |\n|-------|--------|---------|",
     new_string="| Phase | Status | Details |\n|-------|--------|---------|\n| 01 Pre-Flight | ✅ Complete | {details from session context} |\n| 02 Red | ✅ Complete | {details from session context} |\n| 03 Green | ✅ Complete | {details from session context} |\n| 04 Refactor | ✅ Complete | {details from session context} |\n| 4.5 AC Verify | ✅ Complete | {details from session context} |\n| 05 Integration | ✅ Complete | {details from session context} |\n| 5.5 AC Verify | ✅ Complete | {details from session context} |"
   )

   # Edit Files Created/Modified table (empty → populated)
   Edit(
     file_path="${STORY_FILE}",
     old_string="| File | Action | Lines |\n|------|--------|-------|",
     new_string="| File | Action | Lines |\n|------|--------|-------|\n| {file_path} | {Created/Modified} | {line_range} |"
   )
   ```
   - Use phase-state.json for phase list/status; use session context for Details column
   - If phase-state.json not found, use inline observations from current session
   - See `references/dod-update-workflow.md` Step 5 for detailed template

5. **Final validation**
   ```bash
   devforgeai validate-dod ${STORY_FILE}
   # Exit code 0 required before proceeding
   ```

**Reference:** `references/dod-update-workflow.md` for complete workflow
    Read(file_path="references/dod-update-workflow.md")

### Format Requirements

**CORRECT Implementation Notes Format:**
```markdown
## Implementation Notes

- [x] Unit tests written and passing
- [x] Implementation complete
- [x] Code review completed
- [ ] Performance testing (DEFERRED: infrastructure not ready)

**Developer:** DevForgeAI AI Agent
**Implemented:** 2025-12-25

### TDD Workflow Summary (optional subsection OK)
...
```

**INCORRECT Format (will fail validation):**
```markdown
## Implementation Notes

### Definition of Done - Completed Items  ← NO! This subsection causes failures
- [x] Unit tests...
```

---

## Validation Checkpoint

**Before proceeding to Phase 08, verify:**

- [ ] DoD items marked [x] in story file
- [ ] Implementation Notes flat list added (no ### subsections)
- [ ] DoD format validated (exit code 0)
- [ ] Workflow Status updated

**IF any checkbox UNCHECKED:** HALT - Git commit will FAIL without proper DoD

---

## Pre-Exit Checklist

**Before calling `phase-complete`, verify ALL items:**

- [ ] DoD items marked [x] in story file
- [ ] Implementation Notes flat list added (no ### subsections)
- [ ] DoD format validated via devforgeai-validate (exit code 0)
- [ ] Workflow Status updated in story file
- [ ] TDD Workflow Summary table populated

**IF any item UNCHECKED and no N/A justification:** HALT — do not call exit gate.

---

## Optional Captures

### Observation Capture (EPIC-051)

Before exiting this phase, capture observations from DoD update operations:

1. **Collect Explicit Observations:**
   Capture DoD completion status as observations:
   - FOR each DoD item marked [x]:
     - Set category: "success"
     - Set severity: "low"
   - FOR each DoD item still [ ] (unchecked):
     - Set category: "gap"
     - Set severity: "medium"
   - Set source: "self-captured"

2. **Invoke Observation Extractor:**
   ```
   Task(subagent_type="observation-extractor",
        description="Extract observations from Phase 07 DoD update operations",
        prompt="Extract implicit observations from DoD update operations including completion patterns, documentation quality, and status tracking effectiveness.")
   ```
   - Set source: "extracted" for returned observations

3. **Append to Phase State:**
   FOR each observation (self-captured OR extracted):
   - Generate ID: "OBS-07-{timestamp}" (ISO8601 milliseconds)
   - Set fields: id, phase ("07"), category, note, severity, files[], source, timestamp
   - Append to phase-state.json observations[] array
   - Ensure no duplicate observations (skip if same finding in self-captured and extracted)

**Error Handling:** If observation capture fails, log warning and continue phase completion (non-blocking per BR-001).

### Session Memory Update (STORY-341)

Before exiting this phase, append observations to the session memory file:

```
# Append Phase 07 observations to session memory
session_path = ".claude/memory/sessions/${STORY_ID}-session.md"

Edit(
  file_path=session_path,
  old_string="## Observations",
  new_string="## Observations\n\n### Phase 07 (DoD Update)\n${OBSERVATIONS_LIST}"
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
devforgeai-validate phase-complete ${STORY_ID} --phase=07 --checkpoint-passed
# Exit code 0: Phase complete, proceed to Phase 08
# Exit code 1: Cannot complete - DoD format invalid
```
