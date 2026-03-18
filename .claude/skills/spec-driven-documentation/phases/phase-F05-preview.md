# Phase F05: Preview Changes

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --from=F04 --to=F05 --workflow=doc-fix
# Exit 0: proceed | Exit 1: Phase F04 incomplete
```

## Contract

PURPOSE: Display a summary table of all planned changes and obtain user consent before executing any modifications.
REQUIRED SUBAGENTS: (none)
REQUIRED ARTIFACTS: Preview table displayed, user consent obtained
STEP COUNT: 2 mandatory steps

---

## Mandatory Steps

### Step F05.1: Display Change Preview Table

EXECUTE: Show all planned changes in a formatted table.
```
Display: ""
Display: "Planned Changes:"
Display: ""
Display: "| ID    | Type                  | Action              | Target File          | Mode        |"
Display: "|-------|-----------------------|---------------------|----------------------|-------------|"

FOR each f in filtered_findings:
    Display: "| {f['id']} | {f['type']:<21} | {f['fix_action']:<19} | {f['affected'][0]:<20} | {f['fix_mode']:<11} |"

Display: ""
Display: "Total: {len(filtered_findings)} changes across {len(all_affected)} files"
```
VERIFY: Preview table displayed with all findings listed.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=F05 --step=F05.1 --workflow=doc-fix`

---

### Step F05.2: Obtain User Consent

EXECUTE: Ask user for permission to proceed with fixes.
```
AskUserQuestion:
    Question: "Proceed with {len(automated_findings)} automated + {len(interactive_findings)} interactive fixes?"
    Header: "Fix Consent"
    Options:
        - label: "Proceed with all"
          description: "Apply automated fixes and prompt for each interactive fix"
        - label: "Auto-only (skip interactive)"
          description: "Apply only automated fixes, skip all interactive ones"
        - label: "Cancel"
          description: "Exit without making any changes"
    multiSelect: false

IF user chooses "Cancel":
    Display: "Fix workflow cancelled by user."
    # Record cancellation and EXIT
    devforgeai-validate phase-record ${SESSION_ID} --phase=F05 --step=F05.2 --workflow=doc-fix
    devforgeai-validate phase-complete ${SESSION_ID} --phase=F05 --checkpoint-passed --workflow=doc-fix
    EXIT with result = "CANCELLED"

IF user chooses "Auto-only (skip interactive)":
    interactive_findings = []  # Clear interactive list
    Display: "Interactive fixes skipped. Proceeding with {len(automated_findings)} automated fixes only."

IF user chooses "Proceed with all":
    Display: "Proceeding with all {len(filtered_findings)} fixes."
```
VERIFY: User consent obtained. execution_findings list finalized (automated + interactive or automated only).
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=F05 --step=F05.2 --workflow=doc-fix`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --phase=F05 --checkpoint-passed --workflow=doc-fix
```

## Phase Transition Display

```
Display: "Phase F05 complete: Preview Changes"
Display: "  User consent: obtained"
Display: "  Proceeding to Phase F06: Execute Fixes"
```
