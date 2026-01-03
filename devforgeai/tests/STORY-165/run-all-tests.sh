#!/bin/bash

################################################################################
# STORY-165 Test Suite Runner
#
# Purpose: Execute all acceptance criteria tests for STORY-165
# RCA-012: Remove Checkbox Syntax from AC Headers
#
# Test Pyramid Distribution:
#   - Unit Tests (verification tests): 4 tests
#   - Coverage: Template format, story generation, backward compatibility, referencability
#
# Execution:
#   bash devforgeai/tests/STORY-165/run-all-tests.sh
#
# Expected Behavior (TDD Red Phase):
#   - ALL TESTS SHOULD FAIL initially (no implementation exists)
#   - After implementation, all tests should PASS
#
################################################################################

set -e

# Test configuration
TESTS_DIR="devforgeai/tests/STORY-165"
TEST_COUNT=0
PASSED=0
FAILED=0
SKIPPED=0

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Header
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         STORY-165 Test Suite: RCA-012 Checkbox Removal        ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Verify test directory exists
if [ ! -d "$TESTS_DIR" ]; then
    echo -e "${RED}ERROR${NC}: Test directory not found: $TESTS_DIR"
    exit 1
fi

# Find and execute all test scripts
echo -e "${BLUE}Running Tests:${NC}"
echo ""

for test_script in "$TESTS_DIR"/test-*.sh; do
    if [ -f "$test_script" ]; then
        TEST_COUNT=$((TEST_COUNT + 1))
        test_name=$(basename "$test_script" .sh)

        echo -n "  [$TEST_COUNT] $test_name ... "

        # Run test and capture exit code
        if bash "$test_script" > /tmp/test_output_$$.log 2>&1; then
            echo -e "${GREEN}PASS${NC}"
            PASSED=$((PASSED + 1))
        else
            echo -e "${RED}FAIL${NC}"
            FAILED=$((FAILED + 1))

            # Show error output
            if [ -f "/tmp/test_output_$$.log" ]; then
                echo ""
                echo "    Error output:"
                sed 's/^/    /' "/tmp/test_output_$$.log"
                echo ""
            fi
        fi

        # Cleanup
        rm -f "/tmp/test_output_$$.log"
    fi
done

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                       Test Results                             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "  Total Tests:  $TEST_COUNT"
echo -e "  ${GREEN}Passed:${NC}      $PASSED"
echo -e "  ${RED}Failed:${NC}      $FAILED"
echo ""

# Summary
if [ "$FAILED" -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    echo ""
    exit 0
else
    echo -e "${RED}✗ $FAILED test(s) failed${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Review failing test output above"
    echo "  2. Implement AC#1: Update template to use ### AC#N: format"
    echo "  3. Implement AC#2: Ensure /create-story uses updated template"
    echo "  4. Implement AC#3: Verify old stories are not auto-migrated"
    echo "  5. Implement AC#4: Validate numbering referencability"
    echo "  6. Re-run: bash devforgeai/tests/STORY-165/run-all-tests.sh"
    echo ""
    exit 1
fi
