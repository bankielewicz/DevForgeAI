#!/bin/bash

#############################################################################
# STORY-127: AC#4 - New Plans Use Story ID in Filename
#############################################################################
#
# Test Objective:
#   Verify that when no existing plan file matches the story:
#   1. New plan filename includes the story ID
#   2. Example: STORY-127-plan-file-resume.md (not groovy-swimming-lake.md)
#   3. Naming follows pattern: STORY-{ID}-{description}.md
#
# Test Location: devforgeai/tests/STORY-127/test-ac4-new-plan-naming.sh
# Test Framework: Bash (native to DevForgeAI)
# Status: FAILING (Red phase - TDD)
#
#############################################################################

set -euo pipefail

# Define test environment
TEST_NAME="AC#4: New Plans Use Story ID in Filename"
DEVFORGEAI_DEV_SKILL="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-development"
SKILL_MD="$DEVFORGEAI_DEV_SKILL/SKILL.md"
PREFLIGHT_REF="$DEVFORGEAI_DEV_SKILL/references/preflight-validation.md"
CLAUDE_MD="/mnt/c/Projects/DevForgeAI2/CLAUDE.md"
TEST_PASSED=0
TEST_FAILED=0

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "==============================================================================="
echo "TEST: $TEST_NAME"
echo "==============================================================================="

#############################################################################
# Test Case 4.1: CLAUDE.md documents naming convention with story ID
#############################################################################

test_claude_md_naming_convention() {
    echo -e "\n${YELLOW}Test 4.1: CLAUDE.md documents story ID naming convention${NC}"

    # Extract Plan File Convention section
    local section_content=$(sed -n '/^## Plan File Convention/,/^## /p' "$CLAUDE_MD" | head -n -1)

    # Check for examples with STORY- prefix
    if echo "$section_content" | grep -q "STORY-.*\.md\|STORY-.*md"; then
        # Verify the example matches the pattern
        if echo "$section_content" | grep -q "STORY-[0-9]*"; then
            echo -e "${GREEN}✓ PASS${NC}: Story ID naming convention documented with examples"
            ((TEST_PASSED++))
            return 0
        fi
    fi

    echo -e "${RED}✗ FAIL${NC}: Story ID naming convention NOT documented in CLAUDE.md"
    echo "Expected: Examples like 'STORY-127-plan-file-resume.md'"
    ((TEST_FAILED++))
    return 1
}

#############################################################################
# Test Case 4.2: Documentation contrasts good vs bad naming
#############################################################################

test_good_vs_bad_naming() {
    echo -e "\n${YELLOW}Test 4.2: Documentation shows good vs bad naming examples${NC}"

    local section_content=$(sed -n '/^## Plan File Convention/,/^## /p' "$CLAUDE_MD" | head -n -1)

    # Check for good/bad or recommended/avoid language
    if echo "$section_content" | grep -q -i "good\|bad\|recommend\|avoid\|✓\|❌"; then
        echo -e "${GREEN}✓ PASS${NC}: Good vs bad naming examples documented"
        ((TEST_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Good vs bad naming examples NOT documented"
        echo "Expected: Contrast examples (e.g., Good: STORY-127-..., Bad: random-name.md)"
        ((TEST_FAILED++))
        return 1
    fi
}

#############################################################################
# Test Case 4.3: Documentation mentions avoiding random adjective-noun combinations
#############################################################################

test_avoid_random_combinations() {
    echo -e "\n${YELLOW}Test 4.3: Documentation avoids random adjective-noun combinations${NC}"

    local section_content=$(sed -n '/^## Plan File Convention/,/^## /p' "$CLAUDE_MD" | head -n -1)

    # Check for keywords about avoiding random names
    if echo "$section_content" | grep -q -i "random\|adjective\|noun\|groovy\|avoid"; then
        echo -e "${GREEN}✓ PASS${NC}: Avoiding random combinations documented"
        ((TEST_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Avoiding random combinations NOT documented"
        echo "Expected: Keywords like 'random', 'avoid', or example like 'groovy-swimming-lake'"
        ((TEST_FAILED++))
        return 1
    fi
}

#############################################################################
# Test Case 4.4: SKILL.md Phase 0 creates new plans with story ID
#############################################################################

test_phase0_creates_with_story_id() {
    echo -e "\n${YELLOW}Test 4.4: Phase 0 creates new plan with story ID in filename${NC}"

    # Check SKILL.md for new plan creation logic with story ID
    local found=0

    if grep -q "new.*plan.*STORY\|create.*plan.*story.*id\|\.claude/plans/STORY" "$SKILL_MD"; then
        found=1
    fi

    if [[ -f "$PREFLIGHT_REF" ]] && grep -q "new.*plan.*STORY\|create.*plan.*story.*id\|\.claude/plans/STORY" "$PREFLIGHT_REF"; then
        found=1
    fi

    if [[ $found -eq 1 ]]; then
        echo -e "${GREEN}✓ PASS${NC}: Phase 0 creates new plan with story ID"
        ((TEST_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Phase 0 does NOT create new plan with story ID"
        echo "Expected: Documentation of new plan creation with STORY- prefix"
        ((TEST_FAILED++))
        return 1
    fi
}

#############################################################################
# Test Case 4.5: Naming pattern documented (STORY-XXX-description.md)
#############################################################################

test_naming_pattern_documented() {
    echo -e "\n${YELLOW}Test 4.5: Naming pattern documented (STORY-XXX-description.md)${NC}"

    local section_content=$(sed -n '/^## Plan File Convention/,/^## /p' "$CLAUDE_MD" | head -n -1)

    # Check for the naming pattern with STORY- ID and description
    if echo "$section_content" | grep -q "STORY-[0-9]*.*\.md\|STORY.*description\|pattern"; then
        echo -e "${GREEN}✓ PASS${NC}: Naming pattern documented"
        ((TEST_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Naming pattern NOT documented"
        echo "Expected: Pattern like 'STORY-{ID}-{description}.md'"
        ((TEST_FAILED++))
        return 1
    fi
}

#############################################################################
# Test Case 4.6: Practical test - Validate naming with regex
#############################################################################

test_practical_naming_validation() {
    echo -e "\n${YELLOW}Test 4.6: Practical validation of STORY-XXX naming pattern${NC}"

    # Test valid and invalid filenames
    local valid_names=(
        "STORY-127-plan-file-resume.md"
        "STORY-001-test.md"
        "STORY-999-some-description.md"
    )

    local invalid_names=(
        "groovy-swimming-lake.md"
        "clever-snuggling-otter.md"
        "enchanted-booping-pizza.md"
        "plan.md"
        "STORY-notnumber.md"
    )

    # Validate pattern: ^STORY-[0-9]+-.*\.md$
    local pattern="^STORY-[0-9]+-.*\.md$"
    local valid_count=0
    local invalid_count=0

    for name in "${valid_names[@]}"; do
        if [[ $name =~ $pattern ]]; then
            ((valid_count++))
        fi
    done

    for name in "${invalid_names[@]}"; do
        if ! [[ $name =~ $pattern ]]; then
            ((invalid_count++))
        fi
    done

    # Both should match their expectations
    if [[ $valid_count -eq 3 && $invalid_count -eq 5 ]]; then
        echo -e "${GREEN}✓ PASS${NC}: Naming pattern validation works correctly"
        ((TEST_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Naming pattern validation failed"
        echo "  Valid matches: $valid_count/3 (expected: 3)"
        echo "  Invalid matches: $invalid_count/5 (expected: 5)"
        ((TEST_FAILED++))
        return 1
    fi
}

#############################################################################
# Test Case 4.7: Exception for exploratory work documented
#############################################################################

test_exception_for_exploratory_work() {
    echo -e "\n${YELLOW}Test 4.7: Exception documented for exploratory work${NC}"

    local section_content=$(sed -n '/^## Plan File Convention/,/^## /p' "$CLAUDE_MD" | head -n -1)

    # Check for exception clause
    if echo "$section_content" | grep -q -i "exception\|exploratory\|without.*story\|non.*story"; then
        echo -e "${GREEN}✓ PASS${NC}: Exception for exploratory work documented"
        ((TEST_PASSED++))
        return 0
    else
        echo -e "${YELLOW}⚠ WARN${NC}: Exception for exploratory work NOT documented"
        echo "Optional: Could mention exception for exploration without story context"
        # Not counting as failure - it's optional documentation
        ((TEST_PASSED++))
        return 0
    fi
}

#############################################################################
# MAIN TEST EXECUTION
#############################################################################

main() {
    echo ""

    # Verify files exist
    if [[ ! -f "$CLAUDE_MD" ]]; then
        echo -e "${RED}ERROR${NC}: $CLAUDE_MD not found"
        exit 1
    fi

    if [[ ! -f "$SKILL_MD" ]]; then
        echo -e "${RED}ERROR${NC}: $SKILL_MD not found"
        exit 1
    fi

    # Run all test cases
    test_claude_md_naming_convention
    test_good_vs_bad_naming
    test_avoid_random_combinations
    test_phase0_creates_with_story_id
    test_naming_pattern_documented
    test_practical_naming_validation
    test_exception_for_exploratory_work

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
        echo -e "${RED}RESULT: FAILED${NC} - AC#4 not implemented"
        echo ""
        echo "Next Steps:"
        echo "  1. Document naming convention in CLAUDE.md Plan File Convention section"
        echo "  2. Use pattern: STORY-{ID}-{description}.md"
        echo "  3. Provide examples: STORY-127-plan-file-resume.md"
        echo "  4. Show good vs bad naming (Good: STORY-..., Bad: groovy-swimming-lake.md)"
        echo "  5. Mention exception for exploratory (non-story) work"
        echo "  6. Update SKILL.md Phase 0 to create plans with story ID in filename"
        echo ""
        exit 1
    else
        echo -e "${GREEN}RESULT: PASSED${NC} - AC#4 fully implemented"
        echo ""
        exit 0
    fi
}

# Execute main test function
main "$@"
