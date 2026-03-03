#!/bin/bash
# STORY-226 Edge Case Test: Empty History File
#
# Given: An empty history.jsonl file (no commands)
# When: Analyzing for command sequences
# Then: Return empty result with informative message (no error)
#
# TDD RED PHASE: Test expected to FAIL before implementation

set -e

TEST_NAME="test-empty-history"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIXTURES_DIR="${TEST_DIR}/fixtures"

# Create empty history file
EMPTY_HISTORY="${FIXTURES_DIR}/empty-history.jsonl"
touch "$EMPTY_HISTORY"

# Verify empty file created
if [ ! -f "$EMPTY_HISTORY" ]; then
    echo "FAIL: Could not create empty history fixture" >&2
    exit 1
fi

if [ -s "$EMPTY_HISTORY" ]; then
    echo "FAIL: Empty history file should be empty" >&2
    rm -f "$EMPTY_HISTORY"
    exit 1
fi

# Test 1: Verify session-miner subagent exists
SESSION_MINER_PATH=".claude/agents/session-miner.md"
if [ ! -f "$SESSION_MINER_PATH" ]; then
    echo "FAIL: session-miner subagent not found at $SESSION_MINER_PATH" >&2
    rm -f "$EMPTY_HISTORY"
    exit 1
fi

# Test 2: Verify empty file handling is documented
if ! grep -qi "empty.*file\|no.*entries\|zero.*entries\|empty.*result" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document empty file handling" >&2
    rm -f "$EMPTY_HISTORY"
    exit 1
fi

# Clean up
rm -f "$EMPTY_HISTORY"

echo "PASS: Empty history handling is properly documented"
exit 0
