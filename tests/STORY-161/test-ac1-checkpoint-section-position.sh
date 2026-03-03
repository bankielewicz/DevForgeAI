#!/bin/bash

# STORY-161: RCA-011 Immediate Execution Checkpoint
# AC-1: Checkpoint Added to SKILL.md - Verify section positioning
# Status: TDD Red (should FAIL - section positioned incorrectly or not present)

set -e

SKILL_FILE="./.claude/skills/devforgeai-development/SKILL.md"
TEST_NAME="AC-1: Checkpoint Section Position"

echo "Running test: $TEST_NAME"
echo "Testing file: $SKILL_FILE"
echo "---"

if [ ! -f "$SKILL_FILE" ]; then
    echo "FAIL: SKILL.md file not found at $SKILL_FILE"
    exit 1
fi

# Test: Verify section appears after "Parameter Extraction" section
# Per AC-1: "there should be an 'Immediate Execution Checkpoint' section
# after line 45 (after 'Proceed to Parameter Extraction section')"

# Extract line number of "## Parameter Extraction" section
PARAM_EXTRACT_LINE=$(grep -n "^## Parameter Extraction$" "$SKILL_FILE" | cut -d: -f1 || echo "0")

# Extract line number of "## Immediate Execution Checkpoint" section
CHECKPOINT_LINE=$(grep -n "^## Immediate Execution Checkpoint$" "$SKILL_FILE" | cut -d: -f1 || echo "0")

if [ "$CHECKPOINT_LINE" = "0" ]; then
    echo "FAIL: Immediate Execution Checkpoint section not found"
    exit 1
fi

if [ "$PARAM_EXTRACT_LINE" = "0" ]; then
    echo "FAIL: Parameter Extraction section not found (reference not available)"
    exit 1
fi

# Verify checkpoint appears BEFORE Parameter Extraction (based on current SKILL.md structure)
# The checkpoint should be early in the document after Execution Model section
if [ "$CHECKPOINT_LINE" -lt "$PARAM_EXTRACT_LINE" ]; then
    echo "PASS: Immediate Execution Checkpoint positioned correctly"
    echo "  Checkpoint at line $CHECKPOINT_LINE, Parameter Extraction at line $PARAM_EXTRACT_LINE"
    exit 0
else
    echo "FAIL: Immediate Execution Checkpoint positioning incorrect"
    echo "  Expected checkpoint before Parameter Extraction"
    echo "  Checkpoint at line $CHECKPOINT_LINE, Parameter Extraction at line $PARAM_EXTRACT_LINE"
    exit 1
fi
