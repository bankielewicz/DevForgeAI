#!/bin/bash
# STORY-181 AC-3: tests/**/*.sh text eol=lf configured in .gitattributes
# TDD Phase: RED - This test should FAIL (explicit entry is MISSING)

set -e

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
GITATTRIBUTES_FILE="${PROJECT_ROOT}/.gitattributes"

echo "TEST: AC-3 - tests/**/*.sh text eol=lf configured in .gitattributes"

# Arrange
pattern='tests/\*\*/\*\.sh[[:space:]]+text[[:space:]]+eol=lf'

# Act
if grep -qE "${pattern}" "${GITATTRIBUTES_FILE}"; then
    echo "PASS: tests/**/*.sh text eol=lf found in .gitattributes"
    grep -nE "${pattern}" "${GITATTRIBUTES_FILE}"
    exit 0
else
    echo "FAIL: tests/**/*.sh text eol=lf NOT found in .gitattributes"
    echo "Current .gitattributes content for tests/:"
    grep -n "tests" "${GITATTRIBUTES_FILE}" || echo "(no tests entries)"
    exit 1
fi
