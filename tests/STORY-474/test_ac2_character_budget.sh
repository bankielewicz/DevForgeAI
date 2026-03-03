#!/bin/bash
# Test: AC#2 - Character Budget Constraint
# Story: STORY-474
# Generated: 2026-02-23

PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/commands/audit-alignment.md"

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

echo "=== AC#2: Character Budget (10,000 max) ==="

# Test 1: Target file exists
test -f "$TARGET_FILE"
run_test "audit-alignment.md file exists" $?

# Test 2: File is at most 10,000 characters
CHAR_COUNT=$(wc -c < "$TARGET_FILE" 2>/dev/null || echo "99999")
[ "$CHAR_COUNT" -le 10000 ]
run_test "File within 10,000 character budget (actual: $CHAR_COUNT)" $?

# Test 3: File is non-empty
[ "$CHAR_COUNT" -gt 0 ] 2>/dev/null
run_test "File is non-empty" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
