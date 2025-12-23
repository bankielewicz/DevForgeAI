#!/bin/bash

#############################################################################
# STORY-127: AC#3 - Plan Files with Story ID Are Prioritized
#############################################################################
#
# Test Objective:
#   Verify that when multiple plan files exist:
#   1. Files containing the current story ID are prioritized
#   2. Random-named files without story ID are deprioritized
#   3. Story ID match is suggested first
#
# Test Location: devforgeai/tests/STORY-127/test-ac3-story-id-priority.sh
# Test Framework: Bash (native to DevForgeAI)
# Status: FAILING (Red phase - TDD)
#
#############################################################################

set -euo pipefail

# Define test environment
TEST_NAME="AC#3: Plan Files with Story ID Are Prioritized"
DEVFORGEAI_DEV_SKILL="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-development"
PREFLIGHT_REF="$DEVFORGEAI_DEV_SKILL/references/preflight-validation.md"
SKILL_MD="$DEVFORGEAI_DEV_SKILL/SKILL.md"
CLAUDE_PLANS_FIXTURE="/tmp/test-claude-plans-$$"
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

# Setup: Create temporary test fixture
setup_fixture() {
    mkdir -p "$CLAUDE_PLANS_FIXTURE"

    # Create test plan files
    cat > "$CLAUDE_PLANS_FIXTURE/STORY-127-plan-file-resume.md" << 'EOF'
# Plan for STORY-127

This is the story ID named plan file.
Contains: STORY-127
EOF

    cat > "$CLAUDE_PLANS_FIXTURE/clever-snuggling-otter.md" << 'EOF'
# Random named plan file

This is a random-named file that also contains STORY-127 in content.
Reference: STORY-127
EOF

    cat > "$CLAUDE_PLANS_FIXTURE/enchanted-booping-pizza.md" << 'EOF'
# Another random plan

No story ID reference here.
This is unrelated to STORY-127.
EOF
}

# Cleanup: Remove temporary fixture
cleanup_fixture() {
    rm -rf "$CLAUDE_PLANS_FIXTURE"
}

#############################################################################
# Test Case 3.1: Documentation mentions prioritization strategy
#############################################################################

test_prioritization_documented() {
    echo -e "\n${YELLOW}Test 3.1: Prioritization strategy documented${NC}"

    local found=0

    # Check for prioritization/priority/suggest documentation
    if [[ -f "$SKILL_MD" ]] && grep -q -i "priorit\|suggest.*first\|prefer" "$SKILL_MD"; then
        found=1
    fi

    if [[ -f "$PREFLIGHT_REF" ]] && grep -q -i "priorit\|suggest.*first\|prefer" "$PREFLIGHT_REF"; then
        found=1
    fi

    if [[ $found -eq 1 ]]; then
        echo -e "${GREEN}✓ PASS${NC}: Prioritization strategy documented"
        ((TEST_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Prioritization strategy NOT documented"
        echo "Expected: Keywords like 'prioritize', 'suggest first', 'prefer'"
        ((TEST_FAILED++))
        return 1
    fi
}

#############################################################################
# Test Case 3.2: Documentation mentions deprioritizing random names
#############################################################################

test_deprioritize_random_names() {
    echo -e "\n${YELLOW}Test 3.2: Documentation mentions deprioritizing random names${NC}"

    local found=0

    # Check for deprioritize/random/names documentation
    if [[ -f "$SKILL_MD" ]] && grep -q -i "random.*name\|depriorit\|avoid.*random" "$SKILL_MD"; then
        found=1
    fi

    if [[ -f "$PREFLIGHT_REF" ]] && grep -q -i "random.*name\|depriorit\|avoid.*random" "$PREFLIGHT_REF"; then
        found=1
    fi

    if [[ $found -eq 1 ]]; then
        echo -e "${GREEN}✓ PASS${NC}: Deprioritizing random names documented"
        ((TEST_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Deprioritizing random names NOT documented"
        echo "Expected: Keywords like 'random', 'deprioritize', or 'avoid random'"
        ((TEST_FAILED++))
        return 1
    fi
}

#############################################################################
# Test Case 3.3: Search algorithm sorts by story ID match
#############################################################################

test_search_sorts_by_story_id() {
    echo -e "\n${YELLOW}Test 3.3: Search algorithm sorts results by story ID match${NC}"

    setup_fixture

    # Simulate search: find all files, grep for story ID, sort by match
    local story_id="STORY-127"
    local matches=()

    # Find files with story ID in name
    while IFS= read -r file; do
        if [[ $(basename "$file") == *"$story_id"* ]]; then
            matches+=("$file (name match)")
        fi
    done < <(find "$CLAUDE_PLANS_FIXTURE" -name "*.md" -type f)

    # Find files with story ID in content
    while IFS= read -r file; do
        local basename=$(basename "$file")
        # Skip if already in matches
        if [[ ! " ${matches[@]} " =~ " $file " ]]; then
            if grep -q "$story_id" "$file"; then
                matches+=("$file (content match)")
            fi
        fi
    done < <(find "$CLAUDE_PLANS_FIXTURE" -name "*.md" -type f)

    cleanup_fixture

    # Check if story ID file is first or prioritized
    if [[ ${#matches[@]} -gt 0 ]]; then
        # Should have at least 2 matches (STORY-127 file + clever-snuggling file)
        if [[ ${#matches[@]} -ge 2 ]]; then
            # First match should be the story ID named file
            if [[ "${matches[0]}" == *"STORY-127-plan-file-resume"* ]]; then
                echo -e "${GREEN}✓ PASS${NC}: Story ID file prioritized in search results"
                ((TEST_PASSED++))
                return 0
            fi
        fi
    fi

    echo -e "${RED}✗ FAIL${NC}: Story ID file NOT prioritized in search results"
    echo "Expected: Story ID named file appears first in results"
    echo "Got: ${matches[@]}"
    ((TEST_FAILED++))
    return 1
}

#############################################################################
# Test Case 3.4: Documentation covers word boundary matching
#############################################################################

test_word_boundary_matching() {
    echo -e "\n${YELLOW}Test 3.4: Word boundary matching prevents false positives${NC}"

    local found=0

    # Check for word boundary documentation (STORY-11 vs STORY-114 issue)
    if [[ -f "$SKILL_MD" ]] && grep -q -i "word.*bound\|\\\\b\|false.*positive" "$SKILL_MD"; then
        found=1
    fi

    if [[ -f "$PREFLIGHT_REF" ]] && grep -q -i "word.*bound\|\\\\b\|false.*positive" "$PREFLIGHT_REF"; then
        found=1
    fi

    if [[ $found -eq 1 ]]; then
        echo -e "${GREEN}✓ PASS${NC}: Word boundary matching documented"
        ((TEST_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Word boundary matching NOT documented"
        echo "Expected: Keywords like 'word boundary', '\\\\b', 'false positive'"
        echo "Reason: Prevent STORY-11 matching STORY-114 filename/content"
        ((TEST_FAILED++))
        return 1
    fi
}

#############################################################################
# Test Case 3.5: Documentation covers handling of multiple matches
#############################################################################

test_multiple_matches_handled() {
    echo -e "\n${YELLOW}Test 3.5: Handling of multiple plan file matches documented${NC}"

    local found=0

    # Check for documentation on multiple matches scenario
    if [[ -f "$SKILL_MD" ]] && grep -q -i "multiple.*match\|multiple.*file\|several.*plan" "$SKILL_MD"; then
        found=1
    fi

    if [[ -f "$PREFLIGHT_REF" ]] && grep -q -i "multiple.*match\|multiple.*file\|several.*plan" "$PREFLIGHT_REF"; then
        found=1
    fi

    if [[ $found -eq 1 ]]; then
        echo -e "${GREEN}✓ PASS${NC}: Multiple matches handling documented"
        ((TEST_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Multiple matches handling NOT documented"
        echo "Expected: Guidance on handling multiple matching plan files"
        ((TEST_FAILED++))
        return 1
    fi
}

#############################################################################
# Test Case 3.6: Practical test - Simulate search with test fixtures
#############################################################################

test_practical_search_simulation() {
    echo -e "\n${YELLOW}Test 3.6: Practical simulation of prioritization logic${NC}"

    setup_fixture

    local story_id="STORY-127"

    # Simulate the search algorithm:
    # 1. Find all plan files
    # 2. Prioritize: name match first, then content match
    # 3. Deprioritize: unrelated files

    local name_matches=()
    local content_matches=()
    local no_matches=()

    for file in "$CLAUDE_PLANS_FIXTURE"/*.md; do
        if [[ $(basename "$file") == *"$story_id"* ]]; then
            name_matches+=("$file")
        elif grep -q "$story_id" "$file"; then
            content_matches+=("$file")
        else
            no_matches+=("$file")
        fi
    done

    cleanup_fixture

    # Verify: Story ID file found first, random-named file second, unrelated last
    if [[ ${#name_matches[@]} -eq 1 && ${#content_matches[@]} -eq 1 && ${#no_matches[@]} -eq 1 ]]; then
        echo -e "${GREEN}✓ PASS${NC}: Correct prioritization order"
        echo "  - Name match (highest priority): $(basename "${name_matches[0]}")"
        echo "  - Content match (medium priority): $(basename "${content_matches[0]}")"
        echo "  - No match (lowest priority): $(basename "${no_matches[0]}")"
        ((TEST_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Incorrect match categorization"
        echo "  - Name matches: ${#name_matches[@]} (expected: 1)"
        echo "  - Content matches: ${#content_matches[@]} (expected: 1)"
        echo "  - No matches: ${#no_matches[@]} (expected: 1)"
        ((TEST_FAILED++))
        return 1
    fi
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
    test_prioritization_documented
    test_deprioritize_random_names
    test_search_sorts_by_story_id
    test_word_boundary_matching
    test_multiple_matches_handled
    test_practical_search_simulation

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
        echo -e "${RED}RESULT: FAILED${NC} - AC#3 not implemented"
        echo ""
        echo "Next Steps:"
        echo "  1. Document prioritization strategy in SKILL.md Phase 0"
        echo "  2. Sort search results: name match (STORY-127 in filename) first"
        echo "  3. Content matches (STORY-127 in file content) second"
        echo "  4. Unrelated files deprioritized"
        echo "  5. Use word boundary grep to prevent false positives"
        echo "  6. Handle multiple matching files gracefully"
        echo ""
        exit 1
    else
        echo -e "${GREEN}RESULT: PASSED${NC} - AC#3 fully implemented"
        echo ""
        exit 0
    fi
}

# Execute main test function
main "$@"
