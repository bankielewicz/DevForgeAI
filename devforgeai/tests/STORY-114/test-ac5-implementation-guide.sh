#!/bin/bash
################################################################################
# TEST SUITE: AC#5 - Implementation Guide Enhancement
# Story: STORY-114
# Description: Validates parallel-orchestration-guide.md exists with tutorials
#
# Acceptance Criteria:
# - File exists at docs/guides/parallel-orchestration-guide.md
# - Introduction section present
# - Step-by-step tutorials for all 3 patterns
# - Troubleshooting section present
# - Anti-patterns documented
#
# Test Status: FAILING (Red Phase)
################################################################################

set -uo pipefail

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET_FILE="$PROJECT_ROOT/docs/guides/parallel-orchestration-guide.md"
TEST_NAME="AC#5: Implementation Guide"

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

echo -e "${BLUE}Test Group 1: File Existence${NC}"
echo "----------------------------------------"

# Test 1.1: Implementation guide file exists
assert_file_exists "$TARGET_FILE" "Implementation guide file exists"

echo ""
echo -e "${BLUE}Test Group 2: Introduction Section${NC}"
echo "----------------------------------------"

# Test 2.1: Introduction section present
assert_pattern_in_file "$TARGET_FILE" "Introduction\|## Overview\|# Parallel" \
    "Introduction/Overview section present"

echo ""
echo -e "${BLUE}Test Group 3: Pattern Tutorials${NC}"
echo "----------------------------------------"

# Test 3.1: Pattern 1 tutorial - Parallel Subagents
assert_pattern_in_file "$TARGET_FILE" "Pattern.*1\|Parallel.*Subagent\|## Subagent" \
    "Pattern 1 (Parallel Subagents) tutorial present"

# Test 3.2: Pattern 2 tutorial - Background Tasks
assert_pattern_in_file "$TARGET_FILE" "Pattern.*2\|Background.*Task\|## Background" \
    "Pattern 2 (Background Tasks) tutorial present"

# Test 3.3: Pattern 3 tutorial - Parallel Tools
assert_pattern_in_file "$TARGET_FILE" "Pattern.*3\|Parallel.*Tool\|## Tool" \
    "Pattern 3 (Parallel Tools) tutorial present"

echo ""
echo -e "${BLUE}Test Group 4: Best Practices${NC}"
echo "----------------------------------------"

# Test 4.1: Anti-patterns/Don'ts section
assert_pattern_in_file "$TARGET_FILE" "anti-pattern\|don't\|avoid\|forbidden" \
    "Anti-patterns section present"

# Test 4.2: Best practices/Do's section
assert_pattern_in_file "$TARGET_FILE" "best.*practice\|do\|recommend" \
    "Best practices section present"

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
RESULTS_FILE="$PROJECT_ROOT/devforgeai/tests/STORY-114/test-ac5-results.json"
cat > "$RESULTS_FILE" << EOF
{
  "test_name": "AC#5: Implementation Guide",
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
