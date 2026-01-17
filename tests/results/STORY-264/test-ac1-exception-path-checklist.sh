#!/bin/bash
# =============================================================================
# STORY-264 AC#1: Exception Path Coverage Checklist
# =============================================================================
# Test: Validates test-automator.md contains 4-category coverage checklist
#       (Happy | Errors | Exceptions | Boundaries)
#
# Implementation Type: Slash Command (.md) - structural validation
# Target File: .claude/agents/test-automator.md
# Expected State: FAILING (RED) - guidance not yet implemented
# =============================================================================

set -e

# Test configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
TARGET_FILE="${PROJECT_ROOT}/.claude/agents/test-automator.md"
TEST_NAME="AC#1: Exception Path Coverage Checklist"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Test tracking
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Helper function
assert_pattern_exists() {
    local pattern="$1"
    local description="$2"
    TESTS_RUN=$((TESTS_RUN + 1))

    if grep -qE "$pattern" "$TARGET_FILE" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}: $description"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}FAIL${NC}: $description"
        echo "       Pattern not found: $pattern"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

assert_section_exists() {
    local section="$1"
    local description="$2"
    TESTS_RUN=$((TESTS_RUN + 1))

    if grep -qE "^##+ .*${section}" "$TARGET_FILE" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}: $description"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}FAIL${NC}: $description"
        echo "       Section header not found: $section"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

# =============================================================================
# TEST EXECUTION
# =============================================================================

echo "=============================================="
echo "STORY-264 ${TEST_NAME}"
echo "=============================================="
echo "Target: ${TARGET_FILE}"
echo ""

# Verify target file exists
if [[ ! -f "$TARGET_FILE" ]]; then
    echo -e "${RED}ERROR${NC}: Target file not found: $TARGET_FILE"
    exit 1
fi

echo "--- Structural Tests: 4-Category Framework ---"
echo ""

# Test 1: Section header for Exception Path Coverage exists
assert_section_exists "Exception Path Coverage" \
    "Section header '## Exception Path Coverage' exists"

# Test 2: 4-Category framework definition section exists
assert_section_exists "4-Category Coverage" \
    "Section header '4-Category Coverage Framework' exists"

# Test 3: HAPPY_PATH category documented
assert_pattern_exists "HAPPY_PATH|Happy [Pp]ath" \
    "HAPPY_PATH category documented in coverage framework"

# Test 4: ERROR_PATHS category documented
assert_pattern_exists "ERROR_PATH|Error [Pp]ath|Error [Rr]eturn" \
    "ERROR_PATHS category documented in coverage framework"

# Test 5: EXCEPTION_HANDLERS category documented
assert_pattern_exists "EXCEPTION_HANDLER|Exception [Hh]andler|try.*(except|catch)" \
    "EXCEPTION_HANDLERS category documented in coverage framework"

# Test 6: BOUNDARY_CONDITIONS category documented
assert_pattern_exists "BOUNDARY_CONDITION|Boundary [Cc]ondition|[Ee]dge [Cc]ase" \
    "BOUNDARY_CONDITIONS category documented in coverage framework"

# Test 7: Checklist format for 4 categories (checkbox pattern)
assert_pattern_exists "\[[ x]\].*[Hh]appy" \
    "Checklist checkbox for Happy path exists"

assert_pattern_exists "\[[ x]\].*[Ee]rror" \
    "Checklist checkbox for Error paths exists"

assert_pattern_exists "\[[ x]\].*[Ee]xception" \
    "Checklist checkbox for Exception handlers exists"

assert_pattern_exists "\[[ x]\].*[Bb]oundary" \
    "Checklist checkbox for Boundary conditions exists"

# Test 8: Coverage checklist generation guidance
assert_pattern_exists "generate.*checklist|checklist.*generat" \
    "Guidance for generating coverage checklist exists"

echo ""
echo "=============================================="
echo "RESULTS: ${TESTS_PASSED}/${TESTS_RUN} tests passed"
echo "=============================================="

if [[ $TESTS_FAILED -gt 0 ]]; then
    echo -e "${RED}STATUS: FAILING (RED)${NC} - Implementation needed"
    exit 1
else
    echo -e "${GREEN}STATUS: PASSING (GREEN)${NC}"
    exit 0
fi
