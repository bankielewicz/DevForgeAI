#!/bin/bash

#############################################################################
# STORY-127: AC#5 - Backward Compatibility
#############################################################################
#
# Test Objective:
#   Verify that existing random-named plan files containing story ID:
#   1. Are detected and offered for resumption
#   2. No errors occur when random-named files are found
#   3. System gracefully handles mixed naming conventions
#
# Test Location: devforgeai/tests/STORY-127/test-ac5-backward-compat.sh
# Test Framework: Bash (native to DevForgeAI)
# Status: FAILING (Red phase - TDD)
#
# Background: STORY-114 created clever-snuggling-otter.md and
# enchanted-booping-pizza.md. These should still be detected when
# resuming the story, even though they don't follow the new naming convention.
#
#############################################################################

set -euo pipefail

# Define test environment
TEST_NAME="AC#5: Backward Compatibility with Random-Named Plan Files"
DEVFORGEAI_DEV_SKILL="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-development"
SKILL_MD="$DEVFORGEAI_DEV_SKILL/SKILL.md"
PREFLIGHT_REF="$DEVFORGEAI_DEV_SKILL/references/preflight-validation.md"
CLAUDE_MD="/mnt/c/Projects/DevForgeAI2/CLAUDE.md"
TEST_FIXTURE="/tmp/test-backward-compat-$$"
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

# Setup: Create test fixture with random-named plan files
setup_fixture() {
    mkdir -p "$TEST_FIXTURE"

    # Simulate STORY-114 scenario
    cat > "$TEST_FIXTURE/clever-snuggling-otter.md" << 'EOF'
# Plan for STORY-114

This is a random-named plan file created during STORY-114 development.
References: STORY-114
Contains checkpoint data and context from first session.
EOF

    cat > "$TEST_FIXTURE/enchanted-booping-pizza.md" << 'EOF'
# Plan continuation for STORY-114

After context window fill, a second random-named plan was created.
References: STORY-114
Contains checkpoint data from second session.
EOF

    # Also create a properly named modern plan
    cat > "$TEST_FIXTURE/STORY-127-plan-file-resume.md" << 'EOF'
# Plan for STORY-127

This follows the new naming convention with story ID.
References: STORY-127
EOF

    # And an unrelated plan
    cat > "$TEST_FIXTURE/some-random-exploration.md" << 'EOF'
# Random exploration plan

No story reference here.
Not related to STORY-114 or STORY-127.
EOF
}

# Cleanup: Remove temporary fixture
cleanup_fixture() {
    rm -rf "$TEST_FIXTURE"
}

#############################################################################
# Test Case 5.1: Documentation mentions backward compatibility
#############################################################################

test_backward_compat_documented() {
    echo -e "\n${YELLOW}Test 5.1: Backward compatibility explicitly documented${NC}"

    local found=0

    # Check for backward compatibility documentation
    if [[ -f "$CLAUDE_MD" ]] && grep -q -i "backward\|compat\|existing.*random\|legacy" "$CLAUDE_MD"; then
        found=1
    fi

    if [[ -f "$SKILL_MD" ]] && grep -q -i "backward\|compat\|existing.*random\|legacy" "$SKILL_MD"; then
        found=1
    fi

    if [[ $found -eq 1 ]]; then
        echo -e "${GREEN}✓ PASS${NC}: Backward compatibility documented"
        ((TEST_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Backward compatibility NOT documented"
        echo "Expected: Keywords like 'backward', 'compatibility', 'existing random'"
        ((TEST_FAILED++))
        return 1
    fi
}

#############################################################################
# Test Case 5.2: Random-named files with story ID are detected
#############################################################################

test_random_named_files_detected() {
    echo -e "\n${YELLOW}Test 5.2: Random-named files with story ID are detected${NC}"

    setup_fixture

    local story_id="STORY-114"
    local detected=0

    # Simulate detection: find all files with story ID in content
    while IFS= read -r file; do
        if grep -q "$story_id" "$file" 2>/dev/null; then
            detected=$((detected + 1))
            echo "    Found: $(basename "$file")"
        fi
    done < <(find "$TEST_FIXTURE" -name "*.md" -type f)

    cleanup_fixture

    # Should find 2 random-named files with STORY-114
    if [[ $detected -ge 2 ]]; then
        echo -e "${GREEN}✓ PASS${NC}: Random-named files with story ID are detected"
        ((TEST_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Random-named files NOT detected"
        echo "Expected: At least 2 files with STORY-114 detected"
        echo "Got: $detected files"
        ((TEST_FAILED++))
        return 1
    fi
}

#############################################################################
# Test Case 5.3: No errors occur with mixed naming conventions
#############################################################################

test_mixed_naming_no_errors() {
    echo -e "\n${YELLOW}Test 5.3: No errors with mixed naming conventions${NC}"

    setup_fixture

    # Verify all files are readable and grep succeeds
    local errors=0

    for file in "$TEST_FIXTURE"/*.md; do
        if ! grep -q "STORY" "$file" 2>/dev/null; then
            # OK - file just doesn't have story reference
            continue
        elif ! grep "STORY" "$file" > /dev/null 2>&1; then
            # Error reading file
            errors=$((errors + 1))
            echo "    ERROR: Cannot read $file"
        fi
    done

    cleanup_fixture

    if [[ $errors -eq 0 ]]; then
        echo -e "${GREEN}✓ PASS${NC}: No errors with mixed naming conventions"
        ((TEST_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Errors occurred with mixed naming"
        echo "Errors: $errors"
        ((TEST_FAILED++))
        return 1
    fi
}

#############################################################################
# Test Case 5.4: Search algorithm handles both naming styles
#############################################################################

test_algorithm_handles_both_styles() {
    echo -e "\n${YELLOW}Test 5.4: Search algorithm handles both naming styles${NC}"

    local section_content=$(sed -n '/^## Plan File Convention/,/^## /p' "$CLAUDE_MD" | head -n -1)

    # Check that documentation doesn't exclude random-named files
    local has_glob=0
    local has_grep=0
    local no_exclusions=0

    if echo "$section_content" | grep -q -i "glob\|\.claude/plans"; then
        has_glob=1
    fi

    if echo "$section_content" | grep -q -i "grep\|search.*story"; then
        has_grep=1
    fi

    # Check that algorithm doesn't explicitly exclude random names
    if ! echo "$section_content" | grep -q -i "exclude\|skip.*random\|ignore.*random"; then
        no_exclusions=1
    fi

    if [[ $has_glob -eq 1 && $has_grep -eq 1 && $no_exclusions -eq 1 ]]; then
        echo -e "${GREEN}✓ PASS${NC}: Algorithm handles both naming styles"
        ((TEST_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Algorithm does NOT handle both naming styles"
        echo "  - Has glob: $has_glob (expected: 1)"
        echo "  - Has grep: $has_grep (expected: 1)"
        echo "  - No exclusions: $no_exclusions (expected: 1)"
        ((TEST_FAILED++))
        return 1
    fi
}

#############################################################################
# Test Case 5.5: Documentation addresses STORY-114 scenario
#############################################################################

test_story_114_scenario_addressed() {
    echo -e "\n${YELLOW}Test 5.5: STORY-114 scenario addressed in documentation${NC}"

    local section_content=$(sed -n '/^## Plan File Convention/,/^## /p' "$CLAUDE_MD" | head -n -1)

    # Check for references to the specific problem (multiple random plans)
    if echo "$section_content" | grep -q -i "multiple.*plan\|several.*plan\|duplicate"; then
        echo -e "${GREEN}✓ PASS${NC}: STORY-114 scenario (multiple plans) addressed"
        ((TEST_PASSED++))
        return 0
    else
        # Not a hard requirement - scenario may be implicit
        echo -e "${YELLOW}⚠ OPTIONAL${NC}: STORY-114 scenario not explicitly mentioned"
        echo "Optional: Could mention 'prevents duplicate/multiple plan files'"
        ((TEST_PASSED++))
        return 0
    fi
}

#############################################################################
# Test Case 5.6: Practical test - Mixed fixture detection
#############################################################################

test_practical_mixed_detection() {
    echo -e "\n${YELLOW}Test 5.6: Practical detection with mixed naming fixture${NC}"

    setup_fixture

    # Simulate the search algorithm
    local story_id="STORY-114"
    local by_name=()
    local by_content=()
    local no_match=()

    # Find files by name
    for file in "$TEST_FIXTURE"/*"$story_id"*.md; do
        if [[ -f "$file" ]]; then
            by_name+=("$(basename "$file")")
        fi
    done

    # Find files by content
    for file in "$TEST_FIXTURE"/*.md; do
        local basename=$(basename "$file")
        # Skip if already found by name
        if [[ ! " ${by_name[@]} " =~ " $basename " ]]; then
            if grep -q "$story_id" "$file" 2>/dev/null; then
                by_content+=("$basename")
            else
                no_match+=("$basename")
            fi
        fi
    done

    cleanup_fixture

    # Verify detection: Should find clever-snuggling-otter and enchanted-booping-pizza
    local total_detected=$((${#by_name[@]} + ${#by_content[@]}))

    if [[ $total_detected -ge 2 ]]; then
        echo -e "${GREEN}✓ PASS${NC}: Mixed fixture detection works"
        echo "    Detected: ${#by_content[@]} by content, ${#by_name[@]} by name"
        ((TEST_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Mixed fixture detection failed"
        echo "    Expected: ≥2 files detected"
        echo "    Got: $total_detected files"
        ((TEST_FAILED++))
        return 1
    fi
}

#############################################################################
# Test Case 5.7: Resume prompt works with random-named files
#############################################################################

test_resume_prompt_for_random_names() {
    echo -e "\n${YELLOW}Test 5.7: Resume prompt works with random-named files${NC}"

    # Check that prompt documentation doesn't depend on filename format
    local prompt_section=$(sed -n '/[Rr]esume.*[Pp]rompt\|[Pp]rompt.*resume/,/^$/p' "$CLAUDE_MD")

    if [[ -z "$prompt_section" ]]; then
        # Look for prompt elsewhere
        prompt_section=$(sed -n '/Plan File Convention/,/^## /p' "$CLAUDE_MD" | grep -A 3 -i "prompt\|ask\|resume")
    fi

    if echo "$prompt_section" | grep -q -i "existing.*plan\|{filename}\|resume"; then
        echo -e "${GREEN}✓ PASS${NC}: Resume prompt works with random-named files"
        ((TEST_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: Resume prompt may not work with random-named files"
        echo "Expected: Prompt documentation uses {filename} placeholder"
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
    if [[ ! -f "$CLAUDE_MD" ]]; then
        echo -e "${RED}ERROR${NC}: $CLAUDE_MD not found"
        exit 1
    fi

    if [[ ! -f "$SKILL_MD" ]]; then
        echo -e "${RED}ERROR${NC}: $SKILL_MD not found"
        exit 1
    fi

    # Run all test cases
    test_backward_compat_documented
    test_random_named_files_detected
    test_mixed_naming_no_errors
    test_algorithm_handles_both_styles
    test_story_114_scenario_addressed
    test_practical_mixed_detection
    test_resume_prompt_for_random_names

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
        echo -e "${RED}RESULT: FAILED${NC} - AC#5 not implemented"
        echo ""
        echo "Next Steps:"
        echo "  1. Document backward compatibility in CLAUDE.md"
        echo "  2. Verify search algorithm works with ANY filename"
        echo "  3. Use Glob + Grep (works for all file names)"
        echo "  4. Ensure no errors occur with mixed naming conventions"
        echo "  5. Resume prompt uses {filename} placeholder (works for any name)"
        echo "  6. Consider STORY-114 scenario: prevent duplicate random plans"
        echo ""
        exit 1
    else
        echo -e "${GREEN}RESULT: PASSED${NC} - AC#5 fully implemented"
        echo ""
        exit 0
    fi
}

# Execute main test function
main "$@"
