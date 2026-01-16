#!/bin/bash
# =============================================================================
# STORY-266 AC#3: Successful Execution Reporting
# =============================================================================
# Tests that documentation mentions "PASSED" message format for successful
# runtime smoke test execution.
#
# Expected: FAIL (RED state - files don't exist yet)
# =============================================================================

set -e

# Test configuration
PHASE_FILE=".claude/skills/devforgeai-qa/phases/phase-01-deep-validation.md"
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
# AC#3 Test Cases
# -----------------------------------------------------------------------------

echo "=============================================="
echo "STORY-266 AC#3: Success Reporting Tests"
echo "=============================================="
echo ""

# Test 3.1: PASSED message format documented
echo "Test 3.1: PASSED message format documented"
if [ -f "${PROJECT_ROOT}/${PHASE_FILE}" ]; then
    if grep -qE "PASSED|[Pp]assed" "${PROJECT_ROOT}/${PHASE_FILE}"; then
        test_pass "PASSED message format found"
    else
        test_fail "PASSED message format NOT found (expected: 'Runtime smoke test PASSED')"
    fi
else
    test_fail "Cannot check PASSED format - phase file missing"
fi

# Test 3.2: Success output pattern includes language
echo ""
echo "Test 3.2: Success message includes language reference"
if [ -f "${PROJECT_ROOT}/${PHASE_FILE}" ]; then
    if grep -qE "PASSED.*language|language.*PASSED|PASSED.*CLI|CLI.*PASSED" "${PROJECT_ROOT}/${PHASE_FILE}"; then
        test_pass "Success message includes language context"
    else
        test_fail "Success message missing language context (expected: 'Runtime smoke test PASSED: {language} CLI is executable')"
    fi
else
    test_fail "Cannot check success message - phase file missing"
fi

# Test 3.3: Exit code 0 documented as success
echo ""
echo "Test 3.3: Exit code 0 documented as success condition"
if [ -f "${PROJECT_ROOT}/${PHASE_FILE}" ]; then
    if grep -qE "exit.*code.*0|exit.*0|code.*0.*success" "${PROJECT_ROOT}/${PHASE_FILE}"; then
        test_pass "Exit code 0 success condition documented"
    else
        test_fail "Exit code 0 NOT documented as success condition"
    fi
else
    test_fail "Cannot check exit code documentation - phase file missing"
fi

# Test 3.4: No violations on success
echo ""
echo "Test 3.4: Documentation states no violations added on success"
if [ -f "${PROJECT_ROOT}/${PHASE_FILE}" ]; then
    if grep -qiE "no violation|no.*added|continue.*next" "${PROJECT_ROOT}/${PHASE_FILE}"; then
        test_pass "No violations on success documented"
    else
        test_fail "Success behavior (no violations) NOT clearly documented"
    fi
else
    test_fail "Cannot check violation behavior - phase file missing"
fi

# Test 3.5: Workflow continues after success
echo ""
echo "Test 3.5: Workflow continuation after success documented"
if [ -f "${PROJECT_ROOT}/${PHASE_FILE}" ]; then
    if grep -qiE "continue|proceed|next.*step" "${PROJECT_ROOT}/${PHASE_FILE}"; then
        test_pass "Workflow continuation documented"
    else
        test_fail "Workflow continuation after success NOT documented"
    fi
else
    test_fail "Cannot check workflow continuation - phase file missing"
fi

# -----------------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------------
echo ""
echo "=============================================="
echo "AC#3 Test Summary"
echo "=============================================="
echo "Passed: ${TESTS_PASSED}"
echo "Failed: ${TESTS_FAILED}"
echo ""

if [ ${TESTS_FAILED} -gt 0 ]; then
    echo -e "${RED}AC#3 TESTS FAILED (RED state - expected for TDD)${NC}"
    exit 1
else
    echo -e "${GREEN}AC#3 TESTS PASSED${NC}"
    exit 0
fi
