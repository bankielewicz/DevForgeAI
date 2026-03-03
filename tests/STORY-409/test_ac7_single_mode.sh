#!/bin/bash
# Test: AC#7 - Single Story Mode Unchanged
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

echo "=== AC#7: Single Story Mode Unchanged ==="

# Test 1: Steps 1.1-1.6 still exist (not removed)
grep -q "Step 1\.1\|Step 1\.2\|Step 1\.3" "$TARGET_FILE" 2>/dev/null
run_test "Steps 1.x still exist in story-discovery.md" $?

# Test 2: Conditional branching between batch and single mode
grep -qiE "IF.*batch_mode|IF.*EPIC_BATCH|single.*mode|batch.*mode.*false" "$TARGET_FILE" 2>/dev/null
run_test "Conditional branching between batch and single mode" $?

# Test 3: Steps 0.x bypass documented for single mode
grep -qi "bypass\|skip.*batch\|proceed.*Step 1\|ELSE.*Step 1" "$TARGET_FILE" 2>/dev/null
run_test "Batch steps bypass documented for single mode" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
