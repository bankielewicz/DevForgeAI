#!/bin/bash
# Test: AC#6 - Subagent Invocation
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

echo "=== AC#6: Subagent Invocation ==="

# Test 1: Target file exists
test -f "$TARGET_FILE"
run_test "audit-alignment.md file exists" $?

# Test 2: Task() call present
grep -q "Task(" "$TARGET_FILE"
run_test "Task() invocation present" $?

# Test 3: Uses alignment-auditor subagent
grep -qE 'subagent_type\s*=\s*"alignment-auditor"' "$TARGET_FILE"
run_test "Task uses subagent_type=\"alignment-auditor\"" $?

# Test 4: Task has description parameter
grep -qE 'description\s*=' "$TARGET_FILE"
run_test "Task has description parameter" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
