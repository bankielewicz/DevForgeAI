#!/bin/bash
##############################################################################
# STORY-182 AC-5: Violation Message Clear
#
# Tests that violation message uses format:
# "Claims {claimed} files, found {actual}"
#
# Expected: FAIL (implementation not yet created)
##############################################################################

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET_FILE="${PROJECT_ROOT}/.claude/skills/devforgeai-qa/references/deep-validation-workflow.md"

echo "[AC-5] Verify clear violation message format"

# Test 1: Check for Claims/found message pattern
if grep -qE "Claims.*files.*found|Claims.*\{.*\}.*found.*\{.*\}" "${TARGET_FILE}"; then
    echo -e "${GREEN}PASS${NC}: Clear violation message format documented"
else
    echo -e "${RED}FAIL${NC}: Missing message format 'Claims {claimed} files, found {actual}'"
    exit 1
fi

# Test 2: Check for variable placeholders in message
if grep -qE "\{claimed\}|\{actual\}|claimed_count.*actual_count" "${TARGET_FILE}"; then
    echo -e "${GREEN}PASS${NC}: Variable placeholders in message format"
else
    echo -e "${RED}FAIL${NC}: Missing variable placeholders in violation message"
    exit 1
fi

# Test 3: Verify message field exists in violation structure
if grep -qE "message:.*Claims|\"message\".*:.*Claims" "${TARGET_FILE}"; then
    echo -e "${GREEN}PASS${NC}: Message field in violation structure"
else
    echo -e "${RED}FAIL${NC}: Missing message field in violation structure"
    exit 1
fi

echo -e "${GREEN}AC-5 PASSED${NC}"
exit 0
