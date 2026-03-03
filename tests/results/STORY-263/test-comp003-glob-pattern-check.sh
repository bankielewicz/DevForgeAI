#!/bin/bash
# STORY-263 COMP-003: Check gaps.json existence using Glob
# Test: Glob pattern for gaps.json file check is present
#
# Expected: FAIL (Glob check not yet implemented in Step 0.3)

# Note: No 'set -e' - we need to track failures, not exit on first grep failure

TARGET_FILE="/mnt/c/Projects/DevForgeAI2/.claude/commands/dev.md"
STORY_ID="STORY-263"
TEST_ID="COMP-003"

echo "================================================================"
echo "  ${STORY_ID} - ${TEST_ID}: Glob pattern for gaps.json check"
echo "================================================================"
echo ""
echo "Target: ${TARGET_FILE}"
echo ""

# Track test results
TESTS_PASSED=0
TESTS_FAILED=0

# Test C3.1: File exists
echo "Test C3.1: Target file exists"
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

# Test C3.2: Glob tool usage for gaps.json detection
echo ""
echo "Test C3.2: Glob tool used for detection"
# Look for Glob(pattern=...) or Glob(...gaps.json...)
if grep -qE 'Glob\(.*gaps|Glob.*pattern.*gaps' "${TARGET_FILE}"; then
    echo "  PASS: Glob tool used for gaps.json detection"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Glob tool NOT used for gaps.json detection"
    echo "        Expected: Glob(pattern=\"devforgeai/qa/reports/STORY-XXX-gaps.json\")"
    ((TESTS_FAILED++))
fi

# Test C3.3: Glob in Step 0.3 context (not elsewhere)
echo ""
echo "Test C3.3: Glob in Step 0.3 context"
STEP_03_CONTENT=$(sed -n '/Step 0\.3/,/Step 0\.4\|Phase 1/p' "${TARGET_FILE}" 2>/dev/null)
if [[ -n "${STEP_03_CONTENT}" ]]; then
    if echo "${STEP_03_CONTENT}" | grep -qiE "Glob"; then
        echo "  PASS: Glob usage in Step 0.3"
        ((TESTS_PASSED++))
    else
        echo "  FAIL: No Glob usage in Step 0.3"
        echo "        Glob may exist elsewhere but not in detection step"
        ((TESTS_FAILED++))
    fi
else
    echo "  FAIL: Step 0.3 not found"
    ((TESTS_FAILED++))
fi

# Test C3.4: Uses native tool (not Bash find/ls)
echo ""
echo "Test C3.4: Uses native Glob (not Bash commands)"
# Per tech-stack.md: Use Glob() instead of Bash(find) or Bash(ls)
STEP_03_CONTENT=$(sed -n '/Step 0\.3/,/Step 0\.4\|Phase 1/p' "${TARGET_FILE}" 2>/dev/null)
if [[ -n "${STEP_03_CONTENT}" ]]; then
    # Check for prohibited patterns
    if echo "${STEP_03_CONTENT}" | grep -qE 'Bash.*find|Bash.*ls.*gaps'; then
        echo "  FAIL: Uses Bash commands instead of Glob (violates tech-stack.md)"
        ((TESTS_FAILED++))
    else
        echo "  PASS: Does not use prohibited Bash patterns in detection"
        ((TESTS_PASSED++))
    fi
else
    # If Step 0.3 doesn't exist, this is a soft pass (nothing wrong yet)
    echo "  SKIP: Step 0.3 not implemented - native tool check deferred"
    ((TESTS_PASSED++))
fi

# Test C3.5: Glob result handling (empty = no gaps file)
echo ""
echo "Test C3.5: Glob result handling documented"
# Look for handling of Glob returning empty or no match
if grep -qE "(Glob.*empty|no.*match|not.*found|result.*length|count.*0)" "${TARGET_FILE}"; then
    echo "  PASS: Glob result handling documented"
    ((TESTS_PASSED++))
else
    echo "  FAIL: No documentation of Glob result handling"
    echo "        Expected: Logic for empty Glob result (no gaps file)"
    ((TESTS_FAILED++))
fi

# Summary
echo ""
echo "================================================================"
echo "  SUMMARY: ${TEST_ID}"
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
