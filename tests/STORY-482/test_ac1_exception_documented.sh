#!/bin/bash

# Test: AC#1 - Test Pyramid Exception Documented
# Story: STORY-482
# Generated: 2026-02-23
#
# This test verifies that a "Test Pyramid Exceptions" section
# exists in .claude/agents/test-automator.md documenting that
# pure-logic detector modules are exempt from 70/20/10 ratio.

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE=".claude/agents/test-automator.md"

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

echo "Testing AC#1: Test Pyramid Exception Documented"
echo "=================================================="

# === Arrange ===
# Verify target file exists
if [ ! -f "$TARGET_FILE" ]; then
    echo "ERROR: Target file not found: $TARGET_FILE"
    exit 1
fi

# === Act & Assert ===

# Test 1: Section header exists
grep -q "^## Test Pyramid Exceptions" "$TARGET_FILE"
run_test "Section header 'Test Pyramid Exceptions' exists" $?

# Test 2: Exception description mentions pure-logic modules
grep -q "pure-logic.*exempt" "$TARGET_FILE"
run_test "Documentation mentions pure-logic modules exempt from ratio" $?

# Test 3: Section header at correct level (##, not ###)
grep "^## Test Pyramid Exceptions" "$TARGET_FILE" > /dev/null
run_test "Section is at correct markdown level (##)" $?

# Test 4: Section appears in subagent documentation area
awk '/^## Test Pyramid Exceptions/{found=1; next} found && /[a-zA-Z]/{print; exit}' "$TARGET_FILE" | grep -q "."
run_test "Section content exists and is not empty" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
