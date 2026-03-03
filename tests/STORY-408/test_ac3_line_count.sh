#!/bin/bash
# Test: AC#3 - Command file reduced to 150 lines or fewer
# Story: STORY-408
# Generated: 2026-02-16

PASSED=0
FAILED=0
TARGET_FILE="src/claude/commands/create-story.md"

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

echo "=== AC#3: Command file reduced to 150 lines or fewer ==="

# Test 1: File exists
[ -f "$TARGET_FILE" ]
run_test "Target file exists" $?

# Test 2: Line count <= 150
LINE_COUNT=$(wc -l < "$TARGET_FILE")
echo "    INFO: Current line count: $LINE_COUNT"
[ "$LINE_COUNT" -le 150 ]
run_test "Line count <= 150 (actual: $LINE_COUNT)" $?

# Test 3: Character count < 8000 (NFR-002)
CHAR_COUNT=$(wc -c < "$TARGET_FILE")
echo "    INFO: Current character count: $CHAR_COUNT"
[ "$CHAR_COUNT" -lt 8000 ]
run_test "Character count < 8,000 (actual: $CHAR_COUNT)" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
