#!/bin/bash
# STORY-184 AC-4: Response Format Defined
# Verifies format: Status, Coverage%, Key findings (max 3), Blocking issues

set -e

TARGET_FILE=".claude/skills/devforgeai-qa/references/parallel-validation.md"
TEST_NAME="AC-4: Response Format Definition"

echo "Testing: ${TEST_NAME}"

# Check file exists
if [[ ! -f "${TARGET_FILE}" ]]; then
    echo "FAIL: Target file not found: ${TARGET_FILE}"
    exit 1
fi

# AC-4: Must define all 4 format elements
if ! grep -q "Status: PASS/FAIL" "${TARGET_FILE}"; then
    echo "FAIL: Missing format element 'Status: PASS/FAIL'"
    exit 1
fi

if ! grep -q "Coverage %" "${TARGET_FILE}"; then
    echo "FAIL: Missing format element 'Coverage %'"
    exit 1
fi

if ! grep -q "Key findings" "${TARGET_FILE}" || ! grep -q "max 3" "${TARGET_FILE}"; then
    echo "FAIL: Missing format element 'Key findings (max 3)'"
    exit 1
fi

if ! grep -q "Blocking issues" "${TARGET_FILE}"; then
    echo "FAIL: Missing format element 'Blocking issues'"
    exit 1
fi

echo "PASS: ${TEST_NAME}"
