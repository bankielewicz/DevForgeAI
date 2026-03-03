#!/bin/bash
# STORY-229 Unit Test: AC#4 - Error Code Registry
#
# AC#4: Error Code Registry
#
# Given: unique error patterns
# When: building registry
# Then: error codes (ERR-001, ERR-002) are assigned for tracking
#
# This test validates error code registry creation.
#
# Registry requirements:
# - Unique error codes (ERR-001, ERR-002, etc.)
# - Pattern matching to group similar errors
# - Occurrence counting
# - First/last seen timestamps
# - Category and severity association
#
# TDD RED PHASE: Test expected to FAIL before implementation

set -e

TEST_NAME="test-ac4-error-registry"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIXTURES_DIR="${TEST_DIR}/fixtures"
EXPECTED_REGISTRY="${FIXTURES_DIR}/expected-error-registry.json"

# Verify test fixture exists
if [ ! -f "$EXPECTED_REGISTRY" ]; then
    echo "FAIL: Expected registry file not found: $EXPECTED_REGISTRY" >&2
    exit 1
fi

SESSION_MINER_PATH=".claude/agents/session-miner.md"
if [ ! -f "$SESSION_MINER_PATH" ]; then
    echo "FAIL: session-miner subagent not found at $SESSION_MINER_PATH" >&2
    exit 1
fi

# Test 1: Verify session-miner documents error registry capability
if ! grep -qi "error.*registry\|registry.*error\|error.*code" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document error registry capability" >&2
    exit 1
fi

# Test 2: Verify error code format is documented (ERR-XXX)
if ! grep -qi "ERR-[0-9]\|error.*code.*format\|code.*ERR" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document error code format (ERR-XXX)" >&2
    exit 1
fi

# Test 3: Verify unique pattern identification is documented
if ! grep -qi "unique.*pattern\|pattern.*identify\|group.*similar" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document unique pattern identification" >&2
    exit 1
fi

# Test 4: Verify occurrence counting is documented
if ! grep -qi "occurrence.*count\|count.*occurrence\|frequency" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document occurrence counting" >&2
    exit 1
fi

# Test 5: Verify timestamp tracking is documented
if ! grep -qi "first.*seen\|last.*seen\|timestamp.*track" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document first/last seen timestamps" >&2
    exit 1
fi

# Test 6: Verify category association in registry is documented
if ! grep -qi "registry.*categor\|categor.*registry\|code.*categor" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document category association in registry" >&2
    exit 1
fi

# Test 7: Verify severity association in registry is documented
if ! grep -qi "registry.*severity\|severity.*registry\|code.*severity" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document severity association in registry" >&2
    exit 1
fi

echo "PASS: Error registry is properly documented in session-miner"
exit 0
