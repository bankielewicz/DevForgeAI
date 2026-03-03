#!/bin/bash
##############################################################################
# Integration Tests: STORY-526 - SubagentStop Hook Auto-Track Invocations
#
# Tests:
#   1. E2E Hook Flow (built-in filter, DevForgeAI recording, sequential events)
#   2. Settings Integration (SubagentStop entry, existing hooks preserved)
#   3. Security Integration (injection character rejection)
##############################################################################

set -euo pipefail

# Counters
PASSED=0
FAILED=0
TOTAL=0

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/../.."
HOOK_SCRIPT="${PROJECT_ROOT}/src/claude/hooks/track-subagent-invocation.sh"
SETTINGS_FILE="${PROJECT_ROOT}/src/claude/settings.json"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

##############################################################################
# Helpers
##############################################################################

assert_eq() {
    local desc="$1" expected="$2" actual="$3"
    TOTAL=$((TOTAL + 1))
    if [ "$expected" = "$actual" ]; then
        echo -e "  ${GREEN}PASS${NC}: $desc"
        PASSED=$((PASSED + 1))
    else
        echo -e "  ${RED}FAIL${NC}: $desc"
        echo "    Expected: '$expected'"
        echo "    Actual:   '$actual'"
        FAILED=$((FAILED + 1))
    fi
}

assert_contains() {
    local desc="$1" haystack="$2" needle="$3"
    TOTAL=$((TOTAL + 1))
    if echo "$haystack" | grep -qF -- "$needle"; then
        echo -e "  ${GREEN}PASS${NC}: $desc"
        PASSED=$((PASSED + 1))
    else
        echo -e "  ${RED}FAIL${NC}: $desc"
        echo "    Expected to contain: '$needle'"
        echo "    In: '$haystack'"
        FAILED=$((FAILED + 1))
    fi
}

assert_not_contains() {
    local desc="$1" haystack="$2" needle="$3"
    TOTAL=$((TOTAL + 1))
    if ! echo "$haystack" | grep -qF -- "$needle"; then
        echo -e "  ${GREEN}PASS${NC}: $desc"
        PASSED=$((PASSED + 1))
    else
        echo -e "  ${RED}FAIL${NC}: $desc"
        echo "    Expected NOT to contain: '$needle'"
        FAILED=$((FAILED + 1))
    fi
}

##############################################################################
# Setup temp environment
##############################################################################

setup_temp_env() {
    TMPDIR=$(mktemp -d)
    # Create project structure
    mkdir -p "$TMPDIR/devforgeai/workflows"
    touch "$TMPDIR/CLAUDE.md"

    # Create mock phase-state.json
    cat > "$TMPDIR/devforgeai/workflows/STORY-526-phase-state.json" <<'PSJSON'
{
    "story_id": "STORY-526",
    "current_phase": "03",
    "phases": {
        "01": {"status": "completed"},
        "02": {"status": "completed"},
        "03": {"status": "in_progress"}
    }
}
PSJSON

    # Create mock devforgeai-validate in temp bin
    MOCK_BIN="$TMPDIR/bin"
    mkdir -p "$MOCK_BIN"
    MOCK_LOG="$TMPDIR/validate-calls.log"
    cat > "$MOCK_BIN/devforgeai-validate" <<MOCKEOF
#!/bin/bash
echo "\$@" >> "$MOCK_LOG"
MOCKEOF
    chmod +x "$MOCK_BIN/devforgeai-validate"

    export PATH="$MOCK_BIN:$PATH"
    export CLAUDE_PROJECT_DIR="$TMPDIR"
}

teardown_temp_env() {
    rm -rf "$TMPDIR"
}

##############################################################################
# Test 1: E2E Hook Flow
##############################################################################

echo "=== Test Group 1: E2E Hook Flow ==="

# 1a: Built-in agent (Explore) should NOT trigger phase-record
setup_temp_env
echo '{"agent_type": "Explore"}' | bash "$HOOK_SCRIPT" 2>/dev/null
if [ -f "$MOCK_LOG" ]; then
    CALL_COUNT=$(wc -l < "$MOCK_LOG")
else
    CALL_COUNT=0
fi
assert_eq "Built-in agent Explore is filtered (no CLI call)" "0" "$CALL_COUNT"
teardown_temp_env

# 1b: DevForgeAI agent (test-automator) SHOULD trigger phase-record
setup_temp_env
echo '{"agent_type": "test-automator"}' | bash "$HOOK_SCRIPT" 2>/dev/null
if [ -f "$MOCK_LOG" ]; then
    LOGGED=$(cat "$MOCK_LOG")
else
    LOGGED=""
fi
assert_contains "test-automator triggers phase-record" "$LOGGED" "phase-record"
assert_contains "phase-record includes STORY-526" "$LOGGED" "STORY-526"
assert_contains "phase-record includes phase 03" "$LOGGED" "--phase=03"
assert_contains "phase-record includes subagent name" "$LOGGED" "--subagent=test-automator"
teardown_temp_env

# 1c: Multiple sequential SubagentStop events each recorded
setup_temp_env
echo '{"agent_type": "test-automator"}' | bash "$HOOK_SCRIPT" 2>/dev/null
echo '{"agent_type": "code-reviewer"}' | bash "$HOOK_SCRIPT" 2>/dev/null
echo '{"agent_type": "backend-architect"}' | bash "$HOOK_SCRIPT" 2>/dev/null
if [ -f "$MOCK_LOG" ]; then
    CALL_COUNT=$(wc -l < "$MOCK_LOG")
    LOGGED=$(cat "$MOCK_LOG")
else
    CALL_COUNT=0
    LOGGED=""
fi
assert_eq "Three sequential events produce three CLI calls" "3" "$CALL_COUNT"
assert_contains "First call records test-automator" "$LOGGED" "--subagent=test-automator"
assert_contains "Second call records code-reviewer" "$LOGGED" "--subagent=code-reviewer"
assert_contains "Third call records backend-architect" "$LOGGED" "--subagent=backend-architect"
teardown_temp_env

# 1d: Built-in agents Plan, Bash, general-purpose also filtered
setup_temp_env
for builtin_agent in Plan Bash general-purpose; do
    echo "{\"agent_type\": \"$builtin_agent\"}" | bash "$HOOK_SCRIPT" 2>/dev/null
done
if [ -f "$MOCK_LOG" ]; then
    CALL_COUNT=$(wc -l < "$MOCK_LOG")
else
    CALL_COUNT=0
fi
assert_eq "Built-in agents Plan/Bash/general-purpose all filtered" "0" "$CALL_COUNT"
teardown_temp_env

##############################################################################
# Test 2: Settings Integration
##############################################################################

echo ""
echo "=== Test Group 2: Settings Integration ==="

SETTINGS_CONTENT=$(cat "$SETTINGS_FILE")

# 2a: SubagentStop hook entry exists
assert_contains "settings.json contains SubagentStop hook" "$SETTINGS_CONTENT" '"SubagentStop"'

# 2b: Hook command path is correct
assert_contains "SubagentStop hook command references track-subagent-invocation.sh" "$SETTINGS_CONTENT" "track-subagent-invocation.sh"

# 2c: Existing PreToolUse hook still present
assert_contains "PreToolUse hook still present" "$SETTINGS_CONTENT" '"PreToolUse"'

# 2d: Existing PostToolUse hook still present
assert_contains "PostToolUse hook still present" "$SETTINGS_CONTENT" '"PostToolUse"'

# 2e: Existing PermissionRequest hook still present
assert_contains "PermissionRequest hook still present" "$SETTINGS_CONTENT" '"PermissionRequest"'

# 2f: pre-tool-use.sh reference preserved
assert_contains "pre-tool-use.sh hook reference preserved" "$SETTINGS_CONTENT" "pre-tool-use.sh"

# 2g: post-edit-write-check.sh reference preserved
assert_contains "post-edit-write-check.sh hook reference preserved" "$SETTINGS_CONTENT" "post-edit-write-check.sh"

##############################################################################
# Test 3: Security Integration
##############################################################################

echo ""
echo "=== Test Group 3: Security Integration ==="

# 3a: Injection characters in agent_type are rejected
setup_temp_env
echo '{"agent_type": "test; rm -rf /"}' | bash "$HOOK_SCRIPT" 2>/dev/null
if [ -f "$MOCK_LOG" ]; then
    CALL_COUNT=$(wc -l < "$MOCK_LOG")
else
    CALL_COUNT=0
fi
assert_eq "Semicolon injection rejected (no CLI call)" "0" "$CALL_COUNT"
teardown_temp_env

# 3b: Pipe injection rejected
setup_temp_env
echo '{"agent_type": "test|cat /etc/passwd"}' | bash "$HOOK_SCRIPT" 2>/dev/null
if [ -f "$MOCK_LOG" ]; then
    CALL_COUNT=$(wc -l < "$MOCK_LOG")
else
    CALL_COUNT=0
fi
assert_eq "Pipe injection rejected (no CLI call)" "0" "$CALL_COUNT"
teardown_temp_env

# 3c: Backtick injection rejected
setup_temp_env
echo '{"agent_type": "test`whoami`"}' | bash "$HOOK_SCRIPT" 2>/dev/null
if [ -f "$MOCK_LOG" ]; then
    CALL_COUNT=$(wc -l < "$MOCK_LOG")
else
    CALL_COUNT=0
fi
assert_eq "Backtick injection rejected (no CLI call)" "0" "$CALL_COUNT"
teardown_temp_env

# 3d: Valid agent_type passes through
setup_temp_env
echo '{"agent_type": "test-automator"}' | bash "$HOOK_SCRIPT" 2>/dev/null
if [ -f "$MOCK_LOG" ]; then
    CALL_COUNT=$(wc -l < "$MOCK_LOG")
else
    CALL_COUNT=0
fi
assert_eq "Valid agent_type test-automator passes security check" "1" "$CALL_COUNT"
teardown_temp_env

# 3e: Underscore in agent_type is valid
setup_temp_env
echo '{"agent_type": "my_agent_name"}' | bash "$HOOK_SCRIPT" 2>/dev/null
if [ -f "$MOCK_LOG" ]; then
    CALL_COUNT=$(wc -l < "$MOCK_LOG")
else
    CALL_COUNT=0
fi
assert_eq "Underscore in agent_type is valid" "1" "$CALL_COUNT"
teardown_temp_env

# 3f: Space injection rejected
setup_temp_env
echo '{"agent_type": "test automator"}' | bash "$HOOK_SCRIPT" 2>/dev/null
if [ -f "$MOCK_LOG" ]; then
    CALL_COUNT=$(wc -l < "$MOCK_LOG")
else
    CALL_COUNT=0
fi
assert_eq "Space in agent_type rejected" "0" "$CALL_COUNT"
teardown_temp_env

##############################################################################
# Summary
##############################################################################

echo ""
echo "=========================================="
echo "  STORY-526 Integration Test Results"
echo "=========================================="
echo "  Total:  $TOTAL"
echo -e "  ${GREEN}Passed: $PASSED${NC}"
if [ "$FAILED" -gt 0 ]; then
    echo -e "  ${RED}Failed: $FAILED${NC}"
fi
echo "=========================================="

if [ "$FAILED" -gt 0 ]; then
    exit 1
fi
exit 0
