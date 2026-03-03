#!/bin/bash
# Test: AC#6 - Single story mode invokes skill immediately after description validation
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

echo "=== AC#6: Single story mode immediate invocation ==="

# Find Skill() call line
SKILL_LINE=$(grep -n 'Skill(command="devforgeai-story-creation")' "$TARGET_FILE" | head -1 | cut -d: -f1)
if [ -z "$SKILL_LINE" ]; then
    echo "  FAIL: Cannot find Skill() call"
    exit 1
fi

BEFORE_SKILL=$(head -n "$((SKILL_LINE - 1))" "$TARGET_FILE")

# Test 1: SINGLE_STORY mode marker exists in file
grep -q 'SINGLE_STORY' "$TARGET_FILE"
run_test "SINGLE_STORY mode marker exists in command file" $?

# Test 2: Mode marker set before Skill() call
echo "$BEFORE_SKILL" | grep -q 'SINGLE_STORY'
run_test "SINGLE_STORY marker set before Skill() invocation" $?

# Test 3: Feature Description marker exists before Skill()
echo "$BEFORE_SKILL" | grep -qE '\*\*Feature Description:\*\*|\*\*Feature.Description\*\*|feature.description'
run_test "Feature Description context marker set before Skill() invocation" $?

# Test 4: Description validation (10+ words) documented before Skill()
echo "$BEFORE_SKILL" | grep -qE '10.*word|word.*10|minimum.*word'
run_test "Description word count validation (10+ words) documented before Skill()" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
