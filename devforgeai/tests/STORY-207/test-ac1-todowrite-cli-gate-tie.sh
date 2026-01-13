#!/bin/bash
# STORY-207 AC-1: TodoWrite Status Tied to CLI Gate
# Tests that documentation requires CLI gate exit code 0 before TodoWrite completion

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
SKILL_FILE="${PROJECT_ROOT}/.claude/skills/devforgeai-development/SKILL.md"

# Test name for reporting
TEST_NAME="AC-1: TodoWrite Status Tied to CLI Gate"

echo "Running: ${TEST_NAME}"
echo "File: ${SKILL_FILE}"

# AC-1 Requirement: Documentation MUST state that TodoWrite "completed" status
# requires CLI gate `devforgeai-validate phase-complete` to return exit code 0

# Check 1: Pattern linking TodoWrite completion to CLI gate exit code 0
PATTERN1='exit.*(code|_code).*0.*TodoWrite|TodoWrite.*exit.*(code|_code).*0|completed.*phase-complete.*exit.*0|exit.*0.*mark.*completed'

if grep -qiE "${PATTERN1}" "${SKILL_FILE}"; then
    echo "PASS: Found TodoWrite-to-CLI-gate linkage pattern"
    RESULT1="PASS"
else
    echo "FAIL: Missing explicit linkage between TodoWrite completion and CLI gate exit code 0"
    RESULT1="FAIL"
fi

# Check 2: Must mention devforgeai-validate phase-complete in TodoWrite context
PATTERN2='phase-complete.*TodoWrite|TodoWrite.*phase-complete|mark.*completed.*phase-complete'

if grep -qiE "${PATTERN2}" "${SKILL_FILE}"; then
    echo "PASS: Found phase-complete command in TodoWrite context"
    RESULT2="PASS"
else
    echo "FAIL: Missing phase-complete command near TodoWrite completion instructions"
    RESULT2="FAIL"
fi

# Check 3: Must explicitly require exit code 0
PATTERN3='MUST.*exit.*code.*0|exit.*code.*0.*MUST|gate.*return.*exit.*0'

if grep -qiE "${PATTERN3}" "${SKILL_FILE}"; then
    echo "PASS: Found MUST requirement for exit code 0"
    RESULT3="PASS"
else
    echo "FAIL: Missing MUST requirement for CLI gate exit code 0"
    RESULT3="FAIL"
fi

# Summary
echo ""
echo "=== Test Summary ==="
if [[ "${RESULT1}" == "PASS" && "${RESULT2}" == "PASS" && "${RESULT3}" == "PASS" ]]; then
    echo "AC-1: ALL CHECKS PASSED"
    exit 0
else
    echo "AC-1: FAILED - Missing TodoWrite-CLI gate integration documentation"
    exit 1
fi
