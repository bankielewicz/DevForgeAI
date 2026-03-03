#!/bin/bash
###############################################################################
# Test Suite: STORY-178 AC-2 - Structural Testing Guidance
#
# AC-2: Structural Testing Guidance
# Then: guidance for testing section headers, phase markers documented
#
# Tests validate:
# - Guidance for testing structural elements (headers, markers)
# - Documentation of section header validation patterns
# - Documentation of phase marker testing patterns
###############################################################################

set -euo pipefail

TEST_NAME="AC-2: Structural Testing Guidance"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$TEST_DIR/../.." && pwd)"
TARGET_FILE=".claude/agents/test-automator.md"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

run_test() {
    local test_name=$1
    local test_func=$2

    TESTS_RUN=$((TESTS_RUN + 1))
    echo -e "\n${BLUE}[Test $TESTS_RUN]${NC} $test_name"

    if $test_func; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "${GREEN}  PASS${NC}"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}  FAIL${NC}"
    fi
}

###############################################################################
# TEST 1: Section header testing guidance documented
###############################################################################

test_section_header_guidance() {
    # Test: Document contains guidance for testing section headers
    # Pattern: mentions testing headers/headings in structural context

    if grep -qiE "(section|heading|header).*(test|validat|check)" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: Section header testing guidance"
        return 0
    elif grep -qiE "(test|validat|check).*(section|heading|header)" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: Header validation guidance"
        return 0
    else
        echo "  ERROR: No section header testing guidance found"
        echo "  Expected: Guidance for testing/validating section headers"
        return 1
    fi
}

###############################################################################
# TEST 2: Phase marker testing guidance documented
###############################################################################

test_phase_marker_guidance() {
    # Test: Document contains guidance for testing phase markers
    # Pattern: mentions phase markers, phase sections, or workflow phases

    if grep -qiE "(phase|marker|workflow).*(test|validat|check)" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: Phase marker testing guidance"
        return 0
    elif grep -qiE "(test|validat|check).*(phase|marker)" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: Marker validation guidance"
        return 0
    else
        echo "  ERROR: No phase marker testing guidance found"
        echo "  Expected: Guidance for testing phase markers in spec files"
        return 1
    fi
}

###############################################################################
# TEST 3: Structural element testing concept documented
###############################################################################

test_structural_testing_concept() {
    # Test: Document explains structural vs content testing
    # This is the core concept - test structure not narrative text

    if grep -qiE "structur.*(test|validat)" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: Structural testing concept"
        return 0
    elif grep -qiE "(test|validat).*structur" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: Structure validation concept"
        return 0
    else
        echo "  ERROR: Structural testing concept not documented"
        echo "  Expected: Guidance on testing structural elements"
        return 1
    fi
}

###############################################################################
# TEST 4: grep/pattern matching guidance for structure
###############################################################################

test_pattern_matching_guidance() {
    # Test: Document mentions grep, regex, or pattern matching for structure
    # These are the tools used for structural validation

    if grep -qiE "(grep|regex|pattern).*(structur|header|section)" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: Pattern matching guidance for structure"
        return 0
    elif grep -qiE "(structur|header|section).*(grep|regex|pattern)" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: Structural pattern matching guidance"
        return 0
    else
        echo "  ERROR: No pattern matching guidance for structural testing"
        echo "  Expected: References to grep/regex/pattern for structure validation"
        return 1
    fi
}

###############################################################################
# Main Test Execution
###############################################################################

main() {
    echo -e "${BLUE}=============================================================${NC}"
    echo -e "${BLUE}$TEST_NAME${NC}"
    echo -e "${BLUE}=============================================================${NC}"
    echo ""
    echo "Target file: $TARGET_FILE"
    echo ""

    run_test "AC-2.1: Section header testing guidance" "test_section_header_guidance"
    run_test "AC-2.2: Phase marker testing guidance" "test_phase_marker_guidance"
    run_test "AC-2.3: Structural testing concept documented" "test_structural_testing_concept"
    run_test "AC-2.4: Pattern matching guidance" "test_pattern_matching_guidance"

    # Summary
    echo ""
    echo -e "${BLUE}=============================================================${NC}"
    echo -e "Tests run:    ${BLUE}$TESTS_RUN${NC}"
    echo -e "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
    echo -e "Tests failed: ${RED}$TESTS_FAILED${NC}"
    echo -e "${BLUE}=============================================================${NC}"

    [ "$TESTS_FAILED" -eq 0 ] && exit 0 || exit 1
}

main "$@"
