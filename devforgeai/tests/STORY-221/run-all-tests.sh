#!/bin/bash
###############################################################################
# STORY-221 Test Runner - Execute all AC tests
#
# Purpose: Run all acceptance criteria tests and generate summary report
# Usage: ./run-all-tests.sh
###############################################################################

set -uo pipefail

# Color codes for output
BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
TOTAL_PASSED=0
TOTAL_FAILED=0
TOTAL_TESTS=0

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

###############################################################################
# Test execution function
###############################################################################

run_test_file() {
    local test_file="$1"
    local test_name=$(basename "$test_file" .sh)

    echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}Running: $test_name${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════════════${NC}"
    echo ""

    # Make test executable
    chmod +x "$test_file"

    # Run test and capture results
    if bash "$test_file" 2>&1; then
        local exit_code=0
    else
        local exit_code=$?
    fi

    echo ""
    return $exit_code
}

###############################################################################
# Main execution
###############################################################################

main() {
    echo -e "${YELLOW}╔═══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║${NC}  STORY-221: Parse and Normalize history.jsonl Data for Session Mining    ${YELLOW}║${NC}"
    echo -e "${YELLOW}║${NC}  Comprehensive Test Suite (TDD Red Phase)                                 ${YELLOW}║${NC}"
    echo -e "${YELLOW}╚═══════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""

    # Find all test files
    local test_files=()
    while IFS= read -r -d '' file; do
        test_files+=("$file")
    done < <(find "$SCRIPT_DIR" -maxdepth 1 -name "test-*.sh" -print0 | sort -z)

    if [ ${#test_files[@]} -eq 0 ]; then
        echo -e "${RED}ERROR: No test files found in $SCRIPT_DIR${NC}"
        exit 1
    fi

    # Run each test file
    local test_results=()
    for test_file in "${test_files[@]}"; do
        if run_test_file "$test_file"; then
            test_results+=("PASS")
        else
            test_results+=("FAIL")
        fi
    done

    ###############################################################################
    # Generate Summary Report
    ###############################################################################

    echo ""
    echo -e "${YELLOW}╔═══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║${NC}  COMPLETE TEST SUITE SUMMARY                                             ${YELLOW}║${NC}"
    echo -e "${YELLOW}╚═══════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""

    # Count results
    local passed=0
    local failed=0
    for result in "${test_results[@]}"; do
        if [ "$result" == "PASS" ]; then
            ((passed++))
        else
            ((failed++))
        fi
    done

    # Print detailed results
    echo "Test Results by Acceptance Criteria:"
    echo ""

    local i=0
    for test_file in "${test_files[@]}"; do
        local test_name=$(basename "$test_file" .sh)
        local result="${test_results[$i]}"
        local color="${GREEN}"

        if [ "$result" == "FAIL" ]; then
            color="${RED}"
        fi

        echo -e "${color}  [${result}]${NC} $test_name"
        ((i++))
    done

    echo ""
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════════════════${NC}"
    echo "Summary Statistics:"
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════════════════${NC}"
    echo "Total Test Suites:  ${#test_files[@]}"
    echo -e "${GREEN}Passed:             $passed${NC}"
    echo -e "${RED}Failed:             $failed${NC}"

    local pass_rate=0
    if [ ${#test_files[@]} -gt 0 ]; then
        pass_rate=$(( (passed * 100) / ${#test_files[@]} ))
    fi
    echo "Pass Rate:          $pass_rate%"
    echo ""

    ###############################################################################
    # Status information
    ###############################################################################

    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}Test Phase Status${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "Phase: TDD Red (Test-First)"
    echo "Status: EXPECTED TO FAIL (session-miner subagent not implemented)"
    echo ""
    echo "These tests are designed to:"
    echo "  1. Fail initially (no implementation exists)"
    echo "  2. Drive implementation of session-miner subagent"
    echo "  3. Validate acceptance criteria when implementation complete"
    echo ""

    ###############################################################################
    # Next Steps
    ###############################################################################

    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}Next Steps (TDD Workflow)${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "1. CREATE: .claude/agents/session-miner.md"
    echo "   - Implement JSON lines parsing with error tolerance"
    echo "   - Support streaming with offset/limit parameters"
    echo "   - Return normalized output structure"
    echo ""
    echo "2. GREEN Phase: Run tests again"
    echo "   bash run-all-tests.sh"
    echo ""
    echo "3. REFACTOR: Optimize implementation"
    echo "   - Improve error handling"
    echo "   - Enhance performance"
    echo "   - Update documentation"
    echo ""
    echo "Reference Files:"
    echo "  - Test Requirements: devforgeai/specs/Stories/STORY-221-history-jsonl-parser.story.md"
    echo "  - Epic Overview: devforgeai/specs/Epics/EPIC-034-session-data-mining.epic.md"
    echo ""

    ###############################################################################
    # Exit with status
    ###############################################################################

    if [ $failed -eq 0 ]; then
        echo -e "${GREEN}All test suites passed!${NC}"
        exit 0
    else
        echo -e "${RED}Some test suites failed (expected in RED phase).${NC}"
        exit 1
    fi
}

main "$@"
