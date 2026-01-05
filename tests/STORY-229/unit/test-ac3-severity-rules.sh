#!/bin/bash
# STORY-229 Unit Test: AC#3 - Severity Assignment Rules
#
# AC#3: Severity Assignment
#
# This test validates specific severity assignment rules and mapping.
#
# Severity mapping rules:
# - critical: context-overflow, API connection failures (ECONNREFUSED)
# - high: timeout, API rate limits
# - medium: validation failures, file-not-found
# - low: other/unknown errors
#
# TDD RED PHASE: Test expected to FAIL before implementation

set -e

TEST_NAME="test-ac3-severity-rules"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIXTURES_DIR="${TEST_DIR}/fixtures"
EXPECTED_SEVERITY="${FIXTURES_DIR}/expected-severity.json"

# Verify test fixture exists
if [ ! -f "$EXPECTED_SEVERITY" ]; then
    echo "FAIL: Expected severity file not found: $EXPECTED_SEVERITY" >&2
    exit 1
fi

SESSION_MINER_PATH=".claude/agents/session-miner.md"
if [ ! -f "$SESSION_MINER_PATH" ]; then
    echo "FAIL: session-miner subagent not found at $SESSION_MINER_PATH" >&2
    exit 1
fi

# Test 1: Verify context-overflow maps to critical severity
if ! grep -qi "context.*overflow.*critical\|critical.*context.*overflow\|overflow.*halt" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document context-overflow as critical severity" >&2
    exit 1
fi

# Test 2: Verify connection failures map to critical severity
if ! grep -qi "connection.*critical\|critical.*connect\|ECONNREFUSED.*critical" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document connection failures as critical severity" >&2
    exit 1
fi

# Test 3: Verify timeouts map to high severity
if ! grep -qi "timeout.*high\|high.*timeout\|timeout.*block" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document timeouts as high severity" >&2
    exit 1
fi

# Test 4: Verify rate limits map to high severity
if ! grep -qi "rate.*limit.*high\|high.*rate.*limit\|rate.*limit.*block" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document rate limits as high severity" >&2
    exit 1
fi

# Test 5: Verify validation failures map to medium severity
if ! grep -qi "validation.*medium\|medium.*validation\|validation.*recover" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document validation failures as medium severity" >&2
    exit 1
fi

# Test 6: Verify file-not-found maps to medium severity
if ! grep -qi "file.*not.*found.*medium\|medium.*file.*not.*found\|missing.*medium" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document file-not-found as medium severity" >&2
    exit 1
fi

# Test 7: Verify other/unknown maps to low severity
if ! grep -qi "other.*low\|low.*other\|unknown.*low" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document other/unknown as low severity" >&2
    exit 1
fi

echo "PASS: Severity assignment rules are properly documented"
exit 0
