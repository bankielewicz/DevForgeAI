# Phase F04: Classify Findings

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --from=F03 --to=F04 --workflow=doc-fix
# Exit 0: proceed | Exit 1: Phase F03 incomplete
```

## Contract

PURPOSE: Group filtered findings into automated (deterministic, safe) and interactive (requires user approval) categories. Display fix plan.
REQUIRED SUBAGENTS: (none)
REQUIRED ARTIFACTS: automated_findings list, interactive_findings list, fix plan displayed
STEP COUNT: 2 mandatory steps

---

## Mandatory Steps

### Step F04.1: Group by Fix Mode

EXECUTE: Separate findings into automated and interactive groups.
```
automated_findings = [f for f in filtered_findings if f["fix_mode"] == "automated"]
interactive_findings = [f for f in filtered_findings if f["fix_mode"] == "interactive"]

Display: "Classification:"
Display: "  Automated: {len(automated_findings)} findings (will apply without prompting)"
Display: "  Interactive: {len(interactive_findings)} findings (will ask for approval)"

IF automated_findings:
    Display: ""
    Display: "  Automated fixes:"
    FOR each f in automated_findings:
        Display: "    {f['id']} [{f['severity']}] {f['summary']}"

IF interactive_findings:
    Display: ""
    Display: "  Interactive fixes:"
    FOR each f in interactive_findings:
        Display: "    {f['id']} [{f['severity']}] {f['summary']}"
```
VERIFY: automated_findings + interactive_findings == filtered_findings (no findings lost).
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=F04 --step=F04.1 --workflow=doc-fix`

---

### Step F04.2: Display Fix Plan Summary

EXECUTE: Show a concise fix plan with counts and estimated scope.
```
Display: ""
Display: "Fix Plan:"
Display: "  {len(automated_findings)} automated fixes (will apply without prompting)"
Display: "  {len(interactive_findings)} interactive fixes (will ask for approval)"
Display: ""

# Count unique affected files
all_affected = set()
FOR each f in filtered_findings:
    FOR each file in f["affected"]:
        all_affected.add(file)

Display: "  Files that will be modified: {len(all_affected)}"
FOR each file in sorted(all_affected):
    Display: "    {file}"
```
VERIFY: Fix plan displayed with file counts.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=F04 --step=F04.2 --workflow=doc-fix`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --phase=F04 --checkpoint-passed --workflow=doc-fix
```

## Phase Transition Display

```
Display: "Phase F04 complete: Classify Findings"
Display: "  Proceeding to Phase F05: Preview Changes"
```
