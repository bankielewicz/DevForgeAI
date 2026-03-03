#!/bin/bash
# Test: AC#2 - Reference file Step 5 heading changed to MANDATORY, content preserved
# Story: STORY-516
# Generated: 2026-02-28

PASSED=0
FAILED=0

TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/skills/implementing-stories/references/dod-update-workflow.md"

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

echo "=== AC#2: Reference file MANDATORY heading ==="

# Test 4: Step 5 heading line contains [MANDATORY]
grep -q '## Step 5:.*\[MANDATORY\]' "$TARGET_FILE"
run_test "Step 5 heading contains [MANDATORY]" $?

# Test 5: "Optional but Recommended" does NOT appear on Step 5 heading
! grep -q 'Step 5:.*Optional but Recommended' "$TARGET_FILE"
run_test "Optional but Recommended removed from Step 5 heading" $?

# Test 6: Preserved content still present
grep -q 'Phase 02 (Red)' "$TARGET_FILE"
run_test "Preserved content: Phase 02 (Red)" $?

grep -q 'Phase 03 (Green)' "$TARGET_FILE"
run_test "Preserved content: Phase 03 (Green)" $?

grep -q 'Files Created/Modified' "$TARGET_FILE"
run_test "Preserved content: Files Created/Modified" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
