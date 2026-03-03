#!/bin/bash
# Test: AC#1 - Hook Script Receives and Parses SubagentStop JSON Input
# Story: STORY-526
# Generated: 2026-03-02

set -euo pipefail

PASSED=0
FAILED=0
HOOK_SCRIPT="$(cd "$(dirname "$0")/../.." && pwd)/src/claude/hooks/track-subagent-invocation.sh"

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

echo "=== AC#1: JSON Parsing Tests ==="

# --- Arrange ---
VALID_JSON='{"session_id":"abc","agent_type":"test-automator","conversation_id":"xyz"}'
MALFORMED_JSON='{"session_id": broken json'
EMPTY_INPUT=""

# --- Act & Assert ---

# Test 1: Hook script exists at expected path
test -f "$HOOK_SCRIPT"
run_test "Hook script exists at src/claude/hooks/track-subagent-invocation.sh" $?

# Test 2: Hook script is executable
test -x "$HOOK_SCRIPT"
run_test "Hook script is executable" $?

# Test 3: Valid JSON is accepted without error
echo "$VALID_JSON" | "$HOOK_SCRIPT" > /dev/null 2>&1
run_test "Valid JSON input accepted without error" $?

# Test 4: agent_type is correctly extracted from valid JSON (appears in stderr debug output)
EXTRACTED=$(echo "$VALID_JSON" | "$HOOK_SCRIPT" 2>&1 1>/dev/null | grep -o "test-automator" | head -1 || true)
[ -n "$EXTRACTED" ]
run_test "agent_type correctly extracted from valid JSON" $?

# Test 5: Malformed JSON does not crash (exits 0)
echo "$MALFORMED_JSON" | "$HOOK_SCRIPT" > /dev/null 2>&1
EXIT_CODE=$?
[ "$EXIT_CODE" -eq 0 ]
run_test "Malformed JSON does not crash - exits 0" $?

# Test 6: Empty input does not crash (exits 0)
echo "$EMPTY_INPUT" | "$HOOK_SCRIPT" > /dev/null 2>&1
EXIT_CODE=$?
[ "$EXIT_CODE" -eq 0 ]
run_test "Empty input does not crash - exits 0" $?

# Test 7: JSON without agent_type field exits 0
echo '{"session_id":"abc","conversation_id":"xyz"}' | "$HOOK_SCRIPT" > /dev/null 2>&1
EXIT_CODE=$?
[ "$EXIT_CODE" -eq 0 ]
run_test "JSON without agent_type field exits 0" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
