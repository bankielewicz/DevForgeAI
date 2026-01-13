#!/bin/bash

################################################################################
# TEST RUNNER: STORY-210 - PATTERNS.md Knowledge Base
# Description: Orchestrate all AC validation tests and provide summary
#
# Test Status: TDD Red Phase - All tests expected to fail initially
################################################################################

# Note: NOT using set -e since we need to continue running tests even if some fail

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TESTS_DIR="$PROJECT_ROOT/devforgeai/tests/STORY-210"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "============================================================"
echo "  STORY-210: PATTERNS.md Knowledge Base Validation Tests"
echo "============================================================"
echo ""

# Test counters
TOTAL_TESTS_PASSED=0
TOTAL_TESTS_FAILED=0
TEST_FILES_PASSED=0
TEST_FILES_FAILED=0

# Run each test file
for test_file in "$TESTS_DIR"/test-ac*.sh; do
    if [ ! -f "$test_file" ]; then
        continue
    fi

    test_name=$(basename "$test_file")
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Running: $test_name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    # Execute test file and capture result
    if bash "$test_file" 2>&1; then
        echo ""
        echo -e "${GREEN}✓ $test_name PASSED${NC}"
        ((TEST_FILES_PASSED++))
    else
        echo ""
        echo -e "${RED}✗ $test_name FAILED${NC}"
        ((TEST_FILES_FAILED++))
    fi

    echo ""
done

# Print overall summary
echo "============================================================"
echo "  Test Suite Summary"
echo "============================================================"
echo ""
echo "Test files run:     $((TEST_FILES_PASSED + TEST_FILES_FAILED))"
echo "Test files passed:  $TEST_FILES_PASSED"
echo "Test files failed:  $TEST_FILES_FAILED"
echo ""

# Determine overall result
if [ "$TEST_FILES_FAILED" -eq 0 ]; then
    echo -e "${GREEN}✓ ALL TESTS PASSED${NC}"
    echo ""
    echo "Status: TDD Green Phase - Ready for implementation"
    exit 0
else
    echo -e "${RED}✗ SOME TESTS FAILED${NC}"
    echo ""
    echo "Status: TDD Red Phase - ${TEST_FILES_FAILED} test file(s) failing"
    echo "This is expected. Implementation should make all tests pass."
    exit 1
fi
