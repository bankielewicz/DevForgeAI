#!/bin/bash
# STORY-226: Analyze Command Sequence Patterns - Master Test Runner
#
# This script runs all 12 tests for command sequence pattern analysis:
# - 6 unit tests (n-gram extraction, success rates, report generation)
# - 2 integration tests (pipeline, insights command)
# - 4 edge case tests (empty, single command, malformed, fewer than 10)
#
# TDD RED PHASE: Tests are expected to FAIL before implementation
#
# Acceptance Criteria Covered:
# - AC#1: N-gram Sequence Extraction (2-gram and 3-gram)
# - AC#2: Success Rate Correlation
# - AC#3: Top Patterns Report (top 10 by frequency with success rates)

set -e

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
echo -e "${BLUE}  STORY-226: Command Sequence Pattern Analysis - Test Suite${NC}"
echo -e "${BLUE}================================================================${NC}"
echo ""
echo "Test Breakdown:"
echo "  - 6 Unit Tests (n-gram extraction, success rate, report)"
echo "  - 2 Integration Tests (pipeline, insights command)"
echo "  - 4 Edge Cases (empty, single, malformed, few patterns)"
echo ""
echo -e "${YELLOW}Status: TDD RED PHASE - Tests expected to FAIL${NC}"
echo ""
echo "Acceptance Criteria:"
echo "  AC#1: N-gram Sequence Extraction (2-gram and 3-gram)"
echo "  AC#2: Success Rate Correlation"
echo "  AC#3: Top Patterns Report"
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
    printf "  Running: %-45s " "$test_name"

    if bash "$test_script" >/dev/null 2>&1; then
        echo -e "${GREEN}PASS${NC}"
        ((PASSED_TESTS++))
    else
        echo -e "${RED}FAIL${NC}"
        ((FAILED_TESTS++))
    fi
}

# =============================================================================
# UNIT TESTS - AC#1: N-gram Extraction
# =============================================================================
echo -e "${CYAN}UNIT TESTS: AC#1 - N-gram Sequence Extraction${NC}"
echo "----------------------------------------------------------------"
run_test "$TEST_DIR/unit/test-ac1-2gram-extraction.sh"
run_test "$TEST_DIR/unit/test-ac1-3gram-extraction.sh"
echo ""

# =============================================================================
# UNIT TESTS - AC#2: Success Rate Correlation
# =============================================================================
echo -e "${CYAN}UNIT TESTS: AC#2 - Success Rate Correlation${NC}"
echo "----------------------------------------------------------------"
run_test "$TEST_DIR/unit/test-ac2-success-rate-calculation.sh"
run_test "$TEST_DIR/unit/test-ac2-success-rate-edge-cases.sh"
echo ""

# =============================================================================
# UNIT TESTS - AC#3: Top Patterns Report
# =============================================================================
echo -e "${CYAN}UNIT TESTS: AC#3 - Top Patterns Report${NC}"
echo "----------------------------------------------------------------"
run_test "$TEST_DIR/unit/test-ac3-top-patterns-report.sh"
run_test "$TEST_DIR/unit/test-ac3-report-ranking.sh"
echo ""

# =============================================================================
# INTEGRATION TESTS
# =============================================================================
echo -e "${CYAN}INTEGRATION TESTS${NC}"
echo "----------------------------------------------------------------"
run_test "$TEST_DIR/integration/test-session-miner-integration.sh"
run_test "$TEST_DIR/integration/test-insights-command-patterns.sh"
echo ""

# =============================================================================
# EDGE CASE TESTS
# =============================================================================
echo -e "${CYAN}EDGE CASE TESTS${NC}"
echo "----------------------------------------------------------------"
run_test "$TEST_DIR/edge-cases/test-empty-history.sh"
run_test "$TEST_DIR/edge-cases/test-single-command-session.sh"
run_test "$TEST_DIR/edge-cases/test-malformed-entries.sh"
run_test "$TEST_DIR/edge-cases/test-fewer-than-10-patterns.sh"
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
    echo "  1. Enhance session-miner.md with n-gram extraction logic"
    echo "  2. Add success rate calculation per sequence"
    echo "  3. Integrate with devforgeai-insights for report formatting"
    echo "  4. Document edge case handling"
    echo ""
    exit 1
else
    echo -e "${GREEN}All tests passed! Ready for QA validation.${NC}"
    exit 0
fi
