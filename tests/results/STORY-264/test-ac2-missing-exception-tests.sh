#!/bin/bash
# =============================================================================
# STORY-264 AC#2: Identify Missing Exception Tests
# =============================================================================
# Test: Validates test-automator.md has guidance for identifying which
#       coverage categories lack tests (missing: Happy | Errors | Exceptions | Boundaries)
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
TEST_NAME="AC#2: Identify Missing Exception Tests"

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

echo "--- Structural Tests: Missing Test Identification ---"
echo ""

# Test 1: Section for identifying missing tests
assert_section_exists "Identify.*Missing|Missing.*Test|Coverage Gap" \
    "Section for identifying missing exception tests exists"

# Test 2: Workflow for analyzing existing test suite
assert_pattern_exists "analyz.*existing.*test|existing.*test.*analyz|test suite.*analyz" \
    "Guidance for analyzing existing test suite against checklist"

# Test 3: Output format showing which categories lack coverage
assert_pattern_exists "missing.*category|category.*lack|lack.*coverage" \
    "Output format for missing category identification"

# Test 4: Pattern for listing missing categories (format: missing: X | Y | Z)
assert_pattern_exists "missing:.*\|" \
    "Pattern showing 'missing: X | Y' format for category gaps"

# Test 5: Guidance for comparing tests against 4-category framework
assert_pattern_exists "compar.*checklist|checklist.*compar|match.*category" \
    "Comparison workflow: tests vs. 4-category checklist"

# Test 6: Example output showing gap identification
assert_pattern_exists "gap.*identif|identif.*gap|coverage.*gap" \
    "Example showing coverage gap identification output"

# Test 7: Workflow step for test coverage mapping
assert_pattern_exists "map.*test.*category|category.*map|coverage.*map" \
    "Test-to-category mapping workflow documented"

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
