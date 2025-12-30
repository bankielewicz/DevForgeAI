#!/bin/bash

################################################################################
# Test: AC#1 - Phase 1 (Discovery) includes TodoWrite at end
#
# Validates: TodoWrite completion is invoked at Phase 1 end with:
# - status: "completed"
# - content: "Phase 1: Discovery & Problem Understanding"
#
# Test Approach: Search for TodoWrite with completed status near end of file
# Expected: FAIL initially (no implementation yet)
################################################################################

DISCOVERY_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-ideation/references/discovery-workflow.md"
TEST_NAME="AC#1 - Phase 1 End TodoWrite"

# Arrange: File paths
if [ ! -f "$DISCOVERY_FILE" ]; then
    echo "FAIL: [$TEST_NAME] File not found: $DISCOVERY_FILE"
    exit 1
fi

# Count total lines
TOTAL_LINES=$(wc -l < "$DISCOVERY_FILE")

# Act: Get last 100 lines and search for TodoWrite with completed status
LAST_LINES=$((TOTAL_LINES - 100))
if [ $LAST_LINES -lt 1 ]; then
    LAST_LINES=1
fi

END_TODOWRITE=$(tail -100 "$DISCOVERY_FILE" | grep -n "TodoWrite" | tail -1)

if [ -z "$END_TODOWRITE" ]; then
    echo "FAIL: [$TEST_NAME] TodoWrite completion not found at Phase 1 end"
    echo "  Expected: TodoWrite with status=\"completed\" in last 100 lines"
    echo "  File: $DISCOVERY_FILE"
    exit 1
fi

# Act: Verify it has completed status (check within tail section)
COMPLETED_STATUS=$(tail -100 "$DISCOVERY_FILE" | grep -i "TodoWrite.*completed\|status.*completed")

if [ -z "$COMPLETED_STATUS" ]; then
    echo "FAIL: [$TEST_NAME] TodoWrite completion status not found"
    echo "  Expected: status=\"completed\" for Phase 1 end"
    echo "  File: $DISCOVERY_FILE"
    exit 1
fi

# All assertions passed
echo "PASS: [$TEST_NAME] TodoWrite completion found at Phase 1 end"
echo "  Content: Phase 1: Discovery & Problem Understanding"
echo "  Status: completed"
exit 0
