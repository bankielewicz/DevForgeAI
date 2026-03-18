# Phase 08: Completion Report

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=stories --from=07 --to=08 --project-root=.
```

| Exit Code | Action |
|-----------|--------|
| 0 | Prerequisites met. Proceed. |
| 1 | Phase 07 incomplete. HALT. |
| 127 | CLI not installed. Proceed without enforcement. |

---

## Contract

- **PURPOSE:** Generate structured completion summary and guide next actions
- **REQUIRED SUBAGENTS:** none
- **REQUIRED ARTIFACTS:** Completion report displayed, next action recommendation
- **STEP COUNT:** 3
- **REFERENCE FILES:**
  - `references/completion-report.md`

---

## Reference Loading [MANDATORY]

```
Read(file_path="src/claude/skills/spec-driven-stories/references/completion-report.md")
```

IF Read fails: HALT -- "Phase 08 reference file not loaded."

Do NOT rely on memory of previous reads. Load reference fresh.

---

## Mandatory Steps (3)

### Step 8.1: Generate Completion Summary

**EXECUTE:**
```
Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Story Creation Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Story: ${STORY_ID}
Title: ${story_title}
File: ${STORY_FILE_PATH}
Status: Backlog
Priority: ${PRIORITY}
Points: ${POINTS}
Type: ${TYPE}
Epic: ${EPIC_ID || 'N/A'}
Sprint: ${SPRINT_ID}

Sections Generated:
  - User Story (As a/I want/So that)
  - ${ac_count} Acceptance Criteria (Given/When/Then)
  - Technical Specification (v2.0 YAML)
  - UI Specification: ${ui_detected ? 'Yes' : 'N/A'}
  - Non-Functional Requirements
  - Definition of Done
  - Test Strategy

Validation: ${VALIDATION_RESULT}
Epic Linked: ${epic_linked}
Sprint Linked: ${sprint_linked}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

**VERIFY:** Summary displayed with all key fields populated.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=08 --step=8.1 --project-root=.
```
Update checkpoint: `phases["08"].steps_completed.append("8.1")`

---

### Step 8.2: Determine Next Action

**EXECUTE:**
```
IF $BATCH_MODE == true:
  # Batch mode: skip question, return control to batch loop
  Display: "Batch mode - returning control to command for next feature."
ELSE:
  # Interactive mode: ask user what to do next
  AskUserQuestion:
    Question: "What would you like to do next?"
    Header: "Next Step"
    Options:
      - label: "Create another story"
        description: "Run /create-story again for a new feature"
      - label: "Start development"
        description: "Run /dev ${STORY_ID} to begin TDD implementation"
      - label: "Review the story"
        description: "Read the generated story file for review"
      - label: "Done for now"
        description: "End the story creation workflow"
```

**VERIFY:** Next action determined (batch: implicit return, interactive: user selection).

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=08 --step=8.2 --project-root=.
```
Update checkpoint: `phases["08"].steps_completed.append("8.2")`

---

### Step 8.3: Finalize Session

**EXECUTE:**
```
# Update checkpoint to completed
checkpoint.status = "completed"
checkpoint.updated_at = current ISO 8601 timestamp
checkpoint.progress.phases_completed.append("08")
checkpoint.progress.current_phase = 8

Write updated checkpoint to disk
Verify write via Glob()

Display: "Session ${SESSION_ID} complete. All 8 phases executed."
```

**VERIFY:** Checkpoint status is "completed" and written to disk.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=08 --step=8.3 --project-root=.
```
Update checkpoint: `phases["08"].steps_completed.append("8.3")`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=stories --phase=08 --checkpoint-passed --project-root=.
```

## Exit Verification Checklist

- [ ] Completion summary displayed with all fields
- [ ] Next action determined (batch return or user selection)
- [ ] Checkpoint updated to "completed" status
- [ ] Checkpoint written to disk and verified

IF any unchecked: HALT -- "Phase 08 exit criteria not met"

## Workflow Complete

```
Display: "All 8 phases completed - Workflow validation passed"
Display: "Story ${STORY_ID} is ready for development."
```
