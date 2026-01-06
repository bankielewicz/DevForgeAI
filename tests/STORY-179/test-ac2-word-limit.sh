#!/bin/bash

##############################################################################
# Test Suite: STORY-179 AC#2 - Maximum Word Limit Specified
#
# AC#2: Maximum Word Limit Specified
#   Given: Response Constraints section in phase files
#   When: reading the constraint content
#   Then: 500 words maximum limit MUST be specified
#
# Test Strategy:
#   - Verify "500 words" appears in each phase file
#   - Verify limit instruction is present ("Limit response to")
#   - Verify "maximum" is specified with word count
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
# AC#2 Test Cases - 500 Word Maximum Limit
##############################################################################

echo ""
echo "============================================================================"
echo " STORY-179 AC#2: Maximum Word Limit Specified (500 words)"
echo "============================================================================"
echo ""

# Test 2.1: Verify phase-02 contains 500 words limit
run_test \
    "test_ac2_phase02_word_limit" \
    "Verify phase-02-test-first.md contains '500 words' constraint"
assert_file_exists "$PHASE_02"
assert_grep_match "500 words" "$PHASE_02" "Phase 02 word limit"

# Test 2.2: Verify phase-03 contains 500 words limit
run_test \
    "test_ac2_phase03_word_limit" \
    "Verify phase-03-implementation.md contains '500 words' constraint"
assert_file_exists "$PHASE_03"
assert_grep_match "500 words" "$PHASE_03" "Phase 03 word limit"

# Test 2.3: Verify phase-04 contains 500 words limit
run_test \
    "test_ac2_phase04_word_limit" \
    "Verify phase-04-refactoring.md contains '500 words' constraint"
assert_file_exists "$PHASE_04"
assert_grep_match "500 words" "$PHASE_04" "Phase 04 word limit"

# Test 2.4: Verify phase-05 contains 500 words limit
run_test \
    "test_ac2_phase05_word_limit" \
    "Verify phase-05-integration.md contains '500 words' constraint"
assert_file_exists "$PHASE_05"
assert_grep_match "500 words" "$PHASE_05" "Phase 05 word limit"

# Test 2.5: Verify "maximum" keyword is present with word limit
run_test \
    "test_ac2_maximum_keyword_present" \
    "Verify 'maximum' keyword appears with word limit instruction"
count=0
for file in "$PHASE_02" "$PHASE_03" "$PHASE_04" "$PHASE_05"; do
    if grep -qi "maximum" "$file" 2>/dev/null && grep -qi "500 words" "$file" 2>/dev/null; then
        count=$((count + 1))
    fi
done

if [[ $count -eq 4 ]]; then
    echo -e "${GREEN}PASSED${NC}: All 4 phase files contain 'maximum' with '500 words'"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAILED${NC}: Only $count/4 phase files contain 'maximum' with '500 words'"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 2.6: Verify "Limit response to" instruction format
run_test \
    "test_ac2_limit_response_instruction" \
    "Verify 'Limit response to' instruction appears in phase files"
count=0
for file in "$PHASE_02" "$PHASE_03" "$PHASE_04" "$PHASE_05"; do
    if grep -qi "Limit response to" "$file" 2>/dev/null; then
        count=$((count + 1))
    fi
done

if [[ $count -ge 1 ]]; then
    echo -e "${GREEN}PASSED${NC}: 'Limit response to' instruction found in $count file(s)"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAILED${NC}: 'Limit response to' instruction NOT found in any phase file"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

##############################################################################
# Summary Report
##############################################################################

echo ""
echo "============================================================================"
echo "Test Summary Report - AC#2: Maximum Word Limit (500 words)"
echo "============================================================================"
echo "Total Tests Run:    $TESTS_RUN"
echo -e "Tests Passed:       ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed:       ${RED}$TESTS_FAILED${NC}"
echo "============================================================================"

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}SUCCESS: All AC#2 tests passed${NC}"
    exit 0
else
    echo -e "${RED}FAILURE: AC#2 test failures detected - 500 word limit not specified${NC}"
    exit 1
fi
