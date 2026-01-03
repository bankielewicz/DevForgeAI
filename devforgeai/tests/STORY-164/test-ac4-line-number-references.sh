#!/bin/bash

################################################################################
# TEST SUITE: AC#4 - Line Number References
# Story: STORY-164
# Description: Verify line number reference format in completion displays
#
# Acceptance Criteria:
# Line numbers should reference actual conversation lines where Task/Skill called
# Format should be consistent across all displays (lines XXX-YYY or similar)
#
# Test Status: FAILING (Red Phase) - line number format documentation missing
################################################################################

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SKILL_FILE=".claude/skills/devforgeai-development/SKILL.md"
TEST_NAME="AC#4: Line Number References"

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

echo -e "${BLUE}Test Group 1: Line Number Reference Format Documented${NC}"
echo ""

assert_pattern_exists "$SKILL_FILE" "lines.*XXX.*YYY\|line number.*format\|lines.*reference" \
    "Line number reference format is documented"

assert_pattern_exists "$SKILL_FILE" "XXX-YYY\|XXX.*YYY" \
    "Format example (XXX-YYY) is clearly shown"

echo ""
echo -e "${BLUE}Test Group 2: Line References in Phase Displays${NC}"
echo ""

assert_pattern_exists "$SKILL_FILE" "(lines" \
    "Line references use consistent format with parentheses"

assert_pattern_exists "$SKILL_FILE" "invoked (lines" \
    "Invocation references use 'invoked (lines' format"

echo ""
echo -e "${BLUE}Test Group 3: Consistency of Format${NC}"
echo ""

assert_pattern_exists "$SKILL_FILE" "(lines [0-9]" \
    "Line references use consistent format with numeric values"

echo ""
echo -e "${BLUE}Test Group 4: Documentation of Conversation Lines${NC}"
echo ""

assert_pattern_exists "$SKILL_FILE" "conversation.*line\|actual.*line\|Task.*invoked\|Skill.*invoked" \
    "Documentation explains references point to conversation lines"

echo ""
echo -e "${BLUE}Test Group 5: Phase Sections Found${NC}"
echo ""

assert_pattern_exists "$SKILL_FILE" "Phase 03 Completion Display\|Phase 03.*Completion\|Phase 2 Completion Display\|Phase 2.*Completion" \
    "Phase 03 (Implementation) completion display section exists"

assert_pattern_exists "$SKILL_FILE" "Phase 04 Completion Display\|Phase 04.*Completion\|Phase 3 Completion Display\|Phase 3.*Completion" \
    "Phase 04 (Refactoring) completion display section exists"

assert_pattern_exists "$SKILL_FILE" "Phase 10 Completion Display\|Phase 10.*Completion\|Phase 7 Completion Display\|dev-result-interpreter" \
    "Phase 10 (Result Interpretation) completion display section exists"

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}TEST SUMMARY: AC#4${NC}"
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
    echo "Reason:   Line number reference format not documented in SKILL.md"
    echo ""
    exit 1
else
    echo -e "${GREEN}STATUS: PASSING ✓${NC}"
    echo ""
    echo "All assertions passed. AC#4 requirements satisfied."
    echo ""
    exit 0
fi
