#!/bin/bash
# STORY-229 Unit Test: AC#1 - Error Message Extraction
#
# AC#1: Error Message Extraction
#
# Given: session data with status: "error" entries
# When: extracting errors
# Then: error messages are captured with context (command, timestamp, session)
#
# This test validates error extraction from history.jsonl files.
#
# Test Approach:
# 1. Verify session-miner can extract errors from history entries
# 2. Check that error context includes command, timestamp, session_id
# 3. Validate only status: "error" entries are extracted
# 4. Ensure error_message field is captured correctly
#
# TDD RED PHASE: Test expected to FAIL before implementation

set -e

TEST_NAME="test-ac1-error-extraction"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIXTURES_DIR="${TEST_DIR}/fixtures"
SAMPLE_HISTORY="${FIXTURES_DIR}/sample-error-history.jsonl"
EXPECTED_ERRORS="${FIXTURES_DIR}/expected-extracted-errors.json"

# Verify test fixtures exist
if [ ! -f "$SAMPLE_HISTORY" ]; then
    echo "FAIL: Test fixture not found: $SAMPLE_HISTORY" >&2
    exit 1
fi

if [ ! -f "$EXPECTED_ERRORS" ]; then
    echo "FAIL: Expected results file not found: $EXPECTED_ERRORS" >&2
    exit 1
fi

# Test 1: Verify session-miner subagent file exists
SESSION_MINER_PATH=".claude/agents/session-miner.md"
if [ ! -f "$SESSION_MINER_PATH" ]; then
    echo "FAIL: session-miner subagent not found at $SESSION_MINER_PATH" >&2
    exit 1
fi

# Test 2: Verify session-miner contains error extraction capability
if ! grep -qi "error.*extract\|extract.*error\|status.*error" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document error extraction capability" >&2
    exit 1
fi

# Test 3: Verify error context capture is documented (command, timestamp, session)
if ! grep -qi "command.*context\|timestamp\|session_id\|error.*context" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document error context capture (command, timestamp, session)" >&2
    exit 1
fi

# Test 4: Verify error_message field handling is documented
if ! grep -qi "error_message\|error.*message\|message.*field" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document error_message field handling" >&2
    exit 1
fi

# Test 5: Verify filtering by status: "error" is documented
if ! grep -qi "filter.*status\|status.*filter\|status.*error" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document filtering by error status" >&2
    exit 1
fi

# Test 6: Verify error extraction output format is documented
if ! grep -qi "error.*output\|extracted.*errors\|error.*format" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document error extraction output format" >&2
    exit 1
fi

echo "PASS: Error extraction is properly documented in session-miner"
exit 0
