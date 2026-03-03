#!/bin/bash
# Test: AC#5 - Epic batch mode context markers set correctly before skill invocation
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

echo "=== AC#5: Epic batch mode context markers ==="

# Find Skill() call line
SKILL_LINE=$(grep -n 'Skill(command="devforgeai-story-creation")' "$TARGET_FILE" | head -1 | cut -d: -f1)
if [ -z "$SKILL_LINE" ]; then
    echo "  FAIL: Cannot find Skill() call"
    exit 1
fi

BEFORE_SKILL=$(head -n "$((SKILL_LINE - 1))" "$TARGET_FILE")

# Test 1: EPIC_BATCH mode marker exists in file
grep -q 'EPIC_BATCH' "$TARGET_FILE"
run_test "EPIC_BATCH mode marker exists in command file" $?

# Test 2: Mode marker set before Skill() call
echo "$BEFORE_SKILL" | grep -q 'EPIC_BATCH'
run_test "EPIC_BATCH marker set before Skill() invocation" $?

# Test 3: Epic ID marker pattern exists before Skill()
echo "$BEFORE_SKILL" | grep -qE '\*\*Epic ID:\*\*|\*\*Epic.ID\*\*|epic.id'
run_test "Epic ID context marker set before Skill() invocation" $?

# Test 4: No feature extraction before Skill() in batch mode section
echo "$BEFORE_SKILL" | grep -qi 'extract features'
[ $? -ne 0 ]
run_test "No feature extraction before Skill() in batch mode" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
