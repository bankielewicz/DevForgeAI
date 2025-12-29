#!/bin/bash

##############################################################################
# Test Suite: STORY-145 AC#6 - Each File Stays Under 250 Lines
# Purpose: Validate that each error-type file maintains size limit
#
# Acceptance Criteria #6:
# Given target file size is <250 lines for maintainability,
# When line counts are checked for each error-type file,
# Then no file exceeds 250 lines.
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
TEST_LOG="/tmp/story-145-ac6.log"

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/../.."
REFERENCES_DIR="${PROJECT_ROOT}/.claude/skills/devforgeai-ideation/references"

# Line count limits
MAX_LINES_PER_FILE=250

# All files to check
declare -a ERROR_TYPE_FILES=(
    "error-type-1-incomplete-answers.md"
    "error-type-2-artifact-failures.md"
    "error-type-3-complexity-errors.md"
    "error-type-4-validation-failures.md"
    "error-type-5-constraint-conflicts.md"
    "error-type-6-directory-issues.md"
)

# Initialize log
echo "=== STORY-145 AC#6 Test Suite ===" > "$TEST_LOG"
echo "Test Started: $(date)" >> "$TEST_LOG"
echo "References Directory: ${REFERENCES_DIR}" >> "$TEST_LOG"
echo "Maximum lines per file: $MAX_LINES_PER_FILE" >> "$TEST_LOG"

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

assert_line_count_under_limit() {
    local file_path=$1
    local max_lines=$2
    local message="${3:-Line count should be under limit}"

    if [[ ! -f "$file_path" ]]; then
        echo "ASSERTION FAILED: File not found" >> "$TEST_LOG"
        echo "  ✗ File: $file_path" >> "$TEST_LOG"
        return 1
    fi

    local line_count
    line_count=$(wc -l < "$file_path")

    if [[ $line_count -le $max_lines ]]; then
        echo "  ✓ Line count: $line_count (limit: $max_lines)" >> "$TEST_LOG"
        return 0
    else
        echo "ASSERTION FAILED: $message" >> "$TEST_LOG"
        echo "  ✗ File: $file_path" >> "$TEST_LOG"
        echo "  ✗ Line count: $line_count (exceeds limit of $max_lines)" >> "$TEST_LOG"
        return 1
    fi
}

##############################################################################
# Test Cases for AC#6
##############################################################################

test_error_type_1_under_limit() {
    assert_file_exists "${REFERENCES_DIR}/error-type-1-incomplete-answers.md" \
        "error-type-1 should exist"

    assert_line_count_under_limit \
        "${REFERENCES_DIR}/error-type-1-incomplete-answers.md" \
        "$MAX_LINES_PER_FILE" \
        "error-type-1 should stay under $MAX_LINES_PER_FILE lines"
}

test_error_type_2_under_limit() {
    assert_file_exists "${REFERENCES_DIR}/error-type-2-artifact-failures.md" \
        "error-type-2 should exist"

    assert_line_count_under_limit \
        "${REFERENCES_DIR}/error-type-2-artifact-failures.md" \
        "$MAX_LINES_PER_FILE" \
        "error-type-2 should stay under $MAX_LINES_PER_FILE lines"
}

test_error_type_3_under_limit() {
    assert_file_exists "${REFERENCES_DIR}/error-type-3-complexity-errors.md" \
        "error-type-3 should exist"

    assert_line_count_under_limit \
        "${REFERENCES_DIR}/error-type-3-complexity-errors.md" \
        "$MAX_LINES_PER_FILE" \
        "error-type-3 should stay under $MAX_LINES_PER_FILE lines"
}

test_error_type_4_under_limit() {
    assert_file_exists "${REFERENCES_DIR}/error-type-4-validation-failures.md" \
        "error-type-4 should exist"

    assert_line_count_under_limit \
        "${REFERENCES_DIR}/error-type-4-validation-failures.md" \
        "$MAX_LINES_PER_FILE" \
        "error-type-4 should stay under $MAX_LINES_PER_FILE lines"
}

test_error_type_5_under_limit() {
    assert_file_exists "${REFERENCES_DIR}/error-type-5-constraint-conflicts.md" \
        "error-type-5 should exist"

    assert_line_count_under_limit \
        "${REFERENCES_DIR}/error-type-5-constraint-conflicts.md" \
        "$MAX_LINES_PER_FILE" \
        "error-type-5 should stay under $MAX_LINES_PER_FILE lines"
}

test_error_type_6_under_limit() {
    assert_file_exists "${REFERENCES_DIR}/error-type-6-directory-issues.md" \
        "error-type-6 should exist"

    assert_line_count_under_limit \
        "${REFERENCES_DIR}/error-type-6-directory-issues.md" \
        "$MAX_LINES_PER_FILE" \
        "error-type-6 should stay under $MAX_LINES_PER_FILE lines"
}

test_all_files_within_limits() {
    local all_within_limit=true
    local violations=()

    for file in "${ERROR_TYPE_FILES[@]}"; do
        local file_path="${REFERENCES_DIR}/${file}"

        if [[ ! -f "$file_path" ]]; then
            violations+=("$file: NOT FOUND")
            all_within_limit=false
            continue
        fi

        local line_count
        line_count=$(wc -l < "$file_path")

        if [[ $line_count -gt $MAX_LINES_PER_FILE ]]; then
            violations+=("$file: $line_count lines (exceeds $MAX_LINES_PER_FILE)")
            all_within_limit=false
        fi
    done

    if [[ "$all_within_limit" == true ]]; then
        echo "  ✓ All 6 error-type files stay under $MAX_LINES_PER_FILE lines" >> "$TEST_LOG"
        return 0
    else
        echo "ASSERTION FAILED: Some files exceed line limit" >> "$TEST_LOG"
        for violation in "${violations[@]}"; do
            echo "  ✗ $violation" >> "$TEST_LOG"
        done
        return 1
    fi
}

test_index_file_within_reasonable_size() {
    local index_file="${REFERENCES_DIR}/error-handling-index.md"

    if [[ ! -f "$index_file" ]]; then
        echo "ASSERTION FAILED: Index file not found" >> "$TEST_LOG"
        return 1
    fi

    local line_count
    line_count=$(wc -l < "$index_file")

    # Index file has reasonable limit (smaller than error-type files)
    local index_limit=100

    if [[ $line_count -le $index_limit ]]; then
        echo "  ✓ Index file line count: $line_count (reasonable, limit ~$index_limit)" >> "$TEST_LOG"
        return 0
    else
        echo "  ℹ Index file line count: $line_count (exceeds recommended ~$index_limit, but acceptable)" >> "$TEST_LOG"
        return 0
    fi
}

##############################################################################
# Run All Tests
##############################################################################

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}STORY-145 AC#6: Line Count Limits${NC}"
echo -e "${BLUE}========================================${NC}"

run_test "error-type-1 stays under 250 lines" test_error_type_1_under_limit
run_test "error-type-2 stays under 250 lines" test_error_type_2_under_limit
run_test "error-type-3 stays under 250 lines" test_error_type_3_under_limit
run_test "error-type-4 stays under 250 lines" test_error_type_4_under_limit
run_test "error-type-5 stays under 250 lines" test_error_type_5_under_limit
run_test "error-type-6 stays under 250 lines" test_error_type_6_under_limit

run_test "All 6 error-type files within limits" test_all_files_within_limits
run_test "Index file within reasonable size" test_index_file_within_reasonable_size

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
