#!/bin/bash

###############################################################################
# Test Suite Runner: STORY-157 - Batch Story Creation
###############################################################################
#
# Runs all test files for STORY-157 validation.
#
# Test Files:
# - test-ac1-marker-mapping.sh       (AC#1: Field Mapping)
# - test-ac2-batch-mode-invocation.sh (AC#2: Batch Mode Invocation)
# - test-ac3-sequential-processing.sh (AC#3: Sequential Processing)
# - test-ac4-failure-handling.sh      (AC#4: Failure Handling)
# - test-ac5-summary-report.sh        (AC#5: Summary Report)
# - test-br-business-rules.sh         (BR-001 to BR-004)
# - test-error-handling.sh            (Error Handling Section)
#
###############################################################################

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_DIR="$SCRIPT_DIR"
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_SKIPPED=0

# Array to store test results
declare -a TEST_RESULTS

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║    STORY-157: Batch Story Creation Test Suite                  ║"
echo "║    Testing: .claude/commands/create-stories-from-rca.md        ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Function to run a test file
run_test() {
    local test_file=$1
    local test_name=$(basename "$test_file" .sh)

    if [ ! -f "$test_file" ]; then
        echo -e "${YELLOW}⊘ SKIP${NC} - $test_name (File not found)"
        TESTS_SKIPPED=$((TESTS_SKIPPED + 1))
        return 1
    fi

    # Run test and capture result
    if bash "$test_file" > /tmp/test-output.txt 2>&1; then
        echo -e "${GREEN}✓ PASS${NC} - $test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        TEST_RESULTS+=("PASS: $test_name")
        return 0
    else
        echo -e "${RED}✗ FAIL${NC} - $test_name"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        TEST_RESULTS+=("FAIL: $test_name")

        # Display test output for failed tests
        echo "  Error details:"
        cat /tmp/test-output.txt | sed 's/^/    /'
        return 1
    fi
}

echo "Running tests..."
echo "=================================================="
echo ""

# Run all test files
run_test "$TEST_DIR/test-ac1-marker-mapping.sh"
run_test "$TEST_DIR/test-ac2-batch-mode-invocation.sh"
run_test "$TEST_DIR/test-ac3-sequential-processing.sh"
run_test "$TEST_DIR/test-ac4-failure-handling.sh"
run_test "$TEST_DIR/test-ac5-summary-report.sh"
run_test "$TEST_DIR/test-br-business-rules.sh"
run_test "$TEST_DIR/test-error-handling.sh"

echo ""
echo "=================================================="
echo "Test Summary"
echo "=================================================="
echo ""
echo -e "  ${GREEN}Passed:${NC}  $TESTS_PASSED"
echo -e "  ${RED}Failed:${NC}  $TESTS_FAILED"
echo -e "  ${YELLOW}Skipped:${NC} $TESTS_SKIPPED"
echo ""

TOTAL_TESTS=$((TESTS_PASSED + TESTS_FAILED + TESTS_SKIPPED))
echo "  Total:   $TOTAL_TESTS"
echo ""

# Print detailed results
if [ ${#TEST_RESULTS[@]} -gt 0 ]; then
    echo "Detailed Results:"
    echo "=================================================="
    for result in "${TEST_RESULTS[@]}"; do
        if [[ $result == PASS* ]]; then
            echo -e "  ${GREEN}✓${NC} ${result#PASS: }"
        else
            echo -e "  ${RED}✗${NC} ${result#FAIL: }"
        fi
    done
    echo ""
fi

# Exit code
if [ $TESTS_FAILED -eq 0 ] && [ $TESTS_PASSED -gt 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    exit 0
elif [ $TESTS_FAILED -gt 0 ]; then
    echo -e "${RED}❌ Some tests failed. Expected in TDD Red phase.${NC}"
    exit 1
else
    echo -e "${YELLOW}⊘ No tests executed${NC}"
    exit 2
fi
