# Phase 08: Finalization

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --from={prev_phase} --to=08
```

## Contract

PURPOSE: Generate completion summary with timeline, metrics, and phase results. Shared across ALL operating modes. This is always the last phase executed.
REQUIRED SUBAGENTS: (none)
REQUIRED ARTIFACTS: Structured summary returned to calling command
STEP COUNT: 4 mandatory steps

---

## Mandatory Steps

### Step 1: Collect Phase Results

EXECUTE: Gather results from all executed phases in this workflow.
```
phase_results = {
  "mode": MODE,
  "phases_executed": PHASE_SEQUENCE,
  "story_id": STORY_ID,
  "start_time": workflow_start_time,
  "end_time": current_time
}

# Mode-specific result collection
IF MODE == "story-management":
  phase_results["story_status"] = current_status
  phase_results["target_skill"] = target_skill
  phase_results["skill_result"] = skill_result.status
  phase_results["qa_retry_outcome"] = qa_retry_outcome
  phase_results["checkpoint"] = checkpoint_status

ELSE IF MODE == "sprint-planning":
  phase_results["sprint_name"] = SPRINT_NAME
  phase_results["stories_count"] = len(SELECTED_STORIES)
  phase_results["total_points"] = sprint_total_points
  phase_results["sprint_file"] = sprint_file_path

ELSE IF MODE == "audit-deferrals":
  phase_results["stories_audited"] = audit_story_count
  phase_results["deferrals_found"] = deferral_count
  phase_results["violations"] = violation_summary
  phase_results["report_path"] = audit_report_path

ELSE IF MODE == "retrospective":
  phase_results["sprint_name"] = retrospective_sprint
  phase_results["debt_items"] = debt_item_count
  phase_results["recommendations"] = debt_recommendations
```

VERIFY: phase_results is populated with mode-specific data.
```
IF phase_results["mode"] is empty: HALT -- "Phase results missing mode."
IF phase_results["phases_executed"] is empty: HALT -- "Phase results missing executed phases."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=08 --step=1`

### Step 2: Determine Overall Status

EXECUTE: Compute the overall orchestration status.
```
IF MODE == "story-management":
  IF current_status == "Released":
    overall_status = "success"
    status_message = "Story ${STORY_ID} successfully released"
  ELSE IF qa_retry_outcome == "max_retries_exceeded":
    overall_status = "max_retries"
    status_message = "QA max retries exceeded for ${STORY_ID}"
  ELSE IF skill_result.status == "failed":
    overall_status = "halted"
    status_message = "Workflow halted: {target_skill} failed"
  ELSE:
    overall_status = "success"
    status_message = "Story ${STORY_ID} progressed to: {current_status}"

ELSE IF MODE == "sprint-planning":
  overall_status = "success"
  status_message = "Sprint '{SPRINT_NAME}' created with {stories_count} stories"

ELSE IF MODE == "audit-deferrals":
  IF violation_count > 0:
    overall_status = "findings"
    status_message = "Audit complete: {violation_count} violations found"
  ELSE:
    overall_status = "success"
    status_message = "Audit complete: No violations found"

ELSE IF MODE == "retrospective":
  overall_status = "success"
  status_message = "Sprint retrospective complete"
```

VERIFY: overall_status is one of: success, halted, max_retries, findings, already_released.
```
IF overall_status is empty: HALT -- "Overall status not determined."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=08 --step=2`

### Step 3: Generate Summary

EXECUTE: Build the structured summary for return to the calling command.
```
summary = {
  "status": overall_status,
  "story_id": STORY_ID,
  "mode": MODE,
  "final_status": current_status,
  "summary_message": status_message,
  "phases_executed": len(PHASE_SEQUENCE),
  "duration": end_time - start_time,
  "next_steps": recommendations (from Phase 07 if story mode)
}

# Display formatted summary
Display:
"Lifecycle Orchestration Complete
 Mode: {MODE}
 Status: {overall_status}
 {status_message}

 Phases Executed: {len(PHASE_SEQUENCE)}
 Duration: {duration}"
```

VERIFY: summary object has all required fields.
```
IF summary["status"] is empty: HALT -- "Summary missing status."
IF summary["summary_message"] is empty: HALT -- "Summary missing message."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=08 --step=3`

### Step 4: Return Result to Command

EXECUTE: Return the structured summary to the calling command for display.
```
# The calling command (/orchestrate, /create-sprint, /audit-deferrals)
# receives this summary and displays it to the user.

Display summary (pre-formatted for command display):

IF overall_status == "success" AND MODE == "story-management":
  "Story ${STORY_ID} Orchestration Complete!

   Development: {dev_summary}
   QA: {qa_summary}
   Release: {release_summary}

   Status: {current_status}
   Duration: {duration}"

ELSE IF overall_status == "success" AND MODE == "sprint-planning":
  "Sprint '${SPRINT_NAME}' Created!

   Stories: {stories_count}
   Total Points: {total_points}
   Sprint File: {sprint_file_path}

   Next: Run /dev STORY-ID for each story"

ELSE IF MODE == "audit-deferrals":
  "Deferral Audit Complete

   Stories Audited: {stories_audited}
   Deferrals Found: {deferral_count}
   Violations: {violation_count}
   Report: {audit_report_path}"
```

VERIFY: Summary displayed to conversation.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=08 --step=4`

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=08 --checkpoint-passed
```
