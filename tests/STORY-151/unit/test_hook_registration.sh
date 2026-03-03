#!/usr/bin/env bash

# STORY-151: Post-Subagent Recording Hook - Hook Registration Tests (AC#1)
# Tests that hook is properly registered in hooks.yaml with correct configuration

set -euo pipefail

# Setup
readonly TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "${TEST_DIR}/../../../" && pwd)"
readonly HOOKS_YAML="${PROJECT_ROOT}/.claude/hooks.yaml"

# Color codes for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m' # No Color

# Test counters
tests_run=0
tests_passed=0
tests_failed=0

# Test helper functions
run_test() {
    local test_name="$1"
    local test_func="$2"

    echo -e "\n${YELLOW}Running: ${test_name}${NC}"
    tests_run=$((tests_run + 1))

    if $test_func; then
        echo -e "${GREEN}✓ PASSED${NC}"
        tests_passed=$((tests_passed + 1))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC}"
        tests_failed=$((tests_failed + 1))
        return 1
    fi
}

assert_file_exists() {
    local file="$1"
    local message="${2:-File not found: $file}"

    if [[ ! -f "$file" ]]; then
        echo "  Error: $message"
        return 1
    fi
    return 0
}

assert_contains() {
    local file="$1"
    local pattern="$2"
    local message="${3:-Pattern not found in file}"

    if ! grep -q "$pattern" "$file"; then
        echo "  Error: $message"
        echo "  File: $file"
        echo "  Pattern: $pattern"
        return 1
    fi
    return 0
}

assert_yaml_has_key() {
    local file="$1"
    local key="$2"
    local message="${3:-YAML key not found}"

    if ! grep -E "^\s*$key:" "$file" > /dev/null; then
        echo "  Error: $message"
        echo "  File: $file"
        echo "  Key: $key"
        return 1
    fi
    return 0
}

# TEST AC#1.1: Hook registration file exists
test_hooks_yaml_exists() {
    assert_file_exists "$HOOKS_YAML" "hooks.yaml not found at $HOOKS_YAML"
}

# TEST AC#1.2: post-subagent-recording hook is registered under post_tool_call event
test_hook_registered_under_post_tool_call() {
    local error_msg=""

    # Check that post_tool_call event exists
    if ! assert_contains "$HOOKS_YAML" "^[[:space:]]*post_tool_call:" "post_tool_call event not found"; then
        return 1
    fi

    # Check that post-subagent-recording hook exists under post_tool_call
    if ! assert_contains "$HOOKS_YAML" "post-subagent-recording" "post-subagent-recording hook not registered"; then
        return 1
    fi

    return 0
}

# TEST AC#1.3: Hook script path is correct
test_hook_script_path_correct() {
    local expected_script="devforgeai/hooks/post-subagent-recording.sh"

    if ! assert_contains "$HOOKS_YAML" "script:.*$expected_script" "Script path not correct"; then
        echo "  Expected script path: $expected_script"
        echo "  Current hooks.yaml content (relevant lines):"
        grep -A 5 "post-subagent-recording" "$HOOKS_YAML" || echo "    (no hook found)"
        return 1
    fi

    return 0
}

# TEST AC#1.4: Hook has blocking: false (non-blocking)
test_hook_blocking_flag_false() {
    # Find the post-subagent-recording hook section and verify blocking: false
    local hook_section=""

    # Extract hook section (from post-subagent-recording to next hook or end)
    if ! grep -A 10 "post-subagent-recording" "$HOOKS_YAML" | grep -q "blocking: false"; then
        echo "  Error: Hook blocking flag is not set to false"
        echo "  Hook configuration (from hooks.yaml):"
        grep -A 10 "post-subagent-recording" "$HOOKS_YAML" || echo "    (no hook found)"
        return 1
    fi

    return 0
}

# TEST AC#1.5: Hook has filter matching Task tool calls with subagent_type
test_hook_filter_matches_task_tool() {
    # Verify filter section exists
    if ! grep -A 15 "post-subagent-recording" "$HOOKS_YAML" | grep -q "filter:"; then
        echo "  Error: Filter section not found in hook configuration"
        return 1
    fi

    # Verify filter checks for Task tool
    if ! grep -A 15 "post-subagent-recording" "$HOOKS_YAML" | grep -q "tool:.*Task"; then
        echo "  Error: Filter does not match Task tool"
        echo "  Hook configuration:"
        grep -A 15 "post-subagent-recording" "$HOOKS_YAML" || echo "    (no hook found)"
        return 1
    fi

    return 0
}

# TEST AC#1.6: Hook filter includes subagent_type parameter requirement
test_hook_filter_requires_subagent_type_param() {
    # Check if filter references subagent_type parameter
    if ! grep -A 15 "post-subagent-recording" "$HOOKS_YAML" | grep -qE "(subagent|has_param.*subagent)"; then
        echo "  Error: Filter does not check for subagent_type parameter"
        echo "  Hook configuration:"
        grep -A 15 "post-subagent-recording" "$HOOKS_YAML" || echo "    (no hook found)"
        return 1
    fi

    return 0
}

# TEST AC#1.7: hooks.yaml is valid YAML format
test_hooks_yaml_valid_format() {
    if ! command -v python3 &> /dev/null; then
        echo "  Skipping YAML validation (python3 not available)"
        return 0
    fi

    if ! python3 -c "import yaml; yaml.safe_load(open('$HOOKS_YAML'))" 2>/dev/null; then
        echo "  Error: hooks.yaml has invalid YAML syntax"
        return 1
    fi

    return 0
}

# TEST AC#1.8: Event name matches post_tool_call (case-sensitive)
test_event_name_post_tool_call_case_sensitive() {
    if ! grep "^[[:space:]]*post_tool_call:" "$HOOKS_YAML" > /dev/null; then
        echo "  Error: Event should be 'post_tool_call' (lowercase, with underscore)"
        echo "  Found events:"
        grep "^[[:space:]]*[a-z_]*:" "$HOOKS_YAML" || echo "    (no events found)"
        return 1
    fi

    return 0
}

# TEST AC#1.9: Hook name is post-subagent-recording (case-sensitive with hyphens)
test_hook_name_format_correct() {
    if ! grep -q "name:.*post-subagent-recording" "$HOOKS_YAML"; then
        echo "  Error: Hook name should be 'post-subagent-recording' (lowercase, with hyphens)"
        grep "name:" "$HOOKS_YAML" || echo "    (no name found)"
        return 1
    fi

    return 0
}

# TEST AC#1.10: Multiple hook entries can coexist under post_tool_call
test_multiple_hooks_can_coexist() {
    # This is a structural test - post_tool_call can have multiple hooks
    # Verify the hooks.yaml structure allows this

    if ! grep -A 20 "post_tool_call:" "$HOOKS_YAML" | grep -q "hooks:"; then
        echo "  Error: hooks.yaml should support multiple hooks under post_tool_call"
        return 1
    fi

    return 0
}

# MAIN - Run all tests
echo "========================================="
echo "STORY-151: Hook Registration Tests (AC#1)"
echo "========================================="

run_test "hooks.yaml exists" test_hooks_yaml_exists
run_test "hook registered under post_tool_call event" test_hook_registered_under_post_tool_call
run_test "hook script path is correct" test_hook_script_path_correct
run_test "hook blocking flag is false" test_hook_blocking_flag_false
run_test "hook filter matches Task tool" test_hook_filter_matches_task_tool
run_test "hook filter requires subagent_type parameter" test_hook_filter_requires_subagent_type_param
run_test "hooks.yaml has valid YAML format" test_hooks_yaml_valid_format
run_test "event name is post_tool_call (case-sensitive)" test_event_name_post_tool_call_case_sensitive
run_test "hook name is post-subagent-recording" test_hook_name_format_correct
run_test "multiple hooks can coexist under post_tool_call" test_multiple_hooks_can_coexist

# Print summary
echo ""
echo "========================================="
echo "Test Summary"
echo "========================================="
echo "Total: $tests_run"
echo "Passed: $tests_passed"
echo "Failed: $tests_failed"
echo "========================================="

exit $tests_failed
