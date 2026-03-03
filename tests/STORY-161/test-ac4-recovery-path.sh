#!/bin/bash

# STORY-161: RCA-011 Immediate Execution Checkpoint
# AC-4: Recovery Path - Verify clear recovery instructions
# Status: TDD Red (should FAIL - recovery path not present)

set -e

SKILL_FILE="./.claude/skills/devforgeai-development/SKILL.md"
TEST_NAME="AC-4: Recovery Path"

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

# Per AC-4: recovery path should provide clear instructions
# "Go directly to Phase 0 now. Do not ask questions."

PASS_COUNT=0
TOTAL_CHECKS=2

# Check for "Go directly to Phase 0 now" or similar
if echo "$SECTION_CONTENT" | grep -iq "go directly.*phase 0\|go.*phase 0"; then
    echo "PASS: 'Go directly to Phase 0' instruction found"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo "FAIL: 'Go directly to Phase 0' instruction not found"
fi

# Check for "Do not ask questions" or similar
if echo "$SECTION_CONTENT" | grep -iq "do not ask\|don't ask"; then
    echo "PASS: 'Do not ask questions' instruction found"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo "FAIL: 'Do not ask questions' instruction not found"
fi

echo "---"
echo "Recovery path checks passed: $PASS_COUNT/$TOTAL_CHECKS"

if [ "$PASS_COUNT" -eq "$TOTAL_CHECKS" ]; then
    echo "PASS: Recovery path is clear and complete"
    exit 0
else
    echo "FAIL: Recovery path incomplete"
    echo "Per AC-4: 'Go directly to Phase 0 now. Do not ask questions.'"
    exit 1
fi
