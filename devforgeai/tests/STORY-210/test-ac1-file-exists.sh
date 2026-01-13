#!/bin/bash

################################################################################
# TEST SUITE: AC#1 - PATTERNS.md File Created
# Story: STORY-210
# Description: Verify PATTERNS.md file exists at correct location
#
# Acceptance Criteria:
# - File exists at devforgeai/RCA/PATTERNS.md
# - File is readable
# - File is not empty (has content)
#
# Test Status: FAILING (Red Phase) - file does not yet exist
################################################################################

set -e

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEST_NAME="AC#1: PATTERNS.md File Created"
PATTERNS_FILE="$PROJECT_ROOT/devforgeai/RCA/PATTERNS.md"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Helper function to assert file exists
assert_file_exists() {
    local file_path="$1"
    local description="$2"
    ((TESTS_RUN++))

    if [ -f "$file_path" ]; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        echo "  File: $file_path"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Expected file: $file_path"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Helper function to assert file is readable
assert_file_readable() {
    local file_path="$1"
    local description="$2"
    ((TESTS_RUN++))

    if [ -f "$file_path" ] && [ -r "$file_path" ]; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  File not readable: $file_path"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Helper function to assert file is non-empty
assert_file_nonempty() {
    local file_path="$1"
    local description="$2"
    ((TESTS_RUN++))

    if [ -f "$file_path" ] && [ -s "$file_path" ]; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        local file_size=$(wc -c < "$file_path")
        echo "  File size: $file_size bytes"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  File is empty or does not exist: $file_path"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Print test header
echo ""
echo "====== $TEST_NAME ======"
echo ""

# Run tests
assert_file_exists "$PATTERNS_FILE" "PATTERNS.md file exists at devforgeai/RCA/PATTERNS.md" || true
assert_file_readable "$PATTERNS_FILE" "PATTERNS.md file is readable" || true
assert_file_nonempty "$PATTERNS_FILE" "PATTERNS.md file is not empty" || true

# Print summary
echo ""
echo "====== Test Results ======"
echo "Tests run:   $TESTS_RUN"
echo "Passed:      $TESTS_PASSED"
echo "Failed:      $TESTS_FAILED"

# Exit with appropriate code
if [ "$TESTS_FAILED" -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed${NC}"
    exit 1
fi
