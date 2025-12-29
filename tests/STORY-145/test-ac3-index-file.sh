#!/bin/bash

##############################################################################
# Test Suite: STORY-145 AC#3 - Master Index File Created
# Purpose: Validate error-handling-index.md with decision tree and links
#
# Acceptance Criteria #3:
# Given error-handling.md has been split into 6 files,
# When developers need to identify which error type they're experiencing,
# Then error-handling-index.md exists with:
#   - Decision tree: "Which error type am I experiencing?"
#   - Quick reference table mapping symptoms to error types
#   - Links to each of the 6 error-type files
##############################################################################

set -o pipefail

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
TEST_LOG="/tmp/story-145-ac3.log"

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/../.."
REFERENCES_DIR="${PROJECT_ROOT}/.claude/skills/devforgeai-ideation/references"
INDEX_FILE="${REFERENCES_DIR}/error-handling-index.md"

# All 6 error-type files that should be referenced
declare -a ERROR_TYPE_FILES=(
    "error-type-1-incomplete-answers.md"
    "error-type-2-artifact-failures.md"
    "error-type-3-complexity-errors.md"
    "error-type-4-validation-failures.md"
    "error-type-5-constraint-conflicts.md"
    "error-type-6-directory-issues.md"
)

# Initialize log
echo "=== STORY-145 AC#3 Test Suite ===" > "$TEST_LOG"
echo "Test Started: $(date)" >> "$TEST_LOG"
echo "Index File: ${INDEX_FILE}" >> "$TEST_LOG"

##############################################################################
# Test Framework Functions
##############################################################################

run_test() {
    local test_name=$1
    local test_func=$2

    TESTS_RUN=$((TESTS_RUN + 1))
    echo -e "\n${BLUE}[Test $TESTS_RUN]${NC} $test_name"

    if $test_func 2>> "$TEST_LOG"; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "${GREEN}✓${NC} PASSED"
        return 0
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}✗${NC} FAILED"
        return 1
    fi
}

assert_file_exists() {
    local file_path=$1
    local message="${2:-File should exist}"

    if [[ -f "$file_path" ]]; then
        echo "  ✓ File exists: $file_path" >> "$TEST_LOG"
        return 0
    else
        echo "ASSERTION FAILED: $message" >> "$TEST_LOG"
        echo "  ✗ File not found: $file_path" >> "$TEST_LOG"
        return 1
    fi
}

assert_file_is_readable() {
    local file_path=$1
    local message="${2:-File should be readable}"

    if [[ -r "$file_path" ]]; then
        echo "  ✓ File is readable: $file_path" >> "$TEST_LOG"
        return 0
    else
        echo "ASSERTION FAILED: $message" >> "$TEST_LOG"
        echo "  ✗ File is not readable: $file_path" >> "$TEST_LOG"
        return 1
    fi
}

assert_file_not_empty() {
    local file_path=$1
    local message="${2:-File should not be empty}"

    if [[ -s "$file_path" ]]; then
        echo "  ✓ File is not empty: $file_path" >> "$TEST_LOG"
        return 0
    else
        echo "ASSERTION FAILED: $message" >> "$TEST_LOG"
        echo "  ✗ File is empty: $file_path" >> "$TEST_LOG"
        return 1
    fi
}

assert_contains_text() {
    local file_path=$1
    local search_text=$2
    local message="${3:-File should contain text}"

    if [[ ! -f "$file_path" ]]; then
        echo "ASSERTION FAILED: File not found" >> "$TEST_LOG"
        echo "  ✗ File: $file_path" >> "$TEST_LOG"
        return 1
    fi

    local file_content
    file_content=$(cat "$file_path")

    if [[ "$file_content" == *"$search_text"* ]]; then
        echo "  ✓ Contains: $search_text" >> "$TEST_LOG"
        return 0
    else
        echo "ASSERTION FAILED: $message" >> "$TEST_LOG"
        echo "  ✗ File: $file_path" >> "$TEST_LOG"
        echo "  ✗ Did not find: $search_text" >> "$TEST_LOG"
        return 1
    fi
}

##############################################################################
# Test Cases for AC#3
##############################################################################

test_index_file_exists() {
    assert_file_exists "$INDEX_FILE" \
        "error-handling-index.md should exist"
}

test_index_file_readable() {
    assert_file_is_readable "$INDEX_FILE" \
        "error-handling-index.md should be readable"
}

test_index_file_not_empty() {
    assert_file_not_empty "$INDEX_FILE" \
        "error-handling-index.md should not be empty"
}

test_index_has_decision_tree() {
    assert_contains_text "$INDEX_FILE" \
        "## Decision Tree" \
        "Index file should have Decision Tree section"
}

test_index_has_quick_reference() {
    assert_contains_text "$INDEX_FILE" \
        "## Quick Reference" \
        "Index file should have Quick Reference section"
}

test_index_references_error_type_1() {
    assert_contains_text "$INDEX_FILE" \
        "error-type-1-incomplete-answers" \
        "Index should reference error-type-1-incomplete-answers"
}

test_index_references_error_type_2() {
    assert_contains_text "$INDEX_FILE" \
        "error-type-2-artifact-failures" \
        "Index should reference error-type-2-artifact-failures"
}

test_index_references_error_type_3() {
    assert_contains_text "$INDEX_FILE" \
        "error-type-3-complexity-errors" \
        "Index should reference error-type-3-complexity-errors"
}

test_index_references_error_type_4() {
    assert_contains_text "$INDEX_FILE" \
        "error-type-4-validation-failures" \
        "Index should reference error-type-4-validation-failures"
}

test_index_references_error_type_5() {
    assert_contains_text "$INDEX_FILE" \
        "error-type-5-constraint-conflicts" \
        "Index should reference error-type-5-constraint-conflicts"
}

test_index_references_error_type_6() {
    assert_contains_text "$INDEX_FILE" \
        "error-type-6-directory-issues" \
        "Index should reference error-type-6-directory-issues"
}

test_all_error_types_referenced() {
    if [[ ! -f "$INDEX_FILE" ]]; then
        echo "ASSERTION FAILED: Index file not found" >> "$TEST_LOG"
        return 1
    fi

    local file_content
    file_content=$(cat "$INDEX_FILE")

    local missing_refs=()

    for file in "${ERROR_TYPE_FILES[@]}"; do
        # Remove .md extension and check for reference (may be as link)
        local file_base="${file%.md}"
        if [[ "$file_content" != *"$file_base"* ]]; then
            missing_refs+=("$file_base")
        fi
    done

    if [[ ${#missing_refs[@]} -eq 0 ]]; then
        echo "  ✓ All 6 error-type files referenced in index" >> "$TEST_LOG"
        return 0
    else
        echo "ASSERTION FAILED: Not all error-type files referenced" >> "$TEST_LOG"
        echo "  ✗ Missing references:" >> "$TEST_LOG"
        for ref in "${missing_refs[@]}"; do
            echo "    - $ref" >> "$TEST_LOG"
        done
        return 1
    fi
}

test_index_has_proper_links() {
    if [[ ! -f "$INDEX_FILE" ]]; then
        echo "ASSERTION FAILED: Index file not found" >> "$TEST_LOG"
        return 1
    fi

    local file_content
    file_content=$(cat "$INDEX_FILE")

    # Check for Markdown link format: [text](error-type-N-*.md)
    # Look for at least some links to error-type files
    if echo "$file_content" | grep -q "error-type-[1-6].*\.md"; then
        echo "  ✓ Index contains links to error-type files" >> "$TEST_LOG"
        return 0
    else
        echo "ASSERTION FAILED: Index does not contain proper Markdown links" >> "$TEST_LOG"
        echo "  ✗ Expected format: [text](error-type-N-*.md)" >> "$TEST_LOG"
        return 1
    fi
}

##############################################################################
# Run All Tests
##############################################################################

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}STORY-145 AC#3: Master Index File${NC}"
echo -e "${BLUE}========================================${NC}"

run_test "error-handling-index.md exists" test_index_file_exists
run_test "error-handling-index.md is readable" test_index_file_readable
run_test "error-handling-index.md is not empty" test_index_file_not_empty

run_test "Index has Decision Tree section" test_index_has_decision_tree
run_test "Index has Quick Reference section" test_index_has_quick_reference

run_test "Index references error-type-1-incomplete-answers" test_index_references_error_type_1
run_test "Index references error-type-2-artifact-failures" test_index_references_error_type_2
run_test "Index references error-type-3-complexity-errors" test_index_references_error_type_3
run_test "Index references error-type-4-validation-failures" test_index_references_error_type_4
run_test "Index references error-type-5-constraint-conflicts" test_index_references_error_type_5
run_test "Index references error-type-6-directory-issues" test_index_references_error_type_6

run_test "All 6 error-type files referenced in index" test_all_error_types_referenced
run_test "Index has proper Markdown links to error-type files" test_index_has_proper_links

##############################################################################
# Test Summary
##############################################################################

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}Test Results${NC}"
echo -e "${BLUE}========================================${NC}"

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}✓ All $TESTS_RUN tests passed${NC}"
    echo "Results: $TESTS_PASSED/$TESTS_RUN passed, $TESTS_FAILED failed" >> "$TEST_LOG"
    exit 0
else
    echo -e "${RED}✗ $TESTS_FAILED of $TESTS_RUN tests failed${NC}"
    echo "Results: $TESTS_PASSED/$TESTS_RUN passed, $TESTS_FAILED failed" >> "$TEST_LOG"
    echo -e "\n${YELLOW}See test log for details:${NC} $TEST_LOG"
    exit 1
fi
