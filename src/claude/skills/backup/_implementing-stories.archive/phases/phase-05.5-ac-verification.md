# Phase 05.5: AC Compliance Verification (Post-Integration)

**Entry Gate:**
```bash
devforgeai-validate phase-check ${STORY_ID} --from=05 --to=5.5
# Exit code 0: Transition allowed
# Exit code 1: Phase 05 not complete - HALT
# Exit code 2: Missing subagents from Phase 05 - HALT
```

---

## Progressive Task Disclosure

Read and follow `references/progressive-task-disclosure.md` (substitute PHASE_ID = "5.5").

---

## Mandatory Steps

**Purpose:** Verify acceptance criteria fulfillment using fresh-context technique after integration testing

**Required Subagents:** ac-compliance-verifier

**Execution:** Read and follow `references/ac-verification-workflow.md` for the complete verification workflow.

**Phase-specific details:**
- Record invocation: `devforgeai-validate phase-record ${STORY_ID} --phase=5.5 --subagent=ac-compliance-verifier`
- On PASS: Proceed to Phase 06
- On FAIL: HALT workflow (100% stop rate guarantee per STORY-277)

---

## Validation Checkpoint

**Before proceeding to Phase 06, verify:**

- [ ] ac-compliance-verifier subagent invoked
- [ ] Verification completed (not timed out)
- [ ] All ACs passed OR workflow HALTed
- [ ] Subagent invocation recorded via phase-record

**IF any checkbox UNCHECKED:** HALT workflow

---

## Optional Captures

**Before exiting, reflect:** Did verification catch issues introduced by integration changes? Were any ACs affected?

**If observations exist:** Append to phase-state.json `observations` array with id "obs-5.5-{seq}", phase "5.5".

**Reference:** `references/observation-capture.md`

---

## Exit Gate
```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=5.5 --checkpoint-passed
# Exit code 0: Phase complete, proceed to Phase 06
# Exit code 1: Cannot complete - verification failed or incomplete
```
