#!/bin/bash
# Test AC#2: Treelint god class threshold remains unchanged at >20
# STORY-405: Unify God Class Threshold to >20 Methods
#
# Validates:
# - treelint-review-patterns.md contains ">20 methods" on line 17 and/or 34
# - treelint-review-patterns.md contains ">20 methods per class"
#
# Expected: PASS (Treelint already uses >20, this is a guard test)

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TREELINT_FILE="$PROJECT_ROOT/src/claude/agents/code-reviewer/references/treelint-review-patterns.md"

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

pass_test() {
    TESTS_PASSED=$((TESTS_PASSED + 1))
    echo "[PASS] $1"
}

fail_test() {
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo "[FAIL] $1: $2"
}

run_test() {
    TESTS_RUN=$((TESTS_RUN + 1))
    shift
    "$@"
}

# -----------------------------------------------------------------------------
# Test 1: treelint-review-patterns.md exists
# -----------------------------------------------------------------------------
test_treelint_file_exists() {
    local test_name="treelint-review-patterns.md exists"
    if [ -f "$TREELINT_FILE" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "File not found: $TREELINT_FILE"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: Contains ">20" in god class detection section
# -----------------------------------------------------------------------------
test_treelint_has_20_threshold() {
    local test_name="treelint-review-patterns.md contains '>20' threshold"
    local match_count
    match_count=$(grep -c ">20" "$TREELINT_FILE" 2>/dev/null)
    match_count=${match_count:-0}
    if [ "$match_count" -ge 1 ]; then
        pass_test "$test_name (found $match_count references)"
    else
        fail_test "$test_name" "No '>20' threshold found"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: Contains ">20 methods per class" exact phrase
# -----------------------------------------------------------------------------
test_treelint_exact_threshold() {
    local test_name="treelint-review-patterns.md contains '>20 methods per class'"
    if grep -q ">20.*methods per class\|>20 methods" "$TREELINT_FILE" 2>/dev/null; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Exact phrase '>20 methods per class' not found"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Does NOT contain ">15 methods" (guard against regression)
# -----------------------------------------------------------------------------
test_treelint_no_15_threshold() {
    local test_name="treelint-review-patterns.md has no '>15 methods' references"
    local match_count
    match_count=$(grep -c ">15 methods" "$TREELINT_FILE" 2>/dev/null)
    match_count=${match_count:-0}
    if [ "$match_count" -eq 0 ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Found $match_count references to '>15 methods'"
    fi
}

echo "=============================================="
echo "STORY-405 AC#2: Treelint Threshold Unchanged"
echo "=============================================="
echo ""

run_test "1" test_treelint_file_exists
run_test "2" test_treelint_has_20_threshold
run_test "3" test_treelint_exact_threshold
run_test "4" test_treelint_no_15_threshold

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
