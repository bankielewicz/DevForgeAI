#!/bin/bash
################################################################################
# TEST SUITE: AC#2 - Parallel Feature Analysis
# Story: STORY-111
# Description: Validates parallel feature analysis with multiple Task() calls
#              in a single message for concurrent epic feature decomposition.
#
# Acceptance Criteria:
# Given an epic has 5+ features to analyze,
# When the orchestration skill decomposes features,
# Then 3-5 features are analyzed concurrently using multiple Task() calls in
# a single message.
#
# Test Status: FAILING (Red Phase) - expected to fail until implementation complete
################################################################################

set -e

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEST_NAME="AC#2: Parallel Feature Analysis"

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
EPIC_MANAGEMENT_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-orchestration/references/epic-management.md"
PARALLEL_CONFIG_FILE="$PROJECT_ROOT/devforgeai/config/parallel-orchestration.yaml"

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

assert_count_in_file() {
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

    local count=$(grep -c "$pattern" "$file_path" 2>/dev/null || echo "0")

    if [ "$count" -ge "$min_count" ]; then
        echo -e "${GREEN}✓ PASS${NC}: $description (found $count occurrences)"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Expected at least $min_count occurrences, found $count"
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

# Test 1: feature-analyzer.md reference file exists
echo -e "${BLUE}Test 1: Reference file existence${NC}"
assert_file_exists "$FEATURE_ANALYZER_FILE" \
    "feature-analyzer.md reference file exists"

# Test 2: Verify batching uses max_concurrent_tasks
echo -e "\n${BLUE}Test 2: Batching configuration${NC}"
assert_pattern_in_file "$FEATURE_ANALYZER_FILE" \
    "max_concurrent_tasks" \
    "Documents use of max_concurrent_tasks from config"

# Test 3: Verify Task() pattern documented
echo -e "\n${BLUE}Test 3: Task() tool pattern${NC}"
assert_count_in_file "$FEATURE_ANALYZER_FILE" \
    "Task(" \
    3 \
    "Documents multiple Task() calls for parallel analysis"

# Test 4: Verify examples for different feature counts
echo -e "\n${BLUE}Test 4: Batching examples${NC}"
assert_pattern_in_file "$FEATURE_ANALYZER_FILE" \
    "batch\|Batch" \
    "Documents batching examples for feature analysis"

# Test 5: Verify requirements-analyst delegation
echo -e "\n${BLUE}Test 5: Subagent delegation${NC}"
assert_pattern_in_file "$FEATURE_ANALYZER_FILE" \
    "requirements-analyst" \
    "Documents delegation to requirements-analyst subagent"

# Test 6: Verify epic-management.md references feature-analyzer.md
echo -e "\n${BLUE}Test 6: epic-management.md integration${NC}"
assert_pattern_in_file "$EPIC_MANAGEMENT_FILE" \
    "feature-analyzer.md" \
    "epic-management.md references feature-analyzer.md"

# Test 7: Verify result aggregation documented
echo -e "\n${BLUE}Test 7: Result aggregation${NC}"
assert_pattern_in_file "$FEATURE_ANALYZER_FILE" \
    "aggregat\|Aggregat\|merge\|Merge\|combine\|Combine" \
    "Documents result aggregation from parallel tasks"

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
