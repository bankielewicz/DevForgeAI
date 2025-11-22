#!/bin/bash
################################################################################
# Test Suite: AC#7 - Source and Operational Sync Preparation
#
# Tests for acceptance criterion 7: Verifying that documentation updates are
# in source files (src/*), not operational files (.claude/memory/), and that
# a sync checklist is created for STORY-060.
#
# Test Framework: Bash/Shell (grep, test -f)
# Test Pattern: AAA (Arrange, Act, Assert)
#
# Status: RED PHASE - All tests should FAIL (implementation not started)
################################################################################

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

TESTS_PASSED=0
TESTS_FAILED=0

# Source files (these SHOULD be updated)
SOURCE_CLAUDE_MD="src/CLAUDE.md"
SOURCE_COMMANDS_REF="src/claude/memory/commands-reference.md"
SOURCE_SKILLS_REF="src/claude/memory/skills-reference.md"

# Operational files (these should NOT be directly modified by STORY-058)
OPERATIONAL_CLAUDE_MD="CLAUDE.md"
OPERATIONAL_COMMANDS_REF=".claude/memory/commands-reference.md"
OPERATIONAL_SKILLS_REF=".claude/memory/skills-reference.md"

# Sync checklist file
SYNC_CHECKLIST=".devforgeai/stories/STORY-058/sync-checklist.md"

################################################################################
# Helper Functions
################################################################################

assert_file_exists() {
    local file="$1"
    local test_name="$2"

    if [[ -f "$file" ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        echo "  File exists: $file"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  File not found: $file"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

assert_file_not_modified() {
    local file="$1"
    local test_name="$2"

    if [[ ! -f "$file" ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        echo "  File not modified (not present): $file"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        # Check if file was modified in this git session
        # (This is a soft check - file may be from previous work)
        echo -e "${YELLOW}INFO${NC}: $test_name"
        echo "  File exists (may be from pre-existing state): $file"
        echo "  Note: STORY-058 should NOT directly modify operational files"
    fi
}

assert_source_file_has_content() {
    local file="$1"
    local search_pattern="$2"
    local test_name="$3"

    if [[ ! -f "$file" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Source file not found: $file"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi

    if grep -q "$search_pattern" "$file"; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Pattern not found: '$search_pattern' in $file"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

assert_checklist_entry() {
    local file="$1"
    local from_file="$2"
    local to_file="$3"
    local test_name="$4"

    if [[ ! -f "$file" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Sync checklist not found: $file"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi

    # Look for entry in checklist
    if grep -q "$from_file.*$to_file\|$from_file\|$to_file" "$file"; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Sync entry not found in checklist for $from_file -> $to_file"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

################################################################################
# TEST CASES: AC#7 - Source and Operational Sync Preparation
################################################################################

echo "=========================================="
echo "TEST SUITE: AC#7 - Sync Preparation"
echo "=========================================="
echo ""

# Test 7.1: Source files exist and contain updates
echo "Test 7.1: Source CLAUDE.md exists with Learning section"
assert_source_file_has_content "$SOURCE_CLAUDE_MD" \
    "Learning DevForgeAI" \
    "Source file has Learning section" || true
echo ""

echo "Test 7.2: Source commands-reference.md exists with cross-references"
assert_source_file_has_content "$SOURCE_COMMANDS_REF" \
    "User Input Guidance" \
    "Source file has User Input Guidance sections" || true
echo ""

echo "Test 7.3: Source skills-reference.md exists with cross-references"
assert_source_file_has_content "$SOURCE_SKILLS_REF" \
    "User Input Guidance" \
    "Source file has User Input Guidance sections" || true
echo ""

# Test 7.2: Verify source files are updated (not just operational)
echo "Test 7.4: Cross-references are in src/ tree (source files)"
{
    local claude_updated=0
    local commands_updated=0
    local skills_updated=0

    [[ -f "$SOURCE_CLAUDE_MD" ]] && \
        grep -q "Learning DevForgeAI" "$SOURCE_CLAUDE_MD" && \
        claude_updated=1

    [[ -f "$SOURCE_COMMANDS_REF" ]] && \
        grep -q "User Input Guidance" "$SOURCE_COMMANDS_REF" && \
        commands_updated=1

    [[ -f "$SOURCE_SKILLS_REF" ]] && \
        grep -q "User Input Guidance" "$SOURCE_SKILLS_REF" && \
        skills_updated=1

    if [[ $claude_updated -eq 1 && $commands_updated -eq 1 && $skills_updated -eq 1 ]]; then
        echo -e "${GREEN}PASS${NC}: All three source files updated"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC}: Not all source files have updates"
        echo "  CLAUDE.md: $claude_updated, commands-reference.md: $commands_updated, skills-reference.md: $skills_updated"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}
echo ""

# Test 7.3: Operational files NOT modified by STORY-058 (left for STORY-060)
echo "Test 7.5: Operational files not modified (reserved for STORY-060 sync)"
{
    # Note: These checks are informational since operational files may exist from before
    local info_message=""

    if [[ -f "$OPERATIONAL_CLAUDE_MD" ]]; then
        info_message="$info_message\n  - CLAUDE.md exists (from pre-existing state)"
    fi

    if [[ -f "$OPERATIONAL_COMMANDS_REF" ]]; then
        info_message="$info_message\n  - .claude/memory/commands-reference.md exists"
    fi

    if [[ -f "$OPERATIONAL_SKILLS_REF" ]]; then
        info_message="$info_message\n  - .claude/memory/skills-reference.md exists"
    fi

    echo -e "${YELLOW}INFO${NC}: Operational files status"
    if [[ -z "$info_message" ]]; then
        echo "  No operational documentation files found (clean for STORY-060 sync)"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "  Following files exist (check if from STORY-058 or pre-existing)$info_message"
        echo "  ✓ STORY-058 should not modify operational files"
    fi
}
echo ""

# Test 7.4: Sync checklist exists
echo "Test 7.6: Sync checklist created for STORY-060"
{
    if [[ -f "$SYNC_CHECKLIST" ]]; then
        echo -e "${GREEN}PASS${NC}: Sync checklist file exists: $SYNC_CHECKLIST"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC}: Sync checklist not found: $SYNC_CHECKLIST"
        echo "  Expected path: $SYNC_CHECKLIST"
        echo "  Or acceptable alternative: .devforgeai/stories/STORY-058/SYNC-CHECKLIST.md"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}
echo ""

# Test 7.5: Sync checklist contains required entries
echo "Test 7.7: Sync checklist lists all 3 files requiring synchronization"
{
    if [[ -f "$SYNC_CHECKLIST" ]]; then
        local has_claude=0
        local has_commands=0
        local has_skills=0

        grep -q "src/CLAUDE.md\|CLAUDE.md" "$SYNC_CHECKLIST" && has_claude=1
        grep -q "commands-reference.md" "$SYNC_CHECKLIST" && has_commands=1
        grep -q "skills-reference.md" "$SYNC_CHECKLIST" && has_skills=1

        if [[ $has_claude -eq 1 && $has_commands -eq 1 && $has_skills -eq 1 ]]; then
            echo -e "${GREEN}PASS${NC}: All 3 file synchronizations listed"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo -e "${RED}FAIL${NC}: Incomplete sync checklist"
            echo "  CLAUDE.md: $has_claude, commands-reference.md: $has_commands, skills-reference.md: $has_skills"
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi
    else
        echo -e "${RED}FAIL${NC}: Cannot verify checklist (file not found)"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}
echo ""

# Test 7.6: Sync checklist has clear source->destination mappings
echo "Test 7.8: Sync checklist specifies source and destination paths"
{
    if [[ -f "$SYNC_CHECKLIST" ]]; then
        # Look for arrow or mapping notation (-> or to or →)
        if grep -q "->.*\|to\|→" "$SYNC_CHECKLIST"; then
            echo -e "${GREEN}PASS${NC}: Sync checklist has clear mappings"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo -e "${RED}FAIL${NC}: Sync checklist missing source->destination mappings"
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi
    else
        echo -e "${RED}FAIL${NC}: Cannot verify checklist structure (file not found)"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}
echo ""

# Test 7.7: Sync checklist has checkbox items
echo "Test 7.9: Sync checklist has checkbox items for tracking completion"
{
    if [[ -f "$SYNC_CHECKLIST" ]]; then
        local checkbox_count=$(grep -c "\[ \]\|\[x\]\|\[X\]" "$SYNC_CHECKLIST" || echo 0)

        if [[ $checkbox_count -ge 3 ]]; then
            echo -e "${GREEN}PASS${NC}: Found $checkbox_count checkbox items"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo -e "${RED}FAIL${NC}: Insufficient checkboxes ($checkbox_count found, expected ≥3)"
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi
    else
        echo -e "${RED}FAIL${NC}: Cannot verify checklist items (file not found)"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}
echo ""

# Test 7.8: Sync checklist mentions STORY-060
echo "Test 7.10: Sync checklist references STORY-060 (the sync story)"
{
    if [[ -f "$SYNC_CHECKLIST" ]]; then
        if grep -q "STORY-060\|story-060\|sync" "$SYNC_CHECKLIST"; then
            echo -e "${GREEN}PASS${NC}: Checklist references STORY-060"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo -e "${YELLOW}INFO${NC}: Checklist may not explicitly reference STORY-060"
            echo "  This is acceptable if context is clear from filename"
        fi
    else
        echo -e "${RED}FAIL${NC}: Cannot verify checklist (file not found)"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}
echo ""

################################################################################
# Test Summary
################################################################################

echo "=========================================="
echo "TEST SUMMARY: AC#7"
echo "=========================================="
echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [[ $TESTS_FAILED -gt 0 ]]; then
    exit 1
else
    exit 0
fi
