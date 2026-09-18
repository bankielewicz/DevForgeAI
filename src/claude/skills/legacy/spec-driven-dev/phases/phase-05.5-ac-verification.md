# Phase 5.5: AC Compliance Verification (Post-Integration)

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --from=05 --to=5.5
# Exit 0: proceed | Exit 1: Phase 05 incomplete
```

## Contract

PURPOSE: Final independent verification that all acceptance criteria remain fulfilled after integration testing.
REQUIRED SUBAGENTS: ac-compliance-verifier
REQUIRED ARTIFACTS: None
STEP COUNT: 4 mandatory steps

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-dev/references/ac-verification-workflow.md")
```

IF any Read fails: HALT -- "Phase 5.5 reference files not loaded."

---

## Mandatory Steps

### Step 1: Load AC Verification Workflow

EXECUTE: Read the detailed verification reference.
```
Read(file_path="references/ac-verification-workflow.md")
```
VERIFY: File content loaded successfully.

### Step 2: Invoke AC Compliance Verifier

EXECUTE: Delegate verification to fresh-context subagent.
```
Task(
  subagent_type="ac-compliance-verifier",
  prompt="Final AC compliance verification for ${STORY_ID} (post-integration).
  Story file: ${STORY_FILE}

  For EACH acceptance criterion:
  1. Read the AC text
  2. Find the implementation code that fulfills it
  3. Verify using ONLY integration test evidence. Unit test verification was completed in Phase 4.5 -- do not re-read unit test files. If an AC was PASS in Phase 4.5 and no integration test is relevant to that AC, carry forward the PASS verdict. Focus on ACs where integration tests provide new coverage.
  4. Determine: PASS (evidence found or carried forward from Phase 4.5) or FAIL (no evidence)

  Return structured result with per-AC verdicts and evidence file paths."
)
```
VERIFY: Task result returned with per-AC verdicts. Result is not a timeout.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=5.5 --subagent=ac-compliance-verifier`

### Step 3: Evaluate Verification Result

EXECUTE: Check the subagent's verdict.
```
IF all ACs PASS: Proceed to Exit Gate.
IF any AC FAIL: HALT immediately.
  Display: "Final AC Verification FAILED. ACs not fulfilled: <list>"
```
VERIFY: Decision recorded (PASS or HALT).

### Step 4: Record Invocation

EXECUTE: Record the subagent invocation in phase state.
```bash
devforgeai-validate phase-record ${STORY_ID} --phase=5.5 --subagent=ac-compliance-verifier
```
VERIFY: Command executed successfully.

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=5.5 --checkpoint-passed
# Exit 0: proceed to Phase 06 | Exit 1: verification failed
```

## Hook-backed OUT-Attestation

This phase has Phase-D dispatch entries in `subagent_out_attestation_registry.json`. When dispatching those named subagents, instruct them to return a `subagent-result-v1` result that includes `coverage_attestation` in the normal response. Phase completion is blocked by `subagent-out-attestation-gate.sh` when the hook-owned ledger line lacks `coverage_attestation_present:true`. This Phase-D path is OUT-attestation-only and does not require `tmp/<WORK_ID>/handoffs/`.
