#!/bin/bash
# STORY-229 Edge Case Test: Duplicate Error Patterns
#
# Given: history.jsonl with many identical error messages
# When: Building error registry
# Then: Group into single error code with accurate occurrence count
#
# TDD RED PHASE: Test expected to FAIL before implementation

set -e

TEST_NAME="test-duplicate-errors"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIXTURES_DIR="${TEST_DIR}/fixtures"

# Create history with duplicate errors
DUPLICATE_HISTORY="${FIXTURES_DIR}/duplicate-errors-history.jsonl"

cat > "$DUPLICATE_HISTORY" << 'EOF'
{"timestamp": "2025-01-02T10:00:00Z", "command": "/dev STORY-100", "status": "error", "error_message": "API rate limit exceeded", "session_id": "dup-001"}
{"timestamp": "2025-01-02T10:05:00Z", "command": "/dev STORY-101", "status": "error", "error_message": "API rate limit exceeded", "session_id": "dup-001"}
{"timestamp": "2025-01-02T10:10:00Z", "command": "/qa STORY-100", "status": "error", "error_message": "API rate limit exceeded", "session_id": "dup-001"}
{"timestamp": "2025-01-02T11:00:00Z", "command": "/dev STORY-102", "status": "error", "error_message": "API rate limit exceeded", "session_id": "dup-002"}
{"timestamp": "2025-01-02T11:05:00Z", "command": "/dev STORY-103", "status": "error", "error_message": "API rate limit exceeded", "session_id": "dup-002"}
EOF

# Verify fixture created
if [ ! -f "$DUPLICATE_HISTORY" ]; then
    echo "FAIL: Could not create duplicate errors fixture" >&2
    exit 1
fi

SESSION_MINER_PATH=".claude/agents/session-miner.md"
if [ ! -f "$SESSION_MINER_PATH" ]; then
    echo "FAIL: session-miner subagent not found at $SESSION_MINER_PATH" >&2
    rm -f "$DUPLICATE_HISTORY"
    exit 1
fi

# Test 1: Verify duplicate handling is documented
if ! grep -qi "duplicate.*error\|identical.*error\|same.*pattern\|group.*duplicate" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document duplicate error handling" >&2
    rm -f "$DUPLICATE_HISTORY"
    exit 1
fi

# Test 2: Verify occurrence aggregation is documented
if ! grep -qi "occurrence.*aggregate\|aggregate.*count\|sum.*occurrence" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document occurrence aggregation for duplicates" >&2
    rm -f "$DUPLICATE_HISTORY"
    exit 1
fi

# Test 3: Document expected behavior
echo "INFO: Test data contains:"
echo "  - 5 error entries"
echo "  - All with identical message: 'API rate limit exceeded'"
echo "  - Across 2 different sessions"
echo ""
echo "INFO: Expected results:"
echo "  - 1 error code in registry (ERR-001)"
echo "  - occurrences: 5"
echo "  - first_seen: 2025-01-02T10:00:00Z"
echo "  - last_seen: 2025-01-02T11:05:00Z"
echo "  - category: api"
echo "  - severity: high"

# Clean up
rm -f "$DUPLICATE_HISTORY"

echo "PASS: Duplicate error handling is properly documented"
exit 0
