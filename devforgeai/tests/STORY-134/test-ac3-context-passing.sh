#!/bin/bash

################################################################################
# TEST SUITE: AC#3 - Smart Mode Context Passing
# Story: STORY-134 (Smart Greenfield/Brownfield Detection)
# Description: Verify the detected mode is passed to the skill via context
#              marker, and the skill's Phase 6.6 reads and uses it
#
# Acceptance Criteria:
# - Given: Command has determined project mode (greenfield or brownfield)
# - When: Phase 1 completes and control transfers to skill
# - Then: Context marker contains detected mode, parseable by Phase 6.6
#
# Context Marker Format:
#   **Project Mode Context:**
#   - **Mode:** {greenfield|brownfield}
#   - **Context Files Found:** {count}/6
#   - **Detection Method:** Filesystem glob
#
# Skill Consumption (Phase 6.6):
#   - Greenfield → recommend `/create-context [project-name]`
#   - Brownfield → recommend `/create-sprint` or `/create-story`
#
# Test Status: FAILING (Red Phase) - Context passing not yet implemented
################################################################################

set +e  # Do NOT exit on error (we handle failures in test assertions)

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEST_NAME="AC#3: Smart Mode Context Passing"
COMMAND_FILE="${PROJECT_ROOT}/.claude/commands/ideate.md"
SKILL_FILE="${PROJECT_ROOT}/.claude/skills/devforgeai-ideation/SKILL.md"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Helper function: Assert condition
assert_true() {
    local condition="$1"
    local description="$2"
    ((TESTS_RUN++))

    if eval "$condition"; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Helper function: Assert file contains text
assert_file_contains() {
    local file="$1"
    local search_text="$2"
    local description="$3"
    ((TESTS_RUN++))

    if [ ! -f "$file" ]; then
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  File not found: $file"
        ((TESTS_FAILED++))
        return 1
    fi

    if grep -q "$search_text" "$file"; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Not found in: $file"
        echo "  Search text: $search_text"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Helper function: Assert file does NOT contain text
assert_file_not_contains() {
    local file="$1"
    local search_text="$2"
    local description="$3"
    ((TESTS_RUN++))

    if [ ! -f "$file" ]; then
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  File not found: $file"
        ((TESTS_FAILED++))
        return 1
    fi

    if ! grep -q "$search_text" "$file"; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Found unexpected text in: $file"
        echo "  Unexpected text: $search_text"
        ((TESTS_FAILED++))
        return 1
    fi
}

################################################################################
# TEST 3.1: Context marker header displayed before skill invocation
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 3.1: Context Marker Header Display"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

assert_file_contains "$COMMAND_FILE" \
    "Project Mode Context" \
    "ideate.md displays 'Project Mode Context' header before skill invocation"

################################################################################
# TEST 3.2: Mode value displayed
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 3.2: Mode Value Display"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

assert_file_contains "$COMMAND_FILE" \
    "\*\*Mode:\*\*" \
    "Mode value displayed in context marker"

################################################################################
# TEST 3.3: Context files count displayed
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 3.3: Context Files Count Display"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

assert_file_contains "$COMMAND_FILE" \
    "Context Files Found.*6" \
    "Context files count displayed in format (e.g., '3/6')"

################################################################################
# TEST 3.4: Detection method documented
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 3.4: Detection Method Documentation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

assert_file_contains "$COMMAND_FILE" \
    "Detection Method\|Filesystem glob" \
    "Detection method documented in context marker"

################################################################################
# TEST 3.5: Skill reads mode in Phase 6.6
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 3.5: Skill Phase 6.6 References Mode"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

assert_file_contains "$SKILL_FILE" \
    "Phase 6\.6\|completion-handoff\|Mode:" \
    "Skill Phase 6.6 references mode for next-action recommendation"

################################################################################
# TEST 3.6: Greenfield path in Phase 6.6
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 3.6: Greenfield Next Action (Phase 6.6)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

assert_file_contains "$SKILL_FILE" \
    "greenfield.*create-context\|create-context.*greenfield" \
    "Skill Phase 6.6 recommends '/create-context' for greenfield mode"

################################################################################
# TEST 3.7: Brownfield path in Phase 6.6
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 3.7: Brownfield Next Action (Phase 6.6)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

assert_file_contains "$SKILL_FILE" \
    "brownfield.*orchestrate\|orchestrate.*brownfield" \
    "Skill Phase 6.6 recommends '/orchestrate' for brownfield mode"

################################################################################
# TEST 3.8: Mode marker is parseable (simple pattern matching)
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 3.8: Mode Marker Parseability"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Test that the marker format matches the specification
assert_file_contains "$COMMAND_FILE" \
    "\*\*Mode:\*\*.*greenfield\|\*\*Mode:\*\*.*brownfield" \
    "Mode marker follows specified format (**Mode:** greenfield|brownfield)"

################################################################################
# TEST 3.9: Context marker appears before Skill() invocation
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 3.9: Context Marker Timing (Before Skill Invocation)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check that both context marker and Skill() invocation exist
assert_file_contains "$COMMAND_FILE" \
    "Project Mode Context" \
    "Context marker exists in ideate.md"

assert_file_contains "$COMMAND_FILE" \
    "Skill(" \
    "Skill invocation exists in ideate.md"

# Extract line numbers (approximate check)
echo -e "${YELLOW}Note:${NC} Verifying context marker appears before Skill() invocation"
echo "This requires manual code review (context-passing-order)"

################################################################################
# TEST 3.10: No hardcoded next-actions in command
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 3.10: Mode-Based Decision in Skill (Not Hardcoded in Command)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# The command should NOT hardcode next-actions; it should be in the skill
assert_file_not_contains "$COMMAND_FILE" \
    "next-action.*greenfield\|next-action.*brownfield" \
    "Command does not hardcode next-actions (decision deferred to skill Phase 6.6)"

echo -e "${YELLOW}Note:${NC} Next-action decisions should be in skill Phase 6.6, not in command"

################################################################################
# SUMMARY
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "$TEST_NAME"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Tests run: $TESTS_RUN"
echo -e "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests failed: ${RED}$TESTS_FAILED${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ "$TESTS_FAILED" -gt 0 ]; then
    exit 1
fi

exit 0
