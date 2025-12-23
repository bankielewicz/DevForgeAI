#!/bin/bash

#############################################################################
# STORY-127: AC#2 - /dev Phase 0 Checks for Existing Plans
#############################################################################
#
# Test Objective:
#   Verify that /dev Phase 0 preflight validation:
#   1. Searches .claude/plans/*.md for files containing the story ID
#   2. Prompts user when existing plan found: "Existing plan file found: {filename}. Resume this plan?"
#
# Test Location: devforgeai/tests/STORY-127/test-ac2-phase0-search.sh
# Test Framework: Bash (native to DevForgeAI)
# Status: FAILING (Red phase - TDD)
#
#############################################################################

set -euo pipefail

# Define test environment
TEST_NAME="AC#2: /dev Phase 0 Checks for Existing Plans"
DEVFORGEAI_DEV_SKILL="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-development"
PREFLIGHT_REF="$DEVFORGEAI_DEV_SKILL/references/preflight-validation.md"
SKILL_MD="$DEVFORGEAI_DEV_SKILL/SKILL.md"
TEST_PASSED=0
TEST_FAILED=0

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "==============================================================================="
echo "TEST: $TEST_NAME"
echo "==============================================================================="

#############################################################################
# Test Case 2.1: SKILL.md Phase 0 includes plan file search logic
#############################################################################

test_skill_md_phase0_search() {
    echo -e "\n${YELLOW}Test 2.1: SKILL.md Phase 0 includes plan file search logic${NC}"

    # Check if SKILL.md documents plan file search in Phase 0
    if grep -q "plan.*file\|\.claude/plans" "$SKILL_MD"; then
        # Verify it's in Phase 0/Pre-Flight section
        if grep -B 50 "plan.*file\|\.claude/plans" "$SKILL_MD" | grep -q "Phase.*0\|Pre.*[Ff]light"; then
            echo -e "${GREEN}✓ PASS${NC}: SKILL.md documents plan file search in Phase 0"
            ((TEST_PASSED++))
            return 0
        fi
    fi

    echo -e "${RED}✗ FAIL${NC}: SKILL.md does NOT document plan file search in Phase 0"
    echo "Expected: Plan file detection documented in Phase 0/Pre-Flight section"
    ((TEST_FAILED++))
    return 1
}

#############################################################################
# Test Case 2.2: Search uses Glob to list plan files
#############################################################################

test_search_uses_glob() {
    echo -e "\n${YELLOW}Test 2.2: Search algorithm uses Glob to list plan files${NC}"

    # Look for both SKILL.md and preflight-validation.md
    local found=0

    if [[ -f "$SKILL_MD" ]] && grep -q "Glob.*\.claude/plans\|Glob.*pattern.*plans" "$SKILL_MD"; then
        found=1
    fi

    if [[ -f "$PREFLIGHT_REF" ]] && grep -q "Glob.*\.claude/plans\|Glob.*pattern.*plans" "$PREFLIGHT_REF"; then
        found=1
    fi

    if [[ $found -eq 1 ]]; then
        echo -e "${GREEN}✓ PASS${NC}: Search algorithm uses Glob to list plan files"
        ((TEST_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Search algorithm does NOT use Glob to list plan files"
        echo "Expected: 'Glob(pattern=\".claude/plans/*.md\")' or similar"
        ((TEST_FAILED++))
        return 1
    fi
}

#############################################################################
# Test Case 2.3: Search uses Grep to find story ID in plan files
#############################################################################

test_search_uses_grep_for_story_id() {
    echo -e "\n${YELLOW}Test 2.3: Search algorithm uses Grep to find story ID${NC}"

    local found=0

    # Check for Grep with story ID pattern
    if [[ -f "$SKILL_MD" ]] && grep -q "Grep.*STORY\|Grep.*story.*id\|grep.*STORY" "$SKILL_MD"; then
        found=1
    fi

    if [[ -f "$PREFLIGHT_REF" ]] && grep -q "Grep.*STORY\|Grep.*story.*id\|grep.*STORY" "$PREFLIGHT_REF"; then
        found=1
    fi

    if [[ $found -eq 1 ]]; then
        echo -e "${GREEN}✓ PASS${NC}: Search algorithm uses Grep to find story ID"
        ((TEST_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Search algorithm does NOT use Grep to find story ID"
        echo "Expected: Grep pattern matching 'STORY-XXX' or similar"
        ((TEST_FAILED++))
        return 1
    fi
}

#############################################################################
# Test Case 2.4: Resume prompt documented in Phase 0
#############################################################################

test_resume_prompt_documented() {
    echo -e "\n${YELLOW}Test 2.4: Resume prompt documented when plan found${NC}"

    local found=0

    # Check for AskUserQuestion with resume prompt
    if [[ -f "$SKILL_MD" ]] && grep -q "Existing plan file found\|Resume.*plan"; then
        found=1
    fi

    if [[ -f "$PREFLIGHT_REF" ]] && grep -q "Existing plan file found\|Resume.*plan"; then
        found=1
    fi

    if [[ $found -eq 1 ]]; then
        echo -e "${GREEN}✓ PASS${NC}: Resume prompt documented in Phase 0"
        ((TEST_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Resume prompt NOT documented in Phase 0"
        echo "Expected: Prompt text like 'Existing plan file found: {filename}. Resume this plan?'"
        ((TEST_FAILED++))
        return 1
    fi
}

#############################################################################
# Test Case 2.5: Resume prompt uses AskUserQuestion
#############################################################################

test_resume_uses_ask_user_question() {
    echo -e "\n${YELLOW}Test 2.5: Resume logic uses AskUserQuestion for user interaction${NC}"

    local found=0

    # Check for AskUserQuestion invocation
    if [[ -f "$SKILL_MD" ]] && grep -q "AskUserQuestion.*resume\|AskUserQuestion.*plan"; then
        found=1
    fi

    if [[ -f "$PREFLIGHT_REF" ]] && grep -q "AskUserQuestion.*resume\|AskUserQuestion.*plan"; then
        found=1
    fi

    if [[ $found -eq 1 ]]; then
        echo -e "${GREEN}✓ PASS${NC}: Resume logic uses AskUserQuestion"
        ((TEST_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Resume logic does NOT use AskUserQuestion"
        echo "Expected: AskUserQuestion tool call for resume decision"
        ((TEST_FAILED++))
        return 1
    fi
}

#############################################################################
# Test Case 2.6: Phase 0 executes search BEFORE creating new plan
#############################################################################

test_search_before_create() {
    echo -e "\n${YELLOW}Test 2.6: Plan file search executes BEFORE creating new plan${NC}"

    # Check order in SKILL.md Phase 0 section
    local phase0_section=$(sed -n '/^## Pre.*Flight.*Phase.*01\|^## Phase.*0/,/^## Phase.*0[2-9]\|^## [A-Z]/p' "$SKILL_MD" | head -n -1)

    if echo "$phase0_section" | grep -q "plan.*file\|\.claude/plans"; then
        # Verify search comes before new plan creation
        local search_line=$(echo "$phase0_section" | grep -n "plan.*file\|\.claude/plans" | head -1 | cut -d: -f1)
        local create_line=$(echo "$phase0_section" | grep -n "create.*plan\|new.*plan" | head -1 | cut -d: -f1)

        if [[ -z "$create_line" ]] || [[ $search_line -lt $create_line ]]; then
            echo -e "${GREEN}✓ PASS${NC}: Plan file search executes before creating new plan"
            ((TEST_PASSED++))
            return 0
        fi
    fi

    echo -e "${RED}✗ FAIL${NC}: Plan file search does NOT execute before creating new plan"
    echo "Expected: Search logic documented before new plan creation in Phase 0"
    ((TEST_FAILED++))
    return 1
}

#############################################################################
# MAIN TEST EXECUTION
#############################################################################

main() {
    echo ""

    # Verify files exist
    if [[ ! -f "$SKILL_MD" ]]; then
        echo -e "${RED}ERROR${NC}: $SKILL_MD not found"
        exit 1
    fi

    # Run all test cases
    test_skill_md_phase0_search
    test_search_uses_glob
    test_search_uses_grep_for_story_id
    test_resume_prompt_documented
    test_resume_uses_ask_user_question
    test_search_before_create

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
        echo -e "${RED}RESULT: FAILED${NC} - AC#2 not implemented"
        echo ""
        echo "Next Steps:"
        echo "  1. Add plan file search to devforgeai-development SKILL.md Phase 0"
        echo "  2. Use Glob to list .claude/plans/*.md files"
        echo "  3. Use Grep to search for story ID in each plan file"
        echo "  4. Document resume prompt: 'Existing plan file found: {filename}. Resume this plan?'"
        echo "  5. Use AskUserQuestion for user decision"
        echo "  6. Execute search BEFORE creating new plan"
        echo ""
        exit 1
    else
        echo -e "${GREEN}RESULT: PASSED${NC} - AC#2 fully implemented"
        echo ""
        exit 0
    fi
}

# Execute main test function
main "$@"
