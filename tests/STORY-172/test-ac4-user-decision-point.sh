#!/bin/bash

# STORY-172: RCA-013 Story Complexity Heuristics
# AC#4: User Decision Point
# Status: TDD Red (should FAIL - user decision point not yet implemented)

set -e

PREFLIGHT_FILE="./.claude/skills/devforgeai-development/references/preflight/_index.md"
TEST_NAME="AC#4: User Decision Point"

echo "Running test: $TEST_NAME"
echo "Testing file: $PREFLIGHT_FILE"
echo "---"

if [ ! -f "$PREFLIGHT_FILE" ]; then
    echo "FAIL: preflight-validation.md file not found at $PREFLIGHT_FILE"
    exit 1
fi

# Test 1: Verify AskUserQuestion is used for decision point
echo "Test 1: Checking for AskUserQuestion usage..."
if ! grep -q "AskUserQuestion" "$PREFLIGHT_FILE"; then
    echo "FAIL: AskUserQuestion not used for complexity decision point"
    echo "Expected: AskUserQuestion invocation in complexity section"
    exit 1
fi
echo "PASS: AskUserQuestion usage found"

# Test 2: Verify Option 1 - Continue
echo "Test 2: Checking for 'Continue' option..."
if ! grep -q "[Cc]ontinue.*[Ii] understand.*large story\|[Cc]ontinue.*this is a large story" "$PREFLIGHT_FILE"; then
    echo "FAIL: 'Continue - I understand this is a large story' option not documented"
    echo "Expected: 'Continue - I understand this is a large story' option"
    exit 1
fi
echo "PASS: Continue option documented"

# Test 3: Verify Option 2 - Show split suggestions
echo "Test 3: Checking for 'Show me what could be split' option..."
if ! grep -q "[Ss]how.*what could be split\|[Ss]how.*split" "$PREFLIGHT_FILE"; then
    echo "FAIL: 'Show me what could be split out' option not documented"
    echo "Expected: 'Show me what could be split out' option"
    exit 1
fi
echo "PASS: Show split option documented"

# Test 4: Verify Option 3 - Stop
echo "Test 4: Checking for 'Stop' option..."
if ! grep -q "[Ss]top.*break.*smaller stories\|[Ss]top.*I'll break" "$PREFLIGHT_FILE"; then
    echo "FAIL: 'Stop - I'll break this into smaller stories first' option not documented"
    echo "Expected: 'Stop - I'll break this into smaller stories first' option"
    exit 1
fi
echo "PASS: Stop option documented"

# Test 5: Verify multiSelect is false (single selection)
echo "Test 5: Checking for single selection mode..."
if ! grep -q "multiSelect.*false" "$PREFLIGHT_FILE"; then
    echo "FAIL: multiSelect: false not documented"
    echo "Expected: 'multiSelect: false' in AskUserQuestion configuration"
    exit 1
fi
echo "PASS: Single selection mode documented"

# Test 6: Verify 3 options are defined
echo "Test 6: Verifying all 3 options are defined..."
# Check for the specific option keywords
CONTINUE_FOUND=$(grep -c "[Cc]ontinue.*large story" "$PREFLIGHT_FILE" || echo "0")
SPLIT_FOUND=$(grep -c "[Ss]how.*split" "$PREFLIGHT_FILE" || echo "0")
STOP_FOUND=$(grep -c "[Ss]top.*smaller stories\|[Ss]top.*I'll break" "$PREFLIGHT_FILE" || echo "0")

if [ "$CONTINUE_FOUND" -lt 1 ] || [ "$SPLIT_FOUND" -lt 1 ] || [ "$STOP_FOUND" -lt 1 ]; then
    echo "FAIL: Not all 3 decision options are defined"
    echo "Found: Continue=$CONTINUE_FOUND, Split=$SPLIT_FOUND, Stop=$STOP_FOUND"
    echo "Expected: All 3 options (Continue, Show split, Stop) defined"
    exit 1
fi
echo "PASS: All 3 options defined"

echo "---"
echo "ALL TESTS PASSED for $TEST_NAME"
exit 0
