#!/bin/bash
# STORY-229 Unit Test: AC#4 - Error Registry Tracking
#
# AC#4: Error Code Registry
#
# This test validates error registry tracking capabilities.
#
# Tracking requirements:
# - Automatic error code assignment (sequential)
# - Occurrence aggregation for similar errors
# - Temporal tracking (first_seen, last_seen)
# - Registry persistence and versioning
#
# TDD RED PHASE: Test expected to FAIL before implementation

set -e

TEST_NAME="test-ac4-registry-tracking"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIXTURES_DIR="${TEST_DIR}/fixtures"
EXPECTED_REGISTRY="${FIXTURES_DIR}/expected-error-registry.json"
SAMPLE_HISTORY="${FIXTURES_DIR}/sample-error-history.jsonl"

# Verify test fixtures exist
if [ ! -f "$EXPECTED_REGISTRY" ]; then
    echo "FAIL: Expected registry file not found: $EXPECTED_REGISTRY" >&2
    exit 1
fi

if [ ! -f "$SAMPLE_HISTORY" ]; then
    echo "FAIL: Sample history file not found: $SAMPLE_HISTORY" >&2
    exit 1
fi

SESSION_MINER_PATH=".claude/agents/session-miner.md"
if [ ! -f "$SESSION_MINER_PATH" ]; then
    echo "FAIL: session-miner subagent not found at $SESSION_MINER_PATH" >&2
    exit 1
fi

# Test 1: Verify automatic code assignment is documented
if ! grep -qi "auto.*assign\|assign.*code\|sequential.*code\|increment.*code" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document automatic error code assignment" >&2
    exit 1
fi

# Test 2: Verify occurrence aggregation is documented
if ! grep -qi "aggregate.*occurrence\|occurrence.*aggregate\|similar.*group\|group.*error" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document occurrence aggregation" >&2
    exit 1
fi

# Test 3: Verify registry persistence is documented
if ! grep -qi "persist.*registry\|registry.*persist\|save.*registry\|registry.*file" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document registry persistence" >&2
    exit 1
fi

# Test 4: Verify registry versioning is documented
if ! grep -qi "registry.*version\|version.*registry\|registry.*update" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document registry versioning" >&2
    exit 1
fi

# Test 5: Verify expected error codes in fixture
EXPECTED_CODES=$(grep -o '"code": "ERR-[0-9]*"' "$EXPECTED_REGISTRY" | wc -l)
if [ "$EXPECTED_CODES" -lt 5 ]; then
    echo "FAIL: Expected at least 5 unique error codes in registry fixture" >&2
    exit 1
fi

# Test 6: Verify occurrence counts in fixture
TOTAL_OCCURRENCES=$(grep -o '"occurrences": [0-9]*' "$EXPECTED_REGISTRY" | awk -F': ' '{sum += $2} END {print sum}')
if [ "$TOTAL_OCCURRENCES" -lt 10 ]; then
    echo "FAIL: Expected at least 10 total occurrences in registry fixture" >&2
    exit 1
fi

echo "PASS: Error registry tracking is properly documented"
exit 0
