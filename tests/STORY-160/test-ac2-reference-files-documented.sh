#!/bin/bash
##############################################################################
# STORY-160: AC-2 Verification Tests
# AC-2: Reference Files Documented
#
# Test that SKILL.md Reference Files section includes required documentation
#
# Acceptance Criteria:
# Given the SKILL.md Reference Files section
# When I review the listed references
# Then it should include:
#   - preflight-validation.md with note about RCA-008 user consent steps
#   - git-workflow-conventions.md with note about Stash Safety Protocol
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
PREFLIGHT_REF="${PROJECT_ROOT}/.claude/skills/devforgeai-development/references/preflight-validation.md"
GIT_WORKFLOW_REF="${PROJECT_ROOT}/.claude/skills/devforgeai-development/references/git-workflow-conventions.md"

# Test counter
tests_passed=0
tests_failed=0

##############################################################################
# Test AC-2.1: preflight-validation.md reference documented in SKILL.md
##############################################################################
echo -e "${YELLOW}[TEST AC-2.1]${NC} Verify preflight-validation.md is listed in SKILL.md Reference Files"
if grep -q "preflight-validation\.md" "${SKILL_FILE}"; then
    echo -e "${GREEN}PASS${NC}: preflight-validation.md reference found in SKILL.md"
    ((tests_passed++))
else
    echo -e "${RED}FAIL${NC}: preflight-validation.md reference not found in SKILL.md"
    ((tests_failed++))
fi

##############################################################################
# Test AC-2.2: preflight-validation.md reference includes RCA-008 note
##############################################################################
echo -e "${YELLOW}[TEST AC-2.2]${NC} Verify preflight-validation.md reference includes RCA-008 note"
if grep -A2 "preflight-validation\.md" "${SKILL_FILE}" | grep -qi "RCA-008\|user consent"; then
    echo -e "${GREEN}PASS${NC}: RCA-008 or user consent note found with preflight-validation.md reference"
    ((tests_passed++))
else
    echo -e "${RED}FAIL${NC}: No RCA-008 or user consent note found with preflight-validation.md reference"
    # Show context
    echo "Context in SKILL.md:"
    grep -A2 "preflight-validation\.md" "${SKILL_FILE}" || echo "No preflight-validation.md reference found"
    ((tests_failed++))
fi

##############################################################################
# Test AC-2.3: git-workflow-conventions.md reference documented in SKILL.md
##############################################################################
echo -e "${YELLOW}[TEST AC-2.3]${NC} Verify git-workflow-conventions.md is listed in SKILL.md Reference Files"
if grep -q "git-workflow-conventions\.md" "${SKILL_FILE}"; then
    echo -e "${GREEN}PASS${NC}: git-workflow-conventions.md reference found in SKILL.md"
    ((tests_passed++))
else
    echo -e "${RED}FAIL${NC}: git-workflow-conventions.md reference not found in SKILL.md"
    ((tests_failed++))
fi

##############################################################################
# Test AC-2.4: git-workflow-conventions.md reference includes Stash Safety Protocol note
##############################################################################
echo -e "${YELLOW}[TEST AC-2.4]${NC} Verify git-workflow-conventions.md reference includes Stash Safety Protocol note"
if grep -A2 "git-workflow-conventions\.md" "${SKILL_FILE}" | grep -qi "Stash\|Safety Protocol"; then
    echo -e "${GREEN}PASS${NC}: Stash Safety Protocol note found with git-workflow-conventions.md reference"
    ((tests_passed++))
else
    echo -e "${RED}FAIL${NC}: No Stash Safety Protocol note found with git-workflow-conventions.md reference"
    # Show context
    echo "Context in SKILL.md:"
    grep -A2 "git-workflow-conventions\.md" "${SKILL_FILE}" || echo "No git-workflow-conventions.md reference found"
    ((tests_failed++))
fi

##############################################################################
# Test AC-2.5: preflight-validation.md file exists
##############################################################################
echo -e "${YELLOW}[TEST AC-2.5]${NC} Verify preflight-validation.md file exists"
if [ -f "${PREFLIGHT_REF}" ]; then
    echo -e "${GREEN}PASS${NC}: preflight-validation.md exists at ${PREFLIGHT_REF}"
    ((tests_passed++))
else
    echo -e "${RED}FAIL${NC}: preflight-validation.md not found at ${PREFLIGHT_REF}"
    ((tests_failed++))
fi

##############################################################################
# Test AC-2.6: git-workflow-conventions.md file exists
##############################################################################
echo -e "${YELLOW}[TEST AC-2.6]${NC} Verify git-workflow-conventions.md file exists"
if [ -f "${GIT_WORKFLOW_REF}" ]; then
    echo -e "${GREEN}PASS${NC}: git-workflow-conventions.md exists at ${GIT_WORKFLOW_REF}"
    ((tests_passed++))
else
    echo -e "${RED}FAIL${NC}: git-workflow-conventions.md not found at ${GIT_WORKFLOW_REF}"
    ((tests_failed++))
fi

##############################################################################
# Test AC-2.7: Reference Files section exists in SKILL.md
##############################################################################
echo -e "${YELLOW}[TEST AC-2.7]${NC} Verify Reference Files section exists in SKILL.md"
if grep -qi "Reference" "${SKILL_FILE}" && grep -qi "phases/" "${SKILL_FILE}"; then
    echo -e "${GREEN}PASS${NC}: Reference Files section found in SKILL.md"
    ((tests_passed++))
else
    echo -e "${RED}FAIL${NC}: Reference Files section not found in SKILL.md"
    ((tests_failed++))
fi

##############################################################################
# Test AC-2.8: Both files have RCA-008 related content
##############################################################################
echo -e "${YELLOW}[TEST AC-2.8]${NC} Verify both reference files contain RCA-008 related content"
preflight_has_rca=$(grep -ci "RCA-008\|consent\|stash\|safety" "${PREFLIGHT_REF}" || echo "0")
git_workflow_has_rca=$(grep -ci "RCA-008\|consent\|stash\|safety" "${GIT_WORKFLOW_REF}" || echo "0")

if [ "${preflight_has_rca}" -gt 0 ] && [ "${git_workflow_has_rca}" -gt 0 ]; then
    echo -e "${GREEN}PASS${NC}: Both reference files contain RCA-008 related content"
    echo "  - preflight-validation.md: ${preflight_has_rca} mentions"
    echo "  - git-workflow-conventions.md: ${git_workflow_has_rca} mentions"
    ((tests_passed++))
else
    echo -e "${RED}FAIL${NC}: One or both reference files missing RCA-008 content"
    echo "  - preflight-validation.md: ${preflight_has_rca} mentions"
    echo "  - git-workflow-conventions.md: ${git_workflow_has_rca} mentions"
    ((tests_failed++))
fi

##############################################################################
# Summary
##############################################################################
echo ""
echo "=========================================="
echo "AC-2 Test Summary"
echo "=========================================="
echo -e "Passed: ${GREEN}${tests_passed}${NC}"
echo -e "Failed: ${RED}${tests_failed}${NC}"
echo "=========================================="

if [ ${tests_failed} -eq 0 ]; then
    echo -e "${GREEN}✓ AC-2 VERIFICATION PASSED${NC}"
    exit 0
else
    echo -e "${RED}✗ AC-2 VERIFICATION FAILED${NC}"
    exit 1
fi
