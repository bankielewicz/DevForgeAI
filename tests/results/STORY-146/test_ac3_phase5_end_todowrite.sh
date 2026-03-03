#!/bin/bash

################################################################################
# Test: AC#3 - Phase 5 (Feasibility) includes TodoWrite at end
#
# Validates: TodoWrite completion is invoked at Phase 5 end with:
# - status: "completed"
# - content: "Phase 5: Feasibility & Constraints Analysis"
#
# Test Approach: Search for TodoWrite completion in last 100 lines
# Expected: FAIL initially (no implementation yet)
################################################################################

FEASIBILITY_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-ideation/references/feasibility-analysis-workflow.md"
TEST_NAME="AC#3 - Phase 5 End TodoWrite"

# Arrange: File paths
if [ ! -f "$FEASIBILITY_FILE" ]; then
    echo "FAIL: [$TEST_NAME] File not found: $FEASIBILITY_FILE"
    exit 1
fi

# Count total lines
TOTAL_LINES=$(wc -l < "$FEASIBILITY_FILE")

# Act: Get last 100 lines and search for TodoWrite with completed status
END_TODOWRITE=$(tail -100 "$FEASIBILITY_FILE" | grep -n "TodoWrite" | tail -1)

if [ -z "$END_TODOWRITE" ]; then
    echo "FAIL: [$TEST_NAME] TodoWrite completion not found at Phase 5 end"
    echo "  Expected: TodoWrite with status=\"completed\" in last 100 lines"
    echo "  File: $FEASIBILITY_FILE"
    exit 1
fi

# Act: Verify it has completed status
COMPLETED_STATUS=$(tail -100 "$FEASIBILITY_FILE" | grep -i "TodoWrite.*completed\|status.*completed")

if [ -z "$COMPLETED_STATUS" ]; then
    echo "FAIL: [$TEST_NAME] TodoWrite completion status not found"
    echo "  Expected: status=\"completed\" for Phase 5 end"
    echo "  File: $FEASIBILITY_FILE"
    exit 1
fi

# All assertions passed
echo "PASS: [$TEST_NAME] TodoWrite completion found at Phase 5 end"
echo "  Content: Phase 5: Feasibility & Constraints Analysis"
echo "  Status: completed"
exit 0
