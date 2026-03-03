#!/bin/bash
# Test AC#3: Both detection modes produce identical results
# STORY-405: Unify God Class Threshold to >20 Methods
#
# Validates:
# - anti-pattern-scanner.md Phase 5 uses >20 in detection logic
# - phase5-code-smells.md uses >20 in detection logic
# - Both files agree on the same threshold value
#
# Expected: FAIL initially (TDD Red phase - files currently use >15)

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SCANNER_FILE="$PROJECT_ROOT/src/claude/agents/anti-pattern-scanner.md"
PHASE5_FILE="$PROJECT_ROOT/src/claude/docs/agents/anti-pattern-scanner/phase5-code-smells.md"
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
# Test 1: anti-pattern-scanner.md Phase 5 uses >20 for god class detection
# -----------------------------------------------------------------------------
test_scanner_phase5_uses_20() {
    local test_name="Scanner Phase 5 god class check uses >20"
    # Check that Category 4 / Phase 5 detection uses >20
    if grep -q ">20 methods" "$SCANNER_FILE" 2>/dev/null; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Phase 5 does not use '>20 methods' threshold"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: phase5-code-smells.md Check 1 uses >20
# -----------------------------------------------------------------------------
test_phase5_check1_uses_20() {
    local test_name="phase5-code-smells.md Check 1 uses >20"
    if grep -q ">20 methods" "$PHASE5_FILE" 2>/dev/null; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Check 1 does not use '>20 methods' threshold"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: phase5-code-smells.md detection logic uses method_count > 20
# -----------------------------------------------------------------------------
test_phase5_detection_logic_20() {
    local test_name="phase5-code-smells.md detection uses 'method_count > 20'"
    if grep -q "method_count > 20" "$PHASE5_FILE" 2>/dev/null; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Detection logic does not use 'method_count > 20'"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Scanner and Treelint use same threshold (both >20)
# -----------------------------------------------------------------------------
test_thresholds_match() {
    local test_name="Scanner and Treelint use same god class threshold"
    local scanner_has_20
    local treelint_has_20
    scanner_has_20=$(grep -c ">20 methods" "$SCANNER_FILE" 2>/dev/null)
    scanner_has_20=${scanner_has_20:-0}
    treelint_has_20=$(grep -c ">20" "$TREELINT_FILE" 2>/dev/null)
    treelint_has_20=${treelint_has_20:-0}
    if [ "$scanner_has_20" -ge 1 ] && [ "$treelint_has_20" -ge 1 ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Scanner '>20 methods': $scanner_has_20, Treelint '>20': $treelint_has_20"
    fi
}

echo "=============================================="
echo "STORY-405 AC#3: Identical Detection Results"
echo "=============================================="
echo ""

run_test "1" test_scanner_phase5_uses_20
run_test "2" test_phase5_check1_uses_20
run_test "3" test_phase5_detection_logic_20
run_test "4" test_thresholds_match

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
