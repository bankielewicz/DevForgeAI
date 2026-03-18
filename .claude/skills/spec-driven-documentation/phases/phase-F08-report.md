# Phase F08: Fix Report

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --from=F07 --to=F08 --workflow=doc-fix
# Exit 0: proceed | Exit 1: Phase F07 incomplete
```

## Contract

PURPOSE: Append fix session to doc-audit.json, display completion summary with applied/skipped counts, files modified, and next steps. Finalize fix workflow and EXIT.
REQUIRED SUBAGENTS: (none)
REQUIRED ARTIFACTS: Fix session appended to audit JSON, summary displayed, session finalized
STEP COUNT: 2 mandatory steps

---

## Mandatory Steps

### Step F08.1: Append Fix Session to Audit JSON

EXECUTE: Record this fix session in the audit file for idempotency tracking.
```
audit_content = Read(file_path="devforgeai/qa/audit/doc-audit.json")
audit_data = parse_json(audit_content)

applied_count = len([d for d in fix_details if d["status"] == "applied"])
skipped_count = len([d for d in fix_details if d["status"] == "skipped"])

fix_session = {
    "session_id": SESSION_ID,
    "timestamp": current_timestamp,
    "type_filter": $DOC_TYPE if $DOC_TYPE != "all" else "all",
    "finding_filter": $FINDING_FILTER,
    "findings_processed": len(fix_details),
    "automated_applied": len([d for d in fix_details if d["status"] == "applied" and d["id"] in [f["id"] for f in automated_findings]]),
    "interactive_applied": len([d for d in fix_details if d["status"] == "applied" and d["id"] in [f["id"] for f in interactive_findings]]),
    "skipped": skipped_count,
    "details": fix_details
}

audit_data["fix_sessions"].append(fix_session)

Write(file_path="devforgeai/qa/audit/doc-audit.json", content=JSON(audit_data, indent=2))

Display: "Fix session appended to doc-audit.json"
```
VERIFY: Audit JSON updated with new fix_sessions entry.
```
result = Read(file_path="devforgeai/qa/audit/doc-audit.json")
IF SESSION_ID not in result: HALT -- "Fix session not found in audit JSON after write"
```
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=F08 --step=F08.1 --workflow=doc-fix`

---

### Step F08.2: Display Summary and Finalize

EXECUTE: Display the completion report and finalize the session.
```
Display: ""
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: "  Documentation Fix Complete"
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: ""
Display: "Session: {SESSION_ID}"
Display: ""
Display: "Applied: {applied_count} fixes"
Display: "Skipped: {skipped_count} fixes (user deferred)"

# Calculate remaining
total_findings = len(audit_data["findings"])
total_applied_all_sessions = 0
FOR each session in audit_data["fix_sessions"]:
    total_applied_all_sessions += len([d for d in session["details"] if d["status"] == "applied"])

remaining = total_findings - total_applied_all_sessions
Display: "Remaining: {remaining} findings not yet addressed"
Display: ""

IF files_created:
    Display: "Files created:"
    FOR each f in files_created:
        Display: "  + {f}"

IF files_modified:
    Display: "Files modified:"
    FOR each f in files_modified:
        Display: "  ~ {f}"

Display: ""
Display: "Next Steps:"
Display: "  - Review changes before committing"
Display: "  - Run /document --audit=dryrun to re-score"
Display: "  - Commit with: git add ... && git commit"
Display: ""
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Finalize session checkpoint
checkpoint = Read(file_path="devforgeai/workflows/${SESSION_ID}-checkpoint.json")
checkpoint.current_phase = "COMPLETE"
checkpoint.completed_at = current_timestamp
checkpoint.phases_completed.append("F08")
checkpoint.result = "SUCCESS"
checkpoint.applied_count = applied_count
checkpoint.skipped_count = skipped_count

Write(file_path="devforgeai/workflows/${SESSION_ID}-checkpoint.json", content=JSON(checkpoint))

# Validate all fix phases completed
completed_count = len(checkpoint.phases_completed)
EXPECTED_COUNT = 8  # 01, 02, F03-F08

IF completed_count < EXPECTED_COUNT:
    Display: "WARNING: Only {completed_count}/{EXPECTED_COUNT} phases completed"
ELSE:
    Display: "All {EXPECTED_COUNT} phases completed - Fix workflow passed"
```
VERIFY: Summary displayed. Checkpoint shows result = "SUCCESS".
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=F08 --step=F08.2 --workflow=doc-fix`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --phase=F08 --checkpoint-passed --workflow=doc-fix
```

## Phase Transition Display

```
Display: ""
Display: "Fix workflow complete. EXIT."
Display: ""
```

**EXIT after this phase. Do not proceed to any generation or audit phases.**
