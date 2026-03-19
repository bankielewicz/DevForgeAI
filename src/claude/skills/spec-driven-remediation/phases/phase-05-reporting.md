# Phase 05: Fix Report + Session Record

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=remediation --from=04 --to=05
# Exit 0: proceed | Exit 1: Phase 04 incomplete
# Note: If dry run, this may follow Phase 02 directly (Phases 03-04 skipped)
```

## Contract

PURPOSE: Generate the fix report, display to user, and append session record to audit file for resume capability.
REQUIRED SUBAGENTS: None
REQUIRED ARTIFACTS: Fix report displayed, session record appended to audit file
STEP COUNT: 3 mandatory steps

---

## Mandatory Steps

### Step 1: Load Report Template

EXECUTE: Load the fix report template fresh.
```
Read(file_path="{SKILL_DIR}/assets/templates/fix-report-template.md")
```

VERIFY: Template content loaded.
```
ASSERT template content is non-empty
ASSERT template contains "Fix Session Report" heading
```

RECORD: Template load confirmed.

---

### Step 2: Generate and Display Report

EXECUTE: Calculate summary counts from the findings list and populate the report template.
```
count_auto_applied        = count findings WHERE classification == "automated" AND status == "applied" AND verification == "passed"
count_interactive_applied = count findings WHERE classification == "interactive" AND status == "applied" AND verification == "passed"
count_deferred            = count findings WHERE status == "deferred"
count_skipped             = count findings WHERE status == "skipped"
count_failed              = count findings WHERE verification == "failed"
count_previously_fixed    = count findings WHERE status == "previously_fixed"

mode_label = "Dry Run" if DRY_RUN else ("Auto Only" if AUTO_ONLY else "Full")

Display the report:

## Fix Session Report

**Audit Source:** {AUDIT_FILE}
**Session Date:** {current_date}
**Mode:** {mode_label}

### Results Summary

| Outcome | Count |
|---------|-------|
| Applied (automated) | {count_auto_applied} |
| Applied (interactive) | {count_interactive_applied} |
| Deferred | {count_deferred} |
| Skipped | {count_skipped} |
| Failed verification | {count_failed} |
| Previously fixed | {count_previously_fixed} |

### Applied Fixes

{FOR each finding WHERE status == "applied" AND verification == "passed":}
- [x] {finding_id} ({type}): {change_summary} -- verified

### Deferred Items

{FOR each finding WHERE status == "deferred":}
- [ ] {finding_id} ({severity}): {reason}

### Remaining Findings

{FOR each finding WHERE status == "pending" OR status == "skipped":}
- {finding_id} ({severity}): {summary}

### Next Steps

{IF all findings resolved: "All findings resolved. Run `/validate-stories` to confirm clean audit."}
{IF remaining findings: "Re-run `/fix-story` to address remaining findings."}
{IF deferred items: "Address deferred items in a future session."}
```

VERIFY: Report displayed contains all required sections (Results Summary, Applied Fixes, Deferred Items, Remaining Findings, Next Steps).
```
ASSERT report contains "Results Summary"
ASSERT report contains "Applied Fixes"
ASSERT report contains "Next Steps"
ASSERT total of all counts == total findings
```

RECORD:
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=remediation --phase=05 --step=report
```

---

### Step 3: Append Session Record to Audit File

EXECUTE: If this is not a dry run and the audit file exists, append a fix session record to enable resume detection on re-run.
```
IF AUDIT_FILE exists AND DRY_RUN == false:

    session_record = """

## 9. Fix Session: {current_date}

**Applied:** {count_applied} | **Deferred:** {count_deferred} | **Skipped:** {count_skipped}

| Finding | Status | Verification |
|---------|--------|-------------|
{FOR each finding:}
| {finding_id} | {status} | {verification_status} |

"""

    # Read current audit file content
    current_content = Read(file_path=AUDIT_FILE)

    # Check if a "## 9. Fix Session" section already exists
    IF current_content contains "## 9. Fix Session":
        # Append as additional session (don't overwrite previous sessions)
        # Find the end of the file and append
        Edit(
            file_path = AUDIT_FILE,
            old_string = {last_line_of_file},
            new_string = {last_line_of_file + session_record}
        )
    ELSE:
        # First session — append at end of file
        Edit(
            file_path = AUDIT_FILE,
            old_string = {last_line_of_file},
            new_string = {last_line_of_file + session_record}
        )

ELIF DRY_RUN == true:
    Display: "Dry run — no session record appended to audit file."
```

VERIFY: If not dry run, confirm the session record was appended.
```
IF DRY_RUN == false:
    Grep(pattern="## 9. Fix Session: {current_date}", path=AUDIT_FILE)
    # Must return a match
ELSE:
    # Dry run — no verification needed for audit file
    Display: "Dry run verified — no files modified."
```

RECORD: Final phase completion.
```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=remediation --phase=05 --checkpoint-passed
```

Update checkpoint as final state:
```
Update checkpoint:
  current_phase: 5
  phase_completion:
    phase_00: true
    phase_01: true
    phase_02: true
    phase_03: true    # or skipped if dry run
    phase_04: true    # or skipped if dry run
    phase_05: true
  status: "completed"
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=remediation --phase=05 --checkpoint-passed
# Exit 0: workflow complete | Exit 1: phase incomplete
```

Display final status:
```
"All 6 phases completed — Remediation workflow passed"
```
