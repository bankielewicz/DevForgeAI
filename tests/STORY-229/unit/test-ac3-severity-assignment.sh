#!/bin/bash
# STORY-229 Unit Test: AC#3 - Severity Assignment
#
# AC#3: Severity Assignment
#
# Given: categorized errors
# When: assigning severity
# Then: errors are marked: critical, high, medium, low based on impact
#
# This test validates severity assignment rules.
#
# Severity levels:
# - critical: Workflow halting errors (context overflow, connection failures)
# - high: Operation blocking errors (timeouts, rate limits)
# - medium: Recoverable errors (validation failures, file not found)
# - low: Minor errors (unknown, other)
#
# TDD RED PHASE: Test expected to FAIL before implementation

set -e

TEST_NAME="test-ac3-severity-assignment"
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

# Test 1: Verify session-miner documents severity assignment capability
if ! grep -qi "severity\|impact.*level\|error.*level" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document severity assignment capability" >&2
    exit 1
fi

# Test 2: Verify 'critical' severity level is defined
if ! grep -qi "critical.*severity\|critical.*error\|halt.*workflow" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document 'critical' severity level" >&2
    exit 1
fi

# Test 3: Verify 'high' severity level is defined
if ! grep -qi "high.*severity\|high.*error\|block.*operation" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document 'high' severity level" >&2
    exit 1
fi

# Test 4: Verify 'medium' severity level is defined
if ! grep -qi "medium.*severity\|medium.*error\|recover" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document 'medium' severity level" >&2
    exit 1
fi

# Test 5: Verify 'low' severity level is defined
if ! grep -qi "low.*severity\|low.*error\|minor" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document 'low' severity level" >&2
    exit 1
fi

# Test 6: Verify severity-to-category mapping is documented
if ! grep -qi "severity.*categor\|categor.*severity\|map.*severity" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document severity-to-category mapping" >&2
    exit 1
fi

# Test 7: Verify severity rules are documented
if ! grep -qi "severity.*rule\|rule.*severity\|assign.*severity" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document severity assignment rules" >&2
    exit 1
fi

echo "PASS: Severity assignment is properly documented in session-miner"
exit 0
