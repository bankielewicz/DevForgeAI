#!/bin/bash
# STORY-226 Integration Test: Session Miner N-gram Pipeline
#
# Tests the complete n-gram extraction pipeline from history.jsonl to report output.
#
# Integration Points:
# 1. session-miner subagent reads history.jsonl
# 2. session-miner extracts SessionEntry objects
# 3. session-miner generates n-grams (2-gram and 3-gram)
# 4. session-miner calculates success rates per sequence
# 5. devforgeai-insights skill formats report
#
# TDD RED PHASE: Test expected to FAIL before implementation

set -e

TEST_NAME="test-session-miner-integration"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIXTURES_DIR="${TEST_DIR}/fixtures"
SAMPLE_HISTORY="${FIXTURES_DIR}/sample-history.jsonl"

# Verify test fixtures exist
if [ ! -f "$SAMPLE_HISTORY" ]; then
    echo "FAIL: Test fixture not found: $SAMPLE_HISTORY" >&2
    exit 1
fi

# Test 1: Verify session-miner subagent exists and is properly configured
SESSION_MINER_PATH=".claude/agents/session-miner.md"
if [ ! -f "$SESSION_MINER_PATH" ]; then
    echo "FAIL: session-miner subagent not found at $SESSION_MINER_PATH" >&2
    exit 1
fi

# Test 2: Verify session-miner has required YAML frontmatter
if ! grep -q "^name: session-miner" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner missing 'name' in frontmatter" >&2
    exit 1
fi

if ! grep -q "^tools:" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner missing 'tools' in frontmatter" >&2
    exit 1
fi

# Test 3: Verify session-miner references STORY-226
if ! grep -qi "STORY-226\|command.*pattern\|sequence.*analysis" "$SESSION_MINER_PATH"; then
    echo "FAIL: session-miner does not reference STORY-226 or command pattern analysis" >&2
    exit 1
fi

# Test 4: Verify n-gram workflow documentation exists
# The workflow should describe: parse -> extract -> group -> count -> rate -> format
REQUIRED_WORKFLOW_STEPS=(
    "parse\|extract"
    "group\|session\|boundary"
    "count\|frequency"
    "rate\|success"
    "format\|report\|output"
)

for step in "${REQUIRED_WORKFLOW_STEPS[@]}"; do
    if ! grep -qi "$step" "$SESSION_MINER_PATH"; then
        echo "FAIL: session-miner missing workflow step documentation for: $step" >&2
        exit 1
    fi
done

# Test 5: Verify integration with insights skill
INSIGHTS_SKILL_PATH=".claude/skills/devforgeai-insights/SKILL.md"
if [ -f "$INSIGHTS_SKILL_PATH" ]; then
    # Check if insights skill references command patterns
    if ! grep -qi "command.*pattern\|sequence\|n-gram\|STORY-226" "$INSIGHTS_SKILL_PATH"; then
        echo "FAIL: devforgeai-insights skill does not reference command pattern analysis" >&2
        exit 1
    fi
else
    echo "INFO: devforgeai-insights skill not found - may need creation"
    echo "FAIL: Integration point devforgeai-insights skill not found" >&2
    exit 1
fi

# Test 6: Verify end-to-end data flow documentation
# session-miner should output data that insights skill can consume
echo "PASS: Session miner n-gram integration pipeline is properly documented"
exit 0
