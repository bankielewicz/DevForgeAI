#!/bin/bash
# STORY-229 Unit Test: AC#1 - Error Context Capture
#
# AC#1: Error Message Extraction
#
# Given: session data with status: "error" entries
# When: extracting errors
# Then: error messages are captured with context (command, timestamp, session)
#
# This test specifically validates that ALL required context fields are captured.
#
# Required context fields:
# - command: The command that produced the error (e.g., "/dev STORY-100")
# - timestamp: When the error occurred (ISO 8601 format)
# - session_id: Which session the error belongs to
# - error_message: The actual error message text
#
# TDD RED PHASE: Test expected to FAIL before implementation

set -e

TEST_NAME="test-ac1-error-context-capture"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIXTURES_DIR="${TEST_DIR}/fixtures"
SAMPLE_HISTORY="${FIXTURES_DIR}/sample-error-history.jsonl"

# Verify test fixture exists
if [ ! -f "$SAMPLE_HISTORY" ]; then
    echo "FAIL: Test fixture not found: $SAMPLE_HISTORY" >&2
    exit 1
fi

SESSION_MINER_PATH=".claude/agents/session-miner.md"
if [ ! -f "$SESSION_MINER_PATH" ]; then
    echo "FAIL: session-miner subagent not found at $SESSION_MINER_PATH" >&2
    exit 1
fi

# Test 1: Verify command field is documented as required context
if ! grep -qi "command.*field\|capture.*command\|extract.*command" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document command field as required context" >&2
    exit 1
fi

# Test 2: Verify timestamp field is documented as required context
if ! grep -qi "timestamp.*field\|capture.*timestamp\|extract.*timestamp" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document timestamp field as required context" >&2
    exit 1
fi

# Test 3: Verify session_id field is documented as required context
if ! grep -qi "session_id\|session.*identifier\|session.*id" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document session_id as required context" >&2
    exit 1
fi

# Test 4: Verify error extraction preserves all context fields
if ! grep -qi "preserve.*context\|context.*fields\|all.*fields" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document preservation of all context fields" >&2
    exit 1
fi

# Test 5: Verify sample fixture has expected structure
ERROR_COUNT=$(grep -c '"status": "error"' "$SAMPLE_HISTORY" || echo "0")
if [ "$ERROR_COUNT" -lt 1 ]; then
    echo "FAIL: Sample history should contain at least 1 error entry" >&2
    exit 1
fi

# Test 6: Verify errors have required context in fixture
FIRST_ERROR=$(grep '"status": "error"' "$SAMPLE_HISTORY" | head -1)
if ! echo "$FIRST_ERROR" | grep -q '"command":'; then
    echo "FAIL: Sample error missing 'command' field" >&2
    exit 1
fi
if ! echo "$FIRST_ERROR" | grep -q '"timestamp":'; then
    echo "FAIL: Sample error missing 'timestamp' field" >&2
    exit 1
fi
if ! echo "$FIRST_ERROR" | grep -q '"session_id":'; then
    echo "FAIL: Sample error missing 'session_id' field" >&2
    exit 1
fi
if ! echo "$FIRST_ERROR" | grep -q '"error_message":'; then
    echo "FAIL: Sample error missing 'error_message' field" >&2
    exit 1
fi

echo "PASS: Error context capture is properly documented and fixture is valid"
exit 0
