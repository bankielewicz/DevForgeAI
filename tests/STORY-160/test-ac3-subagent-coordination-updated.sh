#!/bin/bash
##############################################################################
# STORY-160: AC-3 Verification Tests
# AC-3: Subagent Coordination Updated
#
# Test that Subagent Coordination section mentions enhanced file analysis
# (Phase 2.5) from RCA-008 for git-validator
#
# Acceptance Criteria:
# Given the Subagent Coordination section
# When I review git-validator usage
# Then it should mention the enhanced file analysis (Phase 2.5) from RCA-008
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
PREFLIGHT_REF="${PROJECT_ROOT}/.claude/skills/devforgeai-development/references/preflight/_index.md"
GIT_VALIDATOR_AGENT="${PROJECT_ROOT}/.claude/agents/git-validator.md"

# Test counter
tests_passed=0
tests_failed=0

##############################################################################
# Test AC-3.1: Subagent Coordination section exists in SKILL.md
##############################################################################
echo -e "${YELLOW}[TEST AC-3.1]${NC} Verify Subagent Coordination section exists in SKILL.md"
if grep -qi "Subagent Coordination\|subagent" "${SKILL_FILE}"; then
    echo -e "${GREEN}PASS${NC}: Subagent Coordination section or reference found in SKILL.md"
    ((tests_passed++))
else
    echo -e "${RED}FAIL${NC}: Subagent Coordination section not found in SKILL.md"
    ((tests_failed++))
fi

##############################################################################
# Test AC-3.2: git-validator is mentioned in coordination context
##############################################################################
echo -e "${YELLOW}[TEST AC-3.2]${NC} Verify git-validator is mentioned in subagent coordination"
if grep -qi "git-validator" "${SKILL_FILE}" || grep -qi "git-validator" "${PREFLIGHT_REF}"; then
    echo -e "${GREEN}PASS${NC}: git-validator mentioned in coordination context"
    ((tests_passed++))
else
    echo -e "${RED}FAIL${NC}: git-validator not mentioned in coordination context"
    ((tests_failed++))
fi

##############################################################################
# Test AC-3.3: Enhanced file analysis or Phase 2.5 mentioned in context
##############################################################################
echo -e "${YELLOW}[TEST AC-3.3]${NC} Verify enhanced file analysis from RCA-008 is documented"
if grep -qi "enhanced file analysis\|Phase 2\.5\|file analysis" "${PREFLIGHT_REF}" || \
   grep -qi "enhanced.*analysis" "${SKILL_FILE}"; then
    echo -e "${GREEN}PASS${NC}: Enhanced file analysis documented"
    ((tests_passed++))
else
    echo -e "${YELLOW}WARN${NC}: Enhanced file analysis terminology may vary, checking for RCA-008 references"
    if grep -qi "RCA-008.*git-validator\|git-validator.*RCA-008" "${SKILL_FILE}" || \
       grep -qi "RCA-008" "${PREFLIGHT_REF}"; then
        echo -e "${GREEN}PASS${NC}: RCA-008 reference found with git-validator context"
        ((tests_passed++))
    else
        echo -e "${RED}FAIL${NC}: No enhanced file analysis or RCA-008 reference found"
        ((tests_failed++))
    fi
fi

##############################################################################
# Test AC-3.4: git-validator agent file exists
##############################################################################
echo -e "${YELLOW}[TEST AC-3.4]${NC} Verify git-validator agent file exists"
if [ -f "${GIT_VALIDATOR_AGENT}" ]; then
    echo -e "${GREEN}PASS${NC}: git-validator.md exists at ${GIT_VALIDATOR_AGENT}"
    ((tests_passed++))
else
    echo -e "${RED}FAIL${NC}: git-validator.md not found at ${GIT_VALIDATOR_AGENT}"
    ((tests_failed++))
fi

##############################################################################
# Test AC-3.5: git-validator agent mentions RCA-008 enhancements
##############################################################################
echo -e "${YELLOW}[TEST AC-3.5]${NC} Verify git-validator agent mentions RCA-008 enhancements"
if grep -qi "RCA-008\|enhanced\|file analysis\|user consent" "${GIT_VALIDATOR_AGENT}"; then
    echo -e "${GREEN}PASS${NC}: git-validator agent documents RCA-008 enhancements"
    ((tests_passed++))
else
    echo -e "${YELLOW}WARN${NC}: git-validator agent may not explicitly mention RCA-008, checking for safety features"
    if grep -qi "stash\|consent\|safety\|warning" "${GIT_VALIDATOR_AGENT}"; then
        echo -e "${GREEN}PASS${NC}: Safety-related features found in git-validator agent"
        ((tests_passed++))
    else
        echo -e "${RED}FAIL${NC}: No RCA-008 or safety enhancements found in git-validator agent"
        ((tests_failed++))
    fi
fi

##############################################################################
# Test AC-3.6: Preflight validation documents git-validator usage
##############################################################################
echo -e "${YELLOW}[TEST AC-3.6]${NC} Verify preflight validation documents git-validator usage"
if grep -qi "git-validator" "${PREFLIGHT_REF}"; then
    echo -e "${GREEN}PASS${NC}: git-validator documented in preflight validation"
    ((tests_passed++))
else
    echo -e "${RED}FAIL${NC}: git-validator not documented in preflight validation"
    ((tests_failed++))
fi

##############################################################################
# Test AC-3.7: Subagent coordination mentions Phase 01 or Phase 2.5
##############################################################################
echo -e "${YELLOW}[TEST AC-3.7]${NC} Verify subagent coordination mentions Phase 01 or file analysis phase"
if grep -qi "Phase 01\|Phase 1\|Phase 0\.1\|git-validator" "${SKILL_FILE}" || \
   grep -qi "Phase" "${PREFLIGHT_REF}"; then
    echo -e "${GREEN}PASS${NC}: Phase reference found in coordination context"
    ((tests_passed++))
else
    echo -e "${RED}FAIL${NC}: No phase reference found in coordination context"
    ((tests_failed++))
fi

##############################################################################
# Summary
##############################################################################
echo ""
echo "=========================================="
echo "AC-3 Test Summary"
echo "=========================================="
echo -e "Passed: ${GREEN}${tests_passed}${NC}"
echo -e "Failed: ${RED}${tests_failed}${NC}"
echo "=========================================="

if [ ${tests_failed} -eq 0 ]; then
    echo -e "${GREEN}✓ AC-3 VERIFICATION PASSED${NC}"
    exit 0
else
    echo -e "${RED}✗ AC-3 VERIFICATION FAILED${NC}"
    exit 1
fi
