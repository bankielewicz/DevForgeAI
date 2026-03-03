#!/bin/bash
# Test: AC#2 - Filters Built-in Agents and Records DevForgeAI Subagents
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

echo "=== AC#2: Filter Built-in Agents Tests ==="

# --- Arrange ---
TEST_DIR=$(mktemp -d "$PROJECT_ROOT/tests/STORY-526/tmp.XXXXXX")
trap "rm -rf $TEST_DIR" EXIT

# Create mock devforgeai-validate that logs calls
MOCK_BIN="$TEST_DIR/bin"
mkdir -p "$MOCK_BIN"
cat > "$MOCK_BIN/devforgeai-validate" << 'MOCK'
#!/bin/bash
echo "$@" >> "$MOCK_LOG_FILE"
MOCK
chmod +x "$MOCK_BIN/devforgeai-validate"

# Set up phase-state.json so hook can find story context
mkdir -p "$TEST_DIR/devforgeai/workflows"
cat > "$TEST_DIR/devforgeai/workflows/STORY-526-phase-state.json" << 'STATE'
{"story_id": "STORY-526", "current_phase": "02"}
STATE
# Create CLAUDE.md so hook detects project root
touch "$TEST_DIR/CLAUDE.md"

export PATH="$MOCK_BIN:$PATH"
export MOCK_LOG_FILE="$TEST_DIR/mock-calls.log"
export CLAUDE_PROJECT_DIR="$TEST_DIR"

# --- Act & Assert ---

# Test 1: Built-in agent "Explore" is NOT recorded
> "$MOCK_LOG_FILE"
echo '{"session_id":"s1","agent_type":"Explore","conversation_id":"c1"}' | "$HOOK_SCRIPT" > /dev/null 2>&1 || true
if [ -f "$MOCK_LOG_FILE" ]; then
    ! grep -q "phase-record" "$MOCK_LOG_FILE" 2>/dev/null
    run_test "Built-in agent 'Explore' is NOT recorded" $?
else
    run_test "Built-in agent 'Explore' is NOT recorded" 0
fi

# Test 2: Built-in agent "Plan" is NOT recorded
> "$MOCK_LOG_FILE"
echo '{"session_id":"s1","agent_type":"Plan","conversation_id":"c1"}' | "$HOOK_SCRIPT" > /dev/null 2>&1 || true
if [ -f "$MOCK_LOG_FILE" ]; then
    ! grep -q "phase-record" "$MOCK_LOG_FILE" 2>/dev/null
    run_test "Built-in agent 'Plan' is NOT recorded" $?
else
    run_test "Built-in agent 'Plan' is NOT recorded" 0
fi

# Test 3: Built-in agent "Bash" is NOT recorded
> "$MOCK_LOG_FILE"
echo '{"session_id":"s1","agent_type":"Bash","conversation_id":"c1"}' | "$HOOK_SCRIPT" > /dev/null 2>&1 || true
if [ -f "$MOCK_LOG_FILE" ]; then
    ! grep -q "phase-record" "$MOCK_LOG_FILE" 2>/dev/null
    run_test "Built-in agent 'Bash' is NOT recorded" $?
else
    run_test "Built-in agent 'Bash' is NOT recorded" 0
fi

# Test 4: Built-in agent "general-purpose" is NOT recorded
> "$MOCK_LOG_FILE"
echo '{"session_id":"s1","agent_type":"general-purpose","conversation_id":"c1"}' | "$HOOK_SCRIPT" > /dev/null 2>&1 || true
if [ -f "$MOCK_LOG_FILE" ]; then
    ! grep -q "phase-record" "$MOCK_LOG_FILE" 2>/dev/null
    run_test "Built-in agent 'general-purpose' is NOT recorded" $?
else
    run_test "Built-in agent 'general-purpose' is NOT recorded" 0
fi

# Test 5: DevForgeAI subagent "test-automator" IS recorded
> "$MOCK_LOG_FILE"
echo '{"session_id":"s1","agent_type":"test-automator","conversation_id":"c1"}' | "$HOOK_SCRIPT" > /dev/null 2>&1 || true
grep -q "phase-record" "$MOCK_LOG_FILE" 2>/dev/null
run_test "DevForgeAI subagent 'test-automator' IS recorded" $?

# Test 6: DevForgeAI subagent "code-reviewer" IS recorded
> "$MOCK_LOG_FILE"
echo '{"session_id":"s1","agent_type":"code-reviewer","conversation_id":"c1"}' | "$HOOK_SCRIPT" > /dev/null 2>&1 || true
grep -q "phase-record" "$MOCK_LOG_FILE" 2>/dev/null
run_test "DevForgeAI subagent 'code-reviewer' IS recorded" $?

# Test 7: DevForgeAI subagent "backend-architect" IS recorded
> "$MOCK_LOG_FILE"
echo '{"session_id":"s1","agent_type":"backend-architect","conversation_id":"c1"}' | "$HOOK_SCRIPT" > /dev/null 2>&1 || true
grep -q "phase-record" "$MOCK_LOG_FILE" 2>/dev/null
run_test "DevForgeAI subagent 'backend-architect' IS recorded" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
