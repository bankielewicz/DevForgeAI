#!/bin/bash
# Test AC#3: Missing Optional Section Triggers WARNING
# STORY-389: Update Agent-Generator with Template Compliance Enforcement
#
# Validates that agent-generator.md and/or template-compliance-validation.md contain:
# - WARNING (not BLOCK) for missing optional sections
# - Write() proceeds despite missing optional section
# - Category detection (Validator, Implementor, Analyzer, Formatter)
# - PASS WITH WARNINGS status
# - Suggestion per missing optional section
#
# Expected: FAIL initially (TDD Red phase - WARNING logic not yet implemented)

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
# Test 1: WARNING status for optional sections
# -----------------------------------------------------------------------------
test_warning_for_optional() {
    local test_name="WARNING status for missing optional sections"

    if search_both_files "(WARNING|WARN).*(optional|category)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No WARNING status for missing optional sections"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: Write() proceeds despite optional missing
# -----------------------------------------------------------------------------
test_write_proceeds() {
    local test_name="Write() proceeds despite missing optional section"

    if search_both_files "(does NOT block|proceed|allow).*(Write|writing|optional)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No logic allowing Write() to proceed when optional sections missing"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: Category detection - Validator
# -----------------------------------------------------------------------------
test_category_validator() {
    local test_name="Category detection: Validator"

    if search_both_files "Validator"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No 'Validator' category reference found"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Category detection - Implementor
# -----------------------------------------------------------------------------
test_category_implementor() {
    local test_name="Category detection: Implementor"

    if search_both_files "Implementor"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No 'Implementor' category reference found"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: Category detection - Analyzer
# -----------------------------------------------------------------------------
test_category_analyzer() {
    local test_name="Category detection: Analyzer"

    if search_both_files "Analyzer"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No 'Analyzer' category reference found"
    fi
}

# -----------------------------------------------------------------------------
# Test 6: Category detection - Formatter
# -----------------------------------------------------------------------------
test_category_formatter() {
    local test_name="Category detection: Formatter"

    if search_both_files "Formatter"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No 'Formatter' category reference found"
    fi
}

# -----------------------------------------------------------------------------
# Test 7: PASS WITH WARNINGS status
# -----------------------------------------------------------------------------
test_pass_with_warnings_status() {
    local test_name="PASS WITH WARNINGS status defined"

    if search_both_files "PASS WITH WARNINGS"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No 'PASS WITH WARNINGS' status found"
    fi
}

# -----------------------------------------------------------------------------
# Test 8: Category-specific optional sections identified
# -----------------------------------------------------------------------------
test_category_specific_sections() {
    local test_name="Category-specific optional sections identified"

    if search_both_files "(category.specific|optional section).*(detect|identif|list)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No logic to identify category-specific optional sections"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-389 AC#3: Warning Missing Optional"
echo "=============================================="
echo "Agent-generator: $AGENT_GENERATOR"
echo "Compliance ref: $COMPLIANCE_REF"
echo "----------------------------------------------"
echo ""

run_test "1" test_warning_for_optional
run_test "2" test_write_proceeds
run_test "3" test_category_validator
run_test "4" test_category_implementor
run_test "5" test_category_analyzer
run_test "6" test_category_formatter
run_test "7" test_pass_with_warnings_status
run_test "8" test_category_specific_sections

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
