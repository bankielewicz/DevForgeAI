# Cleanup Workflow (SKILL.md Phase 6)

> **Phase mapping:** This file uses legacy step numbering (4.1-4.5). In SKILL.md v3.0, Cleanup is **Phase 6** with steps 6.1-6.5. The step content is identical — only the numbering prefix differs.

**Purpose:** Release locks, invoke feedback hooks, display final summary.

---

### Step 4.1: Release Lock File

```
IF config.concurrency.locking_enabled:
    Remove(file_path="{story_paths.results_dir}/.qa-lock")
    Display: "✓ Lock released for {STORY_ID}"
```

### Step 4.2: Invoke Feedback Hooks

**Reference:** `references/feedback-hooks-workflow.md`
    Read(file_path=".claude/skills/spec-driven-qa/references/feedback-hooks-workflow.md")

```
# Map QA result to hook status
IF overall_status == "PASSED": STATUS = "success"
ELIF overall_status == "FAILED": STATUS = "failure"
ELSE: STATUS = "partial"

# Check and invoke hooks (non-blocking)
Bash(command="devforgeai-validate check-hooks --operation=qa --status=$STATUS")
IF exit_code == 0:
    Bash(command="devforgeai-validate invoke-hooks --operation=qa --story=$STORY_ID")
```

### Step 4.3: Execution Summary [MANDATORY - HALT ON INCOMPLETE]

**Purpose:** Enforce visibility of all phase executions before workflow completion.

**Constitution Alignment:** Quality gates MUST block on violations (architecture-constraints.md line 106)

Display the following summary (CANNOT be skipped):

```
╔══════════════════════════════════════════════════════════════╗
║                    QA EXECUTION SUMMARY                      ║
╠══════════════════════════════════════════════════════════════╣
║  Story: {STORY_ID}                                           ║
║  Mode: {MODE}                                                ║
╠══════════════════════════════════════════════════════════════╣
║  PHASE EXECUTION STATUS:                                     ║
║  - [x] Phase 0: Setup (Lock: {YES/NO})                       ║
║  - [x] Phase 1: Validation (Traceability: {score}%)          ║
║  - [x] Phase 2: Analysis (Validators: {count}/3)             ║
║  - [x] Phase 3: Reporting (Status: {status})                 ║
║  - [x] Phase 4: Cleanup (Hooks: {status})                    ║
╠══════════════════════════════════════════════════════════════╣
║  Story File Updated: {YES/NO}                                ║
║  Result: {PASSED/FAILED}                                     ║
╚══════════════════════════════════════════════════════════════╝
```

**Enforcement Logic:**

```
# Count unchecked phases
unchecked_count = count_unchecked_phases()

IF unchecked_count > 0:
    Display: "⚠️ WARNING: {unchecked_count} phases may have been skipped"

    AskUserQuestion:
        Question: "Phases appear incomplete. How should I proceed?"
        Header: "Incomplete Execution"
        Options:
            - label: "Re-run skipped phases now"
              description: "Return to first skipped phase and complete workflow"
            - label: "Continue with incomplete execution (NOT RECOMMENDED)"
              description: "Proceed despite missing phases - may cause issues"
            - label: "Abort QA validation"
              description: "Stop workflow and investigate manually"
        multiSelect: false

    IF user chooses "Re-run": GOTO first skipped phase
    IF user chooses "Continue": Log warning, proceed with caution
    IF user chooses "Abort": HALT workflow

IF unchecked_count == 0:
    Display: "✓ All phases complete - No skipped steps detected"
```

**Validation Checkpoint:**
- [ ] Execution summary displayed?
- [ ] All phases marked complete?
- [ ] Story file update confirmed?
- [ ] **IF QA FAILED: gaps.json exists?** [RCA-002]

**gaps.json Verification (Conditional):**
```
IF overall_status == "FAILED" OR overall_status == "PASS WITH WARNINGS":
    gaps_file = Glob(pattern="devforgeai/qa/reports/{STORY-ID}-gaps.json")
    IF NOT gaps_file:
        Display: "❌ CRITICAL: gaps.json missing for {overall_status} QA"
        HALT: "Create gaps.json before completing QA workflow"
    ELSE:
        Display: "✓ gaps.json verified: {gaps_file}"
ELSE:
    # PASSED (clean) - skip gaps.json check
    Display: "✓ gaps.json check skipped (QA passed with no issues)"
```

IF any checkbox unchecked: HALT with "Execution incomplete"

---

### Step 4.4: Display Final Summary

```
Display:
╔════════════════════════════════════════════════════════╗
║                    QA VALIDATION COMPLETE              ║
╠════════════════════════════════════════════════════════╣
║ Story: {STORY_ID}                                      ║
║ Mode: {mode}                                           ║
║ Result: {overall_status}                               ║
╠════════════════════════════════════════════════════════╣
║ Coverage:                                              ║
║   Business Logic: {biz}% | Application: {app}%         ║
║   Infrastructure: {infra}% | Overall: {overall}%       ║
╠════════════════════════════════════════════════════════╣
║ Violations: {critical} CRITICAL | {high} HIGH          ║
║             {medium} MEDIUM | {low} LOW                ║
╠════════════════════════════════════════════════════════╣
║ Next Steps:                                            ║
║   [If PASSED] Ready for /release {STORY_ID}            ║
║   [If FAILED] Run /dev {STORY_ID} for remediation      ║
╚════════════════════════════════════════════════════════╝
```

### Step 4.5: Marker Cleanup [CONDITIONAL - QA PASSED ONLY]

**Purpose:** Preserve qa-phase-state.json as the permanent audit trail and delete legacy .qa-phase-N.marker files after successful QA validation.

**Trigger:** Execute ONLY when overall_status == "PASSED"

**Critical:** DO NOT delete qa-phase-state.json — it remains as the permanent audit trail after cleanup. Only DELETE legacy .qa-phase-N.marker files.

```
IF overall_status == "PASSED":
    # PRESERVE: qa-phase-state.json remains after cleanup (permanent audit trail)
    # DO NOT delete qa-phase-state.json — it is retained indefinitely
    Glob(pattern="devforgeai/workflows/{STORY_ID}-qa-phase-state.json")
    IF NOT found:
        Display: "⚠️ WARNING: qa-phase-state.json not found — audit trail missing"
    ELSE:
        Display: "✓ qa-phase-state.json preserved as permanent audit trail"

    # DELETE: legacy .qa-phase-N.marker files (superseded by qa-phase-state.json)
    Glob(pattern="devforgeai/qa/reports/{STORY_ID}/.qa-phase-*.marker")

    FOR each marker_file in results:
        Bash(command="rm {marker_file}")

    Display: "✓ Legacy .qa-phase-N.marker files cleaned up for {STORY_ID}"

ELSE:
    Display: "⚠️ QA FAILED - All files retained for debugging and resume capability"
```

**Rationale:**
- **qa-phase-state.json IS the permanent audit trail** — preserved indefinitely, matching /dev workflow behavior where phase-state.json files persist
- **Legacy .qa-phase-N.marker files** — deleted on PASS since they are superseded by qa-phase-state.json
- **FAILED:** All files retained for debugging and to enable resume from last completed phase
