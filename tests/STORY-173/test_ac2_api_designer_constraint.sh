#!/bin/bash

##############################################################################
# Test Suite: STORY-173 AC#2 - API Designer Plan File Constraint
#
# AC#2: API Designer Plan File Constraint
#   Given: the `api-designer.md` subagent file
#   When: I review its Constraints section
#   Then: it MUST contain: "Do NOT create files in .claude/plans/ directory"
#
# Test Strategy:
#   - Verify api-designer.md file exists
#   - Verify Constraints section exists
#   - Verify constraint text is present
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

# Test file path
API_DESIGNER="/mnt/c/Projects/DevForgeAI2/.claude/agents/api-designer.md"

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

assert_file_exists() {
    local file="$1"

    if [[ ! -f "$file" ]]; then
        echo -e "${RED}FAILED${NC}: File $file does not exist"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    else
        echo -e "${GREEN}PASSED${NC}: File $file exists"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    fi
}

assert_grep_match() {
    local pattern="$1"
    local file="$2"
    local test_name="$3"

    if grep -q "$pattern" "$file" 2>/dev/null; then
        echo -e "${GREEN}PASSED${NC}: Pattern '$pattern' found in $file"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}FAILED${NC}: Pattern '$pattern' NOT found in $file"
        echo "Expected: The file should contain the constraint text"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

assert_section_exists() {
    local section_pattern="$1"
    local file="$2"
    local section_name="$3"

    if grep -qi "$section_pattern" "$file" 2>/dev/null; then
        echo -e "${GREEN}PASSED${NC}: Section '$section_name' exists in $file"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}FAILED${NC}: Section '$section_name' NOT found in $file"
        echo "Expected: A section matching pattern '$section_pattern' should exist"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

##############################################################################
# AC#2 Test Cases
##############################################################################

echo ""
echo "========================================================================"
echo " STORY-173 AC#2: API Designer Plan File Constraint"
echo "========================================================================"
echo ""

# Test 2.1: Verify api-designer.md exists
run_test \
    "test_api_designer_file_exists" \
    "Verify api-designer.md subagent file exists"
assert_file_exists "$API_DESIGNER"

# Test 2.2: Verify Constraints section exists
run_test \
    "test_constraints_section_exists" \
    "Verify Constraints section exists in api-designer.md"
assert_section_exists "^## Constraints\|^### Constraints" "$API_DESIGNER" "Constraints"

# Test 2.3: Verify plan file constraint is present (exact text)
run_test \
    "test_plan_file_constraint_exact" \
    "Verify exact constraint text 'Do NOT create files in .claude/plans/ directory' exists"
assert_grep_match "Do NOT create files in \`\?\.claude/plans/\`\? directory" "$API_DESIGNER" "Plan file constraint"

# Test 2.4: Verify constraint is within Constraints section (contextual check)
run_test \
    "test_constraint_in_correct_section" \
    "Verify plan file constraint appears after Constraints heading"
# This test extracts content after Constraints section and checks for constraint
if grep -A 50 -i "^## Constraints\|^### Constraints" "$API_DESIGNER" 2>/dev/null | grep -qE "Do NOT create files in \`?\.claude/plans/\`? directory"; then
    echo -e "${GREEN}PASSED${NC}: Constraint text found in Constraints section"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAILED${NC}: Constraint text NOT found in Constraints section"
    echo "Expected: 'Do NOT create files in .claude/plans/ directory' within Constraints section"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

##############################################################################
# Summary Report
##############################################################################

echo ""
echo "========================================================================"
echo "Test Summary Report - AC#2"
echo "========================================================================"
echo "Total Tests Run:    $TESTS_RUN"
echo -e "Tests Passed:       ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed:       ${RED}$TESTS_FAILED${NC}"
echo "========================================================================"

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}SUCCESS: All AC#2 tests passed${NC}"
    exit 0
else
    echo -e "${RED}FAILURE: AC#2 tests failed - Implementation required${NC}"
    exit 1
fi
