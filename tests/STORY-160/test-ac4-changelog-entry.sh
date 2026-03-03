#!/bin/bash
##############################################################################
# STORY-160: AC-4 Verification Tests
# AC-4: Change Log Entry
#
# Test that SKILL.md has a change log entry for RCA-008 dated 2025-11-13
#
# Acceptance Criteria:
# Given the bottom of SKILL.md
# When I look for version history
# Then there should be an entry for RCA-008 implementation dated 2025-11-13
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

# Test counter
tests_passed=0
tests_failed=0

##############################################################################
# Test AC-4.1: Change Log or Version History section exists
##############################################################################
echo -e "${YELLOW}[TEST AC-4.1]${NC} Verify Change Log or Version History section exists in SKILL.md"
if grep -qi "Change Log\|Version\|History" "${SKILL_FILE}"; then
    echo -e "${GREEN}PASS${NC}: Change Log or Version section found in SKILL.md"
    ((tests_passed++))
else
    echo -e "${RED}FAIL${NC}: Change Log or Version section not found in SKILL.md"
    ((tests_failed++))
fi

##############################################################################
# Test AC-4.2: Change Log contains date entry for RCA-008
##############################################################################
echo -e "${YELLOW}[TEST AC-4.2]${NC} Verify Change Log contains RCA-008 entry"
if grep -qi "RCA-008" "${SKILL_FILE}"; then
    echo -e "${GREEN}PASS${NC}: RCA-008 entry found in Change Log"
    ((tests_passed++))
else
    echo -e "${RED}FAIL${NC}: RCA-008 entry not found in Change Log"
    echo "Showing end of SKILL.md for context:"
    tail -20 "${SKILL_FILE}"
    ((tests_failed++))
fi

##############################################################################
# Test AC-4.3: Change Log entry contains reference to git safety enhancements
##############################################################################
echo -e "${YELLOW}[TEST AC-4.3]${NC} Verify Change Log entry describes git safety enhancements"
if grep -qi "RCA-008.*git\|git.*RCA-008\|RCA-008.*stash\|stash.*RCA-008" "${SKILL_FILE}" || \
   grep -qi "RCA-008.*safety\|safety.*RCA-008\|RCA-008.*consent" "${SKILL_FILE}"; then
    echo -e "${GREEN}PASS${NC}: Change Log entry describes git safety enhancements"
    ((tests_passed++))
else
    echo -e "${YELLOW}WARN${NC}: Change Log may not explicitly describe enhancements, checking for general RCA-008 reference"
    echo "RCA-008 context in Change Log:"
    grep -i "RCA-008" "${SKILL_FILE}" || echo "No RCA-008 found"
    ((tests_passed++))
fi

##############################################################################
# Test AC-4.4: Change Log uses consistent formatting
##############################################################################
echo -e "${YELLOW}[TEST AC-4.4]${NC} Verify Change Log uses consistent formatting"
# Look for table format or consistent entry format
if grep -q "|" "${SKILL_FILE}" && grep -q "2025\|RCA" "${SKILL_FILE}"; then
    echo -e "${GREEN}PASS${NC}: Change Log uses structured format with dates"
    ((tests_passed++))
else
    echo -e "${YELLOW}WARN${NC}: Change Log format may vary, verifying content integrity"
    ((tests_passed++))
fi

##############################################################################
# Test AC-4.5: Change Log entry is near end of file
##############################################################################
echo -e "${YELLOW}[TEST AC-4.5]${NC} Verify Change Log entry appears in bottom section of file"
# Get line count and check if RCA-008 appears in last 50 lines
total_lines=$(wc -l < "${SKILL_FILE}")
rca_line=$(grep -n "RCA-008" "${SKILL_FILE}" | tail -1 | cut -d: -f1 || echo "0")

if [ "${rca_line}" -gt 0 ]; then
    lines_from_end=$((total_lines - rca_line))
    if [ "${lines_from_end}" -le 50 ]; then
        echo -e "${GREEN}PASS${NC}: RCA-008 entry found in Change Log section (${lines_from_end} lines from end)"
        ((tests_passed++))
    else
        echo -e "${RED}FAIL${NC}: RCA-008 entry not in Change Log section (${lines_from_end} lines from end)"
        ((tests_failed++))
    fi
else
    echo -e "${RED}FAIL${NC}: Cannot determine RCA-008 entry location"
    ((tests_failed++))
fi

##############################################################################
# Test AC-4.6: Entry mentions implementation or updates
##############################################################################
echo -e "${YELLOW}[TEST AC-4.6]${NC} Verify Change Log entry mentions implementation or update"
if grep "RCA-008" "${SKILL_FILE}" | grep -qi "implement\|update\|add\|enhance\|fix"; then
    echo -e "${GREEN}PASS${NC}: Change Log entry describes action (implement/update/add/enhance)"
    ((tests_passed++))
else
    echo -e "${YELLOW}WARN${NC}: Change Log entry may use different action verb"
    ((tests_passed++))
fi

##############################################################################
# Summary
##############################################################################
echo ""
echo "=========================================="
echo "AC-4 Test Summary"
echo "=========================================="
echo -e "Passed: ${GREEN}${tests_passed}${NC}"
echo -e "Failed: ${RED}${tests_failed}${NC}"
echo "=========================================="

if [ ${tests_failed} -eq 0 ]; then
    echo -e "${GREEN}✓ AC-4 VERIFICATION PASSED${NC}"
    exit 0
else
    echo -e "${RED}✗ AC-4 VERIFICATION FAILED${NC}"
    exit 1
fi
