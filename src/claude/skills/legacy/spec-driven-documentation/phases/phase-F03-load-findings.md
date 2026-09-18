# Phase F03: Load Findings

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --from=02 --to=F03 --workflow=doc-fix
# Exit 0: proceed | Exit 1: Phase 02 incomplete
```

## Contract

PURPOSE: Read the audit JSON file, parse findings, filter by --type or --finding arguments, skip previously applied findings.
REQUIRED SUBAGENTS: (none)
REQUIRED ARTIFACTS: Filtered findings list ready for classification
STEP COUNT: 3 mandatory steps

---

## Reference Loading [MANDATORY]

```
Read(file_path="references/audit-fix-catalog.md")
```

IF Read fails: HALT -- "Phase F03 reference file not loaded. Cannot proceed."

---

## Mandatory Steps

### Step F03.1: Read Audit File

EXECUTE: Load and parse the audit JSON file.
```
audit_file = "devforgeai/qa/audit/doc-audit.json"
content = Read(file_path=audit_file)

IF Read fails:
    HALT: "No audit file found at {audit_file}. Run '/document --audit=dryrun' first."

audit_data = parse_json(content)
all_findings = audit_data["findings"]
fix_sessions = audit_data.get("fix_sessions", [])

Display: "Audit file loaded: {len(all_findings)} total findings"
Display: "Previous fix sessions: {len(fix_sessions)}"
```
VERIFY: audit_data is valid JSON with "findings" array.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=F03 --step=F03.1 --workflow=doc-fix`

---

### Step F03.2: Apply Filters

EXECUTE: Filter findings based on --type and --finding arguments.
```
filtered_findings = all_findings.copy()

# Filter by type
IF $FINDING_FILTER != "all" AND $FINDING_FILTER matches "F-[0-9]+":
    # Single finding mode
    filtered_findings = [f for f in filtered_findings if f["id"] == $FINDING_FILTER]
    IF not filtered_findings:
        HALT: "Finding {$FINDING_FILTER} not found in audit file"
    Display: "Filtered to single finding: {$FINDING_FILTER}"

ELIF $DOC_TYPE != "all":
    # Type filter mode
    filtered_findings = [f for f in filtered_findings if f["type"].startswith($DOC_TYPE)]
    Display: "Filtered by type '{$DOC_TYPE}': {len(filtered_findings)} findings"

ELSE:
    Display: "No filter applied: processing all {len(filtered_findings)} findings"
```
VERIFY: filtered_findings is a non-empty list. If empty after filter, HALT with message.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=F03 --step=F03.2 --workflow=doc-fix`

---

### Step F03.3: Skip Previously Applied

EXECUTE: Remove findings that were already fixed in previous sessions.
```
previously_applied = set()
FOR each session in fix_sessions:
    FOR each detail in session.get("details", []):
        IF detail["status"] == "applied":
            previously_applied.add(detail["id"])

skipped_count = 0
remaining_findings = []
FOR each finding in filtered_findings:
    IF finding["id"] in previously_applied:
        skipped_count += 1
    ELSE:
        remaining_findings.append(finding)

filtered_findings = remaining_findings

Display: "Loaded {len(filtered_findings)} findings to process ({skipped_count} previously applied)"

IF len(filtered_findings) == 0:
    Display: "All findings already applied. Nothing to fix."
    # Record phase as complete and EXIT
    devforgeai-validate phase-complete ${SESSION_ID} --phase=F03 --checkpoint-passed --workflow=doc-fix
    EXIT
```
VERIFY: filtered_findings updated to exclude previously applied. skipped_count >= 0.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=F03 --step=F03.3 --workflow=doc-fix`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --phase=F03 --checkpoint-passed --workflow=doc-fix
```

## Phase Transition Display

```
Display: "Phase F03 complete: Load Findings"
Display: "  Findings to process: {len(filtered_findings)}"
Display: "  Previously applied: {skipped_count}"
Display: "  Proceeding to Phase F04: Classify Findings"
```
