#!/bin/bash
# STORY-181 AC-1: .gitattributes file exists at project root
# TDD Phase: RED - This test should PASS (file exists)

set -e

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
GITATTRIBUTES_FILE="${PROJECT_ROOT}/.gitattributes"

echo "TEST: AC-1 - .gitattributes file exists at project root"

# Arrange
expected_file="${GITATTRIBUTES_FILE}"

# Act & Assert
if [[ -f "${expected_file}" ]]; then
    echo "PASS: .gitattributes exists at ${expected_file}"
    exit 0
else
    echo "FAIL: .gitattributes NOT found at ${expected_file}"
    exit 1
fi
