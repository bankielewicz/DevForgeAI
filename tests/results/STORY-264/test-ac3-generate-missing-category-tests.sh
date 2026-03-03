#!/bin/bash
# =============================================================================
# STORY-264 AC#3: Generate Tests for Missing Categories
# =============================================================================
# Test: Validates test-automator.md has guidance for generating tests
#       specifically targeting each missing category with descriptive names
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
TEST_NAME="AC#3: Generate Tests for Missing Categories"

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

echo "--- Structural Tests: Test Generation for Missing Categories ---"
echo ""

# Test 1: Section for generating tests targeting missing categories
assert_section_exists "Generate.*Missing|Remediation.*Test|Target.*Missing" \
    "Section for generating tests targeting missing categories"

# Test 2: Category-specific test generation guidance
assert_pattern_exists "generat.*target.*category|category.*specific.*test" \
    "Category-specific test generation guidance"

# Test 3: Descriptive test naming convention for exceptions
assert_pattern_exists "test_.*exception|test_.*error|exception.*test.*name" \
    "Descriptive test naming for exception tests (test_*_exception_*)"

# Test 4: Descriptive test naming convention for errors
assert_pattern_exists "test_.*_error_|error.*naming.*convention" \
    "Descriptive test naming for error tests (test_*_error_*)"

# Test 5: Descriptive test naming convention for boundaries
assert_pattern_exists "test_.*boundary|test_.*edge|boundary.*naming" \
    "Descriptive test naming for boundary tests"

# Test 6: Workflow for generating remediation tests per category
assert_pattern_exists "FOR.*category|for each.*missing|generat.*each.*category" \
    "Loop workflow for generating tests per missing category"

# Test 7: Example generated test showing category targeting
assert_pattern_exists "def test_|test.*function|@Test|\\[Fact\\]" \
    "Example generated test function in documentation"

# Test 8: Test output mapping (which test covers which category)
assert_pattern_exists "test.*cover.*category|category.*test.*map|generated.*test.*category" \
    "Test-to-category mapping in output"

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
