#!/bin/bash
# Master Test Runner for STORY-186
# Auto-Regenerate Subagent Registry in Pre-Commit Hook
#
# Tests verify that pre-commit hook automatically regenerates
# the subagent registry without user intervention.

set -e

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ANSI colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test tracking
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Test results
declare -A TEST_RESULTS

echo "========================================"
echo "STORY-186 Test Suite"
echo "Auto-Regenerate Subagent Registry"
echo "========================================"
echo ""

# Run test suite
run_test_suite() {
    local suite_name=$1
    local suite_dir=$2

    echo -e "${BLUE}=== $suite_name ===${NC}"

    if [ ! -d "$suite_dir" ]; then
        echo -e "${YELLOW}  SKIPPED: Directory not found${NC}"
        return
    fi

    for test_file in "$suite_dir"/*.sh; do
        if [ ! -f "$test_file" ]; then
            continue
        fi

        test_name=$(basename "$test_file" .sh)
        TOTAL_TESTS=$((TOTAL_TESTS + 1))

        echo -n "  Running $test_name... "

        # Make executable if not already
        chmod +x "$test_file"

        # Run test
        if "$test_file" > "/tmp/test-output-$$-$test_name.log" 2>&1; then
            echo -e "${GREEN}PASS${NC}"
            PASSED_TESTS=$((PASSED_TESTS + 1))
            TEST_RESULTS["$test_name"]="PASS"
        else
            exit_code=$?
            echo -e "${RED}FAIL (exit $exit_code)${NC}"
            FAILED_TESTS=$((FAILED_TESTS + 1))
            TEST_RESULTS["$test_name"]="FAIL"

            # Show last 20 lines of output
            echo -e "${YELLOW}  Last 20 lines of output:${NC}"
            tail -20 "/tmp/test-output-$$-$test_name.log" | sed 's/^/    /'
        fi
    done

    echo ""
}

# Run all test suites
run_test_suite "Unit Tests" "$TEST_DIR/unit"

# Summary
echo "========================================"
echo "Test Summary"
echo "========================================"
echo "Total:  $TOTAL_TESTS"
echo -e "Passed: ${GREEN}$PASSED_TESTS${NC}"
echo -e "Failed: ${RED}$FAILED_TESTS${NC}"
echo ""

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}ALL TESTS PASSED${NC}"
    echo ""
    echo "Coverage:"
    echo "  - AC1: Pre-commit runs registry script"
    echo "  - AC2: Non-blocking on failure"
    echo "  - AC3: CLAUDE.md auto-staged if changed"
    echo "  - AC4: No user intervention required"
    echo ""
    exit 0
else
    echo -e "${RED}$FAILED_TESTS TEST(S) FAILED${NC}"
    echo ""
    echo "Failed tests:"
    for test_name in "${!TEST_RESULTS[@]}"; do
        if [ "${TEST_RESULTS[$test_name]}" = "FAIL" ]; then
            echo "  - $test_name"
        fi
    done
    echo ""
    exit 1
fi

# Cleanup
rm -f /tmp/test-output-$$-*.log
