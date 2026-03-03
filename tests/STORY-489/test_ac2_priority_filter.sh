#!/bin/bash
# Test: AC#2 - Prompts for CRITICAL/HIGH Recommendations Only
# Story: STORY-489
# Generated: 2026-02-23

set -e

PASSED=0
FAILED=0
TARGET_FILE="src/claude/skills/devforgeai-rca/SKILL.md"

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

echo "=== AC#2: Prompts for CRITICAL/HIGH Recommendations Only ==="

# Extract Phase 7.5 section for targeted testing
PHASE75_START=$(grep -n "Phase 7.5" "$TARGET_FILE" | head -1 | cut -d: -f1)

# Test 1: Phase 7.5 mentions AskUserQuestion
sed -n "${PHASE75_START:-1},\$p" "$TARGET_FILE" | grep -q "AskUserQuestion" 2>/dev/null
run_test "Phase 7.5 mentions AskUserQuestion" $?

# Test 2: Phase 7.5 mentions CRITICAL priority filtering
sed -n "${PHASE75_START:-1},\$p" "$TARGET_FILE" | grep -q "CRITICAL" 2>/dev/null
run_test "Phase 7.5 mentions CRITICAL priority" $?

# Test 3: Phase 7.5 mentions HIGH priority filtering
sed -n "${PHASE75_START:-1},\$p" "$TARGET_FILE" | grep -q "HIGH" 2>/dev/null
run_test "Phase 7.5 mentions HIGH priority" $?

# Test 4: Phase 7.5 mentions MEDIUM/LOW skip behavior
sed -n "${PHASE75_START:-1},\$p" "$TARGET_FILE" | grep -q "MEDIUM" 2>/dev/null
run_test "Phase 7.5 mentions MEDIUM skip" $?

# Test 5: Phase 7.5 mentions informational note for skipped recs
sed -n "${PHASE75_START:-1},\$p" "$TARGET_FILE" | grep -qi "skip\|informational" 2>/dev/null
run_test "Phase 7.5 mentions skip with informational note" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
