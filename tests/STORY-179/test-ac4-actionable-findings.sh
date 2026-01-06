#!/bin/bash

##############################################################################
# Test Suite: STORY-179 AC#4 - Actionable Findings Only
#
# AC#4: Actionable Findings Only
#   Given: Response Constraints section in phase files
#   When: reading the constraint content
#   Then: "Only include actionable findings" instruction MUST be present
#
# Test Strategy:
#   - Verify "actionable" keyword appears in phase files
#   - Verify "Only include actionable" instruction exists
#   - Verify instruction appears in all 4 phase files
##############################################################################

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# File paths
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
PHASE_02="${PROJECT_ROOT}/.claude/skills/devforgeai-development/phases/phase-02-test-first.md"
PHASE_03="${PROJECT_ROOT}/.claude/skills/devforgeai-development/phases/phase-03-implementation.md"
PHASE_04="${PROJECT_ROOT}/.claude/skills/devforgeai-development/phases/phase-04-refactoring.md"
PHASE_05="${PROJECT_ROOT}/.claude/skills/devforgeai-development/phases/phase-05-integration.md"

##############################################################################
# Helper Functions
##############################################################################

run_test() {
    local test_name="$1"
    local test_description="$2"

    TESTS_RUN=$((TESTS_RUN + 1))

    echo ""
    echo -e "${YELLOW}Test $TESTS_RUN: $test_name${NC}"
    echo "Description: $test_description"
    echo "---"
}

assert_grep_match() {
    local pattern="$1"
    local file="$2"
    local test_name="$3"

    if grep -qi "$pattern" "$file" 2>/dev/null; then
        echo -e "${GREEN}PASSED${NC}: Pattern '$pattern' found in $(basename $file)"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}FAILED${NC}: Pattern '$pattern' NOT found in $(basename $file)"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

assert_file_exists() {
    local file="$1"

    if [[ ! -f "$file" ]]; then
        echo -e "${RED}FAILED${NC}: File $file does not exist"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    else
        echo -e "${GREEN}PASSED${NC}: File $(basename $file) exists"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    fi
}

##############################################################################
# AC#4 Test Cases - Actionable Findings Only
##############################################################################

echo ""
echo "============================================================================"
echo " STORY-179 AC#4: Actionable Findings Only"
echo "============================================================================"
echo ""

# Test 4.1: Verify phase-02 contains actionable instruction
run_test \
    "test_ac4_phase02_actionable" \
    "Verify phase-02-test-first.md contains 'actionable' instruction"
assert_file_exists "$PHASE_02"
assert_grep_match "actionable" "$PHASE_02" "Phase 02 actionable"

# Test 4.2: Verify phase-03 contains actionable instruction
run_test \
    "test_ac4_phase03_actionable" \
    "Verify phase-03-implementation.md contains 'actionable' instruction"
assert_file_exists "$PHASE_03"
assert_grep_match "actionable" "$PHASE_03" "Phase 03 actionable"

# Test 4.3: Verify phase-04 contains actionable instruction
run_test \
    "test_ac4_phase04_actionable" \
    "Verify phase-04-refactoring.md contains 'actionable' instruction"
assert_file_exists "$PHASE_04"
assert_grep_match "actionable" "$PHASE_04" "Phase 04 actionable"

# Test 4.4: Verify phase-05 contains actionable instruction
run_test \
    "test_ac4_phase05_actionable" \
    "Verify phase-05-integration.md contains 'actionable' instruction"
assert_file_exists "$PHASE_05"
assert_grep_match "actionable" "$PHASE_05" "Phase 05 actionable"

# Test 4.5: Verify "Only include actionable findings" exact instruction
run_test \
    "test_ac4_only_include_actionable_findings" \
    "Verify 'Only include actionable findings' instruction exists"
count=0
for file in "$PHASE_02" "$PHASE_03" "$PHASE_04" "$PHASE_05"; do
    if grep -qi "Only include actionable" "$file" 2>/dev/null; then
        count=$((count + 1))
    fi
done

if [[ $count -ge 1 ]]; then
    echo -e "${GREEN}PASSED${NC}: 'Only include actionable' instruction found in $count file(s)"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAILED${NC}: 'Only include actionable' instruction NOT found in any phase file"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 4.6: Verify "findings" keyword appears with actionable
run_test \
    "test_ac4_actionable_findings_phrase" \
    "Verify 'actionable findings' phrase appears in phase files"
count=0
for file in "$PHASE_02" "$PHASE_03" "$PHASE_04" "$PHASE_05"; do
    if grep -qi "actionable findings" "$file" 2>/dev/null; then
        count=$((count + 1))
    fi
done

if [[ $count -ge 1 ]]; then
    echo -e "${GREEN}PASSED${NC}: 'actionable findings' phrase found in $count file(s)"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAILED${NC}: 'actionable findings' phrase NOT found in any phase file"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

##############################################################################
# Summary Report
##############################################################################

echo ""
echo "============================================================================"
echo "Test Summary Report - AC#4: Actionable Findings Only"
echo "============================================================================"
echo "Total Tests Run:    $TESTS_RUN"
echo -e "Tests Passed:       ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed:       ${RED}$TESTS_FAILED${NC}"
echo "============================================================================"

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}SUCCESS: All AC#4 tests passed${NC}"
    exit 0
else
    echo -e "${RED}FAILURE: AC#4 test failures detected - Actionable findings instruction missing${NC}"
    exit 1
fi
