#!/bin/bash

################################################################################
# TEST SUITE: AC#1 - Brownfield Mode Detection
# Story: STORY-134 (Smart Greenfield/Brownfield Detection)
# Description: Verify /ideate command detects brownfield mode when all 6 context
#              files are present, and passes 'mode: brownfield' to skill
#
# Acceptance Criteria:
# - Given: 6 context files present in devforgeai/specs/context/
# - When: /ideate command executes Phase 1 (argument validation)
# - Then: Command detects brownfield mode and passes `mode: brownfield` to skill
#
# Context Files Required:
# 1. devforgeai/specs/context/tech-stack.md
# 2. devforgeai/specs/context/source-tree.md
# 3. devforgeai/specs/context/dependencies.md
# 4. devforgeai/specs/context/coding-standards.md
# 5. devforgeai/specs/context/architecture-constraints.md
# 6. devforgeai/specs/context/anti-patterns.md
#
# Test Status: FAILING (Red Phase) - Detection logic not yet implemented
################################################################################

set +e  # Do NOT exit on error (we handle failures in test assertions)

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEST_NAME="AC#1: Brownfield Mode Detection"
COMMAND_FILE="${PROJECT_ROOT}/.claude/commands/ideate.md"
CONTEXT_DIR="${PROJECT_ROOT}/devforgeai/specs/context"

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

# Helper function: Count files matching pattern
count_context_files() {
    local pattern="$1"
    local count=$(find "$CONTEXT_DIR" -maxdepth 1 -name "$pattern" -type f 2>/dev/null | wc -l)
    echo "$count"
}

################################################################################
# TEST 1.1: All 6 context files are present in fixture/brownfield directory
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 1.1: Context File Existence Check (Brownfield Scenario)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

REQUIRED_FILES=(
    "tech-stack.md"
    "source-tree.md"
    "dependencies.md"
    "coding-standards.md"
    "architecture-constraints.md"
    "anti-patterns.md"
)

for file in "${REQUIRED_FILES[@]}"; do
    assert_true "[ -f '${CONTEXT_DIR}/${file}' ]" \
        "Context file exists: ${file}"
done

################################################################################
# TEST 1.2: Glob check in ideate.md Phase 1
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 1.2: Glob Check in ideate.md Phase 1"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

assert_file_contains "$COMMAND_FILE" \
    "Glob.*pattern.*devforgeai/specs/context" \
    "ideate.md contains Glob check for context files in Phase 1"

################################################################################
# TEST 1.3: Mode determination logic (6 files = brownfield)
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 1.3: Mode Determination Logic"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

assert_file_contains "$COMMAND_FILE" \
    "== 6.*brownfield" \
    "ideate.md contains logic: 6 context files = brownfield"

assert_file_contains "$COMMAND_FILE" \
    "mode.*brownfield" \
    "ideate.md contains 'mode: brownfield' or similar marker"

################################################################################
# TEST 1.4: Context marker passed to skill
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 1.4: Context Marker Passed to Skill"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

assert_file_contains "$COMMAND_FILE" \
    "Mode:" \
    "ideate.md displays mode information before skill invocation"

assert_file_contains "$COMMAND_FILE" \
    "Context Files Found" \
    "ideate.md displays count of context files before skill invocation"

################################################################################
# TEST 1.5: Detection completes in <50ms (execution timing)
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 1.5: Detection Latency (<50ms)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Simulate the detection logic with Glob
START_TIME=$(date +%s%N)
file_count=$(find "$CONTEXT_DIR" -maxdepth 1 -name "*.md" -type f 2>/dev/null | wc -l)
END_TIME=$(date +%s%N)

ELAPSED_MS=$(( (END_TIME - START_TIME) / 1000000 ))

echo "Detection elapsed time: ${ELAPSED_MS}ms"

if [ "$ELAPSED_MS" -lt 50 ]; then
    echo -e "${GREEN}✓ PASS${NC}: Glob detection completes in <50ms"
    ((TESTS_RUN++))
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Glob detection took ${ELAPSED_MS}ms (expected <50ms)"
    ((TESTS_RUN++))
    ((TESTS_FAILED++))
fi

################################################################################
# TEST 1.6: Mode marker format is correct
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 1.6: Mode Marker Format"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

assert_file_contains "$COMMAND_FILE" \
    "\*\*Mode:\*\*.*brownfield" \
    "Mode marker uses correct Markdown format (**Mode:** brownfield)"

assert_file_contains "$COMMAND_FILE" \
    "Detection Method" \
    "Mode marker documents detection method"

################################################################################
# TEST 1.7: Next action suggestion for brownfield
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 1.7: Next Action Suggestion (Brownfield)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

assert_file_contains "$COMMAND_FILE" \
    "orchestrate\|create-sprint\|create-story" \
    "ideate.md suggests appropriate next steps for brownfield (/orchestrate, /create-sprint, or /create-story)"

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
