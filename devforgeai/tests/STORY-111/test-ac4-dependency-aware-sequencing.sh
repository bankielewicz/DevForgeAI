#!/bin/bash
################################################################################
# TEST SUITE: AC#4 - Dependency-Aware Sequencing
# Story: STORY-111
# Description: Validates dependency detection and appropriate sequencing to
#              prevent parallelizing dependent tasks.
#
# Acceptance Criteria:
# Given some tasks depend on others,
# When the skill plans parallel execution,
# Then dependent tasks wait for prerequisites (no parallel calls with dependencies).
#
# Test Status: FAILING (Red Phase) - expected to fail until implementation complete
################################################################################

set -e

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEST_NAME="AC#4: Dependency-Aware Sequencing"

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
DEPENDENCY_GRAPH_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-orchestration/references/dependency-graph.md"
FEATURE_ANALYZER_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-orchestration/references/feature-analyzer.md"

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

################################################################################
# Test Cases
################################################################################

echo ""
echo "=============================================================================="
echo "  $TEST_NAME"
echo "=============================================================================="
echo ""

# Test 1: dependency-graph.md reference file exists
echo -e "${BLUE}Test 1: Reference file existence${NC}"
assert_file_exists "$DEPENDENCY_GRAPH_FILE" \
    "dependency-graph.md reference file exists"

# Test 2: Verify dependency detection algorithm documented
echo -e "\n${BLUE}Test 2: Detection algorithm${NC}"
assert_pattern_in_file "$DEPENDENCY_GRAPH_FILE" \
    "detect\|Detect\|algorithm\|Algorithm" \
    "Documents dependency detection algorithm"

# Test 3: Verify sequential execution for dependent tasks
echo -e "\n${BLUE}Test 3: Sequential for dependencies${NC}"
assert_pattern_in_file "$DEPENDENCY_GRAPH_FILE" \
    "sequential\|Sequential\|wait\|Wait" \
    "Documents sequential execution for dependent tasks"

# Test 4: Verify parallel execution for independent tasks
echo -e "\n${BLUE}Test 4: Parallel for independent${NC}"
assert_pattern_in_file "$DEPENDENCY_GRAPH_FILE" \
    "parallel\|Parallel\|independent\|Independent\|concurrent" \
    "Documents parallel execution for independent tasks"

# Test 5: Verify dependency example documented
echo -e "\n${BLUE}Test 5: Example documented${NC}"
assert_pattern_in_file "$DEPENDENCY_GRAPH_FILE" \
    "depends on\|depends_on\|prerequisite\|Prerequisite" \
    "Documents dependency example (e.g., 'Feature 2 depends on Feature 1')"

# Test 6: Verify transitive dependency handling
echo -e "\n${BLUE}Test 6: Transitive handling${NC}"
assert_pattern_in_file "$DEPENDENCY_GRAPH_FILE" \
    "transitive\|Transitive\|chain\|Chain" \
    "Documents transitive dependency handling (A→B→C)"

# Test 7: Verify circular dependency detection
echo -e "\n${BLUE}Test 7: Circular detection${NC}"
assert_pattern_in_file "$DEPENDENCY_GRAPH_FILE" \
    "circular\|Circular\|cycle\|Cycle" \
    "Documents circular dependency detection and HALT behavior"

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
