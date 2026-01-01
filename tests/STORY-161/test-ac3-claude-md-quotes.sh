#!/bin/bash

# STORY-161: RCA-011 Immediate Execution Checkpoint
# AC-3: CLAUDE.md References - Verify required quotes present
# Status: TDD Red (should FAIL - quotes not present)

set -e

SKILL_FILE="./.claude/skills/devforgeai-development/SKILL.md"
TEST_NAME="AC-3: CLAUDE.md References"

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
    NEXT_SECTION=$(wc -l < "$SKILL_FILE")
fi

# Extract checkpoint section content
SECTION_CONTENT=$(sed -n "$((CHECKPOINT_START + 1)),$((NEXT_SECTION - 1))p" "$SKILL_FILE")

# Per AC-3: error message should quote CLAUDE.md statements:
# - "There are no time constraints"
# - "Your context window is plenty big"
# - "Focus on quality"

PASS_COUNT=0
TOTAL_CHECKS=3

# Check for "no time constraints" or similar
if echo "$SECTION_CONTENT" | grep -q "no time constraint"; then
    echo "PASS: 'no time constraint' reference found"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo "FAIL: 'no time constraint' reference not found"
fi

# Check for "context window is plenty big" or similar
if echo "$SECTION_CONTENT" | grep -iq "context window.*plenty"; then
    echo "PASS: 'context window is plenty big' reference found"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo "FAIL: 'context window is plenty big' reference not found"
fi

# Check for "Focus on quality" or similar
if echo "$SECTION_CONTENT" | grep -iq "focus.*quality"; then
    echo "PASS: 'Focus on quality' reference found"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo "FAIL: 'Focus on quality' reference not found"
fi

echo "---"
echo "CLAUDE.md quote checks passed: $PASS_COUNT/$TOTAL_CHECKS"

if [ "$PASS_COUNT" -ge 2 ]; then
    echo "PASS: Required CLAUDE.md guidance quoted"
    exit 0
else
    echo "FAIL: Not enough CLAUDE.md guidance quoted"
    echo "Per AC-3: error message should quote at least 2-3 CLAUDE.md statements"
    exit 1
fi
