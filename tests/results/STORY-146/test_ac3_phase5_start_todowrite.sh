#!/bin/bash

################################################################################
# Test: AC#3 - Phase 5 (Feasibility) includes TodoWrite at start
#
# Validates: TodoWrite is invoked at Phase 5 start with:
# - content: "Phase 5: Feasibility & Constraints Analysis"
# - status: "in_progress"
# - activeForm: "Analyzing constraints"
#
# Test Approach: Search for TodoWrite within first 50 lines of feasibility file
# Expected: FAIL initially (no implementation yet)
################################################################################

FEASIBILITY_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-ideation/references/feasibility-analysis-workflow.md"
TEST_NAME="AC#3 - Phase 5 Start TodoWrite"

# Arrange: File paths
if [ ! -f "$FEASIBILITY_FILE" ]; then
    echo "FAIL: [$TEST_NAME] File not found: $FEASIBILITY_FILE"
    exit 1
fi

# Act: Search for TodoWrite at phase start (within first 50 lines)
START_TODOWRITE=$(head -50 "$FEASIBILITY_FILE" | grep -n "TodoWrite" | head -1)

# Assert: TodoWrite found at start
if [ -z "$START_TODOWRITE" ]; then
    echo "FAIL: [$TEST_NAME] TodoWrite not found at Phase 5 start"
    echo "  Expected: TodoWrite(status=\"in_progress\") within first 50 lines"
    echo "  File: $FEASIBILITY_FILE"
    exit 1
fi

# Act: Check for specific content format "Phase 5: Feasibility & Constraints Analysis"
PHASE5_CONTENT=$(head -50 "$FEASIBILITY_FILE" | grep -i "Phase 5.*Feasibility.*Constraints.*Analysis")

if [ -z "$PHASE5_CONTENT" ]; then
    echo "FAIL: [$TEST_NAME] TodoWrite content mismatch"
    echo "  Expected: 'Phase 5: Feasibility & Constraints Analysis'"
    echo "  File: $FEASIBILITY_FILE"
    exit 1
fi

# Act: Check for activeForm with present continuous (-ing) tense
ACTIVEFORM_ANALYZING=$(head -50 "$FEASIBILITY_FILE" | grep -i "Analyzing constraints")

if [ -z "$ACTIVEFORM_ANALYZING" ]; then
    echo "FAIL: [$TEST_NAME] activeForm mismatch"
    echo "  Expected: 'Analyzing constraints' (present continuous)"
    echo "  File: $FEASIBILITY_FILE"
    exit 1
fi

# All assertions passed
echo "PASS: [$TEST_NAME] TodoWrite found at Phase 5 start"
echo "  Location: Line $(echo $START_TODOWRITE | cut -d: -f1)"
echo "  Content: Phase 5: Feasibility & Constraints Analysis"
echo "  ActiveForm: Analyzing constraints"
exit 0
