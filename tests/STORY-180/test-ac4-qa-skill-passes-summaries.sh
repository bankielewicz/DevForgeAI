#!/bin/bash
# =============================================================================
# STORY-180 AC-4: QA Skill Passes Summaries
# =============================================================================
# Tests that verify the QA skill's parallel-validation.md passes context
# summaries to validators during deep validation.
#
# Expected to FAIL initially (TDD Red Phase):
#   - parallel-validation.md doesn't include context summary passing
#   - Task invocations don't include summary parameter
#
# Run: bash tests/STORY-180/test-ac4-qa-skill-passes-summaries.sh
# =============================================================================

set -uo pipefail

# Disable pipefail for grep pipelines (grep -q causes SIGPIPE with pipefail)
run_grep_pipeline() {
    set +o pipefail
    "$@"
    local result=$?
    set -o pipefail
    return $result
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
pass() {
    echo -e "${GREEN}PASS${NC}: $1"
    ((TESTS_PASSED++))
    ((TESTS_RUN++))
}

fail() {
    echo -e "${RED}FAIL${NC}: $1"
    echo "       Expected: $2"
    echo "       Actual: ${3:-'(not found)'}"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

# Target file
TARGET_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-qa/references/parallel-validation.md"

# =============================================================================
# Test 1: Context Summary section exists in parallel-validation.md
# =============================================================================
test_context_summary_section_exists() {
    local test_name="Context Summary section exists in parallel-validation.md"

    if grep -qiE '^##.*Context Summar|^###.*Context Summar' "$TARGET_FILE" 2>/dev/null; then
        pass "$test_name"
    else
        fail "$test_name" \
             "Section header '## Context Summary' or '### Context Summary'" \
             "Section not found"
    fi
}

# =============================================================================
# Test 2: Task invocations include context_summary parameter
# =============================================================================
test_task_includes_context_summary_param() {
    local test_name="Task invocations include context_summary in prompt"

    # Look for Task calls with context summary in the prompt
    if grep -B5 -A20 'Task(' "$TARGET_FILE" 2>/dev/null | \
       grep -qiE 'context.*summar|summar.*context'; then
        pass "$test_name"
    else
        fail "$test_name" \
             "Task invocations with context_summary in prompt" \
             "context_summary not found in Task calls"
    fi
}

# =============================================================================
# Test 3: Summary passed to test-automator
# =============================================================================
test_summary_passed_to_test_automator() {
    local test_name="Context summary passed to test-automator subagent"

    if run_grep_pipeline bash -c "grep -B10 -A30 'test-automator' '$TARGET_FILE' 2>/dev/null | grep -qiE 'context.*summar|summar'"; then
        pass "$test_name"
    else
        fail "$test_name" \
             "test-automator invocation includes context summary" \
             "Summary not found in test-automator section"
    fi
}

# =============================================================================
# Test 4: Summary passed to code-reviewer
# =============================================================================
test_summary_passed_to_code_reviewer() {
    local test_name="Context summary passed to code-reviewer subagent"

    if run_grep_pipeline bash -c "grep -B10 -A30 'code-reviewer' '$TARGET_FILE' 2>/dev/null | grep -qiE 'context.*summar|summar'"; then
        pass "$test_name"
    else
        fail "$test_name" \
             "code-reviewer invocation includes context summary" \
             "Summary not found in code-reviewer section"
    fi
}

# =============================================================================
# Test 5: Summary passed to security-auditor
# =============================================================================
test_summary_passed_to_security_auditor() {
    local test_name="Context summary passed to security-auditor subagent"

    if run_grep_pipeline bash -c "grep -B10 -A30 'security-auditor' '$TARGET_FILE' 2>/dev/null | grep -qiE 'context.*summar|summar'"; then
        pass "$test_name"
    else
        fail "$test_name" \
             "security-auditor invocation includes context summary" \
             "Summary not found in security-auditor section"
    fi
}

# =============================================================================
# Test 6: Summary generation step documented before Task invocations
# =============================================================================
test_summary_generation_step() {
    local test_name="Summary generation step documented before Task invocations"

    # Look for a step that generates/prepares the summary
    if grep -qiE 'generat.*summar|prepar.*summar|creat.*summar|build.*summar' "$TARGET_FILE" 2>/dev/null; then
        pass "$test_name"
    else
        fail "$test_name" \
             "Step: 'Generate context summary' or 'Prepare context summary'" \
             "Summary generation step not documented"
    fi
}

# =============================================================================
# Test 7: Format matches story specification
# =============================================================================
test_format_matches_story_spec() {
    local test_name="Summary format matches story specification template"

    # Check for the exact template from the story
    if grep -q 'Context Summary (do not re-read files)' "$TARGET_FILE" 2>/dev/null; then
        pass "$test_name"
    else
        fail "$test_name" \
             "Template: '**Context Summary (do not re-read files):**'" \
             "Story-specified template not found"
    fi
}

# =============================================================================
# Test 8: Parallel invocation includes summary in all 3 tasks
# =============================================================================
test_parallel_invocation_all_three() {
    local test_name="All 3 parallel Task invocations include summary"

    # Count occurrences of summary in Task context
    local task_section
    task_section=$(grep -A50 'Single Message with 3 Task\|Parallel Invocation Pattern' "$TARGET_FILE" 2>/dev/null || echo "")

    if [ -n "$task_section" ]; then
        local summary_count
        summary_count=$(echo "$task_section" | grep -ciE 'context.*summar|summar' 2>/dev/null | head -1 || echo "0")
        # Ensure numeric value
        summary_count=${summary_count:-0}

        if [[ "$summary_count" =~ ^[0-9]+$ ]] && [ "$summary_count" -ge 3 ]; then
            pass "$test_name"
        else
            fail "$test_name" \
                 "3 occurrences of context_summary in parallel Task invocations" \
                 "$summary_count occurrences found"
        fi
    else
        fail "$test_name" \
             "Parallel invocation section with 3 summary usages" \
             "Parallel invocation section not found"
    fi
}

# =============================================================================
# Run all tests
# =============================================================================
echo "========================================================================"
echo "STORY-180 AC-4: QA Skill Passes Summaries"
echo "========================================================================"
echo ""

test_context_summary_section_exists
test_task_includes_context_summary_param
test_summary_passed_to_test_automator
test_summary_passed_to_code_reviewer
test_summary_passed_to_security_auditor
test_summary_generation_step
test_format_matches_story_spec
test_parallel_invocation_all_three

echo ""
echo "========================================================================"
echo "Test Results: $TESTS_PASSED/$TESTS_RUN passed, $TESTS_FAILED failed"
echo "========================================================================"

# Exit with failure if any tests failed (TDD Red expected)
if [[ $TESTS_FAILED -gt 0 ]]; then
    echo -e "${YELLOW}NOTE: Failures expected in TDD Red phase${NC}"
    exit 1
fi

exit 0
