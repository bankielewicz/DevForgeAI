#!/bin/bash
# Test: AC#5 - Missing Context Graceful Degradation
# Story: STORY-534
# Generated: 2026-03-04
#
# Verifies the command handles missing context files gracefully:
# - Logs warnings for missing individual files
# - Proceeds with whatever context files are available
# - Does not fail/halt when some files are missing

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="src/claude/commands/business-plan.md"

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

echo "=== AC#5: Missing Context Graceful Degradation ==="
echo ""

# === Arrange ===
if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file does not exist: $TARGET_FILE"
    echo ""
    echo "Results: 0 passed, 1 failed (file missing - expected in RED phase)"
    exit 1
fi

# === Act & Assert ===

# Test 1: Command logs warnings for missing files
grep -qiE "warn|warning|log.*missing|missing.*file" "$TARGET_FILE"
run_test "Logs warnings for missing files" $?

# Test 2: Command proceeds with available context files
grep -qiE "proceed|continue|available.*context|partial.*context" "$TARGET_FILE"
run_test "Proceeds with available context files" $?

# Test 3: Command does not halt on missing individual files
grep -qiE "graceful|degrad|not.*halt|not.*fail|skip.*missing" "$TARGET_FILE"
run_test "Graceful degradation - does not halt" $?

# Test 4: Command checks each context file individually
grep -qiE "IF.*exist|check.*file|file.*exist|each.*context" "$TARGET_FILE"
run_test "Checks each context file individually" $?

# Test 5: Command provides fallback behavior for missing data
grep -qiE "fallback|default|without.*context|missing.*proceed" "$TARGET_FILE"
run_test "Provides fallback for missing context data" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
