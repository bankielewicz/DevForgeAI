#!/bin/bash
# =============================================================================
# STORY-266 AC#4: Failed Execution as CRITICAL Violation
# =============================================================================
# Tests that documentation mentions CRITICAL severity for runtime failures
# and RUNTIME_EXECUTION_FAILURE violation type.
#
# Expected: FAIL (RED state - files don't exist yet)
# =============================================================================

set -e

# Test configuration
PHASE_FILE=".claude/skills/devforgeai-qa/phases/phase-01-deep-validation.md"
CONFIG_FILE=".claude/skills/devforgeai-qa/assets/language-smoke-tests.yaml"
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

TESTS_PASSED=0
TESTS_FAILED=0

# -----------------------------------------------------------------------------
# Test Helper Functions
# -----------------------------------------------------------------------------
test_pass() {
    echo -e "${GREEN}PASS${NC}: $1"
    TESTS_PASSED=$((TESTS_PASSED + 1))
}

test_fail() {
    echo -e "${RED}FAIL${NC}: $1"
    TESTS_FAILED=$((TESTS_FAILED + 1))
}

# -----------------------------------------------------------------------------
# AC#4 Test Cases
# -----------------------------------------------------------------------------

echo "=============================================="
echo "STORY-266 AC#4: CRITICAL Violation Tests"
echo "=============================================="
echo ""

# Test 4.1: CRITICAL severity documented
echo "Test 4.1: CRITICAL severity for failures documented"
if [ -f "${PROJECT_ROOT}/${PHASE_FILE}" ]; then
    if grep -q "CRITICAL" "${PROJECT_ROOT}/${PHASE_FILE}"; then
        test_pass "CRITICAL severity documented"
    else
        test_fail "CRITICAL severity NOT documented (failures must be CRITICAL)"
    fi
else
    test_fail "Cannot check CRITICAL severity - phase file missing"
fi

# Test 4.2: RUNTIME_EXECUTION_FAILURE violation type
echo ""
echo "Test 4.2: RUNTIME_EXECUTION_FAILURE violation type documented"
if [ -f "${PROJECT_ROOT}/${PHASE_FILE}" ]; then
    if grep -qE "RUNTIME_EXECUTION_FAILURE|Runtime.*Execution.*Failure" "${PROJECT_ROOT}/${PHASE_FILE}"; then
        test_pass "RUNTIME_EXECUTION_FAILURE type documented"
    else
        test_fail "RUNTIME_EXECUTION_FAILURE type NOT documented"
    fi
else
    test_fail "Cannot check violation type - phase file missing"
fi

# Test 4.3: Non-zero exit code triggers failure
echo ""
echo "Test 4.3: Non-zero exit code failure condition documented"
if [ -f "${PROJECT_ROOT}/${PHASE_FILE}" ]; then
    if grep -qiE "exit.*code.*!=.*0|non.zero|exit.*fail" "${PROJECT_ROOT}/${PHASE_FILE}"; then
        test_pass "Non-zero exit code failure condition documented"
    else
        test_fail "Non-zero exit code failure condition NOT documented"
    fi
else
    test_fail "Cannot check exit code failure - phase file missing"
fi

# Test 4.4: Timeout triggers failure
echo ""
echo "Test 4.4: Timeout triggers failure documented"
if [ -f "${PROJECT_ROOT}/${PHASE_FILE}" ]; then
    if grep -qiE "timeout.*fail|timeout.*exceeded|exceeded.*timeout" "${PROJECT_ROOT}/${PHASE_FILE}"; then
        test_pass "Timeout failure condition documented"
    else
        test_fail "Timeout failure condition NOT documented"
    fi
else
    test_fail "Cannot check timeout failure - phase file missing"
fi

# Test 4.5: QA status set to FAILED
echo ""
echo "Test 4.5: QA overall_status FAILED on violation"
if [ -f "${PROJECT_ROOT}/${PHASE_FILE}" ]; then
    if grep -qiE "overall.*status.*FAILED|status.*FAILED|QA.*FAILED" "${PROJECT_ROOT}/${PHASE_FILE}"; then
        test_pass "QA FAILED status documented"
    else
        test_fail "QA FAILED status NOT documented on runtime failure"
    fi
else
    test_fail "Cannot check QA status - phase file missing"
fi

# Test 4.6: Remediation guidance in config
echo ""
echo "Test 4.6: Remediation guidance in language config"
if [ -f "${PROJECT_ROOT}/${CONFIG_FILE}" ]; then
    if grep -qE "remediation|Remediation" "${PROJECT_ROOT}/${CONFIG_FILE}"; then
        test_pass "Remediation guidance found in config"
    else
        test_fail "Remediation guidance NOT found in config"
    fi
else
    test_fail "Cannot check remediation - config file missing"
fi

# Test 4.7: gaps.json mentioned for violation tracking
echo ""
echo "Test 4.7: gaps.json violation tracking documented"
if [ -f "${PROJECT_ROOT}/${PHASE_FILE}" ]; then
    if grep -qE "gaps\.json|gaps json" "${PROJECT_ROOT}/${PHASE_FILE}"; then
        test_pass "gaps.json violation tracking documented"
    else
        test_fail "gaps.json violation tracking NOT documented"
    fi
else
    test_fail "Cannot check gaps.json - phase file missing"
fi

# Test 4.8: Error message includes language context
echo ""
echo "Test 4.8: Error message format includes language"
if [ -f "${PROJECT_ROOT}/${PHASE_FILE}" ]; then
    if grep -qE "language.*cannot|CLI.*cannot|cannot.*executed" "${PROJECT_ROOT}/${PHASE_FILE}"; then
        test_pass "Error message with language context documented"
    else
        test_fail "Error message format missing language context (expected: '{language} CLI cannot be executed: {error}')"
    fi
else
    test_fail "Cannot check error message - phase file missing"
fi

# -----------------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------------
echo ""
echo "=============================================="
echo "AC#4 Test Summary"
echo "=============================================="
echo "Passed: ${TESTS_PASSED}"
echo "Failed: ${TESTS_FAILED}"
echo ""

if [ ${TESTS_FAILED} -gt 0 ]; then
    echo -e "${RED}AC#4 TESTS FAILED (RED state - expected for TDD)${NC}"
    exit 1
else
    echo -e "${GREEN}AC#4 TESTS PASSED${NC}"
    exit 0
fi
