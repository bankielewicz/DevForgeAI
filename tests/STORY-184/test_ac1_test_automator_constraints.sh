#!/bin/bash
# STORY-184 AC-1: Test-Automator Prompt Has Constraints
# Verifies response constraints added to test-automator prompt section

set -e

TARGET_FILE=".claude/skills/devforgeai-qa/references/parallel-validation.md"
TEST_NAME="AC-1: Test-Automator Response Constraints"

echo "Testing: ${TEST_NAME}"

# Check file exists
if [[ ! -f "${TARGET_FILE}" ]]; then
    echo "FAIL: Target file not found: ${TARGET_FILE}"
    exit 1
fi

# AC-1: test-automator section must have Response Constraints
if ! grep -A 20 'subagent_type="test-automator"' "${TARGET_FILE}" | grep -q "Response Constraints"; then
    echo "FAIL: test-automator prompt missing 'Response Constraints' section"
    exit 1
fi

# Verify constraint format elements
if ! grep -A 30 'subagent_type="test-automator"' "${TARGET_FILE}" | grep -q "Status: PASS/FAIL"; then
    echo "FAIL: test-automator missing 'Status: PASS/FAIL' constraint"
    exit 1
fi

if ! grep -A 30 'subagent_type="test-automator"' "${TARGET_FILE}" | grep -q "Coverage %"; then
    echo "FAIL: test-automator missing 'Coverage %' constraint"
    exit 1
fi

echo "PASS: ${TEST_NAME}"
