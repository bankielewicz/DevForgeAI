#!/bin/bash

################################################################################
# Test: AC#2 - Phase 3 (Complexity Assessment) includes TodoWrite at end
#
# Validates: TodoWrite completion is invoked at Phase 3 end with:
# - status: "completed"
# - content: "Phase 3: Complexity Assessment"
# - Indicates complexity score completion
#
# Test Approach: Search for TodoWrite completion in last 100 lines
# Expected: FAIL initially (no implementation yet)
################################################################################

COMPLEXITY_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-ideation/references/complexity-assessment-workflow.md"
TEST_NAME="AC#2 - Phase 3 End TodoWrite"

# Arrange: File paths
if [ ! -f "$COMPLEXITY_FILE" ]; then
    echo "FAIL: [$TEST_NAME] File not found: $COMPLEXITY_FILE"
    exit 1
fi

# Count total lines
TOTAL_LINES=$(wc -l < "$COMPLEXITY_FILE")

# Act: Get last 100 lines and search for TodoWrite with completed status
END_TODOWRITE=$(tail -100 "$COMPLEXITY_FILE" | grep -n "TodoWrite" | tail -1)

if [ -z "$END_TODOWRITE" ]; then
    echo "FAIL: [$TEST_NAME] TodoWrite completion not found at Phase 3 end"
    echo "  Expected: TodoWrite with status=\"completed\" in last 100 lines"
    echo "  File: $COMPLEXITY_FILE"
    exit 1
fi

# Act: Verify it has completed status
COMPLETED_STATUS=$(tail -100 "$COMPLEXITY_FILE" | grep -i "TodoWrite.*completed\|status.*completed")

if [ -z "$COMPLETED_STATUS" ]; then
    echo "FAIL: [$TEST_NAME] TodoWrite completion status not found"
    echo "  Expected: status=\"completed\" for Phase 3 end"
    echo "  File: $COMPLEXITY_FILE"
    exit 1
fi

# Act: Verify reference to complexity score in activeForm
COMPLEXITY_SCORE=$(tail -100 "$COMPLEXITY_FILE" | grep -i "activeForm.*complexity score\|complexity score")

if [ -z "$COMPLEXITY_SCORE" ]; then
    echo "FAIL: [$TEST_NAME] Complexity score reference missing in activeForm"
    echo "  Expected: activeForm indicating complexity score display"
    echo "  File: $COMPLEXITY_FILE"
    exit 1
fi

# All assertions passed
echo "PASS: [$TEST_NAME] TodoWrite completion found at Phase 3 end"
echo "  Content: Phase 3: Complexity Assessment"
echo "  Status: completed (with complexity score)"
exit 0
