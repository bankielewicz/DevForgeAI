#!/bin/bash

# Test: AC#2 - Exception Criteria Defined
# Story: STORY-482
# Generated: 2026-02-23
#
# This test verifies that clear criteria define when the exception applies:
# - no external dependencies
# - no I/O operations
# - no database access
# - no network calls
# - pure function transforms only

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

echo "Testing AC#2: Exception Criteria Defined"
echo "========================================="

# === Arrange ===
if [ ! -f "$TARGET_FILE" ]; then
    echo "ERROR: Target file not found: $TARGET_FILE"
    exit 1
fi

# === Act & Assert ===

# Test 1: Criteria section exists (after exception header)
grep -A 20 "^## Test Pyramid Exceptions" "$TARGET_FILE" | grep -q -i "criteria"
run_test "Criteria section mentioned in exception documentation" $?

# Test 2: Document mentions "no external dependencies"
grep -A 50 "^## Test Pyramid Exceptions" "$TARGET_FILE" | grep -q "external.*dependenc"
run_test "Documentation mentions 'no external dependencies'" $?

# Test 3: Document mentions "no I/O operations"
grep -A 50 "^## Test Pyramid Exceptions" "$TARGET_FILE" | grep -q -i "i/o\|input.*output"
run_test "Documentation mentions 'no I/O operations'" $?

# Test 4: Document mentions "no database access"
grep -A 50 "^## Test Pyramid Exceptions" "$TARGET_FILE" | grep -q -i "database\|db"
run_test "Documentation mentions 'no database access'" $?

# Test 5: Document mentions "no network calls"
grep -A 50 "^## Test Pyramid Exceptions" "$TARGET_FILE" | grep -q -i "network\|http\|api"
run_test "Documentation mentions 'no network calls'" $?

# Test 6: Document mentions "pure function" or similar concept
grep -A 50 "^## Test Pyramid Exceptions" "$TARGET_FILE" | grep -q -i "pure.*function\|pure.*logic\|transform"
run_test "Documentation mentions 'pure function transforms'" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
