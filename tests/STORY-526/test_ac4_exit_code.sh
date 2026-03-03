#!/bin/bash
# Test: AC#4 - Hook Always Exits Code 0 (Non-Blocking)
# Story: STORY-526
# Generated: 2026-03-02

set -euo pipefail

PASSED=0
FAILED=0
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
HOOK_SCRIPT="$PROJECT_ROOT/src/claude/hooks/track-subagent-invocation.sh"

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

echo "=== AC#4: Exit Code 0 (Non-Blocking) Tests ==="

# --- Arrange ---
TEST_DIR=$(mktemp -d "$PROJECT_ROOT/tests/STORY-526/tmp.XXXXXX")
trap "rm -rf $TEST_DIR" EXIT

# --- Act & Assert ---

# Test 1: Valid input exits 0
echo '{"session_id":"s1","agent_type":"test-automator","conversation_id":"c1"}' | "$HOOK_SCRIPT" > /dev/null 2>&1
run_test "Valid input exits 0" $?

# Test 2: Malformed JSON exits 0
echo '{broken' | "$HOOK_SCRIPT" > /dev/null 2>&1
run_test "Malformed JSON exits 0" $?

# Test 3: Empty stdin exits 0
echo "" | "$HOOK_SCRIPT" > /dev/null 2>&1
run_test "Empty stdin exits 0" $?

# Test 4: Missing devforgeai-validate CLI exits 0
(
    mkdir -p "$TEST_DIR/empty-bin"
    export PATH="$TEST_DIR/empty-bin:/usr/bin:/bin"
    echo '{"session_id":"s1","agent_type":"test-automator","conversation_id":"c1"}' | "$HOOK_SCRIPT" > /dev/null 2>&1
)
run_test "Missing devforgeai-validate CLI exits 0" $?

# Test 5: Missing phase-state.json exits 0
(
    export DEVFORGEAI_PROJECT_ROOT="$TEST_DIR/nonexistent"
    echo '{"session_id":"s1","agent_type":"test-automator","conversation_id":"c1"}' | "$HOOK_SCRIPT" > /dev/null 2>&1
)
run_test "Missing phase-state.json exits 0" $?

# Test 6: Built-in agent type exits 0
echo '{"session_id":"s1","agent_type":"Explore","conversation_id":"c1"}' | "$HOOK_SCRIPT" > /dev/null 2>&1
run_test "Built-in agent type exits 0" $?

# Test 7: JSON with null agent_type exits 0
echo '{"session_id":"s1","agent_type":null,"conversation_id":"c1"}' | "$HOOK_SCRIPT" > /dev/null 2>&1
run_test "Null agent_type exits 0" $?

# Test 8: Very large JSON input exits 0
LARGE_JSON="{\"session_id\":\"$(head -c 10000 /dev/urandom | base64 | tr -d '\n' | head -c 5000)\",\"agent_type\":\"test-automator\",\"conversation_id\":\"c1\"}"
echo "$LARGE_JSON" | "$HOOK_SCRIPT" > /dev/null 2>&1
run_test "Very large JSON input exits 0" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
