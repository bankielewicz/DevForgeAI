#!/bin/bash
# STORY-174 AC#1: qa.md Command Has execution-mode Frontmatter
#
# Given the qa.md command file
# Then it contains `execution-mode: immediate` in YAML frontmatter
#
# Test Status: RED (expected to FAIL before implementation)

set -e

TEST_NAME="AC#1: qa.md execution-mode frontmatter"
COMMAND_FILE="/mnt/c/Projects/DevForgeAI2/.claude/commands/qa.md"

echo "=============================================="
echo "TEST: ${TEST_NAME}"
echo "=============================================="

# Arrange
if [[ ! -f "${COMMAND_FILE}" ]]; then
    echo "FAIL: Command file not found: ${COMMAND_FILE}"
    exit 1
fi

# Act - Extract YAML frontmatter and check for execution-mode
# YAML frontmatter is between first --- (line 1) and second ---
# Handle CRLF line endings (Windows files)
# Use tr to remove \r, then awk to extract frontmatter
FRONTMATTER=$(tr -d '\r' < "${COMMAND_FILE}" | awk '/^---$/{if(++n==1)next; if(n==2)exit} n==1')

echo "Frontmatter content:"
echo "${FRONTMATTER}"
echo ""

# Assert - Check for execution-mode: immediate in frontmatter
if echo "${FRONTMATTER}" | grep -q "^execution-mode: immediate$"; then
    echo "PASS: qa.md contains 'execution-mode: immediate' in frontmatter"
    exit 0
else
    echo "FAIL: qa.md does NOT contain 'execution-mode: immediate' in frontmatter"
    echo ""
    echo "Expected: execution-mode: immediate"
    echo "Actual frontmatter:"
    echo "${FRONTMATTER}"
    exit 1
fi
