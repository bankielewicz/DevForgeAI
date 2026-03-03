#!/bin/bash

################################################################################
# TEST: AC#3 - devforgeai-development Skill Appends Changelog Entries
#
# GIVEN a developer runs `/dev STORY-XXX` to implement a story
# WHEN each TDD phase completes (Red, Green, Refactor, Integration, DoD, Git)
# THEN the skill appends a Change Log entry with:
#   - Correct subagent author (e.g., `claude/test-automator` for Red phase)
#   - Phase/Action description (e.g., "Red (Phase 02)")
#   - Change summary (e.g., "Tests for AC#1-3")
#   - Files affected list
################################################################################

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
DEV_SKILL="${PROJECT_ROOT}/.claude/skills/devforgeai-development/SKILL.md"
DOD_WORKFLOW="${PROJECT_ROOT}/.claude/skills/devforgeai-development/references/dod-update-workflow.md"

# Track test results
PASS_COUNT=0
FAIL_COUNT=0

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "================================================================"
echo "TEST: AC#3 - devforgeai-development Skill Changelog Integration"
echo "================================================================"
echo ""

# Test 1: devforgeai-development SKILL.md exists
echo -n "TEST 1: devforgeai-development SKILL.md exists... "
if [ -f "$DEV_SKILL" ]; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected file: $DEV_SKILL"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 2: SKILL.md references changelog-update-guide
echo -n "TEST 2: SKILL.md references 'changelog-update-guide'... "
if grep -q "changelog-update-guide" "$DEV_SKILL"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Reference to .claude/references/changelog-update-guide.md"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 3: SKILL.md contains changelog append instruction for Red phase
echo -n "TEST 3: SKILL.md contains changelog append for Red phase... "
if grep -q "Red\|Phase 02\|Test" "$DEV_SKILL" && grep -q "Change Log\|changelog" "$DEV_SKILL"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Changelog append instruction in Red phase section"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 4: SKILL.md contains changelog append instruction for Green phase
echo -n "TEST 4: SKILL.md contains changelog append for Green phase... "
if grep -q "Green\|Phase 03\|implement" "$DEV_SKILL" && grep -q "Change Log\|changelog" "$DEV_SKILL"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Changelog append instruction in Green phase section"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 5: SKILL.md mentions test-automator as Red phase author
echo -n "TEST 5: SKILL.md specifies 'claude/test-automator' author for tests... "
if grep -q "claude/test-automator\|test-automator" "$DEV_SKILL"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: claude/test-automator as author for Red phase entries"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 6: dod-update-workflow.md exists
echo -n "TEST 6: dod-update-workflow.md exists... "
if [ -f "$DOD_WORKFLOW" ]; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected file: $DOD_WORKFLOW"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 7: dod-update-workflow.md references Change Log (not Workflow Status)
echo -n "TEST 7: dod-update-workflow.md uses 'Change Log' section... "
if grep -q "## Change Log" "$DOD_WORKFLOW"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Reference to ## Change Log section"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 8: dod-update-workflow.md does NOT reference Workflow Status
echo -n "TEST 8: dod-update-workflow.md does NOT reference 'Workflow Status'... "
if ! grep -q "## Workflow Status" "$DOD_WORKFLOW"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: No reference to deprecated ## Workflow Status"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 9: dod-update-workflow.md Step 4 contains changelog edit instruction
echo -n "TEST 9: dod-update-workflow.md Step 4 has changelog edit... "
if grep -A 20 "^## Step 4\|^### Step 4" "$DOD_WORKFLOW" | grep -q "Change Log\|changelog\|Edit.*Change"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Step 4 to contain changelog editing instructions"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 10: SKILL.md mentions multiple subagent authors
echo -n "TEST 10: SKILL.md references multiple subagent authors... "
author_count=$(grep -c "claude/" "$DEV_SKILL" 2>/dev/null) || author_count=0
if [ "$author_count" -ge 3 ]; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC} (found $author_count authors, expected >= 3)"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 11: SKILL.md contains Edit tool usage pattern
echo -n "TEST 11: SKILL.md contains Edit tool usage examples... "
if grep -q "Edit(" "$DEV_SKILL"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Edit() tool examples for appending entries"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 12: dod-update-workflow.md is properly formatted markdown
echo -n "TEST 12: dod-update-workflow.md is valid markdown... "
if head -3 "$DOD_WORKFLOW" | grep -q "^#\|^---"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Valid markdown structure"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Summary
echo ""
echo "================================================================"
echo "SUMMARY: AC#3 Tests"
echo "================================================================"
echo -e "PASSED: ${GREEN}${PASS_COUNT}${NC}"
echo -e "FAILED: ${RED}${FAIL_COUNT}${NC}"
echo "TOTAL:  $((PASS_COUNT + FAIL_COUNT))"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}All AC#3 tests PASSED${NC}"
    exit 0
else
    echo -e "${RED}Some AC#3 tests FAILED${NC}"
    exit 1
fi
