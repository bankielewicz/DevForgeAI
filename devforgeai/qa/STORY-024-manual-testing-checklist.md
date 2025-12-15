# STORY-024 Manual Testing Checklist

**Story:** Wire hooks into /qa command
**Date:** 2025-11-13
**Tester:** [Your Name]

---

## Prerequisites

- [ ] DevForgeAI hooks configured (`.devforgeai/hooks/hooks.yaml` exists)
- [ ] Feedback skill available (`.claude/skills/devforgeai-feedback/`)
- [ ] At least 2 test stories available (one passing QA, one failing QA)
- [ ] Python 3.12.3 + pytest installed
- [ ] devforgeai CLI installed (`pip install -e .claude/scripts/`)

---

## Test 1: QA Deep Failure Triggers Feedback

**Goal:** Verify feedback triggers when deep QA fails (failures-only mode)

**Steps:**
1. Ensure hooks config has `trigger_on: failures-only`
2. Identify or create a story that will fail QA (e.g., coverage <80%)
3. Run: `/qa <STORY-ID> deep`
4. Observe QA validation results

**Expected Results:**
- [ ] QA validation runs and completes
- [ ] QA result: FAILED (with specific violations listed)
- [ ] Message displayed: "ℹ️ Feedback hook invoked (qa failed)"
- [ ] Feedback conversation starts automatically
- [ ] Questions reference specific violations (e.g., "Coverage was 75%...")
- [ ] After feedback, QA result remains FAILED
- [ ] Story status NOT updated (remains in previous status)

**Actual Results:**
```
[Record what actually happened]
```

**Status:** [ ] PASS  [ ] FAIL  [ ] SKIP

**Notes:**
```
[Any observations, issues, or deviations]
```

---

## Test 2: QA Deep Pass Skips Feedback

**Goal:** Verify feedback does NOT trigger when deep QA passes (failures-only mode)

**Steps:**
1. Ensure hooks config has `trigger_on: failures-only`
2. Identify or create a story that will pass QA (coverage ≥80%, no violations)
3. Run: `/qa <STORY-ID> deep`
4. Observe QA validation results

**Expected Results:**
- [ ] QA validation runs and completes
- [ ] QA result: PASSED (all quality gates met)
- [ ] NO feedback hook message displayed
- [ ] NO feedback conversation starts
- [ ] /qa completes normally with success message
- [ ] Story status updated to "QA Approved"
- [ ] QA Validation History section added to story file

**Actual Results:**
```
[Record what actually happened]
```

**Status:** [ ] PASS  [ ] FAIL  [ ] SKIP

**Notes:**
```
[Any observations, issues, or deviations]
```

---

## Test 3: QA Light Mode Integration

**Goal:** Verify hook integration works with light mode

**Steps:**
1. Identify or create a story with QA failures
2. Run: `/qa <STORY-ID> light`
3. Observe results

**Expected Results:**
- [ ] Light QA validation runs (quick checks only)
- [ ] If light QA fails → feedback triggers
- [ ] If light QA passes → no feedback
- [ ] Hook behavior same as deep mode
- [ ] Light mode result NOT affected by hook

**Actual Results:**
```
[Record what actually happened]
```

**Status:** [ ] PASS  [ ] FAIL  [ ] SKIP

**Notes:**
```
[Any observations, issues, or deviations]
```

---

## Test 4: Hook Failure Non-Blocking

**Goal:** Verify hook failures don't break /qa command

**Steps:**
1. Temporarily break feedback hook:
   - Option A: Set invalid skill name in hooks.yaml
   - Option B: Disable devforgeai-feedback skill temporarily
2. Run: `/qa <STORY-ID> deep` (with a failing story)
3. Observe error handling

**Expected Results:**
- [ ] QA validation completes successfully
- [ ] Hook invocation fails (expected)
- [ ] Warning message: "⚠️ Feedback hook failed, QA result unchanged"
- [ ] QA result still displayed correctly (FAILED in this case)
- [ ] Story status reflects actual QA outcome (not affected by hook)
- [ ] /qa command completes (doesn't crash or halt)

**Actual Results:**
```
[Record what actually happened]
```

**Status:** [ ] PASS  [ ] FAIL  [ ] SKIP

**Cleanup:**
- [ ] Restore hooks.yaml or re-enable feedback skill

**Notes:**
```
[Any observations, issues, or deviations]
```

---

## Test 5: Violation Context Passed to Feedback

**Goal:** Verify feedback receives specific violation details

**Steps:**
1. Create/identify story with known violations:
   - Coverage gap (e.g., 75% when target is 85%)
   - Specific anti-pattern (e.g., God Object)
2. Run: `/qa <STORY-ID> deep`
3. When feedback starts, review the questions

**Expected Results:**
- [ ] Feedback conversation starts
- [ ] Questions mention specific coverage % (e.g., "Coverage was 75%")
- [ ] Questions mention number of violations (e.g., "3 violations detected")
- [ ] Questions reference violation types (coverage, anti-patterns, spec compliance)
- [ ] Context is human-readable and actionable

**Actual Results:**
```
[Record violation context displayed in feedback]
```

**Status:** [ ] PASS  [ ] FAIL  [ ] SKIP

**Notes:**
```
[Any observations, issues, or deviations]
```

---

## Test 6: Performance <5s Overhead

**Goal:** Verify Phase 4 hook integration adds <5 seconds overhead

**Steps:**
1. Run `/qa <STORY-ID> deep` and measure total time
2. Note time for Phase 4 execution specifically
3. Repeat 5 times for consistency
4. Calculate average overhead

**Expected Results:**
- [ ] Phase 4 execution time: <5 seconds (each run)
- [ ] Average overhead: <5 seconds
- [ ] No significant slowdown of /qa command
- [ ] QA result determination unaffected

**Measurements:**
```
Run 1: Phase 4 time = ___ seconds
Run 2: Phase 4 time = ___ seconds
Run 3: Phase 4 time = ___ seconds
Run 4: Phase 4 time = ___ seconds
Run 5: Phase 4 time = ___ seconds

Average: ___ seconds
```

**Status:** [ ] PASS (<5s)  [ ] FAIL (≥5s)  [ ] SKIP

**Notes:**
```
[Performance observations]
```

---

## Test 7: Reliability - QA Result Accuracy

**Goal:** Verify hooks don't affect QA result accuracy (100% consistency)

**Steps:**
1. Select 5 stories (mix of pass/fail scenarios)
2. For each story:
   a. Run `/qa <STORY-ID> deep` WITH hooks enabled
   b. Record QA result (PASSED/FAILED/PARTIAL)
   c. Disable hooks temporarily
   d. Run `/qa <STORY-ID> deep` WITHOUT hooks
   e. Record QA result
   f. Compare results

**Expected Results:**
- [ ] Results identical with hooks ON vs OFF (100% match)
- [ ] No false positives (hook causing pass → fail)
- [ ] No false negatives (hook causing fail → pass)
- [ ] QA validation logic unchanged

**Measurements:**
```
Story 1:
  - With hooks: ___________
  - Without hooks: ___________
  - Match: YES / NO

Story 2:
  - With hooks: ___________
  - Without hooks: ___________
  - Match: YES / NO

Story 3:
  - With hooks: ___________
  - Without hooks: ___________
  - Match: YES / NO

Story 4:
  - With hooks: ___________
  - Without hooks: ___________
  - Match: YES / NO

Story 5:
  - With hooks: ___________
  - Without hooks: ___________
  - Match: YES / NO

Accuracy: ___% (should be 100%)
```

**Status:** [ ] PASS (100%)  [ ] FAIL (<100%)  [ ] SKIP

**Notes:**
```
[Reliability observations]
```

---

## Edge Cases

### Edge Case 1: Partial QA Result

**Scenario:** QA passes with warnings (PARTIAL status)

**Steps:**
1. Create story with warnings but no blocking issues
2. Run `/qa <STORY-ID> deep`

**Expected:**
- [ ] QA result: PARTIAL
- [ ] STATUS mapped to "partial"
- [ ] Hook behavior determined by config (check-hooks decides)

**Actual:**
```
[Record what happened]
```

---

### Edge Case 2: Multiple QA Attempts

**Scenario:** Running /qa multiple times on same story

**Steps:**
1. Run `/qa <STORY-ID> deep` (fails)
2. Fix some issues
3. Run `/qa <STORY-ID> deep` again (still fails)
4. Fix remaining issues
5. Run `/qa <STORY-ID> deep` (passes)

**Expected:**
- [ ] Each attempt triggers hook independently
- [ ] Feedback doesn't reference previous attempts
- [ ] Each run behaves as if first run

**Actual:**
```
[Record what happened]
```

---

## Summary

**Tests Completed:** __ / 7
**Tests Passed:** __ / 7
**Tests Failed:** __ / 7
**Tests Skipped:** __ / 7

**Pass Rate:** ___%

**Overall Assessment:**
- [ ] All critical tests passed
- [ ] Performance requirements met
- [ ] Reliability requirements met
- [ ] No regressions detected
- [ ] Edge cases handled correctly

**Issues Found:**
```
[List any bugs, unexpected behavior, or concerns]
```

**Recommendations:**
```
[Suggested fixes, improvements, or follow-up actions]
```

---

## Approval

**Tested By:** ___________________
**Date:** ___________________
**Approved:** [ ] YES  [ ] NO  [ ] WITH CONDITIONS

**Conditions (if applicable):**
```
[List any conditions for approval]
```

---

**Next Steps:**
- [ ] Update story DoD checkboxes based on test results
- [ ] File issues for any failures
- [ ] Mark story as "Dev Complete" if all tests pass
- [ ] Proceed to formal QA validation if manual testing complete
