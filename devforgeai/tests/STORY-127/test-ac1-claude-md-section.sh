#!/bin/bash

#############################################################################
# STORY-127: AC#1 - CLAUDE.md Includes Plan File Convention Section
#############################################################################
#
# Test Objective:
#   Verify that CLAUDE.md contains a "Plan File Convention" section with
#   proper documentation of: plan file detection, search algorithm,
#   naming convention, and resume decision logic.
#
# Test Location: devforgeai/tests/STORY-127/test-ac1-claude-md-section.sh
# Test Framework: Bash (native to DevForgeAI)
# Status: FAILING (Red phase - TDD)
#
#############################################################################

set -euo pipefail

# Define test environment
TEST_NAME="AC#1: CLAUDE.md Includes Plan File Convention Section"
CLAUDE_MD_PATH="/mnt/c/Projects/DevForgeAI2/CLAUDE.md"
TEST_PASSED=0
TEST_FAILED=0

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "==============================================================================="
echo "TEST: $TEST_NAME"
echo "==============================================================================="

#############################################################################
# Test Case 1.1: Plan File Convention Section Exists
#############################################################################

test_section_exists() {
    echo -e "\n${YELLOW}Test 1.1: Plan File Convention section exists${NC}"

    if grep -q "## Plan File Convention" "$CLAUDE_MD_PATH"; then
        echo -e "${GREEN}✓ PASS${NC}: Plan File Convention section found in CLAUDE.md"
        ((TEST_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Plan File Convention section NOT found in CLAUDE.md"
        echo "Expected section header: '## Plan File Convention'"
        ((TEST_FAILED++))
        return 1
    fi
}

#############################################################################
# Test Case 1.2: Documents "check for existing plans"
#############################################################################

test_documents_check_for_existing() {
    echo -e "\n${YELLOW}Test 1.2: Documents checking for existing plan files${NC}"

    # Extract Plan File Convention section and search for documentation
    local section_content=$(sed -n '/^## Plan File Convention/,/^## /p' "$CLAUDE_MD_PATH" | head -n -1)

    if echo "$section_content" | grep -q -i "check.*existing\|existing.*plan"; then
        echo -e "${GREEN}✓ PASS${NC}: Section documents checking for existing plan files"
        ((TEST_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Section does NOT document checking for existing plan files"
        echo "Expected keywords: 'check', 'existing', 'plan'"
        ((TEST_FAILED++))
        return 1
    fi
}

#############################################################################
# Test Case 1.3: Documents Search Algorithm (glob + grep)
#############################################################################

test_documents_search_algorithm() {
    echo -e "\n${YELLOW}Test 1.3: Documents search algorithm (glob and grep patterns)${NC}"

    local section_content=$(sed -n '/^## Plan File Convention/,/^## /p' "$CLAUDE_MD_PATH" | head -n -1)

    # Check for both glob and grep mentions in algorithm
    local has_glob=0
    local has_grep=0
    local has_algorithm=0

    if echo "$section_content" | grep -q -i "glob\|\.claude/plans"; then
        has_glob=1
    fi

    if echo "$section_content" | grep -q -i "grep\|search.*story\|pattern"; then
        has_grep=1
    fi

    if echo "$section_content" | grep -q -i "algorithm\|search"; then
        has_algorithm=1
    fi

    if [[ $has_algorithm -eq 1 && $has_glob -eq 1 && $has_grep -eq 1 ]]; then
        echo -e "${GREEN}✓ PASS${NC}: Section documents search algorithm with glob and grep"
        ((TEST_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Section does NOT properly document search algorithm"
        echo "  - Has 'algorithm' or 'search': $has_algorithm (expected: 1)"
        echo "  - Has 'glob' or '.claude/plans': $has_glob (expected: 1)"
        echo "  - Has 'grep' or pattern references: $has_grep (expected: 1)"
        ((TEST_FAILED++))
        return 1
    fi
}

#############################################################################
# Test Case 1.4: Documents Naming Convention with Story ID
#############################################################################

test_documents_naming_convention() {
    echo -e "\n${YELLOW}Test 1.4: Documents naming convention with story ID${NC}"

    local section_content=$(sed -n '/^## Plan File Convention/,/^## /p' "$CLAUDE_MD_PATH" | head -n -1)

    if echo "$section_content" | grep -q -i "naming\|story.*id\|STORY-"; then
        echo -e "${GREEN}✓ PASS${NC}: Section documents naming convention with story ID"
        ((TEST_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Section does NOT document naming convention with story ID"
        echo "Expected keywords: 'naming', 'story ID', or STORY- example"
        ((TEST_FAILED++))
        return 1
    fi
}

#############################################################################
# Test Case 1.5: Documents Resume vs Create Decision Logic
#############################################################################

test_documents_resume_decision() {
    echo -e "\n${YELLOW}Test 1.5: Documents resume vs create decision logic${NC}"

    local section_content=$(sed -n '/^## Plan File Convention/,/^## /p' "$CLAUDE_MD_PATH" | head -n -1)

    local has_resume=0
    local has_create=0

    if echo "$section_content" | grep -q -i "resume"; then
        has_resume=1
    fi

    if echo "$section_content" | grep -q -i "create\|new"; then
        has_create=1
    fi

    if [[ $has_resume -eq 1 && $has_create -eq 1 ]]; then
        echo -e "${GREEN}✓ PASS${NC}: Section documents resume vs create decision logic"
        ((TEST_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Section does NOT document resume vs create decision logic"
        echo "  - Has 'resume': $has_resume (expected: 1)"
        echo "  - Has 'create' or 'new': $has_create (expected: 1)"
        ((TEST_FAILED++))
        return 1
    fi
}

#############################################################################
# MAIN TEST EXECUTION
#############################################################################

main() {
    echo ""

    # Run all test cases
    test_section_exists
    test_documents_check_for_existing
    test_documents_search_algorithm
    test_documents_naming_convention
    test_documents_resume_decision

    # Summary
    echo ""
    echo "==============================================================================="
    echo "TEST SUMMARY: $TEST_NAME"
    echo "==============================================================================="
    echo -e "Tests Passed: ${GREEN}$TEST_PASSED${NC}"
    echo -e "Tests Failed: ${RED}$TEST_FAILED${NC}"
    echo "Total Tests:  $((TEST_PASSED + TEST_FAILED))"
    echo ""

    if [[ $TEST_FAILED -gt 0 ]]; then
        echo -e "${RED}RESULT: FAILED${NC} - AC#1 not implemented"
        echo ""
        echo "Next Steps:"
        echo "  1. Add '## Plan File Convention' section to CLAUDE.md"
        echo "  2. Document: check for existing plan files"
        echo "  3. Document: search algorithm (glob + grep for story ID)"
        echo "  4. Document: naming convention with story ID"
        echo "  5. Document: resume vs create decision logic"
        echo ""
        exit 1
    else
        echo -e "${GREEN}RESULT: PASSED${NC} - AC#1 fully implemented"
        echo ""
        exit 0
    fi
}

# Execute main test function
main "$@"
