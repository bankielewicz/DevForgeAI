#!/bin/bash
# STORY-184 AC-3: Security-Auditor Prompt Has Constraints
# Verifies response constraints added to security-auditor prompt section

set -e

TARGET_FILE=".claude/skills/devforgeai-qa/references/parallel-validation.md"
TEST_NAME="AC-3: Security-Auditor Response Constraints"

echo "Testing: ${TEST_NAME}"

# Check file exists
if [[ ! -f "${TARGET_FILE}" ]]; then
    echo "FAIL: Target file not found: ${TARGET_FILE}"
    exit 1
fi

# AC-3: security-auditor section must have Response Constraints
if ! grep -A 20 'subagent_type="security-auditor"' "${TARGET_FILE}" | grep -q "Response Constraints"; then
    echo "FAIL: security-auditor prompt missing 'Response Constraints' section"
    exit 1
fi

# Verify constraint format elements
if ! grep -A 30 'subagent_type="security-auditor"' "${TARGET_FILE}" | grep -q "Status: PASS/FAIL"; then
    echo "FAIL: security-auditor missing 'Status: PASS/FAIL' constraint"
    exit 1
fi

if ! grep -A 30 'subagent_type="security-auditor"' "${TARGET_FILE}" | grep -q "Blocking issues"; then
    echo "FAIL: security-auditor missing 'Blocking issues' constraint"
    exit 1
fi

echo "PASS: ${TEST_NAME}"
