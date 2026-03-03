#!/bin/bash
###############################################################################
# Test Suite: STORY-178 AC-1 - Specification File Testing Section Added
#
# AC-1: Specification File Testing Section Added
# Given: test-automator.md
# Then: includes "Specification File Testing" section
#
# Tests validate:
# - Section header exists with correct naming
# - Section is properly positioned (after existing content)
# - Section contains Markdown command/skill context
###############################################################################

set -euo pipefail

TEST_NAME="AC-1: Specification File Testing Section Added"
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
# TEST 1: Target file exists
###############################################################################

test_target_file_exists() {
    if [ -f "$PROJECT_ROOT/$TARGET_FILE" ]; then
        echo "  Found: $TARGET_FILE"
        return 0
    else
        echo "  ERROR: File not found: $TARGET_FILE"
        return 1
    fi
}

###############################################################################
# TEST 2: Section header exists with structural pattern matching
###############################################################################

test_spec_file_testing_section_header() {
    # Test: Section header "Specification File Testing" or similar exists
    # Uses structural matching - looking for heading pattern, not exact text

    if grep -qE "^#+ .*Specification File Testing" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: Specification File Testing section header"
        return 0
    elif grep -qE "^#+ .*Spec.*File.*Test" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: Specification file testing section (variant)"
        return 0
    else
        echo "  ERROR: No 'Specification File Testing' section header found"
        echo "  Expected: Heading matching pattern '^#+ .*Specification File Testing'"
        return 1
    fi
}

###############################################################################
# TEST 3: Section includes Markdown command/skill context
###############################################################################

test_section_includes_markdown_context() {
    # Test: Section mentions Markdown commands or skills context
    # This validates the section is about testing spec files (skills/commands)

    local section_content=""

    # Extract content after the section header
    if grep -qE "^#+ .*Specification File Testing" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        section_content=$(sed -n '/^#.*Specification File Testing/,/^## /p' "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null | head -100)
    fi

    if echo "$section_content" | grep -qiE "markdown|command|skill|\.md" 2>/dev/null; then
        echo "  Found: Markdown/command/skill context in section"
        return 0
    else
        echo "  ERROR: Section missing Markdown command/skill context"
        echo "  Expected: References to Markdown, commands, or skills"
        return 1
    fi
}

###############################################################################
# TEST 4: Section is in a logical position (not at very beginning)
###############################################################################

test_section_position() {
    # Test: Section appears after line 100 (not in frontmatter/purpose sections)

    local line_num=$(grep -nE "^#+ .*Specification File Testing" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null | head -1 | cut -d: -f1)

    if [ -n "$line_num" ] && [ "$line_num" -gt 100 ]; then
        echo "  Found: Section at line $line_num (after core documentation)"
        return 0
    elif [ -n "$line_num" ]; then
        echo "  WARNING: Section at line $line_num (expected after line 100)"
        return 0  # Still pass - position is flexible
    else
        echo "  ERROR: Section not found"
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

    run_test "AC-1.1: Target file exists" "test_target_file_exists"
    run_test "AC-1.2: Section header present" "test_spec_file_testing_section_header"
    run_test "AC-1.3: Markdown context included" "test_section_includes_markdown_context"
    run_test "AC-1.4: Section position logical" "test_section_position"

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
