#!/bin/bash
# STORY-207 AC-3: No Premature Completion Marking
# Tests that SKILL.md enforces phase remains "in_progress" until gate passes

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
SKILL_FILE="${PROJECT_ROOT}/.claude/skills/devforgeai-development/SKILL.md"

# Test name for reporting
TEST_NAME="AC-3: No Premature Completion Marking"

echo "Running: ${TEST_NAME}"
echo "File: ${SKILL_FILE}"

# AC-3 Requirements:
# 1. Phase MUST remain "in_progress" until gate passes
# 2. Enforcement text includes CRITICAL rules

# Check 1: Must state phase remains in_progress until gate passes
PATTERN1='in_progress.*until.*gate|remain.*in_progress.*gate|MUST.*remain.*in_progress|in_progress.*MUST.*not.*completed'

if grep -qiE "${PATTERN1}" "${SKILL_FILE}"; then
    echo "PASS: Found in_progress-until-gate requirement"
    RESULT1="PASS"
else
    echo "FAIL: Missing requirement for phase to remain in_progress until gate passes"
    RESULT1="FAIL"
fi

# Check 2: Must include CRITICAL keyword in enforcement rules
PATTERN2='CRITICAL.*TodoWrite|CRITICAL.*completion|CRITICAL.*premature|TodoWrite.*CRITICAL'

if grep -qiE "${PATTERN2}" "${SKILL_FILE}"; then
    echo "PASS: Found CRITICAL keyword in enforcement context"
    RESULT2="PASS"
else
    echo "FAIL: Missing CRITICAL rules for TodoWrite completion enforcement"
    RESULT2="FAIL"
fi

# Check 3: Must prohibit marking completed without gate call
PATTERN3='[Nn]ever.*completed.*without.*gate|[Mm]ust.*not.*mark.*completed.*before|[Dd]o.*not.*mark.*completed.*until|[Pp]rohibit.*premature.*completion'

if grep -qiE "${PATTERN3}" "${SKILL_FILE}"; then
    echo "PASS: Found prohibition against premature completion"
    RESULT3="PASS"
else
    echo "FAIL: Missing explicit prohibition against premature completion marking"
    RESULT3="FAIL"
fi

# Check 4: Must reference CLI gate before TodoWrite status change
PATTERN4='gate.*before.*status|CLI.*gate.*then.*TodoWrite|phase-complete.*before.*completed'

if grep -qiE "${PATTERN4}" "${SKILL_FILE}"; then
    echo "PASS: Found gate-before-status-change requirement"
    RESULT4="PASS"
else
    echo "FAIL: Missing requirement for gate call before status change"
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
    echo "AC-3: ALL CHECKS PASSED"
    exit 0
else
    echo "AC-3: FAILED - Missing premature completion prevention rules (${PASS_COUNT}/4 passed)"
    exit 1
fi
