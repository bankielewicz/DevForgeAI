#!/bin/bash
# STORY-207 AC-2: Enforcement Pattern Documented with 5 Steps
# Tests that SKILL.md contains explicit 5-step enforcement pattern for TodoWrite

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
SKILL_FILE="${PROJECT_ROOT}/.claude/skills/devforgeai-development/SKILL.md"

# Test name for reporting
TEST_NAME="AC-2: Enforcement Pattern Documented with 5 Steps"

echo "Running: ${TEST_NAME}"
echo "File: ${SKILL_FILE}"

# AC-2 Requirement: TodoWrite usage section MUST include explicit enforcement
# pattern with exactly 5 steps

# Check 1: Must have a TodoWrite usage section or enforcement pattern section
PATTERN1='TodoWrite.*[Uu]sage|[Uu]sage.*TodoWrite|TodoWrite.*[Ee]nforcement|[Ee]nforcement.*[Pp]attern'

if grep -qiE "${PATTERN1}" "${SKILL_FILE}"; then
    echo "PASS: Found TodoWrite usage/enforcement section"
    RESULT1="PASS"
else
    echo "FAIL: Missing TodoWrite usage or enforcement pattern section"
    RESULT1="FAIL"
fi

# Check 2: Must contain numbered steps (1. through 5. or Step 1 through Step 5)
STEP_COUNT=0
for i in 1 2 3 4 5; do
    if grep -qE "(^|\s)${i}\.|Step ${i}|step ${i}" "${SKILL_FILE}"; then
        STEP_COUNT=$((STEP_COUNT + 1))
    fi
done

# Look for 5 consecutive enforcement steps in TodoWrite context
PATTERN2='1\..*2\..*3\..*4\..*5\.'
if grep -qzoE 'TodoWrite.*\n.*1\..*\n.*2\..*\n.*3\..*\n.*4\..*\n.*5\.' "${SKILL_FILE}" 2>/dev/null; then
    echo "PASS: Found 5-step pattern near TodoWrite"
    RESULT2="PASS"
else
    echo "FAIL: Missing explicit 5-step enforcement pattern for TodoWrite"
    RESULT2="FAIL"
fi

# Check 3: Enforcement steps should include key actions
REQUIRED_ACTIONS=("phase-complete" "exit" "in_progress" "completed" "HALT")
FOUND_ACTIONS=0

for action in "${REQUIRED_ACTIONS[@]}"; do
    if grep -qi "${action}" "${SKILL_FILE}"; then
        FOUND_ACTIONS=$((FOUND_ACTIONS + 1))
    fi
done

if [[ ${FOUND_ACTIONS} -ge 4 ]]; then
    echo "PASS: Found required enforcement actions (${FOUND_ACTIONS}/5)"
    RESULT3="PASS"
else
    echo "FAIL: Missing key enforcement actions (found ${FOUND_ACTIONS}/5)"
    RESULT3="FAIL"
fi

# Summary
echo ""
echo "=== Test Summary ==="
if [[ "${RESULT1}" == "PASS" && "${RESULT2}" == "PASS" && "${RESULT3}" == "PASS" ]]; then
    echo "AC-2: ALL CHECKS PASSED"
    exit 0
else
    echo "AC-2: FAILED - Missing 5-step enforcement pattern documentation"
    exit 1
fi
