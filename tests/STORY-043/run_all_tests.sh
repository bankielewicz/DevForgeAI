#!/bin/bash

##############################################################################
# Test Runner: STORY-043 Complete Test Suite
# Purpose: Execute all acceptance criteria tests in sequence
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
    "test-ac1-audit-classification.sh"
    "test-ac2-update-safety.sh"
    "test-ac3-validation.sh"
    "test-ac4-progressive-disclosure.sh"
    "test-ac5-integration.sh"
    "test-ac6-deploy-preservation.sh"
    "test-ac7-script-safety.sh"
)

# Overall tracking
TOTAL_TESTS=0
TOTAL_PASSED=0
TOTAL_FAILED=0
FAILED_SUITES=()

##############################################################################
# Main Test Execution
##############################################################################

main() {
    cd "$PROJECT_ROOT"

    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC}  STORY-043: Update Internal Path References (src/claude/)  ${BLUE}║${NC}"
    echo -e "${BLUE}║${NC}  Complete Test Suite                                       ${BLUE}║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
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
            TOTAL_FAILED=$((TOTAL_FAILED + 1))
            FAILED_SUITES+=("$test_file (NOT FOUND)")
            continue
        fi

        echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${BLUE}[Suite $test_num/7]${NC} Running: ${YELLOW}$test_file${NC}"
        echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo ""

        # Make executable and run
        chmod +x "$test_path"
        if "$test_path"; then
            echo ""
            echo -e "${GREEN}✓ SUITE PASSED${NC}"
        else
            echo ""
            echo -e "${RED}✗ SUITE FAILED${NC}"
            FAILED_SUITES+=("$test_file")
        fi

        echo ""
        test_num=$((test_num + 1))
    done

    # Summary
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC}  TEST SUITE EXECUTION SUMMARY                             ${BLUE}║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""

    local passed=0
    local failed=0
    for test_file in "${TESTS[@]}"; do
        local found=false
        for failed_suite in "${FAILED_SUITES[@]}"; do
            if [[ "$failed_suite" == "$test_file"* ]]; then
                echo -e "${RED}✗${NC} $test_file"
                failed=$((failed + 1))
                found=true
                break
            fi
        done
        if [ "$found" = false ]; then
            echo -e "${GREEN}✓${NC} $test_file"
            passed=$((passed + 1))
        fi
    done

    echo ""
    echo -e "Total test suites: ${BLUE}${#TESTS[@]}${NC}"
    echo -e "Suites passed:     ${GREEN}$passed${NC}"
    echo -e "Suites failed:     ${RED}$failed${NC}"
    echo ""

    if [ "$failed" -eq 0 ]; then
        echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
        echo -e "${GREEN}ALL TEST SUITES PASSED${NC}"
        echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
        echo "End time: $(date '+%Y-%m-%d %H:%M:%S')"
        exit 0
    else
        echo -e "${RED}═══════════════════════════════════════════════════════════${NC}"
        echo -e "${RED}SOME TEST SUITES FAILED${NC}"
        echo -e "${RED}═══════════════════════════════════════════════════════════${NC}"
        echo ""
        echo "Failed suites:"
        for failed_suite in "${FAILED_SUITES[@]}"; do
            echo -e "  ${RED}•${NC} $failed_suite"
        done
        echo ""
        echo "End time: $(date '+%Y-%m-%d %H:%M:%S')"
        exit 1
    fi
}

# Run main
main "$@"
