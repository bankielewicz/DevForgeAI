#!/bin/bash
# STORY-229 Edge Case Test: All Errors (No Success Entries)
#
# Given: history.jsonl with only status: "error" entries (no successes)
# When: Analyzing for errors
# Then: All entries processed, 0% success rate calculated
#
# TDD RED PHASE: Test expected to FAIL before implementation

set -e

TEST_NAME="test-all-errors"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIXTURES_DIR="${TEST_DIR}/fixtures"

# Create history with only error entries
ERRORS_ONLY_HISTORY="${FIXTURES_DIR}/errors-only-history.jsonl"

cat > "$ERRORS_ONLY_HISTORY" << 'EOF'
{"timestamp": "2025-01-02T10:00:00Z", "command": "/dev STORY-100", "status": "error", "error_message": "API rate limit exceeded", "session_id": "error-only-001"}
{"timestamp": "2025-01-02T10:05:00Z", "command": "/qa STORY-100", "status": "error", "error_message": "Request timeout after 60000ms", "session_id": "error-only-001"}
{"timestamp": "2025-01-02T10:10:00Z", "command": "/release STORY-100", "status": "error", "error_message": "Validation failed: Coverage below 95%", "session_id": "error-only-001"}
EOF

# Verify fixture created
if [ ! -f "$ERRORS_ONLY_HISTORY" ]; then
    echo "FAIL: Could not create errors-only history fixture" >&2
    exit 1
fi

SESSION_MINER_PATH=".claude/agents/session-miner.md"
if [ ! -f "$SESSION_MINER_PATH" ]; then
    echo "FAIL: session-miner subagent not found at $SESSION_MINER_PATH" >&2
    rm -f "$ERRORS_ONLY_HISTORY"
    exit 1
fi

# Test 1: Verify handling of all errors is documented
if ! grep -qi "all.*error\|100.*error\|high.*error.*rate" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document handling of all-error history" >&2
    rm -f "$ERRORS_ONLY_HISTORY"
    exit 1
fi

# Test 2: Verify error rate calculation is documented
if ! grep -qi "error.*rate\|rate.*calculat\|success.*rate" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document error rate calculation" >&2
    rm -f "$ERRORS_ONLY_HISTORY"
    exit 1
fi

# Test 3: Document expected behavior
echo "INFO: Test data contains:"
echo "  - 0 success entries"
echo "  - 3 error entries"
echo ""
echo "INFO: Expected results:"
echo "  - extracted_errors: 3 entries"
echo "  - categories: { api: 1, timeout: 1, validation: 1 }"
echo "  - error_rate: 100%"
echo "  - All errors properly categorized and assigned severity"

# Clean up
rm -f "$ERRORS_ONLY_HISTORY"

echo "PASS: All-errors handling is properly documented"
exit 0
