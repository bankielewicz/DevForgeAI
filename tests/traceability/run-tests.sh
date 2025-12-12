#!/bin/bash
#
# Master Test Runner for STORY-083 Requirements Traceability Matrix
#
# Runs all test suites and reports overall results
#

set -o pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Test suites configuration
SUITES=(
    "test_epic_parsing.sh:Epic Parsing:AC#1:12"
    "test_story_parsing.sh:Story Parsing:AC#2:11"
    "test_data_model.sh:Data Model:AC#3:8"
    "test_validation.sh:Validation:AC#4:8"
    "test_orphan_detection.sh:Orphan Detection:AC#5:8"
    "test_performance.sh:Performance:AC#6:6"
)

# Overall counters
TOTAL_SUITES=0
SUITES_PASSED=0
SUITES_FAILED=0
TOTAL_TESTS=0
TOTAL_PASSED=0
TOTAL_FAILED=0

##############################################################################
# Functions
##############################################################################

run_suite() {
    local file="$1"
    local name="$2"
    local ac="$3"
    local expected_count="$4"

    TOTAL_SUITES=$((TOTAL_SUITES + 1))

    echo -e "\n${CYAN}╭──────────────────────────────────────────────────────────╮${NC}"
    echo -e "${CYAN}│ ${name} Tests (${ac}) - ${expected_count} tests${NC}"
    echo -e "${CYAN}╰──────────────────────────────────────────────────────────╯${NC}"

    if [ ! -f "${SCRIPT_DIR}/${file}" ]; then
        echo -e "${RED}✗ Test file not found: ${file}${NC}"
        SUITES_FAILED=$((SUITES_FAILED + 1))
        return 1
    fi

    # Run test suite and capture output
    local output exit_code
    output=$(bash "${SCRIPT_DIR}/${file}" 2>&1)
    exit_code=$?

    # Extract results from output
    local tests_run tests_passed tests_failed
    tests_run=$(echo "$output" | grep "Tests Run:" | awk '{print $NF}')
    tests_passed=$(echo "$output" | grep "Tests Passed:" | sed 's/\x1b\[[0-9;]*m//g' | awk '{print $NF}')
    tests_failed=$(echo "$output" | grep "Tests Failed:" | sed 's/\x1b\[[0-9;]*m//g' | awk '{print $NF}')

    # Display summary for this suite
    if [ "$exit_code" -eq 0 ]; then
        echo -e "${GREEN}✓${NC} ${name}: ${tests_passed}/${tests_run} tests passed"
        SUITES_PASSED=$((SUITES_PASSED + 1))
    else
        echo -e "${RED}✗${NC} ${name}: ${tests_passed}/${tests_run} tests passed, ${tests_failed} failed"
        SUITES_FAILED=$((SUITES_FAILED + 1))
        # Show failures
        echo "$output" | grep -A 1 "FAILED$" | head -20
    fi

    # Update totals
    TOTAL_TESTS=$((TOTAL_TESTS + ${tests_run:-0}))
    TOTAL_PASSED=$((TOTAL_PASSED + ${tests_passed:-0}))
    TOTAL_FAILED=$((TOTAL_FAILED + ${tests_failed:-0}))
}

##############################################################################
# Main Execution
##############################################################################

main() {
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║                                                          ║${NC}"
    echo -e "${BLUE}║  STORY-083: Requirements Traceability Matrix            ║${NC}"
    echo -e "${BLUE}║            Master Test Suite                             ║${NC}"
    echo -e "${BLUE}║                                                          ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"

    # Export WSL2_SLOW if running on WSL2 (check kernel name)
    if uname -r | grep -qi "microsoft"; then
        export WSL2_SLOW=1
        echo -e "${YELLOW}Detected WSL2 - Using extended performance thresholds${NC}"
    fi

    # Run all test suites
    for suite in "${SUITES[@]}"; do
        IFS=':' read -r file name ac count <<< "$suite"
        run_suite "$file" "$name" "$ac" "$count"
    done

    # Overall summary
    echo ""
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║                    OVERALL SUMMARY                       ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "  Test Suites: ${TOTAL_SUITES}"
    echo -e "  Suites Passed: ${GREEN}${SUITES_PASSED}${NC}"
    echo -e "  Suites Failed: ${RED}${SUITES_FAILED}${NC}"
    echo ""
    echo -e "  Total Tests: ${TOTAL_TESTS}"
    echo -e "  Tests Passed: ${GREEN}${TOTAL_PASSED}${NC}"
    echo -e "  Tests Failed: ${RED}${TOTAL_FAILED}${NC}"
    echo ""

    # Check if all acceptance criteria passed
    if [ "$SUITES_FAILED" -eq 0 ]; then
        echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
        echo -e "${GREEN}║                 ✓ ALL TESTS PASSED                       ║${NC}"
        echo -e "${GREEN}║          All 6 Acceptance Criteria Verified              ║${NC}"
        echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
        exit 0
    else
        echo -e "${RED}╔══════════════════════════════════════════════════════════╗${NC}"
        echo -e "${RED}║                 ✗ SOME TESTS FAILED                      ║${NC}"
        echo -e "${RED}╚══════════════════════════════════════════════════════════╝${NC}"
        exit 1
    fi
}

main "$@"
