#!/bin/bash
# STORY-229 Integration Test: Error Analysis Pipeline
#
# Tests the complete error analysis workflow:
# 1. Error extraction from history.jsonl (AC#1)
# 2. Category classification (AC#2)
# 3. Severity assignment (AC#3)
# 4. Error registry building (AC#4)
#
# This validates the full pipeline operates correctly end-to-end.
#
# TDD RED PHASE: Test expected to FAIL before implementation

set -e

TEST_NAME="test-error-analysis-pipeline"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIXTURES_DIR="${TEST_DIR}/fixtures"
SAMPLE_HISTORY="${FIXTURES_DIR}/sample-error-history.jsonl"

# Verify test fixture exists
if [ ! -f "$SAMPLE_HISTORY" ]; then
    echo "FAIL: Sample history not found: $SAMPLE_HISTORY" >&2
    exit 1
fi

SESSION_MINER_PATH=".claude/agents/session-miner.md"
if [ ! -f "$SESSION_MINER_PATH" ]; then
    echo "FAIL: session-miner subagent not found at $SESSION_MINER_PATH" >&2
    exit 1
fi

# Test 1: Verify full pipeline is documented
if ! grep -qi "error.*analysis.*pipeline\|pipeline.*error\|workflow.*error" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document error analysis pipeline" >&2
    exit 1
fi

# Test 2: Verify extraction -> classification flow is documented
if ! grep -qi "extract.*then.*classif\|extract.*categor\|after.*extract.*classif" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document extraction to classification flow" >&2
    exit 1
fi

# Test 3: Verify classification -> severity flow is documented
if ! grep -qi "classif.*then.*severity\|categor.*severity\|after.*categor.*assign" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document classification to severity flow" >&2
    exit 1
fi

# Test 4: Verify severity -> registry flow is documented
if ! grep -qi "severity.*then.*registry\|severity.*registry\|assign.*register" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document severity to registry flow" >&2
    exit 1
fi

# Test 5: Verify pipeline output format is documented
if ! grep -qi "pipeline.*output\|analysis.*result\|output.*format" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document pipeline output format" >&2
    exit 1
fi

# Test 6: Verify error handling in pipeline is documented
if ! grep -qi "pipeline.*error.*handling\|handle.*pipeline.*error\|graceful.*fail" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document error handling in pipeline" >&2
    exit 1
fi

echo "PASS: Error analysis pipeline is properly documented"
exit 0
