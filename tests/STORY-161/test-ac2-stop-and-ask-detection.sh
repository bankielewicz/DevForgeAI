#!/bin/bash

# STORY-161: RCA-011 Immediate Execution Checkpoint
# AC-2: Stop-and-Ask Detection - Verify checkpoint detects violations
# Status: TDD Red (should FAIL - detection descriptions not present)

set -e

SKILL_FILE="./.claude/skills/devforgeai-development/SKILL.md"
TEST_NAME="AC-2: Stop-and-Ask Detection"

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

# Per AC-2: checkpoint should detect these behaviors:
# - Token budget
# - Time constraints
# - Approach/scope options
# - Waiting passively

PASS_COUNT=0
TOTAL_CHECKS=4

# Check for token budget mention
if echo "$SECTION_CONTENT" | grep -iq "token.*budget"; then
    echo "PASS: Token budget mentioned"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo "FAIL: Token budget not mentioned"
fi

# Check for time constraints mention
if echo "$SECTION_CONTENT" | grep -iq "time.*constraint"; then
    echo "PASS: Time constraints mentioned"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo "FAIL: Time constraints not mentioned"
fi

# Check for approach/scope mention
if echo "$SECTION_CONTENT" | grep -iq "approach\|scope"; then
    echo "PASS: Approach/scope mentioned"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo "FAIL: Approach/scope not mentioned"
fi

# Check for waiting passively mention
if echo "$SECTION_CONTENT" | grep -iq "wait.*passive\|passively"; then
    echo "PASS: Waiting passively mentioned"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo "FAIL: Waiting passively not mentioned"
fi

echo "---"
echo "Detection checks passed: $PASS_COUNT/$TOTAL_CHECKS"

if [ "$PASS_COUNT" -eq "$TOTAL_CHECKS" ]; then
    echo "PASS: All stop-and-ask behaviors detected"
    exit 0
else
    echo "FAIL: Not all stop-and-ask behaviors mentioned"
    echo "Per AC-2: checkpoint should detect token budget, time constraints, approach/scope, and waiting passively"
    exit 1
fi
