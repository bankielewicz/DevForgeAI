#!/bin/bash
# STORY-229: Categorize and Classify Session Errors - Master Test Runner
#
# This script runs all 12 tests for error categorization and classification:
# - 8 unit tests (error extraction, category classification, severity assignment, error registry)
# - 2 integration tests (pipeline, insights report)
# - 4 edge case tests (no errors, all errors, missing message, duplicates)
#
# TDD RED PHASE: Tests are expected to FAIL before implementation
#
# Acceptance Criteria Covered:
# - AC#1: Error Message Extraction (command, timestamp, session context)
# - AC#2: Category Classification (API, validation, timeout, context-overflow, file-not-found, other)
# - AC#3: Severity Assignment (critical, high, medium, low based on impact)
# - AC#4: Error Code Registry (ERR-001, ERR-002 codes for tracking)

# NOTE: Do NOT use set -e as we need to continue after test failures

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$TEST_DIR/../.." && pwd)"

# Change to project root for relative path resolution
cd "$PROJECT_ROOT"

TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
SKIPPED_TESTS=0

echo -e "${BLUE}================================================================${NC}"
echo -e "${BLUE}  STORY-229: Error Categorization and Classification - Test Suite${NC}"
echo -e "${BLUE}================================================================${NC}"
echo ""
echo "Test Breakdown:"
echo "  - 8 Unit Tests (error extraction, categories, severity, registry)"
echo "  - 2 Integration Tests (pipeline, insights report)"
echo "  - 4 Edge Cases (no errors, all errors, missing message, duplicates)"
echo ""
echo -e "${YELLOW}Status: TDD RED PHASE - Tests expected to FAIL${NC}"
echo ""
echo "Acceptance Criteria:"
echo "  AC#1: Error Message Extraction (command, timestamp, session)"
echo "  AC#2: Category Classification (API, validation, timeout, etc.)"
echo "  AC#3: Severity Assignment (critical, high, medium, low)"
echo "  AC#4: Error Code Registry (ERR-XXX tracking codes)"
echo ""

# Function to run a test script
run_test() {
    local test_script="$1"
    local test_name=$(basename "$test_script" .sh)

    if [ ! -f "$test_script" ]; then
        echo -e "  ${YELLOW}SKIP${NC}: $test_name (file not found)"
        ((SKIPPED_TESTS++))
        ((TOTAL_TESTS++))
        return 0
    fi

    # Make script executable
    chmod +x "$test_script" 2>/dev/null || true

    ((TOTAL_TESTS++))
    printf "  Running: %-50s " "$test_name"

    if bash "$test_script" >/dev/null 2>&1; then
        echo -e "${GREEN}PASS${NC}"
        ((PASSED_TESTS++))
    else
        echo -e "${RED}FAIL${NC}"
        ((FAILED_TESTS++))
    fi
}

# =============================================================================
# UNIT TESTS - AC#1: Error Message Extraction
# =============================================================================
echo -e "${CYAN}UNIT TESTS: AC#1 - Error Message Extraction${NC}"
echo "----------------------------------------------------------------"
run_test "$TEST_DIR/unit/test-ac1-error-extraction.sh"
run_test "$TEST_DIR/unit/test-ac1-error-context-capture.sh"
echo ""

# =============================================================================
# UNIT TESTS - AC#2: Category Classification
# =============================================================================
echo -e "${CYAN}UNIT TESTS: AC#2 - Category Classification${NC}"
echo "----------------------------------------------------------------"
run_test "$TEST_DIR/unit/test-ac2-category-classification.sh"
run_test "$TEST_DIR/unit/test-ac2-category-patterns.sh"
echo ""

# =============================================================================
# UNIT TESTS - AC#3: Severity Assignment
# =============================================================================
echo -e "${CYAN}UNIT TESTS: AC#3 - Severity Assignment${NC}"
echo "----------------------------------------------------------------"
run_test "$TEST_DIR/unit/test-ac3-severity-assignment.sh"
run_test "$TEST_DIR/unit/test-ac3-severity-rules.sh"
echo ""

# =============================================================================
# UNIT TESTS - AC#4: Error Code Registry
# =============================================================================
echo -e "${CYAN}UNIT TESTS: AC#4 - Error Code Registry${NC}"
echo "----------------------------------------------------------------"
run_test "$TEST_DIR/unit/test-ac4-error-registry.sh"
run_test "$TEST_DIR/unit/test-ac4-registry-tracking.sh"
echo ""

# =============================================================================
# INTEGRATION TESTS
# =============================================================================
echo -e "${CYAN}INTEGRATION TESTS${NC}"
echo "----------------------------------------------------------------"
run_test "$TEST_DIR/integration/test-error-analysis-pipeline.sh"
run_test "$TEST_DIR/integration/test-insights-error-report.sh"
echo ""

# =============================================================================
# EDGE CASE TESTS
# =============================================================================
echo -e "${CYAN}EDGE CASE TESTS${NC}"
echo "----------------------------------------------------------------"
run_test "$TEST_DIR/edge-cases/test-no-errors.sh"
run_test "$TEST_DIR/edge-cases/test-all-errors.sh"
run_test "$TEST_DIR/edge-cases/test-missing-error-message.sh"
run_test "$TEST_DIR/edge-cases/test-duplicate-errors.sh"
echo ""

# =============================================================================
# SUMMARY
# =============================================================================
echo -e "${BLUE}================================================================${NC}"
echo "Test Summary:"
echo "  Total:   $TOTAL_TESTS"
echo -e "  Passed:  ${GREEN}$PASSED_TESTS${NC}"
echo -e "  Failed:  ${RED}$FAILED_TESTS${NC}"
echo -e "  Skipped: ${YELLOW}$SKIPPED_TESTS${NC}"
echo -e "${BLUE}================================================================${NC}"

# Calculate pass rate
if [ $TOTAL_TESTS -gt 0 ]; then
    PASS_RATE=$((PASSED_TESTS * 100 / TOTAL_TESTS))
    echo "Pass Rate: $PASS_RATE%"
fi

echo ""

# Exit with appropriate status
if [ $FAILED_TESTS -gt 0 ]; then
    echo -e "${RED}TDD RED PHASE: Implementation required to make tests pass${NC}"
    echo ""
    echo "Next Steps:"
    echo "  1. Enhance session-miner.md with error extraction capability"
    echo "  2. Add category classification logic with pattern matching"
    echo "  3. Implement severity assignment rules"
    echo "  4. Create error code registry with ERR-XXX format"
    echo "  5. Integrate with devforgeai-insights for report generation"
    echo ""
    exit 1
else
    echo -e "${GREEN}All tests passed! Ready for QA validation.${NC}"
    exit 0
fi
