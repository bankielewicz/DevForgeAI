# Phase 02: Safety Preview

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=remediation --from=01 --to=02
# Exit 0: proceed | Exit 1: Phase 01 incomplete
```

## Contract

PURPOSE: Generate and display previews for automated fixes, handle dry-run exit, get user confirmation for fix approach.
REQUIRED SUBAGENTS: None
REQUIRED ARTIFACTS: Fix previews displayed, user confirmation recorded
STEP COUNT: 3 mandatory steps

---

## Mandatory Steps

### Step 1: Generate Fix Previews

EXECUTE: For each finding classified as "automated", generate a preview showing the exact change that will be made.
```
FOR each finding WHERE classification == "automated":
    target_file = resolve file path from finding.Affected
    old_string = extract from finding.Evidence (the incorrect value)
    new_string = extract from finding.Remediation (the correct value)

    Display:

    <fix_preview>
      <finding_id>{finding_id}</finding_id>
      <severity>{severity}</severity>
      <file>{target_file_path}</file>
      <before>{old_string}</before>
      <after>{new_string}</after>
    </fix_preview>
```

If there are interactive or adr_required findings, also display a brief summary:
```
IF count_interactive > 0:
    Display: "{count_interactive} interactive findings will require your input in Phase 03."
IF count_adr > 0:
    Display: "{count_adr} findings require ADR review in Phase 03."
IF count_advisory > 0:
    Display: "{count_advisory} advisory findings (informational only, no fix)."
```

VERIFY: Every automated finding has a preview generated and displayed.
```
FOR each finding WHERE classification == "automated":
    ASSERT preview was displayed with finding_id, file, before, after
```

RECORD: Checkpoint write — previews generated.

---

### Step 2: Dry Run Exit Check

EXECUTE: If DRY_RUN is true, display completion message and skip to Phase 05 (report only).
```
IF DRY_RUN == true:
    Display: "Dry run complete. No files were modified."
    Display: "Re-run without --dry-run to apply fixes."
    Display: "{count_auto} automated fixes previewed."
    Display: "{count_interactive + count_adr} interactive/ADR fixes identified."

    Set SKIP_TO_PHASE_05 = true

    Update checkpoint:
      dry_run_active: true
      current_phase: 2
      phase_completion:
        phase_02: true
        phase_03: true    # Skipped (dry run)
        phase_04: true    # Skipped (dry run)

    GOTO Phase 05 (skip Phase 03 and Phase 04)
```

VERIFY: If dry run, confirm skip flag is set. If not dry run, proceed normally.
```
IF DRY_RUN == true:
    ASSERT SKIP_TO_PHASE_05 == true
ELSE:
    ASSERT SKIP_TO_PHASE_05 == false or undefined
```

RECORD:
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=remediation --phase=02 --step=dry-run-check
```

---

### Step 3: User Confirmation

EXECUTE: If not a dry run and there are automated fixes, ask the user how to proceed.
```
IF DRY_RUN == true:
    SKIP this step (already handled in Step 2)

IF count_auto > 0:
    AskUserQuestion:
        Question: "Apply {count_auto} automated fixes now?"
        Header: "Fix Mode"
        Options:
            - label: "Apply all automated fixes (Recommended)"
              description: "Safe, non-structural changes with post-fix verification"
            - label: "Review each fix individually"
              description: "Walk through each automated fix one at a time"
            - label: "Skip automated, do interactive only"
              description: "Manual control for all changes"

    Record user choice as USER_APPROVAL_MODE:
        "apply_all" | "review_each" | "skip_auto"

ELIF count_auto == 0 AND (count_interactive > 0 OR count_adr > 0):
    Display: "No automated fixes. Proceeding to interactive fixes."
    USER_APPROVAL_MODE = "no_auto"

ELIF count_auto == 0 AND count_interactive == 0 AND count_adr == 0:
    Display: "All findings are advisory or previously fixed. Nothing to apply."
    GOTO Phase 05
```

VERIFY: User response recorded and mapped to a valid approval mode.
```
ASSERT USER_APPROVAL_MODE in ["apply_all", "review_each", "skip_auto", "no_auto"]
```

RECORD: Update checkpoint with user approval mode.
```
Update checkpoint:
  current_phase: 2
  user_decisions:
    - timestamp: {current_timestamp}
      phase_02_approval: {USER_APPROVAL_MODE}
  phase_completion:
    phase_02: true
```

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=remediation --phase=02 --step=user-confirm
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=remediation --phase=02 --checkpoint-passed
# Exit 0: proceed to Phase 03 (or Phase 05 if dry run) | Exit 1: phase incomplete
```
