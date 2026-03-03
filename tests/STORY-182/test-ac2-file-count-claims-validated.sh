#!/bin/bash
##############################################################################
# STORY-182 AC-2: File Count Claims Validated
#
# Tests that SKILL.md "Total: N reference files" claims are validated
# against actual Glob count
#
# Expected: FAIL (implementation not yet created)
##############################################################################

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET_FILE="${PROJECT_ROOT}/.claude/skills/devforgeai-qa/references/deep-validation-workflow.md"

echo "[AC-2] Verify file count validation logic exists"

# Test 1: Check for extraction pattern documentation
if grep -qE "Total:.*reference files|extract_number" "${TARGET_FILE}"; then
    echo -e "${GREEN}PASS${NC}: File count extraction pattern documented"
else
    echo -e "${RED}FAIL${NC}: Missing file count extraction pattern (e.g., 'Total: N reference files')"
    exit 1
fi

# Test 2: Check for Glob comparison logic
if grep -qE "Glob.*references.*\.md|actual_count.*Glob|glob.*pattern" "${TARGET_FILE}"; then
    echo -e "${GREEN}PASS${NC}: Glob comparison for reference files documented"
else
    echo -e "${RED}FAIL${NC}: Missing Glob comparison logic for reference file counting"
    exit 1
fi

# Test 3: Check for claimed vs actual comparison
if grep -qE "claimed.*actual|claimed_count.*!=.*actual_count|mismatch" "${TARGET_FILE}"; then
    echo -e "${GREEN}PASS${NC}: Claimed vs actual comparison logic documented"
else
    echo -e "${RED}FAIL${NC}: Missing claimed vs actual comparison logic"
    exit 1
fi

echo -e "${GREEN}AC-2 PASSED${NC}"
exit 0
