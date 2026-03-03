#!/bin/bash
# AC#3 Verification Script - STORY-454
# Downstream consumption verification documented
# Run from project root: bash src/tests/results/STORY-454/test-ac3-downstream-verification.sh

SKILL_FILE="src/claude/skills/discovering-requirements/SKILL.md"
STORY_FILE="devforgeai/specs/Stories/STORY-454-structured-phase-output-tags-command-consolidation.story.md"
PASSED=0
FAILED=0

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        PASSED=$((PASSED + 1))
    else
        echo "  FAIL: $name"
        FAILED=$((FAILED + 1))
    fi
}

echo "=== AC#3: Downstream Consumption Verification Documented ==="
echo ""

# Test 1: Story Notes contains "Downstream Consumption Verification" with findings
grep -q 'Downstream Consumption Verification' "$STORY_FILE"
t1=$?
# Must have more than just the placeholder "(To be completed during implementation"
! grep -q 'To be completed during implementation' "$STORY_FILE"
t2=$?
[ "$t1" -eq 0 ] && [ "$t2" -eq 0 ]
run_test "Downstream Consumption Verification section populated (not placeholder)" $?

# Test 2: Documentation states whether tags are consumed or documentation-only
grep -q 'documentation-only\|consumed programmatically\|consumed by' "$STORY_FILE"
run_test "Story documents whether tags are consumed or documentation-only" $?

# Test 3: Tags labeled in SKILL.md (either with XML comment or upgraded)
labeled_count=$(grep -c 'documentation-only\|produce your output' "$SKILL_FILE")
[ "$labeled_count" -ge 1 ]
run_test "Phase output tags labeled (documentation-only comment or production instruction) in SKILL.md (found: $labeled_count)" $?

echo ""
echo "=== Results: $PASSED passed, $FAILED failed ==="

if [ "$FAILED" -gt 0 ]; then
    exit 1
else
    exit 0
fi
