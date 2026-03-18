# Phase 06: Cleanup

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --workflow=qa --from=05 --to=06 --project-root=.
# Exit 0: proceed | Exit 1: Phase 05 incomplete
```

## Contract

PURPOSE: Release locks, invoke feedback hooks, display execution summary.
REQUIRED SUBAGENTS: none
REQUIRED ARTIFACTS: Execution summary displayed, feedback hooks invoked
STEP COUNT: 5 mandatory steps

---

## Reference Loading

Load BEFORE executing steps:
```
Read(file_path=".claude/skills/devforgeai-qa/references/phase-4-cleanup-workflow.md")
Read(file_path=".claude/skills/devforgeai-qa/references/feedback-hooks-workflow.md")
```

---

## Mandatory Steps

### Step 6.1: Release Lock File

EXECUTE: Delete the QA lock file acquired in Phase 01.
```
lock_file = "{story_paths.results_dir}/.qa-lock"

Glob(pattern=lock_file)
IF exists:
    Bash(command="rm {lock_file}")
    Display: "Lock released for ${STORY_ID}"
ELSE:
    Display: "Lock file not found (already released or not acquired)"
```

VERIFY: Lock file no longer exists on disk.
```
Glob(pattern=lock_file)
IF still exists: Display "WARNING: Lock file removal failed"
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=06 --step=6.1 --project-root=.`

---

### Step 6.2: Invoke Feedback Hooks (Non-Blocking)

EXECUTE: Check and invoke feedback hooks. Map QA result to hook status. Failures in hooks do NOT block QA completion.
```
# Map QA result to hook status
IF overall_status == "PASSED": STATUS = "success"
ELIF overall_status == "FAILED": STATUS = "failure"
ELSE: STATUS = "partial"

# Check hooks availability
Bash(command="source .venv/bin/activate && devforgeai-validate check-hooks --operation=qa --status=${STATUS} --project-root=. 2>&1")

IF exit_code == 0:
    # Hooks available -- invoke them
    Bash(command="source .venv/bin/activate && devforgeai-validate invoke-hooks --operation=qa --story=${STORY_ID} --project-root=. 2>&1")
    Display: "Feedback hooks: Invoked (status: ${STATUS})"
ELSE:
    Display: "Feedback hooks: Not available or disabled"

# Non-blocking: regardless of hook result, continue to Step 6.3
```

VERIFY: Hook check executed (exit code captured). Hook invocation attempted if available. Workflow continues regardless of hook outcome.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=06 --step=6.2 --project-root=.`

---

### Step 6.3: Display Execution Summary (MANDATORY)

EXECUTE: Display phase-by-phase completion status. This step CANNOT be skipped -- it enforces visibility of all phase executions before workflow completion.
```
Display:
"
======================================================================
                      QA EXECUTION SUMMARY
======================================================================
  Story: ${STORY_ID}
  Mode: ${MODE}
----------------------------------------------------------------------
  PHASE EXECUTION STATUS:
  - [x] Phase 01: Setup (Lock: YES, Type: ${DELIVERABLE_TYPE})
  - [x] Phase 02: Validation (Traceability: {traceability_score}%)
  - [x] Phase 03: Diff Regression (Result: {phase_3_result})
  - [x] Phase 04: Analysis (Validators: {success}/{total})
  - [x] Phase 05: Reporting (Status: {overall_status})
  - [x] Phase 06: Cleanup (Hooks: {hook_status})
----------------------------------------------------------------------
  Story File Updated: YES
  Result: {overall_status}
======================================================================
"
```

**Enforcement Logic:**
```
# Count unchecked phases
unchecked_count = count_unchecked_phases()

IF unchecked_count > 0:
    Display: "WARNING: {unchecked_count} phases may have been skipped"

    AskUserQuestion:
        Question: "Phases appear incomplete. How should I proceed?"
        Header: "Incomplete"
        Options:
            - label: "Re-run skipped phases"
              description: "Return to first skipped phase and complete workflow"
            - label: "Continue (NOT RECOMMENDED)"
              description: "Proceed despite missing phases"
            - label: "Abort QA"
              description: "Stop workflow and investigate manually"
        multiSelect: false

    IF user chooses "Re-run": GOTO first skipped phase
    IF user chooses "Continue": Log warning
    IF user chooses "Abort": HALT workflow

IF unchecked_count == 0:
    Display: "All phases complete -- no skipped steps detected"
```

VERIFY: Execution summary displayed. All phases marked complete (or user acknowledged incomplete state).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=06 --step=6.3 --project-root=.`

---

### Step 6.4: Display Final QA Validation Summary

EXECUTE: Display the formatted final summary with metrics and next steps.
```
Display:
"
======================================================================
                    QA VALIDATION COMPLETE
======================================================================
  Story: ${STORY_ID}
  Mode: ${MODE}
  Result: {overall_status}
----------------------------------------------------------------------
  Coverage:
    Business Logic: {biz}% | Application: {app}%
    Infrastructure: {infra}% | Overall: {overall}%
----------------------------------------------------------------------
  Violations: {critical} CRITICAL | {high} HIGH
              {medium} MEDIUM | {low} LOW
----------------------------------------------------------------------
  Next Steps:
    [If PASSED] Ready for /release ${STORY_ID}
    [If FAILED] Run /dev ${STORY_ID} --fix for remediation
======================================================================
"
```

**gaps.json Verification (Conditional):**
```
IF overall_status == "FAILED" OR overall_status == "PASS WITH WARNINGS":
    Glob(pattern="devforgeai/qa/reports/${STORY_ID}-gaps.json")
    IF NOT found:
        Display: "CRITICAL: gaps.json missing for {overall_status} QA"
        HALT: "Create gaps.json before completing QA workflow"
    ELSE:
        Display: "gaps.json verified: exists"
ELSE:
    Display: "gaps.json check skipped (QA passed with no issues)"
```

VERIFY: Final summary displayed. If FAILED/WARNINGS, gaps.json verified to exist.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=06 --step=6.4 --project-root=.`

---

### Step 6.5: Marker Cleanup (PASSED Only)

EXECUTE: Preserve qa-phase-state.json as permanent audit trail. Delete legacy marker files only if QA PASSED.
```
IF overall_status == "PASSED":
    # PRESERVE: qa-phase-state.json (permanent audit trail -- DO NOT DELETE)
    Glob(pattern="devforgeai/workflows/${STORY_ID}-qa-phase-state.json")
    IF found:
        Display: "qa-phase-state.json preserved as permanent audit trail"
    ELSE:
        Display: "WARNING: qa-phase-state.json not found -- audit trail missing"

    # DELETE: legacy .qa-phase-N.marker files (superseded by qa-phase-state.json)
    Glob(pattern="devforgeai/qa/reports/${STORY_ID}/.qa-phase-*.marker")
    FOR each marker_file in results:
        Bash(command="rm {marker_file}")
    Display: "Legacy .qa-phase-N.marker files cleaned up"

ELSE:
    Display: "QA FAILED -- all files retained for debugging and resume capability"
```

VERIFY: If PASSED, qa-phase-state.json preserved and legacy markers deleted. If FAILED, all files retained.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=06 --step=6.5 --project-root=.`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --workflow=qa --phase=06 --checkpoint-passed --project-root=.
# Exit 0: QA workflow complete | Exit 1: HALT
```

## Phase 06 Completion Display

```
Phase 06 Complete: Cleanup
  QA workflow complete -- all 6 phase gates passed
  Result: {overall_status}
```
