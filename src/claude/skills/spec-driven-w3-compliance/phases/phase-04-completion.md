# Phase 04: Completion

## Entry Gate

```bash
devforgeai-validate phase-check W3-AUDIT --workflow=w3-compliance --from=03 --to=04 --project-root=.
# Exit 0: proceed | Exit 1: HALT (Phase 03 not complete)
```

## Contract

PURPOSE: Determine exit status based on violation severity, display final summary, and mark workflow as complete.
REQUIRED SUBAGENTS: none
REQUIRED ARTIFACTS: Exit status determination, workflow completion marker
STEP COUNT: 3 mandatory steps

---

## Mandatory Steps

### Step 4.1: Determine Exit Status

EXECUTE: Set exit status based on violation severity. CRITICAL violations cause audit failure (exit 1). All other results pass (exit 0).
```
IF CRITICAL_COUNT > 0:
    $EXIT_STATUS = 1
    $RESULT_LABEL = "FAILED"
    $RESULT_ICON = "AUDIT FAILED"
    Display: "AUDIT FAILED: {CRITICAL_COUNT} CRITICAL violations detected"
ELIF HIGH_COUNT > 0:
    $EXIT_STATUS = 0
    $RESULT_LABEL = "WARNING"
    $RESULT_ICON = "AUDIT WARNING"
    Display: "AUDIT WARNING: {HIGH_COUNT} HIGH priority violations require review"
ELSE:
    $EXIT_STATUS = 0
    $RESULT_LABEL = "PASSED"
    $RESULT_ICON = "W3 AUDIT PASSED"
    Display: "W3 AUDIT PASSED"
```
VERIFY: $EXIT_STATUS is set to 0 or 1. $RESULT_LABEL is set to FAILED, WARNING, or PASSED.
RECORD: `devforgeai-validate phase-record W3-AUDIT --workflow=w3-compliance --phase=04 --step=4.1 --project-root=.`

---

### Step 4.2: Display Final Summary

EXECUTE: Display a final summary line with the audit result.
```
Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
"  ${RESULT_ICON}"
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
"  CRITICAL: ${CRITICAL_COUNT}"
"  HIGH:     ${HIGH_COUNT}"
"  MEDIUM:   ${MEDIUM_COUNT}"
"  INFO:     ${INFO_COUNT}"
"  Result:   ${RESULT_LABEL}"
"  Exit:     ${EXIT_STATUS}"
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```
VERIFY: Final summary displayed with all violation counts and exit status.
RECORD: `devforgeai-validate phase-record W3-AUDIT --workflow=w3-compliance --phase=04 --step=4.2 --project-root=.`

---

### Step 4.3: Mark Workflow Complete

EXECUTE: Record workflow completion. All 4 phases have been executed.
```
Display: "All 4 phases completed - W3 compliance audit workflow complete"
Display: ""
Display: "Phases executed:"
Display: "  Phase 01: Setup - DONE"
Display: "  Phase 02: Scanning - DONE"
Display: "  Phase 03: Reporting - DONE"
Display: "  Phase 04: Completion - DONE"
```
VERIFY: Completion message displayed. All 4 phases listed as DONE.
RECORD: `devforgeai-validate phase-record W3-AUDIT --workflow=w3-compliance --phase=04 --step=4.3 --project-root=.`

---

## Exit Gate

```bash
devforgeai-validate phase-complete W3-AUDIT --workflow=w3-compliance --phase=04 --checkpoint-passed --project-root=.
# Exit 0: workflow complete | Exit 1: HALT
```

## Phase 04 Completion Display

```
Phase 04 Complete: Completion
  Result: ${RESULT_LABEL}
  Exit status: ${EXIT_STATUS}
  Workflow: Complete
```
