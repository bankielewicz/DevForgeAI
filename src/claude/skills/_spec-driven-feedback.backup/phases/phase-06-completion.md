# Phase 06: Completion & Display

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=feedback --from=05 --to=06 --project-root=.
```

| Exit Code | Action |
|-----------|--------|
| 0 | Prerequisites met. Proceed. |
| 1 | Phase 05 incomplete. HALT. |
| 2 | Validation error. HALT. |
| 127 | CLI not installed. Proceed without enforcement. |

---

## Contract

- **PURPOSE:** Generate completion summary, finalize checkpoint, display results to user
- **REQUIRED SUBAGENTS:** none
- **REQUIRED ARTIFACTS:** Completion summary displayed, checkpoint status = "complete"
- **STEP COUNT:** 3
- **REFERENCE FILES:** none (all data already captured in previous phases)

---

## Reference Loading

No additional reference loading needed for this phase. All data is in the checkpoint.

---

## Mandatory Steps (3)

### Step 6.1: Generate Completion Summary

**EXECUTE:**
```
Build completion summary based on feedback type:

SWITCH $FEEDBACK_TYPE:
  CASE "conversation":
    summary = {
      feedback_id: SESSION_ID,
      type: "Conversation Feedback",
      file: output.feedback_file_path,
      questions_asked: phases["03"].questions_asked,
      questions_answered: phases["03"].questions_answered,
      next_steps: [
        "Review feedback at: ${output.feedback_file_path}",
        "Search feedback: /feedback-search ${OPERATION_CONTEXT.story_id}",
        "View trends: /feedback-search --severity=high"
      ]
    }

  CASE "summary":
    summary = {
      feedback_id: SESSION_ID,
      type: "Operation Summary",
      file: output.feedback_file_path,
      next_steps: [
        "Review summary at: ${output.feedback_file_path}",
        "Export: /feedback-export-data --format=markdown"
      ]
    }

  CASE "metrics":
    summary = {
      feedback_id: SESSION_ID,
      type: "Metrics Collection",
      file: output.feedback_file_path,
      next_steps: [
        "Review metrics at: ${output.feedback_file_path}",
        "Export: /feedback-export-data --format=json"
      ]
    }

  CASE "checklist":
    summary = {
      feedback_id: SESSION_ID,
      type: "Sprint Retrospective",
      file: output.feedback_file_path,
      completion: "${completion_percentage}%",
      next_steps: [
        "Review checklist at: ${output.feedback_file_path}",
        "Plan improvements based on unchecked items"
      ]
    }

  CASE "ai_analysis":
    summary = {
      feedback_id: SESSION_ID,
      type: "AI Analysis",
      file: output.feedback_file_path,
      recommendations: filtered_recommendations.length,
      high_priority_queued: high_priority_recs.length,
      next_steps: [
        "Review analysis at: ${output.feedback_file_path}",
        IF high_priority_recs.length > 0:
          "Triage recommendations: /recommendations-triage"
        ELSE:
          "No HIGH priority recommendations queued"
      ]
    }

  CASE "triage":
    summary = {
      feedback_id: SESSION_ID,
      type: "Recommendation Triage",
      stories_created: output.stories_created,
      recommendations_triaged: output.recommendations_triaged,
      next_steps: [
        FOR each story_id in output.stories_created:
          "Implement: /dev ${story_id}",
        "Remaining recommendations: /recommendations-triage"
      ]
    }

  CASE "config":
    summary = {
      feedback_id: SESSION_ID,
      type: "Configuration ${SUBCOMMAND}",
      next_steps: ["Configuration operation completed"]
    }

  CASE "search":
    summary = {
      feedback_id: SESSION_ID,
      type: "Feedback Search",
      next_steps: ["Search results displayed above"]
    }

  CASE "export":
    summary = {
      feedback_id: SESSION_ID,
      type: "Feedback Export",
      file: output.feedback_file_path,
      next_steps: ["Export file created at: ${output.feedback_file_path}"]
    }

  CASE "import":
    summary = {
      feedback_id: SESSION_ID,
      type: "Feedback Import",
      next_steps: ["Import completed. Run /feedback-reindex to rebuild index."]
    }
```

**VERIFY:** Summary contains `feedback_id` and `type` fields.
```
IF summary.feedback_id is null: HALT -- "Completion summary missing feedback_id"
IF summary.type is null: HALT -- "Completion summary missing type"
```

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=06 --step=6.1 --project-root=.
```
Update checkpoint:
```
checkpoint.phases["06"].summary_generated = true
checkpoint.phases["06"].steps_completed.append("6.1")
```

---

### Step 6.2: Finalize Checkpoint

**EXECUTE:**
```
checkpoint.status = "complete"
checkpoint.updated_at = current ISO 8601
checkpoint.phases["06"].status = "completed"
checkpoint.phases["06"].checkpoint_finalized = true
checkpoint.progress.current_phase = 7  # Beyond final phase
checkpoint.progress.phases_completed.append("06")
checkpoint.progress.total_steps_completed = sum(all steps_completed arrays)

Write(file_path="devforgeai/feedback/checkpoints/${SESSION_ID}.checkpoint.json", content=checkpoint)
```

**VERIFY:**
```
Read(file_path="devforgeai/feedback/checkpoints/${SESSION_ID}.checkpoint.json")
IF content does NOT contain '"status": "complete"': HALT -- "Checkpoint was NOT finalized"
```

**RECORD:**
```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=feedback --phase=06 --checkpoint-passed --project-root=.
```
Update checkpoint:
```
checkpoint.phases["06"].steps_completed.append("6.2")
```

---

### Step 6.3: Display Results

**EXECUTE:**
```
Display formatted completion summary:

"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DevForgeAI Feedback Complete ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Session: ${SESSION_ID}
  Type: ${summary.type}
  ${IF summary.file: "File: ${summary.file}"}
  ${IF summary.questions_answered: "Questions: ${summary.questions_answered}/${summary.questions_asked}"}
  ${IF summary.stories_created: "Stories Created: ${summary.stories_created.length}"}
  ${IF summary.recommendations: "Recommendations: ${summary.recommendations}"}
  ${IF summary.completion: "Completion: ${summary.completion}"}

  Phases: 6/6 ✓
  Steps: ${total_steps_completed}

  Next Steps:
  ${FOR each step in summary.next_steps: "  → ${step}"}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

**VERIFY:** Results displayed to user (non-blocking — display is best-effort).

**RECORD:**
```
checkpoint.phases["06"].results_displayed = true
checkpoint.phases["06"].steps_completed.append("6.3")
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=feedback --phase=06 --checkpoint-passed --project-root=.
```

---

## Exit Verification Checklist

Workflow is COMPLETE when ALL are true:

- [ ] Completion summary generated with feedback_id and type
- [ ] Checkpoint status = "complete"
- [ ] Checkpoint written to disk (verified via Read)
- [ ] Results displayed to user
- [ ] All 6 phases in phases_completed array

**Workflow completion validation:**
```
IF phases_completed.length < 6: HALT "WORKFLOW INCOMPLETE - ${phases_completed.length}/6 phases"
IF output.feedback_id is null: HALT "Feedback ID not generated"
IF checkpoint.status != "complete": HALT "Checkpoint not finalized"
```

---

## Phase Transition Display

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 06: Completion ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Summary: Generated
  Checkpoint: Finalized
  Results: Displayed
  Steps: 3/3

  WORKFLOW COMPLETE ✓
  All 6 phases executed successfully.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
