#!/bin/bash
# Test: AC#3 - Calls devforgeai-validate phase-record With Correct Arguments
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

echo "=== AC#3: Phase Record CLI Arguments Tests ==="

# --- Arrange ---
TEST_DIR=$(mktemp -d "$PROJECT_ROOT/tests/STORY-526/tmp.XXXXXX")
trap "rm -rf $TEST_DIR" EXIT

# Create mock devforgeai-validate that logs full invocation
MOCK_BIN="$TEST_DIR/bin"
mkdir -p "$MOCK_BIN"
cat > "$MOCK_BIN/devforgeai-validate" << 'MOCK'
#!/bin/bash
echo "CALL: $@" >> "$MOCK_LOG_FILE"
MOCK
chmod +x "$MOCK_BIN/devforgeai-validate"

export PATH="$MOCK_BIN:$PATH"
export MOCK_LOG_FILE="$TEST_DIR/mock-calls.log"

# Create phase-state.json with known story ID and phase
mkdir -p "$TEST_DIR/devforgeai/workflows"
cat > "$TEST_DIR/devforgeai/workflows/STORY-526-phase-state.json" << 'STATE'
{"story_id": "STORY-526", "current_phase": "02"}
STATE
# Create CLAUDE.md so hook detects project root
touch "$TEST_DIR/CLAUDE.md"
export CLAUDE_PROJECT_DIR="$TEST_DIR"

# --- Act & Assert ---

# Test 1: CLI receives story_id argument
> "$MOCK_LOG_FILE"
echo '{"session_id":"s1","agent_type":"test-automator","conversation_id":"c1"}' | "$HOOK_SCRIPT" > /dev/null 2>&1 || true
grep -q "STORY-526" "$MOCK_LOG_FILE" 2>/dev/null
run_test "CLI receives story_id argument (STORY-526)" $?

# Test 2: CLI receives --subagent flag with agent_type value
> "$MOCK_LOG_FILE"
echo '{"session_id":"s1","agent_type":"test-automator","conversation_id":"c1"}' | "$HOOK_SCRIPT" > /dev/null 2>&1 || true
grep -q "\-\-subagent=test-automator" "$MOCK_LOG_FILE" 2>/dev/null
run_test "CLI receives --subagent=test-automator flag" $?

# Test 3: CLI receives --phase flag from phase-state.json
> "$MOCK_LOG_FILE"
echo '{"session_id":"s1","agent_type":"test-automator","conversation_id":"c1"}' | "$HOOK_SCRIPT" > /dev/null 2>&1 || true
grep -q "\-\-phase=02" "$MOCK_LOG_FILE" 2>/dev/null
run_test "CLI receives --phase=02 from phase-state.json" $?

# Test 4: CLI call includes phase-record subcommand
> "$MOCK_LOG_FILE"
echo '{"session_id":"s1","agent_type":"test-automator","conversation_id":"c1"}' | "$HOOK_SCRIPT" > /dev/null 2>&1 || true
grep -q "phase-record" "$MOCK_LOG_FILE" 2>/dev/null
run_test "CLI call includes phase-record subcommand" $?

# Test 5: Missing phase-state.json exits 0 with warning (no crash)
rm -f "$TEST_DIR/devforgeai/workflows/STORY-526-phase-state.json"
> "$MOCK_LOG_FILE"
echo '{"session_id":"s1","agent_type":"test-automator","conversation_id":"c1"}' | "$HOOK_SCRIPT" > /dev/null 2>&1
EXIT_CODE=$?
[ "$EXIT_CODE" -eq 0 ]
run_test "Missing phase-state.json exits 0 (non-blocking)" $?

# Test 6: Missing phase-state.json does NOT call phase-record
if [ -f "$MOCK_LOG_FILE" ]; then
    ! grep -q "phase-record" "$MOCK_LOG_FILE" 2>/dev/null
    run_test "Missing phase-state.json skips phase-record call" $?
else
    run_test "Missing phase-state.json skips phase-record call" 0
fi

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
