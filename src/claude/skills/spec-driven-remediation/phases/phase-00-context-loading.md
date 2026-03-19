# Phase 00: Context Loading + Finding Extraction

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=remediation --from=init --to=00
# Exit 0: proceed | Exit 1: initialization incomplete
```

## Contract

PURPOSE: Load audit file, parse findings, load reference files, apply filters, detect resume state.
REQUIRED SUBAGENTS: None (all work is inline)
REQUIRED ARTIFACTS: Findings list, checkpoint file
STEP COUNT: 5 mandatory steps

---

## Mandatory Steps

### Step 1: Read Context Markers

EXECUTE: Read the context markers set by the `/fix-story` command in the conversation. Extract all 5 parameters.
```
Extract from conversation context:
  FIX_MODE     = audit_file | story_id | epic_id
  AUDIT_FILE   = path to audit file (already resolved by /fix-story command)
  DRY_RUN      = true | false
  AUTO_ONLY    = true | false
  FINDING_FILTER = F-NNN | "all"
```

VERIFY: All 5 markers are non-null. If any marker is missing, HALT and use AskUserQuestion to request it.
```
IF FIX_MODE is null OR AUDIT_FILE is null:
    HALT: AskUserQuestion — "Missing context markers. Was this invoked via /fix-story?"
```

RECORD:
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=remediation --phase=00 --step=markers
```

---

### Step 2: Load Audit File + Parse Findings

EXECUTE: Read the audit file and extract all findings from the "## 4. Findings Detail" section.
```
audit_content = Read(file_path=AUDIT_FILE)

Parse findings from "## 4. Findings Detail" section.
Each finding is a table with fields:
  - Finding ID (e.g., F-001)
  - Severity (CRITICAL | HIGH | MEDIUM | LOW)
  - Type (e.g., quality/broken_file_reference)
  - Affected (comma-separated story/epic IDs)
  - Phase (audit phase that detected it)
  - Summary (description of issue)
  - Evidence (proof of issue with file/line references)
  - Remediation (fix instructions)
  - Verification (how to confirm fix worked)
```

VERIFY: Confirm the findings section exists and at least one finding was parsed.
```
Grep(pattern="## 4. Findings Detail", path=AUDIT_FILE)
# Must return a match

IF findings_count == 0:
    HALT: "No findings found in audit file. Nothing to remediate."
```

RECORD:
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=remediation --phase=00 --step=audit-load
```

Display: "**{N} findings loaded** from audit file"

---

### Step 3: Load Reference File — fix-actions-catalog.md

EXECUTE: Load the fix actions catalog for classification procedures.
```
Read(file_path="references/fix-actions-catalog.md")
```
This file is relative to the skill directory. Use the full path:
```
Read(file_path="{SKILL_DIR}/references/fix-actions-catalog.md")
```
Where SKILL_DIR is the directory containing this skill's SKILL.md.

VERIFY: Content loaded and contains the "Classification Matrix" heading.
```
Grep(pattern="## Classification Matrix", path="{SKILL_DIR}/references/fix-actions-catalog.md")
# Must return a match
```

RECORD: Checkpoint write — reference loaded.

---

### Step 4: Apply Finding Filter

EXECUTE: If FINDING_FILTER is not "all", narrow the findings list to the specified finding ID.
```
IF FINDING_FILTER != "all":
    findings = [f for f in findings if f.finding_id == FINDING_FILTER]

    IF findings is empty:
        HALT: "Finding {FINDING_FILTER} not found in audit file."
        AskUserQuestion:
            Question: "Finding {FINDING_FILTER} was not found. Available findings: {list}. Which finding?"
            Header: "Finding"
            Options:
                - label: "Show all findings"
                  description: "Process all findings instead of a specific one"
                - label: "Enter different finding ID"
                  description: "Specify a different F-NNN identifier"
```

VERIFY: If filter applied, filtered list is non-empty. If filter is "all", all findings remain.
```
Display: "Filter: {FINDING_FILTER} — {len(findings)} findings in scope"
```

RECORD: Checkpoint write — filter state recorded.

---

### Step 5: Resume Detection

EXECUTE: Check if the audit file contains a previous fix session record, indicating a resumed session.
```
IF audit_content contains "## 9. Fix Session":
    Parse previously fixed finding IDs from fix session records.
    For each finding ID in session records:
        Mark that finding as "previously_fixed" in the findings list.

    Display: "Resuming: {K} findings already fixed in prior session"
ELSE:
    Display: "New session — no prior fix records found"
```

VERIFY: Previously fixed findings are correctly identified and marked.
```
Grep(pattern="## 9. Fix Session", path=AUDIT_FILE)
# Match = resuming, No match = new session
```

RECORD: Write initial checkpoint file with full findings state.
```
Write checkpoint to: devforgeai/temp/.remediation-checkpoint-${SESSION_ID}.yaml

Content (see references/checkpoint-schema.md for full schema):
  session_id: ${SESSION_ID}
  timestamp: {current_timestamp}
  audit_file: ${AUDIT_FILE}
  mode:
    dry_run: ${DRY_RUN}
    auto_only: ${AUTO_ONLY}
    finding_filter: ${FINDING_FILTER}
  current_phase: 0
  findings: [{finding_id, severity, type, classification: "pending", status: "pending", ...}]
  phase_completion:
    phase_00: true
    phase_01: false
    phase_02: false
    phase_03: false
    phase_04: false
    phase_05: false
```

Display final summary: "**{N} findings loaded** ({M} new, {K} previously fixed)"

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=remediation --phase=00 --checkpoint-passed
# Exit 0: proceed to Phase 01 | Exit 1: phase incomplete
```
