#!/bin/bash
################################################################################
# TEST SUITE: AC#3 - Configurable Timeouts
# Story: STORY-108
# Description: Validates timeout documentation in parallel-config.md
#
# Acceptance Criteria:
# - Timeout monitoring documented
# - Graceful termination documented (KillShell)
# - Error logging documented
#
# Test Status: FAILING (Red Phase)
################################################################################

set -uo pipefail

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
DOC_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-orchestration/references/parallel-config.md"
TEST_NAME="AC#3: Configurable Timeouts"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

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
        echo "  File not found: $file_path"
        ((TESTS_FAILED++))
        return 1
    fi
}

assert_doc_contains() {
    local pattern="$1"
    local description="$2"
    ((TESTS_RUN++))

    if [ ! -f "$DOC_FILE" ]; then
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Documentation file not found: $DOC_FILE"
        ((TESTS_FAILED++))
        return 1
    fi

    if grep -iE "$pattern" "$DOC_FILE" > /dev/null 2>&1; then
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

################################################################################
# Test Suite
################################################################################

echo ""
echo "========================================"
echo "  $TEST_NAME"
echo "  Story: STORY-108"
echo "========================================"
echo ""

echo -e "${BLUE}Test Group 1: Timeout Documentation${NC}"
echo "----------------------------------------"

# Test 1: Timeout monitoring documented
assert_doc_contains "timeout.*monitor|Timeout.*Handling|timeout_ms" "Timeout monitoring/handling documented"

# Test 2: Graceful termination documented (KillShell or graceful)
assert_doc_contains "KillShell|graceful.*terminat|SIGTERM" "Graceful termination mechanism documented"

# Test 3: Error logging documented
assert_doc_contains "error.*log|log.*timeout|logger\." "Error logging for timeouts documented"

################################################################################
# Summary
################################################################################

echo ""
echo "========================================"
echo "  Test Summary"
echo "========================================"
echo "Tests Run:    $TESTS_RUN"
echo "Tests Passed: $TESTS_PASSED"
echo "Tests Failed: $TESTS_FAILED"
echo ""

if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "${RED}RESULT: FAILED${NC}"
    exit 1
else
    echo -e "${GREEN}RESULT: PASSED${NC}"
    exit 0
fi
