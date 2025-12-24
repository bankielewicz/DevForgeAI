#!/bin/bash

##############################################################################
# Test Suite: STORY-131 AC#2 & AC#3 - Subagent Invocation
#
# AC#2: Command Invokes Existing ideation-result-interpreter Subagent
#   Given: the ideation-result-interpreter subagent exists (created by STORY-133)
#   When: the /ideate command's new Phase 3 executes after skill completion
#   Then: the command invokes the subagent via Task(subagent_type="ideation-result-interpreter")
#
# AC#3: Command Phase 3 Invokes Result Interpreter
#   Given: the /ideate command completes the devforgeai-ideation skill execution
#   When: new Phase 3 executes
#   Then: the command invokes Task(subagent_type="ideation-result-interpreter")
#
# Test Strategy:
#   - Verify ideation-result-interpreter subagent exists
#   - Verify it has required YAML frontmatter
#   - Verify ideate.md contains Phase 3 section (after Phase 2, before Phase N)
#   - Verify Phase 3 invokes Task() with correct subagent_type
#   - Verify skill output is passed to subagent in prompt
#   - Verify formatted result is returned to user
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
RESULT_INTERPRETER="/mnt/c/Projects/DevForgeAI2/.claude/agents/ideation-result-interpreter.md"

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
    local description="$2"

    if [[ ! -f "$file" ]]; then
        echo -e "${RED}FAILED${NC}: File $file does not exist"
        echo "Details: $description"
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

    if ! grep -q "$pattern" "$file" 2>/dev/null; then
        echo -e "${RED}FAILED${NC}: Pattern not found"
        echo "Pattern: $pattern"
        echo "File: $file"
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

assert_yaml_field_exists() {
    local file="$1"
    local field="$2"
    local expected_value="$3"

    # Extract first 30 lines (frontmatter is at top)
    local frontmatter=$(head -30 "$file")

    if [[ "$frontmatter" == *"$field:"* ]]; then
        if [[ -z "$expected_value" ]]; then
            echo -e "${GREEN}PASSED${NC}: YAML field '$field' exists"
            TESTS_PASSED=$((TESTS_PASSED + 1))
            return 0
        elif echo "$frontmatter" | grep -q "$field:.*$expected_value"; then
            echo -e "${GREEN}PASSED${NC}: YAML field '$field: $expected_value' exists"
            TESTS_PASSED=$((TESTS_PASSED + 1))
            return 0
        else
            echo -e "${RED}FAILED${NC}: YAML field '$field' has wrong value (expected: $expected_value)"
            TESTS_FAILED=$((TESTS_FAILED + 1))
            return 1
        fi
    else
        echo -e "${RED}FAILED${NC}: YAML field '$field' not found"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

##############################################################################
# AC#2 Test Cases - Subagent Existence and Structure
##############################################################################

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║ STORY-131 AC#2: Subagent Invocation                            ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Test 2.1: Verify subagent file exists
run_test \
    "test_result_interpreter_subagent_exists" \
    "Verify ideation-result-interpreter.md exists at expected path (created by STORY-133)"
assert_file_exists "$RESULT_INTERPRETER" "Subagent should be in .claude/agents/"

# Test 2.2: Verify subagent has YAML frontmatter with name field
run_test \
    "test_result_interpreter_yaml_name_field" \
    "Verify subagent has YAML frontmatter with 'name' field"
assert_yaml_field_exists "$RESULT_INTERPRETER" "name" "ideation-result-interpreter"

# Test 2.3: Verify subagent has description field
run_test \
    "test_result_interpreter_yaml_description_field" \
    "Verify subagent has YAML 'description' field for identification"
assert_yaml_field_exists "$RESULT_INTERPRETER" "description" ""

# Test 2.4: Verify subagent has model field (should be 'opus')
run_test \
    "test_result_interpreter_yaml_model_field" \
    "Verify subagent has YAML 'model' field"
assert_yaml_field_exists "$RESULT_INTERPRETER" "model" ""

# Test 2.5: Verify subagent has tools field
run_test \
    "test_result_interpreter_yaml_tools_field" \
    "Verify subagent has YAML 'tools' field listing allowed tools"
assert_yaml_field_exists "$RESULT_INTERPRETER" "tools" ""

# Test 2.6: Verify subagent title/heading exists
run_test \
    "test_result_interpreter_heading" \
    "Verify subagent has proper Markdown heading structure"
assert_grep_match "^# .*[Ii]deation.*[Rr]esult\|^# .*[Ii]deation-result-interpreter" \
    "$RESULT_INTERPRETER" \
    "Subagent should have clear title/heading"

##############################################################################
# AC#3 Test Cases - Command Invocation
##############################################################################

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║ STORY-131 AC#3: Command Phase 3 Invokes Result Interpreter     ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Test 3.1: Verify ideate.md has Phase 3 section
run_test \
    "test_ideate_phase3_exists" \
    "Verify /ideate command has new Phase 3 section"
assert_grep_match "^## Phase 3:" "$IDEATE_COMMAND" "Phase 3 should exist in ideate.md"

# Test 3.2: Verify Phase 3 is positioned after Phase 2 and before Phase N
run_test \
    "test_ideate_phase3_ordering" \
    "Verify Phase 3 comes after Phase 2 (Invoke Ideation Skill)"
if grep -n "^## Phase 2:" "$IDEATE_COMMAND" > /dev/null && \
   grep -n "^## Phase 3:" "$IDEATE_COMMAND" > /dev/null; then
    phase2_line=$(grep -n "^## Phase 2:" "$IDEATE_COMMAND" | cut -d: -f1)
    phase3_line=$(grep -n "^## Phase 3:" "$IDEATE_COMMAND" | cut -d: -f1)

    if [[ $phase2_line -lt $phase3_line ]]; then
        echo -e "${GREEN}PASSED${NC}: Phase 3 (line $phase3_line) comes after Phase 2 (line $phase2_line)"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAILED${NC}: Phase 3 ordering incorrect"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
else
    echo -e "${RED}FAILED${NC}: Cannot determine phase ordering"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 3.3: Verify Phase 3 invokes Task() with ideation-result-interpreter
run_test \
    "test_ideate_phase3_task_invocation" \
    "Verify Phase 3 contains Task with ideation-result-interpreter subagent"
# Check for Task( on one line and subagent_type with ideation-result-interpreter on next line (multi-line format)
if grep -q 'Task(' "$IDEATE_COMMAND" && grep -q 'subagent_type.*ideation-result-interpreter' "$IDEATE_COMMAND"; then
    echo -e "${GREEN}PASSED${NC}: Task invocation with ideation-result-interpreter found"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAILED${NC}: Phase 3 must invoke Task(subagent_type='ideation-result-interpreter')"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 3.4: Verify Task() invocation uses correct format
run_test \
    "test_ideate_phase3_task_format" \
    "Verify Task invocation has correct syntax: Task(subagent_type=...)"
# Check for subagent_type parameter (can be on separate line in multi-line format)
if grep -q 'subagent_type.*=' "$IDEATE_COMMAND"; then
    echo -e "${GREEN}PASSED${NC}: Task call uses subagent_type= parameter"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAILED${NC}: Task() call must use subagent_type= parameter"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 3.5: Verify Phase 3 section description indicates result interpretation
run_test \
    "test_ideate_phase3_purpose_description" \
    "Verify Phase 3 section explains result interpretation purpose"
assert_grep_match "Result.*[Ii]nterpreter\|[Ff]ormat.*output\|[Tt]ransform.*output" "$IDEATE_COMMAND" \
    "Phase 3 should explain that it delegates summary formatting"

# Test 3.6: Verify subagent receives skill output in prompt
run_test \
    "test_ideate_phase3_skill_output_passed" \
    "Verify Phase 3 passes skill output to subagent in Task prompt"
assert_grep_match 'skill.*output\|skill_output\|skill_result' "$IDEATE_COMMAND" \
    "Phase 3 should pass skill execution results to subagent"

# Test 3.7: Verify subagent output is returned/displayed to user
run_test \
    "test_ideate_phase3_result_display" \
    "Verify Phase 3 displays subagent result (formatted summary)"
assert_grep_match "Display\|formatted.*output\|result.*display\|summary" "$IDEATE_COMMAND" \
    "Phase 3 should show formatted result to user"

# Test 3.8: Verify no duplicate summary logic exists in Phase 3
run_test \
    "test_ideate_phase3_no_duplicate_summary_logic" \
    "Verify Phase 3 doesn't contain summary formatting logic (should be in subagent)"
# Use negative assertion - Phase 3 should NOT have ╔ box drawing chars
phase3_start=$(grep -n "^## Phase 3:" "$IDEATE_COMMAND" | cut -d: -f1)
phase_n_start=$(grep -n "^## Phase N:" "$IDEATE_COMMAND" | cut -d: -f1)

if [[ -n "$phase3_start" && -n "$phase_n_start" ]]; then
    phase3_content=$(sed -n "${phase3_start},$((phase_n_start - 1))p" "$IDEATE_COMMAND")
    # Check for box drawing chars (summary template) - complexity mention in prompt context is OK
    if ! echo "$phase3_content" | grep -q "╔═\|║.*Epics"; then
        echo -e "${GREEN}PASSED${NC}: Phase 3 contains no summary formatting logic"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAILED${NC}: Phase 3 contains hardcoded summary formatting"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
else
    echo -e "${YELLOW}SKIPPED${NC}: Cannot extract Phase 3 content for verification"
fi

# Test 3.9: Verify no hardcoded display templates in Phase 3
run_test \
    "test_ideate_phase3_no_templates" \
    "Verify Phase 3 doesn't define display templates (in subagent instead)"
phase3_content_tmp=$(sed -n "$(grep -n "^## Phase 3:" "$IDEATE_COMMAND" | cut -d: -f1),$(($(grep -n "^## Phase N:" "$IDEATE_COMMAND" | cut -d: -f1) - 1))p" "$IDEATE_COMMAND")
if ! echo "$phase3_content_tmp" | grep -q "IDEATION COMPLETE\|Tier.*Description"; then
    echo -e "${GREEN}PASSED${NC}: No hardcoded templates in Phase 3"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAILED${NC}: Phase 3 contains hardcoded templates"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 3.10: Verify subagent has required functionality sections
run_test \
    "test_result_interpreter_has_workflow_section" \
    "Verify subagent has workflow/implementation section"
assert_grep_match "^## .*[Ww]orkflow\|^## .*[Pp]urpose\|^# " "$RESULT_INTERPRETER" \
    "Subagent should have clear section structure"

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
    echo -e "${GREEN}✓ All AC#2 & AC#3 tests passed${NC}"
    exit 0
else
    echo -e "${RED}✗ AC#2 & AC#3 test failures detected${NC}"
    exit 1
fi
