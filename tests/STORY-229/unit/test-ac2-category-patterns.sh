#!/bin/bash
# STORY-229 Unit Test: AC#2 - Category Pattern Matching
#
# AC#2: Category Classification
#
# This test validates specific pattern matching rules for each category.
#
# Pattern matching rules:
# - api: "rate limit", "API", "ECONNREFUSED", "JSON response", "connection"
# - validation: "Validation failed", "invalid", "missing.*field", "threshold"
# - timeout: "timeout", "timed out", ends with "ms"
# - context-overflow: "context.*overflow", "token", "window"
# - file-not-found: "File not found", "not found", "missing"
#
# TDD RED PHASE: Test expected to FAIL before implementation

set -e

TEST_NAME="test-ac2-category-patterns"
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

# Test 1: Verify API error patterns are documented
# Should match: "rate limit", "ECONNREFUSED", "Invalid JSON response"
if ! grep -qi "rate.limit\|ECONNREFUSED\|invalid.*json\|api.*pattern" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document API error patterns" >&2
    exit 1
fi

# Test 2: Verify validation error patterns are documented
# Should match: "Validation failed", "missing field", "threshold"
if ! grep -qi "Validation.failed\|missing.*field\|threshold\|validation.*pattern" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document validation error patterns" >&2
    exit 1
fi

# Test 3: Verify timeout error patterns are documented
# Should match: "timeout", "timed out", duration patterns
if ! grep -qi "timeout.*pattern\|timed.*out\|duration.*exceed" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document timeout error patterns" >&2
    exit 1
fi

# Test 4: Verify context overflow patterns are documented
# Should match: "context window overflow", "200K tokens"
if ! grep -qi "context.*window\|token.*exceed\|overflow.*pattern" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document context overflow patterns" >&2
    exit 1
fi

# Test 5: Verify file-not-found patterns are documented
# Should match: "File not found", "not found:", "missing"
if ! grep -qi "file.*not.*found.*pattern\|not.*found\|missing.*pattern" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document file-not-found patterns" >&2
    exit 1
fi

# Test 6: Verify category assignments in fixture
# Expected: 4 API, 2 validation, 2 timeout, 1 context-overflow, 2 file-not-found, 1 other
API_COUNT=$(grep -c "rate limit\|ECONNREFUSED\|Invalid JSON" "$FIXTURES_DIR/sample-error-history.jsonl" || echo "0")
if [ "$API_COUNT" -lt 3 ]; then
    echo "FAIL: Expected at least 3 API errors in sample data" >&2
    exit 1
fi

echo "PASS: Category patterns are properly documented"
exit 0
