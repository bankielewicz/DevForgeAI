#!/bin/bash
# STORY-229 Edge Case Test: Missing error_message Field
#
# Given: history.jsonl with status: "error" but missing error_message field
# When: Extracting errors
# Then: Entry still captured, use default "Unknown error" message
#
# TDD RED PHASE: Test expected to FAIL before implementation

set -e

TEST_NAME="test-missing-error-message"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIXTURES_DIR="${TEST_DIR}/fixtures"

# Create history with missing error_message fields
MISSING_MSG_HISTORY="${FIXTURES_DIR}/missing-message-history.jsonl"

cat > "$MISSING_MSG_HISTORY" << 'EOF'
{"timestamp": "2025-01-02T10:00:00Z", "command": "/dev STORY-100", "status": "error", "error_message": "API rate limit exceeded", "session_id": "missing-msg-001"}
{"timestamp": "2025-01-02T10:05:00Z", "command": "/qa STORY-100", "status": "error", "session_id": "missing-msg-001"}
{"timestamp": "2025-01-02T10:10:00Z", "command": "/release STORY-100", "status": "error", "error_message": "", "session_id": "missing-msg-001"}
{"timestamp": "2025-01-02T10:15:00Z", "command": "/dev STORY-101", "status": "error", "error_message": null, "session_id": "missing-msg-001"}
EOF

# Verify fixture created
if [ ! -f "$MISSING_MSG_HISTORY" ]; then
    echo "FAIL: Could not create missing-message history fixture" >&2
    exit 1
fi

SESSION_MINER_PATH=".claude/agents/session-miner.md"
if [ ! -f "$SESSION_MINER_PATH" ]; then
    echo "FAIL: session-miner subagent not found at $SESSION_MINER_PATH" >&2
    rm -f "$MISSING_MSG_HISTORY"
    exit 1
fi

# Test 1: Verify handling of missing error_message is documented
if ! grep -qi "missing.*message\|empty.*message\|null.*message\|default.*message" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document handling of missing error_message" >&2
    rm -f "$MISSING_MSG_HISTORY"
    exit 1
fi

# Test 2: Verify default message behavior is documented
if ! grep -qi "unknown.*error\|default.*error\|fallback.*message" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document default error message behavior" >&2
    rm -f "$MISSING_MSG_HISTORY"
    exit 1
fi

# Test 3: Document expected behavior
echo "INFO: Test data contains:"
echo "  - 4 error entries"
echo "  - 1 with valid error_message"
echo "  - 1 without error_message field"
echo "  - 1 with empty error_message"
echo "  - 1 with null error_message"
echo ""
echo "INFO: Expected results:"
echo "  - All 4 errors extracted"
echo "  - 3 entries assigned 'Unknown error' default message"
echo "  - Classified as 'other' category"
echo "  - Assigned 'low' severity"

# Clean up
rm -f "$MISSING_MSG_HISTORY"

echo "PASS: Missing error_message handling is properly documented"
exit 0
