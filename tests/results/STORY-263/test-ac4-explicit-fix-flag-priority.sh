#!/bin/bash
# STORY-263 AC#4: Explicit --fix flag still works
# Test: --fix flag takes priority over auto-detection
#
# Expected: PASS (--fix flag already implemented - this test validates backward compatibility)

# Note: No 'set -e' - we need to track failures, not exit on first grep failure

TARGET_FILE="/mnt/c/Projects/DevForgeAI2/.claude/commands/dev.md"
STORY_ID="STORY-263"
AC_NUM="AC#4"

echo "================================================================"
echo "  ${STORY_ID} - ${AC_NUM}: Explicit --fix flag still works"
echo "================================================================"
echo ""
echo "Target: ${TARGET_FILE}"
echo ""

# Track test results
TESTS_PASSED=0
TESTS_FAILED=0

# Test 4.1: File exists
echo "Test 4.1: Target file exists"
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

# Test 4.2: --fix flag parsing exists (backward compatibility)
echo ""
echo "Test 4.2: --fix flag parsing exists"
if grep -qE 'arg.*==.*"--fix"|"--fix"' "${TARGET_FILE}"; then
    echo "  PASS: --fix flag parsing present"
    ((TESTS_PASSED++))
else
    echo "  FAIL: --fix flag parsing NOT found"
    ((TESTS_FAILED++))
fi

# Test 4.3: --fix sets REMEDIATION_MODE = true
echo ""
echo "Test 4.3: --fix sets REMEDIATION_MODE = true"
# Check for the pattern: IF/ELIF arg == "--fix": REMEDIATION_MODE = true
if grep -qE "--fix.*REMEDIATION_MODE.*true|REMEDIATION_MODE.*true.*--fix" "${TARGET_FILE}" || \
   grep -A2 '"\-\-fix"' "${TARGET_FILE}" | grep -qE "REMEDIATION_MODE.*=.*true"; then
    echo "  PASS: --fix flag sets REMEDIATION_MODE = true"
    ((TESTS_PASSED++))
else
    # Check more carefully with context
    FIX_CONTEXT=$(grep -A5 '"\-\-fix"' "${TARGET_FILE}" 2>/dev/null)
    if echo "${FIX_CONTEXT}" | grep -qE "REMEDIATION_MODE"; then
        echo "  PASS: REMEDIATION_MODE referenced after --fix parsing"
        ((TESTS_PASSED++))
    else
        echo "  FAIL: --fix does not set REMEDIATION_MODE"
        ((TESTS_FAILED++))
    fi
fi

# Test 4.4: --fix takes priority (processed before auto-detection OR short-circuits)
echo ""
echo "Test 4.4: --fix flag priority over auto-detection"
# Look for explicit priority documentation OR ordering (--fix before auto-detect)
# BR-002: "Explicit --fix flag takes priority over auto-detection"
if grep -qE "(--fix.*prior|prior.*--fix|override.*auto|explicit.*flag)" "${TARGET_FILE}"; then
    echo "  PASS: Explicit priority documentation found"
    ((TESTS_PASSED++))
else
    # Check if --fix is in Step 0.1 (before Step 0.3 auto-detect)
    FIX_LINE=$(grep -n '"\-\-fix"' "${TARGET_FILE}" | head -1 | cut -d: -f1)
    STEP_03_LINE=$(grep -n "Step 0\.3" "${TARGET_FILE}" | head -1 | cut -d: -f1)

    if [[ -n "${FIX_LINE}" && -n "${STEP_03_LINE}" ]]; then
        if [[ ${FIX_LINE} -lt ${STEP_03_LINE} ]]; then
            echo "  PASS: --fix parsed (line ${FIX_LINE}) before auto-detect (line ${STEP_03_LINE})"
            ((TESTS_PASSED++))
        else
            echo "  FAIL: --fix should be parsed before Step 0.3 auto-detection"
            ((TESTS_FAILED++))
        fi
    elif [[ -n "${FIX_LINE}" && -z "${STEP_03_LINE}" ]]; then
        echo "  INFO: --fix exists (line ${FIX_LINE}), Step 0.3 not yet implemented"
        echo "  FAIL: Step 0.3 auto-detection not implemented (priority check incomplete)"
        ((TESTS_FAILED++))
    else
        echo "  FAIL: Cannot verify priority ordering"
        ((TESTS_FAILED++))
    fi
fi

# Test 4.5: --fix flag usage documented in help text
echo ""
echo "Test 4.5: --fix flag in help/usage text"
if grep -qE "/dev.*--fix|--fix.*Resolve|--fix.*gaps" "${TARGET_FILE}"; then
    echo "  PASS: --fix documented in usage examples"
    ((TESTS_PASSED++))
else
    echo "  FAIL: --fix not documented in help text"
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
