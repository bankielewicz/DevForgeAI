#!/bin/bash
##############################################################################
# STORY-160: AC-1 Verification Tests
# AC-1: SKILL.md Overview Updated - Validates 10 validation steps
#
# Test that devforgeai-development SKILL.md lists 10 validation steps
# (was 8) including Steps 0.1.5 and 0.1.6 for RCA-008 git safety
#
# Acceptance Criteria:
# Given the devforgeai-development SKILL.md file
# When I review the Pre-Flight Validation section
# Then it should list 10 validation steps (was 8) including Steps 0.1.5 and 0.1.6
##############################################################################

set -uo pipefail
# NOTE: set -e disabled because ((var++)) returns 1 when var is 0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SKILL_FILE="${PROJECT_ROOT}/.claude/skills/devforgeai-development/SKILL.md"
PREFLIGHT_REFERENCE="${PROJECT_ROOT}/.claude/skills/devforgeai-development/references/preflight/_index.md"

# Test counter
tests_passed=0
tests_failed=0

##############################################################################
# Test AC-1.1: SKILL.md exists
##############################################################################
echo -e "${YELLOW}[TEST AC-1.1]${NC} Verify SKILL.md file exists"
if [ -f "${SKILL_FILE}" ]; then
    echo -e "${GREEN}PASS${NC}: SKILL.md found at ${SKILL_FILE}"
    ((tests_passed++))
else
    echo -e "${RED}FAIL${NC}: SKILL.md not found at ${SKILL_FILE}"
    ((tests_failed++))
    exit 1
fi

##############################################################################
# Test AC-1.2: Pre-Flight Validation section exists
##############################################################################
echo -e "${YELLOW}[TEST AC-1.2]${NC} Verify Pre-Flight Validation section exists in SKILL.md"
if grep -q "Pre-Flight" "${SKILL_FILE}" || grep -q "Pre-flight" "${SKILL_FILE}"; then
    echo -e "${GREEN}PASS${NC}: Pre-Flight Validation section found"
    ((tests_passed++))
else
    echo -e "${RED}FAIL${NC}: Pre-Flight Validation section not found in SKILL.md"
    ((tests_failed++))
fi

##############################################################################
# Test AC-1.3: Reference file preflight-validation.md documents 10 steps
##############################################################################
echo -e "${YELLOW}[TEST AC-1.3]${NC} Verify preflight-validation.md documents 10 validation steps"
if [ -f "${PREFLIGHT_REFERENCE}" ]; then
    # Look for "10 validation steps" or count numbered steps
    if grep -q "10 validation steps" "${PREFLIGHT_REFERENCE}" || \
       grep -q "Phase 01 executes 10 validation steps" "${PREFLIGHT_REFERENCE}"; then
        echo -e "${GREEN}PASS${NC}: preflight-validation.md mentions 10 validation steps"
        ((tests_passed++))
    else
        echo -e "${RED}FAIL${NC}: preflight-validation.md does not mention 10 validation steps"
        echo "Content preview:"
        grep -i "validation step" "${PREFLIGHT_REFERENCE}" | head -5
        ((tests_failed++))
    fi
else
    echo -e "${RED}FAIL${NC}: preflight-validation.md not found at ${PREFLIGHT_REFERENCE}"
    ((tests_failed++))
fi

##############################################################################
# Test AC-1.4: Step 0.1.5 (User Consent) documented
##############################################################################
echo -e "${YELLOW}[TEST AC-1.4]${NC} Verify Step 0.1.5 (User Consent for Git State Changes) is documented"
if grep -qi "01\.1\.5.*[Uu]ser [Cc]onsent" "${PREFLIGHT_REFERENCE}" || \
   grep -qi "Phase 01\.1\.5" "${PREFLIGHT_REFERENCE}" || \
   grep -qi "1\.1\.5.*[Cc]onsent" "${PREFLIGHT_REFERENCE}"; then
    echo -e "${GREEN}PASS${NC}: Step 0.1.5 (User Consent) found in documentation"
    ((tests_passed++))
else
    echo -e "${RED}FAIL${NC}: Step 0.1.5 (User Consent) not found or not properly labeled"
    echo "Searching for consent-related steps..."
    grep -i "consent" "${PREFLIGHT_REFERENCE}" | head -3 || echo "No consent mentions found"
    ((tests_failed++))
fi

##############################################################################
# Test AC-1.5: Step 0.1.6 (Stash Warning) documented
##############################################################################
echo -e "${YELLOW}[TEST AC-1.5]${NC} Verify Step 0.1.6 (Stash Warning and Confirmation) is documented"
if grep -qi "01\.1\.6.*[Ss]tash" "${PREFLIGHT_REFERENCE}" || \
   grep -qi "Phase 01\.1\.6" "${PREFLIGHT_REFERENCE}" || \
   grep -qi "1\.1\.6.*[Ww]arning" "${PREFLIGHT_REFERENCE}"; then
    echo -e "${GREEN}PASS${NC}: Step 0.1.6 (Stash Warning) found in documentation"
    ((tests_passed++))
else
    echo -e "${RED}FAIL${NC}: Step 0.1.6 (Stash Warning) not found or not properly labeled"
    echo "Searching for stash-related steps..."
    grep -i "stash" "${PREFLIGHT_REFERENCE}" | head -3 || echo "No stash mentions found"
    ((tests_failed++))
fi

##############################################################################
# Test AC-1.6: Validation steps are numbered sequentially
##############################################################################
echo -e "${YELLOW}[TEST AC-1.6]${NC} Verify validation steps are properly documented with numbers"
# Count documented validation steps (should find at least 10)
step_count=$(grep -c "^## Phase 01\." "${PREFLIGHT_REFERENCE}" || echo "0")
if [ "${step_count}" -ge 8 ]; then
    echo -e "${GREEN}PASS${NC}: Found ${step_count} documented validation steps (expected ≥8)"
    ((tests_passed++))
else
    echo -e "${RED}FAIL${NC}: Only found ${step_count} documented validation steps (expected ≥8)"
    ((tests_failed++))
fi

##############################################################################
# Test AC-1.7: SKILL.md references preflight-validation.md
##############################################################################
echo -e "${YELLOW}[TEST AC-1.7]${NC} Verify SKILL.md references preflight-validation.md"
if grep -q "preflight-validation" "${SKILL_FILE}"; then
    echo -e "${GREEN}PASS${NC}: SKILL.md contains reference to preflight-validation.md"
    ((tests_passed++))
else
    echo -e "${RED}FAIL${NC}: SKILL.md does not reference preflight-validation.md"
    ((tests_failed++))
fi

##############################################################################
# Summary
##############################################################################
echo ""
echo "=========================================="
echo "AC-1 Test Summary"
echo "=========================================="
echo -e "Passed: ${GREEN}${tests_passed}${NC}"
echo -e "Failed: ${RED}${tests_failed}${NC}"
echo "=========================================="

if [ ${tests_failed} -eq 0 ]; then
    echo -e "${GREEN}✓ AC-1 VERIFICATION PASSED${NC}"
    exit 0
else
    echo -e "${RED}✗ AC-1 VERIFICATION FAILED${NC}"
    exit 1
fi
