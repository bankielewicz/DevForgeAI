#!/bin/bash
# Test: AC#1 - Batch Mode Detection in Skill Phase 1
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

echo "=== AC#1: Batch Mode Detection ==="

# Test 1: Step 0.1 section exists
grep -q "Step 0\.1" "$TARGET_FILE" 2>/dev/null
run_test "Step 0.1 section exists in story-discovery.md" $?

# Test 2: EPIC_BATCH marker detection documented
grep -qi "EPIC_BATCH" "$TARGET_FILE" 2>/dev/null
run_test "EPIC_BATCH marker detection documented" $?

# Test 3: epic_id extraction logic present
grep -qi "epic_id" "$TARGET_FILE" 2>/dev/null
run_test "epic_id extraction logic present" $?

# Test 4: batch_mode variable set
grep -qi "batch_mode" "$TARGET_FILE" 2>/dev/null
run_test "batch_mode variable assignment documented" $?

# Test 5: Fallback to interactive mode documented
grep -qi "fallback\|interactive\|single.*mode\|Step 1\." "$TARGET_FILE" 2>/dev/null
run_test "Fallback to interactive mode documented" $?

# Test 6: Epic ID format validation (EPIC-NNN)
grep -qE "EPIC-[0-9]{3}|EPIC-\\\\d" "$TARGET_FILE" 2>/dev/null
run_test "Epic ID format validation pattern present" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
