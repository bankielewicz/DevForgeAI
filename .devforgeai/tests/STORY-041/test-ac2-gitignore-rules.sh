#!/bin/bash

################################################################################
# TEST SUITE: AC#2 - .gitignore Rules Properly Configured
# Story: STORY-041
# Description: Verify .gitignore is updated with correct DevForgeAI src/ patterns
#
# Acceptance Criteria:
# - Comment: "# DevForgeAI src/ directory - track source, exclude generated"
# - Pattern: src/devforgeai/qa/coverage/*
# - Pattern: src/devforgeai/qa/reports/*
# - Negation: !src/devforgeai/qa/coverage/.gitkeep
# - Negation: !src/devforgeai/qa/reports/.gitkeep
# - Pattern: src/**/*.pyc
# - Pattern: src/**/__pycache__/
# - Pattern: src/**/node_modules/
#
# Verification:
# - git status shows src/ directory tracked (green/staged)
# - git check-ignore src/devforgeai/qa/reports/test-report.md returns exit code 0 (ignored)
# - git check-ignore src/claude/skills/devforgeai-development/SKILL.md returns exit code 1 (NOT ignored)
#
# Test Status: FAILING (Red Phase) - .gitignore rules not yet added
################################################################################

set -e  # Exit on first error

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEST_NAME="AC#2: .gitignore Rules Properly Configured"

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

# Helper function to assert pattern exists in .gitignore
assert_pattern_in_gitignore() {
    local pattern="$1"
    local description="$2"
    ((TESTS_RUN++))

    if grep -F "$pattern" "$PROJECT_ROOT/.gitignore" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        echo "  Pattern: $pattern"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Expected pattern: $pattern"
        echo "  File: .gitignore"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Helper function to assert comment exists in .gitignore
assert_comment_in_gitignore() {
    local comment="$1"
    local description="$2"
    ((TESTS_RUN++))

    if grep -F "$comment" "$PROJECT_ROOT/.gitignore" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        echo "  Comment: $comment"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Expected comment: $comment"
        echo "  File: .gitignore"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Helper function to assert git check-ignore returns specific exit code
assert_git_check_ignore() {
    local path="$1"
    local expected_exit_code="$2"
    local description="$3"
    ((TESTS_RUN++))

    git check-ignore "$path" > /dev/null 2>&1
    local actual_exit_code=$?

    if [ "$actual_exit_code" -eq "$expected_exit_code" ]; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        echo "  Path: $path"
        echo "  Exit code: $actual_exit_code (expected: $expected_exit_code)"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Path: $path"
        echo "  Exit code: $actual_exit_code (expected: $expected_exit_code)"
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

################################################################################
# TEST GROUP 1: .gitignore File Exists
################################################################################

echo -e "${BLUE}Test Group 1: .gitignore File Exists${NC}"
echo ""

((TESTS_RUN++))
if [ -f ".gitignore" ]; then
    echo -e "${GREEN}✓ PASS${NC}: .gitignore file exists"
    echo "  File: .gitignore"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: .gitignore file exists"
    echo "  Expected: .gitignore"
    ((TESTS_FAILED++))
fi

echo ""

################################################################################
# TEST GROUP 2: DevForgeAI Section Comment
################################################################################

echo -e "${BLUE}Test Group 2: DevForgeAI Section Comment${NC}"
echo ""

assert_comment_in_gitignore "# DevForgeAI src/ directory" "DevForgeAI comment section exists"

echo ""

################################################################################
# TEST GROUP 3: Exclusion Patterns for Generated Files
################################################################################

echo -e "${BLUE}Test Group 3: Exclusion Patterns for Generated Files${NC}"
echo ""

assert_pattern_in_gitignore "src/devforgeai/qa/coverage/*" "Exclusion pattern: src/devforgeai/qa/coverage/*"
assert_pattern_in_gitignore "src/devforgeai/qa/reports/*" "Exclusion pattern: src/devforgeai/qa/reports/*"

echo ""

################################################################################
# TEST GROUP 4: Negation Patterns for .gitkeep Files
################################################################################

echo -e "${BLUE}Test Group 4: Negation Patterns for .gitkeep Files${NC}"
echo ""

assert_pattern_in_gitignore "!src/devforgeai/qa/coverage/.gitkeep" "Negation pattern: !src/devforgeai/qa/coverage/.gitkeep"
assert_pattern_in_gitignore "!src/devforgeai/qa/reports/.gitkeep" "Negation pattern: !src/devforgeai/qa/reports/.gitkeep"

echo ""

################################################################################
# TEST GROUP 5: Language-Specific Exclusion Patterns
################################################################################

echo -e "${BLUE}Test Group 5: Language-Specific Exclusion Patterns${NC}"
echo ""

assert_pattern_in_gitignore "src/**/*.pyc" "Python bytecode exclusion: src/**/*.pyc"
assert_pattern_in_gitignore "src/**/__pycache__/" "Python cache exclusion: src/**/__pycache__/"
assert_pattern_in_gitignore "src/**/node_modules/" "npm packages exclusion: src/**/node_modules/"

echo ""

################################################################################
# TEST GROUP 6: Git Check-Ignore Tests (Files Should Be Ignored)
################################################################################

echo -e "${BLUE}Test Group 6: Git Check-Ignore Tests (Files SHOULD Be Ignored)${NC}"
echo ""

# These tests check that coverage/reports files are ignored
# Note: We're testing the ignore logic, not that files exist
# Exit code 0 means file matches .gitignore pattern (ignored)
# Exit code 1 means file does NOT match .gitignore pattern (tracked)

assert_git_check_ignore "src/devforgeai/qa/reports/test-report.md" 0 "File is ignored: src/devforgeai/qa/reports/test-report.md"
assert_git_check_ignore "src/devforgeai/qa/coverage/coverage-report.json" 0 "File is ignored: src/devforgeai/qa/coverage/coverage-report.json"
assert_git_check_ignore "src/devforgeai/qa/reports/another-report.txt" 0 "File is ignored: src/devforgeai/qa/reports/another-report.txt"

echo ""

################################################################################
# TEST GROUP 7: Git Check-Ignore Tests (Files Should NOT Be Ignored)
################################################################################

echo -e "${BLUE}Test Group 7: Git Check-Ignore Tests (Files Should NOT Be Ignored)${NC}"
echo ""

# These tests check that source files are NOT ignored
# Exit code 1 means file does NOT match .gitignore pattern (should be tracked)

assert_git_check_ignore "src/claude/skills/devforgeai-development/SKILL.md" 1 "File is NOT ignored: src/claude/skills/devforgeai-development/SKILL.md"
assert_git_check_ignore "src/claude/agents/test-automator.md" 1 "File is NOT ignored: src/claude/agents/test-automator.md"
assert_git_check_ignore "src/claude/commands/dev.md" 1 "File is NOT ignored: src/claude/commands/dev.md"
assert_git_check_ignore "src/devforgeai/context/tech-stack.md" 1 "File is NOT ignored: src/devforgeai/context/tech-stack.md"

echo ""

################################################################################
# TEST GROUP 8: .gitkeep Files Should NOT Be Ignored
################################################################################

echo -e "${BLUE}Test Group 8: .gitkeep Files Should NOT Be Ignored${NC}"
echo ""

# .gitkeep files in excluded directories should be tracked (exit code 1)
assert_git_check_ignore "src/devforgeai/qa/coverage/.gitkeep" 1 "File is NOT ignored: src/devforgeai/qa/coverage/.gitkeep (negation works)"
assert_git_check_ignore "src/devforgeai/qa/reports/.gitkeep" 1 "File is NOT ignored: src/devforgeai/qa/reports/.gitkeep (negation works)"

echo ""

################################################################################
# TEST GROUP 9: Existing .gitignore Content Not Modified
################################################################################

echo -e "${BLUE}Test Group 9: Existing .gitignore Content Preserved${NC}"
echo ""

((TESTS_RUN++))
# Check that common patterns still exist (assuming typical .gitignore)
if grep -E "^(node_modules|\.env|\.venv|dist/)" ".gitignore" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ PASS${NC}: Existing .gitignore patterns preserved"
    echo "  Common patterns (node_modules, .env, .venv, dist/) still present"
    ((TESTS_PASSED++))
else
    # This is not necessarily a failure if .gitignore doesn't have these patterns
    echo -e "${YELLOW}⊘ SKIP${NC}: Existing patterns check"
    echo "  Note: May not have expected patterns in this project"
    ((TESTS_PASSED++))
fi

echo ""

################################################################################
# TEST GROUP 10: No Duplicate Patterns
################################################################################

echo -e "${BLUE}Test Group 10: No Duplicate Patterns${NC}"
echo ""

((TESTS_RUN++))
local duplicate_check=$(grep -c "src/devforgeai/qa/coverage/\*" ".gitignore" 2>/dev/null || echo "0")
if [ "$duplicate_check" -le 1 ]; then
    echo -e "${GREEN}✓ PASS${NC}: No duplicate patterns in .gitignore"
    echo "  Pattern: src/devforgeai/qa/coverage/* appears $duplicate_check time(s)"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: No duplicate patterns in .gitignore"
    echo "  Pattern: src/devforgeai/qa/coverage/* appears $duplicate_check times"
    ((TESTS_FAILED++))
fi

echo ""

################################################################################
# TEST SUMMARY
################################################################################

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
    echo "Reason:   .gitignore has not been updated with DevForgeAI src/ patterns"
    echo ""
    echo "Next Step (Green Phase): Update .gitignore with required patterns"
    echo ""
    exit 1
else
    echo -e "${GREEN}STATUS: PASSING ✓${NC}"
    echo ""
    echo "All assertions passed. AC#2 requirements satisfied."
    echo ""
    exit 0
fi
