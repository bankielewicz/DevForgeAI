#!/bin/bash

################################################################################
# TEST SUITE: AC#2 - Greenfield Mode Detection
# Story: STORY-134 (Smart Greenfield/Brownfield Detection)
# Description: Verify /ideate command detects greenfield mode when fewer than 6
#              context files are present, and passes 'mode: greenfield' to skill
#
# Acceptance Criteria:
# - Given: Fewer than 6 context files present (0-5 files)
# - When: /ideate command executes Phase 1 (argument validation)
# - Then: Command detects greenfield mode and passes `mode: greenfield` to skill
#
# Test Scenarios:
# 1. No context files (0/6)
# 2. One context file (1/6)
# 3. Partial context files (3/6)
# 4. Almost complete (5/6)
#
# Test Status: FAILING (Red Phase) - Detection logic not yet implemented
################################################################################

set +e  # Do NOT exit on error (we handle failures in test assertions)

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEST_NAME="AC#2: Greenfield Mode Detection"
COMMAND_FILE="${PROJECT_ROOT}/.claude/commands/ideate.md"
CONTEXT_DIR="${PROJECT_ROOT}/devforgeai/specs/context"
FIXTURE_DIR="/tmp/greenfield-test-fixture"

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

# Helper function: Assert condition
assert_true() {
    local condition="$1"
    local description="$2"
    ((TESTS_RUN++))

    if eval "$condition"; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Helper function: Assert file contains text
assert_file_contains() {
    local file="$1"
    local search_text="$2"
    local description="$3"
    ((TESTS_RUN++))

    if [ ! -f "$file" ]; then
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  File not found: $file"
        ((TESTS_FAILED++))
        return 1
    fi

    if grep -q "$search_text" "$file"; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        echo "  Found: $search_text"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Not found in: $file"
        echo "  Search text: $search_text"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Helper function: Count files in directory
count_files() {
    local dir="$1"
    local count=$(find "$dir" -maxdepth 1 -name "*.md" -type f 2>/dev/null | wc -l)
    echo "$count"
}

################################################################################
# TEST 2.1: Mode determination logic (< 6 files = greenfield)
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 2.1: Mode Determination Logic"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

assert_file_contains "$COMMAND_FILE" \
    "< 6.*greenfield" \
    "ideate.md contains logic: fewer than 6 context files = greenfield"

assert_file_contains "$COMMAND_FILE" \
    "mode.*greenfield" \
    "ideate.md contains 'mode: greenfield' or similar marker"

################################################################################
# TEST 2.2: Context marker indicates greenfield mode
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 2.2: Greenfield Mode Marker"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

assert_file_contains "$COMMAND_FILE" \
    "\*\*Mode:\*\*.*greenfield" \
    "Mode marker shows greenfield when <6 files exist"

################################################################################
# TEST 2.3: Greenfield-specific guidance provided
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 2.3: Greenfield Guidance"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

assert_file_contains "$COMMAND_FILE" \
    "create-context" \
    "ideate.md recommends /create-context for greenfield projects"

################################################################################
# TEST 2.4: File count is displayed
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 2.4: File Count Display"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

assert_file_contains "$COMMAND_FILE" \
    "Context Files Found" \
    "ideate.md displays actual context file count"

################################################################################
# TEST 2.5: Zero context files scenario
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 2.5: Zero Context Files (Fresh Greenfield)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Create a test fixture with zero context files
mkdir -p "$FIXTURE_DIR/zero-context"

# Count files in fixture (should be 0)
zero_count=$(find "$FIXTURE_DIR/zero-context" -maxdepth 1 -name "*.md" -type f 2>/dev/null | wc -l)

if [ "$zero_count" -eq 0 ]; then
    echo -e "${GREEN}✓ PASS${NC}: Fixture with zero context files created"
    ((TESTS_RUN++))
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Fixture setup failed (has $zero_count files, expected 0)"
    ((TESTS_RUN++))
    ((TESTS_FAILED++))
fi

# Test: Zero files should trigger greenfield mode
if [ "$zero_count" -lt 6 ]; then
    echo -e "${GREEN}✓ PASS${NC}: Detection logic: 0 files < 6 = greenfield"
    ((TESTS_RUN++))
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Detection logic failed for zero files"
    ((TESTS_RUN++))
    ((TESTS_FAILED++))
fi

################################################################################
# TEST 2.6: Partial context files (5/6) - almost but not brownfield
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 2.6: Partial Context Files (5/6)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Create a test fixture with 5 context files
mkdir -p "$FIXTURE_DIR/five-context"
touch "$FIXTURE_DIR/five-context/tech-stack.md"
touch "$FIXTURE_DIR/five-context/source-tree.md"
touch "$FIXTURE_DIR/five-context/dependencies.md"
touch "$FIXTURE_DIR/five-context/coding-standards.md"
touch "$FIXTURE_DIR/five-context/architecture-constraints.md"

# Count files in fixture (should be 5)
five_count=$(find "$FIXTURE_DIR/five-context" -maxdepth 1 -name "*.md" -type f 2>/dev/null | wc -l)

if [ "$five_count" -eq 5 ]; then
    echo -e "${GREEN}✓ PASS${NC}: Fixture with 5 context files created"
    ((TESTS_RUN++))
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Fixture setup failed (has $five_count files, expected 5)"
    ((TESTS_RUN++))
    ((TESTS_FAILED++))
fi

# Test: 5 files should trigger greenfield mode (not brownfield)
if [ "$five_count" -lt 6 ]; then
    echo -e "${GREEN}✓ PASS${NC}: Detection logic: 5 files < 6 = greenfield (not brownfield)"
    ((TESTS_RUN++))
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Detection logic failed for 5 files"
    ((TESTS_RUN++))
    ((TESTS_FAILED++))
fi

################################################################################
# TEST 2.7: Consistent results across multiple invocations
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 2.7: Consistency Across Multiple Invocations"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Run detection multiple times on the same fixture
count1=$(find "$FIXTURE_DIR/five-context" -maxdepth 1 -name "*.md" -type f 2>/dev/null | wc -l)
count2=$(find "$FIXTURE_DIR/five-context" -maxdepth 1 -name "*.md" -type f 2>/dev/null | wc -l)
count3=$(find "$FIXTURE_DIR/five-context" -maxdepth 1 -name "*.md" -type f 2>/dev/null | wc -l)

if [ "$count1" -eq "$count2" ] && [ "$count2" -eq "$count3" ]; then
    echo -e "${GREEN}✓ PASS${NC}: Detection produces consistent results across multiple invocations"
    echo "  Invocation 1: $count1 files"
    echo "  Invocation 2: $count2 files"
    echo "  Invocation 3: $count3 files"
    ((TESTS_RUN++))
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Detection results are inconsistent"
    echo "  Invocation 1: $count1 files"
    echo "  Invocation 2: $count2 files"
    echo "  Invocation 3: $count3 files"
    ((TESTS_RUN++))
    ((TESTS_FAILED++))
fi

################################################################################
# CLEANUP
################################################################################
rm -rf "$FIXTURE_DIR"

################################################################################
# SUMMARY
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "$TEST_NAME"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Tests run: $TESTS_RUN"
echo -e "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests failed: ${RED}$TESTS_FAILED${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ "$TESTS_FAILED" -gt 0 ]; then
    exit 1
fi

exit 0
