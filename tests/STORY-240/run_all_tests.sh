#!/bin/bash

##############################################################################
# Test Runner: STORY-240 Complete Test Suite
# Purpose: Execute all release skill integration tests
# Output: Comprehensive test results with pass/fail summary
##############################################################################

set -o pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Directories
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$TEST_DIR/../../" && pwd)"

# Test files
TESTS=(
    "test_release_skill_integration.sh"
)

# Overall tracking
FAILED_SUITES=()

##############################################################################
# Main Test Execution
##############################################################################

main() {
    cd "$PROJECT_ROOT"

    echo -e "${BLUE}================================================================${NC}"
    echo -e "${BLUE}  STORY-240: Release Skill Build Phase Integration${NC}"
    echo -e "${BLUE}  Complete Test Suite Runner${NC}"
    echo -e "${BLUE}================================================================${NC}"
    echo ""
    echo "Start time: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "Project root: $PROJECT_ROOT"
    echo ""

    # Run each test suite
    local test_num=1
    for test_file in "${TESTS[@]}"; do
        local test_path="$TEST_DIR/$test_file"

        if [ ! -f "$test_path" ]; then
            echo -e "${RED}ERROR: Test file not found: $test_file${NC}"
            FAILED_SUITES+=("$test_file (NOT FOUND)")
            continue
        fi

        echo -e "${YELLOW}--------------------------------------------------------------${NC}"
        echo -e "${BLUE}[Suite $test_num/${#TESTS[@]}]${NC} Running: ${YELLOW}$test_file${NC}"
        echo -e "${YELLOW}--------------------------------------------------------------${NC}"
        echo ""

        # Make executable and run
        chmod +x "$test_path"
        if "$test_path"; then
            echo ""
            echo -e "${GREEN}SUITE PASSED${NC}"
        else
            echo ""
            echo -e "${RED}SUITE FAILED${NC}"
            FAILED_SUITES+=("$test_file")
        fi

        echo ""
        test_num=$((test_num + 1))
    done

    # Summary
    echo -e "${BLUE}================================================================${NC}"
    echo -e "${BLUE}  TEST SUITE EXECUTION SUMMARY${NC}"
    echo -e "${BLUE}================================================================${NC}"
    echo ""

    local passed=0
    local failed=0
    for test_file in "${TESTS[@]}"; do
        local found=false
        for failed_suite in "${FAILED_SUITES[@]}"; do
            if [[ "$failed_suite" == "$test_file"* ]]; then
                echo -e "${RED}x${NC} $test_file"
                failed=$((failed + 1))
                found=true
                break
            fi
        done
        if [ "$found" = false ]; then
            echo -e "${GREEN}o${NC} $test_file"
            passed=$((passed + 1))
        fi
    done

    echo ""
    echo -e "Total test suites: ${BLUE}${#TESTS[@]}${NC}"
    echo -e "Suites passed:     ${GREEN}$passed${NC}"
    echo -e "Suites failed:     ${RED}$failed${NC}"
    echo ""

    if [ "$failed" -eq 0 ]; then
        echo -e "${GREEN}================================================================${NC}"
        echo -e "${GREEN}ALL TEST SUITES PASSED${NC}"
        echo -e "${GREEN}================================================================${NC}"
        echo "End time: $(date '+%Y-%m-%d %H:%M:%S')"
        exit 0
    else
        echo -e "${RED}================================================================${NC}"
        echo -e "${RED}SOME TEST SUITES FAILED (TDD RED state expected)${NC}"
        echo -e "${RED}================================================================${NC}"
        echo ""
        echo "Failed suites:"
        for failed_suite in "${FAILED_SUITES[@]}"; do
            echo -e "  ${RED}*${NC} $failed_suite"
        done
        echo ""
        echo "End time: $(date '+%Y-%m-%d %H:%M:%S')"
        exit 1
    fi
}

# Run main
main "$@"
