#!/bin/bash

################################################################################
# Test: AC#1 - Phase 1 (Discovery) includes TodoWrite at start
#
# Validates: TodoWrite is invoked at Phase 1 start with:
# - content: "Phase 1: Discovery & Problem Understanding"
# - status: "in_progress"
# - activeForm: "Discovering problem space"
#
# Test Approach: Search for TodoWrite instruction at start of discovery-workflow.md
# Expected: FAIL initially (no implementation yet)
################################################################################

DISCOVERY_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-ideation/references/discovery-workflow.md"
TEST_NAME="AC#1 - Phase 1 Start TodoWrite"

# Arrange: File paths
if [ ! -f "$DISCOVERY_FILE" ]; then
    echo "FAIL: [$TEST_NAME] File not found: $DISCOVERY_FILE"
    exit 1
fi

# Act: Search for TodoWrite at phase start
# Look for TodoWrite within first 50 lines with Phase 1 reference and in_progress status
START_TODOWRITE=$(head -50 "$DISCOVERY_FILE" | grep -n "TodoWrite" | head -1)

# Assert: TodoWrite found at start
if [ -z "$START_TODOWRITE" ]; then
    echo "FAIL: [$TEST_NAME] TodoWrite not found at Phase 1 start"
    echo "  Expected: TodoWrite(status=\"in_progress\") within first 50 lines"
    echo "  File: $DISCOVERY_FILE"
    exit 1
fi

# Act: Check for specific content format "Phase 1: Discovery & Problem Understanding"
PHASE1_CONTENT=$(head -50 "$DISCOVERY_FILE" | grep -i "Phase 1.*Discovery.*Problem")

if [ -z "$PHASE1_CONTENT" ]; then
    echo "FAIL: [$TEST_NAME] TodoWrite content mismatch"
    echo "  Expected: 'Phase 1: Discovery & Problem Understanding'"
    echo "  File: $DISCOVERY_FILE"
    exit 1
fi

# Act: Check for activeForm with present continuous (-ing) tense
ACTIVEFORM_DISCOVERING=$(head -50 "$DISCOVERY_FILE" | grep -i "Discovering problem space")

if [ -z "$ACTIVEFORM_DISCOVERING" ]; then
    echo "FAIL: [$TEST_NAME] activeForm mismatch"
    echo "  Expected: 'Discovering problem space' (present continuous)"
    echo "  File: $DISCOVERY_FILE"
    exit 1
fi

# All assertions passed
echo "PASS: [$TEST_NAME] TodoWrite found at Phase 1 start"
echo "  Location: Line $(echo $START_TODOWRITE | cut -d: -f1)"
echo "  Content: Phase 1: Discovery & Problem Understanding"
echo "  ActiveForm: Discovering problem space"
exit 0
