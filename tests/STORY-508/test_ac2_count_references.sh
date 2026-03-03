#!/bin/bash
# Test: AC#2 - Count References Updated
# Story: STORY-508
# Generated: 2026-02-28

PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/skills/designing-systems/references/artifact-generation.md"

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

echo "=== AC#2: Count References Updated ==="

# Test 1: No references to "12 constitutional sections" remain
OLD_COUNT=$(grep -c "12 constitutional sections" "$TARGET_FILE")
[ "$OLD_COUNT" -eq 0 ]
run_test "Zero occurrences of '12 constitutional sections' remain" $?

# Test 2: At least one reference to "13 constitutional sections" exists
grep -q "13 constitutional sections" "$TARGET_FILE"
run_test "At least one reference to '13 constitutional sections' exists" $?

# Test 3: "verify all 12 sections" updated to "verify all 13 sections"
OLD_VERIFY=$(grep -c "verify all 12 sections" "$TARGET_FILE")
[ "$OLD_VERIFY" -eq 0 ]
run_test "No references to 'verify all 12 sections' remain" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
