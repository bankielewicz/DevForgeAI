#!/bin/bash
# Test: AC#5 - Skipped Phases Write Markers per STORY-497 Protocol
# Story: STORY-498
# Generated: 2026-02-24

PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-release/SKILL.md"

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

echo "=== AC#5: Skipped Phases Write Markers per STORY-497 Protocol ==="

# Test 1: Exact skip marker reason text exists
grep -q "Library project: no deployment target" "$TARGET_FILE"
run_test "Skip marker reason text 'Library project: no deployment target' present" $?

# Test 2: Skip marker reason text appears in context of library/skipped phases
grep -B5 -A5 "Library project: no deployment target" "$TARGET_FILE" | grep -qi "skip\|marker\|phase"
run_test "Skip marker reason associated with phase skipping context" $?

# Test 3: Library adaptive path references STORY-497 marker protocol explicitly
grep -A80 "Project Type Classification" "$TARGET_FILE" | grep -q "STORY-497"
run_test "Library path references STORY-497 marker protocol" $?

# Test 4: Skipped phases load references before writing marker
grep -A80 "Project Type Classification" "$TARGET_FILE" | grep -qi "load.*reference\|reference.*file"
run_test "Skipped phases load references before writing marker" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
