#!/bin/bash

##############################################################################
# STORY-179 Test Runner - Execute All Acceptance Criteria Tests
#
# This script runs all AC tests for STORY-179: Add Response Length Constraints
# to Subagent Prompts
#
# Usage: ./run-all-tests.sh
##############################################################################

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test result counters
TOTAL_SUITES=0
SUITES_PASSED=0
SUITES_FAILED=0

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "============================================================================"
echo -e "${BLUE}STORY-179: Add Response Length Constraints to Subagent Prompts${NC}"
echo "============================================================================"
echo ""
echo "Target Files:"
echo "  - .claude/skills/devforgeai-development/phases/phase-02-test-first.md"
echo "  - .claude/skills/devforgeai-development/phases/phase-03-implementation.md"
echo "  - .claude/skills/devforgeai-development/phases/phase-04-refactoring.md"
echo "  - .claude/skills/devforgeai-development/phases/phase-05-integration.md"
echo ""
echo "Expected Constraint Template:"
echo "  **Response Constraints:**"
echo "  - Limit response to 500 words maximum"
echo "  - Use bullet points, not paragraphs"
echo "  - Only include actionable findings"
echo "  - No code snippets unless essential"
echo ""
echo "============================================================================"

run_test_suite() {
    local test_file="$1"
    local test_name="$2"

    TOTAL_SUITES=$((TOTAL_SUITES + 1))

    echo ""
    echo -e "${YELLOW}Running: $test_name${NC}"
    echo "File: $test_file"
    echo "---"

    if bash "$test_file"; then
        echo -e "${GREEN}Suite PASSED: $test_name${NC}"
        SUITES_PASSED=$((SUITES_PASSED + 1))
        return 0
    else
        echo -e "${RED}Suite FAILED: $test_name${NC}"
        SUITES_FAILED=$((SUITES_FAILED + 1))
        return 1
    fi
}

# Run all test suites
echo ""
echo "Starting test execution..."
echo ""

run_test_suite "${SCRIPT_DIR}/test-ac1-response-constraints-section.sh" \
    "AC#1: All Subagent Prompts Include Response Constraints" || true

run_test_suite "${SCRIPT_DIR}/test-ac2-word-limit.sh" \
    "AC#2: Maximum Word Limit Specified (500 words)" || true

run_test_suite "${SCRIPT_DIR}/test-ac3-bullet-point-format.sh" \
    "AC#3: Bullet Point Format Mandated" || true

run_test_suite "${SCRIPT_DIR}/test-ac4-actionable-findings.sh" \
    "AC#4: Actionable Findings Only" || true

run_test_suite "${SCRIPT_DIR}/test-ac5-complete-constraint-template.sh" \
    "AC#5: Complete Constraint Template" || true

##############################################################################
# Final Summary Report
##############################################################################

echo ""
echo "============================================================================"
echo -e "${BLUE}STORY-179 Final Test Summary${NC}"
echo "============================================================================"
echo ""
echo "Total Test Suites:     $TOTAL_SUITES"
echo -e "Suites Passed:         ${GREEN}$SUITES_PASSED${NC}"
echo -e "Suites Failed:         ${RED}$SUITES_FAILED${NC}"
echo ""
echo "============================================================================"

if [[ $SUITES_FAILED -eq 0 ]]; then
    echo -e "${GREEN}SUCCESS: All STORY-179 acceptance criteria tests passed!${NC}"
    echo ""
    echo "Response Constraints have been properly added to all subagent prompts."
    exit 0
else
    echo -e "${RED}FAILURE: $SUITES_FAILED/$TOTAL_SUITES test suites failed${NC}"
    echo ""
    echo "TDD Red Phase: Tests are failing as expected."
    echo "Implementation needed to add Response Constraints section to phase files."
    echo ""
    echo "Next Step: Implement the Response Constraints template in each phase file."
    exit 1
fi
