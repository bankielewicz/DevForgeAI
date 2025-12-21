# Manual Testing Checklist - STORY-025

**Story:** Wire hooks into /release command

**Purpose:** Manual validation scenarios for hook integration (post-merge testing)

**Created:** 2025-11-14

**Status:** PENDING (requires infrastructure to execute actual /release deployments)

---

## Pre-Testing Setup

### Prerequisites

- [ ] devforgeai CLI installed: `devforgeai --version`
- [ ] hooks.yaml configured in `devforgeai/config/`
- [ ] Feedback directory exists: `devforgeai/feedback/releases/`
- [ ] Log directory exists: `devforgeai/logs/`
- [ ] Test story in "QA Approved" status (for actual deployment)
- [ ] Staging environment accessible
- [ ] Production environment accessible (if testing production hooks)

### Baseline Measurement

```bash
# Before testing, establish baseline deployment time
time /release {TEST-STORY-ID} staging
# Record baseline: _____ seconds

# With hooks enabled, measure overhead
time /release {TEST-STORY-ID} staging
# Record with hooks: _____ seconds

# Calculate overhead
# Target: <3.5s additional time
```

---

## Test Scenario 1: Staging Deployment Success with Hooks Enabled

**DoD Reference:** "Manual test: /release with hooks enabled (staging failure triggers feedback)"

### Setup

```bash
# Enable staging hooks
cat > devforgeai/config/hooks.yaml << 'EOF'
enabled: true
operations:
  release-staging:
    enabled: true
    trigger_on: "all"
    questions:
      - "How did the staging deployment go?"
      - "Any issues or surprises?"
      - "Performance observations?"
EOF
```

### Execute

```bash
/release STORY-TEST-001 staging
```

### Expected Behavior

1. ✅ Staging deployment completes successfully
2. ✅ Feedback prompt appears: "How did the staging deployment go?"
3. ✅ User answers questions (or skips)
4. ✅ Feedback saved to `devforgeai/feedback/releases/STORY-TEST-001-staging-{timestamp}.json`
5. ✅ Deployment proceeds to completion message
6. ✅ Hook overhead <3.5 seconds

### Verification

- [ ] Feedback file created with correct timestamp
- [ ] JSON structure includes: `operation`, `story_id`, `environment`, `deployment_status`
- [ ] `deployment_status`: "SUCCESS"
- [ ] `environment`: "staging"
- [ ] Log file created: `devforgeai/logs/release-hooks-STORY-TEST-001.log`
- [ ] Log shows: check-hooks returned 0, invoke-hooks completed
- [ ] Deployment completed successfully (status updated in story file)

**Test Result:** ⬜ PASS / ⬜ FAIL

**Notes:**
```
[Record observations, actual times, any issues]
```

---

## Test Scenario 2: Staging Deployment Failure with Hooks

**DoD Reference:** "Manual test: /release with hooks enabled (staging failure triggers feedback)"

### Setup

Same as Scenario 1 (hooks enabled)

### Simulate Failure

Option A: Intentionally fail smoke tests
```bash
# Temporarily break smoke test config
mv devforgeai/smoke-tests/config.json devforgeai/smoke-tests/config.json.backup
echo '{"invalid": "config"}' > devforgeai/smoke-tests/config.json
```

Option B: Break deployment configuration

### Execute

```bash
/release STORY-TEST-001 staging
```

### Expected Behavior

1. ✅ Staging deployment FAILS (smoke tests fail or deployment error)
2. ✅ Feedback prompt appears with failure-specific questions
3. ✅ User provides failure context
4. ✅ Feedback saved with `"deployment_status": "FAILURE"`
5. ✅ Deployment stops (deployment failed, not hook issue)

### Verification

- [ ] Deployment status = FAILURE (accurate)
- [ ] Feedback file includes: `"deployment_status": "FAILURE"`
- [ ] Failure-specific questions asked (different from success questions)
- [ ] Log shows failure context
- [ ] Story status NOT updated to "Released" (deployment failed)

### Cleanup

```bash
# Restore smoke test config
mv devforgeai/smoke-tests/config.json.backup devforgeai/smoke-tests/config.json
```

**Test Result:** ⬜ PASS / ⬜ FAIL

**Notes:**
```
[Record observations]
```

---

## Test Scenario 3: Production Success (Failures-Only Mode)

**DoD Reference:** "Manual test: /release production success (skips feedback by default)"

### Setup

```bash
# Configure production hooks in failures-only mode (default)
cat > devforgeai/config/hooks.yaml << 'EOF'
enabled: true
operations:
  release-production:
    enabled: true
    trigger_on: "failures-only"
    on_success: false
    on_failure: true
EOF
```

### Execute

```bash
/release STORY-TEST-001 production
```

### Expected Behavior

1. ✅ Staging deployment completes (may trigger staging feedback)
2. ✅ Production deployment completes successfully
3. ✅ **NO production feedback prompt** (failures-only mode)
4. ✅ Message: "ℹ️ Production feedback skipped (failures-only mode, deployment succeeded)"
5. ✅ Deployment completion summary displayed

### Verification

- [ ] NO production feedback file created: `ls devforgeai/feedback/releases/*-production-*.json`
- [ ] Log shows: "check-hooks returned: 1 (not eligible - failures-only mode)"
- [ ] Deployment marked as SUCCESS
- [ ] Story status updated to "Released"
- [ ] No errors displayed

**Test Result:** ⬜ PASS / ⬜ FAIL

**Notes:**
```
[Confirm production success correctly skips feedback]
```

---

## Test Scenario 4: Production Failure (Triggers Feedback)

**DoD Reference:** "Manual test: /release production failure (triggers feedback)"

### Setup

Same as Scenario 3 (failures-only mode)

### Simulate Production Failure

```bash
# Break production smoke tests
# OR intentionally fail production deployment
```

### Execute

```bash
/release STORY-TEST-001 production
```

### Expected Behavior

1. ✅ Production deployment FAILS
2. ✅ **Feedback prompt appears** (failures always trigger, even in failures-only mode)
3. ✅ Critical incident questions presented
4. ✅ User provides failure/rollback observations
5. ✅ Feedback saved with `"metadata": {"severity": "critical"}`
6. ✅ Deployment failure summary displayed

### Verification

- [ ] Production feedback file created with FAILURE status
- [ ] JSON includes: `"deployment_status": "FAILURE"`, `"severity": "critical"`
- [ ] Critical incident questions asked (different from staging questions)
- [ ] Log shows: check-hooks returned 0 (eligible), invoke-hooks completed
- [ ] Deployment marked as FAILED (accurate)
- [ ] Story status NOT updated to "Released"

**Test Result:** ⬜ PASS / ⬜ FAIL

**Notes:**
```
[Confirm production failure triggers feedback correctly]
```

---

## Test Scenario 5: Hook CLI Not Installed

**DoD Reference:** "Manual test: Hook CLI not installed (warning logged, deployment succeeds)"

### Setup

```bash
# Temporarily make devforgeai CLI unavailable
mv $(which devforgeai) /tmp/devforgeai.backup
```

### Execute

```bash
/release STORY-TEST-001 staging
```

### Expected Behavior

1. ✅ Deployment proceeds normally (no hooks)
2. ✅ No feedback prompt appears
3. ✅ **NO errors** displayed (graceful skip)
4. ✅ Deployment completes successfully
5. ✅ Story status updated correctly

### Verification

- [ ] Deployment status = SUCCESS (hook absence doesn't affect deployment)
- [ ] No feedback files created
- [ ] No hook logs created (hooks never attempted)
- [ ] No error messages about hooks (silent skip)
- [ ] Story status updated to "Released" (deployment successful)

### Cleanup

```bash
# Restore devforgeai CLI
mv /tmp/devforgeai.backup $(which devforgeai)
```

**Test Result:** ⬜ PASS / ⬜ FAIL

**Notes:**
```
[Verify graceful degradation when CLI not installed]
```

---

## Test Scenario 6: User Skips All Feedback Questions

**DoD Reference:** "Manual test: User skips all feedback questions (skip tracking increments)"

### Setup

Hooks enabled (any configuration)

### Execute

```bash
/release STORY-TEST-001 staging
# When feedback prompt appears, press Enter (skip) for ALL questions
```

### Expected Behavior

1. ✅ Feedback prompt appears
2. ✅ User skips all questions (press Enter for each)
3. ✅ Skip tracking recorded (skip count increments for each question)
4. ✅ Feedback file saved with all questions marked `"skipped": true`
5. ✅ Deployment continues normally

### Verification

- [ ] Feedback file exists despite all questions skipped
- [ ] JSON shows: `{"question": "...", "answer": "", "skipped": true}` for all questions
- [ ] Skip tracking data present in feedback metadata
- [ ] Deployment completed successfully
- [ ] No errors or warnings

**Test Result:** ⬜ PASS / ⬜ FAIL

**Notes:**
```
[Verify skip tracking works correctly]
```

---

## Test Scenario 7: User Aborts Feedback (Ctrl+C)

**DoD Reference:** "Manual test: User aborts feedback with Ctrl+C (deployment status accurate)"

### Setup

Hooks enabled

### Execute

```bash
/release STORY-TEST-001 staging
# When feedback prompt appears, answer 1-2 questions, then press Ctrl+C
```

### Expected Behavior

1. ✅ Feedback prompt appears
2. ✅ User answers some questions
3. ✅ User presses Ctrl+C (aborts remaining questions)
4. ✅ **Partial feedback saved** (questions answered before abort)
5. ✅ Deployment continues immediately (user returned to workflow)
6. ✅ Deployment status accurate (SUCCESS or FAILURE based on deployment, not hook abort)

### Verification

- [ ] Partial feedback file exists
- [ ] JSON shows: Answered questions have `"skipped": false`, unanswered have `"skipped": true`
- [ ] Deployment completed after abort (didn't hang)
- [ ] Deployment status accurate (SUCCESS if deployment succeeded)
- [ ] Story status updated correctly

**Test Result:** ⬜ PASS / ⬜ FAIL

**Notes:**
```
[Verify graceful abort handling]
```

---

## Test Scenario 8: Multiple Deployment Retries (Same Story)

**DoD Reference:** "Manual test: Multiple deployment retries (separate feedback files per attempt)"

### Setup

Hooks enabled

### Execute

```bash
# First attempt (simulate failure)
/release STORY-TEST-001 staging  # Fail deliberately

# Wait for feedback to complete, then fix issue

# Second attempt (success)
/release STORY-TEST-001 staging  # Should succeed
```

### Expected Behavior

1. ✅ First attempt: Deployment fails, feedback collected
2. ✅ First feedback saved: `STORY-TEST-001-staging-{timestamp1}.json`
3. ✅ Second attempt: Deployment succeeds, feedback collected
4. ✅ Second feedback saved: `STORY-TEST-001-staging-{timestamp2}.json`
5. ✅ **Two separate files** (no overwrites)

### Verification

- [ ] Two feedback files exist with different timestamps
- [ ] First file: `"deployment_status": "FAILURE"`
- [ ] Second file: `"deployment_status": "SUCCESS"`
- [ ] Both files have same story_id but different timestamps
- [ ] No file overwrites occurred

**Test Result:** ⬜ PASS / ⬜ FAIL

**Notes:**
```
[Verify timestamp differentiation prevents overwrites]
```

---

## Performance Testing

### Test: Hook Overhead Measurement

**Execute:**
```bash
# Measure total time from deployment start to completion
START=$(date +%s)
/release STORY-TEST-001 staging
END=$(date +%s)
TOTAL_TIME=$((END - START))

# Estimate hook overhead (compare to baseline without hooks)
HOOK_OVERHEAD=$((TOTAL_TIME - BASELINE_TIME))

echo "Hook overhead: ${HOOK_OVERHEAD}s (target: <3.5s)"
```

### Targets

- [ ] check-hooks: <100ms (p95)
- [ ] invoke-hooks: <3s (p95, excluding user interaction)
- [ ] Total overhead: <3.5s (p95)

**Measured:**
- check-hooks: _____ ms
- invoke-hooks: _____ s
- Total overhead: _____ s

**Result:** ⬜ PASS (all within targets) / ⬜ FAIL (exceeds targets)

---

## Integration Testing

### Test: Consistent UX Across /dev, /qa, /release

**Execute all three commands with hooks enabled:**

```bash
/dev STORY-TEST-002       # Development workflow with hooks
/qa STORY-TEST-002        # QA validation with hooks
/release STORY-TEST-002   # Release deployment with hooks
```

### Expected: Same User Experience

- [ ] Same CLI commands (`devforgeai check-hooks`, `devforgeai invoke-hooks`)
- [ ] Same question presentation format
- [ ] Same skip behavior (press Enter to skip)
- [ ] Same Ctrl+C abort behavior (partial feedback saved)
- [ ] Same feedback file structure (JSON schema)
- [ ] Same log format

**Test Result:** ⬜ PASS / ⬜ FAIL

**Notes:**
```
[Verify UX consistency across commands]
```

---

## Regression Testing

### Test: /release Works WITHOUT Hooks

**Execute with hooks disabled:**

```bash
# Disable hooks
cat > devforgeai/config/hooks.yaml << 'EOF'
enabled: false
EOF

/release STORY-TEST-001 staging
```

### Expected: Normal Deployment (No Changes)

- [ ] Deployment proceeds normally
- [ ] No feedback prompts
- [ ] No hook logs created
- [ ] Deployment completes successfully
- [ ] Story status updated correctly
- [ ] **EXACT SAME behavior as before STORY-025**

**Test Result:** ⬜ PASS / ⬜ FAIL

**Notes:**
```
[Verify backward compatibility - existing behavior unchanged]
```

---

## Post-Testing Cleanup

### Reset Environment

```bash
# Restore production hooks.yaml
cp devforgeai/config/hooks.yaml.production devforgeai/config/hooks.yaml

# Clean up test feedback files
rm devforgeai/feedback/releases/STORY-TEST-*.json

# Clean up test logs
rm devforgeai/logs/release-hooks-STORY-TEST-*.log

# Verify cleanup
ls devforgeai/feedback/releases/
ls devforgeai/logs/
```

---

## Summary Report

**Date Tested:** _______________

**Tester:** _______________

**Environment:** ⬜ Staging  ⬜ Production  ⬜ Both

### Results

| Scenario | Result | Notes |
|----------|--------|-------|
| 1. Staging Success | ⬜ PASS / ⬜ FAIL | |
| 2. Staging Failure | ⬜ PASS / ⬜ FAIL | |
| 3. Production Success (failures-only) | ⬜ PASS / ⬜ FAIL | |
| 4. Production Failure | ⬜ PASS / ⬜ FAIL | |
| 5. CLI Not Installed | ⬜ PASS / ⬜ FAIL | |
| 6. User Skips All Questions | ⬜ PASS / ⬜ FAIL | |
| 7. User Aborts (Ctrl+C) | ⬜ PASS / ⬜ FAIL | |
| 8. Multiple Retries | ⬜ PASS / ⬜ FAIL | |
| Performance | ⬜ PASS / ⬜ FAIL | Overhead: _____ s |
| UX Consistency | ⬜ PASS / ⬜ FAIL | |
| Regression | ⬜ PASS / ⬜ FAIL | |

### Overall Assessment

**Total Tests:** 11
**Passed:** ___ / 11
**Failed:** ___ / 11
**Pass Rate:** ____%

**Ready for Production:** ⬜ YES / ⬜ NO

**Blockers (if any):**
```
[List any issues preventing production deployment]
```

**Recommendations:**
```
[Any improvements or follow-up work needed]
```

---

## Sign-Off

**Tested By:** _______________
**Date:** _______________
**Signature:** _______________

**Approved for Production:** ⬜ YES / ⬜ NO

---

**Note:** These manual tests should be executed after merge, in an environment with actual deployment infrastructure. The 100 automated tests provide confidence, but manual validation with real deployments confirms end-to-end functionality.
