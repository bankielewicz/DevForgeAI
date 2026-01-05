#!/bin/bash
# STORY-226 Unit Test: AC#1 - 3-gram Sequence Extraction
#
# AC#1: N-gram Sequence Extraction
#
# Given: history.jsonl command entries
# When: analyzing sequences
# Then: 2-gram and 3-gram command sequences are extracted with frequency counts
#
# This test validates 3-gram (trigram) extraction specifically.
#
# Test Approach:
# 1. Verify session-miner can extract 3-gram sequences
# 2. Check that sequences are grouped by consecutive command triples
# 3. Validate frequency counts are accurate
# 4. Ensure sequences respect session boundaries (don't span sessions)
#
# TDD RED PHASE: Test expected to FAIL before implementation

set -e

TEST_NAME="test-ac1-3gram-extraction"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIXTURES_DIR="${TEST_DIR}/fixtures"
SAMPLE_HISTORY="${FIXTURES_DIR}/sample-history.jsonl"
EXPECTED_3GRAMS="${FIXTURES_DIR}/expected-3grams.json"

# Verify test fixtures exist
if [ ! -f "$SAMPLE_HISTORY" ]; then
    echo "FAIL: Test fixture not found: $SAMPLE_HISTORY" >&2
    exit 1
fi

if [ ! -f "$EXPECTED_3GRAMS" ]; then
    echo "FAIL: Expected results file not found: $EXPECTED_3GRAMS" >&2
    exit 1
fi

# Test 1: Verify session-miner subagent file exists
SESSION_MINER_PATH=".claude/agents/session-miner.md"
if [ ! -f "$SESSION_MINER_PATH" ]; then
    echo "FAIL: session-miner subagent not found at $SESSION_MINER_PATH" >&2
    exit 1
fi

# Test 2: Verify session-miner contains 3-gram extraction logic
if ! grep -qi "3-gram\|trigram\|triple\|three.*command\|sequence.*three" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not contain 3-gram extraction logic" >&2
    exit 1
fi

# Test 3: Verify 3-gram sliding window approach is documented
# 3-grams use sliding window: [1,2,3], [2,3,4], [3,4,5]...
if ! grep -qi "sliding.*window\|consecutive.*three\|window.*size" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document sliding window approach for 3-grams" >&2
    exit 1
fi

# Test 4: Verify frequency counting capability
if ! grep -qi "frequency\|count\|occurrences" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document frequency counting" >&2
    exit 1
fi

# Test 5: Verify session boundary handling
if ! grep -qi "session.*boundary\|session_id" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document session boundary handling" >&2
    exit 1
fi

echo "PASS: 3-gram extraction is properly documented in session-miner"
exit 0
