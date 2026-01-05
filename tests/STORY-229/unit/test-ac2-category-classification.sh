#!/bin/bash
# STORY-229 Unit Test: AC#2 - Category Classification
#
# AC#2: Category Classification
#
# Given: extracted errors
# When: classifying
# Then: errors are categorized: API, validation, timeout, context-overflow, file-not-found, other
#
# This test validates error categorization logic.
#
# Required categories:
# - api: API rate limits, connection failures, invalid responses
# - validation: Missing fields, threshold failures
# - timeout: Request timeouts, execution timeouts
# - context-overflow: Token limit exceeded, context window overflow
# - file-not-found: Missing files, stories, agents
# - other: Uncategorized errors
#
# TDD RED PHASE: Test expected to FAIL before implementation

set -e

TEST_NAME="test-ac2-category-classification"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIXTURES_DIR="${TEST_DIR}/fixtures"
EXPECTED_CATEGORIES="${FIXTURES_DIR}/expected-categories.json"

# Verify test fixture exists
if [ ! -f "$EXPECTED_CATEGORIES" ]; then
    echo "FAIL: Expected categories file not found: $EXPECTED_CATEGORIES" >&2
    exit 1
fi

SESSION_MINER_PATH=".claude/agents/session-miner.md"
if [ ! -f "$SESSION_MINER_PATH" ]; then
    echo "FAIL: session-miner subagent not found at $SESSION_MINER_PATH" >&2
    exit 1
fi

# Test 1: Verify session-miner documents error categorization capability
if ! grep -qi "categor\|classif\|error.*type" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document error categorization capability" >&2
    exit 1
fi

# Test 2: Verify 'api' category is defined
if ! grep -qi "api.*error\|api.*categor\|rate.*limit\|connection.*fail" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document 'api' error category" >&2
    exit 1
fi

# Test 3: Verify 'validation' category is defined
if ! grep -qi "validation.*error\|validation.*categor\|validation.*fail" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document 'validation' error category" >&2
    exit 1
fi

# Test 4: Verify 'timeout' category is defined
if ! grep -qi "timeout.*error\|timeout.*categor\|request.*timeout" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document 'timeout' error category" >&2
    exit 1
fi

# Test 5: Verify 'context-overflow' category is defined
if ! grep -qi "context.*overflow\|token.*limit\|context.*window" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document 'context-overflow' error category" >&2
    exit 1
fi

# Test 6: Verify 'file-not-found' category is defined
if ! grep -qi "file.*not.*found\|missing.*file\|not.*found" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document 'file-not-found' error category" >&2
    exit 1
fi

# Test 7: Verify 'other' category exists as fallback
if ! grep -qi "other\|uncategor\|fallback\|default.*categor" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document 'other' fallback category" >&2
    exit 1
fi

# Test 8: Verify category pattern matching is documented
if ! grep -qi "pattern.*match\|regex\|categor.*pattern\|match.*pattern" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document category pattern matching logic" >&2
    exit 1
fi

echo "PASS: Category classification is properly documented in session-miner"
exit 0
