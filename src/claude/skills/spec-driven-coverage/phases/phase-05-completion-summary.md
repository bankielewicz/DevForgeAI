# Phase 05: Completion Summary

**Purpose:** Delegate batch results display to the epic-coverage-result-interpreter subagent. Present success/failure counts, per-story status, and next steps.

**Mode:** create only (skip this phase for validate and detect modes)

**Pre-Flight:** Verify Phase 04 completed and batch results are available.

---

## Step 5.1: Verify Phase 04 Completion

**EXECUTE:**
Check that results from Phase 04 is available in working memory.

**VERIFY:**
- results object exists
- results.success is an array
- results.failed is an array
- results.success.length + results.failed.length > 0

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=05 --step=5.1 --project-root=. 2>&1")
```

---

## Step 5.2: Delegate to epic-coverage-result-interpreter Subagent

**EXECUTE:**
```
Task(
    subagent_type="epic-coverage-result-interpreter",
    description="Format batch completion summary",
    prompt="""
    Generate batch summary display.

    Data:
    - Success count: ${results.success.length}
    - Failed count: ${results.failed.length}
    - Success list: ${JSON.stringify(results.success)}
    - Failed list: ${JSON.stringify(results.failed)}
    - Epic ID: ${EPIC_ID}

    Include:
    - Success/fail counts with clear visual indicators
    - Per-story status (story ID + feature name) for successful stories
    - Failure details with error messages for failed stories
    - Recovery commands for failed stories (e.g., /create-story commands)
    - Next steps guidance:
      - Review created stories
      - Run /validate-epic-coverage ${EPIC_ID} to verify updated coverage
      - Start development with /dev STORY-NNN
    """
)
```

**VERIFY:**
- Subagent was invoked (Task call completed)
- Subagent returned summary output
- Summary includes success/fail counts

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=05 --step=5.2 --project-root=. 2>&1")
```

---

## Step 5.3: Present Completion Summary

**EXECUTE:**
Present the subagent's formatted summary to the user. The summary includes:
- Total stories created vs failed
- Per-story details (story ID, feature name, status)
- Error details for any failed creations
- Recovery commands for retrying failed stories
- Next steps for the user

**VERIFY:**
- Summary output presented to user
- All batch results accounted for

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=05 --step=5.3 --project-root=. 2>&1")
```

---

## Phase 05 Completion

**EXECUTE:**
```
Bash(command="devforgeai-validate phase-complete ${IDENTIFIER} --phase=05 --project-root=. 2>&1")
```

**VERIFY:**
- Exit code 0 or 2 (backward compatibility)

**NEXT:** DONE for create mode. Return batch results to the invoking command.
