#!/bin/bash
# STORY-226 Integration Test: /insights Command - Command Patterns Query
#
# Tests that the /insights command can query for command patterns.
#
# User Flow:
# 1. User runs: /insights command-patterns
# 2. insights skill routes to session-miner for n-gram analysis
# 3. session-miner returns analyzed sequences with success rates
# 4. insights skill formats and displays top 10 patterns
#
# TDD RED PHASE: Test expected to FAIL before implementation

set -e

TEST_NAME="test-insights-command-patterns"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Test 1: Verify /insights command exists
INSIGHTS_COMMAND_PATH=".claude/commands/insights.md"
if [ ! -f "$INSIGHTS_COMMAND_PATH" ]; then
    echo "FAIL: /insights command not found at $INSIGHTS_COMMAND_PATH" >&2
    exit 1
fi

# Test 2: Verify /insights command routes to command-patterns query
if ! grep -qi "command-pattern\|pattern\|sequence\|n-gram" "$INSIGHTS_COMMAND_PATH"; then
    echo "FAIL: /insights command does not support command-patterns query" >&2
    exit 1
fi

# Test 3: Verify insights command has proper YAML frontmatter
if ! grep -q "^description:" "$INSIGHTS_COMMAND_PATH"; then
    echo "FAIL: /insights command missing description in frontmatter" >&2
    exit 1
fi

if ! grep -q "^argument-hint:" "$INSIGHTS_COMMAND_PATH"; then
    echo "FAIL: /insights command missing argument-hint in frontmatter" >&2
    exit 1
fi

# Test 4: Verify command-patterns is documented as a valid query type
# The command should accept: /insights command-patterns
# Or: /insights patterns
# Or: /insights sequences
PATTERN_KEYWORDS="command-pattern\|patterns\|sequences"
if ! grep -qi "$PATTERN_KEYWORDS" "$INSIGHTS_COMMAND_PATH"; then
    echo "FAIL: /insights command does not document command-patterns query type" >&2
    exit 1
fi

# Test 5: Verify integration with devforgeai-insights skill
INSIGHTS_SKILL_PATH=".claude/skills/devforgeai-insights/SKILL.md"
if [ -f "$INSIGHTS_SKILL_PATH" ]; then
    # Check routing logic for command-patterns
    if ! grep -qi "command-pattern\|route.*pattern\|case.*pattern" "$INSIGHTS_SKILL_PATH"; then
        echo "FAIL: devforgeai-insights skill does not route command-patterns query" >&2
        exit 1
    fi
else
    echo "FAIL: devforgeai-insights skill not found at $INSIGHTS_SKILL_PATH" >&2
    exit 1
fi

# Test 6: Verify session-miner invocation from insights skill
if ! grep -qi "session-miner\|Task.*session" "$INSIGHTS_SKILL_PATH"; then
    echo "FAIL: devforgeai-insights skill does not invoke session-miner subagent" >&2
    exit 1
fi

echo "PASS: /insights command-patterns integration is properly documented"
exit 0
