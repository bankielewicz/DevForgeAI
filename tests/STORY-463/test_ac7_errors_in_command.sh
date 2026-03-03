#!/bin/bash
# Test: AC#7 - feedback-search.md preserves all 4 error blocks in the command file
# Story: STORY-463
# Generated: 2026-02-21
# TDD Phase: RED - these tests MUST FAIL before refactoring

PASSED=0
FAILED=0
TARGET="src/claude/commands/feedback-search.md"

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

echo "=== AC#7: Error Blocks Preserved in Command File ==="
echo "Target: $TARGET"
echo ""

if [ ! -f "$TARGET" ]; then
    echo "  ERROR: Target file not found: $TARGET"
    exit 1
fi

# === Test 1: "Query Too Long" error present ===
grep -q "Query Too Long" "$TARGET"
run_test "feedback-search.md contains 'Query Too Long' error" $?

# === Test 2: "Invalid Limit" error present ===
grep -q "Invalid Limit" "$TARGET"
run_test "feedback-search.md contains 'Invalid Limit' error" $?

# === Test 3: "Invalid Page" error present ===
grep -q "Invalid Page" "$TARGET"
run_test "feedback-search.md contains 'Invalid Page' error" $?

# === Test 4: "Empty Feedback" error present ===
grep -q "Empty Feedback" "$TARGET"
run_test "feedback-search.md contains 'Empty Feedback' error" $?

echo ""
echo "=== Results: $PASSED passed, $FAILED failed ==="
[ $FAILED -eq 0 ] && exit 0 || exit 1
