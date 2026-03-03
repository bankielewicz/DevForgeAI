#!/bin/bash
# STORY-231: Anti-Pattern Mining Test Suite
# TDD Red Phase - All tests expected to FAIL initially

set -e

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ANSI colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo -e "${BLUE}=============================================${NC}"
echo -e "${BLUE}  STORY-231: Anti-Pattern Mining Test Suite  ${NC}"
echo -e "${BLUE}  TDD Red Phase - Tests Expected to FAIL     ${NC}"
echo -e "${BLUE}=============================================${NC}"
echo ""

TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

run_test_file() {
    local test_file="$1"
    local test_name=$(basename "$test_file" .sh)

    echo -e "${YELLOW}Running: $test_name${NC}"
    echo "-------------------------------------------"

    if bash "$test_file"; then
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi

    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo ""
}

echo -e "${BLUE}=== AC#1: Anti-Pattern Matching ===${NC}"
echo ""

# Unit tests for AC#1
for test_file in "$TEST_DIR"/unit/test_antipattern_matching_*.sh; do
    if [ -f "$test_file" ]; then
        run_test_file "$test_file"
    fi
done

echo -e "${BLUE}=== AC#2: Violation Counting ===${NC}"
echo ""

# Unit tests for AC#2
for test_file in "$TEST_DIR"/unit/test_violation_counting_*.sh; do
    if [ -f "$test_file" ]; then
        run_test_file "$test_file"
    fi
done

echo -e "${BLUE}=== AC#3: Consequence Tracking ===${NC}"
echo ""

# Unit tests for AC#3
for test_file in "$TEST_DIR"/unit/test_consequence_tracking_*.sh; do
    if [ -f "$test_file" ]; then
        run_test_file "$test_file"
    fi
done

echo -e "${BLUE}=== Integration Tests ===${NC}"
echo ""

# Integration tests
for test_file in "$TEST_DIR"/integration/*.sh; do
    if [ -f "$test_file" ]; then
        run_test_file "$test_file"
    fi
done

echo -e "${BLUE}=== Edge Case Tests ===${NC}"
echo ""

# Edge case tests
for test_file in "$TEST_DIR"/edge-cases/*.sh; do
    if [ -f "$test_file" ]; then
        run_test_file "$test_file"
    fi
done

echo "============================================="
echo -e "${BLUE}  STORY-231 Test Summary${NC}"
echo "============================================="
echo "Total test files: $TOTAL_TESTS"
echo -e "Passed: ${GREEN}$PASSED_TESTS${NC}"
echo -e "Failed: ${RED}$FAILED_TESTS${NC}"
echo ""

if [ $FAILED_TESTS -gt 0 ]; then
    echo -e "${YELLOW}TDD Red Phase: $FAILED_TESTS test file(s) failed as expected.${NC}"
    echo -e "${YELLOW}Implement session-miner anti-pattern mining to make tests pass.${NC}"
    exit 1
else
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
fi
