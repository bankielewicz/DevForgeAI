#!/bin/bash

################################################################################
# TEST SUITE: AC#1 - Phase 2 Completion Display
# Story: STORY-164
# Description: Verify Phase 2 completion display in SKILL.md with correct format
#
# Acceptance Criteria:
# Claude must display confirmation before marking Phase 2 complete showing:
# - Unicode box-drawing characters (━) for visual distinction
# - "Phase 2/9: Implementation - Mandatory Steps Completed" header
# - backend-architect invocation with line numbers
# - context-validator invocation with line numbers
#
# Test Status: FAILING (Red Phase) - self-check display section does not exist
################################################################################

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SKILL_FILE=".claude/skills/devforgeai-development/SKILL.md"
TEST_NAME="AC#1: Phase 2 Completion Display"

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

assert_pattern_exists() {
    local file_path="$1"
    local pattern="$2"
    local description="$3"
    ((TESTS_RUN++))

    if grep -q "$pattern" "$file_path" 2>/dev/null; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        ((TESTS_FAILED++))
        return 1
    fi
}

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}TEST SUITE: $TEST_NAME${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

cd "$PROJECT_ROOT" || exit 1

echo -e "${BLUE}Test Group 1: Phase 2 Completion Display Section${NC}"
echo ""

assert_pattern_exists "$SKILL_FILE" "### Phase 03 Completion Display\|### Phase 2 Completion Display" \
    "Phase 03 (Implementation) Completion Display section header exists"

assert_pattern_exists "$SKILL_FILE" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" \
    "Unicode box-drawing characters (━) used for visual distinction"

echo ""
echo -e "${BLUE}Test Group 2: Phase 2 Header Content${NC}"
echo ""

assert_pattern_exists "$SKILL_FILE" "Phase 03/10\|Phase 2/10" \
    "Header contains Phase 03/10 or Phase 2/10 reference"

assert_pattern_exists "$SKILL_FILE" "Implementation" \
    "Header contains 'Implementation' phase name"

assert_pattern_exists "$SKILL_FILE" "Mandatory Steps Completed" \
    "Header contains 'Mandatory Steps Completed' message"

echo ""
echo -e "${BLUE}Test Group 3: backend-architect Invocation Reference${NC}"
echo ""

assert_pattern_exists "$SKILL_FILE" "backend-architect" \
    "backend-architect invocation mentioned in Phase 2 display"

assert_pattern_exists "$SKILL_FILE" "backend-architect.*lines\|lines.*backend-architect" \
    "backend-architect reference includes line number reference"

echo ""
echo -e "${BLUE}Test Group 4: context-validator Invocation Reference${NC}"
echo ""

assert_pattern_exists "$SKILL_FILE" "context-validator" \
    "context-validator invocation mentioned in Phase 2 display"

assert_pattern_exists "$SKILL_FILE" "context-validator.*lines\|lines.*context-validator" \
    "context-validator reference includes line number reference"

echo ""
echo -e "${BLUE}Test Group 5: Checkmark and Completion Message${NC}"
echo ""

assert_pattern_exists "$SKILL_FILE" "✓" \
    "Checkmark symbols (✓) indicate completed steps"

assert_pattern_exists "$SKILL_FILE" "All Phase 03 mandatory steps completed\|All Phase 2 mandatory steps completed" \
    "Completion message confirms all Phase 03 steps completed"

assert_pattern_exists "$SKILL_FILE" "Proceeding to Phase 04\|Proceeding to Phase 3" \
    "Message indicates proceeding to next phase"

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}TEST SUMMARY: AC#1${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Tests Run:    $TESTS_RUN"
echo "Tests Passed: $TESTS_PASSED"
echo "Tests Failed: $TESTS_FAILED"
echo ""

if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "${RED}STATUS: FAILING (Red Phase) ✗${NC}"
    echo ""
    echo "Expected: All tests should be FAILING initially (TDD Red phase)"
    echo "Reason:   Phase 2 Completion Display section not yet added to SKILL.md"
    echo ""
    exit 1
else
    echo -e "${GREEN}STATUS: PASSING ✓${NC}"
    echo ""
    echo "All assertions passed. AC#1 requirements satisfied."
    echo ""
    exit 0
fi
