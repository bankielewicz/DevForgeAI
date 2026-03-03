#!/bin/bash
# STORY-313 AC#2: CI verifies mirror sync
# Test: .github/workflows/sync-verification.yml

set -e

# Test Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
CI_WORKFLOW="$PROJECT_ROOT/.github/workflows/sync-verification.yml"

# Test Results
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test Helper Functions
pass() {
    echo "[PASS] $1"
    TESTS_PASSED=$((TESTS_PASSED + 1))
    TESTS_RUN=$((TESTS_RUN + 1))
}

fail() {
    echo "[FAIL] $1"
    TESTS_FAILED=$((TESTS_FAILED + 1))
    TESTS_RUN=$((TESTS_RUN + 1))
}

# ------------------------------------------------------------------------------
# Test: CI-000 - Workflow file exists
# ------------------------------------------------------------------------------
test_workflow_exists() {
    if [ -f "$CI_WORKFLOW" ]; then
        pass "CI-000: CI workflow exists at .github/workflows/sync-verification.yml"
    else
        fail "CI-000: CI workflow NOT FOUND at .github/workflows/sync-verification.yml"
    fi
}

# ------------------------------------------------------------------------------
# Test: CI-001 - Run diff check on every PR (pull_request trigger)
# ------------------------------------------------------------------------------
test_pull_request_trigger() {
    if [ -f "$CI_WORKFLOW" ]; then
        if grep -q "pull_request" "$CI_WORKFLOW"; then
            pass "CI-001: Workflow has pull_request trigger"
        else
            fail "CI-001: Workflow does NOT have pull_request trigger"
        fi
    else
        fail "CI-001: Workflow not found, cannot check trigger"
    fi
}

# ------------------------------------------------------------------------------
# Test: CI-002 - Fail PR if mirrors are out of sync (diff command with exit)
# ------------------------------------------------------------------------------
test_diff_failure_exit() {
    if [ -f "$CI_WORKFLOW" ]; then
        # Check for diff command usage
        if grep -qE "(diff\s+-r|diff\s+--recursive)" "$CI_WORKFLOW"; then
            pass "CI-002: Workflow uses recursive diff command"
        else
            fail "CI-002: Workflow does NOT use recursive diff command"
        fi
    else
        fail "CI-002: Workflow not found, cannot check diff command"
    fi
}

test_workflow_name() {
    if [ -f "$CI_WORKFLOW" ]; then
        if grep -qE "^name:" "$CI_WORKFLOW"; then
            pass "CI-002: Workflow has name defined"
        else
            fail "CI-002: Workflow missing name definition"
        fi
    else
        fail "CI-002: Workflow not found"
    fi
}

test_workflow_jobs() {
    if [ -f "$CI_WORKFLOW" ]; then
        if grep -q "jobs:" "$CI_WORKFLOW"; then
            pass "CI-002: Workflow has jobs section"
        else
            fail "CI-002: Workflow missing jobs section"
        fi
    else
        fail "CI-002: Workflow not found"
    fi
}

# ------------------------------------------------------------------------------
# Run All Tests
# ------------------------------------------------------------------------------
echo "=========================================="
echo "STORY-313 AC#2: CI Workflow Tests"
echo "=========================================="
echo ""

test_workflow_exists
test_pull_request_trigger
test_diff_failure_exit
test_workflow_name
test_workflow_jobs

echo ""
echo "=========================================="
echo "Test Summary: $TESTS_PASSED/$TESTS_RUN passed"
echo "=========================================="

if [ $TESTS_FAILED -gt 0 ]; then
    exit 1
fi
exit 0
