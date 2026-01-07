#!/bin/bash
# STORY-184 AC-2: Code-Reviewer Prompt Has Constraints
# Verifies response constraints added to code-reviewer prompt section

set -e

TARGET_FILE=".claude/skills/devforgeai-qa/references/parallel-validation.md"
TEST_NAME="AC-2: Code-Reviewer Response Constraints"

echo "Testing: ${TEST_NAME}"

# Check file exists
if [[ ! -f "${TARGET_FILE}" ]]; then
    echo "FAIL: Target file not found: ${TARGET_FILE}"
    exit 1
fi

# AC-2: code-reviewer section must have Response Constraints
if ! grep -A 20 'subagent_type="code-reviewer"' "${TARGET_FILE}" | grep -q "Response Constraints"; then
    echo "FAIL: code-reviewer prompt missing 'Response Constraints' section"
    exit 1
fi

# Verify constraint format elements
if ! grep -A 30 'subagent_type="code-reviewer"' "${TARGET_FILE}" | grep -q "Status: PASS/FAIL"; then
    echo "FAIL: code-reviewer missing 'Status: PASS/FAIL' constraint"
    exit 1
fi

if ! grep -A 30 'subagent_type="code-reviewer"' "${TARGET_FILE}" | grep -q "Key findings"; then
    echo "FAIL: code-reviewer missing 'Key findings' constraint"
    exit 1
fi

echo "PASS: ${TEST_NAME}"
