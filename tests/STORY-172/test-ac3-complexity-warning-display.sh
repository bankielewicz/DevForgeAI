#!/bin/bash

# STORY-172: RCA-013 Story Complexity Heuristics
# AC#3: Display Complexity Warning
# Status: TDD Red (should FAIL - warning display not yet implemented)

set -e

PREFLIGHT_FILE="./.claude/skills/devforgeai-development/references/preflight-validation.md"
TEST_NAME="AC#3: Display Complexity Warning"

echo "Running test: $TEST_NAME"
echo "Testing file: $PREFLIGHT_FILE"
echo "---"

if [ ! -f "$PREFLIGHT_FILE" ]; then
    echo "FAIL: preflight-validation.md file not found at $PREFLIGHT_FILE"
    exit 1
fi

# Test 1: Verify warning display section exists
echo "Test 1: Checking for Warning Display section..."
if ! grep -q "Warning.*[Dd]isplay\|STORY COMPLEXITY ASSESSMENT" "$PREFLIGHT_FILE"; then
    echo "FAIL: Warning Display section not documented"
    echo "Expected: 'Warning Display' section or 'STORY COMPLEXITY ASSESSMENT' header"
    exit 1
fi
echo "PASS: Warning Display section found"

# Test 2: Verify complexity level is displayed
echo "Test 2: Checking for complexity level in warning..."
if ! grep -q "[Cc]omplexity.*[Ll]evel\|complexity_level" "$PREFLIGHT_FILE"; then
    echo "FAIL: Complexity level not shown in warning"
    echo "Expected: documentation of 'Complexity Level: {complexity_level}' display"
    exit 1
fi
echo "PASS: Complexity level in warning documented"

# Test 3: Verify metrics display format (shows which metrics exceeded thresholds)
echo "Test 3: Checking for metrics display in warning..."
if ! grep -q "[Mm]etrics:" "$PREFLIGHT_FILE"; then
    echo "FAIL: Metrics section not shown in warning"
    echo "Expected: 'Metrics:' section in warning display"
    exit 1
fi
echo "PASS: Metrics section documented"

# Test 4: Verify threshold values are shown in warning
echo "Test 4: Checking for threshold display in warning..."
if ! grep -q "threshold:" "$PREFLIGHT_FILE"; then
    echo "FAIL: Threshold values not shown in warning"
    echo "Expected: '(threshold: XX)' format in warning display"
    exit 1
fi
echo "PASS: Threshold values in warning documented"

# Test 5: Verify suggestion to break story is included
echo "Test 5: Checking for story split suggestion..."
if ! grep -q "[Bb]reak.*into.*smaller.*stories\|[Ss]plit\|multiple.*TDD.*iterations" "$PREFLIGHT_FILE"; then
    echo "FAIL: Suggestion to break story not documented"
    echo "Expected: suggestion like 'Consider: Break into smaller stories?'"
    exit 1
fi
echo "PASS: Story split suggestion documented"

# Test 6: Verify warning only shows when score >= 2 (HIGH or above)
echo "Test 6: Checking for HIGH threshold trigger (score >= 2)..."
if ! grep -q "score.*>=.*2\|[Hh][Ii][Gg][Hh].*warning" "$PREFLIGHT_FILE"; then
    echo "FAIL: HIGH threshold trigger condition not documented"
    echo "Expected: 'score >= 2' or 'HIGH' warning condition"
    exit 1
fi
echo "PASS: HIGH threshold trigger documented"

echo "---"
echo "ALL TESTS PASSED for $TEST_NAME"
exit 0
