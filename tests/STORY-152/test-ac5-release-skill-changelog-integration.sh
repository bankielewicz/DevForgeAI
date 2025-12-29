#!/bin/bash

################################################################################
# TEST: AC#5 - devforgeai-release Skill Appends Changelog and Archives Story
#
# GIVEN a story transitions from QA Approved to Released via `/release STORY-XXX`
# WHEN the devforgeai-release skill completes release workflow
# THEN the skill:
#   - Appends final Change Log entry with author `claude/deployment-engineer`
#   - Updates `**Current Status:**` to "Released"
#   - Moves story file to `devforgeai/specs/Stories/archive/` subdirectory
#   - Updates project CHANGELOG.md with story reference
################################################################################

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
RELEASE_SKILL="${PROJECT_ROOT}/.claude/skills/devforgeai-release/SKILL.md"
RELEASE_DOCS="${PROJECT_ROOT}/.claude/skills/devforgeai-release/references/release-documentation.md"
SOURCE_TREE="${PROJECT_ROOT}/devforgeai/specs/context/source-tree.md"
ARCHIVE_DIR="${PROJECT_ROOT}/devforgeai/specs/Stories/archive"

# Track test results
PASS_COUNT=0
FAIL_COUNT=0

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "================================================================"
echo "TEST: AC#5 - devforgeai-release Skill Changelog & Archive"
echo "================================================================"
echo ""

# Test 1: devforgeai-release SKILL.md exists
echo -n "TEST 1: devforgeai-release SKILL.md exists... "
if [ -f "$RELEASE_SKILL" ]; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected file: $RELEASE_SKILL"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 2: SKILL.md contains reference to changelog-update-guide
echo -n "TEST 2: SKILL.md references 'changelog-update-guide'... "
if grep -q "changelog-update-guide\|Change Log\|changelog" "$RELEASE_SKILL"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Reference to changelog guide or Change Log section"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 3: SKILL.md contains Phase 5 reference
echo -n "TEST 3: SKILL.md contains 'Phase 5' reference... "
if grep -q "Phase 5" "$RELEASE_SKILL"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Phase 5 section in release skill"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 4: SKILL.md contains changelog append instruction in Phase 5
echo -n "TEST 4: Phase 5 contains changelog append instruction... "
if grep -A 30 "Phase 5" "$RELEASE_SKILL" | grep -q "Change Log\|changelog\|append\|Edit"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Changelog append instructions in Phase 5"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 5: SKILL.md specifies 'claude/deployment-engineer' author
echo -n "TEST 5: SKILL.md specifies 'claude/deployment-engineer' author... "
if grep -q "claude/deployment-engineer\|deployment-engineer" "$RELEASE_SKILL"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: claude/deployment-engineer as release entry author"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 6: SKILL.md mentions story archiving
echo -n "TEST 6: SKILL.md mentions archiving story... "
if grep -q "archiv\|archive\|move.*story\|Stories/archive" "$RELEASE_SKILL"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Reference to story archiving workflow"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 7: release-documentation.md exists
echo -n "TEST 7: release-documentation.md exists... "
if [ -f "$RELEASE_DOCS" ]; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected file: $RELEASE_DOCS"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 8: release-documentation.md contains archive step
echo -n "TEST 8: release-documentation.md contains archive step... "
if grep -q "archiv\|archive\|move.*file\|Stories/archive" "$RELEASE_DOCS"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Archive/move step documentation"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 9: source-tree.md documents Stories/archive directory
echo -n "TEST 9: source-tree.md mentions 'Stories/archive' directory... "
if grep -q "Stories/archive\|archive/" "$SOURCE_TREE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of archive directory in source-tree.md"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 10: SKILL.md mentions updating Current Status to Released
echo -n "TEST 10: SKILL.md mentions 'Released' status update... "
if grep -q "Released\|released\|status.*Released" "$RELEASE_SKILL"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Reference to updating status to Released"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 11: SKILL.md mentions CHANGELOG.md update
echo -n "TEST 11: SKILL.md mentions 'CHANGELOG.md' update... "
if grep -q "CHANGELOG\|changelog" "$RELEASE_SKILL"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Reference to project CHANGELOG.md update"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 12: SKILL.md is valid markdown
echo -n "TEST 12: SKILL.md is valid markdown file... "
if head -1 "$RELEASE_SKILL" | grep -q "^#\|^---"; then
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
echo "SUMMARY: AC#5 Tests"
echo "================================================================"
echo -e "PASSED: ${GREEN}${PASS_COUNT}${NC}"
echo -e "FAILED: ${RED}${FAIL_COUNT}${NC}"
echo "TOTAL:  $((PASS_COUNT + FAIL_COUNT))"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}All AC#5 tests PASSED${NC}"
    exit 0
else
    echo -e "${RED}Some AC#5 tests FAILED${NC}"
    exit 1
fi
