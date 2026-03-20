# Phase 06: QA Retry Loop

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --from=05 --to=06
```

## Contract

PURPOSE: Handle QA failures with intelligent retry logic. Maximum 3 retry attempts before escalation. Story Management mode only.
REQUIRED SUBAGENTS: (none - delegates to skills)
REQUIRED ARTIFACTS: QA retry outcome recorded (success, retry, or max_retries_exceeded)
STEP COUNT: 5 mandatory steps

---

## Mandatory Steps

### Step 1: Check If QA Retry Needed

EXECUTE: Determine if QA retry is applicable based on current state.
```
# Re-read story for latest status
story_files = Glob(pattern="devforgeai/specs/Stories/${STORY_ID}*.story.md")
Read(file_path=story_files[0])
Grep(pattern="^status:", path=story_files[0])

IF current_status != "QA Failed":
  qa_retry_needed = false
  Display: "QA retry not needed - status is: {current_status}"
  # Skip remaining steps in this phase
ELSE:
  qa_retry_needed = true
  Display: "QA Failed detected - entering retry logic"
```

VERIFY: qa_retry_needed flag is set.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=06 --step=1`

### Step 2: Count Retry Attempts

EXECUTE: Count previous QA retry attempts from workflow history.
```
IF qa_retry_needed == false: SKIP to Step 5

# Count "QA Failed" entries in Status History
Grep(pattern="QA Failed", path=story_files[0], output_mode="count")
retry_count = count of QA Failed entries

Display: "QA retry attempt: {retry_count + 1} of 3"
```

VERIFY: retry_count is a non-negative integer.
```
IF retry_count >= 3:
  Display: "Maximum QA retries exceeded (3 attempts)"
  qa_retry_outcome = "max_retries_exceeded"
  # Skip to Step 5
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=06 --step=2`

### Step 3: Present Recovery Options

EXECUTE: If retry count < 3, present options to the user.
```
IF qa_retry_outcome == "max_retries_exceeded": SKIP to Step 5

AskUserQuestion:
  Question: "QA validation failed (attempt {retry_count + 1}/3). How should we proceed?"
  Header: "QA Retry"
  Options:
    - label: "Retry (fix and re-validate)"
      description: "Re-invoke spec-driven-dev to fix issues, then re-run QA"
    - label: "Split story"
      description: "Story scope too large - split into smaller stories"
    - label: "HALT"
      description: "Stop orchestration for manual investigation"
  multiSelect: false
```

VERIFY: User response captured.
```
IF user selects "HALT": HALT -- "Orchestration paused by user at QA retry."
IF user selects "Split story":
  Display: "Use /create-story to create smaller stories from this one."
  HALT -- "Orchestration paused - story splitting recommended."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=06 --step=3`

### Step 4: Execute Retry

EXECUTE: If user selected retry, re-invoke spec-driven-dev then spec-driven-qa.
```
IF user selected "Retry":
  # Update status back to "In Development" for fix
  Edit(file_path=story_files[0],
    old_string="status: QA Failed",
    new_string="status: In Development")

  # Add retry history entry
  history_entry = "- [{YYYY-MM-DD HH:MM}] QA Retry #{retry_count + 1}: Re-entering development for fixes"

  # Re-invoke spec-driven-dev
  Display: "Re-invoking spec-driven-dev for fixes..."
  Skill(command="spec-driven-dev")

  # After dev completes, re-invoke spec-driven-qa
  Display: "Re-invoking spec-driven-qa for validation..."
  Skill(command="spec-driven-qa")

  # Check result
  Read(file_path=story_files[0])
  Grep(pattern="^status:", path=story_files[0])

  IF status == "QA Approved":
    qa_retry_outcome = "success"
    Display: "QA retry successful - story is now QA Approved"
  ELSE:
    qa_retry_outcome = "retry_failed"
    Display: "QA retry failed - will check retry count"
    # Loop back to Step 2 for next attempt (up to 3 total)
```

VERIFY: qa_retry_outcome is set.
```
IF qa_retry_outcome is empty: HALT -- "QA retry outcome not determined."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=06 --step=4`

### Step 5: Record Outcome

EXECUTE: Record the final QA retry outcome.
```
IF qa_retry_needed == false:
  qa_retry_outcome = "not_applicable"
  Display: "QA retry: Not applicable"

ELSE IF qa_retry_outcome == "success":
  Display: "QA retry: Success after {retry_count + 1} attempt(s)"

ELSE IF qa_retry_outcome == "max_retries_exceeded":
  Display: "QA retry: FAILED - Maximum retries (3) exceeded"
  Display: "Recommended: Split story into smaller stories or escalate blockers"
```

VERIFY: qa_retry_outcome is one of: not_applicable, success, max_retries_exceeded, retry_failed.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=06 --step=5`

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=06 --checkpoint-passed
```
