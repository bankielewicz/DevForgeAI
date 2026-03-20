# Phase 05: Status Update

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --from=04 --to=05
```

## Contract

PURPOSE: Update story status and workflow history after skill invocation. Record timestamps, phase results, and checkpoint markers. Story Management mode only.
REQUIRED SUBAGENTS: (none)
REQUIRED ARTIFACTS: Story file updated with new status and history entry
STEP COUNT: 4 mandatory steps

---

## Mandatory Steps

### Step 1: Determine New Status

EXECUTE: Based on skill result from Phase 04, determine the new story status.
```
IF skill_result.status == "success":
  IF target_skill == "spec-driven-architecture":
    new_status = "Ready for Dev"
  ELSE IF target_skill == "spec-driven-dev":
    new_status = "Dev Complete"
  ELSE IF target_skill == "spec-driven-qa":
    new_status = "QA Approved"
  ELSE IF target_skill == "spec-driven-release":
    new_status = "Released"

ELSE IF skill_result.status == "failed":
  IF target_skill == "spec-driven-qa":
    new_status = "QA Failed"
  ELSE:
    new_status = current_status  # No change on failure
    Display: "Skill failed - status unchanged at: {current_status}"
```

VERIFY: new_status is determined and is a valid workflow state.
```
IF new_status is empty: HALT -- "Could not determine new status after {target_skill} execution."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=05 --step=1`

### Step 2: Update Story Status Field

EXECUTE: Edit the story file to update the status field in YAML frontmatter.
```
story_files = Glob(pattern="devforgeai/specs/Stories/${STORY_ID}*.story.md")
Read(file_path=story_files[0])

Edit(file_path=story_files[0],
  old_string="status: {current_status}",
  new_string="status: {new_status}")

# If releasing to Released, add completed_date
IF new_status == "Released":
  Edit(file_path=story_files[0],
    old_string="status: Released",
    new_string="status: Released\ncompleted_date: {YYYY-MM-DD}")
```

VERIFY: Story status field updated.
```
Grep(pattern="^status: {new_status}", path=story_files[0])
IF no match: HALT -- "Status update failed. Expected: {new_status}"
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=05 --step=2`

### Step 3: Add Workflow History Entry

EXECUTE: Append a timestamped entry to the Status History section.
```
history_entry = "- [{YYYY-MM-DD HH:MM}] Status: {current_status} -> {new_status} (via {target_skill})"

# Add checkpoint marker if applicable
IF new_status == "Dev Complete":
  history_entry += "\n  Checkpoint: DEV_COMPLETE"
ELSE IF new_status == "QA Approved":
  history_entry += "\n  Checkpoint: QA_APPROVED"
ELSE IF new_status == "Released":
  history_entry += "\n  Checkpoint: PRODUCTION_COMPLETE"

# Append to Status History section
Grep(pattern="## Status History", path=story_files[0])
IF found:
  # Append after last history entry
  Edit(file_path=story_files[0],
    old_string="## Status History",
    new_string="## Status History\n{history_entry}")
ELSE:
  # Create Status History section if missing
  Edit(file_path=story_files[0],
    old_string="---\n\n",
    new_string="---\n\n## Status History\n{history_entry}\n\n")
```

VERIFY: History entry is present in story file.
```
Grep(pattern="Status:.*{current_status}.*->.*{new_status}", path=story_files[0])
IF no match: Display "Warning: History entry format may differ, but status was updated."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=05 --step=3`

### Step 4: Record Checkpoint

EXECUTE: If a checkpoint was reached, record it for resume functionality.
```
IF new_status in ["Dev Complete", "QA Approved", "Released"]:
  checkpoint_name = status_to_checkpoint[new_status]
  Display: "Checkpoint recorded: {checkpoint_name}"
```

VERIFY: Checkpoint marker exists in story file (if applicable).
```
IF checkpoint expected:
  Grep(pattern="Checkpoint: {checkpoint_name}", path=story_files[0])
  IF no match: Display "Warning: Checkpoint marker not found, but status updated."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=05 --step=4`

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=05 --checkpoint-passed
```
