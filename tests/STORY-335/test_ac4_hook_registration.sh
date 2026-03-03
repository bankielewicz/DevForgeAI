#!/bin/bash
# Test AC#4: Hook Registration in hooks.yaml
# STORY-335: Add Subagent Size Enforcement Mechanism
#
# Validates:
# - Hook entry exists in devforgeai/config/hooks.yaml
# - Entry has correct name: pre-commit-subagent-size
# - Entry has correct event: pre-commit
# - Entry has correct script path
# - Entry is enabled: true
# - Entry has description about 500-line warning
#
# Expected: FAIL initially (TDD Red phase - entry does not exist yet)

# Note: Not using set -e due to arithmetic operations with (( ))

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
HOOKS_YAML="$PROJECT_ROOT/devforgeai/config/hooks.yaml"
HOOK_NAME="pre-commit-subagent-size"
HOOK_SCRIPT=".claude/hooks/pre-commit-subagent-size.sh"

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

# -----------------------------------------------------------------------------
# Test 1: hooks.yaml file exists
# -----------------------------------------------------------------------------
test_hooks_yaml_exists() {
    local test_name="hooks.yaml file exists"
    if [ -f "$HOOKS_YAML" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "File not found: $HOOKS_YAML"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: hooks.yaml contains hook name
# -----------------------------------------------------------------------------
test_hook_name_present() {
    local test_name="Hook name '$HOOK_NAME' present in hooks.yaml"

    if [ ! -f "$HOOKS_YAML" ]; then
        fail_test "$test_name" "Cannot check - hooks.yaml does not exist"
        return
    fi

    if grep -qE "id:[[:space:]]*['\"]?$HOOK_NAME['\"]?|name:[[:space:]]*['\"]?$HOOK_NAME['\"]?" "$HOOKS_YAML"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Hook name '$HOOK_NAME' not found in hooks.yaml"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: Hook entry has pre-commit event type
# -----------------------------------------------------------------------------
test_hook_event_type() {
    local test_name="Hook has pre-commit event type"

    if [ ! -f "$HOOKS_YAML" ]; then
        fail_test "$test_name" "Cannot check - hooks.yaml does not exist"
        return
    fi

    # Look for event: pre-commit or operation_pattern: pre-commit near the hook entry
    if grep -qE "event:[[:space:]]*['\"]?pre-commit['\"]?" "$HOOKS_YAML" || \
       grep -qE "operation_pattern:[[:space:]]*['\"]?pre-commit['\"]?" "$HOOKS_YAML"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "pre-commit event type not found for hook"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Hook entry has correct script path
# -----------------------------------------------------------------------------
test_hook_script_path() {
    local test_name="Hook has correct script path"

    if [ ! -f "$HOOKS_YAML" ]; then
        fail_test "$test_name" "Cannot check - hooks.yaml does not exist"
        return
    fi

    if grep -qE "script:[[:space:]]*['\"]?\.?/?$HOOK_SCRIPT['\"]?" "$HOOKS_YAML" || \
       grep -qE "script:[[:space:]]*['\"]?\.claude/hooks/pre-commit-subagent-size\.sh['\"]?" "$HOOKS_YAML"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Script path '$HOOK_SCRIPT' not found in hooks.yaml"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: Hook entry is enabled
# -----------------------------------------------------------------------------
test_hook_enabled() {
    local test_name="Hook is enabled (enabled: true)"

    if [ ! -f "$HOOKS_YAML" ]; then
        fail_test "$test_name" "Cannot check - hooks.yaml does not exist"
        return
    fi

    # This is a simple check - in reality we'd need to parse YAML properly
    # to ensure enabled: true is associated with the correct hook
    if grep -qE "enabled:[[:space:]]*true" "$HOOKS_YAML"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No 'enabled: true' found in hooks.yaml"
    fi
}

# -----------------------------------------------------------------------------
# Test 6: Hook entry has description mentioning 500 lines
# -----------------------------------------------------------------------------
test_hook_description() {
    local test_name="Hook has description mentioning 500-line warning"

    if [ ! -f "$HOOKS_YAML" ]; then
        fail_test "$test_name" "Cannot check - hooks.yaml does not exist"
        return
    fi

    # Check for description containing '500' and warning-related text
    if grep -qE "description:.*500.*line|description:.*subagent.*size|description:.*warn" "$HOOKS_YAML"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Description mentioning 500-line warning not found"
    fi
}

# -----------------------------------------------------------------------------
# Test 7: Hook entry has tags array
# -----------------------------------------------------------------------------
test_hook_tags() {
    local test_name="Hook has tags array with relevant tags"

    if [ ! -f "$HOOKS_YAML" ]; then
        fail_test "$test_name" "Cannot check - hooks.yaml does not exist"
        return
    fi

    # Check for tags containing 'subagent' or 'size' or 'enforcement'
    if grep -qE "tags:.*\[.*subagent|tags:.*\[.*size|tags:.*\[.*enforcement" "$HOOKS_YAML"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Tags with relevant keywords not found"
    fi
}

# -----------------------------------------------------------------------------
# Test 8: Hook entry follows existing pattern structure
# -----------------------------------------------------------------------------
test_hook_structure() {
    local test_name="Hook entry follows existing YAML pattern"

    if [ ! -f "$HOOKS_YAML" ]; then
        fail_test "$test_name" "Cannot check - hooks.yaml does not exist"
        return
    fi

    # Check for proper indentation and structure (id or name followed by other fields)
    # This validates the hook entry is properly formatted
    local has_id_or_name=false
    local has_script_or_event=false

    if grep -qE "^[[:space:]]+-[[:space:]]+id:" "$HOOKS_YAML" || \
       grep -qE "^[[:space:]]+-[[:space:]]+name:" "$HOOKS_YAML"; then
        has_id_or_name=true
    fi

    if grep -qE "script:" "$HOOKS_YAML" || grep -qE "event:" "$HOOKS_YAML"; then
        has_script_or_event=true
    fi

    if [ "$has_id_or_name" = true ] && [ "$has_script_or_event" = true ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Hook entry structure does not match expected pattern"
    fi
}

# -----------------------------------------------------------------------------
# Test 9: hooks.yaml is valid YAML (basic syntax check)
# -----------------------------------------------------------------------------
test_valid_yaml_syntax() {
    local test_name="hooks.yaml has valid YAML syntax (basic check)"

    if [ ! -f "$HOOKS_YAML" ]; then
        fail_test "$test_name" "Cannot check - hooks.yaml does not exist"
        return
    fi

    # Basic check: file should not have obvious syntax errors
    # (tabs at start of lines, unclosed brackets, etc.)
    local syntax_errors=""

    # Check for tabs at start of lines (YAML should use spaces)
    if grep -qP "^\t" "$HOOKS_YAML" 2>/dev/null; then
        syntax_errors="tabs at line start"
    fi

    if [ -z "$syntax_errors" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Potential YAML syntax issues: $syntax_errors"
    fi
}

# -----------------------------------------------------------------------------
# Test 10: Hook entry near other pre-commit hooks (if any)
# -----------------------------------------------------------------------------
test_hook_placement() {
    local test_name="hooks.yaml file is not empty and has hooks section"

    if [ ! -f "$HOOKS_YAML" ]; then
        fail_test "$test_name" "Cannot check - hooks.yaml does not exist"
        return
    fi

    # Check that hooks: section exists
    if grep -qE "^hooks:" "$HOOKS_YAML"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No 'hooks:' section found in hooks.yaml"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-335 AC#4: Hook Registration in hooks.yaml"
echo "=============================================="
echo "Target file: $HOOKS_YAML"
echo "Hook name: $HOOK_NAME"
echo "Script path: $HOOK_SCRIPT"
echo "----------------------------------------------"
echo ""

run_test "1" test_hooks_yaml_exists
run_test "2" test_hook_name_present
run_test "3" test_hook_event_type
run_test "4" test_hook_script_path
run_test "5" test_hook_enabled
run_test "6" test_hook_description
run_test "7" test_hook_tags
run_test "8" test_hook_structure
run_test "9" test_valid_yaml_syntax
run_test "10" test_hook_placement

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
