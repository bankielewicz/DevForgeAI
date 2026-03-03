#!/bin/bash
# STORY-121: Story-Scoped Pre-Commit Validation - Master Test Runner
#
# This script runs all 11 tests for story-scoped pre-commit validation:
# - 4 unit tests (filtering logic, messages)
# - 4 integration tests (multi-story commits, scoped vs unscoped)
# - 3 edge case tests (format validation, empty var, case sensitivity)
#
# TDD RED PHASE: Tests are expected to FAIL before implementation

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
SKIPPED_TESTS=0

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}STORY-121: Story-Scoped Pre-Commit Validation - Test Suite${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Test Breakdown:"
echo "  • 4 Unit Tests (filtering logic, message output)"
echo "  • 4 Integration Tests (multi-story scenarios)"
echo "  • 3 Edge Cases (format, empty var, case sensitivity)"
echo ""
echo -e "${YELLOW}Status: TDD RED PHASE - Tests expected to FAIL${NC}"
echo ""

# Function to run a test script
run_test() {
    local test_script="$1"
    local test_name=$(basename "$test_script" .sh)

    if [ ! -f "$test_script" ]; then
        echo -e "${YELLOW}SKIP${NC}: $test_name (file not found)"
        ((SKIPPED_TESTS++))
        ((TOTAL_TESTS++))
        return 0
    fi

    echo -n "Running: $test_name ... "
    ((TOTAL_TESTS++))

    if bash "$test_script" >/dev/null 2>&1; then
        echo -e "${GREEN}PASS${NC}"
        ((PASSED_TESTS++))
    else
        echo -e "${RED}FAIL${NC}"
        ((FAILED_TESTS++))
    fi
}

# Unit Tests
echo -e "${BLUE}UNIT TESTS${NC}"
echo "─────────────────────────────────────────────────────────────────"
run_test "$TEST_DIR/unit/test_scoped_filtering.sh"
run_test "$TEST_DIR/unit/test_unscoped_fallback.sh"
run_test "$TEST_DIR/unit/test_scoped_message.sh"
run_test "$TEST_DIR/unit/test_unscoped_message.sh"
echo ""

# Integration Tests
echo -e "${BLUE}INTEGRATION TESTS${NC}"
echo "─────────────────────────────────────────────────────────────────"
run_test "$TEST_DIR/integration/test_scoped_commit_blocks_other.sh"
run_test "$TEST_DIR/integration/test_unscoped_blocks_all.sh"
run_test "$TEST_DIR/integration/test_multiple_stories_scoped.sh"
run_test "$TEST_DIR/integration/test_explicit_story_id.sh"
echo ""

# Edge Cases
echo -e "${BLUE}EDGE CASE TESTS${NC}"
echo "─────────────────────────────────────────────────────────────────"
run_test "$TEST_DIR/edge-cases/test_invalid_format.sh"
run_test "$TEST_DIR/edge-cases/test_empty_env_var.sh"
run_test "$TEST_DIR/edge-cases/test_case_sensitivity.sh"
echo ""

# Summary
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo "Test Summary:"
echo "  Total:   $TOTAL_TESTS"
echo "  Passed:  ${GREEN}$PASSED_TESTS${NC}"
echo "  Failed:  ${RED}$FAILED_TESTS${NC}"
echo "  Skipped: ${YELLOW}$SKIPPED_TESTS${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"

# Exit with failure if any tests failed (TDD RED phase - failures expected)
if [ $FAILED_TESTS -gt 0 ]; then
    echo ""
    echo -e "${RED}TDD RED PHASE: Implementation required to make tests pass${NC}"
    exit 1
else
    echo ""
    echo -e "${GREEN}All tests passed! Moving to GREEN phase (implementation).${NC}"
    exit 0
fi
