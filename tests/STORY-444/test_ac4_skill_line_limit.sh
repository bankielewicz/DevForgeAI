#!/bin/bash
# Test: AC#4 - SKILL.md must remain under 500 lines
# Story: STORY-444
# Generated: 2026-02-18

PASSED=0
FAILED=0
TARGET_FILE="src/claude/skills/discovering-requirements/SKILL.md"

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

echo "=== AC#4: SKILL.md Line Count Under 500 ==="

LINE_COUNT=$(wc -l < "$TARGET_FILE")
echo "  Current line count: $LINE_COUNT"

# Test 1: File is under 500 lines
if [ "$LINE_COUNT" -lt 500 ]; then
    run_test "SKILL.md is under 500 lines ($LINE_COUNT lines)" 0
else
    run_test "SKILL.md is under 500 lines ($LINE_COUNT lines)" 1
fi

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
