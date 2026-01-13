#!/bin/bash

##############################################################################
# Master Test Suite: STORY-206 - Update devforgeai-development Skill to Pass
#                    source-tree.md Context to Subagents
#
# Comprehensive test execution for all acceptance criteria:
#   AC#1: source-tree.md Read in Phase 1 (Red - Test First)
#   AC#2: Context Markers Set Before Subagent Invocation
#   AC#3: Context Available to test-automator
#   AC#4: Context Extraction Logic for Common Patterns
#   AC#5: Reference File Updated
#
# This script:
#   1. Runs all individual test suites
#   2. Aggregates results
#   3. Provides comprehensive summary
#   4. Returns appropriate exit code
##############################################################################

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test directory
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"

# Test counters
TOTAL_SUITES=0
PASSED_SUITES=0
FAILED_SUITES=0

##############################################################################
# Helper Functions
##############################################################################

run_test_suite() {
    local test_file="$1"
    local suite_name=$(basename "$test_file" .sh)

    TOTAL_SUITES=$((TOTAL_SUITES + 1))

    echo ""
    echo "============================================================================"
    echo " Running: $suite_name"
    echo "============================================================================"
    echo ""

    if [[ ! -f "$test_file" ]]; then
        echo -e "${RED}ERROR${NC}: Test file not found: $test_file"
        FAILED_SUITES=$((FAILED_SUITES + 1))
        return 1
    fi

    # Make executable
    chmod +x "$test_file"

    # Run test and capture output
    if bash "$test_file"; then
        echo ""
        echo -e "${GREEN}[PASS] $suite_name PASSED${NC}"
        PASSED_SUITES=$((PASSED_SUITES + 1))
        return 0
    else
        echo ""
        echo -e "${RED}[FAIL] $suite_name FAILED${NC}"
        FAILED_SUITES=$((FAILED_SUITES + 1))
        return 1
    fi
}

##############################################################################
# Main Execution
##############################################################################

echo ""
echo "============================================================================"
echo "  STORY-206: Update devforgeai-development Skill to Pass"
echo "             source-tree.md Context to Subagents"
echo "============================================================================"
echo ""
echo "  TDD Phase: RED (Tests written BEFORE implementation)"
echo ""
echo "============================================================================"
echo ""

# Verify test directory exists
if [[ ! -d "$TEST_DIR" ]]; then
    echo -e "${RED}ERROR${NC}: Test directory not found: $TEST_DIR"
    exit 1
fi

echo "Test directory: $TEST_DIR"
echo "Project root: $PROJECT_ROOT"
echo ""

# Run all test suites in order
echo -e "${BLUE}Executing test suites...${NC}"
echo ""

# Main Test Suite: Source Tree Context Tests (covers all ACs)
run_test_suite "$TEST_DIR/test-source-tree-context.sh" || true

##############################################################################
# Summary Report
##############################################################################

echo ""
echo "============================================================================"
echo "  Comprehensive Test Results Summary"
echo "============================================================================"
echo ""

echo "Test Suites:"
echo "  Total:    $TOTAL_SUITES"
echo -e "  Passed:   ${GREEN}$PASSED_SUITES${NC}"
echo -e "  Failed:   ${RED}$FAILED_SUITES${NC}"
echo ""

if [[ $FAILED_SUITES -eq 0 ]]; then
    echo -e "${GREEN}============================================================================"
    echo "  ALL TEST SUITES PASSED"
    echo "============================================================================${NC}"
    echo ""
    echo "STORY-206 Implementation Status: COMPLETE"
    echo ""
    echo "Acceptance Criteria Summary:"
    echo "  [x] AC#1: source-tree.md read in Phase 1/2"
    echo "  [x] AC#2: Context markers set before subagent"
    echo "  [x] AC#3: Context available to test-automator"
    echo "  [x] AC#4: Pattern matching logic documented"
    echo "  [x] AC#5: Reference file updated"
    echo ""
    echo "Next Steps:"
    echo "  1. Mark AC Verification Checklist items as complete"
    echo "  2. Update Definition of Done checkboxes"
    echo "  3. Run /qa STORY-206 for quality validation"
    echo "  4. Commit changes to git"
    exit 0
else
    echo -e "${RED}============================================================================"
    echo "  SOME TEST SUITES FAILED - TDD RED PHASE"
    echo "============================================================================${NC}"
    echo ""
    echo "TDD Status: RED (tests failing as expected before implementation)"
    echo ""
    echo "Failed Suites: $FAILED_SUITES of $TOTAL_SUITES"
    echo ""
    echo "Implementation Required in:"
    echo "  - .claude/skills/devforgeai-development/SKILL.md"
    echo "  - .claude/skills/devforgeai-development/phases/phase-02-test-first.md"
    echo "  - .claude/skills/devforgeai-development/references/tdd-red-phase.md"
    echo ""
    echo "Review the test output above to identify specific failures."
    echo ""
    echo "Key Implementation Points:"
    echo "  1. Add Read(source-tree.md) in Phase 02 workflow"
    echo "  2. Add context markers template before Task(test-automator)"
    echo "  3. Document test directory pattern matching logic"
    echo "  4. Update tdd-red-phase.md with source-tree context guidance"
    exit 1
fi
