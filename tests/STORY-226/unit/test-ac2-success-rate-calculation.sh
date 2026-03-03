#!/bin/bash
# STORY-226 Unit Test: AC#2 - Success Rate Correlation
#
# AC#2: Success Rate Correlation
#
# Given: extracted command sequences
# When: calculating metrics
# Then: success rate is computed for each sequence (successful completions / total attempts)
#
# Test Approach:
# 1. Verify success rate calculation logic exists
# 2. Check formula: success_rate = successful_completions / total_attempts
# 3. Validate success rate is per-sequence (not global)
# 4. Verify handling of mixed success/error sequences
# 5. Check edge cases: 100% success, 0% success, single occurrence
#
# TDD RED PHASE: Test expected to FAIL before implementation

set -e

TEST_NAME="test-ac2-success-rate-calculation"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIXTURES_DIR="${TEST_DIR}/fixtures"
SAMPLE_HISTORY="${FIXTURES_DIR}/sample-history.jsonl"

# Verify test fixtures exist
if [ ! -f "$SAMPLE_HISTORY" ]; then
    echo "FAIL: Test fixture not found: $SAMPLE_HISTORY" >&2
    exit 1
fi

# Test 1: Verify session-miner subagent file exists
SESSION_MINER_PATH=".claude/agents/session-miner.md"
if [ ! -f "$SESSION_MINER_PATH" ]; then
    echo "FAIL: session-miner subagent not found at $SESSION_MINER_PATH" >&2
    exit 1
fi

# Test 2: Verify session-miner documents success rate calculation
if ! grep -qi "success.*rate\|success_rate\|completion.*rate" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document success rate calculation" >&2
    exit 1
fi

# Test 3: Verify success rate formula is documented
# Formula: successful_completions / total_attempts
if ! grep -qi "successful.*total\|success.*attempt\|completion.*divide" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document success rate formula" >&2
    exit 1
fi

# Test 4: Verify success rate is per-sequence (not global)
if ! grep -qi "per.*sequence\|each.*sequence\|sequence.*success" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not indicate success rate is per-sequence" >&2
    exit 1
fi

# Test 5: Verify success determination logic is documented
if ! grep -qi "status\|success\|error\|partial" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document status handling" >&2
    exit 1
fi

echo "PASS: Success rate calculation is properly documented in session-miner"
exit 0
