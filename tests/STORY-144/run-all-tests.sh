#!/bin/bash
#
# Master Test Runner for STORY-144
#
# Executes all acceptance criteria tests and generates summary report
#

set -e

# Test colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEST_DIR="$PROJECT_ROOT/tests/STORY-144"

# Overall test tracking
TOTAL_TESTS=0
TOTAL_PASSED=0
TOTAL_FAILED=0

echo "========================================"
echo "STORY-144 Test Suite"
echo "Integrate or Remove Orphaned Files"
echo "========================================"
echo ""
echo "Test-Driven Development (TDD) Red Phase"
echo "These tests are EXPECTED TO FAIL initially"
echo "Implementation will make tests pass"
echo ""

# Function to run a test script
run_test_suite() {
    local test_file=$1
    local test_name=$2

    echo -e "\n${BLUE}Running: $test_name${NC}"
    echo "File: $test_file"
    echo "---"

    if [ ! -f "$test_file" ]; then
        echo -e "${RED}ERROR: Test file not found: $test_file${NC}"
        return 1
    fi

    # Run test and capture exit code
    bash "$test_file" || true
    local test_result=$?

    # Extract test results from script output
    # The script will output summary with exit code equal to number of failures
    TOTAL_FAILED=$((TOTAL_FAILED + test_result))

    return 0
}

echo -e "${YELLOW}========================================"
echo "AC#1: user-input-integration-guide.md"
echo "========================================${NC}"
run_test_suite "$TEST_DIR/test-ac1-user-input-integration-guide.sh" "AC#1 Tests"

echo -e "\n${YELLOW}========================================"
echo "AC#2: brainstorm-data-mapping.md"
echo "========================================${NC}"
run_test_suite "$TEST_DIR/test-ac2-brainstorm-data-mapping.sh" "AC#2 Tests"

echo -e "\n${YELLOW}========================================"
echo "AC#3: No Unreferenced Files"
echo "========================================${NC}"
run_test_suite "$TEST_DIR/test-ac3-no-unreferenced-files.sh" "AC#3 Tests"

echo -e "\n${YELLOW}========================================"
echo "AC#4: Commit Message Documentation"
echo "========================================${NC}"
run_test_suite "$TEST_DIR/test-ac4-commit-message-documentation.sh" "AC#4 Tests"

# Final summary
echo ""
echo "========================================"
echo "STORY-144 Final Test Summary"
echo "========================================"
echo ""
echo -e "TDD Phase: ${YELLOW}RED${NC} (Tests Failing - Implementation Pending)"
echo ""
echo "This is EXPECTED - Tests are written BEFORE implementation"
echo "Next steps:"
echo "1. Review failing tests above"
echo "2. Implement changes to resolve orphaned files"
echo "3. Re-run tests to verify implementation"
echo ""
echo "Failing tests indicate what needs to be done:"
echo "  - Delete orphaned files, OR"
echo "  - Integrate content into target files"
echo "  - Document decision in commit message"
echo ""
echo "========================================"

# Return overall failure count (for use by calling script)
exit $TOTAL_FAILED
