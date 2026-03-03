#!/bin/bash
# STORY-181 AC-2: *.sh text eol=lf configured in .gitattributes
# TDD Phase: RED - This test should PASS (line 26 has entry)

set -e

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
GITATTRIBUTES_FILE="${PROJECT_ROOT}/.gitattributes"

echo "TEST: AC-2 - *.sh text eol=lf configured in .gitattributes"

# Arrange
pattern='^\*\.sh[[:space:]]+text[[:space:]]+eol=lf'

# Act
if grep -qE "${pattern}" "${GITATTRIBUTES_FILE}"; then
    echo "PASS: *.sh text eol=lf found in .gitattributes"
    grep -nE "${pattern}" "${GITATTRIBUTES_FILE}"
    exit 0
else
    echo "FAIL: *.sh text eol=lf NOT found in .gitattributes"
    exit 1
fi
