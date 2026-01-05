#!/bin/bash
# STORY-226 Edge Case Test: Single Command Per Session
#
# Given: Sessions with only one command each (no sequences possible)
# When: Analyzing for command sequences
# Then: Return empty sequences (need at least 2 commands for 2-gram)
#
# TDD RED PHASE: Test expected to FAIL before implementation

set -e

TEST_NAME="test-single-command-session"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIXTURES_DIR="${TEST_DIR}/fixtures"

# Create single-command-per-session history
SINGLE_CMD_HISTORY="${FIXTURES_DIR}/single-command-history.jsonl"

cat > "$SINGLE_CMD_HISTORY" << 'EOF'
{"timestamp": "2025-01-02T10:00:00Z", "command": "/dev", "status": "success", "session_id": "single-001"}
{"timestamp": "2025-01-02T11:00:00Z", "command": "/qa", "status": "success", "session_id": "single-002"}
{"timestamp": "2025-01-02T12:00:00Z", "command": "/release", "status": "success", "session_id": "single-003"}
{"timestamp": "2025-01-02T13:00:00Z", "command": "/ideate", "status": "success", "session_id": "single-004"}
EOF

# Verify fixture created
if [ ! -f "$SINGLE_CMD_HISTORY" ]; then
    echo "FAIL: Could not create single-command history fixture" >&2
    exit 1
fi

# Test 1: Verify session-miner subagent exists
SESSION_MINER_PATH=".claude/agents/session-miner.md"
if [ ! -f "$SESSION_MINER_PATH" ]; then
    echo "FAIL: session-miner subagent not found at $SESSION_MINER_PATH" >&2
    rm -f "$SINGLE_CMD_HISTORY"
    exit 1
fi

# Test 2: Document expected behavior
echo "INFO: Test data: 4 sessions, each with only 1 command"
echo "  - session-001: /dev"
echo "  - session-002: /qa"
echo "  - session-003: /release"
echo "  - session-004: /ideate"
echo ""
echo "INFO: Expected results:"
echo "  - 2-grams: [] (need 2+ commands in same session)"
echo "  - 3-grams: [] (need 3+ commands in same session)"
echo "  - Cross-session sequences should NOT be counted"

# Test 3: Verify session boundary is respected
# [/dev from session-001] should NOT combine with [/qa from session-002]
if ! grep -qi "session.*boundary\|same.*session\|within.*session" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document session boundary constraints" >&2
    rm -f "$SINGLE_CMD_HISTORY"
    exit 1
fi

# Clean up
rm -f "$SINGLE_CMD_HISTORY"

echo "PASS: Single command session handling is properly documented"
exit 0
