#!/bin/bash
# STORY-229 Integration Test: Insights Error Report
#
# Tests integration between session-miner error analysis and
# devforgeai-insights report generation.
#
# Expected report format:
# - Error Summary by Category
# - Error Summary by Severity
# - Top Error Patterns (by frequency)
# - Error Registry Reference
#
# TDD RED PHASE: Test expected to FAIL before implementation

set -e

TEST_NAME="test-insights-error-report"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIXTURES_DIR="${TEST_DIR}/fixtures"

SESSION_MINER_PATH=".claude/agents/session-miner.md"
if [ ! -f "$SESSION_MINER_PATH" ]; then
    echo "FAIL: session-miner subagent not found at $SESSION_MINER_PATH" >&2
    exit 1
fi

# Test 1: Verify error report generation is documented
if ! grep -qi "error.*report\|report.*error\|generate.*report" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document error report generation" >&2
    exit 1
fi

# Test 2: Verify category summary in report is documented
if ! grep -qi "category.*summary\|summary.*category\|by.*category" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document category summary in report" >&2
    exit 1
fi

# Test 3: Verify severity summary in report is documented
if ! grep -qi "severity.*summary\|summary.*severity\|by.*severity" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document severity summary in report" >&2
    exit 1
fi

# Test 4: Verify top patterns section in report is documented
if ! grep -qi "top.*pattern\|frequent.*error\|pattern.*frequency" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document top patterns in report" >&2
    exit 1
fi

# Test 5: Verify registry reference in report is documented
if ! grep -qi "registry.*reference\|error.*code.*reference\|registry.*section" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document registry reference in report" >&2
    exit 1
fi

# Test 6: Verify devforgeai-insights integration is documented
if ! grep -qi "devforgeai-insights\|insights.*integration\|insights.*report" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document devforgeai-insights integration" >&2
    exit 1
fi

echo "PASS: Insights error report is properly documented"
exit 0
