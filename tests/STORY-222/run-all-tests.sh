#!/bin/bash
#
# Test Runner for STORY-222 - Plan File Knowledge Base
# Executes all acceptance criteria tests and performance tests
#
# Usage:
#   ./run-all-tests.sh           # Run all tests
#   ./run-all-tests.sh ac1       # Run only AC#1 tests
#   ./run-all-tests.sh ac1 ac2   # Run AC#1 and AC#2 tests
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Test files
declare -A TEST_FILES=(
    [ac1]="$SCRIPT_DIR/test-ac1-yaml-frontmatter-parsing.sh"
    [ac2]="$SCRIPT_DIR/test-ac2-story-id-extraction.sh"
    [ac3]="$SCRIPT_DIR/test-ac3-decision-archive-mapping.sh"
    [ac4]="$SCRIPT_DIR/test-ac4-cross-reference-support.sh"
    [nfr]="$SCRIPT_DIR/test-nfr-010-performance.sh"
)

# Track results
declare -A RESULTS
TOTAL_TESTS=0
TOTAL_PASSED=0
TOTAL_FAILED=0
FAILED_TESTS=()

# Parse arguments - determine which tests to run
TESTS_TO_RUN=()
if [[ $# -eq 0 ]]; then
    # No arguments - run all tests
    TESTS_TO_RUN=("ac1" "ac2" "ac3" "ac4" "nfr")
else
    # Run specified tests
    for arg in "$@"; do
        TESTS_TO_RUN+=("$arg")
    done
fi

# ============================================================================
# Run a single test file
# ============================================================================
run_test() {
    local test_key="$1"
    local test_file="${TEST_FILES[$test_key]}"

    if [[ ! -f "$test_file" ]]; then
        echo -e "${RED}✗ Test file not found: $test_file${NC}"
        RESULTS[$test_key]="MISSING"
        TOTAL_FAILED=$((TOTAL_FAILED + 1))
        FAILED_TESTS+=("$test_key (file not found)")
        return 1
    fi

    if [[ ! -x "$test_file" ]]; then
        chmod +x "$test_file"
    fi

    # Run the test and capture output
    local output
    local exit_code=0
    output=$("$test_file" 2>&1) || exit_code=$?

    # Display test output
    echo "$output"
    echo ""

    # Determine result
    if [[ $exit_code -eq 0 ]]; then
        RESULTS[$test_key]="PASSED"
        # Count the passed tests from output
        local passed_count=$(echo "$output" | grep "Tests passed:" | tail -1 | grep -o '[0-9]\+$' || echo "0")
        TOTAL_PASSED=$((TOTAL_PASSED + passed_count))
    else
        RESULTS[$test_key]="FAILED"
        FAILED_TESTS+=("$test_key")
        local failed_count=$(echo "$output" | grep "Tests failed:" | tail -1 | grep -o '[0-9]\+$' || echo "1")
        TOTAL_FAILED=$((TOTAL_FAILED + failed_count))
    fi

    # Extract total test count
    local test_count=$(echo "$output" | grep "Tests run:" | tail -1 | grep -o '[0-9]\+$' || echo "0")
    TOTAL_TESTS=$((TOTAL_TESTS + test_count))
}

# ============================================================================
# Main execution
# ============================================================================
echo "========================================================================"
echo "STORY-222 Test Suite Runner"
echo "Plan File Knowledge Base for Decision Archive"
echo "========================================================================"
echo ""
echo "Running tests: ${TESTS_TO_RUN[*]}"
echo ""

# Run each test
for test_key in "${TESTS_TO_RUN[@]}"; do
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}Running: $test_key${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    run_test "$test_key"
done

# ============================================================================
# Print final summary
# ============================================================================
echo ""
echo "========================================================================"
echo "Final Summary - STORY-222 Test Suite"
echo "========================================================================"
echo ""

# Test-by-test results
for test_key in "${TESTS_TO_RUN[@]}"; do
    local result="${RESULTS[$test_key]}"
    if [[ "$result" == "PASSED" ]]; then
        echo -e "${GREEN}✓ $test_key${NC}: PASSED"
    elif [[ "$result" == "FAILED" ]]; then
        echo -e "${RED}✗ $test_key${NC}: FAILED"
    else
        echo -e "${YELLOW}? $test_key${NC}: $result"
    fi
done

echo ""
echo "Overall Statistics:"
echo "  Total tests run:    $TOTAL_TESTS"
echo "  Total passed:       $TOTAL_PASSED"
echo "  Total failed:       $TOTAL_FAILED"
echo ""

# Status message
if [[ $TOTAL_FAILED -eq 0 ]]; then
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}STATUS: ALL TESTS PASSED ✓${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    exit 0
else
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}STATUS: SOME TESTS FAILED ✗${NC}"
    echo -e "${RED}Failed tests: ${FAILED_TESTS[*]}${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    exit 1
fi
