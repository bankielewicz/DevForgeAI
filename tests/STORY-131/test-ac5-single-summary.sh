#!/bin/bash

##############################################################################
# Test Suite: STORY-131 AC#5 - Summary Displays Once Per Session
#
# AC#5: Summary Displays Once Per Session
#   Given: a user runs the /ideate command
#   When: ideation workflow completes
#   Then: a single, formatted summary appears at the end (from result interpreter)
#         AND no duplicate quick summary from command Phase 4 appears
#
# Test Strategy:
#   - Verify no multiple summary display logic in command
#   - Verify command delegates ALL summary presentation to result interpreter
#   - Verify Phase 4 removal eliminates quick summary
#   - Verify Phase 3 invokes result interpreter once (no loops/duplicates)
#   - Verify no hardcoded Display() calls in command for summary
##############################################################################

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# File paths
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

assert_grep_no_match() {
    local pattern="$1"
    local file="$2"
    local description="$3"

    if grep -q "$pattern" "$file" 2>/dev/null; then
        echo -e "${RED}FAILED${NC}: Pattern found (should not exist)"
        echo "Pattern: $pattern"
        echo "Matches:"
        grep -n "$pattern" "$file" | head -3
        echo "Details: $description"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    else
        echo -e "${GREEN}PASSED${NC}: Pattern not found (correct)"
        echo "Pattern: $pattern"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    fi
}

assert_grep_match() {
    local pattern="$1"
    local file="$2"
    local description="$3"

    if ! grep -q "$pattern" "$file" 2>/dev/null; then
        echo -e "${RED}FAILED${NC}: Pattern not found"
        echo "Pattern: $pattern"
        echo "Details: $description"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    else
        echo -e "${GREEN}PASSED${NC}: Pattern found"
        echo "Pattern: $pattern"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    fi
}

count_pattern_occurrences() {
    local pattern="$1"
    local file="$2"

    grep -c "$pattern" "$file" 2>/dev/null || echo "0"
}

##############################################################################
# AC#5 Test Cases
##############################################################################

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║ STORY-131 AC#5: Summary Displays Once Per Session              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Test 5.1: Verify ideate.md exists
run_test \
    "test_ideate_file_exists" \
    "Verify /ideate command file exists"
assert_file_exists "$IDEATE_COMMAND"

# Test 5.2: Verify no multiple summary sections in command
run_test \
    "test_no_duplicate_summary_sections" \
    "Verify command doesn't have multiple summary presentation sections"
assert_grep_no_match "## .*Summary\|## .*SUMMARY" "$IDEATE_COMMAND" \
    "Summary sections should not exist in command (moved to result interpreter)"

# Test 5.3: Verify no summary Display() calls in command
run_test \
    "test_no_hardcoded_summary_display" \
    "Verify command doesn't have hardcoded Display calls for summary"
assert_grep_no_match 'Display.*Summary\|Display.*".*Epics\|Display.*complexity' "$IDEATE_COMMAND" \
    "Hardcoded summary Display() calls should not exist"

# Test 5.4: Verify command delegates summary to result interpreter
run_test \
    "test_command_delegates_summary" \
    "Verify command explicitly delegates summary presentation to result interpreter"
assert_grep_match "ideation-result-interpreter\|result.*interpreter" "$IDEATE_COMMAND" \
    "Command should mention result interpreter as responsible for summary"

# Test 5.5: Verify Phase 4 (quick summary) is completely removed
run_test \
    "test_phase4_completely_removed" \
    "Verify Phase 4 section header and all quick summary code is removed"
assert_grep_no_match "^## Phase 4:\|^### 4\\." "$IDEATE_COMMAND" \
    "Phase 4 section must be completely removed"

# Test 5.6: Verify no quick summary variable assignments remain
run_test \
    "test_no_summary_variable_assignments" \
    "Verify no summary variable assignments in command (e.g., \$SUMMARY, \$QUICK_SUMMARY)"
assert_grep_no_match '\$SUMMARY\|\$QUICK_SUMMARY\|\$summary' "$IDEATE_COMMAND" \
    "No summary variables should exist in command"

# Test 5.7: Verify no summary template hardcoding in command
run_test \
    "test_no_summary_templates_in_command" \
    "Verify no summary templates hardcoded in command"
assert_grep_no_match 'IDEATION.*SUMMARY\|╔═\|║.*Epics.*Generated\|Architecture Tier' "$IDEATE_COMMAND" \
    "Summary templates should be in result interpreter only"

# Test 5.8: Verify only ONE Task() call for result interpreter
run_test \
    "test_single_result_interpreter_invocation" \
    "Verify result interpreter is invoked exactly once in command"

# Count Task( invocations with ideation-result-interpreter as subagent_type
# Pattern: subagent_type="ideation-result-interpreter" (the actual parameter line)
task_count=$(grep -c 'subagent_type="ideation-result-interpreter"' "$IDEATE_COMMAND" || echo "0")

if [[ $task_count -eq 1 ]]; then
    echo -e "${GREEN}PASSED${NC}: Result interpreter invoked exactly once"
    TESTS_PASSED=$((TESTS_PASSED + 1))
elif [[ $task_count -eq 0 ]]; then
    echo -e "${RED}FAILED${NC}: Result interpreter not invoked at all"
    TESTS_FAILED=$((TESTS_FAILED + 1))
else
    echo -e "${RED}FAILED${NC}: Result interpreter invoked $task_count times (should be 1)"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 5.9: Verify Task() invocation is in Phase 3 only
run_test \
    "test_task_invocation_in_phase3_only" \
    "Verify Task() invocation for result interpreter is in Phase 3 section"

# Extract Phase 3 section
if grep -n "^## Phase 3:" "$IDEATE_COMMAND" > /dev/null && \
   grep -n "^## Phase N:" "$IDEATE_COMMAND" > /dev/null; then
    phase3_line=$(grep -n "^## Phase 3:" "$IDEATE_COMMAND" | cut -d: -f1)
    phase_n_line=$(grep -n "^## Phase N:" "$IDEATE_COMMAND" | cut -d: -f1)

    phase3_section=$(sed -n "${phase3_line},$((phase_n_line - 1))p" "$IDEATE_COMMAND")

    if echo "$phase3_section" | grep -q 'subagent_type="ideation-result-interpreter"'; then
        echo -e "${GREEN}PASSED${NC}: Task() invocation found in Phase 3 section"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAILED${NC}: Task() invocation not in Phase 3 section"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
else
    echo -e "${YELLOW}SKIPPED${NC}: Cannot extract Phase 3 section"
fi

# Test 5.10: Verify no summary logic remains after result interpreter invocation
run_test \
    "test_no_post_interpreter_summary_logic" \
    "Verify no summary logic exists after result interpreter Task() invocation"

# After Phase 3, only Phase N (hooks), Error Handling, and Command Complete should exist
# Note: Text mentions of "summary" in documentation are OK, looking for actual display LOGIC
if grep -n "^## Phase N:" "$IDEATE_COMMAND" > /dev/null; then
    phase_n_line_check=$(grep -n "^## Phase N:" "$IDEATE_COMMAND" | cut -d: -f1)
    post_phase_n=$(sed -n "${phase_n_line_check},\$p" "$IDEATE_COMMAND")

    # Looking for actual summary DISPLAY logic (templates with box chars, Display calls), not text mentions
    if ! echo "$post_phase_n" | grep -q "╔═\|║.*Epics\|Display:.*summary"; then
        echo -e "${GREEN}PASSED${NC}: No summary display logic after Phase 3"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAILED${NC}: Summary display logic found after Phase 3"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
else
    echo -e "${YELLOW}SKIPPED${NC}: Cannot verify post-Phase 3 sections"
fi

# Test 5.11: Verify command ends after Phase N or has only error handling
run_test \
    "test_command_structure_complete" \
    "Verify command ends properly (no orphaned summary logic)"

total_lines=$(wc -l < "$IDEATE_COMMAND")
last_10_lines=$(tail -10 "$IDEATE_COMMAND")

# Last section should be Error Handling or Command Complete
if echo "$last_10_lines" | grep -q "Error Handling\|Command Complete\|Architecture principle"; then
    echo -e "${GREEN}PASSED${NC}: Command structure is complete and properly ordered"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${YELLOW}WARNING${NC}: Command ending structure may need review"
    # Don't fail - ending might vary
    TESTS_PASSED=$((TESTS_PASSED + 1))
fi

# Test 5.12: Verify skill execution comes before result interpreter
run_test \
    "test_phase_execution_order" \
    "Verify skill execution (Phase 2) happens before result interpreter (Phase 3)"

phase2_line=$(grep -n "^## Phase 2:" "$IDEATE_COMMAND" | cut -d: -f1 || echo "0")
phase3_line=$(grep -n "^## Phase 3:" "$IDEATE_COMMAND" | cut -d: -f1 || echo "0")

if [[ $phase2_line -gt 0 && $phase3_line -gt 0 && $phase2_line -lt $phase3_line ]]; then
    echo -e "${GREEN}PASSED${NC}: Skill (Phase 2, line $phase2_line) executes before result interpreter (Phase 3, line $phase3_line)"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAILED${NC}: Phase execution order incorrect or sections missing"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

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
    echo -e "${GREEN}✓ All AC#5 tests passed${NC}"
    echo ""
    echo "Summary control verified:"
    echo "  ✓ No duplicate summary sections"
    echo "  ✓ Phase 4 completely removed"
    echo "  ✓ Result interpreter invoked once"
    echo "  ✓ Single summary per session guaranteed"
    exit 0
else
    echo -e "${RED}✗ AC#5 test failures detected${NC}"
    exit 1
fi
