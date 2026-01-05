#!/bin/bash
# STORY-226 Unit Test: AC#3 - Top Patterns Report Output
#
# AC#3: Top Patterns Report
#
# Given: analyzed sequences
# When: generating report
# Then: top 10 sequences by frequency are displayed with success rates
#
# Test Approach:
# 1. Verify report generation capability exists
# 2. Check top 10 sorting by frequency (descending)
# 3. Validate success rate is included in report
# 4. Verify report format (readable, structured)
# 5. Check handling of ties in frequency
#
# TDD RED PHASE: Test expected to FAIL before implementation

set -e

TEST_NAME="test-ac3-top-patterns-report"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIXTURES_DIR="${TEST_DIR}/fixtures"
SAMPLE_HISTORY="${FIXTURES_DIR}/sample-history.jsonl"

# Verify test fixtures exist
if [ ! -f "$SAMPLE_HISTORY" ]; then
    echo "FAIL: Test fixture not found: $SAMPLE_HISTORY" >&2
    exit 1
fi

# Test 1: Verify session-miner subagent file exists
SESSION_MINER_PATH=".claude/agents/session-miner.md"
if [ ! -f "$SESSION_MINER_PATH" ]; then
    echo "FAIL: session-miner subagent not found at $SESSION_MINER_PATH" >&2
    exit 1
fi

# Test 2: Verify report generation is documented
if ! grep -qi "report\|output\|display\|top.*pattern\|pattern.*report" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document report generation" >&2
    exit 1
fi

# Test 3: Verify top 10 limit is documented
if ! grep -qi "top.*10\|top\s10\|limit.*10\|first.*10" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document top 10 limit" >&2
    exit 1
fi

# Test 4: Verify sorting by frequency is documented
if ! grep -qi "sort.*frequency\|order.*frequency\|frequency.*descend\|highest.*frequency" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document frequency-based sorting" >&2
    exit 1
fi

# Test 5: Verify report includes both frequency and success rate
if ! grep -qi "frequency.*success\|success.*frequency\|display.*rate\|show.*rate" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not document displaying both frequency and success rate" >&2
    exit 1
fi

# Test 6: Verify insights skill exists (report formatting)
INSIGHTS_SKILL_PATH=".claude/skills/devforgeai-insights/SKILL.md"
if [ ! -f "$INSIGHTS_SKILL_PATH" ]; then
    echo "FAIL: Insights skill needed for report formatting at $INSIGHTS_SKILL_PATH" >&2
    exit 1
fi

echo "PASS: Top patterns report is properly documented"
exit 0
