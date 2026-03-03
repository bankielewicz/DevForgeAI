#!/bin/bash
# Test: AC#9 - Precondition and Postcondition
# Story: STORY-478
# Generated: 2026-02-23
set -uo pipefail

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET="$PROJECT_ROOT/src/claude/skills/designing-systems/SKILL.md"
PASSED=0
FAILED=0

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

echo "=== AC#9: Precondition and Postcondition ==="

# Test 1: Precondition references Phase 5.5 completed
grep -A 30 "Phase 5\.7" "$TARGET" | grep -iq "Phase 5\.5.*completed\|precondition.*5\.5"
run_test "test_should_state_precondition_phase55_completed_when_checked" $?

# Test 2: Postcondition about context-derived content
grep -A 30 "Phase 5\.7" "$TARGET" | grep -iq "postcondition\|context-derived\|context derived"
run_test "test_should_state_postcondition_context_derived_when_checked" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
