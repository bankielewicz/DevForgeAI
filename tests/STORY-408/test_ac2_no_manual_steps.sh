#!/bin/bash
# Test: AC#2 - No manual workflow steps before skill invocation
# Story: STORY-408
# Generated: 2026-02-16

PASSED=0
FAILED=0
TARGET_FILE="src/claude/commands/create-story.md"

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

echo "=== AC#2: No manual workflow steps before skill invocation ==="

# Find the line number of first Skill() call
SKILL_LINE=$(grep -n 'Skill(command="devforgeai-story-creation")' "$TARGET_FILE" | head -1 | cut -d: -f1)
if [ -z "$SKILL_LINE" ]; then
    echo "  FAIL: Cannot find Skill() call - all tests skipped"
    exit 1
fi

# Extract content before Skill() call
BEFORE_SKILL=$(head -n "$((SKILL_LINE - 1))" "$TARGET_FILE")

# Test 1: No Grep( before Skill()
echo "$BEFORE_SKILL" | grep -q 'Grep('
[ $? -ne 0 ]
run_test "No Grep() calls before Skill() invocation" $?

# Test 2: No Read( before Skill()
echo "$BEFORE_SKILL" | grep -q 'Read('
[ $? -ne 0 ]
run_test "No Read() calls before Skill() invocation" $?

# Test 3: No TaskCreate( before Skill()
echo "$BEFORE_SKILL" | grep -q 'TaskCreate('
[ $? -ne 0 ]
run_test "No TaskCreate() calls before Skill() invocation" $?

# Test 4: No AskUserQuestion( before Skill() except for mode clarification
# Count AskUserQuestion occurrences - at most 1 allowed (for ambiguous arg clarification)
ASK_COUNT=$(echo "$BEFORE_SKILL" | grep -c 'AskUserQuestion(')
[ "$ASK_COUNT" -le 1 ]
run_test "At most 1 AskUserQuestion() before Skill() (found $ASK_COUNT)" $?

# Test 5: Glob( is allowed for validation - verify any Glob is for epic file existence only
GLOB_COUNT=$(echo "$BEFORE_SKILL" | grep -c 'Glob(')
[ "$GLOB_COUNT" -le 1 ]
run_test "At most 1 Glob() before Skill() for validation (found $GLOB_COUNT)" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
