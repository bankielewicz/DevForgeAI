#!/bin/bash

# STORY-172: RCA-013 Story Complexity Heuristics
# AC#5: Log Complexity for Retrospective
# Status: TDD Red (should FAIL - complexity logging not yet implemented)

set -e

PREFLIGHT_FILE="./.claude/skills/devforgeai-development/references/preflight-validation.md"
TEST_NAME="AC#5: Log Complexity for Retrospective"

echo "Running test: $TEST_NAME"
echo "Testing file: $PREFLIGHT_FILE"
echo "---"

if [ ! -f "$PREFLIGHT_FILE" ]; then
    echo "FAIL: preflight-validation.md file not found at $PREFLIGHT_FILE"
    exit 1
fi

# Test 1: Verify complexity logging is mentioned
echo "Test 1: Checking for complexity logging documentation..."
if ! grep -q "[Ll]og.*[Cc]omplexity\|[Cc]omplexity.*[Ll]ogg" "$PREFLIGHT_FILE"; then
    echo "FAIL: Complexity logging not documented"
    echo "Expected: documentation of logging complexity for retrospective"
    exit 1
fi
echo "PASS: Complexity logging mentioned"

# Test 2: Verify actual iterations vs predicted is mentioned
echo "Test 2: Checking for actual vs predicted comparison..."
if ! grep -q "actual.*iteration\|iteration.*predicted\|vs.*predicted" "$PREFLIGHT_FILE"; then
    echo "FAIL: Actual iterations vs predicted comparison not documented"
    echo "Expected: documentation of comparing actual iterations to predicted complexity"
    exit 1
fi
echo "PASS: Actual vs predicted comparison documented"

# Test 3: Verify framework learning is mentioned
echo "Test 3: Checking for framework learning documentation..."
if ! grep -q "[Ff]ramework.*[Ll]earning\|[Rr]etrospective\|[Cc]alibrat" "$PREFLIGHT_FILE"; then
    echo "FAIL: Framework learning/retrospective not documented"
    echo "Expected: documentation of using data for framework improvement"
    exit 1
fi
echo "PASS: Framework learning documented"

# Test 4: Verify logging happens after development completes
echo "Test 4: Checking for post-development logging trigger..."
if ! grep -q "[Aa]fter.*development\|[Ww]hen.*development.*completes\|[Dd]evelopment.*complete" "$PREFLIGHT_FILE"; then
    echo "FAIL: Post-development logging trigger not documented"
    echo "Expected: documentation that logging occurs 'when development completes'"
    exit 1
fi
echo "PASS: Post-development logging trigger documented"

echo "---"
echo "ALL TESTS PASSED for $TEST_NAME"
exit 0
