# Phase 08: Feedback & Completion

**Purpose:** Invoke feedback hooks, generate completion report, and finalize the UI generation workflow.

**Pre-Flight:** Verify Phase 07 completed.

---

## Step 8.1: Check Feedback Hook Eligibility

**EXECUTE:**
```
Bash(command="devforgeai-validate check-hooks --operation=create-ui --status=completed 2>&1")
```

**VERIFY:**
- Exit code 0: Hooks are enabled and eligible → proceed to Step 8.2
- Exit code non-zero: Hooks not configured or not eligible → skip to Step 8.3

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=08 --step=8.1 --project-root=. 2>&1")
```

---

## Step 8.2: Invoke Feedback Hooks (Conditional)

**EXECUTE:**
```
IF hooks eligible (Step 8.1 exit code 0):
    Bash(command="devforgeai-validate invoke-hooks --operation=create-ui 2>&1")

    Pass context:
    - ui_type: ${UI_TYPE}
    - technology: ${FRAMEWORK}
    - components: ${COMPONENTS}
    - styling: ${STYLING}
    - story_id: ${STORY_ID} (if story mode)
    - status: ${STATUS}
ELSE:
    Display: "Feedback hooks not configured. Skipping."
```

**VERIFY:**
- Hook invocation completed (success or graceful failure)
- Non-blocking: If hooks fail, log warning and continue

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=08 --step=8.2 --project-root=. 2>&1")
```

---

## Step 8.3: Generate Completion Report

**EXECUTE:**
Display completion report to user:

```
## UI Generation Complete

**Status:** ${STATUS}
**Mode:** ${MODE}
**UI Type:** ${UI_TYPE}
**Framework:** ${FRAMEWORK}
**Styling:** ${STYLING}
**Theme:** ${THEME}

### Generated Files
- Component: ${OUTPUT_PATH}
- Spec Summary: devforgeai/specs/ui/UI-SPEC-SUMMARY.md

### Components Created
${COMPONENTS list with details}

### Next Steps
- Review generated code
- Install any required dependencies
- Run /dev to implement the full story (if story mode)
- Run /qa to validate the implementation
```

If FORMATTER_RESULT contains display template and next_steps, output those as-is.

**VERIFY:**
- Completion report displayed to user
- Report contains: status, mode, files generated, next steps

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=08 --step=8.3 --project-root=. 2>&1")
```

---

## Phase 08 Completion

**EXECUTE:**
```
Bash(command="devforgeai-validate phase-complete ${IDENTIFIER} --workflow=ui --phase=08 --project-root=. 2>&1")
```

**VERIFY:**
- Exit code 0 or 2 (backward compatibility)

**WORKFLOW COMPLETE.** All 9 phases executed successfully.
