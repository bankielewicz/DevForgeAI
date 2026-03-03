#!/bin/bash

# STORY-161: RCA-011 Immediate Execution Checkpoint
# AC-1: Checkpoint Added to SKILL.md - Verify section exists
# Status: TDD Red (should FAIL - section not yet added)

set -e

SKILL_FILE="./.claude/skills/devforgeai-development/SKILL.md"
TEST_NAME="AC-1: Checkpoint Section Exists"

echo "Running test: $TEST_NAME"
echo "Testing file: $SKILL_FILE"
echo "---"

if [ ! -f "$SKILL_FILE" ]; then
    echo "FAIL: SKILL.md file not found at $SKILL_FILE"
    exit 1
fi

# Test: Verify "## Immediate Execution Checkpoint" section exists
if grep -q "^## Immediate Execution Checkpoint$" "$SKILL_FILE"; then
    echo "PASS: Immediate Execution Checkpoint section header found"
    exit 0
else
    echo "FAIL: Immediate Execution Checkpoint section not found in SKILL.md"
    echo "Expected to find: '## Immediate Execution Checkpoint'"
    exit 1
fi
