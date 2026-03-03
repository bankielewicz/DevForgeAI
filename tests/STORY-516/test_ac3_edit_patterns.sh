#!/bin/bash
# Test: AC#3 - Step 4.5 Edit patterns match exact empty table format with skip guard
# Story: STORY-516
# Generated: 2026-02-28

PASSED=0
FAILED=0

TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/skills/implementing-stories/phases/phase-07-dod-update.md"

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        PASSED=$((PASSED + 1))
    else
        echo "  FAIL: $name"
        FAILED=$((FAILED + 1))
    fi
}

echo "=== AC#3: Edit patterns and skip guard ==="

# Test 7: Exact table header for TDD phases table
grep -q '| Phase | Status | Details |' "$TARGET_FILE"
run_test "Contains Phase/Status/Details table header" $?

# Test 8: References phase-state.json
grep -A 50 '4\.5\..*Populate.*TDD' "$TARGET_FILE" | grep -q 'phase-state\.json'
run_test "Step 4.5 references phase-state.json" $?

# Test 9: Skip guard for already-populated tables
grep -A 50 '4\.5\..*Populate.*TDD' "$TARGET_FILE" | grep -qi 'skip\|already.populated\|guard'
run_test "Step 4.5 contains skip/guard logic" $?

# Test 7b: Exact table header for files table
grep -q '| File | Action | Lines |' "$TARGET_FILE"
run_test "Contains File/Action/Lines table header" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
