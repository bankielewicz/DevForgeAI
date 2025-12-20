#!/bin/bash
################################################################################
# TEST SUITE: AC#1 - Architecture Documentation Updates
# Story: STORY-114
# Description: Validates architecture-constraints.md has parallel execution rules
#
# Acceptance Criteria:
# - Parallel Execution Rules section exists
# - Task count limits documented (4-6 recommended, 10 max)
# - Dependency rules documented
# - Fallback/recovery rules documented
#
# Test Status: FAILING (Red Phase)
################################################################################

set -uo pipefail

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET_FILE="$PROJECT_ROOT/devforgeai/specs/context/architecture-constraints.md"
TEST_NAME="AC#1: Architecture Constraints Parallel Section"

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

################################################################################
# Test Suite
################################################################################

echo ""
echo "========================================"
echo "  $TEST_NAME"
echo "  Story: STORY-114"
echo "========================================"
echo ""

echo -e "${BLUE}Test Group 1: Parallel Execution Rules Section${NC}"
echo "----------------------------------------"

# Test 1.1: Parallel Execution Rules section exists
assert_pattern_in_file "$TARGET_FILE" "Parallel Execution Rules" \
    "Parallel Execution Rules section exists"

# Test 1.2: Section is marked as LOCKED
assert_pattern_in_file "$TARGET_FILE" "Parallel Execution Rules.*LOCKED\|LOCKED.*Parallel" \
    "Parallel Execution Rules section is LOCKED"

echo ""
echo -e "${BLUE}Test Group 2: Task Count Limits${NC}"
echo "----------------------------------------"

# Test 2.1: Recommended task count documented (4-6)
assert_pattern_in_file "$TARGET_FILE" "4-6\|recommended.*4\|5-6" \
    "Recommended task count (4-6) documented"

# Test 2.2: Maximum task count documented (10)
assert_pattern_in_file "$TARGET_FILE" "10.*max\|maximum.*10\|limit.*10" \
    "Maximum task count (10) documented"

echo ""
echo -e "${BLUE}Test Group 3: Dependency Rules${NC}"
echo "----------------------------------------"

# Test 3.1: Dependency rules documented
assert_pattern_in_file "$TARGET_FILE" "independent\|dependency\|dependent" \
    "Dependency rules documented"

# Test 3.2: Sequential fallback mentioned
assert_pattern_in_file "$TARGET_FILE" "sequential\|fallback" \
    "Sequential fallback rule documented"

echo ""
echo -e "${BLUE}Test Group 4: Recovery/Failure Rules${NC}"
echo "----------------------------------------"

# Test 4.1: Failure recovery documented
assert_pattern_in_file "$TARGET_FILE" "failure\|recovery\|partial" \
    "Failure recovery rules documented"

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
RESULTS_FILE="$PROJECT_ROOT/devforgeai/tests/STORY-114/test-ac1-results.json"
cat > "$RESULTS_FILE" << EOF
{
  "test_name": "AC#1: Architecture Constraints Parallel Section",
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
