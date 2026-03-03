#!/bin/bash
# STORY-226 Edge Case Test: Fewer Than 10 Unique Patterns
#
# Given: history.jsonl with only 3 unique command sequences
# When: Generating top 10 patterns report
# Then: Display all 3 patterns (not pad to 10, not error)
#
# TDD RED PHASE: Test expected to FAIL before implementation

set -e

TEST_NAME="test-fewer-than-10-patterns"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIXTURES_DIR="${TEST_DIR}/fixtures"

# Create history with only 3 unique patterns
FEW_PATTERNS_HISTORY="${FIXTURES_DIR}/few-patterns-history.jsonl"

cat > "$FEW_PATTERNS_HISTORY" << 'EOF'
{"timestamp": "2025-01-02T10:00:00Z", "command": "/dev", "status": "success", "session_id": "few-001"}
{"timestamp": "2025-01-02T10:01:00Z", "command": "/qa", "status": "success", "session_id": "few-001"}
{"timestamp": "2025-01-02T11:00:00Z", "command": "/dev", "status": "success", "session_id": "few-002"}
{"timestamp": "2025-01-02T11:01:00Z", "command": "/qa", "status": "success", "session_id": "few-002"}
{"timestamp": "2025-01-02T12:00:00Z", "command": "/ideate", "status": "success", "session_id": "few-003"}
{"timestamp": "2025-01-02T12:01:00Z", "command": "/create-epic", "status": "success", "session_id": "few-003"}
{"timestamp": "2025-01-02T13:00:00Z", "command": "/qa", "status": "success", "session_id": "few-004"}
{"timestamp": "2025-01-02T13:01:00Z", "command": "/release", "status": "success", "session_id": "few-004"}
EOF

# Verify fixture created
if [ ! -f "$FEW_PATTERNS_HISTORY" ]; then
    echo "FAIL: Could not create few-patterns history fixture" >&2
    exit 1
fi

# Test 1: Verify session-miner subagent exists
SESSION_MINER_PATH=".claude/agents/session-miner.md"
if [ ! -f "$SESSION_MINER_PATH" ]; then
    echo "FAIL: session-miner subagent not found at $SESSION_MINER_PATH" >&2
    rm -f "$FEW_PATTERNS_HISTORY"
    exit 1
fi

# Test 2: Document expected behavior
echo "INFO: Test data contains only 3 unique 2-gram patterns:"
echo "  1. [/dev, /qa]: 2 occurrences"
echo "  2. [/ideate, /create-epic]: 1 occurrence"
echo "  3. [/qa, /release]: 1 occurrence"
echo ""
echo "INFO: Expected top 10 report:"
echo "  - Display all 3 patterns (not error, not pad)"
echo "  - Rank 1: [/dev, /qa] (freq: 2)"
echo "  - Rank 2: [/ideate, /create-epic] (freq: 1)"
echo "  - Rank 3: [/qa, /release] (freq: 1)"
echo "  - No ranks 4-10 (only 3 patterns exist)"

# Test 3: Verify handling of fewer than 10 patterns is documented
if ! grep -qi "fewer.*than.*10\|less.*than.*10\|under.*10\|minimum.*pattern" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document handling fewer than 10 patterns" >&2
    rm -f "$FEW_PATTERNS_HISTORY"
    exit 1
fi

# Clean up
rm -f "$FEW_PATTERNS_HISTORY"

echo "PASS: Fewer than 10 patterns handling is properly documented"
exit 0
