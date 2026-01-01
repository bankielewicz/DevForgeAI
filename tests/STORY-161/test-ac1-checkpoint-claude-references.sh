#!/bin/bash

# STORY-161: RCA-011 Immediate Execution Checkpoint
# AC-1: Checkpoint Added to SKILL.md - Verify CLAUDE.md references
# Status: TDD Red (should FAIL - references not present)

set -e

SKILL_FILE="./.claude/skills/devforgeai-development/SKILL.md"
TEST_NAME="AC-1: Checkpoint CLAUDE.md References"

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

# Test: Verify CLAUDE.md reference exists
if echo "$SECTION_CONTENT" | grep -q "CLAUDE.md"; then
    echo "PASS: CLAUDE.md reference found in checkpoint section"
    exit 0
else
    echo "FAIL: CLAUDE.md reference not found in checkpoint section"
    echo "Per AC-1: 'References CLAUDE.md guidance'"
    exit 1
fi
