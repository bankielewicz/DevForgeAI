#!/bin/bash

################################################################################
# TEST SUITE: AC#3 - Phase 7 Completion Display
# Story: STORY-164
# Description: Verify Phase 7 completion display in SKILL.md with correct format
#
# Acceptance Criteria:
# Claude must display confirmation before returning final results, showing:
# - Unicode box-drawing characters (━) for visual distinction
# - "Phase 7/9: Result Interpretation - Mandatory Steps Completed" header
# - dev-result-interpreter invocation with line numbers
#
# Test Status: FAILING (Red Phase) - self-check display section does not exist
################################################################################

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SKILL_FILE=".claude/skills/devforgeai-development/SKILL.md"
TEST_NAME="AC#3: Phase 7 Completion Display"

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

echo -e "${BLUE}Test Group 1: Phase 7 Completion Display Section${NC}"
echo ""

assert_pattern_exists "$SKILL_FILE" "### Phase 10 Completion Display\|### Phase 7 Completion Display\|### Final Result Summary" \
    "Phase 10 (Result Interpretation) Completion Display section header exists"

assert_pattern_exists "$SKILL_FILE" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" \
    "Unicode box-drawing characters (━) used in Phase 7 display"

echo ""
echo -e "${BLUE}Test Group 2: Phase 7 Header Content${NC}"
echo ""

assert_pattern_exists "$SKILL_FILE" "Phase.*10/10\|Phase.*7.*9\|Result.*Interpretation\|dev-result-interpreter" \
    "Header references Phase 10 or Result Interpretation phase"

assert_pattern_exists "$SKILL_FILE" "Mandatory Steps Completed" \
    "Header contains 'Mandatory Steps Completed' message"

echo ""
echo -e "${BLUE}Test Group 3: dev-result-interpreter Invocation Reference${NC}"
echo ""

assert_pattern_exists "$SKILL_FILE" "dev-result-interpreter" \
    "dev-result-interpreter invocation mentioned in Phase 7 display"

assert_pattern_exists "$SKILL_FILE" "dev-result-interpreter.*lines\|lines.*dev-result-interpreter" \
    "dev-result-interpreter reference includes line number reference"

echo ""
echo -e "${BLUE}Test Group 4: Checkmark and Completion Message${NC}"
echo ""

assert_pattern_exists "$SKILL_FILE" "✓" \
    "Checkmark symbols (✓) present in Phase 7 display"

assert_pattern_exists "$SKILL_FILE" "All Phase.*mandatory steps completed\|All.*steps completed" \
    "Completion message confirms all mandatory steps completed"

assert_pattern_exists "$SKILL_FILE" "Returning.*results\|Final.*results\|Development complete" \
    "Message indicates returning final results or completing workflow"

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}TEST SUMMARY: AC#3${NC}"
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
    echo "Reason:   Phase 7 Completion Display section not yet added to SKILL.md"
    echo ""
    exit 1
else
    echo -e "${GREEN}STATUS: PASSING ✓${NC}"
    echo ""
    echo "All assertions passed. AC#3 requirements satisfied."
    echo ""
    exit 0
fi
