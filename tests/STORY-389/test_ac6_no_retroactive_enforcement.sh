#!/bin/bash
# Test AC#6: Validation Applies to New/Updated Agents Only
# STORY-389: Update Agent-Generator with Template Compliance Enforcement
#
# Validates that agent-generator.md contains:
# - Validation scoped to creation/update modes only (Single, Batch, Regenerate)
# - Validation does NOT trigger on existing agent read/list operations
# - Legacy agents continue to function without modification
# - Explicit mode scoping logic
#
# Expected: FAIL initially (TDD Red phase - mode scoping not yet implemented)

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
# Test 1: Validation scoped to new/create mode
# -----------------------------------------------------------------------------
test_scoped_to_create() {
    local test_name="Validation scoped to new/create modes"

    if search_both_files "(new|create).*(validat|trigger|scope)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No scoping of validation to create modes"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: Validation scoped to regenerate/update mode
# -----------------------------------------------------------------------------
test_scoped_to_regenerate() {
    local test_name="Validation scoped to regenerate/update mode"

    if search_both_files "(regenerat|update).*(validat|trigger|scope)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No scoping of validation to regenerate mode"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: Validation does NOT trigger on existing agent read/reference
# -----------------------------------------------------------------------------
test_no_retroactive_read() {
    local test_name="Validation NOT triggered on existing agent read/reference"

    if search_both_files "(NOT|not|never|does not).*(trigger|validate|run).*(exist|read|list|Glob|reference|legacy)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No explicit exclusion of read/list operations from validation"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Legacy agents unaffected
# -----------------------------------------------------------------------------
test_legacy_agents_unaffected() {
    local test_name="Legacy agents continue to function without modification"

    if search_both_files "(legacy|existing).*(continue|unaffect|function|without)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No statement that legacy agents are unaffected"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: Explicit mode scoping logic present
# -----------------------------------------------------------------------------
test_mode_scoping_logic() {
    local test_name="Explicit mode scoping logic present"

    # Should have conditional logic referencing generation mode and validation trigger
    if search_both_files "(IF|if|when).*(mode|Single|Batch|Regenerate).*(validat|compliance)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No conditional logic linking generation mode to validation trigger"
    fi
}

# -----------------------------------------------------------------------------
# Test 6: No retroactive enforcement statement
# -----------------------------------------------------------------------------
test_no_retroactive_statement() {
    local test_name="No retroactive enforcement statement"

    if search_both_files "(not retroactive|no retroactive|not.*(retro|backward).*enforc)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No explicit 'not retroactive' enforcement statement"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-389 AC#6: No Retroactive Enforcement"
echo "=============================================="
echo "Agent-generator: $AGENT_GENERATOR"
echo "Compliance ref: $COMPLIANCE_REF"
echo "----------------------------------------------"
echo ""

run_test "1" test_scoped_to_create
run_test "2" test_scoped_to_regenerate
run_test "3" test_no_retroactive_read
run_test "4" test_legacy_agents_unaffected
run_test "5" test_mode_scoping_logic
run_test "6" test_no_retroactive_statement

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
