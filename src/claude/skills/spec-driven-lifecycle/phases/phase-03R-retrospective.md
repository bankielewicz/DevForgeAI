# Phase 03R: Sprint Retrospective

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --from=01 --to=03R
```

## Contract

PURPOSE: Execute sprint retrospective workflow including technical debt analysis, sprint metrics collection, and debt reduction recommendations. Sprint Retrospective mode only. Triggered when last story in sprint reaches "Released" status.
REQUIRED SUBAGENTS: technical-debt-analyzer
REQUIRED ARTIFACTS: Retrospective report with debt analysis and recommendations
STEP COUNT: 5 mandatory steps

---

## Mandatory Steps

### Step 1: Identify Sprint Stories

EXECUTE: Find all stories in the target sprint.
```
# Identify sprint from context or from last released story
sprint_files = Glob(pattern="devforgeai/specs/Sprints/Sprint-*.md")
IF sprint_files is empty:
  Display: "No sprint files found. Cannot run retrospective."
  HALT -- "No sprints to retrospect."

# Find the most recent sprint or specified sprint
Read(file_path=sprint_files[-1])  # Most recent

# Extract story IDs from sprint
Grep(pattern="STORY-[0-9]+", path=sprint_files[-1])
sprint_stories = extracted_story_ids
retrospective_sprint = sprint_id_from_file

Display: "Sprint: {retrospective_sprint}"
Display: "Stories in sprint: {len(sprint_stories)}"
```

VERIFY: Sprint identified with at least 1 story.
```
IF len(sprint_stories) == 0: HALT -- "No stories found in sprint."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03R --step=1`

### Step 2: Collect Sprint Metrics

EXECUTE: Gather metrics from all sprint stories.
```
sprint_metrics = {
  "total_stories": len(sprint_stories),
  "released": 0,
  "qa_approved": 0,
  "in_progress": 0,
  "total_points": 0,
  "completed_points": 0,
  "deferred_items": 0
}

FOR story_id in sprint_stories:
  story_files = Glob(pattern="devforgeai/specs/Stories/${story_id}*.story.md")
  IF story_files:
    Read(file_path=story_files[0])
    Grep(pattern="^status:", path=story_files[0])
    Grep(pattern="^points:", path=story_files[0])

    sprint_metrics["total_points"] += points
    IF status == "Released":
      sprint_metrics["released"] += 1
      sprint_metrics["completed_points"] += points
    ELSE IF status == "QA Approved":
      sprint_metrics["qa_approved"] += 1

    # Count deferred items
    Grep(pattern="- \\[ \\].*[Dd]efer", path=story_files[0])
    sprint_metrics["deferred_items"] += match_count

velocity = sprint_metrics["completed_points"] / sprint_metrics["total_points"] * 100

Display: "Sprint Velocity: {velocity}% ({completed_points}/{total_points} points)"
```

VERIFY: Metrics collected for all sprint stories.
```
IF sprint_metrics["total_stories"] == 0: HALT -- "No story metrics collected."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03R --step=2`

### Step 3: Invoke Technical Debt Analyzer

EXECUTE: Delegate technical debt analysis to subagent.
```
Task(subagent_type="technical-debt-analyzer",
  prompt="Analyze technical debt for sprint: {retrospective_sprint}
    Stories: {sprint_stories}
    Deferred items found: {sprint_metrics['deferred_items']}

    Tasks:
    1. Analyze all deferred DoD items across sprint stories
    2. Identify debt trends (growing, stable, shrinking)
    3. Detect circular deferral patterns
    4. Calculate debt age (days since deferral)
    5. Recommend debt reduction priorities

    Return:
    - debt_item_count: total deferred items
    - oldest_debt_age: days since oldest deferral
    - circular_chains: list of circular deferral chains
    - recommendations: prioritized list of debt reduction actions
    - debt_trend: growing/stable/shrinking")
```

VERIFY: Technical debt analyzer returned results.
```
IF debt_analysis_result is empty: HALT -- "Technical debt analysis failed."

debt_item_count = debt_analysis_result.debt_item_count
debt_recommendations = debt_analysis_result.recommendations
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03R --step=3 --subagent=technical-debt-analyzer`

### Step 4: Generate Retrospective Report

EXECUTE: Compile retrospective findings into a structured report.
```
Display:
"Sprint Retrospective: {retrospective_sprint}

 Metrics:
   Stories: {total_stories} total, {released} released
   Velocity: {velocity}%
   Points: {completed_points}/{total_points}

 Technical Debt:
   Deferred Items: {debt_item_count}
   Oldest Debt: {oldest_debt_age} days
   Circular Chains: {len(circular_chains)}
   Debt Trend: {debt_trend}

 Recommendations:
 {FOR rec in debt_recommendations:}
   - {rec}
 {END FOR}"
```

VERIFY: Report generated with all sections.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03R --step=4`

### Step 5: Recommend Debt Reduction Sprint

EXECUTE: If significant debt detected, recommend creating a debt reduction sprint.
```
IF debt_item_count > 5 OR len(circular_chains) > 0:
  Display: "Recommended: Create a debt reduction sprint."
  Display: "Use: /create-sprint 'Debt Reduction Sprint' to address {debt_item_count} deferred items."

  AskUserQuestion:
    Question: "Create a debt reduction sprint with {debt_item_count} deferred items?"
    Header: "Debt Sprint"
    Options:
      - label: "Yes - create debt sprint"
        description: "Auto-create stories for deferred items"
      - label: "Not now"
        description: "Skip debt sprint creation"
    multiSelect: false

ELSE:
  Display: "Technical debt is manageable ({debt_item_count} items). No debt sprint needed."
```

VERIFY: User response captured or debt assessment completed.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03R --step=5`

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=03R --checkpoint-passed
```
