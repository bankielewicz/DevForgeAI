#!/bin/bash

##############################################################################
# Test Suite: STORY-145 AC#1 - Six Error-Type Files Created
# Purpose: Validate that error-handling.md is split into 6 error-type files
#
# Acceptance Criteria #1:
# Given error-handling.md contains ~1,062 lines covering multiple error types,
# When the file is split by error type,
# Then 6 new files are created:
#   1. error-type-1-incomplete-answers.md (~180 lines)
#   2. error-type-2-artifact-failures.md (~200 lines)
#   3. error-type-3-complexity-errors.md (~150 lines)
#   4. error-type-4-validation-failures.md (~180 lines)
#   5. error-type-5-constraint-conflicts.md (~170 lines)
#   6. error-type-6-directory-issues.md (~180 lines)
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
TEST_LOG="/tmp/story-145-ac1.log"

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/../.."
REFERENCES_DIR="${PROJECT_ROOT}/.claude/skills/devforgeai-ideation/references"

# Expected files for AC#1
declare -a ERROR_TYPE_FILES=(
    "error-type-1-incomplete-answers.md"
    "error-type-2-artifact-failures.md"
    "error-type-3-complexity-errors.md"
    "error-type-4-validation-failures.md"
    "error-type-5-constraint-conflicts.md"
    "error-type-6-directory-issues.md"
)

# Initialize log
echo "=== STORY-145 AC#1 Test Suite ===" > "$TEST_LOG"
echo "Test Started: $(date)" >> "$TEST_LOG"
echo "References Directory: ${REFERENCES_DIR}" >> "$TEST_LOG"

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

##############################################################################
# Test Cases for AC#1
##############################################################################

test_error_type_1_incomplete_answers_exists() {
    assert_file_exists "${REFERENCES_DIR}/error-type-1-incomplete-answers.md" \
        "error-type-1-incomplete-answers.md should exist"
}

test_error_type_1_incomplete_answers_readable() {
    assert_file_is_readable "${REFERENCES_DIR}/error-type-1-incomplete-answers.md" \
        "error-type-1-incomplete-answers.md should be readable"
}

test_error_type_1_incomplete_answers_not_empty() {
    assert_file_not_empty "${REFERENCES_DIR}/error-type-1-incomplete-answers.md" \
        "error-type-1-incomplete-answers.md should not be empty"
}

test_error_type_2_artifact_failures_exists() {
    assert_file_exists "${REFERENCES_DIR}/error-type-2-artifact-failures.md" \
        "error-type-2-artifact-failures.md should exist"
}

test_error_type_2_artifact_failures_readable() {
    assert_file_is_readable "${REFERENCES_DIR}/error-type-2-artifact-failures.md" \
        "error-type-2-artifact-failures.md should be readable"
}

test_error_type_2_artifact_failures_not_empty() {
    assert_file_not_empty "${REFERENCES_DIR}/error-type-2-artifact-failures.md" \
        "error-type-2-artifact-failures.md should not be empty"
}

test_error_type_3_complexity_errors_exists() {
    assert_file_exists "${REFERENCES_DIR}/error-type-3-complexity-errors.md" \
        "error-type-3-complexity-errors.md should exist"
}

test_error_type_3_complexity_errors_readable() {
    assert_file_is_readable "${REFERENCES_DIR}/error-type-3-complexity-errors.md" \
        "error-type-3-complexity-errors.md should be readable"
}

test_error_type_3_complexity_errors_not_empty() {
    assert_file_not_empty "${REFERENCES_DIR}/error-type-3-complexity-errors.md" \
        "error-type-3-complexity-errors.md should not be empty"
}

test_error_type_4_validation_failures_exists() {
    assert_file_exists "${REFERENCES_DIR}/error-type-4-validation-failures.md" \
        "error-type-4-validation-failures.md should exist"
}

test_error_type_4_validation_failures_readable() {
    assert_file_is_readable "${REFERENCES_DIR}/error-type-4-validation-failures.md" \
        "error-type-4-validation-failures.md should be readable"
}

test_error_type_4_validation_failures_not_empty() {
    assert_file_not_empty "${REFERENCES_DIR}/error-type-4-validation-failures.md" \
        "error-type-4-validation-failures.md should not be empty"
}

test_error_type_5_constraint_conflicts_exists() {
    assert_file_exists "${REFERENCES_DIR}/error-type-5-constraint-conflicts.md" \
        "error-type-5-constraint-conflicts.md should exist"
}

test_error_type_5_constraint_conflicts_readable() {
    assert_file_is_readable "${REFERENCES_DIR}/error-type-5-constraint-conflicts.md" \
        "error-type-5-constraint-conflicts.md should be readable"
}

test_error_type_5_constraint_conflicts_not_empty() {
    assert_file_not_empty "${REFERENCES_DIR}/error-type-5-constraint-conflicts.md" \
        "error-type-5-constraint-conflicts.md should not be empty"
}

test_error_type_6_directory_issues_exists() {
    assert_file_exists "${REFERENCES_DIR}/error-type-6-directory-issues.md" \
        "error-type-6-directory-issues.md should exist"
}

test_error_type_6_directory_issues_readable() {
    assert_file_is_readable "${REFERENCES_DIR}/error-type-6-directory-issues.md" \
        "error-type-6-directory-issues.md should be readable"
}

test_error_type_6_directory_issues_not_empty() {
    assert_file_not_empty "${REFERENCES_DIR}/error-type-6-directory-issues.md" \
        "error-type-6-directory-issues.md should not be empty"
}

test_all_six_files_present() {
    local all_present=0
    local missing_files=()

    for file in "${ERROR_TYPE_FILES[@]}"; do
        if [[ ! -f "${REFERENCES_DIR}/${file}" ]]; then
            missing_files+=("$file")
        fi
    done

    if [[ ${#missing_files[@]} -eq 0 ]]; then
        echo "  ✓ All 6 error-type files present" >> "$TEST_LOG"
        return 0
    else
        echo "ASSERTION FAILED: Not all 6 files present" >> "$TEST_LOG"
        echo "  ✗ Missing files:" >> "$TEST_LOG"
        for file in "${missing_files[@]}"; do
            echo "    - $file" >> "$TEST_LOG"
        done
        return 1
    fi
}

##############################################################################
# Run All Tests
##############################################################################

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}STORY-145 AC#1: Six Error-Type Files${NC}"
echo -e "${BLUE}========================================${NC}"

run_test "error-type-1-incomplete-answers.md exists" test_error_type_1_incomplete_answers_exists
run_test "error-type-1-incomplete-answers.md is readable" test_error_type_1_incomplete_answers_readable
run_test "error-type-1-incomplete-answers.md is not empty" test_error_type_1_incomplete_answers_not_empty

run_test "error-type-2-artifact-failures.md exists" test_error_type_2_artifact_failures_exists
run_test "error-type-2-artifact-failures.md is readable" test_error_type_2_artifact_failures_readable
run_test "error-type-2-artifact-failures.md is not empty" test_error_type_2_artifact_failures_not_empty

run_test "error-type-3-complexity-errors.md exists" test_error_type_3_complexity_errors_exists
run_test "error-type-3-complexity-errors.md is readable" test_error_type_3_complexity_errors_readable
run_test "error-type-3-complexity-errors.md is not empty" test_error_type_3_complexity_errors_not_empty

run_test "error-type-4-validation-failures.md exists" test_error_type_4_validation_failures_exists
run_test "error-type-4-validation-failures.md is readable" test_error_type_4_validation_failures_readable
run_test "error-type-4-validation-failures.md is not empty" test_error_type_4_validation_failures_not_empty

run_test "error-type-5-constraint-conflicts.md exists" test_error_type_5_constraint_conflicts_exists
run_test "error-type-5-constraint-conflicts.md is readable" test_error_type_5_constraint_conflicts_readable
run_test "error-type-5-constraint-conflicts.md is not empty" test_error_type_5_constraint_conflicts_not_empty

run_test "error-type-6-directory-issues.md exists" test_error_type_6_directory_issues_exists
run_test "error-type-6-directory-issues.md is readable" test_error_type_6_directory_issues_readable
run_test "error-type-6-directory-issues.md is not empty" test_error_type_6_directory_issues_not_empty

run_test "All 6 error-type files present" test_all_six_files_present

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
