#!/bin/bash
# Test AC#5: No other thresholds are modified
# STORY-405: Unify God Class Threshold to >20 Methods
#
# Validates:
# - >300 lines threshold for god class still present
# - >50 lines threshold for long methods still present
# - Magic number detection still present
# - Only method threshold changes (15->20), others intact
#
# Expected: PASS (guard test - these thresholds should not change)

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SCANNER_FILE="$PROJECT_ROOT/src/claude/agents/anti-pattern-scanner.md"
PHASE5_FILE="$PROJECT_ROOT/src/claude/docs/agents/anti-pattern-scanner/phase5-code-smells.md"

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
# Test 1: anti-pattern-scanner.md contains ">300 lines" threshold
# -----------------------------------------------------------------------------
test_scanner_300_lines() {
    local test_name="Scanner retains '>300 lines' threshold"
    if grep -q ">300 lines" "$SCANNER_FILE" 2>/dev/null; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "'>300 lines' threshold missing"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: anti-pattern-scanner.md contains ">50 lines" threshold
# -----------------------------------------------------------------------------
test_scanner_50_lines() {
    local test_name="Scanner retains '>50 lines' threshold"
    if grep -q ">50 lines" "$SCANNER_FILE" 2>/dev/null; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "'>50 lines' threshold missing"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: phase5-code-smells.md contains ">300 lines" threshold
# -----------------------------------------------------------------------------
test_phase5_300_lines() {
    local test_name="phase5-code-smells.md retains '>300 lines' threshold"
    if grep -q ">300 lines" "$PHASE5_FILE" 2>/dev/null; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "'>300 lines' threshold missing"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: phase5-code-smells.md contains ">50 lines" threshold
# -----------------------------------------------------------------------------
test_phase5_50_lines() {
    local test_name="phase5-code-smells.md retains '>50 lines' threshold"
    if grep -q ">50 lines" "$PHASE5_FILE" 2>/dev/null; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "'>50 lines' threshold missing"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: phase5-code-smells.md retains "line_count > 300"
# -----------------------------------------------------------------------------
test_phase5_detection_300() {
    local test_name="phase5-code-smells.md retains 'line_count > 300' in detection"
    if grep -q "line_count > 300" "$PHASE5_FILE" 2>/dev/null; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "'line_count > 300' not found in detection logic"
    fi
}

# -----------------------------------------------------------------------------
# Test 6: phase5-code-smells.md retains "line_count > 50"
# -----------------------------------------------------------------------------
test_phase5_detection_50() {
    local test_name="phase5-code-smells.md retains 'line_count > 50' in detection"
    if grep -q "line_count > 50" "$PHASE5_FILE" 2>/dev/null; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "'line_count > 50' not found in detection logic"
    fi
}

# -----------------------------------------------------------------------------
# Test 7: Scanner still detects magic numbers
# -----------------------------------------------------------------------------
test_scanner_magic_numbers() {
    local test_name="Scanner retains magic number detection"
    if grep -qi "magic number" "$SCANNER_FILE" 2>/dev/null; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Magic number detection missing"
    fi
}

echo "=============================================="
echo "STORY-405 AC#5: Other Thresholds Unchanged"
echo "=============================================="
echo ""

run_test "1" test_scanner_300_lines
run_test "2" test_scanner_50_lines
run_test "3" test_phase5_300_lines
run_test "4" test_phase5_50_lines
run_test "5" test_phase5_detection_300
run_test "6" test_phase5_detection_50
run_test "7" test_scanner_magic_numbers

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
