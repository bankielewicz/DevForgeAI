#!/bin/bash

##############################################################################
# Test Suite: STORY-131 AC#1 - Phase 4 Removal Preserves Functionality
#
# AC#1: Phase 4 Removal Preserves Functionality
#   Given: the current /ideate command with Phase 4 (quick summary presentation)
#   When: Phase 4 code is removed from the command
#   Then: all summary presentation logic is removed AND no functional gaps exist
#
# Test Strategy:
#   - Verify Phase 4 section doesn't exist in ideate.md
#   - Verify no "Phase 4" headers remain
#   - Verify no summary presentation logic present
#   - Verify Grep searches confirm removal
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
IDEATE_COMMAND="/mnt/c/Projects/DevForgeAI2/.claude/commands/ideate.md"

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

assert_grep_no_match() {
    local pattern="$1"
    local file="$2"
    local test_name="$3"

    if grep -q "$pattern" "$file" 2>/dev/null; then
        echo -e "${RED}FAILED${NC}: Pattern '$pattern' found in $file"
        echo "Matches:"
        grep -n "$pattern" "$file" | head -5
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    else
        echo -e "${GREEN}PASSED${NC}: Pattern '$pattern' not found (correct)"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    fi
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

##############################################################################
# AC#1 Test Cases
##############################################################################

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║ STORY-131 AC#1: Phase 4 Removal Preserves Functionality       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Test 1.1: Verify ideate.md exists
run_test \
    "test_ideate_command_exists" \
    "Verify /ideate command file exists at expected path"
assert_file_exists "$IDEATE_COMMAND"

# Test 1.2: Verify Phase 4 header is not present
run_test \
    "test_phase4_header_removed" \
    "Verify '## Phase 4' header does not exist in ideate.md"
assert_grep_no_match "^## Phase 4" "$IDEATE_COMMAND" "Phase 4 header should not exist"

# Test 1.3: Verify 'Quick Summary' text is removed
run_test \
    "test_quick_summary_text_removed" \
    "Verify 'Quick Summary' presentation logic not present"
assert_grep_no_match "Quick Summary" "$IDEATE_COMMAND" "Quick Summary section should be removed"

# Test 1.4: Verify summary presentation logic removed
run_test \
    "test_summary_presentation_logic_removed" \
    "Verify summary presentation template logic not present (Display with summary box)"
assert_grep_no_match "IDEATION SUMMARY" "$IDEATE_COMMAND" "Summary presentation display should be removed"

# Test 1.5: Verify no hardcoded summary box characters
run_test \
    "test_summary_box_characters_removed" \
    "Verify no ASCII box drawing characters for summary display"
# This test looks for patterns like ╔═══╗ which are used in summary boxes
assert_grep_no_match "╔═" "$IDEATE_COMMAND" "Summary box characters should not exist"

# Test 1.6: Verify no Epic count DISPLAY template remains (Task prompt context references OK)
run_test \
    "test_epic_count_display_removed" \
    "Verify Epic count display TEMPLATE not in command (Task prompt context OK)"
# Looking for display templates like "Epics Generated:" not just mentions
assert_grep_no_match "Epics Generated:\|Epic count:\|║.*[Ee]pic" "$IDEATE_COMMAND" "Epic count display template should be removed"

# Test 1.7: Verify no complexity score DISPLAY template remains (Task prompt context references OK)
run_test \
    "test_complexity_score_display_removed" \
    "Verify complexity score TEMPLATE not in command (Task prompt context OK)"
# Looking for display templates like "Complexity Score:" not mentions in Task prompts
assert_grep_no_match "Complexity Score:\|Score:.*[0-9]/60\|║.*[Cc]omplexity" "$IDEATE_COMMAND" "Complexity score template should be removed"

# Test 1.8: Verify no architecture tier DISPLAY template remains
run_test \
    "test_architecture_tier_display_removed" \
    "Verify architecture tier TEMPLATE not in command"
# Looking for display templates like "Architecture Tier:" not mentions in Task prompts
assert_grep_no_match "Architecture Tier:\|║.*Tier\|Tier [0-9]:" "$IDEATE_COMMAND" "Tier template should be removed"

# Test 1.9: Verify no 'Next Steps' presentation TEMPLATE remains
run_test \
    "test_next_steps_presentation_removed" \
    "Verify Next Steps presentation TEMPLATE not in command"
# Looking for "Next Steps:" display header, not code comments
assert_grep_no_match "^Next Steps:\|║.*Next Steps" "$IDEATE_COMMAND" "Next Steps template should be removed"

# Test 1.10: Verify no greenfield/brownfield recommendation TEMPLATE remains
run_test \
    "test_greenfield_brownfield_recommendations_removed" \
    "Verify greenfield/brownfield recommendation TEMPLATE not in Phase 4"
# Looking for hardcoded templates, not contextual references
assert_grep_no_match "Run /create-context for greenfield\|Run /orchestrate for brownfield" "$IDEATE_COMMAND" "Recommendation templates should be in result interpreter"

##############################################################################
# Summary Report
##############################################################################

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "Test Summary Report"
echo "════════════════════════════════════════════════════════════════"
echo "Total Tests Run:    $TESTS_RUN"
echo -e "Tests Passed:       ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed:       ${RED}$TESTS_FAILED${NC}"
echo "════════════════════════════════════════════════════════════════"

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}✓ All AC#1 tests passed${NC}"
    exit 0
else
    echo -e "${RED}✗ AC#1 test failures detected${NC}"
    exit 1
fi
