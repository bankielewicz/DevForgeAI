#!/bin/bash
# Test: AC#2 - Description and Core Philosophy Naming Corrections
# Story: STORY-451
# Generated: 2026-02-19
# TDD Phase: RED (tests must FAIL against current state)

PASSED=0
FAILED=0

SKILL_MD="/mnt/c/Projects/DevForgeAI2/src/claude/skills/discovering-requirements/SKILL.md"
IDEATE_MD="/mnt/c/Projects/DevForgeAI2/src/claude/commands/ideate.md"

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

echo "=== AC#2: Description and Core Philosophy Naming Corrections ==="
echo ""

# === Arrange ===
# SKILL.md line 3 description must NOT contain "Triggers on keywords like"
# SKILL.md description must contain "Use when users say"
# SKILL.md Core Philosophy must NOT have "Start with Why, Then What, Then How" as standalone heading
# SKILL.md Core Philosophy must NOT have "Ask, Don't Assume" as standalone heading
# ideate.md description must contain "Use when"

# === Act & Assert ===

# Test 1: SKILL.md description must NOT contain meta-trigger instruction text
# Current state: line 3 contains "Triggers on keywords like" (FAIL expected)
# Use ! grep -q so the test FAILS when the pattern IS found
! grep -q 'Triggers on keywords like' "$SKILL_MD"
run_test "SKILL.md description does not contain 'Triggers on keywords like'" $?

# Test 2: SKILL.md description must contain natural user-intent phrase
# Current state: does NOT contain "Use when users say" (FAIL expected)
grep -q 'Use when users say' "$SKILL_MD"
run_test "SKILL.md description contains 'Use when users say'" $?

# Test 3: SKILL.md Core Philosophy must NOT have "Start with Why" as standalone heading
# Current state: line 57 contains **"Start with Why, Then What, Then How"** heading (FAIL expected)
! grep -q '"Start with Why, Then What, Then How"' "$SKILL_MD"
run_test "SKILL.md Core Philosophy does not contain 'Start with Why' standalone heading" $?

# Test 4: SKILL.md Core Philosophy must NOT have "Ask, Don't Assume" as standalone heading
# Current state: line 62 contains **"Ask, Don't Assume"** heading (FAIL expected)
! grep -q '"Ask, Don'"'"'t Assume"' "$SKILL_MD"
run_test "SKILL.md Core Philosophy does not contain 'Ask, Don't Assume' standalone heading" $?

# Test 5: ideate.md description must contain "Use when" trigger context
# Current state: ideate.md description does NOT contain "Use when" (FAIL expected)
grep -q 'Use when' "$IDEATE_MD"
run_test "ideate.md description contains 'Use when' trigger context" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
