#!/bin/bash

##############################################################################
# Test Suite: STORY-179 AC#3 - Bullet Point Format Mandated
#
# AC#3: Bullet Point Format Mandated
#   Given: Response Constraints section in phase files
#   When: reading the constraint content
#   Then: "Use bullet points, not paragraphs" instruction MUST be present
#
# Test Strategy:
#   - Verify exact or equivalent bullet point instruction exists
#   - Verify instruction appears in all 4 phase files
#   - Verify "bullet" keyword is present
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
# AC#3 Test Cases - Bullet Point Format Mandated
##############################################################################

echo ""
echo "============================================================================"
echo " STORY-179 AC#3: Bullet Point Format Mandated"
echo "============================================================================"
echo ""

# Test 3.1: Verify phase-02 contains bullet point instruction
run_test \
    "test_ac3_phase02_bullet_points" \
    "Verify phase-02-test-first.md contains bullet point instruction"
assert_file_exists "$PHASE_02"
assert_grep_match "bullet point" "$PHASE_02" "Phase 02 bullet points"

# Test 3.2: Verify phase-03 contains bullet point instruction
run_test \
    "test_ac3_phase03_bullet_points" \
    "Verify phase-03-implementation.md contains bullet point instruction"
assert_file_exists "$PHASE_03"
assert_grep_match "bullet point" "$PHASE_03" "Phase 03 bullet points"

# Test 3.3: Verify phase-04 contains bullet point instruction
run_test \
    "test_ac3_phase04_bullet_points" \
    "Verify phase-04-refactoring.md contains bullet point instruction"
assert_file_exists "$PHASE_04"
assert_grep_match "bullet point" "$PHASE_04" "Phase 04 bullet points"

# Test 3.4: Verify phase-05 contains bullet point instruction
run_test \
    "test_ac3_phase05_bullet_points" \
    "Verify phase-05-integration.md contains bullet point instruction"
assert_file_exists "$PHASE_05"
assert_grep_match "bullet point" "$PHASE_05" "Phase 05 bullet points"

# Test 3.5: Verify "not paragraphs" instruction is present
run_test \
    "test_ac3_not_paragraphs_instruction" \
    "Verify 'not paragraphs' instruction appears in phase files"
count=0
for file in "$PHASE_02" "$PHASE_03" "$PHASE_04" "$PHASE_05"; do
    if grep -qi "not paragraphs" "$file" 2>/dev/null; then
        count=$((count + 1))
    fi
done

if [[ $count -ge 1 ]]; then
    echo -e "${GREEN}PASSED${NC}: 'not paragraphs' instruction found in $count file(s)"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAILED${NC}: 'not paragraphs' instruction NOT found in any phase file"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 3.6: Verify exact phrase "Use bullet points, not paragraphs"
run_test \
    "test_ac3_exact_bullet_instruction" \
    "Verify exact 'Use bullet points, not paragraphs' instruction exists"
count=0
for file in "$PHASE_02" "$PHASE_03" "$PHASE_04" "$PHASE_05"; do
    if grep -qi "Use bullet points.*not paragraphs" "$file" 2>/dev/null; then
        count=$((count + 1))
    fi
done

if [[ $count -ge 1 ]]; then
    echo -e "${GREEN}PASSED${NC}: Exact bullet point instruction found in $count file(s)"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAILED${NC}: Exact bullet point instruction NOT found in any phase file"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

##############################################################################
# Summary Report
##############################################################################

echo ""
echo "============================================================================"
echo "Test Summary Report - AC#3: Bullet Point Format Mandated"
echo "============================================================================"
echo "Total Tests Run:    $TESTS_RUN"
echo -e "Tests Passed:       ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed:       ${RED}$TESTS_FAILED${NC}"
echo "============================================================================"

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}SUCCESS: All AC#3 tests passed${NC}"
    exit 0
else
    echo -e "${RED}FAILURE: AC#3 test failures detected - Bullet point format not mandated${NC}"
    exit 1
fi
