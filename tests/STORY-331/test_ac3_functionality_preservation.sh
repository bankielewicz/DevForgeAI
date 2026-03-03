#!/bin/bash
# Test AC#3: Functionality Preservation (No Regression)
# STORY-331: Refactor agent-generator.md with Progressive Disclosure
#
# Validates that all original functionality is preserved in core + references:
# - Batch generation mode (generate all subagents)
# - Single subagent generation mode
# - Priority tier generation mode (Critical, High, Medium, Low)
# - Regenerate existing mode
# - YAML validation workflow
# - System prompt generation workflow
# - Framework validation (DevForgeAI + Claude Code patterns)
# - Reference file generation (Step 4.5)
# - Summary report generation
#
# Expected: FAIL initially (TDD Red phase - functionality not yet preserved in new structure)

# Note: Not using set -e due to arithmetic operations with (( ))

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
CORE_FILE="$PROJECT_ROOT/src/claude/agents/agent-generator.md"
REF_DIR="$PROJECT_ROOT/src/claude/agents/agent-generator/references"

# Test tracking
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test helper functions
pass_test() {
    local test_name="$1"
    TESTS_PASSED=$((TESTS_PASSED + 1))
    echo "[PASS] $test_name"
}

fail_test() {
    local test_name="$1"
    local message="$2"
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo "[FAIL] $test_name: $message"
}

run_test() {
    local test_name="$1"
    TESTS_RUN=$((TESTS_RUN + 1))
    shift
    "$@"
}

# Helper: Search in core file and all reference files
search_all_files() {
    local pattern="$1"

    if [ -f "$CORE_FILE" ]; then
        if grep -lqE "$pattern" "$CORE_FILE" 2>/dev/null; then
            return 0
        fi
    fi

    if [ -d "$REF_DIR" ]; then
        if find "$REF_DIR" -name "*.md" -exec grep -lqE "$pattern" {} \; 2>/dev/null | head -n 1 | grep -q .; then
            return 0
        fi
    fi

    return 1
}

# -----------------------------------------------------------------------------
# Test 1: Batch generation mode documented
# -----------------------------------------------------------------------------
test_batch_generation_mode() {
    local test_name="Batch generation mode (generate all) documented"

    if search_all_files "(Generate All|batch.*(mode|generation)|all.*subagents)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No documentation for batch generation mode found"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: Single subagent generation mode documented
# -----------------------------------------------------------------------------
test_single_generation_mode() {
    local test_name="Single subagent generation mode documented"

    if search_all_files "(Generate Specific|single.*subagent|specific.*subagent)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No documentation for single subagent generation found"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: Priority tier generation mode documented
# -----------------------------------------------------------------------------
test_priority_tier_mode() {
    local test_name="Priority tier generation mode documented"

    if search_all_files "(priority.*tier|Generate.*Priority|Critical.*High.*Medium)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No documentation for priority tier generation found"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Regenerate existing mode documented
# -----------------------------------------------------------------------------
test_regenerate_mode() {
    local test_name="Regenerate existing mode documented"

    if search_all_files "(Regenerate|regenerate.*existing|update.*requirements)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No documentation for regenerate mode found"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: YAML validation workflow documented
# -----------------------------------------------------------------------------
test_yaml_validation() {
    local test_name="YAML validation workflow documented"

    if search_all_files "(YAML.*[Vv]alidat|frontmatter.*valid|validate.*YAML)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No YAML validation workflow found"
    fi
}

# -----------------------------------------------------------------------------
# Test 6: System prompt generation documented
# -----------------------------------------------------------------------------
test_system_prompt_generation() {
    local test_name="System prompt generation workflow documented"

    if search_all_files "(system.*prompt.*generat|Generate.*System.*Prompt|prompt.*structure)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No system prompt generation workflow found"
    fi
}

# -----------------------------------------------------------------------------
# Test 7: DevForgeAI framework validation documented
# -----------------------------------------------------------------------------
test_devforgeai_validation() {
    local test_name="DevForgeAI framework validation documented"

    if search_all_files "(DevForgeAI.*[Vv]alidat|Framework.*[Cc]ompliance|context.*file.*aware)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No DevForgeAI framework validation found"
    fi
}

# -----------------------------------------------------------------------------
# Test 8: Claude Code patterns documented
# -----------------------------------------------------------------------------
test_claude_code_patterns() {
    local test_name="Claude Code patterns documented"

    if search_all_files "(Claude.*Code.*[Pp]attern|CLAUDE_CODE_PATTERNS|official.*pattern)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No Claude Code patterns documentation found"
    fi
}

# -----------------------------------------------------------------------------
# Test 9: Reference file generation (Step 4.5) documented
# -----------------------------------------------------------------------------
test_reference_file_generation() {
    local test_name="Reference file generation (Step 4.5) documented"

    if search_all_files "(Step 4\.5|Generate.*[Rr]eference.*[Ff]ile|reference.*file.*generat)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No reference file generation workflow found"
    fi
}

# -----------------------------------------------------------------------------
# Test 10: Summary report generation documented
# -----------------------------------------------------------------------------
test_summary_report() {
    local test_name="Summary report generation documented"

    if search_all_files "(Summary.*[Rr]eport|Generate.*Summary|report.*generat)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No summary report generation found"
    fi
}

# -----------------------------------------------------------------------------
# Test 11: Tool selection logic documented
# -----------------------------------------------------------------------------
test_tool_selection() {
    local test_name="Tool selection logic documented"

    if search_all_files "(Tool.*[Ss]election|tools.*field|principle.*least.*privilege)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No tool selection logic found"
    fi
}

# -----------------------------------------------------------------------------
# Test 12: Model selection logic documented
# -----------------------------------------------------------------------------
test_model_selection() {
    local test_name="Model selection logic documented"

    if search_all_files "(Model.*[Ss]election|haiku|sonnet|opus|model.*field)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No model selection logic found"
    fi
}

# -----------------------------------------------------------------------------
# Test 13: Phase 0 reference loading documented
# -----------------------------------------------------------------------------
test_phase_0_loading() {
    local test_name="Phase 0 reference loading documented"

    if search_all_files "(Phase 0|Load.*Framework.*Reference|framework.*context.*load)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No Phase 0 reference loading found"
    fi
}

# -----------------------------------------------------------------------------
# Test 14: Slash command refactoring section documented
# -----------------------------------------------------------------------------
test_slash_command_refactoring() {
    local test_name="Slash command refactoring section documented"

    if search_all_files "(Slash.*[Cc]ommand.*[Rr]efactor|command.*refactor|lean.*orchestration)"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No slash command refactoring documentation found"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-331 AC#3: Functionality Preservation"
echo "=============================================="
echo "Core file: $CORE_FILE"
echo "Reference directory: $REF_DIR"
echo "----------------------------------------------"
echo ""

run_test "1" test_batch_generation_mode
run_test "2" test_single_generation_mode
run_test "3" test_priority_tier_mode
run_test "4" test_regenerate_mode
run_test "5" test_yaml_validation
run_test "6" test_system_prompt_generation
run_test "7" test_devforgeai_validation
run_test "8" test_claude_code_patterns
run_test "9" test_reference_file_generation
run_test "10" test_summary_report
run_test "11" test_tool_selection
run_test "12" test_model_selection
run_test "13" test_phase_0_loading
run_test "14" test_slash_command_refactoring

echo ""
echo "=============================================="
echo "Test Summary: $TESTS_PASSED/$TESTS_RUN passed"
echo "=============================================="

if [ "$TESTS_FAILED" -gt 0 ]; then
    echo "Status: FAILED ($TESTS_FAILED failures)"
    exit 1
else
    echo "Status: PASSED"
    exit 0
fi
