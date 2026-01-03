#!/bin/bash

################################################################################
# TEST SUITE: AC#2 - Phase 3 Completion Display
# Story: STORY-164
# Description: Verify Phase 3 completion display in SKILL.md with correct format
#
# Acceptance Criteria:
# Claude must display confirmation before marking Phase 3 complete showing:
# - Unicode box-drawing characters (━) for visual distinction
# - "Phase 3/9: Refactoring - Mandatory Steps Completed" header
# - refactoring-specialist invocation with line numbers
# - code-reviewer invocation with line numbers
# - Light QA execution with line numbers
#
# Test Status: FAILING (Red Phase) - self-check display section does not exist
################################################################################

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SKILL_FILE=".claude/skills/devforgeai-development/SKILL.md"
TEST_NAME="AC#2: Phase 3 Completion Display"

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

echo -e "${BLUE}Test Group 1: Phase 3 Completion Display Section${NC}"
echo ""

assert_pattern_exists "$SKILL_FILE" "### Phase 04 Completion Display\|### Phase 3 Completion Display" \
    "Phase 04 (Refactoring) Completion Display section header exists"

assert_pattern_exists "$SKILL_FILE" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" \
    "Unicode box-drawing characters (━) used in Phase 3 display"

echo ""
echo -e "${BLUE}Test Group 2: Phase 3 Header Content${NC}"
echo ""

assert_pattern_exists "$SKILL_FILE" "Phase 04/10\|Phase 3/10" \
    "Header contains Phase 04/10 or Phase 3/10 reference"

assert_pattern_exists "$SKILL_FILE" "Refactoring" \
    "Header contains 'Refactoring' phase name"

assert_pattern_exists "$SKILL_FILE" "Mandatory Steps Completed" \
    "Header contains 'Mandatory Steps Completed' message"

echo ""
echo -e "${BLUE}Test Group 3: refactoring-specialist Invocation Reference${NC}"
echo ""

assert_pattern_exists "$SKILL_FILE" "refactoring-specialist" \
    "refactoring-specialist invocation mentioned in Phase 3 display"

assert_pattern_exists "$SKILL_FILE" "refactoring-specialist.*lines\|lines.*refactoring-specialist" \
    "refactoring-specialist reference includes line number reference"

echo ""
echo -e "${BLUE}Test Group 4: code-reviewer Invocation Reference${NC}"
echo ""

assert_pattern_exists "$SKILL_FILE" "code-reviewer" \
    "code-reviewer invocation mentioned in Phase 3 display"

assert_pattern_exists "$SKILL_FILE" "code-reviewer.*lines\|lines.*code-reviewer" \
    "code-reviewer reference includes line number reference"

echo ""
echo -e "${BLUE}Test Group 5: Light QA Execution Reference${NC}"
echo ""

assert_pattern_exists "$SKILL_FILE" "Light QA" \
    "Light QA execution mentioned in Phase 3 display"

assert_pattern_exists "$SKILL_FILE" "Light QA.*lines\|lines.*Light QA" \
    "Light QA reference includes line number reference"

echo ""
echo -e "${BLUE}Test Group 6: Checkmark and Completion Message${NC}"
echo ""

assert_pattern_exists "$SKILL_FILE" "✓" \
    "Checkmark symbols (✓) present in Phase 3 display"

assert_pattern_exists "$SKILL_FILE" "All Phase 04 mandatory steps completed\|All Phase 3 mandatory steps completed" \
    "Completion message confirms all Phase 04 steps completed"

assert_pattern_exists "$SKILL_FILE" "Proceeding to Phase 05\|Proceeding to Phase 4\|Proceeding to next phase" \
    "Message indicates proceeding to next phase after Phase 04"

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}TEST SUMMARY: AC#2${NC}"
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
    echo "Reason:   Phase 3 Completion Display section not yet added to SKILL.md"
    echo ""
    exit 1
else
    echo -e "${GREEN}STATUS: PASSING ✓${NC}"
    echo ""
    echo "All assertions passed. AC#2 requirements satisfied."
    echo ""
    exit 0
fi
