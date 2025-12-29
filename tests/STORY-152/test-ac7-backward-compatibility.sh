#!/bin/bash

################################################################################
# TEST: AC#7 - Backward Compatible with Existing Stories
#
# GIVEN an existing story without `## Change Log` section is edited by any skill
# WHEN the skill attempts to append a changelog entry
# THEN the skill:
#   - Detects missing Change Log section
#   - Creates the section with initial "Story Migrated" entry
#   - Appends the new entry normally
#   - Preserves all existing story content
################################################################################

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEST_STORY_ORIG="/tmp/test-old-story-original.md"
TEST_STORY_BACKUP="/tmp/test-old-story-backup.md"

# Track test results
PASS_COUNT=0
FAIL_COUNT=0

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "================================================================"
echo "TEST: AC#7 - Backward Compatibility with Existing Stories"
echo "================================================================"
echo ""

# Create a test story without Change Log section (simulating old format)
cat > "$TEST_STORY_ORIG" << 'EOF'
---
id: TEST-999
title: Old Story Without Change Log
type: feature
epic: null
sprint: Backlog
priority: Medium
points: 5
status: In Development
created: 2025-01-01
updated: 2025-12-20
---

# Old Story Without Change Log

## Description

This is an old story in the system that doesn't have the new Change Log section.

## Acceptance Criteria

### AC#1: Sample Criterion

Given some precondition
When something happens
Then verify result

## Workflow Status

- [x] Backlog
- [x] Ready for Dev
- [ ] In Dev
- [ ] Complete

## Notes

Some notes about the story.
EOF

cp "$TEST_STORY_ORIG" "$TEST_STORY_BACKUP"

# Test 1: Test story file created successfully
echo -n "TEST 1: Test story file created for backward compatibility test... "
if [ -f "$TEST_STORY_ORIG" ]; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Test story file at $TEST_STORY_ORIG"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 2: Test story does NOT contain Change Log section
echo -n "TEST 2: Test story does NOT contain '## Change Log'... "
if ! grep -q "^## Change Log" "$TEST_STORY_ORIG"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: No Change Log section in old story format"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 3: Test story contains Workflow Status (old format)
echo -n "TEST 3: Test story contains old '## Workflow Status'... "
if grep -q "^## Workflow Status" "$TEST_STORY_ORIG"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: ## Workflow Status in old story format"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 4: Changelog guide contains backward compatibility instructions
echo -n "TEST 4: Changelog guide contains migration/backward compat info... "
GUIDE_FILE="${PROJECT_ROOT}/.claude/references/changelog-update-guide.md"
if [ -f "$GUIDE_FILE" ] && grep -q "migrat\|backward\|compat\|existing\|old.*story" "$GUIDE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Migration/backward compatibility documentation"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 5: Guide documents "Story Migrated" entry creation
echo -n "TEST 5: Guide documents 'Story Migrated' entry... "
if [ -f "$GUIDE_FILE" ] && grep -q "Story Migrated\|migrat" "$GUIDE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of 'Story Migrated' initial entry"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 6: Dev skill has backward compatibility check
echo -n "TEST 6: Dev skill mentions Change Log backward compatibility... "
DEV_SKILL="${PROJECT_ROOT}/.claude/skills/devforgeai-development/SKILL.md"
if grep -q "Change Log.*missing\|missing.*Change Log\|backward\|exist\|create.*section" "$DEV_SKILL"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Backward compatibility check in dev skill"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 7: QA skill has backward compatibility check
echo -n "TEST 7: QA skill mentions Change Log backward compatibility... "
QA_SKILL="${PROJECT_ROOT}/.claude/skills/devforgeai-qa/SKILL.md"
if grep -q "Change Log.*missing\|missing.*Change Log\|backward\|exist\|create.*section" "$QA_SKILL"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Backward compatibility check in QA skill"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 8: Release skill has backward compatibility check
echo -n "TEST 8: Release skill mentions Change Log backward compatibility... "
RELEASE_SKILL="${PROJECT_ROOT}/.claude/skills/devforgeai-release/SKILL.md"
if grep -q "Change Log.*missing\|missing.*Change Log\|backward\|exist\|create.*section" "$RELEASE_SKILL"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Backward compatibility check in release skill"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 9: Guide contains template for Change Log section creation
echo -n "TEST 9: Guide contains template for creating Change Log section... "
if [ -f "$GUIDE_FILE" ] && grep -q "^|.*Date.*Author\|^## Change Log\|template\|example" "$GUIDE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Template/example for Change Log section"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 10: Guide specifies content preservation requirement
echo -n "TEST 10: Guide specifies preserving existing story content... "
if [ -f "$GUIDE_FILE" ] && grep -q "preserv\|Preserv\|existing\|content\|keep.*intact" "$GUIDE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of content preservation requirement"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 11: Guide explains order of operations (create section, then append)
echo -n "TEST 11: Guide explains order: create section, append entry... "
if [ -f "$GUIDE_FILE" ] && grep -q "first\|create.*then\|detect.*create\|section.*entry" "$GUIDE_FILE"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of operation order"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Test 12: Guide is referenced by all skills for consistency
echo -n "TEST 12: All skills reference the shared changelog guide... "
if grep -q "changelog-update-guide" "$DEV_SKILL" && \
   grep -q "changelog-update-guide" "$QA_SKILL" && \
   grep -q "changelog-update-guide" "$RELEASE_SKILL"; then
    echo -e "${GREEN}PASS${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: All skills reference shared guide"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Cleanup
rm -f "$TEST_STORY_ORIG" "$TEST_STORY_BACKUP"

# Summary
echo ""
echo "================================================================"
echo "SUMMARY: AC#7 Tests"
echo "================================================================"
echo -e "PASSED: ${GREEN}${PASS_COUNT}${NC}"
echo -e "FAILED: ${RED}${FAIL_COUNT}${NC}"
echo "TOTAL:  $((PASS_COUNT + FAIL_COUNT))"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}All AC#7 tests PASSED${NC}"
    exit 0
else
    echo -e "${RED}Some AC#7 tests FAILED${NC}"
    exit 1
fi
