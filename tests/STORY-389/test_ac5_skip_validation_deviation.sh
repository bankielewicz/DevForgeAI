#!/bin/bash
# Test AC#5: Emergency Skip-Validation Bypass Logs Deviation
# STORY-389: Update Agent-Generator with Template Compliance Enforcement
#
# Validates that agent-generator.md and/or template-compliance-validation.md contain:
# - skip-validation directive handling
# - AskUserQuestion prompt for justification
# - Minimum 10 character justification requirement
# - Deviation record with bypass_date, justification, bypassed_checks, operator
# - Warning-severity observation capture
# - DEVIATION banner in summary report
#
# Expected: FAIL initially (TDD Red phase - bypass logic not yet implemented)

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
AGENT_GENERATOR="$PROJECT_ROOT/src/claude/agents/agent-generator.md"
COMPLIANCE_REF="$PROJECT_ROOT/src/claude/agents/agent-generator/references/template-compliance-validation.md"

# Test tracking
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

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

# Helper: search both files
search_both_files() {
    local pattern="$1"
    local found=false

    if [ -f "$AGENT_GENERATOR" ] && grep -qiE "$pattern" "$AGENT_GENERATOR"; then
        found=true
    fi
    if [ -f "$COMPLIANCE_REF" ] && grep -qiE "$pattern" "$COMPLIANCE_REF"; then
        found=true
    fi

    $found
}

# -----------------------------------------------------------------------------
# Test 1: skip-validation directive handling
# -----------------------------------------------------------------------------
test_skip_validation_directive() {
    local test_name="skip-validation directive handling"

    if search_both_files "skip.?validation"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No skip-validation directive found"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: AskUserQuestion for justification
# -----------------------------------------------------------------------------
test_justification_prompt() {
    local test_name="AskUserQuestion prompt for justification"

    if search_both_files "justification"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No justification prompt found"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: Minimum 10 character justification requirement
# -----------------------------------------------------------------------------
test_minimum_justification_length() {
    local test_name="Minimum 10 character justification requirement"

    if search_both_files "(10|ten).*(char|character|minimum)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No 10 character minimum justification requirement found"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Deviation record contains bypass_date
# -----------------------------------------------------------------------------
test_deviation_bypass_date() {
    local test_name="Deviation record contains bypass_date"

    if search_both_files "bypass_date"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No bypass_date field in deviation record"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: Deviation record contains justification field
# -----------------------------------------------------------------------------
test_deviation_justification_field() {
    local test_name="Deviation record contains justification field"

    if search_both_files "deviation.*(justification|record)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No justification field in deviation record"
    fi
}

# -----------------------------------------------------------------------------
# Test 6: Deviation record contains bypassed_checks
# -----------------------------------------------------------------------------
test_deviation_bypassed_checks() {
    local test_name="Deviation record contains bypassed_checks"

    if search_both_files "bypassed_checks"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No bypassed_checks field in deviation record"
    fi
}

# -----------------------------------------------------------------------------
# Test 7: Deviation record contains operator
# -----------------------------------------------------------------------------
test_deviation_operator() {
    local test_name="Deviation record contains operator field"

    if search_both_files "operator"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No operator field in deviation record"
    fi
}

# -----------------------------------------------------------------------------
# Test 8: Warning-severity observation captured
# -----------------------------------------------------------------------------
test_warning_observation() {
    local test_name="Warning-severity observation captured"

    if search_both_files "warning.*(observation|severity|capture)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No warning-severity observation capture for bypass"
    fi
}

# -----------------------------------------------------------------------------
# Test 9: DEVIATION banner in summary report
# -----------------------------------------------------------------------------
test_deviation_banner() {
    local test_name="DEVIATION banner in summary report"

    if search_both_files "DEVIATION.*(banner|report|summary)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No DEVIATION banner defined for summary report"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-389 AC#5: Skip Validation Deviation"
echo "=============================================="
echo "Agent-generator: $AGENT_GENERATOR"
echo "Compliance ref: $COMPLIANCE_REF"
echo "----------------------------------------------"
echo ""

run_test "1" test_skip_validation_directive
run_test "2" test_justification_prompt
run_test "3" test_minimum_justification_length
run_test "4" test_deviation_bypass_date
run_test "5" test_deviation_justification_field
run_test "6" test_deviation_bypassed_checks
run_test "7" test_deviation_operator
run_test "8" test_warning_observation
run_test "9" test_deviation_banner

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
