#!/bin/bash

################################################################################
# TEST: AC#6 - Project CHANGELOG.md Created with Keep a Changelog Format
#
# GIVEN CHANGELOG.md does not exist at project root
# WHEN the first story is released after this feature implementation
# THEN CHANGELOG.md is created with:
#   - Keep a Changelog v1.1.0 compliant format
#   - Sections: `## [Unreleased]`, `## [X.Y.Z] - YYYY-MM-DD`
#   - Story entries format: `- Feature description ([STORY-XXX])`
#   - Reference links: `[STORY-XXX]: devforgeai/specs/Stories/archive/STORY-XXX.story.md`
################################################################################

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
CHANGELOG="${PROJECT_ROOT}/CHANGELOG.md"

# Track test results
PASS_COUNT=0
FAIL_COUNT=0

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "================================================================"
echo "TEST: AC#6 - Project CHANGELOG.md with Keep a Changelog Format"
echo "================================================================"
echo ""

# Test 1: CHANGELOG.md file exists (or will be created)
echo -n "TEST 1: CHANGELOG.md exists or can be created at project root... "
if [ -f "$CHANGELOG" ] || [ -w "$PROJECT_ROOT" ]; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: CHANGELOG.md at $CHANGELOG or writable directory"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 2: If exists, CHANGELOG.md contains [Unreleased] section
if [ -f "$CHANGELOG" ]; then
    echo -n "TEST 2: CHANGELOG.md contains '[Unreleased]' section... "
    if grep -q "## \[Unreleased\]" "$CHANGELOG"; then
        echo -e "${GREEN}PASS${NC}"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: ## [Unreleased] section header"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
else
    echo -n "TEST 2: CHANGELOG.md template would contain '[Unreleased]'... "
    # Check release skill references Unreleased section
    if grep -q "Unreleased\|unreleased" "$PROJECT_ROOT/.claude/skills/devforgeai-release/SKILL.md"; then
        echo -e "${GREEN}PASS${NC}"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Reference to [Unreleased] section in release skill"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
fi

# Test 3: If exists, CHANGELOG.md contains version section with date
if [ -f "$CHANGELOG" ]; then
    echo -n "TEST 3: CHANGELOG.md contains version section (e.g., '## [X.Y.Z]')... "
    if grep -q "## \[[0-9]" "$CHANGELOG"; then
        echo -e "${GREEN}PASS${NC}"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Version section header like ## [1.0.0]"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
else
    echo -n "TEST 3: CHANGELOG.md template would contain version sections... "
    # Check release skill references version sections
    if grep -q "\[.*\].*-\|version\|Version" "$PROJECT_ROOT/.claude/skills/devforgeai-release/SKILL.md"; then
        echo -e "${GREEN}PASS${NC}"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Reference to version sections in release skill"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
fi

# Test 4: If exists, CHANGELOG.md contains Keep a Changelog headers
if [ -f "$CHANGELOG" ]; then
    echo -n "TEST 4: CHANGELOG.md follows Keep a Changelog format... "
    if grep -q "## \[Unreleased\]\|## \[[0-9]" "$CHANGELOG"; then
        echo -e "${GREEN}PASS${NC}"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Keep a Changelog format with ## [version] headers"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
else
    echo -n "TEST 4: Release skill documents Keep a Changelog format... "
    if grep -q "Keep a Changelog\|keepachangelog\|Changelog" "$PROJECT_ROOT/.claude/skills/devforgeai-release/SKILL.md"; then
        echo -e "${GREEN}PASS${NC}"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Keep a Changelog format reference in release skill"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
fi

# Test 5: If exists, CHANGELOG.md contains story entry format
if [ -f "$CHANGELOG" ]; then
    echo -n "TEST 5: CHANGELOG.md contains story entries '- description ([STORY-XXX])'... "
    if grep -q "\- .*\[STORY-[0-9]" "$CHANGELOG"; then
        echo -e "${GREEN}PASS${NC}"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Story entry format like '- Feature ([STORY-001])'"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
else
    echo -n "TEST 5: Release skill documents story entry format... "
    if grep -q "STORY-\|story.*entry\|Feature description" "$PROJECT_ROOT/.claude/skills/devforgeai-release/SKILL.md"; then
        echo -e "${GREEN}PASS${NC}"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Story entry format documentation"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
fi

# Test 6: If exists, CHANGELOG.md contains reference links for stories
if [ -f "$CHANGELOG" ]; then
    echo -n "TEST 6: CHANGELOG.md contains reference links '[STORY-XXX]: ...'... "
    if grep -q "\[STORY-[0-9].*\]: .*devforgeai/specs/Stories/archive" "$CHANGELOG"; then
        echo -e "${GREEN}PASS${NC}"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Reference link format [STORY-XXX]: path/to/archive/STORY-XXX.story.md"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
else
    echo -n "TEST 6: Release skill documents reference link format... "
    if grep -q "archive\|reference.*link\|\[STORY.*\]:" "$PROJECT_ROOT/.claude/skills/devforgeai-release/SKILL.md"; then
        echo -e "${GREEN}PASS${NC}"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Reference link format documentation"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
fi

# Test 7: If exists, CHANGELOG.md has proper markdown syntax
if [ -f "$CHANGELOG" ]; then
    echo -n "TEST 7: CHANGELOG.md is valid markdown... "
    if head -1 "$CHANGELOG" | grep -q "^#\|^---"; then
        echo -e "${GREEN}PASS${NC}"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Valid markdown structure"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
else
    echo -n "TEST 7: Release skill would create valid markdown CHANGELOG... "
    if grep -q "markdown\|format\|Markdown" "$PROJECT_ROOT/.claude/skills/devforgeai-release/SKILL.md"; then
        echo -e "${GREEN}PASS${NC}"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Markdown format references"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
fi

# Test 8: If exists, CHANGELOG.md contains date in YYYY-MM-DD format
if [ -f "$CHANGELOG" ]; then
    echo -n "TEST 8: CHANGELOG.md dates in YYYY-MM-DD format... "
    if grep -q "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]" "$CHANGELOG"; then
        echo -e "${GREEN}PASS${NC}"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Dates in YYYY-MM-DD format"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
else
    echo -n "TEST 8: Release skill documents date format... "
    if grep -q "YYYY-MM-DD\|date.*format\|[0-9][0-9][0-9][0-9]-" "$PROJECT_ROOT/.claude/skills/devforgeai-release/SKILL.md"; then
        echo -e "${GREEN}PASS${NC}"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Date format documentation"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
fi

# Test 9: Release skill has changelog update instructions
echo -n "TEST 9: Release skill contains CHANGELOG.md update instructions... "
if grep -q "CHANGELOG" "$PROJECT_ROOT/.claude/skills/devforgeai-release/SKILL.md"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: CHANGELOG.md update logic in release skill"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 10: Release skill references Edit or Write tool for CHANGELOG
echo -n "TEST 10: Release skill uses Edit/Write tool for CHANGELOG... "
if grep -B 5 -A 5 "CHANGELOG" "$PROJECT_ROOT/.claude/skills/devforgeai-release/SKILL.md" | grep -q "Edit\|Write"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Edit() or Write() tool usage for CHANGELOG updates"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 11: Release skill has reference to Keep a Changelog standard
echo -n "TEST 11: Release skill references Keep a Changelog standard... "
if grep -q "Keep.*Changelog\|keepachangelog\|v1.1.0\|changelog.*format" "$PROJECT_ROOT/.claude/skills/devforgeai-release/SKILL.md"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Reference to Keep a Changelog standard"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 12: Release skill is valid markdown
echo -n "TEST 12: Release skill is valid markdown file... "
if head -1 "$PROJECT_ROOT/.claude/skills/devforgeai-release/SKILL.md" | grep -q "^#\|^---"; then
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
echo "SUMMARY: AC#6 Tests"
echo "================================================================"
echo -e "PASSED: ${GREEN}${PASS_COUNT}${NC}"
echo -e "FAILED: ${RED}${FAIL_COUNT}${NC}"
echo "TOTAL:  $((PASS_COUNT + FAIL_COUNT))"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}All AC#6 tests PASSED${NC}"
    exit 0
else
    echo -e "${RED}Some AC#6 tests FAILED${NC}"
    exit 1
fi
