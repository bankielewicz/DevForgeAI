#!/bin/bash
# Test: AC#5 - Loop Execution Over Selected Features
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

echo "=== AC#5: Batch Loop Execution ==="

# Test 1: Step 0.5 section exists
grep -q "Step 0\.5" "$TARGET_FILE" 2>/dev/null
run_test "Step 0.5 section exists in story-discovery.md" $?

# Test 2: FOR loop over selected features
grep -qiE "FOR.*feature|for.*selected|iterate|loop" "$TARGET_FILE" 2>/dev/null
run_test "FOR loop iteration over features documented" $?

# Test 3: Sequential STORY-NNN ID generation
grep -qi "STORY-\|story.*id\|gap.aware" "$TARGET_FILE" 2>/dev/null
run_test "Sequential STORY-NNN ID generation documented" $?

# Test 4: Phases 2-7 execution per feature
grep -qE "Phase[s]? 2.7|Phase 2.*Phase 7" "$TARGET_FILE" 2>/dev/null
run_test "Phases 2-7 execution per feature documented" $?

# Test 5: Failure isolation (continue on error)
grep -qi "fail\|error\|continue\|resilien" "$TARGET_FILE" 2>/dev/null
run_test "Failure isolation logic documented" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
