#!/bin/bash
# Test: AC#6 - Hook Configuration in settings.json
# Story: STORY-527
# Generated: 2026-03-03

set -euo pipefail

PASSED=0
FAILED=0
SETTINGS_FILE="/mnt/c/Projects/DevForgeAI2/.claude/settings.json"

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        PASSED=$((PASSED + 1))
    else
        echo "  FAIL: $name"
        FAILED=$((FAILED + 1))
    fi
}

echo "=== AC#6: Hook Configuration in settings.json ==="
echo ""

# --- Pre-check: settings.json must exist ---
if [ ! -f "$SETTINGS_FILE" ]; then
    echo "  FAIL: settings.json does not exist at $SETTINGS_FILE"
    echo ""
    echo "Results: 0 passed, 1 failed"
    exit 1
fi

# --- Test 1: settings.json is valid JSON ---
EXIT_CODE=0
jq empty "$SETTINGS_FILE" 2>/dev/null || EXIT_CODE=$?
run_test "should_have_valid_json_in_settings" "$EXIT_CODE"

# --- Test 2: hooks object contains TaskCompleted key ---
TASK_COMPLETED_EXISTS=$(jq 'has("hooks") and (.hooks | has("TaskCompleted"))' "$SETTINGS_FILE" 2>/dev/null || echo "false")
if [ "$TASK_COMPLETED_EXISTS" = "true" ]; then
    run_test "should_have_task_completed_hook_entry" 0
else
    run_test "should_have_task_completed_hook_entry" 1
fi

# --- Test 3: TaskCompleted hook references validate-step-completion.sh ---
HOOK_REF=$(jq -r '.hooks.TaskCompleted[].hooks[].command // ""' "$SETTINGS_FILE" 2>/dev/null || echo "")
if echo "$HOOK_REF" | grep -q "validate-step-completion.sh"; then
    run_test "should_reference_validate_step_completion_script" 0
else
    run_test "should_reference_validate_step_completion_script" 1
fi

# --- Test 4: TaskCompleted hook has timeout configured ---
TIMEOUT_VAL=$(jq '.hooks.TaskCompleted[].hooks[].timeout // null' "$SETTINGS_FILE" 2>/dev/null || echo "null")
if [ "$TIMEOUT_VAL" != "null" ] && [ "$TIMEOUT_VAL" != "" ]; then
    run_test "should_have_timeout_configured" 0
else
    run_test "should_have_timeout_configured" 1
fi

# --- Test 5: Existing hooks are preserved (SubagentStop from STORY-526 should still exist) ---
TOTAL_HOOKS=$(jq '.hooks | length' "$SETTINGS_FILE" 2>/dev/null || echo "0")
if [ "$TOTAL_HOOKS" -ge 2 ]; then
    run_test "should_preserve_existing_hooks" 0
else
    run_test "should_preserve_existing_hooks (found $TOTAL_HOOKS hooks, expected >= 2)" 1
fi

# --- Summary ---
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
