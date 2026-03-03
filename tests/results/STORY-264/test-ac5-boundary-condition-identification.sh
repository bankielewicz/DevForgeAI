#!/bin/bash
# =============================================================================
# STORY-264 AC#5: Boundary Condition Identification
# =============================================================================
# Test: Validates test-automator.md has guidance for identifying boundary
#       conditions (min/max values, off-by-one, empty collections) and
#       generating tests for them
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
TEST_NAME="AC#5: Boundary Condition Identification"

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

echo "--- Structural Tests: Boundary Condition Identification ---"
echo ""

# Test 1: Section for boundary condition identification
assert_section_exists "Boundary.*Condition|Boundary.*Identif|Edge.*Case.*Identif" \
    "Section for boundary condition identification exists"

# Test 2: COMP-003: Identify boundary conditions in numeric code
assert_pattern_exists "numeric.*boundary|boundary.*numeric|range.*boundary" \
    "COMP-003: Numeric boundary identification documented"

# Test 3: Min/max value identification
assert_pattern_exists "min.*max|maximum.*minimum|upper.*lower.*bound" \
    "Min/max value identification guidance"

# Test 4: Off-by-one error testing
assert_pattern_exists "off-by-one|off by one|fence.*post|boundary.*error" \
    "Off-by-one error testing guidance"

# Test 5: Empty collection testing
assert_pattern_exists "empty.*collection|empty.*list|empty.*array|\[\]" \
    "Empty collection boundary testing guidance"

# Test 6: Single element collection testing
assert_pattern_exists "single.*element|one.*element|\[1\]|single.*item" \
    "Single element collection boundary testing"

# Test 7: Loop boundary identification (range, for-in)
assert_pattern_exists "loop.*boundary|range.*boundary|for.*loop.*boundary" \
    "Loop boundary condition identification"

# Test 8: Example showing boundary test generation (0, 9, 10 for range(10))
assert_pattern_exists "0.*9.*10|range\(10\)|boundary.*example" \
    "Example boundary test generation (e.g., 0, 9, 10 for range(10))"

# Test 9: BR-003: Collection boundaries (empty, single, max size)
assert_pattern_exists "collection.*empty.*single|empty.*single.*max" \
    "BR-003: Collection boundary types (empty, single, max)"

# Test 10: Parameterized test generation for boundaries
assert_pattern_exists "parameteriz.*boundary|boundary.*parameteriz|boundary.*test.*data" \
    "Parameterized test generation for boundary conditions"

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
