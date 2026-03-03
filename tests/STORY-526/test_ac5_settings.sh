#!/bin/bash
# Test: AC#5 - Hook Configuration Added to .claude/settings.json
# Story: STORY-526
# Generated: 2026-03-02

set -euo pipefail

PASSED=0
FAILED=0
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SETTINGS_FILE="$PROJECT_ROOT/src/claude/settings.json"

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

echo "=== AC#5: Settings.json Hook Configuration Tests ==="

# --- Act & Assert ---

# Test 1: settings.json exists
test -f "$SETTINGS_FILE"
run_test "settings.json exists at src/claude/settings.json" $?

# Test 2: settings.json is valid JSON
jq empty "$SETTINGS_FILE" > /dev/null 2>&1
run_test "settings.json is valid JSON" $?

# Test 3: hooks section exists
jq -e '.hooks' "$SETTINGS_FILE" > /dev/null 2>&1
run_test "hooks section exists in settings.json" $?

# Test 4: SubagentStop event key exists in hooks
jq -e '.hooks.SubagentStop' "$SETTINGS_FILE" > /dev/null 2>&1
run_test "SubagentStop event key exists in hooks" $?

# Test 5: SubagentStop references track-subagent-invocation.sh
jq -r '.hooks.SubagentStop | .. | .command? // empty' "$SETTINGS_FILE" 2>/dev/null | grep -q "track-subagent-invocation"
run_test "SubagentStop references track-subagent-invocation.sh" $?

# Test 6: Timeout is set to 10 seconds
TIMEOUT=$(jq -r '.hooks.SubagentStop | .. | .timeout? // empty | select(. != null and . != "")' "$SETTINGS_FILE" 2>/dev/null | head -1)
[ "$TIMEOUT" = "10000" ] || [ "$TIMEOUT" = "10" ]
run_test "SubagentStop timeout set to 10 seconds" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
