# Phase 03S: Sprint Planning

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --from=01 --to=03S
```

## Contract

PURPOSE: Execute complete sprint planning workflow including story validation, capacity calculation, sprint document creation, and story status updates. Sprint Planning mode only.
REQUIRED SUBAGENTS: sprint-planner
REQUIRED ARTIFACTS: Sprint file created, stories updated to "Ready for Dev"
STEP COUNT: 6 mandatory steps

---

## Mandatory Steps

### Step 1: Sprint Number Discovery

EXECUTE: Calculate next sprint number from existing sprint files.
```
existing_sprints = Glob(pattern="devforgeai/specs/Sprints/Sprint-*.md")
IF existing_sprints is empty:
  next_sprint_number = 1
ELSE:
  # Extract highest sprint number
  FOR sprint_file in existing_sprints:
    Grep(pattern="Sprint-([0-9]+)", path=sprint_file)
  next_sprint_number = max_number + 1

sprint_id = "Sprint-{next_sprint_number}"
Display: "Next sprint: {sprint_id}"
```

VERIFY: sprint_id is set and follows Sprint-N format.
```
IF sprint_id is empty: HALT -- "Could not determine next sprint number."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03S --step=1`

### Step 2: Validate Selected Stories

EXECUTE: Verify all selected stories exist and are in "Backlog" status.
```
selected_ids = parse SELECTED_STORIES (comma-separated)
valid_stories = []
invalid_stories = []

FOR story_id in selected_ids:
  story_files = Glob(pattern="devforgeai/specs/Stories/${story_id}*.story.md")
  IF story_files is empty:
    invalid_stories.append("{story_id}: File not found")
    CONTINUE

  Read(file_path=story_files[0])
  Grep(pattern="^status:", path=story_files[0])

  IF status != "Backlog":
    invalid_stories.append("{story_id}: Status is '{status}', expected 'Backlog'")
  ELSE:
    valid_stories.append(story_id)
```

VERIFY: At least 1 valid story. Report any invalid stories.
```
IF len(invalid_stories) > 0:
  Display: "Invalid stories: {invalid_stories}"
  AskUserQuestion:
    Question: "{len(invalid_stories)} stories are invalid. Continue with {len(valid_stories)} valid stories?"
    Header: "Invalid Stories"
    Options:
      - label: "Continue with valid stories"
        description: "Create sprint with {len(valid_stories)} stories"
      - label: "HALT"
        description: "Fix invalid stories first"
    multiSelect: false

IF len(valid_stories) == 0: HALT -- "No valid stories for sprint."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03S --step=2`

### Step 3: Calculate Capacity

EXECUTE: Sum story points for valid stories and check against 20-40 point range.
```
total_points = 0
FOR story_id in valid_stories:
  story_files = Glob(pattern="devforgeai/specs/Stories/${story_id}*.story.md")
  Read(file_path=story_files[0])
  Grep(pattern="^points:", path=story_files[0])
  total_points += extracted_points

Display: "Total capacity: {total_points} points (target: 20-40)"
```

VERIFY: Capacity is within acceptable range or user approves deviation.
```
IF total_points > 40:
  AskUserQuestion:
    Question: "Sprint over capacity ({total_points} pts, max 40). Proceed?"
    Header: "Capacity"
    Options:
      - label: "Proceed anyway"
        description: "Accept over-capacity sprint"
      - label: "Remove lowest priority"
        description: "Auto-remove stories to fit capacity"
    multiSelect: false

IF total_points < 20:
  AskUserQuestion:
    Question: "Sprint under capacity ({total_points} pts, min 20). Proceed?"
    Header: "Capacity"
    Options:
      - label: "Proceed anyway"
        description: "Accept under-capacity sprint"
      - label: "Add more stories"
        description: "Show available Backlog stories"
    multiSelect: false
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03S --step=3`

### Step 4: Invoke Sprint-Planner Subagent

EXECUTE: Delegate sprint document creation to sprint-planner subagent.
```
Task(subagent_type="sprint-planner",
  prompt="Create sprint document for {sprint_id}.
    Sprint Name: {SPRINT_NAME}
    Stories: {valid_stories}
    Total Points: {total_points}
    Duration: {DURATION} days
    Start Date: {START_DATE}
    Epic: {EPIC_ID}
    Template: Read assets/templates/sprint-template.md
    Output: Write to devforgeai/specs/Sprints/{sprint_id}.md")
```

VERIFY: Sprint file created.
```
Glob(pattern="devforgeai/specs/Sprints/{sprint_id}.md")
IF not found: HALT -- "Sprint file not created by sprint-planner."

Read(file_path="devforgeai/specs/Sprints/{sprint_id}.md")
# Verify it contains expected content
Grep(pattern="Sprint Name:", path="devforgeai/specs/Sprints/{sprint_id}.md")
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03S --step=4 --subagent=sprint-planner`

### Step 5: Update Story Statuses

EXECUTE: Update all valid stories to "Ready for Dev" and add sprint reference.
```
FOR story_id in valid_stories:
  story_files = Glob(pattern="devforgeai/specs/Stories/${story_id}*.story.md")

  # Update status
  Edit(file_path=story_files[0],
    old_string="status: Backlog",
    new_string="status: Ready for Dev")

  # Add sprint reference if not present
  Grep(pattern="^sprint:", path=story_files[0])
  IF not found:
    Edit(file_path=story_files[0],
      old_string="status: Ready for Dev",
      new_string="status: Ready for Dev\nsprint: {sprint_id}")
  ELSE:
    Edit(file_path=story_files[0],
      old_string="sprint: .*",
      new_string="sprint: {sprint_id}")
```

VERIFY: All stories updated.
```
FOR story_id in valid_stories:
  story_files = Glob(pattern="devforgeai/specs/Stories/${story_id}*.story.md")
  Grep(pattern="^status: Ready for Dev", path=story_files[0])
  IF no match: Display "Warning: {story_id} status update may have failed"
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03S --step=5`

### Step 6: Generate Sprint Summary

EXECUTE: Build summary for return to calling command.
```
sprint_summary = {
  "sprint_id": sprint_id,
  "sprint_name": SPRINT_NAME,
  "stories": valid_stories,
  "total_points": total_points,
  "duration": DURATION,
  "start_date": START_DATE,
  "epic": EPIC_ID,
  "file": "devforgeai/specs/Sprints/{sprint_id}.md"
}

Display:
"Sprint Created: {sprint_id}
 Name: {SPRINT_NAME}
 Stories: {len(valid_stories)}
 Points: {total_points}
 Duration: {DURATION} days
 File: devforgeai/specs/Sprints/{sprint_id}.md"
```

VERIFY: sprint_summary has all required fields.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03S --step=6`

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=03S --checkpoint-passed
```
