#!/bin/bash
##############################################################################
# STORY-182 AC-1: Step Added to Deep Validation
#
# Tests that Step 1.X: Documentation Accuracy Validation exists in
# deep-validation-workflow.md
#
# Expected: FAIL (implementation not yet created)
##############################################################################

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET_FILE="${PROJECT_ROOT}/.claude/skills/devforgeai-qa/references/deep-validation-workflow.md"

echo "[AC-1] Verify Step 1.X Documentation Accuracy Validation exists"

# Test 1: Check for section header
if grep -qE "^### 1\.[0-9]+.*Documentation Accuracy" "${TARGET_FILE}"; then
    echo -e "${GREEN}PASS${NC}: Documentation Accuracy Validation section exists"
else
    echo -e "${RED}FAIL${NC}: Missing '### 1.X Documentation Accuracy Validation' section"
    exit 1
fi

# Test 2: Check section is in Phase 1 (between lines containing "Phase 1" and "Phase 2")
phase1_end=$(grep -n "^## Phase 2" "${TARGET_FILE}" | head -1 | cut -d: -f1)
if [ -z "${phase1_end}" ]; then
    echo -e "${RED}FAIL${NC}: Cannot find Phase 2 marker to validate section position"
    exit 1
fi

section_line=$(grep -n "Documentation Accuracy" "${TARGET_FILE}" | head -1 | cut -d: -f1)
if [ -n "${section_line}" ] && [ "${section_line}" -lt "${phase1_end}" ]; then
    echo -e "${GREEN}PASS${NC}: Section is in Phase 1 (line ${section_line} < Phase 2 at ${phase1_end})"
else
    echo -e "${RED}FAIL${NC}: Section not in Phase 1 or missing"
    exit 1
fi

echo -e "${GREEN}AC-1 PASSED${NC}"
exit 0
