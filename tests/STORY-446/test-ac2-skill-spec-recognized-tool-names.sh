#!/bin/bash
# Test: AC#2 - SKILL.md Uses Spec-Recognized Tool Names
# Story: STORY-446
# Generated: 2026-02-18
# Expected: FAIL (TDD Red) - current file has Bash(git:*), Skill, TodoWrite

PASSED=0
FAILED=0
TARGET="/mnt/c/Projects/DevForgeAI2/src/claude/skills/discovering-requirements/SKILL.md"

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

echo "=== AC#2: SKILL.md Uses Spec-Recognized Tool Names ==="

FRONTMATTER=$(awk '/^---$/{n++; if(n==2) exit} n==1{print}' "$TARGET")

# Test 1: No "Bash(git:*)" pattern in frontmatter
echo "$FRONTMATTER" | grep -q 'Bash(git:\*)'
[ $? -ne 0 ]
run_test "No Bash(git:*) in allowed-tools" $?

# Test 2: No "Skill" tool name (should be "Task")
echo "$FRONTMATTER" | grep -qw 'Skill'
[ $? -ne 0 ]
run_test "No 'Skill' tool name (should be Task)" $?

# Test 3: No "TodoWrite" tool name (not spec-recognized)
echo "$FRONTMATTER" | grep -qw 'TodoWrite'
[ $? -ne 0 ]
run_test "No 'TodoWrite' tool name" $?

# Test 4: Contains "Task" as replacement for Skill
echo "$FRONTMATTER" | grep -qw 'Task'
run_test "Contains 'Task' tool name" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
