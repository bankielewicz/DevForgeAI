#!/bin/bash
##############################################################################
# STORY-182 AC-3: Discrepancies Reported as MEDIUM Severity
#
# Tests that documentation drift discrepancies are reported with
# MEDIUM severity violations
#
# Expected: FAIL (implementation not yet created)
##############################################################################

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET_FILE="${PROJECT_ROOT}/.claude/skills/devforgeai-qa/references/deep-validation-workflow.md"

echo "[AC-3] Verify MEDIUM severity for discrepancies"

# Test 1: Check for MEDIUM severity specification
if grep -qE "severity.*MEDIUM|MEDIUM.*severity|\"MEDIUM\"" "${TARGET_FILE}"; then
    echo -e "${GREEN}PASS${NC}: MEDIUM severity specified for violations"
else
    echo -e "${RED}FAIL${NC}: Missing MEDIUM severity specification"
    exit 1
fi

# Test 2: Check for documentation_drift violation type
if grep -qE "documentation_drift|documentation.drift|doc.*drift" "${TARGET_FILE}"; then
    echo -e "${GREEN}PASS${NC}: documentation_drift violation type defined"
else
    echo -e "${RED}FAIL${NC}: Missing documentation_drift violation type"
    exit 1
fi

# Test 3: Verify MEDIUM is in context of documentation validation (not other validations)
doc_accuracy_section=$(grep -A 30 "Documentation Accuracy" "${TARGET_FILE}" 2>/dev/null || echo "")
if echo "${doc_accuracy_section}" | grep -qE "MEDIUM"; then
    echo -e "${GREEN}PASS${NC}: MEDIUM severity is within Documentation Accuracy section"
else
    echo -e "${RED}FAIL${NC}: MEDIUM severity not found in Documentation Accuracy context"
    exit 1
fi

echo -e "${GREEN}AC-3 PASSED${NC}"
exit 0
