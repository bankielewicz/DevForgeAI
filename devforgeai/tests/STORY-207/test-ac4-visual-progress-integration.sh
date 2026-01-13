#!/bin/bash
# STORY-207 AC-4: Visual Progress Indicator Integration
# Tests that SKILL.md combines gate result with TodoWrite update in display

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
SKILL_FILE="${PROJECT_ROOT}/.claude/skills/devforgeai-development/SKILL.md"

# Test name for reporting
TEST_NAME="AC-4: Visual Progress Indicator Integration"

echo "Running: ${TEST_NAME}"
echo "File: ${SKILL_FILE}"

# AC-4 Requirements:
# 1. References existing "Phase Progress Indicator" display pattern
# 2. Combines gate result with TodoWrite update in display

# Check 1: Must reference Phase Progress Indicator
PATTERN1='[Pp]hase.*[Pp]rogress.*[Ii]ndicator|[Pp]rogress.*[Ii]ndicator.*[Pp]attern|[Vv]isual.*[Pp]rogress'

if grep -qiE "${PATTERN1}" "${SKILL_FILE}"; then
    echo "PASS: Found Phase Progress Indicator reference"
    RESULT1="PASS"
else
    echo "FAIL: Missing Phase Progress Indicator reference"
    RESULT1="FAIL"
fi

# Check 2: Must show combined gate result + TodoWrite display
PATTERN2='gate.*result.*TodoWrite|TodoWrite.*update.*display|display.*gate.*TodoWrite|combine.*gate.*TodoWrite'

if grep -qiE "${PATTERN2}" "${SKILL_FILE}"; then
    echo "PASS: Found combined gate+TodoWrite display pattern"
    RESULT2="PASS"
else
    echo "FAIL: Missing combined gate result with TodoWrite update display"
    RESULT2="FAIL"
fi

# Check 3: Must show visual indicator when gate passes
PATTERN3='gate.*pass.*display|display.*gate.*pass|indicator.*gate.*pass|checkmark.*gate|gate.*checkmark'

if grep -qiE "${PATTERN3}" "${SKILL_FILE}"; then
    echo "PASS: Found visual indicator for gate pass"
    RESULT3="PASS"
else
    echo "FAIL: Missing visual indicator when gate passes"
    RESULT3="FAIL"
fi

# Check 4: Display pattern should include status transition
PATTERN4='in_progress.*completed.*display|status.*transition.*display|display.*status.*change'

if grep -qiE "${PATTERN4}" "${SKILL_FILE}"; then
    echo "PASS: Found status transition in display pattern"
    RESULT4="PASS"
else
    echo "FAIL: Missing status transition in visual display"
    RESULT4="FAIL"
fi

# Summary
echo ""
echo "=== Test Summary ==="
PASS_COUNT=0
[[ "${RESULT1}" == "PASS" ]] && PASS_COUNT=$((PASS_COUNT + 1))
[[ "${RESULT2}" == "PASS" ]] && PASS_COUNT=$((PASS_COUNT + 1))
[[ "${RESULT3}" == "PASS" ]] && PASS_COUNT=$((PASS_COUNT + 1))
[[ "${RESULT4}" == "PASS" ]] && PASS_COUNT=$((PASS_COUNT + 1))

if [[ ${PASS_COUNT} -eq 4 ]]; then
    echo "AC-4: ALL CHECKS PASSED"
    exit 0
else
    echo "AC-4: FAILED - Missing visual progress integration (${PASS_COUNT}/4 passed)"
    exit 1
fi
