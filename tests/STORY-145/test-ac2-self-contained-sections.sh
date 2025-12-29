#!/bin/bash

##############################################################################
# Test Suite: STORY-145 AC#2 - Self-Contained Error-Type Files
# Purpose: Validate that each error-type file has required sections
#
# Acceptance Criteria #2:
# Given an error-type file exists (e.g., error-type-1-incomplete-answers.md),
# When the file is loaded during error handling,
# Then it contains:
#   - Error detection logic (when does this error occur?)
#   - Recovery procedures (self-heal → retry → report)
#   - Example scenarios
#   - Related patterns (cross-reference to other error types if needed)
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
TEST_LOG="/tmp/story-145-ac2.log"

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/../.."
REFERENCES_DIR="${PROJECT_ROOT}/.claude/skills/devforgeai-ideation/references"

# Required sections for each file
declare -a REQUIRED_SECTIONS=(
    "## Error Detection"
    "## Recovery Procedures"
    "## Example Scenarios"
)

# All 6 error-type files
declare -a ERROR_TYPE_FILES=(
    "error-type-1-incomplete-answers.md"
    "error-type-2-artifact-failures.md"
    "error-type-3-complexity-errors.md"
    "error-type-4-validation-failures.md"
    "error-type-5-constraint-conflicts.md"
    "error-type-6-directory-issues.md"
)

# Initialize log
echo "=== STORY-145 AC#2 Test Suite ===" > "$TEST_LOG"
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

assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="${3:-String should contain substring}"

    if [[ "$haystack" == *"$needle"* ]]; then
        return 0
    else
        echo "ASSERTION FAILED: $message" >> "$TEST_LOG"
        echo "  ✗ Expected to find: '$needle'" >> "$TEST_LOG"
        echo "  ✗ In string (first 200 chars): ${haystack:0:200}" >> "$TEST_LOG"
        return 1
    fi
}

assert_file_has_section() {
    local file_path=$1
    local section_name=$2
    local message="${3:-File should contain section}"

    if [[ ! -f "$file_path" ]]; then
        echo "ASSERTION FAILED: File not found" >> "$TEST_LOG"
        echo "  ✗ File: $file_path" >> "$TEST_LOG"
        return 1
    fi

    local file_content
    file_content=$(cat "$file_path")

    if [[ "$file_content" == *"$section_name"* ]]; then
        echo "  ✓ Section found: $section_name" >> "$TEST_LOG"
        return 0
    else
        echo "ASSERTION FAILED: $message" >> "$TEST_LOG"
        echo "  ✗ File: $file_path" >> "$TEST_LOG"
        echo "  ✗ Missing section: $section_name" >> "$TEST_LOG"
        return 1
    fi
}

##############################################################################
# Test Cases: Error Type 1 - Incomplete Answers
##############################################################################

test_error_type_1_has_error_detection() {
    assert_file_has_section \
        "${REFERENCES_DIR}/error-type-1-incomplete-answers.md" \
        "## Error Detection" \
        "error-type-1 should have Error Detection section"
}

test_error_type_1_has_recovery_procedures() {
    assert_file_has_section \
        "${REFERENCES_DIR}/error-type-1-incomplete-answers.md" \
        "## Recovery Procedures" \
        "error-type-1 should have Recovery Procedures section"
}

test_error_type_1_has_example_scenarios() {
    assert_file_has_section \
        "${REFERENCES_DIR}/error-type-1-incomplete-answers.md" \
        "## Example Scenarios" \
        "error-type-1 should have Example Scenarios section"
}

##############################################################################
# Test Cases: Error Type 2 - Artifact Failures
##############################################################################

test_error_type_2_has_error_detection() {
    assert_file_has_section \
        "${REFERENCES_DIR}/error-type-2-artifact-failures.md" \
        "## Error Detection" \
        "error-type-2 should have Error Detection section"
}

test_error_type_2_has_recovery_procedures() {
    assert_file_has_section \
        "${REFERENCES_DIR}/error-type-2-artifact-failures.md" \
        "## Recovery Procedures" \
        "error-type-2 should have Recovery Procedures section"
}

test_error_type_2_has_example_scenarios() {
    assert_file_has_section \
        "${REFERENCES_DIR}/error-type-2-artifact-failures.md" \
        "## Example Scenarios" \
        "error-type-2 should have Example Scenarios section"
}

##############################################################################
# Test Cases: Error Type 3 - Complexity Errors
##############################################################################

test_error_type_3_has_error_detection() {
    assert_file_has_section \
        "${REFERENCES_DIR}/error-type-3-complexity-errors.md" \
        "## Error Detection" \
        "error-type-3 should have Error Detection section"
}

test_error_type_3_has_recovery_procedures() {
    assert_file_has_section \
        "${REFERENCES_DIR}/error-type-3-complexity-errors.md" \
        "## Recovery Procedures" \
        "error-type-3 should have Recovery Procedures section"
}

test_error_type_3_has_example_scenarios() {
    assert_file_has_section \
        "${REFERENCES_DIR}/error-type-3-complexity-errors.md" \
        "## Example Scenarios" \
        "error-type-3 should have Example Scenarios section"
}

##############################################################################
# Test Cases: Error Type 4 - Validation Failures
##############################################################################

test_error_type_4_has_error_detection() {
    assert_file_has_section \
        "${REFERENCES_DIR}/error-type-4-validation-failures.md" \
        "## Error Detection" \
        "error-type-4 should have Error Detection section"
}

test_error_type_4_has_recovery_procedures() {
    assert_file_has_section \
        "${REFERENCES_DIR}/error-type-4-validation-failures.md" \
        "## Recovery Procedures" \
        "error-type-4 should have Recovery Procedures section"
}

test_error_type_4_has_example_scenarios() {
    assert_file_has_section \
        "${REFERENCES_DIR}/error-type-4-validation-failures.md" \
        "## Example Scenarios" \
        "error-type-4 should have Example Scenarios section"
}

##############################################################################
# Test Cases: Error Type 5 - Constraint Conflicts
##############################################################################

test_error_type_5_has_error_detection() {
    assert_file_has_section \
        "${REFERENCES_DIR}/error-type-5-constraint-conflicts.md" \
        "## Error Detection" \
        "error-type-5 should have Error Detection section"
}

test_error_type_5_has_recovery_procedures() {
    assert_file_has_section \
        "${REFERENCES_DIR}/error-type-5-constraint-conflicts.md" \
        "## Recovery Procedures" \
        "error-type-5 should have Recovery Procedures section"
}

test_error_type_5_has_example_scenarios() {
    assert_file_has_section \
        "${REFERENCES_DIR}/error-type-5-constraint-conflicts.md" \
        "## Example Scenarios" \
        "error-type-5 should have Example Scenarios section"
}

##############################################################################
# Test Cases: Error Type 6 - Directory Issues
##############################################################################

test_error_type_6_has_error_detection() {
    assert_file_has_section \
        "${REFERENCES_DIR}/error-type-6-directory-issues.md" \
        "## Error Detection" \
        "error-type-6 should have Error Detection section"
}

test_error_type_6_has_recovery_procedures() {
    assert_file_has_section \
        "${REFERENCES_DIR}/error-type-6-directory-issues.md" \
        "## Recovery Procedures" \
        "error-type-6 should have Recovery Procedures section"
}

test_error_type_6_has_example_scenarios() {
    assert_file_has_section \
        "${REFERENCES_DIR}/error-type-6-directory-issues.md" \
        "## Example Scenarios" \
        "error-type-6 should have Example Scenarios section"
}

##############################################################################
# Comprehensive Test: All files have all required sections
##############################################################################

test_all_files_have_all_required_sections() {
    local all_valid=true

    for file in "${ERROR_TYPE_FILES[@]}"; do
        local file_path="${REFERENCES_DIR}/${file}"

        if [[ ! -f "$file_path" ]]; then
            echo "  ✗ File not found: $file" >> "$TEST_LOG"
            all_valid=false
            continue
        fi

        local file_content
        file_content=$(cat "$file_path")

        for section in "${REQUIRED_SECTIONS[@]}"; do
            if [[ "$file_content" != *"$section"* ]]; then
                echo "  ✗ $file missing section: $section" >> "$TEST_LOG"
                all_valid=false
            fi
        done
    done

    if [[ "$all_valid" == true ]]; then
        echo "  ✓ All 6 files contain all required sections" >> "$TEST_LOG"
        return 0
    else
        return 1
    fi
}

##############################################################################
# Run All Tests
##############################################################################

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}STORY-145 AC#2: Self-Contained Files${NC}"
echo -e "${BLUE}========================================${NC}"

run_test "error-type-1 has Error Detection section" test_error_type_1_has_error_detection
run_test "error-type-1 has Recovery Procedures section" test_error_type_1_has_recovery_procedures
run_test "error-type-1 has Example Scenarios section" test_error_type_1_has_example_scenarios

run_test "error-type-2 has Error Detection section" test_error_type_2_has_error_detection
run_test "error-type-2 has Recovery Procedures section" test_error_type_2_has_recovery_procedures
run_test "error-type-2 has Example Scenarios section" test_error_type_2_has_example_scenarios

run_test "error-type-3 has Error Detection section" test_error_type_3_has_error_detection
run_test "error-type-3 has Recovery Procedures section" test_error_type_3_has_recovery_procedures
run_test "error-type-3 has Example Scenarios section" test_error_type_3_has_example_scenarios

run_test "error-type-4 has Error Detection section" test_error_type_4_has_error_detection
run_test "error-type-4 has Recovery Procedures section" test_error_type_4_has_recovery_procedures
run_test "error-type-4 has Example Scenarios section" test_error_type_4_has_example_scenarios

run_test "error-type-5 has Error Detection section" test_error_type_5_has_error_detection
run_test "error-type-5 has Recovery Procedures section" test_error_type_5_has_recovery_procedures
run_test "error-type-5 has Example Scenarios section" test_error_type_5_has_example_scenarios

run_test "error-type-6 has Error Detection section" test_error_type_6_has_error_detection
run_test "error-type-6 has Recovery Procedures section" test_error_type_6_has_recovery_procedures
run_test "error-type-6 has Example Scenarios section" test_error_type_6_has_example_scenarios

run_test "All files have all required sections" test_all_files_have_all_required_sections

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
