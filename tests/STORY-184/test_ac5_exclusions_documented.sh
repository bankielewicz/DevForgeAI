#!/bin/bash
# STORY-184 AC-5: Exclusions Documented
# Verifies "Do NOT include: full analysis, code snippets, detailed recommendations"

set -e

TARGET_FILE=".claude/skills/devforgeai-qa/references/parallel-validation.md"
TEST_NAME="AC-5: Exclusions Documented"

echo "Testing: ${TEST_NAME}"

# Check file exists
if [[ ! -f "${TARGET_FILE}" ]]; then
    echo "FAIL: Target file not found: ${TARGET_FILE}"
    exit 1
fi

# AC-5: Must document exclusions
if ! grep -q "Do NOT include" "${TARGET_FILE}"; then
    echo "FAIL: Missing 'Do NOT include' exclusion statement"
    exit 1
fi

if ! grep -q "full analysis" "${TARGET_FILE}"; then
    echo "FAIL: Missing exclusion 'full analysis'"
    exit 1
fi

if ! grep -q "code snippets" "${TARGET_FILE}"; then
    echo "FAIL: Missing exclusion 'code snippets'"
    exit 1
fi

if ! grep -q "detailed recommendations" "${TARGET_FILE}"; then
    echo "FAIL: Missing exclusion 'detailed recommendations'"
    exit 1
fi

echo "PASS: ${TEST_NAME}"
