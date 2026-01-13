#!/bin/bash

# STORY-172: RCA-013 Story Complexity Heuristics
# AC#2: Apply Complexity Thresholds
# Status: TDD Red (should FAIL - thresholds not yet defined in preflight-validation.md)

set -e

PREFLIGHT_FILE="./.claude/skills/devforgeai-development/references/preflight/_index.md"
TEST_NAME="AC#2: Apply Complexity Thresholds"

echo "Running test: $TEST_NAME"
echo "Testing file: $PREFLIGHT_FILE"
echo "---"

if [ ! -f "$PREFLIGHT_FILE" ]; then
    echo "FAIL: preflight-validation.md file not found at $PREFLIGHT_FILE"
    exit 1
fi

# Test 1: DoD threshold - High (>20)
echo "Test 1: Checking DoD High threshold (>20)..."
if ! grep -q "dod_count.*>.*20\|DoD.*>.*20.*=.*[Hh]igh" "$PREFLIGHT_FILE"; then
    echo "FAIL: DoD High threshold (>20) not documented"
    echo "Expected: 'DoD items: >20 = High' or similar pattern"
    exit 1
fi
echo "PASS: DoD High threshold documented"

# Test 2: DoD threshold - Very High (>30)
echo "Test 2: Checking DoD Very High threshold (>30)..."
if ! grep -q "dod_count.*>.*30\|DoD.*>.*30.*=.*[Vv]ery.*[Hh]igh" "$PREFLIGHT_FILE"; then
    echo "FAIL: DoD Very High threshold (>30) not documented"
    echo "Expected: 'DoD items: >30 = Very High' or similar pattern"
    exit 1
fi
echo "PASS: DoD Very High threshold documented"

# Test 3: AC threshold - High (>5)
echo "Test 3: Checking AC High threshold (>5)..."
if ! grep -q "ac_count.*>.*5\|AC.*>.*5.*=.*[Hh]igh" "$PREFLIGHT_FILE"; then
    echo "FAIL: AC High threshold (>5) not documented"
    echo "Expected: 'AC count: >5 = High' or similar pattern"
    exit 1
fi
echo "PASS: AC High threshold documented"

# Test 4: AC threshold - Very High (>8)
echo "Test 4: Checking AC Very High threshold (>8)..."
if ! grep -q "ac_count.*>.*8\|AC.*>.*8.*=.*[Vv]ery.*[Hh]igh" "$PREFLIGHT_FILE"; then
    echo "FAIL: AC Very High threshold (>8) not documented"
    echo "Expected: 'AC count: >8 = Very High' or similar pattern"
    exit 1
fi
echo "PASS: AC Very High threshold documented"

# Test 5: Tech spec lines threshold - High (>100)
echo "Test 5: Checking Tech spec High threshold (>100)..."
if ! grep -q "tech_spec_lines.*>.*100\|[Tt]ech.*spec.*>.*100.*=.*[Hh]igh" "$PREFLIGHT_FILE"; then
    echo "FAIL: Tech spec High threshold (>100) not documented"
    echo "Expected: 'Tech spec lines: >100 = High' or similar pattern"
    exit 1
fi
echo "PASS: Tech spec High threshold documented"

# Test 6: Tech spec lines threshold - Very High (>200)
echo "Test 6: Checking Tech spec Very High threshold (>200)..."
if ! grep -q "tech_spec_lines.*>.*200\|[Tt]ech.*spec.*>.*200.*=.*[Vv]ery.*[Hh]igh" "$PREFLIGHT_FILE"; then
    echo "FAIL: Tech spec Very High threshold (>200) not documented"
    echo "Expected: 'Tech spec lines: >200 = Very High' or similar pattern"
    exit 1
fi
echo "PASS: Tech spec Very High threshold documented"

# Test 7: Files touched threshold - High (>10)
echo "Test 7: Checking Files touched High threshold (>10)..."
if ! grep -q "files_touched.*>.*10\|[Ff]iles.*>.*10.*=.*[Hh]igh" "$PREFLIGHT_FILE"; then
    echo "FAIL: Files touched High threshold (>10) not documented"
    echo "Expected: 'Files touched: >10 = High' or similar pattern"
    exit 1
fi
echo "PASS: Files touched High threshold documented"

# Test 8: Files touched threshold - Very High (>20)
echo "Test 8: Checking Files touched Very High threshold (>20)..."
if ! grep -q "files_touched.*>.*20\|[Ff]iles.*>.*20.*=.*[Vv]ery.*[Hh]igh" "$PREFLIGHT_FILE"; then
    echo "FAIL: Files touched Very High threshold (>20) not documented"
    echo "Expected: 'Files touched: >20 = Very High' or similar pattern"
    exit 1
fi
echo "PASS: Files touched Very High threshold documented"

# Test 9: Complexity scoring logic documented
echo "Test 9: Checking complexity scoring logic..."
if ! grep -q "complexity_score\|complexity_level" "$PREFLIGHT_FILE"; then
    echo "FAIL: Complexity scoring logic not documented"
    echo "Expected: 'complexity_score' or 'complexity_level' calculation"
    exit 1
fi
echo "PASS: Complexity scoring logic documented"

echo "---"
echo "ALL TESTS PASSED for $TEST_NAME"
exit 0
