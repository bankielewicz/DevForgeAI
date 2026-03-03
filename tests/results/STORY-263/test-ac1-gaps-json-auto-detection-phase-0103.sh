#!/bin/bash
# STORY-263 AC#1: Automatic gaps.json detection in Phase 01.0.3
# Test: Phase 01.0.3 section exists with gaps.json detection logic
#
# Expected: FAIL (Phase 01.0.3 not yet implemented - only Steps 0.1 and 0.2 exist)

# Note: No 'set -e' - we need to track failures, not exit on first grep failure

TARGET_FILE="/mnt/c/Projects/DevForgeAI2/.claude/commands/dev.md"
STORY_ID="STORY-263"
AC_NUM="AC#1"

echo "================================================================"
echo "  ${STORY_ID} - ${AC_NUM}: Automatic gaps.json detection in Phase 01.0.3"
echo "================================================================"
echo ""
echo "Target: ${TARGET_FILE}"
echo ""

# Track test results
TESTS_PASSED=0
TESTS_FAILED=0

# Test 1.1: File exists
echo "Test 1.1: Target file exists"
if [[ -f "${TARGET_FILE}" ]]; then
    echo "  PASS: File exists"
    ((TESTS_PASSED++))
else
    echo "  FAIL: File does not exist"
    ((TESTS_FAILED++))
    echo ""
    echo "RESULT: FAILED (file not found)"
    exit 1
fi

# Test 1.2: Step 0.3 section header exists (between Step 0.2 and Phase 1)
echo ""
echo "Test 1.2: Step 0.3 section header exists"
if grep -qE "^\*\*Step 0\.3:" "${TARGET_FILE}" || grep -qE "^### Step 0\.3:" "${TARGET_FILE}"; then
    echo "  PASS: Step 0.3 section found"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Step 0.3 section NOT found"
    echo "        Expected: '**Step 0.3:' or '### Step 0.3:'"
    ((TESTS_FAILED++))
fi

# Test 1.3: Step 0.3 contains gaps.json detection logic
echo ""
echo "Test 1.3: Step 0.3 contains gaps.json detection"
if grep -qE "gaps\.json" "${TARGET_FILE}" && grep -qE "Step 0\.3.*[Aa]uto.*[Dd]etect" "${TARGET_FILE}"; then
    echo "  PASS: gaps.json auto-detection in Step 0.3"
    ((TESTS_PASSED++))
else
    # Check if gaps.json is mentioned anywhere (for partial credit)
    if grep -qE "gaps\.json" "${TARGET_FILE}"; then
        echo "  PARTIAL: gaps.json mentioned but not in Step 0.3 auto-detection context"
        echo "           (Current: --fix flag usage only)"
    fi
    echo "  FAIL: Step 0.3 does not contain gaps.json auto-detection logic"
    ((TESTS_FAILED++))
fi

# Test 1.4: REMEDIATION_MODE set based on gaps.json detection (not just --fix flag)
echo ""
echo "Test 1.4: REMEDIATION_MODE set from gaps.json detection (auto-detect path)"
# Look for pattern where REMEDIATION_MODE is set from gap file detection, not just --fix
# Currently only: ELIF arg == "--fix": REMEDIATION_MODE = true
# Need: IF gaps_file_exists: REMEDIATION_MODE = true
if grep -qE "gaps.*exist|detect.*gaps|GAPS_FILE.*true|GAPS_AUTO_DETECTED" "${TARGET_FILE}"; then
    echo "  PASS: Auto-detection logic sets REMEDIATION_MODE"
    ((TESTS_PASSED++))
else
    echo "  FAIL: REMEDIATION_MODE only set via --fix flag (no auto-detection)"
    echo "        Current: 'ELIF arg == \"--fix\": REMEDIATION_MODE = true'"
    echo "        Expected: Detection of gaps.json file also sets REMEDIATION_MODE"
    ((TESTS_FAILED++))
fi

# Test 1.5: Step 0.3 appears between Step 0.2 and Phase 1
echo ""
echo "Test 1.5: Step 0.3 ordering (after 0.2, before Phase 1)"
STEP_02_LINE=$(grep -n "Step 0\.2" "${TARGET_FILE}" | head -1 | cut -d: -f1)
STEP_03_LINE=$(grep -n "Step 0\.3" "${TARGET_FILE}" | head -1 | cut -d: -f1)
PHASE_1_LINE=$(grep -n "### Phase 1:" "${TARGET_FILE}" | head -1 | cut -d: -f1)

if [[ -n "${STEP_02_LINE}" && -n "${STEP_03_LINE}" && -n "${PHASE_1_LINE}" ]]; then
    if [[ ${STEP_03_LINE} -gt ${STEP_02_LINE} && ${STEP_03_LINE} -lt ${PHASE_1_LINE} ]]; then
        echo "  PASS: Step 0.3 (line ${STEP_03_LINE}) is between Step 0.2 (${STEP_02_LINE}) and Phase 1 (${PHASE_1_LINE})"
        ((TESTS_PASSED++))
    else
        echo "  FAIL: Step 0.3 ordering incorrect"
        ((TESTS_FAILED++))
    fi
else
    echo "  FAIL: Could not verify ordering - Step 0.3 not found"
    echo "        Step 0.2 line: ${STEP_02_LINE:-NOT FOUND}"
    echo "        Step 0.3 line: ${STEP_03_LINE:-NOT FOUND}"
    echo "        Phase 1 line: ${PHASE_1_LINE:-NOT FOUND}"
    ((TESTS_FAILED++))
fi

# Summary
echo ""
echo "================================================================"
echo "  SUMMARY: ${AC_NUM}"
echo "================================================================"
echo "  Tests Passed: ${TESTS_PASSED}"
echo "  Tests Failed: ${TESTS_FAILED}"
echo ""

if [[ ${TESTS_FAILED} -eq 0 ]]; then
    echo "RESULT: PASSED"
    exit 0
else
    echo "RESULT: FAILED"
    exit 1
fi
