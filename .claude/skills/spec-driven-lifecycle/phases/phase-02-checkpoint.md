# Phase 02: Checkpoint Detection

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --from=01 --to=02
```

## Contract

PURPOSE: Detect existing workflow checkpoints for resume functionality. Determine starting phase based on previous progress. Story Management mode only.
REQUIRED SUBAGENTS: (none)
REQUIRED ARTIFACTS: Story file with Status History section
STEP COUNT: 4 mandatory steps

---

## Mandatory Steps

### Step 1: Load Story File

EXECUTE: Load the story file for checkpoint scanning.
```
story_files = Glob(pattern="devforgeai/specs/Stories/${STORY_ID}*.story.md")
IF story_files is empty: HALT -- "Story file not found for ${STORY_ID}"

Read(file_path=story_files[0])
```

VERIFY: Story file loaded and contains Status History or Implementation Notes section.
```
Grep(pattern="## (Status History|Implementation Notes)", path=story_files[0])
IF no match: Display "No workflow history found - starting fresh workflow"
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=02 --step=1`

### Step 2: Scan for Checkpoint Markers

EXECUTE: Search story file for checkpoint markers in priority order (most recent progress wins).
```
# Scan for checkpoints in order of most-to-least progressed
Grep(pattern="Checkpoint: PRODUCTION_COMPLETE", path=story_files[0])
Grep(pattern="Checkpoint: STAGING_COMPLETE", path=story_files[0])
Grep(pattern="Checkpoint: QA_APPROVED", path=story_files[0])
Grep(pattern="Checkpoint: DEV_COMPLETE", path=story_files[0])

# Also check story status field
Grep(pattern="^status:", path=story_files[0])
```

VERIFY: checkpoint_status variable is set based on scan results.
```
IF "PRODUCTION_COMPLETE" found:
  checkpoint_status = "PRODUCTION_COMPLETE"
ELSE IF "STAGING_COMPLETE" found:
  checkpoint_status = "STAGING_COMPLETE"
ELSE IF "QA_APPROVED" found:
  checkpoint_status = "QA_APPROVED"
ELSE IF "DEV_COMPLETE" found:
  checkpoint_status = "DEV_COMPLETE"
ELSE:
  checkpoint_status = "NONE"
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=02 --step=2`

### Step 3: Determine Starting Phase

EXECUTE: Map checkpoint to starting phase in the orchestration workflow.
```
IF checkpoint_status == "PRODUCTION_COMPLETE":
  orchestration_result = "ALREADY_RELEASED"
  Display: "Story ${STORY_ID} already released. No further action needed."
  HALT (graceful - return success with already_released status)

ELSE IF checkpoint_status == "STAGING_COMPLETE":
  starting_phase = 05  # Resume at Status Update (post-staging)
  skip_phases = [02, 03, 04]
  Display: "Resuming from Staging Complete checkpoint"

ELSE IF checkpoint_status == "QA_APPROVED":
  starting_phase = 04  # Resume at Skill Invocation (for release)
  skip_phases = [02, 03]
  Display: "Resuming from QA Approved checkpoint"

ELSE IF checkpoint_status == "DEV_COMPLETE":
  starting_phase = 04  # Resume at Skill Invocation (for QA)
  skip_phases = [02, 03]
  Display: "Resuming from Dev Complete checkpoint"

ELSE:
  starting_phase = 03  # Start from Story Validation
  skip_phases = []
  Display: "No checkpoint found - starting from Story Validation"
```

VERIFY: starting_phase and skip_phases are set.
```
IF starting_phase is not set: HALT -- "Could not determine starting phase from checkpoint: {checkpoint_status}"
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=02 --step=3`

### Step 4: Update Phase Sequence

EXECUTE: Modify PHASE_SEQUENCE to skip already-completed phases.
```
# Remove completed phases from sequence
FOR phase in skip_phases:
  Remove phase from PHASE_SEQUENCE

Display:
"Checkpoint: {checkpoint_status}
 Starting Phase: {starting_phase}
 Updated Phase Sequence: {PHASE_SEQUENCE}"
```

VERIFY: PHASE_SEQUENCE reflects checkpoint adjustments.
```
IF PHASE_SEQUENCE is empty: HALT -- "All phases already completed."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=02 --step=4`

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=02 --checkpoint-passed
```
