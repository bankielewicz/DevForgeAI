#!/bin/bash
################################################################################
# TEST SUITE: AC#2 - Quick Reference Card
# Story: STORY-114
# Description: Validates parallel-patterns-quick-reference.md exists with patterns
#
# Acceptance Criteria:
# - File exists at docs/guides/parallel-patterns-quick-reference.md
# - 3 parallel patterns documented (Subagents, Background, Parallel Tools)
# - Task count guidelines present
# - Code examples present
# - Troubleshooting section present
#
# Test Status: FAILING (Red Phase)
################################################################################

set -uo pipefail

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET_FILE="$PROJECT_ROOT/docs/guides/parallel-patterns-quick-reference.md"
TEST_NAME="AC#2: Quick Reference Card"

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

    if grep -qi "$pattern" "$file_path"; then
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

assert_pattern_count() {
    local file_path="$1"
    local pattern="$2"
    local min_count="$3"
    local description="$4"
    ((TESTS_RUN++))

    if [ ! -f "$file_path" ]; then
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  File not found: $file_path"
        ((TESTS_FAILED++))
        return 1
    fi

    local count=$(grep -ci "$pattern" "$file_path" || echo 0)
    if [ "$count" -ge "$min_count" ]; then
        echo -e "${GREEN}✓ PASS${NC}: $description (found $count)"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Expected at least $min_count, found $count"
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
echo "  Story: STORY-114"
echo "========================================"
echo ""

echo -e "${BLUE}Test Group 1: File Existence${NC}"
echo "----------------------------------------"

# Test 1.1: Quick reference file exists
assert_file_exists "$TARGET_FILE" "Quick reference file exists at target location"

echo ""
echo -e "${BLUE}Test Group 2: Pattern Documentation${NC}"
echo "----------------------------------------"

# Test 2.1: Pattern 1 - Parallel Subagents
assert_pattern_in_file "$TARGET_FILE" "Pattern.*1\|Parallel.*Subagent\|Task(" \
    "Pattern 1 (Parallel Subagents) documented"

# Test 2.2: Pattern 2 - Background Tasks
assert_pattern_in_file "$TARGET_FILE" "Pattern.*2\|Background.*Task\|run_in_background" \
    "Pattern 2 (Background Tasks) documented"

# Test 2.3: Pattern 3 - Parallel Tool Calling
assert_pattern_in_file "$TARGET_FILE" "Pattern.*3\|Parallel.*Tool\|Read\|Grep" \
    "Pattern 3 (Parallel Tool Calling) documented"

echo ""
echo -e "${BLUE}Test Group 3: Task Count Guidelines${NC}"
echo "----------------------------------------"

# Test 3.1: Task count guidelines present
assert_pattern_in_file "$TARGET_FILE" "4-6\|5-6\|10.*max\|maximum" \
    "Task count guidelines documented"

echo ""
echo -e "${BLUE}Test Group 4: Code Examples${NC}"
echo "----------------------------------------"

# Test 4.1: At least 2 Task() examples
assert_pattern_count "$TARGET_FILE" "Task(" 2 \
    "At least 2 Task() code examples present"

# Test 4.2: At least 1 Bash example
assert_pattern_count "$TARGET_FILE" "Bash(" 1 \
    "At least 1 Bash() code example present"

echo ""
echo -e "${BLUE}Test Group 5: Troubleshooting${NC}"
echo "----------------------------------------"

# Test 5.1: Troubleshooting section present
assert_pattern_in_file "$TARGET_FILE" "troubleshoot" \
    "Troubleshooting section present"

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

# Write JSON results
RESULTS_FILE="$PROJECT_ROOT/devforgeai/tests/STORY-114/test-ac2-results.json"
cat > "$RESULTS_FILE" << EOF
{
  "test_name": "AC#2: Quick Reference Card",
  "story_id": "STORY-114",
  "total_tests": $TESTS_RUN,
  "passed": $TESTS_PASSED,
  "failed": $TESTS_FAILED,
  "exit_code": $( [ $TESTS_FAILED -gt 0 ] && echo 1 || echo 0 ),
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "${RED}RESULT: FAILED${NC}"
    exit 1
else
    echo -e "${GREEN}RESULT: PASSED${NC}"
    exit 0
fi
