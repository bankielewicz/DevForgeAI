#!/bin/bash
# Test AC#2: Missing Required Section Triggers BLOCK
# STORY-389: Update Agent-Generator with Template Compliance Enforcement
#
# Validates that agent-generator.md and/or template-compliance-validation.md contain:
# - BLOCK result with status TEMPLATE_COMPLIANCE_FAILED
# - Logic to halt Write() on missing required section
# - Lists each missing section by heading name
# - Remediation message per missing section
# - Auto-fix option via AskUserQuestion
#
# Expected: FAIL initially (TDD Red phase - BLOCK logic not yet implemented)

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

# Helper: search both agent-generator and compliance reference
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
# Test 1: TEMPLATE_COMPLIANCE_FAILED status defined
# -----------------------------------------------------------------------------
test_block_status_defined() {
    local test_name="TEMPLATE_COMPLIANCE_FAILED status defined"

    if search_both_files "TEMPLATE_COMPLIANCE_FAILED"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No TEMPLATE_COMPLIANCE_FAILED status found in agent-generator or compliance ref"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: Write() halted on missing required section
# -----------------------------------------------------------------------------
test_write_halted_on_missing() {
    local test_name="Write() halted on missing required section"

    if search_both_files "(halt|block|stop|prevent).*(Write|writing)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No logic to halt Write() when required section missing"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: BLOCK result lists missing section names
# -----------------------------------------------------------------------------
test_block_lists_section_names() {
    local test_name="BLOCK result lists each missing section by name"

    if search_both_files "(list|display|output|report).*(missing|absent).*(section|heading)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No logic to list missing section names in BLOCK result"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Remediation message per missing section
# -----------------------------------------------------------------------------
test_remediation_messages() {
    local test_name="Remediation message provided per missing section"

    if search_both_files "remediation"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No 'remediation' message logic found"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: Auto-fix option offered via AskUserQuestion
# -----------------------------------------------------------------------------
test_auto_fix_option() {
    local test_name="Auto-fix option offered via AskUserQuestion"

    if search_both_files "auto.?fix"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No auto-fix option found"
    fi
}

# -----------------------------------------------------------------------------
# Test 6: AskUserQuestion with three options (apply, show, cancel)
# -----------------------------------------------------------------------------
test_ask_user_question_options() {
    local test_name="AskUserQuestion with apply/show/cancel options"

    if search_both_files "AskUserQuestion"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No AskUserQuestion invocation for auto-fix decision"
    fi
}

# -----------------------------------------------------------------------------
# Test 7: BLOCK is specifically for required sections (not optional)
# -----------------------------------------------------------------------------
test_block_required_only() {
    local test_name="BLOCK applies specifically to required sections"

    if search_both_files "(required|mandatory).*(BLOCK|block|halt)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No explicit link between 'required sections' and BLOCK action"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-389 AC#2: Block Missing Required Section"
echo "=============================================="
echo "Agent-generator: $AGENT_GENERATOR"
echo "Compliance ref: $COMPLIANCE_REF"
echo "----------------------------------------------"
echo ""

run_test "1" test_block_status_defined
run_test "2" test_write_halted_on_missing
run_test "3" test_block_lists_section_names
run_test "4" test_remediation_messages
run_test "5" test_auto_fix_option
run_test "6" test_ask_user_question_options
run_test "7" test_block_required_only

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
