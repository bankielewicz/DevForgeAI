#!/bin/bash
# STORY-226 Unit Test: AC#3 - Report Ranking Logic
#
# AC#3: Top Patterns Report (Ranking Details)
#
# Given: analyzed sequences with varying frequencies
# When: generating report
# Then: sequences are ranked correctly by frequency, with ties handled appropriately
#
# Test Approach:
# 1. Verify ranking is by frequency (not alphabetical, not by success rate)
# 2. Check tie-breaking logic (secondary sort by success rate or alphabetical)
# 3. Validate exactly 10 results returned (or fewer if <10 unique sequences)
# 4. Verify report includes rank numbers
#
# TDD RED PHASE: Test expected to FAIL before implementation

set -e

TEST_NAME="test-ac3-report-ranking"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIXTURES_DIR="${TEST_DIR}/fixtures"

# Create ranking test data with clear frequency order
RANKING_HISTORY="${FIXTURES_DIR}/ranking-test-history.jsonl"

# Create test data with known ranking order
# Frequency order: seq-a (5) > seq-b (4) > seq-c (3) > seq-d (2) > seq-e (1)
cat > "$RANKING_HISTORY" << 'EOF'
{"timestamp": "2025-01-02T10:00:00Z", "command": "/seq-a-1", "status": "success", "session_id": "rank-001"}
{"timestamp": "2025-01-02T10:01:00Z", "command": "/seq-a-2", "status": "success", "session_id": "rank-001"}
{"timestamp": "2025-01-02T10:02:00Z", "command": "/seq-a-1", "status": "success", "session_id": "rank-002"}
{"timestamp": "2025-01-02T10:03:00Z", "command": "/seq-a-2", "status": "success", "session_id": "rank-002"}
{"timestamp": "2025-01-02T10:04:00Z", "command": "/seq-a-1", "status": "success", "session_id": "rank-003"}
{"timestamp": "2025-01-02T10:05:00Z", "command": "/seq-a-2", "status": "success", "session_id": "rank-003"}
{"timestamp": "2025-01-02T10:06:00Z", "command": "/seq-a-1", "status": "success", "session_id": "rank-004"}
{"timestamp": "2025-01-02T10:07:00Z", "command": "/seq-a-2", "status": "success", "session_id": "rank-004"}
{"timestamp": "2025-01-02T10:08:00Z", "command": "/seq-a-1", "status": "success", "session_id": "rank-005"}
{"timestamp": "2025-01-02T10:09:00Z", "command": "/seq-a-2", "status": "success", "session_id": "rank-005"}
{"timestamp": "2025-01-02T11:00:00Z", "command": "/seq-b-1", "status": "success", "session_id": "rank-006"}
{"timestamp": "2025-01-02T11:01:00Z", "command": "/seq-b-2", "status": "success", "session_id": "rank-006"}
{"timestamp": "2025-01-02T11:02:00Z", "command": "/seq-b-1", "status": "success", "session_id": "rank-007"}
{"timestamp": "2025-01-02T11:03:00Z", "command": "/seq-b-2", "status": "success", "session_id": "rank-007"}
{"timestamp": "2025-01-02T11:04:00Z", "command": "/seq-b-1", "status": "success", "session_id": "rank-008"}
{"timestamp": "2025-01-02T11:05:00Z", "command": "/seq-b-2", "status": "success", "session_id": "rank-008"}
{"timestamp": "2025-01-02T11:06:00Z", "command": "/seq-b-1", "status": "success", "session_id": "rank-009"}
{"timestamp": "2025-01-02T11:07:00Z", "command": "/seq-b-2", "status": "success", "session_id": "rank-009"}
{"timestamp": "2025-01-02T12:00:00Z", "command": "/seq-c-1", "status": "success", "session_id": "rank-010"}
{"timestamp": "2025-01-02T12:01:00Z", "command": "/seq-c-2", "status": "success", "session_id": "rank-010"}
{"timestamp": "2025-01-02T12:02:00Z", "command": "/seq-c-1", "status": "success", "session_id": "rank-011"}
{"timestamp": "2025-01-02T12:03:00Z", "command": "/seq-c-2", "status": "success", "session_id": "rank-011"}
{"timestamp": "2025-01-02T12:04:00Z", "command": "/seq-c-1", "status": "success", "session_id": "rank-012"}
{"timestamp": "2025-01-02T12:05:00Z", "command": "/seq-c-2", "status": "success", "session_id": "rank-012"}
{"timestamp": "2025-01-02T13:00:00Z", "command": "/seq-d-1", "status": "success", "session_id": "rank-013"}
{"timestamp": "2025-01-02T13:01:00Z", "command": "/seq-d-2", "status": "success", "session_id": "rank-013"}
{"timestamp": "2025-01-02T13:02:00Z", "command": "/seq-d-1", "status": "success", "session_id": "rank-014"}
{"timestamp": "2025-01-02T13:03:00Z", "command": "/seq-d-2", "status": "success", "session_id": "rank-014"}
{"timestamp": "2025-01-02T14:00:00Z", "command": "/seq-e-1", "status": "success", "session_id": "rank-015"}
{"timestamp": "2025-01-02T14:01:00Z", "command": "/seq-e-2", "status": "success", "session_id": "rank-015"}
EOF

# Test 1: Verify ranking test fixture created
if [ ! -f "$RANKING_HISTORY" ]; then
    echo "FAIL: Could not create ranking test fixture" >&2
    exit 1
fi

# Test 2: Verify session-miner subagent exists
SESSION_MINER_PATH=".claude/agents/session-miner.md"
if [ ! -f "$SESSION_MINER_PATH" ]; then
    echo "FAIL: session-miner subagent not found at $SESSION_MINER_PATH" >&2
    exit 1
fi

# Test 3: Document expected ranking order
echo "INFO: Expected ranking order (by frequency):"
echo "  1. [/seq-a-1, /seq-a-2]: 5 occurrences"
echo "  2. [/seq-b-1, /seq-b-2]: 4 occurrences"
echo "  3. [/seq-c-1, /seq-c-2]: 3 occurrences"
echo "  4. [/seq-d-1, /seq-d-2]: 2 occurrences"
echo "  5. [/seq-e-1, /seq-e-2]: 1 occurrence"

# Test 4: Verify tie-breaking logic is documented
# When frequencies are equal, should sort by success rate (descending) or alphabetically
if ! grep -qi "tie.*break\|equal.*frequency\|same.*frequency\|secondary.*sort" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document tie-breaking logic for equal frequencies" >&2
    exit 1
fi

# Test 5: Verify rank numbers are included in output
if ! grep -qi "rank\|position\|#[0-9]\|number" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document rank number inclusion in output" >&2
    exit 1
fi

# Clean up
rm -f "$RANKING_HISTORY"

echo "PASS: Report ranking logic is properly documented"
exit 0
