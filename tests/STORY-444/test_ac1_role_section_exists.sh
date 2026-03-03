#!/bin/bash
# Test: AC#1 - SKILL.md must contain "## Your Role" section
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

echo "=== AC#1: Role Section Exists in SKILL.md ==="

# Test 1: "## Your Role" heading exists
grep -q "^## Your Role" "$TARGET_FILE"
run_test "SKILL.md contains '## Your Role' heading" $?

# Test 2: Role section appears after execution model section
EXEC_LINE=$(grep -ni "## .*EXECUTION MODEL\|## .*Execution Model" "$TARGET_FILE" | head -1 | cut -d: -f1)
ROLE_LINE=$(grep -n "## Your Role" "$TARGET_FILE" | head -1 | cut -d: -f1)
if [ -n "$EXEC_LINE" ] && [ -n "$ROLE_LINE" ] && [ "$ROLE_LINE" -gt "$EXEC_LINE" ]; then
    run_test "Role section appears after Execution Model section" 0
else
    run_test "Role section appears after Execution Model section" 1
fi

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
