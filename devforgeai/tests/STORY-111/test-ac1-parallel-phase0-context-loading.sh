#!/bin/bash
################################################################################
# TEST SUITE: AC#1 - Parallel Phase 0 Context Loading
# Story: STORY-111
# Description: Validates parallel context file loading pattern with 6 Read calls
#              in a single message for implicit parallel execution.
#
# Acceptance Criteria:
# Given the orchestration skill starts Phase 0,
# When it needs to load 6 context files,
# Then all 6 files are read in parallel using a single message with 6 Read tool calls.
#
# Test Status: FAILING (Red Phase) - expected to fail until implementation complete
################################################################################

set -e

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEST_NAME="AC#1: Parallel Phase 0 Context Loading"

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
CONTEXT_LOADER_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-orchestration/references/context-loader.md"
SKILL_MD_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-orchestration/SKILL.md"

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

# Test 1: context-loader.md reference file exists
echo -e "${BLUE}Test 1: Reference file existence${NC}"
assert_file_exists "$CONTEXT_LOADER_FILE" \
    "context-loader.md reference file exists"

# Test 2: Verify 6 parallel Read calls documented
echo -e "\n${BLUE}Test 2: Parallel Read pattern documented${NC}"
assert_count_in_file "$CONTEXT_LOADER_FILE" \
    'Read(file_path=' \
    6 \
    "Documents 6 Read calls for context files"

# Test 3: Verify single-message pattern documented
echo -e "\n${BLUE}Test 3: Single message pattern${NC}"
assert_pattern_in_file "$CONTEXT_LOADER_FILE" \
    "single message" \
    "Documents single message pattern for implicit parallelization"

# Test 4: Verify SKILL.md references context-loader.md
echo -e "\n${BLUE}Test 4: SKILL.md integration${NC}"
assert_pattern_in_file "$SKILL_MD_FILE" \
    "context-loader.md" \
    "SKILL.md references context-loader.md"

# Test 5: Verify all 6 context files mentioned
echo -e "\n${BLUE}Test 5: All context files included${NC}"
CONTEXT_FILES=(
    "architecture-constraints.md"
    "tech-stack.md"
    "source-tree.md"
    "dependencies.md"
    "coding-standards.md"
    "anti-patterns.md"
)

all_files_found=true
for file in "${CONTEXT_FILES[@]}"; do
    if ! grep -q "$file" "$CONTEXT_LOADER_FILE" 2>/dev/null; then
        all_files_found=false
        break
    fi
done

((TESTS_RUN++))
if [ "$all_files_found" = true ]; then
    echo -e "${GREEN}✓ PASS${NC}: All 6 context files documented in pattern"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Not all 6 context files documented"
    echo "  Expected: ${CONTEXT_FILES[*]}"
    ((TESTS_FAILED++))
fi

# Test 6: Verify error handling documented
echo -e "\n${BLUE}Test 6: Error handling documented${NC}"
assert_pattern_in_file "$CONTEXT_LOADER_FILE" \
    "error\|Error\|partial failure\|min_success_rate" \
    "Error handling for partial failures documented"

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
