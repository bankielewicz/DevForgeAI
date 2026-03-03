#!/bin/bash

# STORY-162 AC-1: Tracker Expanded to ~15 Items
# Test that TodoWrite tracker in SKILL.md has approximately 15 items (was 9)
#
# This test SHOULD FAIL initially (Red phase - TDD)
# Implementation needed: Expand TodoWrite from 10 to ~15 items in SKILL.md

set -e

SKILL_FILE=".claude/skills/devforgeai-development/SKILL.md"
EXPECTED_ITEM_COUNT=15
TOLERANCE=2  # Allow 13-17 items

echo "TEST: AC-1 - Tracker Expanded to ~15 Items"
echo "=========================================="
echo ""

# Check if SKILL.md exists
if [ ! -f "$SKILL_FILE" ]; then
    echo "FAIL: $SKILL_FILE does not exist"
    exit 1
fi

# Extract TodoWrite array section from SKILL.md
# Look for TodoWrite( ... ) block
if ! grep -q "TodoWrite(" "$SKILL_FILE"; then
    echo "FAIL: TodoWrite section not found in $SKILL_FILE"
    exit 1
fi

echo "Looking for TodoWrite array items..."
echo ""

# Count the number of {content: items in the TodoWrite section
# Extract from TodoWrite( to the closing )
TODOWRITE_CONTENT=$(sed -n '/^TodoWrite(/,/^)/p' "$SKILL_FILE")

# Count lines with {content: pattern (each todo item)
ITEM_COUNT=$(echo "$TODOWRITE_CONTENT" | grep -c '{content:' || true)

echo "Current item count: $ITEM_COUNT"
echo "Expected count: $EXPECTED_ITEM_COUNT (tolerance: ±$TOLERANCE items)"
echo ""

# Check if count is within tolerance
MIN_COUNT=$((EXPECTED_ITEM_COUNT - TOLERANCE))
MAX_COUNT=$((EXPECTED_ITEM_COUNT + TOLERANCE))

if [ "$ITEM_COUNT" -ge "$MIN_COUNT" ] && [ "$ITEM_COUNT" -le "$MAX_COUNT" ]; then
    echo "PASS: TodoWrite tracker has $ITEM_COUNT items (expected ~$EXPECTED_ITEM_COUNT)"
    exit 0
else
    echo "FAIL: TodoWrite tracker has $ITEM_COUNT items, expected $EXPECTED_ITEM_COUNT (±$TOLERANCE)"
    echo ""
    echo "Current items:"
    echo "$TODOWRITE_CONTENT" | grep -n '{content:' || echo "  (none found)"
    exit 1
fi
