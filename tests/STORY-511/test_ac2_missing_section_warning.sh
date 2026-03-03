#!/bin/bash
# Test: AC#2 - Missing Section Produces Warning
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

echo "=== AC#2: Missing Section Produces Warning ==="
echo "Target: $TARGET_FILE"
echo ""

# === Arrange ===
if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file does not exist: $TARGET_FILE"
    exit 1
fi

# === Act & Assert ===

# Test 1: WARN-level finding defined for missing Decision Context
grep -q "WARN" "$TARGET_FILE" && grep -q "Missing Decision Context section" "$TARGET_FILE"
run_test "WARN-level finding for Missing Decision Context section defined" $?

# Test 2: The warning is associated with WARN severity (not ERROR or INFO)
grep -B 5 "Missing Decision Context section" "$TARGET_FILE" | grep -qi "WARN\|warning"
run_test "Missing section finding has WARN severity" $?

# Test 3: The warning triggers when epic lacks Decision Context section
grep -B 10 -A 10 "Missing Decision Context section" "$TARGET_FILE" | grep -qi "epic\|document"
run_test "Warning references epic documents lacking Decision Context" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
