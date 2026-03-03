#!/bin/bash
# Test: AC#2 - Full Regression Test Suite Passes
# Story: STORY-398
# Generated: 2026-02-13

set -euo pipefail

# === Test Configuration ===
PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET_FILE="${PROJECT_ROOT}/tests/results/STORY-398/regression-summary.txt"

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        PASSED=$((PASSED + 1))
    else
        echo "  FAIL: $name"
        FAILED=$((FAILED + 1))
    fi
}

echo "=== AC#2: Full Regression Test Suite Passes ==="
echo ""

# --- Arrange ---
# Target: regression-summary.txt at documented path

# --- Act & Assert ---

# Test 1: regression-summary.txt file exists
test -f "$TARGET_FILE"
run_test "regression-summary.txt exists" $?

# Test 2: Shows 100% pass rate
grep -qi "100%" "$TARGET_FILE"
run_test "Shows 100% pass rate" $?

# Test 3: All 39 agents validated
grep -q "39 agents" "$TARGET_FILE"
run_test "All 39 agents validated" $?

# Test 4: All 17 skills validated
grep -q "17 skills" "$TARGET_FILE"
run_test "All 17 skills validated" $?

# Test 5: All 39 commands validated
grep -q "39 commands" "$TARGET_FILE"
run_test "All 39 commands validated" $?

# Test 6: Zero failures reported
grep -qiE "(0 failures|0 failed)" "$TARGET_FILE"
run_test "Zero failures reported" $?

# Test 7: Agent validation section present
grep -qi "agent validation" "$TARGET_FILE"
run_test "Agent validation section present" $?

# Test 8: Skill workflow section present
grep -qi "skill.*workflow\|skill.*test" "$TARGET_FILE"
run_test "Skill workflow section present" $?

# Test 9: Command integration section present
grep -qi "command.*integration\|command.*test" "$TARGET_FILE"
run_test "Command integration section present" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
