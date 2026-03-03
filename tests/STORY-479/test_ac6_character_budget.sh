#!/bin/bash
# Test: AC#6 - Character Budget Compliance
# Story: STORY-479
# Generated: 2026-02-23

PASSED=0
FAILED=0
TARGET_FILE="src/claude/commands/audit-alignment.md"

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

echo "=== AC#6: Character Budget Compliance ==="

# Test 1: File exists
[ -f "$TARGET_FILE" ]
run_test "test_should_exist_when_file_checked" $?

# Test 2: File is within 10,000 character budget
CHAR_COUNT=$(wc -c < "$TARGET_FILE")
[ "$CHAR_COUNT" -le 10000 ]
run_test "test_should_be_within_10000_chars_when_measured (actual: ${CHAR_COUNT})" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
