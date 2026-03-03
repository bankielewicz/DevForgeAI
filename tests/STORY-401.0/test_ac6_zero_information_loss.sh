#!/bin/bash
# Test AC#6: Zero Information Loss
# STORY-401: Extract Anti-Pattern-Scanner to Reference Files
#
# Validates:
# - Combined content of core + reference files contains all key sections
#   from the original 703-line file
# - Specific section headers and key content markers verified
# - No critical content dropped during extraction
#
# Expected: FAIL initially (TDD Red phase - reference files do not exist yet)

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
CORE_FILE="$PROJECT_ROOT/src/claude/agents/anti-pattern-scanner.md"
REF_DIR="$PROJECT_ROOT/src/claude/agents/anti-pattern-scanner/references"
REF_FILE_1="$REF_DIR/integration-testing-guide.md"
REF_FILE_2="$REF_DIR/metrics-reference.md"

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

# Helper: search combined content for a pattern
combined_contains() {
    local pattern="$1"

    if grep -q "$pattern" "$CORE_FILE" 2>/dev/null; then
        return 0
    fi
    if [ -f "$REF_FILE_1" ] && grep -q "$pattern" "$REF_FILE_1" 2>/dev/null; then
        return 0
    fi
    if [ -f "$REF_FILE_2" ] && grep -q "$pattern" "$REF_FILE_2" 2>/dev/null; then
        return 0
    fi
    return 1
}

# -----------------------------------------------------------------------------
# Test 1: All reference files exist (prerequisite for information loss check)
# -----------------------------------------------------------------------------
test_all_files_exist() {
    local test_name="All source files exist for combined check"

    local missing=""

    if [ ! -f "$CORE_FILE" ]; then
        missing="$missing core-file"
    fi
    if [ ! -f "$REF_FILE_1" ]; then
        missing="$missing integration-testing-guide.md"
    fi
    if [ ! -f "$REF_FILE_2" ]; then
        missing="$missing metrics-reference.md"
    fi

    if [ -z "$missing" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Missing files:$missing"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: Integration with devforgeai-qa content preserved
# -----------------------------------------------------------------------------
test_qa_integration_preserved() {
    local test_name="Integration with devforgeai-qa content preserved"

    if combined_contains "devforgeai-qa"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "devforgeai-qa integration content lost"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: Testing section content preserved
# -----------------------------------------------------------------------------
test_testing_content_preserved() {
    local test_name="Testing section content preserved"

    if combined_contains "## Testing"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Testing section content lost"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Token Efficiency content preserved
# -----------------------------------------------------------------------------
test_token_efficiency_preserved() {
    local test_name="Token Efficiency content preserved"

    if combined_contains "Token Efficiency"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Token Efficiency content lost"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: Performance Targets content preserved
# -----------------------------------------------------------------------------
test_performance_targets_preserved() {
    local test_name="Performance Targets content preserved"

    if combined_contains "Performance Targets"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Performance Targets content lost"
    fi
}

# -----------------------------------------------------------------------------
# Test 6: Success Criteria content preserved
# -----------------------------------------------------------------------------
test_success_criteria_preserved() {
    local test_name="Success Criteria content preserved"

    if combined_contains "Success Criteria"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Success Criteria content lost"
    fi
}

# -----------------------------------------------------------------------------
# Test 7: Context Summary Format content preserved
# -----------------------------------------------------------------------------
test_context_summary_preserved() {
    local test_name="Context Summary Format content preserved"

    if combined_contains "Context Summary Format"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Context Summary Format content lost"
    fi
}

# -----------------------------------------------------------------------------
# Test 8: Related Context Files content preserved
# -----------------------------------------------------------------------------
test_related_context_files_preserved() {
    local test_name="Related Context Files content preserved"

    if combined_contains "Related Context Files"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Related Context Files content lost"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-401 AC#6: Zero Information Loss"
echo "=============================================="
echo "Core file: $CORE_FILE"
echo "Reference files: $REF_DIR/"
echo "----------------------------------------------"
echo ""

run_test "1" test_all_files_exist
run_test "2" test_qa_integration_preserved
run_test "3" test_testing_content_preserved
run_test "4" test_token_efficiency_preserved
run_test "5" test_performance_targets_preserved
run_test "6" test_success_criteria_preserved
run_test "7" test_context_summary_preserved
run_test "8" test_related_context_files_preserved

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
