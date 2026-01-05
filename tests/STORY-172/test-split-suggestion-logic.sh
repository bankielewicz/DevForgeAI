#!/bin/bash

# STORY-172: RCA-013 Story Complexity Heuristics
# Technical Specification: Split Suggestion Logic
# Status: TDD Red (should FAIL - split suggestion logic not yet implemented)

set -e

PREFLIGHT_FILE="./.claude/skills/devforgeai-development/references/preflight-validation.md"
TEST_NAME="Split Suggestion Logic (from Tech Spec)"

echo "Running test: $TEST_NAME"
echo "Testing file: $PREFLIGHT_FILE"
echo "---"

if [ ! -f "$PREFLIGHT_FILE" ]; then
    echo "FAIL: preflight-validation.md file not found at $PREFLIGHT_FILE"
    exit 1
fi

# Test 1: Verify split suggestion logic section exists
echo "Test 1: Checking for Split Suggestion section..."
if ! grep -q "[Ss]plit.*[Ss]uggestion\|[Ss]how.*split" "$PREFLIGHT_FILE"; then
    echo "FAIL: Split Suggestion section not documented"
    echo "Expected: 'Split Suggestion Logic' or similar section"
    exit 1
fi
echo "PASS: Split Suggestion section found"

# Test 2: Verify DoD grouping by category is mentioned
echo "Test 2: Checking for DoD category grouping..."
if ! grep -q "[Gg]roup.*DoD\|DoD.*[Cc]ategory\|DoD.*items.*by" "$PREFLIGHT_FILE"; then
    echo "FAIL: DoD grouping by category not documented"
    echo "Expected: documentation of grouping DoD items by category"
    exit 1
fi
echo "PASS: DoD grouping by category documented"

# Test 3: Verify logical boundaries suggestion is mentioned
echo "Test 3: Checking for logical boundaries documentation..."
if ! grep -q "[Ll]ogical.*boundar\|STORY-A\|STORY-B\|items.*could be" "$PREFLIGHT_FILE"; then
    echo "FAIL: Logical boundaries suggestion not documented"
    echo "Expected: documentation suggesting logical boundaries for story split"
    exit 1
fi
echo "PASS: Logical boundaries documented"

echo "---"
echo "ALL TESTS PASSED for $TEST_NAME"
exit 0
