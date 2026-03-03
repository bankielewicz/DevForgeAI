#!/bin/bash
# Test AC#1: Legacy Grep god class method threshold updated to >20
# STORY-405: Unify God Class Threshold to >20 Methods
#
# Validates:
# - No references to ">15 methods" remain in anti-pattern-scanner.md
# - No references to ">15 methods" remain in phase5-code-smells.md
# - No references to ">15 methods" remain in phase1-context-loading.md
#
# Expected: FAIL initially (TDD Red phase - files currently use >15)

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SCANNER_FILE="$PROJECT_ROOT/src/claude/agents/anti-pattern-scanner.md"
PHASE5_FILE="$PROJECT_ROOT/src/claude/docs/agents/anti-pattern-scanner/phase5-code-smells.md"
PHASE1_FILE="$PROJECT_ROOT/src/claude/docs/agents/anti-pattern-scanner/phase1-context-loading.md"

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
# Test 1: anti-pattern-scanner.md has zero references to ">15 methods"
# -----------------------------------------------------------------------------
test_scanner_no_15_methods() {
    local test_name="anti-pattern-scanner.md has zero '>15 methods' references"
    local match_count
    match_count=$(grep -c ">15 methods" "$SCANNER_FILE" 2>/dev/null)
    match_count=${match_count:-0}
    if [ "$match_count" -eq 0 ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Found $match_count references to '>15 methods'"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: phase5-code-smells.md has zero references to ">15 methods"
# -----------------------------------------------------------------------------
test_phase5_no_15_methods() {
    local test_name="phase5-code-smells.md has zero '>15 methods' references"
    local match_count
    match_count=$(grep -c ">15 methods" "$PHASE5_FILE" 2>/dev/null)
    match_count=${match_count:-0}
    if [ "$match_count" -eq 0 ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Found $match_count references to '>15 methods'"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: phase1-context-loading.md has zero references to ">15 methods"
# -----------------------------------------------------------------------------
test_phase1_no_15_methods() {
    local test_name="phase1-context-loading.md has zero '>15 methods' references"
    local match_count
    match_count=$(grep -c ">15 methods" "$PHASE1_FILE" 2>/dev/null)
    match_count=${match_count:-0}
    if [ "$match_count" -eq 0 ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Found $match_count references to '>15 methods'"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: anti-pattern-scanner.md contains ">20 methods" (replacement present)
# -----------------------------------------------------------------------------
test_scanner_has_20_methods() {
    local test_name="anti-pattern-scanner.md contains '>20 methods'"
    local match_count
    match_count=$(grep -c ">20 methods" "$SCANNER_FILE" 2>/dev/null)
    match_count=${match_count:-0}
    if [ "$match_count" -ge 1 ]; then
        pass_test "$test_name (found $match_count references)"
    else
        fail_test "$test_name" "No references to '>20 methods' found"
    fi
}

echo "=============================================="
echo "STORY-405 AC#1: Legacy Grep Threshold Updated"
echo "=============================================="
echo ""

run_test "1" test_scanner_no_15_methods
run_test "2" test_phase5_no_15_methods
run_test "3" test_phase1_no_15_methods
run_test "4" test_scanner_has_20_methods

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
