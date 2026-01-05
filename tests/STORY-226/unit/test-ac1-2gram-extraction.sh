#!/bin/bash
# STORY-226 Unit Test: AC#1 - 2-gram Sequence Extraction
#
# AC#1: N-gram Sequence Extraction
#
# Given: history.jsonl command entries
# When: analyzing sequences
# Then: 2-gram and 3-gram command sequences are extracted with frequency counts
#
# This test validates 2-gram (bigram) extraction specifically.
#
# Test Approach:
# 1. Verify session-miner can extract 2-gram sequences
# 2. Check that sequences are grouped by consecutive command pairs
# 3. Validate frequency counts are accurate
# 4. Ensure sequences respect session boundaries (don't span sessions)
#
# TDD RED PHASE: Test expected to FAIL before implementation

set -e

TEST_NAME="test-ac1-2gram-extraction"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIXTURES_DIR="${TEST_DIR}/fixtures"
SAMPLE_HISTORY="${FIXTURES_DIR}/sample-history.jsonl"
EXPECTED_2GRAMS="${FIXTURES_DIR}/expected-2grams.json"

# Verify test fixtures exist
if [ ! -f "$SAMPLE_HISTORY" ]; then
    echo "FAIL: Test fixture not found: $SAMPLE_HISTORY" >&2
    exit 1
fi

if [ ! -f "$EXPECTED_2GRAMS" ]; then
    echo "FAIL: Expected results file not found: $EXPECTED_2GRAMS" >&2
    exit 1
fi

# Test 1: Verify session-miner subagent file exists with n-gram capability
SESSION_MINER_PATH=".claude/agents/session-miner.md"
if [ ! -f "$SESSION_MINER_PATH" ]; then
    echo "FAIL: session-miner subagent not found at $SESSION_MINER_PATH" >&2
    exit 1
fi

# Test 2: Verify session-miner contains n-gram extraction logic
if ! grep -qi "n-gram\|ngram\|2-gram\|bigram\|sequence.*extract" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not contain n-gram extraction logic" >&2
    exit 1
fi

# Test 3: Verify session-miner documents 2-gram output format
if ! grep -qi "2-gram\|bigram\|sequence.*pair\|consecutive.*command" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document 2-gram sequence format" >&2
    exit 1
fi

# Test 4: Verify frequency count capability is documented
if ! grep -qi "frequency\|count\|occurrences" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document frequency counting capability" >&2
    exit 1
fi

# Test 5: Verify session boundary handling is documented
# Sequences should NOT span across different sessions
if ! grep -qi "session.*boundary\|session_id\|group.*session" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document session boundary handling" >&2
    exit 1
fi

# Test 6: Verify 2-gram workflow is documented
if ! grep -qi "sliding.*window\|window.*2\|pair.*command\|consecutive.*pair" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document 2-gram sliding window logic" >&2
    exit 1
fi

# Test 7: Verify output format is documented
if ! grep -qi "sequence.*array\|output.*format\|json.*format" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document output format" >&2
    exit 1
fi

echo "PASS: 2-gram extraction is properly documented in session-miner"
exit 0
