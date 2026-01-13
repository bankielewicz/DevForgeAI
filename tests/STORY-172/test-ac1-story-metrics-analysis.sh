#!/bin/bash

# STORY-172: RCA-013 Story Complexity Heuristics
# AC#1: Analyze Story Metrics at Phase 0
# Status: TDD Red (should FAIL - Step 11 not yet added to preflight-validation.md)

set -e

PREFLIGHT_FILE="./.claude/skills/devforgeai-development/references/preflight/_index.md"
TEST_NAME="AC#1: Analyze Story Metrics at Phase 0"

echo "Running test: $TEST_NAME"
echo "Testing file: $PREFLIGHT_FILE"
echo "---"

if [ ! -f "$PREFLIGHT_FILE" ]; then
    echo "FAIL: preflight-validation.md file not found at $PREFLIGHT_FILE"
    exit 1
fi

# Test 1: Verify Step 11 section exists
echo "Test 1: Checking for Step 11: Story Complexity Analysis section..."
if ! grep -q "Step 11.*Story Complexity Analysis" "$PREFLIGHT_FILE"; then
    echo "FAIL: Step 11: Story Complexity Analysis section not found"
    echo "Expected to find: 'Step 11: Story Complexity Analysis' or similar"
    exit 1
fi
echo "PASS: Step 11 section found"

# Test 2: Verify DoD item count metric is documented
echo "Test 2: Checking for DoD item count metric..."
if ! grep -q "dod_count\|DoD item count\|DoD items" "$PREFLIGHT_FILE"; then
    echo "FAIL: DoD item count metric not documented"
    echo "Expected: documentation of 'dod_count' or 'DoD item count' metric"
    exit 1
fi
echo "PASS: DoD item count metric documented"

# Test 3: Verify Acceptance criteria count metric is documented
echo "Test 3: Checking for Acceptance Criteria count metric..."
if ! grep -q "ac_count\|Acceptance [Cc]riteria count\|AC count" "$PREFLIGHT_FILE"; then
    echo "FAIL: Acceptance Criteria count metric not documented"
    echo "Expected: documentation of 'ac_count' or 'Acceptance Criteria count' metric"
    exit 1
fi
echo "PASS: Acceptance Criteria count metric documented"

# Test 4: Verify Technical specification size metric is documented
echo "Test 4: Checking for Technical Specification size metric..."
if ! grep -q "tech_spec_lines\|[Tt]ech[nical]* [Ss]pec.* size\|[Tt]ech[nical]* [Ss]pecification.* lines" "$PREFLIGHT_FILE"; then
    echo "FAIL: Technical Specification size metric not documented"
    echo "Expected: documentation of 'tech_spec_lines' or 'Technical Specification size' metric"
    exit 1
fi
echo "PASS: Technical Specification size metric documented"

# Test 5: Verify File touch count metric is documented
echo "Test 5: Checking for File touch count metric..."
if ! grep -q "files_touched\|[Ff]ile.* touch.* count\|[Ff]iles.* mentioned" "$PREFLIGHT_FILE"; then
    echo "FAIL: File touch count metric not documented"
    echo "Expected: documentation of 'files_touched' or 'File touch count' metric"
    exit 1
fi
echo "PASS: File touch count metric documented"

echo "---"
echo "ALL TESTS PASSED for $TEST_NAME"
exit 0
