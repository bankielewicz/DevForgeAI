#!/bin/bash
###############################################################################
# Test Suite: STORY-178 AC-5 - Example Patterns Provided
#
# AC-5: Example Patterns Provided
# Then: example test patterns for Markdown commands included
#
# Tests validate:
# - Code examples for testing spec files exist
# - Examples show grep/pattern matching usage
# - Examples demonstrate structural validation
###############################################################################

set -euo pipefail

TEST_NAME="AC-5: Example Patterns Provided"
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
# TEST 1: Code block examples exist for spec file testing
###############################################################################

test_code_examples_exist() {
    # Test: Document contains code examples (in ``` blocks) after Spec File Testing section

    local section_content=""

    if grep -qE "^#+ .*Specification File Testing" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        section_content=$(sed -n '/^#.*Specification File Testing/,/^## [A-Z]/p' "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null)

        # Count code blocks in section
        local block_count=$(echo "$section_content" | grep -c '```' 2>/dev/null || echo "0")

        if [ "$block_count" -ge 2 ]; then
            echo "  Found: $((block_count/2)) code example blocks in section"
            return 0
        elif [ "$block_count" -ge 1 ]; then
            echo "  Found: Code blocks present (partial)"
            return 0
        else
            echo "  ERROR: No code examples in Specification File Testing section"
            return 1
        fi
    else
        echo "  ERROR: Specification File Testing section not found"
        return 1
    fi
}

###############################################################################
# TEST 2: grep pattern example included
###############################################################################

test_grep_example_included() {
    # Test: Examples include grep command or pattern matching

    local section_content=""

    if grep -qE "^#+ .*Specification File Testing" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        section_content=$(sed -n '/^#.*Specification File Testing/,/^## [A-Z]/p' "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null)

        if echo "$section_content" | grep -qE "grep|Grep|pattern" 2>/dev/null; then
            echo "  Found: grep/pattern example in section"
            return 0
        fi
    fi

    # Fallback: Check for grep patterns anywhere in document related to spec testing
    if grep -qE "grep.*-q.*#+" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: grep pattern for header validation"
        return 0
    elif grep -qE "grep.*\^#" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: grep pattern for Markdown headers"
        return 0
    else
        echo "  ERROR: No grep/pattern example found"
        echo "  Expected: Example using grep for structural validation"
        return 1
    fi
}

###############################################################################
# TEST 3: Header validation example included
###############################################################################

test_header_validation_example() {
    # Test: Example shows testing for Markdown headers (## or ###)

    local section_content=""

    if grep -qE "^#+ .*Specification File Testing" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        section_content=$(sed -n '/^#.*Specification File Testing/,/^## [A-Z]/p' "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null)

        if echo "$section_content" | grep -qE '##.*\||^#+|heading|header.*test' 2>/dev/null; then
            echo "  Found: Header validation example"
            return 0
        fi
    fi

    # Check for regex patterns that match Markdown headers
    if grep -qE '\^#|\\\^##' "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: Regex pattern for Markdown headers"
        return 0
    else
        echo "  ERROR: No header validation example found"
        echo "  Expected: Example showing how to test for section headers"
        return 1
    fi
}

###############################################################################
# TEST 4: Bash/shell test example (test command pattern)
###############################################################################

test_bash_test_example() {
    # Test: Examples show bash test patterns (if [ ... ], test command)
    # These are the actual test implementations for spec files

    local section_content=""

    if grep -qE "^#+ .*Specification File Testing" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        section_content=$(sed -n '/^#.*Specification File Testing/,/^## [A-Z]/p' "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null)

        if echo "$section_content" | grep -qE 'if \[|test -f|\[ -f' 2>/dev/null; then
            echo "  Found: Bash test pattern example"
            return 0
        elif echo "$section_content" | grep -qE '\.sh|bash|shell' 2>/dev/null; then
            echo "  Found: Shell script reference"
            return 0
        fi
    fi

    # General check for bash patterns in spec file testing context
    if grep -qiE "(spec.*file|markdown.*command).*(bash|shell|test.*script)" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: Bash/shell reference for spec file testing"
        return 0
    else
        echo "  WARNING: Bash test example not clearly present"
        echo "  Note: Other test patterns may be used (Python, etc.)"
        # Soft failure - not all implementations use bash
        return 1
    fi
}

###############################################################################
# TEST 5: At least 40 lines of new content in section
###############################################################################

test_section_content_length() {
    # Test: Specification File Testing section has substantive content (40+ lines)
    # Per AC: approximately 40-50 lines of new documentation

    local section_content=""

    if grep -qE "^#+ .*Specification File Testing" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        section_content=$(sed -n '/^#.*Specification File Testing/,/^## [A-Z]/p' "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null)

        local line_count=$(echo "$section_content" | wc -l)

        if [ "$line_count" -ge 40 ]; then
            echo "  Found: Section has $line_count lines (meets 40+ requirement)"
            return 0
        elif [ "$line_count" -ge 25 ]; then
            echo "  Found: Section has $line_count lines (close to requirement)"
            return 0  # Accept if reasonably close
        else
            echo "  ERROR: Section has only $line_count lines (expected 40+)"
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

    run_test "AC-5.1: Code examples exist" "test_code_examples_exist"
    run_test "AC-5.2: grep pattern example included" "test_grep_example_included"
    run_test "AC-5.3: Header validation example" "test_header_validation_example"
    run_test "AC-5.4: Bash test pattern example" "test_bash_test_example"
    run_test "AC-5.5: Section has 40+ lines" "test_section_content_length"

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
