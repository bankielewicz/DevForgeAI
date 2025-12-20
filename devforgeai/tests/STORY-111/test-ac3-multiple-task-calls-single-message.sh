#!/bin/bash
################################################################################
# TEST SUITE: AC#3 - Multiple Task() Calls in Single Message
# Story: STORY-111
# Description: Validates that multiple Task() calls are batched in single
#              messages for implicit parallel execution by Claude Code.
#
# Acceptance Criteria:
# Given multiple independent subagent tasks are needed,
# When the skill invokes them,
# Then they are sent in a single message (not sequential messages) for
# implicit parallel execution.
#
# Test Status: FAILING (Red Phase) - expected to fail until implementation complete
################################################################################

set -e

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEST_NAME="AC#3: Multiple Task() Calls in Single Message"

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

# File paths
FEATURE_ANALYZER_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-orchestration/references/feature-analyzer.md"
CONTEXT_LOADER_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-orchestration/references/context-loader.md"

################################################################################
# Helper Functions
################################################################################

assert_file_exists() {
    local file_path="$1"
    local description="$2"
    ((TESTS_RUN++))

    if [ -f "$file_path" ]; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Expected file: $file_path"
        ((TESTS_FAILED++))
        return 1
    fi
}

assert_pattern_in_file() {
    local file_path="$1"
    local pattern="$2"
    local description="$3"
    ((TESTS_RUN++))

    if [ ! -f "$file_path" ]; then
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  File not found: $file_path"
        ((TESTS_FAILED++))
        return 1
    fi

    if grep -q "$pattern" "$file_path"; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Pattern not found: $pattern"
        ((TESTS_FAILED++))
        return 1
    fi
}

assert_pattern_in_either_file() {
    local file1="$1"
    local file2="$2"
    local pattern="$3"
    local description="$4"
    ((TESTS_RUN++))

    local found=false

    if [ -f "$file1" ] && grep -q "$pattern" "$file1" 2>/dev/null; then
        found=true
    fi

    if [ -f "$file2" ] && grep -q "$pattern" "$file2" 2>/dev/null; then
        found=true
    fi

    if [ "$found" = true ]; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Pattern not found in either file: $pattern"
        ((TESTS_FAILED++))
        return 1
    fi
}

################################################################################
# Test Cases
################################################################################

echo ""
echo "=============================================================================="
echo "  $TEST_NAME"
echo "=============================================================================="
echo ""

# Test 1: Verify multiple Task() pattern documented
echo -e "${BLUE}Test 1: Multiple Task() pattern${NC}"
assert_pattern_in_either_file "$FEATURE_ANALYZER_FILE" "$CONTEXT_LOADER_FILE" \
    "Task(" \
    "Documents multiple Task() calls pattern"

# Test 2: Verify single message emphasis
echo -e "\n${BLUE}Test 2: Single message emphasis${NC}"
assert_pattern_in_either_file "$FEATURE_ANALYZER_FILE" "$CONTEXT_LOADER_FILE" \
    "single message" \
    "Emphasizes single message for parallel execution"

# Test 3: Verify anti-pattern (sequential) documented
echo -e "\n${BLUE}Test 3: Anti-pattern documented${NC}"
assert_pattern_in_either_file "$FEATURE_ANALYZER_FILE" "$CONTEXT_LOADER_FILE" \
    "Anti-[Pp]attern\|DO NOT\|sequential.*wait\|avoid" \
    "Documents anti-pattern of sequential Task() with waits"

# Test 4: Verify batching respects max_concurrent_tasks
echo -e "\n${BLUE}Test 4: Respects concurrency limit${NC}"
assert_pattern_in_file "$FEATURE_ANALYZER_FILE" \
    "max_concurrent_tasks" \
    "Documents batching respects max_concurrent_tasks limit"

# Test 5: Verify implicit parallelization explained
echo -e "\n${BLUE}Test 5: Implicit parallelization explained${NC}"
assert_pattern_in_either_file "$FEATURE_ANALYZER_FILE" "$CONTEXT_LOADER_FILE" \
    "implicit\|parallel\|concurrent" \
    "Explains Claude Code implicit parallelization"

################################################################################
# Summary
################################################################################

echo ""
echo "=============================================================================="
echo "  Test Summary: $TEST_NAME"
echo "=============================================================================="
echo ""
echo -e "  Tests Run:    $TESTS_RUN"
echo -e "  Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "  Tests Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [ "$TESTS_FAILED" -eq 0 ]; then
    echo -e "${GREEN}ALL TESTS PASSED${NC}"
    exit 0
else
    echo -e "${RED}SOME TESTS FAILED${NC}"
    exit 1
fi
