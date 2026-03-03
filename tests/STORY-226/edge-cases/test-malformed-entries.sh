#!/bin/bash
# STORY-226 Edge Case Test: Malformed JSON Entries
#
# Given: history.jsonl with some malformed entries mixed with valid entries
# When: Analyzing for command sequences
# Then: Skip malformed entries, continue processing valid ones
#
# TDD RED PHASE: Test expected to FAIL before implementation

set -e

TEST_NAME="test-malformed-entries"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIXTURES_DIR="${TEST_DIR}/fixtures"

# Create history with malformed entries
MALFORMED_HISTORY="${FIXTURES_DIR}/malformed-history.jsonl"

cat > "$MALFORMED_HISTORY" << 'EOF'
{"timestamp": "2025-01-02T10:00:00Z", "command": "/ideate", "status": "success", "session_id": "malform-001"}
{malformed json without quotes
{"timestamp": "2025-01-02T10:02:00Z", "command": "/create-epic", "status": "success", "session_id": "malform-001"}

{"timestamp": "2025-01-02T10:03:00Z", "command": "/dev", "status": "success", "session_id": "malform-001"}
{"truncated": true
{"timestamp": "2025-01-02T11:00:00Z", "command": "/dev", "status": "success", "session_id": "malform-002"}
{"timestamp": "2025-01-02T11:01:00Z", "command": "/qa", "status": "success", "session_id": "malform-002"}
EOF

# Verify fixture created
if [ ! -f "$MALFORMED_HISTORY" ]; then
    echo "FAIL: Could not create malformed history fixture" >&2
    exit 1
fi

# Test 1: Verify session-miner subagent exists
SESSION_MINER_PATH=".claude/agents/session-miner.md"
if [ ! -f "$SESSION_MINER_PATH" ]; then
    echo "FAIL: session-miner subagent not found at $SESSION_MINER_PATH" >&2
    rm -f "$MALFORMED_HISTORY"
    exit 1
fi

# Test 2: Verify error tolerance is documented
if ! grep -qi "error.*toleran\|malformed.*skip\|invalid.*continue\|parse.*error" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document error tolerance for malformed entries" >&2
    rm -f "$MALFORMED_HISTORY"
    exit 1
fi

# Test 3: Document expected behavior
echo "INFO: Test data contains:"
echo "  - 5 valid JSON entries"
echo "  - 3 malformed entries (invalid JSON, empty line, truncated)"
echo ""
echo "INFO: Expected results:"
echo "  - Valid entries processed: 5"
echo "  - Malformed entries skipped: 3"
echo "  - Sequences extracted from valid entries only"
echo "  - 2-grams: [/ideate, /create-epic], [/create-epic, /dev], [/dev, /qa]"
echo "  - NOTE: Malformed entry breaks [/create-epic, /dev] into two parts"

# Test 4: Verify errors are logged but don't halt processing
if ! grep -qi "log.*error\|continue.*process\|skip.*invalid" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document logging and continuing on errors" >&2
    rm -f "$MALFORMED_HISTORY"
    exit 1
fi

# Clean up
rm -f "$MALFORMED_HISTORY"

echo "PASS: Malformed entry handling is properly documented"
exit 0
