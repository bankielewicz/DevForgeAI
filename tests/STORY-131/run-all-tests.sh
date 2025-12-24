#!/bin/bash

##############################################################################
# Master Test Suite: STORY-131 - Delegate Summary Presentation to Skill
#
# Comprehensive test execution for all acceptance criteria:
#   AC#1: Phase 4 Removal Preserves Functionality
#   AC#2: Command Invokes ideation-result-interpreter Subagent
#   AC#3: Command Phase 3 Invokes Result Interpreter
#   AC#4: Command Size Reduction Achieved
#   AC#5: Summary Displays Once Per Session
#
# This script:
#   1. Runs all individual test suites
#   2. Aggregates results
#   3. Provides comprehensive summary
#   4. Returns appropriate exit code
##############################################################################

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test directory
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"

# Test counters
TOTAL_SUITES=0
PASSED_SUITES=0
FAILED_SUITES=0

TOTAL_TESTS=0
TOTAL_PASSED=0
TOTAL_FAILED=0

##############################################################################
# Helper Functions
##############################################################################

run_test_suite() {
    local test_file="$1"
    local suite_name=$(basename "$test_file" .sh)

    TOTAL_SUITES=$((TOTAL_SUITES + 1))

    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║ Running: $suite_name"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""

    if [[ ! -f "$test_file" ]]; then
        echo -e "${RED}ERROR${NC}: Test file not found: $test_file"
        FAILED_SUITES=$((FAILED_SUITES + 1))
        return 1
    fi

    # Make executable
    chmod +x "$test_file"

    # Run test and capture output
    if bash "$test_file"; then
        echo ""
        echo -e "${GREEN}✓ $suite_name PASSED${NC}"
        PASSED_SUITES=$((PASSED_SUITES + 1))
        return 0
    else
        echo ""
        echo -e "${RED}✗ $suite_name FAILED${NC}"
        FAILED_SUITES=$((FAILED_SUITES + 1))
        return 1
    fi
}

##############################################################################
# Main Execution
##############################################################################

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  STORY-131: Delegate Summary Presentation to Skill             ║"
echo "║  Comprehensive Test Suite Execution                            ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Verify test directory exists
if [[ ! -d "$TEST_DIR" ]]; then
    echo -e "${RED}ERROR${NC}: Test directory not found: $TEST_DIR"
    exit 1
fi

echo "Test directory: $TEST_DIR"
echo "Project root: $PROJECT_ROOT"
echo ""

# Run all test suites in order
echo -e "${BLUE}Executing test suites...${NC}"
echo ""

# Test Suite 1: AC#1 - Phase 4 Removal
run_test_suite "$TEST_DIR/test-ac1-phase4-removal.sh"

# Test Suite 2 & 3: AC#2 & AC#3 - Subagent Invocation
run_test_suite "$TEST_DIR/test-ac2-ac3-subagent-invocation.sh"

# Test Suite 4: AC#4 - Size Reduction
run_test_suite "$TEST_DIR/test-ac4-size-reduction.sh"

# Test Suite 5: AC#5 - Single Summary
run_test_suite "$TEST_DIR/test-ac5-single-summary.sh"

##############################################################################
# Summary Report
##############################################################################

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  Comprehensive Test Results Summary"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

echo "Test Suites:"
echo "  Total:    $TOTAL_SUITES"
echo -e "  Passed:   ${GREEN}$PASSED_SUITES${NC}"
echo -e "  Failed:   ${RED}$FAILED_SUITES${NC}"
echo ""

if [[ $FAILED_SUITES -eq 0 ]]; then
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "✓ ALL TEST SUITES PASSED"
    echo -e "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "STORY-131 Implementation Status:"
    echo "  ✓ AC#1: Phase 4 removal verified"
    echo "  ✓ AC#2: Subagent invocation verified"
    echo "  ✓ AC#3: Command Phase 3 verified"
    echo "  ✓ AC#4: Size reduction verified"
    echo "  ✓ AC#5: Single summary verified"
    echo ""
    echo "Next Steps:"
    echo "  1. Review implementation against test results"
    echo "  2. Update AC Checklist in story file"
    echo "  3. Commit changes to git"
    echo "  4. Mark story as 'Dev Complete'"
    exit 0
else
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "✗ SOME TEST SUITES FAILED"
    echo -e "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "Failed Suites: $FAILED_SUITES of $TOTAL_SUITES"
    echo ""
    echo "Review the test output above to identify failures."
    echo "Common issues:"
    echo "  - Phase 4 section not fully removed from ideate.md"
    echo "  - Task() invocation missing or incorrectly formatted"
    echo "  - File size reduction target not met"
    echo "  - Multiple summary invocations detected"
    exit 1
fi
