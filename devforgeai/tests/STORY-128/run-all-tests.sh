#!/bin/bash
################################################################################
# Test Runner for STORY-128: Git Lock File Recovery
#
# Runs all acceptance criteria tests and reports pass/fail status
# All tests should FAIL initially (Red phase - docs don't exist yet)
################################################################################

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test directory
TEST_DIR="devforgeai/tests/STORY-128"

echo ""
echo "╔═══════════════════════════════════════════════════════════════════════════╗"
echo "║                    STORY-128: Git Lock File Recovery                      ║"
echo "║                         TDD RED PHASE TEST SUITE                          ║"
echo "║                                                                           ║"
echo "║  Expected: ALL TESTS FAIL (Red phase - documentation doesn't exist yet)  ║"
echo "╚═══════════════════════════════════════════════════════════════════════════╝"
echo ""

# Initialize test counters
total_tests=0
passed_tests=0
failed_tests=0
test_results=()

# Test files
test_files=(
    "test-ac1-section-exists.sh"
    "test-ac2-diagnosis-commands.sh"
    "test-ac3-recovery-warning.sh"
    "test-ac4-wsl2-guidance.sh"
    "test-ac5-prevention-tips.sh"
)

echo "Available Test Files:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
for test_file in "${test_files[@]}"; do
    echo "  ✓ $test_file"
done
echo ""

# Run each test
echo "Running Tests (Red Phase - Expecting Failures):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

for test_file in "${test_files[@]}"; do
    test_path="$TEST_DIR/$test_file"
    test_name="${test_file%.sh}"
    ((total_tests++))

    echo -n "[$total_tests/${#test_files[@]}] Running $test_name... "

    # Make test executable
    chmod +x "$test_path" 2>/dev/null || true

    # Run test and capture exit code
    if bash "$test_path" > /tmp/test_output.txt 2>&1; then
        # Test PASSED (but we expect FAILURES in Red phase)
        echo -e "${GREEN}PASS${NC}"
        ((passed_tests++))
        test_results+=("PASS: $test_name")
    else
        # Test FAILED (expected in Red phase)
        echo -e "${RED}FAIL${NC}"
        ((failed_tests++))
        test_results+=("FAIL: $test_name (as expected in Red phase)")

        # Show first few lines of failure output
        if [ -f /tmp/test_output.txt ]; then
            echo ""
            echo "  Failure Details:"
            head -n 5 /tmp/test_output.txt | sed 's/^/    /'
            echo ""
        fi
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test Results Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Total Tests:    $total_tests"
echo "Passed:         $passed_tests"
echo "Failed:         $failed_tests"
echo ""

# Print individual results
echo "Detailed Results:"
for result in "${test_results[@]}"; do
    if [[ $result == PASS* ]]; then
        echo "  $(echo "$result" | sed "s/PASS:/${GREEN}✓ PASS:${NC}/")"
    else
        echo "  $(echo "$result" | sed "s/FAIL:/${RED}✗ FAIL:${NC}/")"
    fi
done
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# RED PHASE VALIDATION
echo "TDD RED PHASE VALIDATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ "$failed_tests" -eq "$total_tests" ]; then
    echo -e "${GREEN}✓ ALL TESTS FAILED (Red phase successful)${NC}"
    echo ""
    echo "Test Suite Status:  ${GREEN}RED PHASE COMPLETE${NC}"
    echo "Documentation:      ${YELLOW}Not yet implemented${NC}"
    echo "Next Phase:         ${BLUE}Green Phase - Implement documentation${NC}"
    echo ""
    exit 0
elif [ "$passed_tests" -eq "$total_tests" ]; then
    echo -e "${GREEN}✓ ALL TESTS PASSED (Green phase complete)${NC}"
    echo ""
    echo "Test Suite Status:  ${GREEN}GREEN PHASE COMPLETE${NC}"
    echo "Documentation:      ${GREEN}Fully implemented${NC}"
    echo "Next Phase:         ${BLUE}Refactoring/QA${NC}"
    echo ""
    exit 0
else
    echo -e "${YELLOW}⚠ MIXED RESULTS (Some tests passing, some failing)${NC}"
    echo ""
    echo "Test Suite Status:  ${YELLOW}PARTIAL IMPLEMENTATION${NC}"
    echo "Documentation:      ${YELLOW}Partially implemented${NC}"
    echo "Missing AC Items:   $(echo $failed_tests)"
    echo ""
    exit 1
fi
