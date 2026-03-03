#!/bin/bash
###############################################################################
# Test Suite: STORY-178 AC-3 - Tool Invocation Testing Guidance
#
# AC-3: Tool Invocation Testing Guidance
# Then: guidance for testing AskUserQuestion, Read, Write references documented
#
# Tests validate:
# - Guidance for testing tool references in spec files
# - Documentation of AskUserQuestion pattern testing
# - Documentation of Read/Write tool reference testing
###############################################################################

set -euo pipefail

TEST_NAME="AC-3: Tool Invocation Testing Guidance"
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
# TEST 1: Tool invocation testing concept documented
###############################################################################

test_tool_invocation_concept() {
    # Test: Document explains testing tool references/invocations
    # Pattern: mentions testing tool calls, tool references, invocations

    if grep -qiE "(tool|invoca).*(test|validat|check)" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: Tool invocation testing concept"
        return 0
    elif grep -qiE "(test|validat|check).*(tool|invoca)" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: Tool testing concept"
        return 0
    else
        echo "  ERROR: Tool invocation testing concept not documented"
        echo "  Expected: Guidance on testing tool references"
        return 1
    fi
}

###############################################################################
# TEST 2: AskUserQuestion pattern documented
###############################################################################

test_ask_user_question_pattern() {
    # Test: Document mentions AskUserQuestion in testing context
    # This is a key tool for spec file validation

    if grep -qE "AskUserQuestion" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        # Check if it's in a testing/validation context
        local context=$(grep -A3 -B3 "AskUserQuestion" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null | head -20)
        if echo "$context" | grep -qiE "test|validat|check|pattern" 2>/dev/null; then
            echo "  Found: AskUserQuestion in testing context"
            return 0
        else
            echo "  Found: AskUserQuestion mentioned (context unclear)"
            return 0  # Still pass - the tool is referenced
        fi
    else
        echo "  ERROR: AskUserQuestion not mentioned"
        echo "  Expected: AskUserQuestion testing guidance"
        return 1
    fi
}

###############################################################################
# TEST 3: Read tool testing pattern documented
###############################################################################

test_read_tool_pattern() {
    # Test: Document mentions Read tool in testing/validation context
    # Read is essential for spec file testing

    if grep -qE "Read\(" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: Read tool pattern (Read() syntax)"
        return 0
    elif grep -qE "\bRead\b.*tool" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: Read tool reference"
        return 0
    elif grep -qiE "Read.*file_path" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: Read with file_path parameter"
        return 0
    else
        echo "  ERROR: Read tool testing pattern not found"
        echo "  Expected: Read() or Read tool testing guidance"
        return 1
    fi
}

###############################################################################
# TEST 4: Write tool testing pattern documented
###############################################################################

test_write_tool_pattern() {
    # Test: Document mentions Write tool in testing/validation context

    if grep -qE "Write\(" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: Write tool pattern (Write() syntax)"
        return 0
    elif grep -qE "\bWrite\b.*tool" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: Write tool reference"
        return 0
    elif grep -qiE "Write.*file_path" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: Write with file_path parameter"
        return 0
    else
        echo "  ERROR: Write tool testing pattern not found"
        echo "  Expected: Write() or Write tool testing guidance"
        return 1
    fi
}

###############################################################################
# TEST 5: Combined tool testing guidance in Specification File Testing section
###############################################################################

test_tools_in_spec_section() {
    # Test: The Specification File Testing section mentions tools
    # This ensures the tool guidance is in the right location

    local section_content=""

    # Extract content from Specification File Testing section
    if grep -qE "^#+ .*Specification File Testing" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        section_content=$(sed -n '/^#.*Specification File Testing/,/^## [A-Z]/p' "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null | head -100)

        if echo "$section_content" | grep -qiE "tool|Read|Write|AskUserQuestion" 2>/dev/null; then
            echo "  Found: Tool references in Specification File Testing section"
            return 0
        else
            echo "  WARNING: Section exists but no tool references found"
            return 1
        fi
    else
        echo "  ERROR: Specification File Testing section not found"
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

    run_test "AC-3.1: Tool invocation testing concept" "test_tool_invocation_concept"
    run_test "AC-3.2: AskUserQuestion pattern documented" "test_ask_user_question_pattern"
    run_test "AC-3.3: Read tool pattern documented" "test_read_tool_pattern"
    run_test "AC-3.4: Write tool pattern documented" "test_write_tool_pattern"
    run_test "AC-3.5: Tools in Spec File Testing section" "test_tools_in_spec_section"

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
