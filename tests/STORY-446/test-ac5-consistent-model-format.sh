#!/bin/bash
# Test: AC#5 - Consistent Model Field Format
# Story: STORY-446
# Generated: 2026-02-18
# Expected: FAIL (TDD Red) - SKILL.md has "claude-opus-4-6", ideate.md has "opus"

PASSED=0
FAILED=0
SKILL="/mnt/c/Projects/DevForgeAI2/src/claude/skills/discovering-requirements/SKILL.md"
IDEATE="/mnt/c/Projects/DevForgeAI2/src/claude/commands/ideate.md"

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

echo "=== AC#5: Consistent Model Field Format ==="

SKILL_FM=$(awk '/^---$/{n++; if(n==2) exit} n==1{print}' "$SKILL")
IDEATE_FM=$(awk '/^---$/{n++; if(n==2) exit} n==1{print}' "$IDEATE")

SKILL_MODEL=$(echo "$SKILL_FM" | grep '^model:' | sed 's/^model:\s*//' | tr -d '[:space:]')
IDEATE_MODEL=$(echo "$IDEATE_FM" | grep '^model:' | sed 's/^model:\s*//' | tr -d '[:space:]')

# Test 1: Both model fields have the same value
[ "$SKILL_MODEL" = "$IDEATE_MODEL" ]
run_test "Model field matches between SKILL.md ($SKILL_MODEL) and ideate.md ($IDEATE_MODEL)" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
