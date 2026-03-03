#!/bin/bash
# STORY-181 AC-5 (Optional): Test-Automator post-generation normalization step
# TDD Phase: RED - This test should FAIL (normalization step not yet added)

set -e

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEST_AUTOMATOR_FILE="${PROJECT_ROOT}/.claude/agents/test-automator.md"

echo "TEST: AC-5 - Test-Automator has normalization step (Optional)"

# Arrange
patterns=("normali" "eol" "line.ending" "CRLF" "Edit.*replace_all")

# Act - Check for any normalization-related content
found=0
for pattern in "${patterns[@]}"; do
    if grep -qiE "${pattern}" "${TEST_AUTOMATOR_FILE}" 2>/dev/null; then
        found=1
        break
    fi
done

# Assert
if [[ "${found}" -eq 1 ]]; then
    echo "PASS: Test-automator contains normalization-related content"
    grep -inE "normali|eol|CRLF" "${TEST_AUTOMATOR_FILE}" | head -5
    exit 0
else
    echo "FAIL: Test-automator missing normalization step"
    echo "Expected: Edit(file_path=..., old_string=\"\\r\\n\", new_string=\"\\n\", replace_all=true)"
    exit 1
fi
