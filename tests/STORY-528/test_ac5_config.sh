#!/bin/bash
# Test: AC#5 - Settings.json Configuration
# Story: STORY-528
# Verifies: Stop hook registered in .claude/settings.json with correct structure

set -uo pipefail

HOOK_SCRIPT="src/claude/hooks/phase-completion-gate.sh"
SETTINGS_FILE="src/claude/settings.json"
PASS=0
FAIL=0

run_test() {
    local description="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "PASS: $description"
        ((PASS++))
    else
        echo "FAIL: $description"
        ((FAIL++))
    fi
}

echo "=== AC#5: Settings.json Configuration ==="
echo "Target: $SETTINGS_FILE"
echo ""

# --- Test 1: Settings file exists ---
run_test "Settings file exists at $SETTINGS_FILE" \
    "$([ -f "$SETTINGS_FILE" ] && echo 0 || echo 1)"

# --- Test 2: Valid JSON ---
if [ -f "$SETTINGS_FILE" ]; then
    jq . "$SETTINGS_FILE" > /dev/null 2>&1
    run_test "Settings file is valid JSON" "$?"
else
    run_test "Settings file is valid JSON" "1"
fi

# --- Test 3: hooks section exists ---
run_test "Contains hooks section" \
    "$(jq -e '.hooks' "$SETTINGS_FILE" > /dev/null 2>&1 && echo 0 || echo 1)"

# --- Test 4: Stop event hook entry (array-of-hook-groups format per Claude Code docs) ---
run_test "Contains Stop event hook" \
    "$(jq -e '.hooks.Stop' "$SETTINGS_FILE" > /dev/null 2>&1 && echo 0 || echo 1)"

# --- Test 5: Stop hook points to phase-completion-gate.sh ---
run_test "Stop hook references phase-completion-gate.sh" \
    "$(jq -e '.hooks.Stop[].hooks[].command' "$SETTINGS_FILE" 2>/dev/null | grep -q "phase-completion-gate" && echo 0 || echo 1)"

# --- Test 6: Timeout is 15 seconds ---
TIMEOUT=$(jq -r '.hooks.Stop[].hooks[].timeout' "$SETTINGS_FILE" 2>/dev/null)
run_test "Stop hook timeout is 15 seconds" \
    "$([ "$TIMEOUT" = "15" ] || [ "$TIMEOUT" = "15000" ] && echo 0 || echo 1)"

# --- Test 7: Existing hooks preserved (PreToolUse, PostToolUse, etc.) ---
# AC#5 requires: "Existing hooks unchanged"
run_test "PreToolUse hook still exists" \
    "$(jq -e '.hooks.PreToolUse' "$SETTINGS_FILE" > /dev/null 2>&1 && echo 0 || echo 1)"

run_test "PostToolUse hook still exists" \
    "$(jq -e '.hooks.PostToolUse' "$SETTINGS_FILE" > /dev/null 2>&1 && echo 0 || echo 1)"

run_test "PermissionRequest hook still exists" \
    "$(jq -e '.hooks.PermissionRequest' "$SETTINGS_FILE" > /dev/null 2>&1 && echo 0 || echo 1)"

run_test "PreToolUse Bash matcher preserved" \
    "$(jq -e '.hooks.PreToolUse[0].matcher' "$SETTINGS_FILE" 2>/dev/null | grep -q 'Bash' && echo 0 || echo 1)"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
