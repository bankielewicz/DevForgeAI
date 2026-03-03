#!/bin/bash
# Test AC#2: CI Check for Hard Failure
# STORY-335: Add Subagent Size Enforcement Mechanism
#
# Validates:
# - GitHub Actions workflow exists at .github/workflows/subagent-size-check.yml
# - Workflow triggers on pull_request events
# - Workflow has correct paths filter for agents directories
# - Workflow fails (exit 1) for files exceeding 600 lines
# - Error message contains expected text
#
# Expected: FAIL initially (TDD Red phase - workflow does not exist yet)

# Note: Not using set -e due to arithmetic operations with (( ))

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
WORKFLOW_FILE="$PROJECT_ROOT/.github/workflows/subagent-size-check.yml"

# Test tracking
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test helper functions
pass_test() {
    local test_name="$1"
    TESTS_PASSED=$((TESTS_PASSED + 1))
    echo "[PASS] $test_name"
}

fail_test() {
    local test_name="$1"
    local message="$2"
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo "[FAIL] $test_name: $message"
}

run_test() {
    local test_name="$1"
    TESTS_RUN=$((TESTS_RUN + 1))
    shift
    "$@"
}

# -----------------------------------------------------------------------------
# Test 1: Workflow file exists
# -----------------------------------------------------------------------------
test_workflow_exists() {
    local test_name="CI workflow file exists"
    if [ -f "$WORKFLOW_FILE" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "File not found: $WORKFLOW_FILE"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: Workflow has correct name
# -----------------------------------------------------------------------------
test_workflow_name() {
    local test_name="Workflow has name: Subagent Size Check"

    if [ ! -f "$WORKFLOW_FILE" ]; then
        fail_test "$test_name" "Cannot check - workflow does not exist"
        return
    fi

    if grep -qE "^name:[[:space:]]*['\"]?Subagent Size Check['\"]?" "$WORKFLOW_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Workflow name not found or incorrect"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: Workflow triggers on pull_request
# -----------------------------------------------------------------------------
test_pull_request_trigger() {
    local test_name="Workflow triggers on pull_request"

    if [ ! -f "$WORKFLOW_FILE" ]; then
        fail_test "$test_name" "Cannot check - workflow does not exist"
        return
    fi

    if grep -qE "^[[:space:]]*pull_request:" "$WORKFLOW_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "pull_request trigger not found"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Workflow has paths filter for src/claude/agents/
# -----------------------------------------------------------------------------
test_paths_filter_src() {
    local test_name="Workflow has paths filter for src/claude/agents/"

    if [ ! -f "$WORKFLOW_FILE" ]; then
        fail_test "$test_name" "Cannot check - workflow does not exist"
        return
    fi

    if grep -qE "src/claude/agents/.*\.md" "$WORKFLOW_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "paths filter for src/claude/agents/*.md not found"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: Workflow has paths filter for .claude/agents/
# -----------------------------------------------------------------------------
test_paths_filter_claude() {
    local test_name="Workflow has paths filter for .claude/agents/"

    if [ ! -f "$WORKFLOW_FILE" ]; then
        fail_test "$test_name" "Cannot check - workflow does not exist"
        return
    fi

    if grep -qE "\.claude/agents/.*\.md" "$WORKFLOW_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "paths filter for .claude/agents/*.md not found"
    fi
}

# -----------------------------------------------------------------------------
# Test 6: Workflow contains checkout step
# -----------------------------------------------------------------------------
test_checkout_step() {
    local test_name="Workflow contains checkout step"

    if [ ! -f "$WORKFLOW_FILE" ]; then
        fail_test "$test_name" "Cannot check - workflow does not exist"
        return
    fi

    if grep -qE "uses:[[:space:]]*actions/checkout" "$WORKFLOW_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "actions/checkout step not found"
    fi
}

# -----------------------------------------------------------------------------
# Test 7: Workflow contains 600-line threshold check
# -----------------------------------------------------------------------------
test_600_line_threshold() {
    local test_name="Workflow contains 600-line threshold check"

    if [ ! -f "$WORKFLOW_FILE" ]; then
        fail_test "$test_name" "Cannot check - workflow does not exist"
        return
    fi

    if grep -qE "600" "$WORKFLOW_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "600-line threshold not found in workflow"
    fi
}

# -----------------------------------------------------------------------------
# Test 8: Workflow contains exit 1 for failures
# -----------------------------------------------------------------------------
test_exit_code_one() {
    local test_name="Workflow contains exit 1 for threshold violations"

    if [ ! -f "$WORKFLOW_FILE" ]; then
        fail_test "$test_name" "Cannot check - workflow does not exist"
        return
    fi

    if grep -qE "exit[[:space:]]+1" "$WORKFLOW_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "exit 1 not found in workflow"
    fi
}

# -----------------------------------------------------------------------------
# Test 9: Workflow contains failure message with FAILED
# -----------------------------------------------------------------------------
test_failure_message() {
    local test_name="Workflow contains FAILED error message"

    if [ ! -f "$WORKFLOW_FILE" ]; then
        fail_test "$test_name" "Cannot check - workflow does not exist"
        return
    fi

    if grep -qE "FAILED|exceeds.*600.*line.*maximum" "$WORKFLOW_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "FAILED error message not found in workflow"
    fi
}

# -----------------------------------------------------------------------------
# Test 10: Workflow excludes references/ directories
# -----------------------------------------------------------------------------
test_references_exclusion() {
    local test_name="Workflow excludes references/ directories"

    if [ ! -f "$WORKFLOW_FILE" ]; then
        fail_test "$test_name" "Cannot check - workflow does not exist"
        return
    fi

    if grep -qE "references/|-not.*path.*references" "$WORKFLOW_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "references/ exclusion not found in workflow"
    fi
}

# -----------------------------------------------------------------------------
# Test 11: Workflow references ADR-012
# -----------------------------------------------------------------------------
test_adr_012_reference() {
    local test_name="Workflow references ADR-012"

    if [ ! -f "$WORKFLOW_FILE" ]; then
        fail_test "$test_name" "Cannot check - workflow does not exist"
        return
    fi

    if grep -qE "ADR-012|ADR012" "$WORKFLOW_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "ADR-012 reference not found in workflow"
    fi
}

# -----------------------------------------------------------------------------
# Test 12: Workflow uses wc -l for line counting
# -----------------------------------------------------------------------------
test_wc_line_counting() {
    local test_name="Workflow uses wc -l for line counting"

    if [ ! -f "$WORKFLOW_FILE" ]; then
        fail_test "$test_name" "Cannot check - workflow does not exist"
        return
    fi

    if grep -qE "wc[[:space:]]+-l|wc[[:space:]]+.*-l" "$WORKFLOW_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "wc -l command not found in workflow"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-335 AC#2: CI Check for Hard Failure"
echo "=============================================="
echo "Target workflow: $WORKFLOW_FILE"
echo "Fail threshold: 600 lines"
echo "Expected behavior: Block PR, exit 1"
echo "----------------------------------------------"
echo ""

run_test "1" test_workflow_exists
run_test "2" test_workflow_name
run_test "3" test_pull_request_trigger
run_test "4" test_paths_filter_src
run_test "5" test_paths_filter_claude
run_test "6" test_checkout_step
run_test "7" test_600_line_threshold
run_test "8" test_exit_code_one
run_test "9" test_failure_message
run_test "10" test_references_exclusion
run_test "11" test_adr_012_reference
run_test "12" test_wc_line_counting

echo ""
echo "=============================================="
echo "Test Summary: $TESTS_PASSED/$TESTS_RUN passed"
echo "=============================================="

if [ "$TESTS_FAILED" -gt 0 ]; then
    echo "Status: FAILED ($TESTS_FAILED failures)"
    exit 1
else
    echo "Status: PASSED"
    exit 0
fi
