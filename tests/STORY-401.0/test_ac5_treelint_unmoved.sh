#!/bin/bash
# Test AC#5: Treelint Patterns File Remains Unmoved
# STORY-401: Extract Anti-Pattern-Scanner to Reference Files
#
# Validates:
# - src/claude/agents/references/treelint-search-patterns.md exists at original location
# - File was NOT moved to anti-pattern-scanner/references/
#
# Expected: PASS initially (file already at correct location, should remain)

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SHARED_REF_FILE="$PROJECT_ROOT/src/claude/agents/references/treelint-search-patterns.md"
WRONG_LOCATION="$PROJECT_ROOT/src/claude/agents/anti-pattern-scanner/references/treelint-search-patterns.md"

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
# Test 1: Shared treelint file exists at original location
# -----------------------------------------------------------------------------
test_treelint_at_original_location() {
    local test_name="treelint-search-patterns.md at shared references location"

    if [ -f "$SHARED_REF_FILE" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "File not found at: $SHARED_REF_FILE"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: Treelint file NOT duplicated into anti-pattern-scanner references
# -----------------------------------------------------------------------------
test_treelint_not_in_scanner_refs() {
    local test_name="treelint-search-patterns.md NOT in anti-pattern-scanner/references/"

    if [ -f "$WRONG_LOCATION" ]; then
        fail_test "$test_name" "File incorrectly duplicated to: $WRONG_LOCATION"
    else
        pass_test "$test_name"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: Shared references directory still exists
# -----------------------------------------------------------------------------
test_shared_refs_dir_exists() {
    local test_name="Shared references directory exists"

    local shared_dir="$PROJECT_ROOT/src/claude/agents/references"

    if [ -d "$shared_dir" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Shared references directory missing: $shared_dir"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-401 AC#5: Treelint Patterns Unmoved"
echo "=============================================="
echo "Expected location: $SHARED_REF_FILE"
echo "----------------------------------------------"
echo ""

run_test "1" test_treelint_at_original_location
run_test "2" test_treelint_not_in_scanner_refs
run_test "3" test_shared_refs_dir_exists

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
