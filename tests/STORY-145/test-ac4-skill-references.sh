#!/bin/bash

##############################################################################
# Test Suite: STORY-145 AC#4 - SKILL.md References Updated
# Purpose: Validate that SKILL.md Error Handling section lists all 6 files
#
# Acceptance Criteria #4:
# Given SKILL.md previously referenced single error-handling.md,
# When the "Error Handling" section is updated,
# Then it lists all 6 error-type files instead of the single file.
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
TEST_LOG="/tmp/story-145-ac4.log"

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/../.."
SKILL_FILE="${PROJECT_ROOT}/.claude/skills/devforgeai-ideation/SKILL.md"

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
echo "=== STORY-145 AC#4 Test Suite ===" > "$TEST_LOG"
echo "Test Started: $(date)" >> "$TEST_LOG"
echo "SKILL.md File: ${SKILL_FILE}" >> "$TEST_LOG"

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

assert_does_not_contain_text() {
    local file_path=$1
    local search_text=$2
    local message="${3:-File should not contain text}"

    if [[ ! -f "$file_path" ]]; then
        echo "ASSERTION FAILED: File not found" >> "$TEST_LOG"
        echo "  ✗ File: $file_path" >> "$TEST_LOG"
        return 1
    fi

    local file_content
    file_content=$(cat "$file_path")

    if [[ "$file_content" != *"$search_text"* ]]; then
        echo "  ✓ Does not contain: $search_text" >> "$TEST_LOG"
        return 0
    else
        echo "ASSERTION FAILED: $message" >> "$TEST_LOG"
        echo "  ✗ File: $file_path" >> "$TEST_LOG"
        echo "  ✗ Unexpectedly found: $search_text" >> "$TEST_LOG"
        return 1
    fi
}

##############################################################################
# Test Cases for AC#4
##############################################################################

test_skill_file_exists() {
    assert_file_exists "$SKILL_FILE" \
        "SKILL.md should exist"
}

test_skill_file_readable() {
    assert_file_is_readable "$SKILL_FILE" \
        "SKILL.md should be readable"
}

test_skill_has_error_handling_section() {
    assert_contains_text "$SKILL_FILE" \
        "Error Handling" \
        "SKILL.md should have Error Handling section"
}

test_skill_references_error_type_1() {
    assert_contains_text "$SKILL_FILE" \
        "error-type-1-incomplete-answers" \
        "SKILL.md should reference error-type-1-incomplete-answers"
}

test_skill_references_error_type_2() {
    assert_contains_text "$SKILL_FILE" \
        "error-type-2-artifact-failures" \
        "SKILL.md should reference error-type-2-artifact-failures"
}

test_skill_references_error_type_3() {
    assert_contains_text "$SKILL_FILE" \
        "error-type-3-complexity-errors" \
        "SKILL.md should reference error-type-3-complexity-errors"
}

test_skill_references_error_type_4() {
    assert_contains_text "$SKILL_FILE" \
        "error-type-4-validation-failures" \
        "SKILL.md should reference error-type-4-validation-failures"
}

test_skill_references_error_type_5() {
    assert_contains_text "$SKILL_FILE" \
        "error-type-5-constraint-conflicts" \
        "SKILL.md should reference error-type-5-constraint-conflicts"
}

test_skill_references_error_type_6() {
    assert_contains_text "$SKILL_FILE" \
        "error-type-6-directory-issues" \
        "SKILL.md should reference error-type-6-directory-issues"
}

test_skill_references_index() {
    assert_contains_text "$SKILL_FILE" \
        "error-handling-index" \
        "SKILL.md should reference error-handling-index"
}

test_all_error_types_in_skill() {
    if [[ ! -f "$SKILL_FILE" ]]; then
        echo "ASSERTION FAILED: SKILL.md not found" >> "$TEST_LOG"
        return 1
    fi

    local skill_content
    skill_content=$(cat "$SKILL_FILE")

    local missing_refs=()

    for file in "${ERROR_TYPE_FILES[@]}"; do
        # Remove .md extension and check for reference
        local file_base="${file%.md}"
        if [[ "$skill_content" != *"$file_base"* ]]; then
            missing_refs+=("$file_base")
        fi
    done

    if [[ ${#missing_refs[@]} -eq 0 ]]; then
        echo "  ✓ All 6 error-type files referenced in SKILL.md" >> "$TEST_LOG"
        return 0
    else
        echo "ASSERTION FAILED: Not all error-type files referenced in SKILL.md" >> "$TEST_LOG"
        echo "  ✗ Missing references:" >> "$TEST_LOG"
        for ref in "${missing_refs[@]}"; do
            echo "    - $ref" >> "$TEST_LOG"
        done
        return 1
    fi
}

test_skill_has_at_least_6_references() {
    if [[ ! -f "$SKILL_FILE" ]]; then
        echo "ASSERTION FAILED: SKILL.md not found" >> "$TEST_LOG"
        return 1
    fi

    local skill_content
    skill_content=$(cat "$SKILL_FILE")

    local reference_count=0

    for file in "${ERROR_TYPE_FILES[@]}"; do
        local file_base="${file%.md}"
        if [[ "$skill_content" == *"$file_base"* ]]; then
            reference_count=$((reference_count + 1))
        fi
    done

    if [[ $reference_count -ge 6 ]]; then
        echo "  ✓ SKILL.md references at least 6 error-type files (found: $reference_count)" >> "$TEST_LOG"
        return 0
    else
        echo "ASSERTION FAILED: SKILL.md references fewer than 6 error-type files (found: $reference_count)" >> "$TEST_LOG"
        return 1
    fi
}

##############################################################################
# Run All Tests
##############################################################################

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}STORY-145 AC#4: SKILL.md References${NC}"
echo -e "${BLUE}========================================${NC}"

run_test "SKILL.md exists" test_skill_file_exists
run_test "SKILL.md is readable" test_skill_file_readable

run_test "SKILL.md has Error Handling section" test_skill_has_error_handling_section

run_test "SKILL.md references error-type-1-incomplete-answers" test_skill_references_error_type_1
run_test "SKILL.md references error-type-2-artifact-failures" test_skill_references_error_type_2
run_test "SKILL.md references error-type-3-complexity-errors" test_skill_references_error_type_3
run_test "SKILL.md references error-type-4-validation-failures" test_skill_references_error_type_4
run_test "SKILL.md references error-type-5-constraint-conflicts" test_skill_references_error_type_5
run_test "SKILL.md references error-type-6-directory-issues" test_skill_references_error_type_6

run_test "SKILL.md references error-handling-index" test_skill_references_index

run_test "All 6 error-type files referenced in SKILL.md" test_all_error_types_in_skill
run_test "SKILL.md has at least 6 error-type references" test_skill_has_at_least_6_references

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
