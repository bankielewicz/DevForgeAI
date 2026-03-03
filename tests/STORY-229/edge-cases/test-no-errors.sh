#!/bin/bash
# STORY-229 Edge Case Test: No Errors in History
#
# Given: history.jsonl with only status: "success" entries (no errors)
# When: Analyzing for errors
# Then: Return empty results gracefully, no errors thrown
#
# TDD RED PHASE: Test expected to FAIL before implementation

set -e

TEST_NAME="test-no-errors"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIXTURES_DIR="${TEST_DIR}/fixtures"

# Create history with only success entries
SUCCESS_ONLY_HISTORY="${FIXTURES_DIR}/success-only-history.jsonl"

cat > "$SUCCESS_ONLY_HISTORY" << 'EOF'
{"timestamp": "2025-01-02T10:00:00Z", "command": "/dev STORY-100", "status": "success", "duration_ms": 5000, "session_id": "success-001"}
{"timestamp": "2025-01-02T10:05:00Z", "command": "/qa STORY-100", "status": "success", "duration_ms": 8000, "session_id": "success-001"}
{"timestamp": "2025-01-02T10:10:00Z", "command": "/release STORY-100", "status": "success", "duration_ms": 3000, "session_id": "success-001"}
EOF

# Verify fixture created
if [ ! -f "$SUCCESS_ONLY_HISTORY" ]; then
    echo "FAIL: Could not create success-only history fixture" >&2
    exit 1
fi

SESSION_MINER_PATH=".claude/agents/session-miner.md"
if [ ! -f "$SESSION_MINER_PATH" ]; then
    echo "FAIL: session-miner subagent not found at $SESSION_MINER_PATH" >&2
    rm -f "$SUCCESS_ONLY_HISTORY"
    exit 1
fi

# Test 1: Verify handling of no errors is documented
if ! grep -qi "no.*error\|empty.*result\|zero.*error" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document handling of history with no errors" >&2
    rm -f "$SUCCESS_ONLY_HISTORY"
    exit 1
fi

# Test 2: Verify graceful empty response is documented
if ! grep -qi "empty.*response\|graceful.*empty\|no.*match" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document graceful empty response" >&2
    rm -f "$SUCCESS_ONLY_HISTORY"
    exit 1
fi

# Test 3: Document expected behavior
echo "INFO: Test data contains:"
echo "  - 3 success entries"
echo "  - 0 error entries"
echo ""
echo "INFO: Expected results:"
echo "  - extracted_errors: []"
echo "  - categories: {}"
echo "  - registry: { error_codes: [] }"
echo "  - No exceptions thrown"

# Clean up
rm -f "$SUCCESS_ONLY_HISTORY"

echo "PASS: No-error handling is properly documented"
exit 0
