#!/bin/bash

################################################################################
# TEST: AC#4 - devforgeai-qa Skill Appends Changelog Entry
#
# GIVEN a QA validator runs `/qa STORY-XXX` on a story
# WHEN QA validation completes (passed or failed)
# THEN the devforgeai-qa skill appends a Change Log entry with:
#   - Author: `claude/qa-result-interpreter`
#   - Phase/Action: "QA {mode}" (Light or Deep)
#   - Change: "{result}: Coverage {pct}%, {violations} violations"
################################################################################

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
QA_SKILL="${PROJECT_ROOT}/.claude/skills/devforgeai-qa/SKILL.md"

# Track test results
PASS_COUNT=0
FAIL_COUNT=0

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "================================================================"
echo "TEST: AC#4 - devforgeai-qa Skill Changelog Integration"
echo "================================================================"
echo ""

# Test 1: devforgeai-qa SKILL.md exists
echo -n "TEST 1: devforgeai-qa SKILL.md exists... "
if [ -f "$QA_SKILL" ]; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected file: $QA_SKILL"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 2: SKILL.md contains reference to changelog-update-guide
echo -n "TEST 2: SKILL.md references 'changelog-update-guide'... "
if grep -q "changelog-update-guide\|Change Log\|changelog" "$QA_SKILL"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Reference to changelog guide or Change Log section"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 3: SKILL.md references Phase 3.4 or Story File Update
echo -n "TEST 3: SKILL.md contains Phase 3.4 or 'Story File Update'... "
if grep -q "Phase 3.4\|3.4\|Story File Update" "$QA_SKILL"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Reference to Phase 3.4 or Story File Update section"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 4: SKILL.md contains changelog append instruction in Phase 3.4
echo -n "TEST 4: Phase 3.4 contains changelog append instruction... "
if grep -q "Phase 3.4\|3.4" "$QA_SKILL" && grep -q "Change Log\|changelog\|append\|Edit" "$QA_SKILL"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Changelog append instructions in Phase 3.4"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 5: SKILL.md specifies 'claude/qa-result-interpreter' author
echo -n "TEST 5: SKILL.md specifies 'claude/qa-result-interpreter' author... "
if grep -q "claude/qa-result-interpreter\|qa-result-interpreter" "$QA_SKILL"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: claude/qa-result-interpreter as QA entry author"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 6: SKILL.md contains format for QA result entry
echo -n "TEST 6: SKILL.md contains QA result format (Coverage %, violations)... "
if grep -q "Coverage\|coverage\|%\|violations" "$QA_SKILL"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: QA result format documentation"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 7: SKILL.md mentions both Light and Deep modes
echo -n "TEST 7: SKILL.md mentions both 'Light' and 'Deep' QA modes... "
if grep -q "Light\|light" "$QA_SKILL" && grep -q "Deep\|deep" "$QA_SKILL"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Both Light and Deep QA mode references"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 8: SKILL.md contains Phase/Action terminology
echo -n "TEST 8: SKILL.md uses 'Phase/Action' terminology... "
if grep -q "Phase.*Action\|Phase/Action\|QA Light\|QA Deep" "$QA_SKILL"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Phase/Action or QA mode descriptions"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 9: SKILL.md contains Example of changelog entry format
echo -n "TEST 9: SKILL.md has example or template of QA changelog entry... "
if grep -q "QA.*Coverage\|Coverage.*%" "$QA_SKILL" && grep -q "|" "$QA_SKILL"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Example QA changelog entry in markdown table format"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 10: SKILL.md contains Edit tool reference for changelog updates
echo -n "TEST 10: SKILL.md references Edit tool for changelog... "
if grep -q "Change Log\|changelog" "$QA_SKILL" && grep -q "Edit" "$QA_SKILL"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Edit() tool usage in changelog append section"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 11: SKILL.md is valid markdown
echo -n "TEST 11: SKILL.md is valid markdown file... "
if head -1 "$QA_SKILL" | grep -q "^#\|^---"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Valid markdown structure"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 12: SKILL.md contains story status update context
echo -n "TEST 12: SKILL.md context shows story status/state transitions... "
if grep -q "status\|Status\|state\|State\|transition\|Transition" "$QA_SKILL"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Context about story status transitions"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Summary
echo ""
echo "================================================================"
echo "SUMMARY: AC#4 Tests"
echo "================================================================"
echo -e "PASSED: ${GREEN}${PASS_COUNT}${NC}"
echo -e "FAILED: ${RED}${FAIL_COUNT}${NC}"
echo "TOTAL:  $((PASS_COUNT + FAIL_COUNT))"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}All AC#4 tests PASSED${NC}"
    exit 0
else
    echo -e "${RED}Some AC#4 tests FAILED${NC}"
    exit 1
fi
