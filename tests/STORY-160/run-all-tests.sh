#!/bin/bash
##############################################################################
# STORY-160 Comprehensive Test Suite Runner
#
# Runs all acceptance criteria verification tests for STORY-160:
# RCA-008 Skill Documentation Update
#
# This script validates that all documentation files accurately reflect
# the RCA-008 git safety enhancements.
##############################################################################

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEST_DIR="${PROJECT_ROOT}/tests/STORY-160"

# Results tracking
total_tests=0
passed_tests=0
failed_tests=0
failed_acs=()

##############################################################################
# Banner
##############################################################################
echo ""
echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  STORY-160: RCA-008 Skill Documentation Update${NC}"
echo -e "${BLUE}  Comprehensive Test Suite${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

##############################################################################
# Function to run a test script
##############################################################################
run_test() {
    local test_name="$1"
    local test_script="$2"

    echo -e "${YELLOW}Running: ${test_name}${NC}"
    echo "─────────────────────────────────────────────────"

    if [ -f "${test_script}" ]; then
        chmod +x "${test_script}"
        if bash "${test_script}"; then
            echo -e "${GREEN}✓ ${test_name} PASSED${NC}"
            echo ""
            return 0
        else
            echo -e "${RED}✗ ${test_name} FAILED${NC}"
            echo ""
            return 1
        fi
    else
        echo -e "${RED}✗ Test script not found: ${test_script}${NC}"
        echo ""
        return 1
    fi
}

##############################################################################
# Test AC-1: SKILL.md Overview Updated (10 validation steps)
##############################################################################
echo -e "${BLUE}[AC-1]${NC} Testing SKILL.md Overview (10 validation steps)"
if run_test "AC-1: SKILL.md Overview Updated" "${TEST_DIR}/test-ac1-skill-md-validation-steps.sh"; then
    ((passed_tests++))
else
    ((failed_tests++))
    failed_acs+=("AC-1")
fi
((total_tests++))

##############################################################################
# Test AC-2: Reference Files Documented
##############################################################################
echo -e "${BLUE}[AC-2]${NC} Testing Reference Files Documentation"
if run_test "AC-2: Reference Files Documented" "${TEST_DIR}/test-ac2-reference-files-documented.sh"; then
    ((passed_tests++))
else
    ((failed_tests++))
    failed_acs+=("AC-2")
fi
((total_tests++))

##############################################################################
# Test AC-3: Subagent Coordination Updated
##############################################################################
echo -e "${BLUE}[AC-3]${NC} Testing Subagent Coordination Updates"
if run_test "AC-3: Subagent Coordination Updated" "${TEST_DIR}/test-ac3-subagent-coordination-updated.sh"; then
    ((passed_tests++))
else
    ((failed_tests++))
    failed_acs+=("AC-3")
fi
((total_tests++))

##############################################################################
# Test AC-4: Change Log Entry
##############################################################################
echo -e "${BLUE}[AC-4]${NC} Testing Change Log Entry"
if run_test "AC-4: Change Log Entry" "${TEST_DIR}/test-ac4-changelog-entry.sh"; then
    ((passed_tests++))
else
    ((failed_tests++))
    failed_acs+=("AC-4")
fi
((total_tests++))

##############################################################################
# Test AC-5: Skills Reference Memory File
##############################################################################
echo -e "${BLUE}[AC-5]${NC} Testing Skills Reference Memory File"
if run_test "AC-5: Skills Reference Memory File" "${TEST_DIR}/test-ac5-skills-reference-memory-file.sh"; then
    ((passed_tests++))
else
    ((failed_tests++))
    failed_acs+=("AC-5")
fi
((total_tests++))

##############################################################################
# Summary Report
##############################################################################
echo ""
echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  TEST SUITE SUMMARY${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""
echo "Total Test Groups:    ${total_tests}"
echo -e "Passed:              ${GREEN}${passed_tests}${NC}"
echo -e "Failed:              ${RED}${failed_tests}${NC}"
echo ""

if [ ${failed_tests} -eq 0 ]; then
    echo -e "${GREEN}════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✓ ALL ACCEPTANCE CRITERIA VERIFIED${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════${NC}"
    echo ""
    echo "STORY-160 Verification Status: PASSED"
    echo "All documentation files accurately reflect RCA-008 git safety enhancements."
    echo ""
    exit 0
else
    echo -e "${RED}════════════════════════════════════════════════${NC}"
    echo -e "${RED}✗ SOME TESTS FAILED${NC}"
    echo -e "${RED}════════════════════════════════════════════════${NC}"
    echo ""
    echo "Failed Acceptance Criteria:"
    for ac in "${failed_acs[@]}"; do
        echo "  - ${ac}"
    done
    echo ""
    exit 1
fi
