#!/bin/bash
# Test: AC#1 - Lean Orchestration Pattern
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

echo "=== AC#1: Lean Orchestration Pattern ==="

# Test 1: Target file exists
test -f "$TARGET_FILE"
run_test "audit-alignment.md file exists" $?

# Test 2: File contains Task() invocation
grep -q "Task(" "$TARGET_FILE"
run_test "File contains Task() invocation" $?

# Test 3: No business logic before Task() - count code blocks before first Task()
# Lean orchestration = no more than 4 code blocks before Task()
BLOCKS_BEFORE_TASK=$(sed -n '1,/Task(/p' "$TARGET_FILE" 2>/dev/null | grep -c '```')
[ "$BLOCKS_BEFORE_TASK" -le 4 ] 2>/dev/null
run_test "At most 4 code blocks before Task() invocation (found: $BLOCKS_BEFORE_TASK)" $?

# Test 4: No implementation logic (grep, sed, awk) before Task()
LOGIC_BEFORE=$(sed -n '1,/Task(/p' "$TARGET_FILE" 2>/dev/null | grep -cE '^\s*(grep|sed|awk|for |while |if \[)')
[ "$LOGIC_BEFORE" -eq 0 ] 2>/dev/null
run_test "No business logic commands before Task() (found: $LOGIC_BEFORE)" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
