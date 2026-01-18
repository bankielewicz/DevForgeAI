#!/bin/bash
# STORY-263 AC#2: Mode change notification displayed
# Test: Notification banner text exists for auto-detection
#
# Expected: FAIL (notification banner not yet implemented)

# Note: No 'set -e' - we need to track failures, not exit on first grep failure

TARGET_FILE="/mnt/c/Projects/DevForgeAI2/.claude/commands/dev.md"
STORY_ID="STORY-263"
AC_NUM="AC#2"

echo "================================================================"
echo "  ${STORY_ID} - ${AC_NUM}: Mode change notification displayed"
echo "================================================================"
echo ""
echo "Target: ${TARGET_FILE}"
echo ""

# Track test results
TESTS_PASSED=0
TESTS_FAILED=0

# Test 2.1: File exists
echo "Test 2.1: Target file exists"
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

# Test 2.2: Auto-detection notification banner exists
echo ""
echo "Test 2.2: Auto-detection notification banner exists"
# Expected format per story: "Auto-detected gaps.json - Remediation mode enabled"
if grep -qE "[Aa]uto.?detect.*gaps" "${TARGET_FILE}"; then
    echo "  PASS: Auto-detection notification text found"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Auto-detection notification NOT found"
    echo "        Expected: 'Auto-detected gaps.json - Remediation mode enabled'"
    ((TESTS_FAILED++))
fi

# Test 2.3: Notification uses Display pattern (consistent with existing notifications)
echo ""
echo "Test 2.3: Notification uses Display pattern"
# Look for Display: with auto-detection message
if grep -qE 'Display:.*[Aa]uto.?detect' "${TARGET_FILE}"; then
    echo "  PASS: Uses Display pattern for auto-detection notification"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Does not use Display pattern for auto-detection"
    echo "        Expected: 'Display: \"...Auto-detected gaps.json...\"'"
    ((TESTS_FAILED++))
fi

# Test 2.4: Notification includes emoji indicator (consistent with other modes)
echo ""
echo "Test 2.4: Notification includes visual indicator"
# Existing patterns use emoji: "Warning: Force mode enabled"
# Expected similar visual indicator for auto-detection
if grep -qE "Auto.*detect.*gaps" "${TARGET_FILE}"; then
    # Check for any indicator in the auto-detect context
    AUTODETECT_CONTEXT=$(grep -A2 -B2 "[Aa]uto.*detect.*gaps" "${TARGET_FILE}" 2>/dev/null)
    if echo "${AUTODETECT_CONTEXT}" | grep -qE "Display:"; then
        echo "  PASS: Notification with Display context found"
        ((TESTS_PASSED++))
    else
        echo "  FAIL: No Display pattern near auto-detection"
        ((TESTS_FAILED++))
    fi
else
    echo "  FAIL: Could not verify notification format"
    ((TESTS_FAILED++))
fi

# Test 2.5: Notification distinct from explicit --fix notification
echo ""
echo "Test 2.5: Distinct notification for auto-detect vs explicit --fix"
# --fix currently shows: "Remediation mode enabled"
# Auto-detect should show different text to distinguish source
FIX_NOTIFICATION=$(grep -c "Remediation mode enabled" "${TARGET_FILE}")
AUTODETECT_NOTIFICATION=$(grep -cE "[Aa]uto.*detect.*gaps" "${TARGET_FILE}")

if [[ ${AUTODETECT_NOTIFICATION} -gt 0 ]]; then
    echo "  PASS: Auto-detect notification present (distinct messaging)"
    ((TESTS_PASSED++))
else
    echo "  FAIL: No auto-detect specific notification"
    echo "        Current: Only '--fix' notification exists"
    echo "        Expected: Separate notification for auto-detection"
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
