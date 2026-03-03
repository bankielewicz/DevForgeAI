#!/bin/bash

################################################################################
# Test: AC#2 - Phase 3 (Complexity Assessment) includes TodoWrite at start
#
# Validates: TodoWrite is invoked at Phase 3 start with:
# - content: "Phase 3: Complexity Assessment"
# - status: "in_progress"
# - activeForm: "Calculating complexity score"
#
# Test Approach: Search for TodoWrite within first 50 lines of complexity file
# Expected: FAIL initially (no implementation yet)
################################################################################

COMPLEXITY_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-ideation/references/complexity-assessment-workflow.md"
TEST_NAME="AC#2 - Phase 3 Start TodoWrite"

# Arrange: File paths
if [ ! -f "$COMPLEXITY_FILE" ]; then
    echo "FAIL: [$TEST_NAME] File not found: $COMPLEXITY_FILE"
    exit 1
fi

# Act: Search for TodoWrite at phase start (within first 50 lines)
START_TODOWRITE=$(head -50 "$COMPLEXITY_FILE" | grep -n "TodoWrite" | head -1)

# Assert: TodoWrite found at start
if [ -z "$START_TODOWRITE" ]; then
    echo "FAIL: [$TEST_NAME] TodoWrite not found at Phase 3 start"
    echo "  Expected: TodoWrite(status=\"in_progress\") within first 50 lines"
    echo "  File: $COMPLEXITY_FILE"
    exit 1
fi

# Act: Check for specific content format "Phase 3: Complexity Assessment"
PHASE3_CONTENT=$(head -50 "$COMPLEXITY_FILE" | grep -i "Phase 3.*Complexity.*Assessment")

if [ -z "$PHASE3_CONTENT" ]; then
    echo "FAIL: [$TEST_NAME] TodoWrite content mismatch"
    echo "  Expected: 'Phase 3: Complexity Assessment'"
    echo "  File: $COMPLEXITY_FILE"
    exit 1
fi

# Act: Check for activeForm with present continuous (-ing) tense
ACTIVEFORM_CALCULATING=$(head -50 "$COMPLEXITY_FILE" | grep -i "Calculating complexity score")

if [ -z "$ACTIVEFORM_CALCULATING" ]; then
    echo "FAIL: [$TEST_NAME] activeForm mismatch"
    echo "  Expected: 'Calculating complexity score' (present continuous)"
    echo "  File: $COMPLEXITY_FILE"
    exit 1
fi

# All assertions passed
echo "PASS: [$TEST_NAME] TodoWrite found at Phase 3 start"
echo "  Location: Line $(echo $START_TODOWRITE | cut -d: -f1)"
echo "  Content: Phase 3: Complexity Assessment"
echo "  ActiveForm: Calculating complexity score"
exit 0
