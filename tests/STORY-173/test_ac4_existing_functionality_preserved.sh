#!/bin/bash

##############################################################################
# Test Suite: STORY-173 AC#4 - Existing Functionality Preserved
#
# AC#4: Existing Functionality Preserved
#   Given: both subagent files after modification
#   When: the agents are invoked during development workflow
#   Then: they MUST still produce architectural plans
#        (content unchanged, only delivery method constrained)
#
# Test Strategy:
#   - Verify critical sections still exist (Purpose, Workflow, Success Criteria)
#   - Verify key functionality references remain
#   - Verify plan generation capability documented
#   - Verify no destructive changes to core content
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

assert_section_exists() {
    local section_pattern="$1"
    local file="$2"
    local section_name="$3"

    if grep -qiE "$section_pattern" "$file" 2>/dev/null; then
        echo -e "${GREEN}PASSED${NC}: Section '$section_name' exists in $(basename $file)"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}FAILED${NC}: Section '$section_name' NOT found in $(basename $file)"
        echo "Expected: A section matching pattern '$section_pattern' should exist"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

assert_grep_match() {
    local pattern="$1"
    local file="$2"
    local description="$3"

    if grep -qi "$pattern" "$file" 2>/dev/null; then
        echo -e "${GREEN}PASSED${NC}: $description"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}FAILED${NC}: $description"
        echo "  Expected pattern: '$pattern' NOT found"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

##############################################################################
# AC#4 Test Cases - Backend Architect
##############################################################################

echo ""
echo "========================================================================"
echo " STORY-173 AC#4: Existing Functionality Preserved"
echo "========================================================================"
echo ""

# Test 4.1: Verify backend-architect.md exists
run_test \
    "test_backend_architect_file_exists" \
    "Verify backend-architect.md subagent file exists"
assert_file_exists "$BACKEND_ARCHITECT"

# Test 4.2: Verify api-designer.md exists
run_test \
    "test_api_designer_file_exists" \
    "Verify api-designer.md subagent file exists"
assert_file_exists "$API_DESIGNER"

echo ""
echo "--- Backend Architect Functionality Tests ---"
echo ""

# Test 4.3: Backend architect - Purpose section preserved
run_test \
    "test_backend_architect_purpose_section" \
    "Verify Purpose section exists in backend-architect.md"
assert_section_exists "^## Purpose" "$BACKEND_ARCHITECT" "Purpose"

# Test 4.4: Backend architect - Workflow section preserved
run_test \
    "test_backend_architect_workflow_section" \
    "Verify Workflow section exists in backend-architect.md"
assert_section_exists "^## Workflow" "$BACKEND_ARCHITECT" "Workflow"

# Test 4.5: Backend architect - Success Criteria section preserved
run_test \
    "test_backend_architect_success_criteria_section" \
    "Verify Success Criteria section exists in backend-architect.md"
assert_section_exists "^## Success Criteria" "$BACKEND_ARCHITECT" "Success Criteria"

# Test 4.6: Backend architect - TDD reference preserved
run_test \
    "test_backend_architect_tdd_reference" \
    "Verify TDD workflow reference preserved"
assert_grep_match "TDD" "$BACKEND_ARCHITECT" "TDD reference exists in backend-architect.md"

# Test 4.7: Backend architect - Implementation capability preserved
run_test \
    "test_backend_architect_implementation_capability" \
    "Verify implementation/architecture capability documented"
assert_grep_match "implement\|architecture\|design" "$BACKEND_ARCHITECT" "Implementation/architecture capability documented"

# Test 4.8: Backend architect - Context file validation preserved
run_test \
    "test_backend_architect_context_validation" \
    "Verify context file validation reference preserved"
assert_grep_match "context.*file\|tech-stack\|coding-standards" "$BACKEND_ARCHITECT" "Context file validation preserved"

echo ""
echo "--- API Designer Functionality Tests ---"
echo ""

# Test 4.9: API designer - Purpose section preserved
run_test \
    "test_api_designer_purpose_section" \
    "Verify Purpose section exists in api-designer.md"
assert_section_exists "^## Purpose" "$API_DESIGNER" "Purpose"

# Test 4.10: API designer - Workflow section preserved
run_test \
    "test_api_designer_workflow_section" \
    "Verify Workflow section exists in api-designer.md"
assert_section_exists "^## Workflow" "$API_DESIGNER" "Workflow"

# Test 4.11: API designer - Success Criteria section preserved
run_test \
    "test_api_designer_success_criteria_section" \
    "Verify Success Criteria section exists in api-designer.md"
assert_section_exists "^## Success Criteria" "$API_DESIGNER" "Success Criteria"

# Test 4.12: API designer - API design capability preserved
run_test \
    "test_api_designer_api_design_capability" \
    "Verify API design capability documented"
assert_grep_match "API.*design\|REST\|GraphQL\|endpoint" "$API_DESIGNER" "API design capability documented"

# Test 4.13: API designer - OpenAPI reference preserved
run_test \
    "test_api_designer_openapi_reference" \
    "Verify OpenAPI/schema reference preserved"
assert_grep_match "OpenAPI\|schema\|specification" "$API_DESIGNER" "OpenAPI/schema reference preserved"

# Test 4.14: Backend architect - YAML frontmatter preserved
run_test \
    "test_backend_architect_frontmatter" \
    "Verify YAML frontmatter exists with name and description"
if head -20 "$BACKEND_ARCHITECT" | grep -q "^name:\|^description:"; then
    echo -e "${GREEN}PASSED${NC}: YAML frontmatter with name/description exists"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAILED${NC}: YAML frontmatter missing or incomplete"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 4.15: API designer - YAML frontmatter preserved
run_test \
    "test_api_designer_frontmatter" \
    "Verify YAML frontmatter exists with name and description"
if head -20 "$API_DESIGNER" | grep -q "^name:\|^description:"; then
    echo -e "${GREEN}PASSED${NC}: YAML frontmatter with name/description exists"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAILED${NC}: YAML frontmatter missing or incomplete"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

##############################################################################
# Summary Report
##############################################################################

echo ""
echo "========================================================================"
echo "Test Summary Report - AC#4"
echo "========================================================================"
echo "Total Tests Run:    $TESTS_RUN"
echo -e "Tests Passed:       ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed:       ${RED}$TESTS_FAILED${NC}"
echo "========================================================================"

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}SUCCESS: All AC#4 tests passed${NC}"
    exit 0
else
    echo -e "${RED}FAILURE: AC#4 tests failed - Implementation may have broken existing functionality${NC}"
    exit 1
fi
