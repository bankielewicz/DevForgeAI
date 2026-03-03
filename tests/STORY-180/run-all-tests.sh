#!/bin/bash
# =============================================================================
# STORY-180: Run All AC Tests
# =============================================================================
# Master test runner for all STORY-180 acceptance criteria tests.
#
# Expected to FAIL initially (TDD Red Phase) - all 5 ACs are not implemented.
#
# Run: bash tests/STORY-180/run-all-tests.sh
# =============================================================================

set -uo pipefail
# Note: -e removed to allow continuing after test failures

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo "========================================================================"
echo -e "${CYAN}STORY-180: Pass Context File Summaries to Subagents${NC}"
echo "========================================================================"
echo ""
echo "Running all acceptance criteria tests..."
echo ""

# Track overall results
TOTAL_TESTS=0
TOTAL_PASSED=0
TOTAL_FAILED=0

# Function to run a test file and capture results
run_test() {
    local test_file=$1
    local ac_name=$2

    echo "------------------------------------------------------------------------"
    echo -e "${CYAN}$ac_name${NC}"
    echo "------------------------------------------------------------------------"

    if bash "$test_file"; then
        echo -e "${GREEN}AC PASSED${NC}"
        ((TOTAL_PASSED++))
    else
        echo -e "${RED}AC FAILED (expected in TDD Red phase)${NC}"
        ((TOTAL_FAILED++))
    fi

    ((TOTAL_TESTS++))
    echo ""
}

# Run all AC tests
run_test "$SCRIPT_DIR/test-ac1-context-summary-format.sh" \
         "AC-1: Context Summary Format Defined"

run_test "$SCRIPT_DIR/test-ac2-anti-pattern-scanner-accepts-summary.sh" \
         "AC-2: Anti-Pattern Scanner Accepts Summary"

run_test "$SCRIPT_DIR/test-ac3-subagent-documentation-updated.sh" \
         "AC-3: Subagent Documentation Updated"

run_test "$SCRIPT_DIR/test-ac4-qa-skill-passes-summaries.sh" \
         "AC-4: QA Skill Passes Summaries"

run_test "$SCRIPT_DIR/test-ac5-token-reduction-measurable.sh" \
         "AC-5: Token Reduction Measurable"

# Summary
echo "========================================================================"
echo -e "${CYAN}STORY-180 Test Summary${NC}"
echo "========================================================================"
echo ""
echo "Acceptance Criteria Results:"
echo "  Passed: $TOTAL_PASSED"
echo "  Failed: $TOTAL_FAILED"
echo "  Total:  $TOTAL_TESTS"
echo ""

if [[ $TOTAL_FAILED -gt 0 ]]; then
    echo -e "${YELLOW}TDD Red Phase: $TOTAL_FAILED AC(s) failing as expected${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Implement AC-1: Add Context Summary Format section to anti-pattern-scanner.md"
    echo "  2. Implement AC-2: Update anti-pattern-scanner.md input contract"
    echo "  3. Implement AC-3: Add conditional summary usage documentation"
    echo "  4. Implement AC-4: Update parallel-validation.md with summary passing"
    echo "  5. Implement AC-5: Document token reduction metrics"
    exit 1
else
    echo -e "${GREEN}All acceptance criteria tests passing!${NC}"
    exit 0
fi
