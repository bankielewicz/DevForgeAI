#!/bin/bash
# Test AC#5: Summary Report for Multiple Violations
# STORY-335: Add Subagent Size Enforcement Mechanism
#
# Validates:
# - Pre-commit hook displays summary table for multiple violations
# - CI workflow displays summary table for multiple violations
# - Table format includes: File, Lines, Threshold, Status columns
# - Aggregated exit code: 0 for warnings only, 1 if any failures
# - Warning status shown with emoji or text indicator
# - Failure status shown with emoji or text indicator
#
# Expected: FAIL initially (TDD Red phase - implementation does not exist yet)

# Note: Not using set -e due to arithmetic operations with (( ))

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
HOOK_SCRIPT="$PROJECT_ROOT/.claude/hooks/pre-commit-subagent-size.sh"
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
# Test 1: Hook script contains summary table header
# -----------------------------------------------------------------------------
test_hook_summary_header() {
    local test_name="Hook contains summary table header"

    if [ ! -f "$HOOK_SCRIPT" ]; then
        fail_test "$test_name" "Cannot check - hook script does not exist"
        return
    fi

    # Check for table header like "Subagent Size Violations:" or similar
    if grep -qiE "Subagent.*Size.*Violation|Size.*Violation.*Report|Violation.*Summary" "$HOOK_SCRIPT"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Summary table header not found in hook"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: Hook script contains table column headers
# -----------------------------------------------------------------------------
test_hook_table_columns() {
    local test_name="Hook contains table with File/Lines/Threshold/Status columns"

    if [ ! -f "$HOOK_SCRIPT" ]; then
        fail_test "$test_name" "Cannot check - hook script does not exist"
        return
    fi

    # Check for table column headers (File, Lines, Threshold, Status)
    local has_file=false
    local has_lines=false
    local has_threshold=false
    local has_status=false

    if grep -qiE "File" "$HOOK_SCRIPT"; then has_file=true; fi
    if grep -qiE "Lines" "$HOOK_SCRIPT"; then has_lines=true; fi
    if grep -qiE "Threshold" "$HOOK_SCRIPT"; then has_threshold=true; fi
    if grep -qiE "Status" "$HOOK_SCRIPT"; then has_status=true; fi

    if [ "$has_file" = true ] && [ "$has_lines" = true ] && [ "$has_threshold" = true ] && [ "$has_status" = true ]; then
        pass_test "$test_name"
    else
        local missing=""
        if [ "$has_file" = false ]; then missing="File "; fi
        if [ "$has_lines" = false ]; then missing="${missing}Lines "; fi
        if [ "$has_threshold" = false ]; then missing="${missing}Threshold "; fi
        if [ "$has_status" = false ]; then missing="${missing}Status "; fi
        fail_test "$test_name" "Missing columns: $missing"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: Hook script uses markdown table format
# -----------------------------------------------------------------------------
test_hook_markdown_table() {
    local test_name="Hook uses markdown table format (pipe separators)"

    if [ ! -f "$HOOK_SCRIPT" ]; then
        fail_test "$test_name" "Cannot check - hook script does not exist"
        return
    fi

    # Check for markdown table pipe separator pattern
    if grep -qE "\|.*\|.*\|" "$HOOK_SCRIPT"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Markdown table format (| col | col |) not found"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Hook script contains warning indicator
# -----------------------------------------------------------------------------
test_hook_warning_indicator() {
    local test_name="Hook contains warning indicator (emoji or text)"

    if [ ! -f "$HOOK_SCRIPT" ]; then
        fail_test "$test_name" "Cannot check - hook script does not exist"
        return
    fi

    # Check for warning indicator (emoji or WARNING text)
    if grep -qE "WARNING|WARN|\\\\u26A0|:warning:" "$HOOK_SCRIPT"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Warning indicator not found"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: Hook script contains failure indicator
# -----------------------------------------------------------------------------
test_hook_failure_indicator() {
    local test_name="Hook contains failure indicator (emoji or text)"

    if [ ! -f "$HOOK_SCRIPT" ]; then
        fail_test "$test_name" "Cannot check - hook script does not exist"
        return
    fi

    # Check for failure indicator (emoji or FAILED text)
    if grep -qE "FAILED|FAIL|ERROR|\\\\u274C|:x:" "$HOOK_SCRIPT"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Failure indicator not found"
    fi
}

# -----------------------------------------------------------------------------
# Test 6: Hook script has aggregated exit code logic
# -----------------------------------------------------------------------------
test_hook_aggregated_exit() {
    local test_name="Hook has aggregated exit code logic (0 for warnings, 1 for failures)"

    if [ ! -f "$HOOK_SCRIPT" ]; then
        fail_test "$test_name" "Cannot check - hook script does not exist"
        return
    fi

    # Check for exit code tracking variable and conditional exit
    local has_exit_0=false
    local has_exit_1=false

    if grep -qE "exit[[:space:]]+0" "$HOOK_SCRIPT"; then has_exit_0=true; fi
    if grep -qE "exit[[:space:]]+1" "$HOOK_SCRIPT"; then has_exit_1=true; fi

    if [ "$has_exit_0" = true ] && [ "$has_exit_1" = true ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Exit code logic incomplete (need both exit 0 and exit 1)"
    fi
}

# -----------------------------------------------------------------------------
# Test 7: CI workflow contains summary table logic
# -----------------------------------------------------------------------------
test_workflow_summary_logic() {
    local test_name="CI workflow contains summary table logic"

    if [ ! -f "$WORKFLOW_FILE" ]; then
        fail_test "$test_name" "Cannot check - workflow does not exist"
        return
    fi

    # Check for summary/table/report logic in workflow
    if grep -qiE "summary|report|table|\|.*\|" "$WORKFLOW_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Summary table logic not found in workflow"
    fi
}

# -----------------------------------------------------------------------------
# Test 8: CI workflow has failure tracking variable
# -----------------------------------------------------------------------------
test_workflow_failure_tracking() {
    local test_name="CI workflow tracks failures for aggregated exit"

    if [ ! -f "$WORKFLOW_FILE" ]; then
        fail_test "$test_name" "Cannot check - workflow does not exist"
        return
    fi

    # Check for failure tracking variable (e.g., HAS_FAILURE=, FAILED_COUNT=, etc.)
    if grep -qE "FAIL.*=|HAS_FAIL|fail_count|VIOLATION" "$WORKFLOW_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Failure tracking variable not found"
    fi
}

# -----------------------------------------------------------------------------
# Test 9: Hook handles multiple files in single commit
# -----------------------------------------------------------------------------
test_hook_multiple_files() {
    local test_name="Hook handles multiple files (loops through files)"

    if [ ! -f "$HOOK_SCRIPT" ]; then
        fail_test "$test_name" "Cannot check - hook script does not exist"
        return
    fi

    # Check for loop construct (for, while) to handle multiple files
    if grep -qE "for[[:space:]]|while[[:space:]]|do$|done$" "$HOOK_SCRIPT"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No loop construct found for handling multiple files"
    fi
}

# -----------------------------------------------------------------------------
# Test 10: Both hook and workflow display consistent output format
# -----------------------------------------------------------------------------
test_consistent_output_format() {
    local test_name="Hook and workflow use consistent output format"

    if [ ! -f "$HOOK_SCRIPT" ] || [ ! -f "$WORKFLOW_FILE" ]; then
        fail_test "$test_name" "Cannot check - one or both files do not exist"
        return
    fi

    # Check both use similar indicators for warnings/failures
    local hook_has_warning=false
    local workflow_has_warning=false
    local hook_has_failure=false
    local workflow_has_failure=false

    if grep -qiE "WARNING|WARN" "$HOOK_SCRIPT"; then hook_has_warning=true; fi
    if grep -qiE "WARNING|WARN" "$WORKFLOW_FILE"; then workflow_has_warning=true; fi
    if grep -qiE "FAILED|FAIL" "$HOOK_SCRIPT"; then hook_has_failure=true; fi
    if grep -qiE "FAILED|FAIL" "$WORKFLOW_FILE"; then workflow_has_failure=true; fi

    if [ "$hook_has_warning" = "$workflow_has_warning" ] && [ "$hook_has_failure" = "$workflow_has_failure" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Output format inconsistent between hook and workflow"
    fi
}

# -----------------------------------------------------------------------------
# Test 11: Summary table header mentions "Subagent Size Violations"
# -----------------------------------------------------------------------------
test_exact_summary_title() {
    local test_name="Summary uses exact title 'Subagent Size Violations'"

    if [ ! -f "$HOOK_SCRIPT" ]; then
        fail_test "$test_name" "Cannot check - hook script does not exist"
        return
    fi

    if grep -qE "Subagent Size Violations" "$HOOK_SCRIPT"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Exact title 'Subagent Size Violations' not found"
    fi
}

# -----------------------------------------------------------------------------
# Test 12: Hook accumulates violations before displaying summary
# -----------------------------------------------------------------------------
test_violation_accumulation() {
    local test_name="Hook accumulates violations before displaying summary"

    if [ ! -f "$HOOK_SCRIPT" ]; then
        fail_test "$test_name" "Cannot check - hook script does not exist"
        return
    fi

    # Check for array or accumulator variable pattern
    if grep -qE "\+=|VIOLATIONS|violations|append|accumulate" "$HOOK_SCRIPT"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No violation accumulation pattern found"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-335 AC#5: Summary Report for Multiple Violations"
echo "=============================================="
echo "Hook script: $HOOK_SCRIPT"
echo "Workflow: $WORKFLOW_FILE"
echo "Expected: Table format with File|Lines|Threshold|Status columns"
echo "----------------------------------------------"
echo ""

run_test "1" test_hook_summary_header
run_test "2" test_hook_table_columns
run_test "3" test_hook_markdown_table
run_test "4" test_hook_warning_indicator
run_test "5" test_hook_failure_indicator
run_test "6" test_hook_aggregated_exit
run_test "7" test_workflow_summary_logic
run_test "8" test_workflow_failure_tracking
run_test "9" test_hook_multiple_files
run_test "10" test_consistent_output_format
run_test "11" test_exact_summary_title
run_test "12" test_violation_accumulation

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
