#!/bin/bash

###############################################################################
# TEST RUNNER: run-all-tests.sh
# Executes all STORY-225 acceptance criteria tests
#
# Story: STORY-225 - Implement devforgeai-insights Skill for Mining Orchestration
# Purpose: Run complete test suite and report aggregate results
#
# Test Framework: Bash shell scripts (DevForgeAI standard)
# Location: /mnt/c/Projects/DevForgeAI2/tests/STORY-225/
#
# TDD Status: RED PHASE (All tests expected to FAIL initially)
###############################################################################

set -u

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Test counters
TOTAL_SUITES=0
SUITES_PASSED=0
SUITES_FAILED=0

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

###############################################################################
# Test Runner Functions
###############################################################################

run_test_suite() {
    local suite_name="$1"
    local suite_file="$2"

    ((TOTAL_SUITES++))

    echo ""
    echo -e "${BOLD}${CYAN}Running: ${suite_name}${NC}"
    echo "=============================================================="

    if [[ ! -f "${SCRIPT_DIR}/${suite_file}" ]]; then
        echo -e "${RED}  ERROR: Test file not found: ${suite_file}${NC}"
        ((SUITES_FAILED++))
        return 1
    fi

    # Run the test suite
    bash "${SCRIPT_DIR}/${suite_file}"
    local exit_code=$?

    if [[ ${exit_code} -eq 0 ]]; then
        ((SUITES_PASSED++))
    else
        ((SUITES_FAILED++))
    fi

    return ${exit_code}
}

###############################################################################
# Main Execution
###############################################################################

main() {
    echo ""
    echo "###################################################################"
    echo "#                                                                 #"
    echo "#    STORY-225: devforgeai-insights Skill Test Suite             #"
    echo "#    TDD Red Phase: All tests expected to FAIL                   #"
    echo "#                                                                 #"
    echo "###################################################################"
    echo ""
    echo "Date: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "Location: ${SCRIPT_DIR}"
    echo ""

    # Run all test suites
    run_test_suite "AC#1: Subagent Orchestration" "test-ac1-subagent-orchestration.sh"
    run_test_suite "AC#2: Result Aggregation" "test-ac2-result-aggregation.sh"
    run_test_suite "AC#3: Output Formatting" "test-ac3-output-formatting.sh"
    run_test_suite "AC#4: Result Caching" "test-ac4-result-caching.sh"
    run_test_suite "NFR: Skill Constraints" "test-nfr-skill-constraints.sh"

    # Print final summary
    echo ""
    echo ""
    echo "###################################################################"
    echo "#                     FINAL TEST SUMMARY                         #"
    echo "###################################################################"
    echo ""
    echo "  Test Suites Run:     ${TOTAL_SUITES}"
    echo "  Suites Passed:       ${SUITES_PASSED}"
    echo "  Suites Failed:       ${SUITES_FAILED}"
    echo ""

    if [[ ${SUITES_FAILED} -eq 0 ]]; then
        echo -e "${GREEN}${BOLD}  ALL TEST SUITES PASSED!${NC}"
        echo ""
        echo "  Skill implementation complete. Ready for QA validation."
        return 0
    else
        echo -e "${RED}${BOLD}  ${SUITES_FAILED} TEST SUITE(S) FAILED${NC}"
        echo ""
        echo "  TDD Red Phase: This is expected until skill implementation."
        echo ""
        echo "  Next Steps:"
        echo "  1. Create .claude/skills/devforgeai-insights/SKILL.md"
        echo "  2. Implement all acceptance criteria:"
        echo "     - AC#1: Subagent orchestration (session-miner invocation)"
        echo "     - AC#2: Result aggregation, filtering, ranking"
        echo "     - AC#3: Markdown output with tables, summaries, recommendations"
        echo "     - AC#4: 1-hour TTL caching mechanism"
        echo "  3. Re-run tests until all pass"
        echo ""
        return 1
    fi
}

# Run the test runner
main "$@"
