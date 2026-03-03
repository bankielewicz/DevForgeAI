#!/bin/bash
# ============================================================================
# STORY-122: Line Ending Normalization - Master Test Runner
# ============================================================================
#
# Runs all tests for STORY-122 and reports results.
# Tests are organized into: unit, integration, edge-cases
#
# Usage: bash tests/STORY-122/run_all_tests.sh
#
# Exit codes:
#   0 - All tests passed
#   1 - One or more tests failed
#   77 - Test skipped (missing prerequisites)
# ============================================================================

set -o pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
GITATTRIBUTES_PATH="$PROJECT_ROOT/.gitattributes"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0
SKIPPED=0
TOTAL=0

# Results array
declare -a TEST_RESULTS

# Function to run a single test
run_test() {
    local test_file="$1"
    local test_name=$(basename "$test_file" .sh)
    local category=$(basename "$(dirname "$test_file")")

    ((TOTAL++))

    printf "  Running %-40s " "[$category] $test_name..."

    # Run test and capture output
    local output
    local exit_code
    output=$(bash "$test_file" 2>&1)
    exit_code=$?

    case $exit_code in
        0)
            echo -e "${GREEN}PASS${NC}"
            ((PASSED++))
            TEST_RESULTS+=("PASS: [$category] $test_name")
            ;;
        77)
            echo -e "${YELLOW}SKIP${NC}"
            ((SKIPPED++))
            TEST_RESULTS+=("SKIP: [$category] $test_name")
            ;;
        *)
            echo -e "${RED}FAIL${NC}"
            ((FAILED++))
            TEST_RESULTS+=("FAIL: [$category] $test_name")
            # Print failure output indented
            echo "$output" | sed 's/^/    /'
            ;;
    esac
}

# Header
echo ""
echo "============================================================================"
echo "  STORY-122: Line Ending Normalization - Test Suite"
echo "============================================================================"
echo ""
echo "Project Root: $PROJECT_ROOT"
echo ".gitattributes: $([ -f "$GITATTRIBUTES_PATH" ] && echo "EXISTS" || echo "NOT FOUND")"
echo ""

# Run unit tests
echo -e "${BLUE}Unit Tests:${NC}"
for test in "$SCRIPT_DIR"/unit/test_*.sh; do
    [ -f "$test" ] && run_test "$test"
done
echo ""

# Run integration tests
echo -e "${BLUE}Integration Tests:${NC}"
for test in "$SCRIPT_DIR"/integration/test_*.sh; do
    [ -f "$test" ] && run_test "$test"
done
echo ""

# Run edge case tests
echo -e "${BLUE}Edge Case Tests:${NC}"
for test in "$SCRIPT_DIR"/edge-cases/test_*.sh; do
    [ -f "$test" ] && run_test "$test"
done
echo ""

# Summary
echo "============================================================================"
echo "  Test Summary"
echo "============================================================================"
echo ""
echo -e "  Total:   $TOTAL"
echo -e "  ${GREEN}Passed:  $PASSED${NC}"
echo -e "  ${RED}Failed:  $FAILED${NC}"
echo -e "  ${YELLOW}Skipped: $SKIPPED${NC}"
echo ""

# Detailed results
if [ ${#TEST_RESULTS[@]} -gt 0 ]; then
    echo "Results:"
    for result in "${TEST_RESULTS[@]}"; do
        echo "  $result"
    done
    echo ""
fi

# Final status
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}RESULT: FAILED${NC} - $FAILED test(s) failed"
    exit 1
elif [ $PASSED -eq 0 ] && [ $SKIPPED -gt 0 ]; then
    echo -e "${YELLOW}RESULT: ALL SKIPPED${NC} - Prerequisites not met"
    exit 77
else
    echo -e "${GREEN}RESULT: PASSED${NC} - All tests passed"
    exit 0
fi
