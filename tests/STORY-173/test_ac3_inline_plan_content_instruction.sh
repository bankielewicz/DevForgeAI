#!/bin/bash

##############################################################################
# Test Suite: STORY-173 AC#3 - Inline Plan Content Instruction
#
# AC#3: Inline Plan Content Instruction
#   Given: both subagent files
#   When: I review their output guidance
#   Then: they MUST instruct to return plan content directly in the response
#
# Test Strategy:
#   - Verify both files contain instruction to return plan content inline
#   - Check for "return plan content directly" or similar phrasing
#   - Verify instruction is in output/response guidance section
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

# Test file paths
BACKEND_ARCHITECT="/mnt/c/Projects/DevForgeAI2/.claude/agents/backend-architect.md"
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
    local description="$3"

    if grep -qi "$pattern" "$file" 2>/dev/null; then
        echo -e "${GREEN}PASSED${NC}: $description"
        echo "  Found pattern: '$pattern'"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}FAILED${NC}: $description"
        echo "  Expected pattern: '$pattern' NOT found in $file"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

##############################################################################
# AC#3 Test Cases
##############################################################################

echo ""
echo "========================================================================"
echo " STORY-173 AC#3: Inline Plan Content Instruction"
echo "========================================================================"
echo ""

# Test 3.1: Verify backend-architect.md exists
run_test \
    "test_backend_architect_file_exists" \
    "Verify backend-architect.md subagent file exists"
assert_file_exists "$BACKEND_ARCHITECT"

# Test 3.2: Verify api-designer.md exists
run_test \
    "test_api_designer_file_exists" \
    "Verify api-designer.md subagent file exists"
assert_file_exists "$API_DESIGNER"

# Test 3.3: Backend architect - check for inline response instruction
run_test \
    "test_backend_architect_inline_response" \
    "Verify backend-architect.md instructs to return plan content directly"
# Pattern matches various phrasings:
# - "return plan content directly in the response"
# - "return plan content inline"
# - "return architectural plan directly"
# - "output plan content in response"
assert_grep_match "return.*plan.*content.*directly\|return.*plan.*inline\|output.*plan.*directly\|plan.*content.*in.*response" \
    "$BACKEND_ARCHITECT" \
    "Backend architect contains inline plan response instruction"

# Test 3.4: API designer - check for inline response instruction
run_test \
    "test_api_designer_inline_response" \
    "Verify api-designer.md instructs to return plan content directly"
assert_grep_match "return.*plan.*content.*directly\|return.*plan.*inline\|output.*plan.*directly\|plan.*content.*in.*response" \
    "$API_DESIGNER" \
    "API designer contains inline plan response instruction"

# Test 3.5: Backend architect - verify instruction is in output/response section
run_test \
    "test_backend_architect_output_section" \
    "Verify instruction exists in output/response guidance section"
# Check for instruction near output-related headings
if grep -A 30 -iE "^## Output|^### Output|^## Response|^### Response|^## Constraints|^### Constraints" "$BACKEND_ARCHITECT" 2>/dev/null | \
   grep -qi "return.*plan.*content.*directly\|return.*plan.*inline\|output.*plan.*directly"; then
    echo -e "${GREEN}PASSED${NC}: Inline instruction found in appropriate section"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAILED${NC}: Inline instruction NOT found in output/response/constraints section"
    echo "Expected: Inline response instruction in Output, Response, or Constraints section"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 3.6: API designer - verify instruction is in output/response section
run_test \
    "test_api_designer_output_section" \
    "Verify instruction exists in output/response guidance section"
if grep -A 30 -iE "^## Output|^### Output|^## Response|^### Response|^## Constraints|^### Constraints" "$API_DESIGNER" 2>/dev/null | \
   grep -qi "return.*plan.*content.*directly\|return.*plan.*inline\|output.*plan.*directly"; then
    echo -e "${GREEN}PASSED${NC}: Inline instruction found in appropriate section"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAILED${NC}: Inline instruction NOT found in output/response/constraints section"
    echo "Expected: Inline response instruction in Output, Response, or Constraints section"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

##############################################################################
# Summary Report
##############################################################################

echo ""
echo "========================================================================"
echo "Test Summary Report - AC#3"
echo "========================================================================"
echo "Total Tests Run:    $TESTS_RUN"
echo -e "Tests Passed:       ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed:       ${RED}$TESTS_FAILED${NC}"
echo "========================================================================"

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}SUCCESS: All AC#3 tests passed${NC}"
    exit 0
else
    echo -e "${RED}FAILURE: AC#3 tests failed - Implementation required${NC}"
    exit 1
fi
