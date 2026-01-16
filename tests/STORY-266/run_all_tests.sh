#!/bin/bash
# =============================================================================
# STORY-266: Run All Acceptance Criteria Tests
# =============================================================================
# Executes all AC tests for STORY-266 and produces summary.
#
# Usage: ./run_all_tests.sh
#
# Expected: ALL FAIL (RED state - TDD phase, files don't exist yet)
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo -e "${BLUE}=============================================="
echo "STORY-266: Language-Agnostic Runtime Smoke Test"
echo "=============================================="
echo -e "Test Suite Execution${NC}"
echo ""
echo "Target files to be created:"
echo "  1. .claude/skills/devforgeai-qa/phases/phase-01-deep-validation.md (Step 1.3)"
echo "  2. .claude/skills/devforgeai-qa/assets/language-smoke-tests.yaml"
echo ""
echo -e "${YELLOW}Expected: ALL TESTS FAIL (TDD RED state)${NC}"
echo ""

# Track results
TOTAL_PASSED=0
TOTAL_FAILED=0
AC_RESULTS=()

# Function to run a test and capture results
run_test() {
    local test_name=$1
    local test_file=$2
    local ac_num=$3

    echo -e "${BLUE}----------------------------------------------${NC}"
    echo -e "${BLUE}Running: ${test_name}${NC}"
    echo -e "${BLUE}----------------------------------------------${NC}"

    if bash "${SCRIPT_DIR}/${test_file}"; then
        AC_RESULTS+=("${ac_num}:PASS")
        echo ""
    else
        AC_RESULTS+=("${ac_num}:FAIL")
        echo ""
    fi
}

# Run all AC tests
run_test "AC#1: Language Detection" "test-ac1-language-detection.sh" "AC1"
run_test "AC#2: Command Execution" "test-ac2-command-execution.sh" "AC2"
run_test "AC#3: Success Reporting" "test-ac3-success-reporting.sh" "AC3"
run_test "AC#4: CRITICAL Violation" "test-ac4-critical-violation.sh" "AC4"
run_test "AC#5: Extensible Pattern" "test-ac5-extensible-pattern.sh" "AC5"

# Calculate totals from test outputs
# Parse the last output line from each test for pass/fail counts

echo ""
echo -e "${BLUE}=============================================="
echo "STORY-266 Test Suite Summary"
echo -e "==============================================${NC}"
echo ""

# Display AC-level results
for result in "${AC_RESULTS[@]}"; do
    ac=$(echo "$result" | cut -d: -f1)
    status=$(echo "$result" | cut -d: -f2)
    if [ "$status" = "PASS" ]; then
        echo -e "  ${GREEN}[PASS]${NC} ${ac}"
    else
        echo -e "  ${RED}[FAIL]${NC} ${ac}"
        ((TOTAL_FAILED++))
    fi
done

echo ""
echo "----------------------------------------------"

# Final summary
if [ ${TOTAL_FAILED} -gt 0 ]; then
    echo -e "${RED}"
    echo "OVERALL: TESTS FAILED (RED state)"
    echo ""
    echo "This is EXPECTED for TDD Phase 02 (Test-First)"
    echo "Implementation files do not exist yet."
    echo ""
    echo "Next step: Implement the following files:"
    echo "  1. .claude/skills/devforgeai-qa/phases/phase-01-deep-validation.md"
    echo "     - Add Step 1.3 for runtime smoke test"
    echo "  2. .claude/skills/devforgeai-qa/assets/language-smoke-tests.yaml"
    echo "     - Create language configuration file"
    echo -e "${NC}"
    exit 1
else
    echo -e "${GREEN}"
    echo "OVERALL: ALL TESTS PASSED"
    echo ""
    echo "Story implementation is complete!"
    echo -e "${NC}"
    exit 0
fi
