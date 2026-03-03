#!/bin/bash
# Test: AC#6 - Batch Summary Return
# Story: STORY-409
# Generated: 2026-02-16

PASSED=0
FAILED=0
TARGET_FILE="src/claude/skills/devforgeai-story-creation/references/story-discovery.md"

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

echo "=== AC#6: Batch Summary Return ==="

# Test 1: Step 0.6 section exists
grep -q "Step 0\.6" "$TARGET_FILE" 2>/dev/null
run_test "Step 0.6 section exists in story-discovery.md" $?

# Test 2: Created stories count
grep -qi "created.*stories\|stories.*created\|created_stories" "$TARGET_FILE" 2>/dev/null
run_test "Created stories count in summary" $?

# Test 3: Failed stories count with reasons
grep -qi "failed.*stories\|stories.*failed\|failed_stories\|failure.*reason" "$TARGET_FILE" 2>/dev/null
run_test "Failed stories with reasons in summary" $?

# Test 4: Suggested next actions
grep -qi "next.*action\|suggested.*action\|next.*step" "$TARGET_FILE" 2>/dev/null
run_test "Suggested next actions in summary" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
