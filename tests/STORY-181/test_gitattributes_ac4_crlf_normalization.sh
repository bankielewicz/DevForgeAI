#!/bin/bash
# STORY-181 AC-4: Existing CRLF files normalized on next commit
# TDD Phase: RED - Verifies git renormalize capability

set -e

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"

echo "TEST: AC-4 - CRLF normalization capability verified"

# Arrange - Check if git can detect files needing normalization
cd "${PROJECT_ROOT}"

# Act - Check for CRLF in shell scripts
crlf_output=$(find tests -name "*.sh" -type f -exec file {} \; 2>/dev/null | grep -c "CRLF" || true)
crlf_count=${crlf_output:-0}

# Assert
if [[ "${crlf_count}" == "0" ]] || [[ -z "${crlf_count}" ]]; then
    echo "PASS: No CRLF line endings found in tests/**/*.sh"
    exit 0
else
    echo "FAIL: ${crlf_count} shell script(s) still have CRLF line endings"
    echo "Run: git add --renormalize . && git commit -m 'chore: normalize line endings'"
    exit 1
fi
