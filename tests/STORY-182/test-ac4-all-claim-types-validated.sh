#!/bin/bash
##############################################################################
# STORY-182 AC-4: All Claim Types Validated
#
# Tests that file count, line count, and section claims are all validated
#
# Expected: FAIL (implementation not yet created)
##############################################################################

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET_FILE="${PROJECT_ROOT}/.claude/skills/devforgeai-qa/references/deep-validation-workflow.md"

echo "[AC-4] Verify all claim types are validated"

# Test 1: File count validation
if grep -qE "file.count|reference.files|Total:.*files" "${TARGET_FILE}"; then
    echo -e "${GREEN}PASS${NC}: File count validation documented"
else
    echo -e "${RED}FAIL${NC}: Missing file count validation"
    exit 1
fi

# Test 2: Line count validation
if grep -qE "line.count|lines.*claim|~.*lines" "${TARGET_FILE}"; then
    echo -e "${GREEN}PASS${NC}: Line count validation documented"
else
    echo -e "${RED}FAIL${NC}: Missing line count validation"
    exit 1
fi

# Test 3: Section claims validation
if grep -qE "section.claim|section.count|contains.*sections" "${TARGET_FILE}"; then
    echo -e "${GREEN}PASS${NC}: Section claims validation documented"
else
    echo -e "${RED}FAIL${NC}: Missing section claims validation"
    exit 1
fi

echo -e "${GREEN}AC-4 PASSED${NC}"
exit 0
