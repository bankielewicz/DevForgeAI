#!/bin/bash
# Test: AC#7 - Lean Orchestration Pattern Compliance
# Story: STORY-479
# Generated: 2026-02-23

PASSED=0
FAILED=0
TARGET_FILE="src/claude/commands/audit-alignment.md"

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

echo "=== AC#7: Lean Orchestration Pattern Compliance ==="

# Test 1: Task() delegation exists in --generate-refs section
grep -A 40 '\-\-generate-refs' "$TARGET_FILE" | grep -q 'Task('
run_test "test_should_delegate_via_task_when_generate_refs_handled" $?

# Test 2: No inline heuristic evaluation logic in command (lean pattern)
# Command should NOT contain inline DH evaluation logic - only delegation
INLINE_LOGIC=$(grep -A 40 '\-\-generate-refs' "$TARGET_FILE" | grep -c 'Read(.*context\|Grep(.*heuristic\|detection.*logic')
[ "$INLINE_LOGIC" -eq 0 ]
run_test "test_should_not_contain_inline_business_logic_when_inspected" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
