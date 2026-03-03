#!/bin/bash
# Test: AC#2 - ideate.md must contain orchestrator role context
# Story: STORY-444
# Generated: 2026-02-18

PASSED=0
FAILED=0
TARGET_FILE="src/claude/commands/ideate.md"

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

echo "=== AC#2: Orchestrator Role Context in ideate.md ==="

# Test 1: Dedicated role section or role prompt exists in header area
grep -q "^## .*[Rr]ole\|^\*\*Your Role:\*\*\|^You are.*requirements.*specialist\|^You are.*discovery.*expert" "$TARGET_FILE"
run_test "ideate.md contains dedicated role prompt or role section" $?

# Test 2: Role context references orchestrator responsibility
grep -q "orchestrat.*requirements\|orchestrat.*discovery\|you.*orchestrat" "$TARGET_FILE"
run_test "ideate.md contains orchestrator role context" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
