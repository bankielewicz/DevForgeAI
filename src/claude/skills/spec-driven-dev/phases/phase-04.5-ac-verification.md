# Phase 4.5: AC Compliance Verification (Post-Refactor)

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --from=04 --to=4.5
# Exit 0: proceed | Exit 1: Phase 04 incomplete
```

## Contract

PURPOSE: Independent verification that all acceptance criteria are fulfilled after refactoring — using a fresh-context subagent to eliminate bias.
REQUIRED SUBAGENTS: ac-compliance-verifier
REQUIRED ARTIFACTS: None
STEP COUNT: 4 mandatory steps

**100% STOP RATE GUARANTEE (STORY-277):** If verification fails, the workflow HALTs. No exceptions.

---

## Mandatory Steps

### Step 1: Load AC Verification Workflow

EXECUTE: Read the detailed verification reference.
```
Read(file_path=".claude/skills/implementing-stories/references/ac-verification-workflow.md")
```
VERIFY: File content loaded successfully.

### Step 2: Invoke AC Compliance Verifier

EXECUTE: Delegate verification to fresh-context subagent.
```
Task(
  subagent_type="ac-compliance-verifier",
  prompt="Verify acceptance criteria compliance for ${STORY_ID}.
  Story file: ${STORY_FILE}

  For EACH acceptance criterion:
  1. Read the AC text
  2. Find the implementation code that fulfills it
  3. Find the test that validates it
  4. Determine: PASS (evidence found) or FAIL (no evidence)

  Return structured result with per-AC verdicts and evidence file paths."
)
```
VERIFY: Task result returned with per-AC verdicts. Result is not a timeout.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=4.5 --subagent=ac-compliance-verifier`

### Step 3: Evaluate Verification Result

EXECUTE: Check the subagent's verdict.
```
IF all ACs PASS: Proceed to Exit Gate.
IF any AC FAIL: HALT immediately.
  Display: "AC Verification FAILED. The following ACs are not fulfilled: <list>"
  Display: "Return to Phase 03 to implement missing functionality."
```
VERIFY: Decision recorded (PASS or HALT).

### Step 4: Record Invocation

EXECUTE: Record the subagent invocation in phase state.
```bash
devforgeai-validate phase-record ${STORY_ID} --phase=4.5 --subagent=ac-compliance-verifier
```
VERIFY: Command executed successfully (exit code 0 or 127 for backward compat).

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=4.5 --checkpoint-passed
# Exit 0: proceed to Phase 05 | Exit 1: verification failed
```
