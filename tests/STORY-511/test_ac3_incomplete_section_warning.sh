#!/bin/bash
# Test: AC#3 - Incomplete Section Produces Warning
# Story: STORY-511
# Generated: 2026-02-28

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE=".claude/agents/context-preservation-validator.md"

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

echo "=== AC#3: Incomplete Section Produces Warning ==="
echo "Target: $TARGET_FILE"
echo ""

# === Arrange ===
if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file does not exist: $TARGET_FILE"
    exit 1
fi

# === Act & Assert ===

# Test 1: WARN-level finding defined for incomplete Decision Context
grep -q "WARN" "$TARGET_FILE" && grep -q "Decision Context section incomplete" "$TARGET_FILE"
run_test "WARN-level finding for Decision Context section incomplete defined" $?

# Test 2: The warning is associated with WARN severity
grep -B 5 "Decision Context section incomplete" "$TARGET_FILE" | grep -qi "WARN\|warning"
run_test "Incomplete section finding has WARN severity" $?

# Test 3: The warning references placeholder text detection
grep -B 10 -A 10 "Decision Context section incomplete" "$TARGET_FILE" | grep -qi "placeholder\|TBD\|TODO\|template"
run_test "Warning references placeholder text detection" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
