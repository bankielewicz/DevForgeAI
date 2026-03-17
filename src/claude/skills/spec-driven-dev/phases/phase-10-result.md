# Phase 10: Result Interpretation

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --from=09 --to=10
# Exit 0: proceed | Exit 1: Phase 09 incomplete
```

## Contract

PURPOSE: Generate a structured result summary and return it to the invoking command for display.
REQUIRED SUBAGENTS: dev-result-interpreter
REQUIRED ARTIFACTS: None (returns result object)
STEP COUNT: 4 mandatory steps

---

## Mandatory Steps

### Step 1: Invoke Dev Result Interpreter

EXECUTE: Delegate result interpretation to specialist subagent.
```
Task(
  subagent_type="dev-result-interpreter",
  prompt="Interpret development workflow results for ${STORY_ID}.
  Story file: ${STORY_FILE}

  Task:
  1. Read story file and extract:
     - Current status
     - TDD phases completed
     - Test results (passing count, coverage %)
     - DoD completion status
     - Deferred items (if any)

  2. Determine overall result:
     - SUCCESS: status='Dev Complete', all tests passing
     - INCOMPLETE: status='In Development', some work remaining
     - FAILURE: workflow error

  3. Generate display template appropriate for result type

  4. Provide next step recommendations

  Return structured JSON with:
  - status: 'success|incomplete|failure'
  - display.template: '...' (formatted display text)
  - display.next_steps: [...] (actionable recommendations)
  - story_status: '...'
  - tdd_phases_completed: [...]
  - workflow_summary: '...'"
)
```
VERIFY: Task result returned with structured JSON.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=10 --subagent=dev-result-interpreter`

### Step 2: Receive Structured Result

EXECUTE: Parse the dev-result-interpreter output.
```
# Extract:
# - result.status (success/incomplete/failure)
# - result.display.template (formatted display text)
# - result.display.next_steps (array of recommendations)
```
VERIFY: Result contains required fields (status, display.template, display.next_steps).

### Step 3: Return Result to Command

EXECUTE: Set the skill's return value for the invoking command to display.
```
# The skill returns result.display.template
# The command (/dev) displays it to the user
# No additional processing — command shows result as-is
```
VERIFY: Result object prepared for return.

### Step 4: Archive Session Memory

EXECUTE: On story completion (status = "Dev Complete"), archive the session memory.
```
Edit(
  file_path=".claude/memory/sessions/${STORY_ID}-session.md",
  old_string="status: active",
  new_string="status: archived"
)
```
VERIFY: Session status updated.
```
Grep(pattern="status: archived", path=".claude/memory/sessions/${STORY_ID}-session.md")
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=10 --checkpoint-passed
# Exit 0: workflow complete | Exit 1: result interpretation failed

# After Phase 10 completion:
devforgeai-validate phase-archive ${STORY_ID}
# Moves state file to devforgeai/workflows/completed/
```

## Workflow Complete

All 10 phases completed. The skill returns the structured result to the invoking command.
