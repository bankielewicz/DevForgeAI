#!/bin/bash
################################################################################
# TEST SUITE: AC#3 - CLAUDE.md Updates
# Story: STORY-114
# Description: Validates CLAUDE.md has parallel orchestration guidance
#
# Acceptance Criteria:
# - Parallel orchestration section added
# - When to parallelize guidance added
# - References to parallel documentation added
#
# Test Status: FAILING (Red Phase)
################################################################################

set -uo pipefail

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET_FILE="$PROJECT_ROOT/CLAUDE.md"
TEST_NAME="AC#3: CLAUDE.md Parallel Section"

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

echo -e "${BLUE}Test Group 1: Parallel Orchestration Section${NC}"
echo "----------------------------------------"

# Test 1.1: Parallel orchestration section exists
assert_pattern_in_file "$TARGET_FILE" "Parallel Orchestration\|## Parallel" \
    "Parallel Orchestration section exists"

echo ""
echo -e "${BLUE}Test Group 2: Parallel Guidance${NC}"
echo "----------------------------------------"

# Test 2.1: When to parallelize guidance
assert_pattern_in_file "$TARGET_FILE" "independent\|parallelize\|concurrent" \
    "When to parallelize guidance present"

# Test 2.2: Pattern reference (subagents, background, tools)
assert_pattern_in_file "$TARGET_FILE" "Subagent\|Background\|Task(" \
    "Parallel pattern types mentioned"

echo ""
echo -e "${BLUE}Test Group 3: Documentation References${NC}"
echo "----------------------------------------"

# Test 3.1: Reference to quick reference card
assert_pattern_in_file "$TARGET_FILE" "parallel-patterns-quick-reference\|quick.*reference" \
    "Quick reference card referenced"

# Test 3.2: Reference to parallel guide
assert_pattern_in_file "$TARGET_FILE" "parallel-orchestration-guide\|parallel.*guide" \
    "Parallel orchestration guide referenced"

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
RESULTS_FILE="$PROJECT_ROOT/devforgeai/tests/STORY-114/test-ac3-results.json"
cat > "$RESULTS_FILE" << EOF
{
  "test_name": "AC#3: CLAUDE.md Parallel Section",
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
