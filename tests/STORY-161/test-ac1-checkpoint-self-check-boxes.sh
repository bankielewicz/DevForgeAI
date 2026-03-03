#!/bin/bash

# STORY-161: RCA-011 Immediate Execution Checkpoint
# AC-1: Checkpoint Added to SKILL.md - Verify 5 self-check boxes
# Status: TDD Red (should FAIL - checkboxes not present)

set -e

SKILL_FILE="./.claude/skills/devforgeai-development/SKILL.md"
TEST_NAME="AC-1: Checkpoint Self-Check Boxes"

echo "Running test: $TEST_NAME"
echo "Testing file: $SKILL_FILE"
echo "---"

if [ ! -f "$SKILL_FILE" ]; then
    echo "FAIL: SKILL.md file not found at $SKILL_FILE"
    exit 1
fi

# Find Immediate Execution Checkpoint section
CHECKPOINT_START=$(grep -n "^## Immediate Execution Checkpoint$" "$SKILL_FILE" | cut -d: -f1)

if [ -z "$CHECKPOINT_START" ]; then
    echo "FAIL: Immediate Execution Checkpoint section not found"
    exit 1
fi

# Get next section start line (next ## header)
NEXT_SECTION=$(awk "NR > $CHECKPOINT_START && /^## / {print NR; exit}" "$SKILL_FILE")

if [ -z "$NEXT_SECTION" ]; then
    # If no next section, use end of file
    NEXT_SECTION=$(wc -l < "$SKILL_FILE")
fi

# Extract checkpoint section content
SECTION_CONTENT=$(sed -n "$((CHECKPOINT_START + 1)),$((NEXT_SECTION - 1))p" "$SKILL_FILE")

# Count checkbox items (- [ ] pattern)
CHECKBOX_COUNT=$(echo "$SECTION_CONTENT" | grep -c "^\- \[ \]" || echo "0")

echo "Found $CHECKBOX_COUNT checkboxes in Immediate Execution Checkpoint section"

if [ "$CHECKBOX_COUNT" -ge 5 ]; then
    echo "PASS: Found at least 5 self-check checkboxes (found: $CHECKBOX_COUNT)"
    exit 0
else
    echo "FAIL: Expected at least 5 self-check checkboxes, found only $CHECKBOX_COUNT"
    echo "Per AC-1: 'Section includes 5 self-check boxes'"
    exit 1
fi
