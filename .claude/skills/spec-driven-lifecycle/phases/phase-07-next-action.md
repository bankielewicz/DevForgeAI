# Phase 07: Next Action Determination

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --from=06 --to=07
```

## Contract

PURPOSE: Analyze current workflow state and recommend next steps. Provide actionable guidance based on story status and orchestration results. Story Management mode only.
REQUIRED SUBAGENTS: (none)
REQUIRED ARTIFACTS: Next action recommendations generated
STEP COUNT: 3 mandatory steps

---

## Mandatory Steps

### Step 1: Analyze Current State

EXECUTE: Read story file and assess current position in the workflow.
```
story_files = Glob(pattern="devforgeai/specs/Stories/${STORY_ID}*.story.md")
Read(file_path=story_files[0])

# Extract current status
Grep(pattern="^status:", path=story_files[0])

# Check for deferred items
Grep(pattern="- \\[ \\].*[Dd]efer", path=story_files[0])
has_deferrals = (match count > 0)

# Check for QA retry outcome
IF qa_retry_outcome == "max_retries_exceeded":
  workflow_state = "blocked"
ELSE IF current_status == "Released":
  workflow_state = "complete"
ELSE IF current_status == "QA Approved":
  workflow_state = "ready_for_release"
ELSE IF current_status == "Dev Complete":
  workflow_state = "ready_for_qa"
ELSE IF current_status == "Ready for Dev":
  workflow_state = "ready_for_dev"
ELSE:
  workflow_state = "in_progress"
```

VERIFY: workflow_state is determined.
```
IF workflow_state is empty: HALT -- "Could not determine workflow state."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=07 --step=1`

### Step 2: Generate Recommendations

EXECUTE: Based on workflow state, generate specific next-action recommendations.
```
recommendations = []

IF workflow_state == "complete":
  recommendations = [
    "Story ${STORY_ID} is Released - no further action needed.",
    "Monitor production metrics for 24 hours.",
    "Consider running /audit-deferrals to check for outstanding work.",
    "If this was the last story in the sprint, run sprint retrospective."
  ]

ELSE IF workflow_state == "ready_for_release":
  recommendations = [
    "Run: /release ${STORY_ID} (defaults to test environment)",
    "Or: /orchestrate ${STORY_ID} to continue full lifecycle",
    "Review QA report before release: devforgeai/qa/reports/${STORY_ID}-qa-report.md"
  ]

ELSE IF workflow_state == "ready_for_qa":
  recommendations = [
    "Run: /qa ${STORY_ID} (deep mode validation)",
    "Or: /orchestrate ${STORY_ID} to continue full lifecycle"
  ]

ELSE IF workflow_state == "ready_for_dev":
  recommendations = [
    "Run: /dev ${STORY_ID} (TDD implementation)",
    "Or: /orchestrate ${STORY_ID} for full lifecycle"
  ]

ELSE IF workflow_state == "blocked":
  recommendations = [
    "Story blocked after 3 QA retry attempts.",
    "Option 1: Split into smaller stories with /create-story",
    "Option 2: Run /rca ${STORY_ID} for root cause analysis",
    "Option 3: Review and address QA findings manually"
  ]

ELSE IF workflow_state == "in_progress":
  recommendations = [
    "Story is in progress (status: {current_status}).",
    "Resume with: /orchestrate ${STORY_ID} (auto-detects checkpoint)",
    "Or run the specific command for current phase"
  ]

IF has_deferrals:
  recommendations.append("Note: Story has deferred items. Run /audit-deferrals to review.")
```

VERIFY: recommendations list is non-empty.
```
IF len(recommendations) == 0: HALT -- "No recommendations generated."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=07 --step=2`

### Step 3: Display Recommendations

EXECUTE: Format and display the recommendations to the user.
```
Display:
"Next Steps for ${STORY_ID}:
 Status: {current_status}
 Workflow State: {workflow_state}

 Recommendations:
 {FOR rec in recommendations:}
   - {rec}
 {END FOR}"
```

VERIFY: Recommendations displayed.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=07 --step=3`

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=07 --checkpoint-passed
```
