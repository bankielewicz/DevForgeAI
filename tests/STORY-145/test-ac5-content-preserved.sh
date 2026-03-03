#!/bin/bash

##############################################################################
# Test Suite: STORY-145 AC#5 - All Original Content Preserved
# Purpose: Validate that total line count >= original 1,062 lines
#
# Acceptance Criteria #5:
# Given error-handling.md contained ~1,062 lines,
# When content is distributed across 6 files + index,
# Then total line count across all 7 files equals or exceeds original (no content loss).
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
TEST_LOG="/tmp/story-145-ac5.log"

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/../.."
REFERENCES_DIR="${PROJECT_ROOT}/.claude/skills/devforgeai-ideation/references"
ORIGINAL_FILE="${REFERENCES_DIR}/error-handling.md"

# All files to check line counts
declare -a ERROR_TYPE_FILES=(
    "error-type-1-incomplete-answers.md"
    "error-type-2-artifact-failures.md"
    "error-type-3-complexity-errors.md"
    "error-type-4-validation-failures.md"
    "error-type-5-constraint-conflicts.md"
    "error-type-6-directory-issues.md"
)

# Original line count requirement
ORIGINAL_LINE_COUNT=1062
MIN_REQUIRED=$ORIGINAL_LINE_COUNT

# Initialize log
echo "=== STORY-145 AC#5 Test Suite ===" > "$TEST_LOG"
echo "Test Started: $(date)" >> "$TEST_LOG"
echo "References Directory: ${REFERENCES_DIR}" >> "$TEST_LOG"
echo "Minimum required line count: $MIN_REQUIRED" >> "$TEST_LOG"

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

get_line_count() {
    local file_path=$1

    if [[ ! -f "$file_path" ]]; then
        echo 0
        return 1
    fi

    wc -l < "$file_path"
}

##############################################################################
# Test Cases for AC#5
##############################################################################

test_total_content_preserved() {
    if [[ ! -f "$ORIGINAL_FILE" ]]; then
        # If original file doesn't exist, we cannot verify (but this is acceptable)
        # The split operation should have consumed it
        echo "  ℹ Original file (error-handling.md) not found (expected: consumed)" >> "$TEST_LOG"
    fi

    local total_lines=0

    # Count lines in all 6 error-type files
    for file in "${ERROR_TYPE_FILES[@]}"; do
        local file_path="${REFERENCES_DIR}/${file}"

        if [[ -f "$file_path" ]]; then
            local line_count
            line_count=$(wc -l < "$file_path")
            total_lines=$((total_lines + line_count))
            echo "  $file: $line_count lines" >> "$TEST_LOG"
        else
            echo "  ✗ File not found: $file" >> "$TEST_LOG"
        fi
    done

    # Count lines in index file
    local index_file="${REFERENCES_DIR}/error-handling-index.md"
    if [[ -f "$index_file" ]]; then
        local index_lines
        index_lines=$(wc -l < "$index_file")
        total_lines=$((total_lines + index_lines))
        echo "  error-handling-index.md: $index_lines lines" >> "$TEST_LOG"
    fi

    echo "  Total lines across all new files: $total_lines" >> "$TEST_LOG"
    echo "  Minimum required: $MIN_REQUIRED" >> "$TEST_LOG"

    if [[ $total_lines -ge $MIN_REQUIRED ]]; then
        echo "  ✓ Content preserved (total: $total_lines >= required: $MIN_REQUIRED)" >> "$TEST_LOG"
        return 0
    else
        echo "ASSERTION FAILED: Content loss detected" >> "$TEST_LOG"
        echo "  ✗ Total lines ($total_lines) < required ($MIN_REQUIRED)" >> "$TEST_LOG"
        return 1
    fi
}

test_error_type_1_has_lines() {
    local file_path="${REFERENCES_DIR}/error-type-1-incomplete-answers.md"

    if [[ ! -f "$file_path" ]]; then
        echo "ASSERTION FAILED: File not found" >> "$TEST_LOG"
        echo "  ✗ File: $file_path" >> "$TEST_LOG"
        return 1
    fi

    local line_count
    line_count=$(wc -l < "$file_path")

    echo "  error-type-1: $line_count lines" >> "$TEST_LOG"

    if [[ $line_count -gt 0 ]]; then
        return 0
    else
        return 1
    fi
}

test_error_type_2_has_lines() {
    local file_path="${REFERENCES_DIR}/error-type-2-artifact-failures.md"

    if [[ ! -f "$file_path" ]]; then
        echo "ASSERTION FAILED: File not found" >> "$TEST_LOG"
        echo "  ✗ File: $file_path" >> "$TEST_LOG"
        return 1
    fi

    local line_count
    line_count=$(wc -l < "$file_path")

    echo "  error-type-2: $line_count lines" >> "$TEST_LOG"

    if [[ $line_count -gt 0 ]]; then
        return 0
    else
        return 1
    fi
}

test_error_type_3_has_lines() {
    local file_path="${REFERENCES_DIR}/error-type-3-complexity-errors.md"

    if [[ ! -f "$file_path" ]]; then
        echo "ASSERTION FAILED: File not found" >> "$TEST_LOG"
        echo "  ✗ File: $file_path" >> "$TEST_LOG"
        return 1
    fi

    local line_count
    line_count=$(wc -l < "$file_path")

    echo "  error-type-3: $line_count lines" >> "$TEST_LOG"

    if [[ $line_count -gt 0 ]]; then
        return 0
    else
        return 1
    fi
}

test_error_type_4_has_lines() {
    local file_path="${REFERENCES_DIR}/error-type-4-validation-failures.md"

    if [[ ! -f "$file_path" ]]; then
        echo "ASSERTION FAILED: File not found" >> "$TEST_LOG"
        echo "  ✗ File: $file_path" >> "$TEST_LOG"
        return 1
    fi

    local line_count
    line_count=$(wc -l < "$file_path")

    echo "  error-type-4: $line_count lines" >> "$TEST_LOG"

    if [[ $line_count -gt 0 ]]; then
        return 0
    else
        return 1
    fi
}

test_error_type_5_has_lines() {
    local file_path="${REFERENCES_DIR}/error-type-5-constraint-conflicts.md"

    if [[ ! -f "$file_path" ]]; then
        echo "ASSERTION FAILED: File not found" >> "$TEST_LOG"
        echo "  ✗ File: $file_path" >> "$TEST_LOG"
        return 1
    fi

    local line_count
    line_count=$(wc -l < "$file_path")

    echo "  error-type-5: $line_count lines" >> "$TEST_LOG"

    if [[ $line_count -gt 0 ]]; then
        return 0
    else
        return 1
    fi
}

test_error_type_6_has_lines() {
    local file_path="${REFERENCES_DIR}/error-type-6-directory-issues.md"

    if [[ ! -f "$file_path" ]]; then
        echo "ASSERTION FAILED: File not found" >> "$TEST_LOG"
        echo "  ✗ File: $file_path" >> "$TEST_LOG"
        return 1
    fi

    local line_count
    line_count=$(wc -l < "$file_path")

    echo "  error-type-6: $line_count lines" >> "$TEST_LOG"

    if [[ $line_count -gt 0 ]]; then
        return 0
    else
        return 1
    fi
}

test_index_has_lines() {
    local file_path="${REFERENCES_DIR}/error-handling-index.md"

    if [[ ! -f "$file_path" ]]; then
        echo "ASSERTION FAILED: File not found" >> "$TEST_LOG"
        echo "  ✗ File: $file_path" >> "$TEST_LOG"
        return 1
    fi

    local line_count
    line_count=$(wc -l < "$file_path")

    echo "  error-handling-index: $line_count lines" >> "$TEST_LOG"

    if [[ $line_count -gt 0 ]]; then
        return 0
    else
        return 1
    fi
}

##############################################################################
# Run All Tests
##############################################################################

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}STORY-145 AC#5: Content Preserved${NC}"
echo -e "${BLUE}========================================${NC}"

run_test "error-type-1 has content (lines > 0)" test_error_type_1_has_lines
run_test "error-type-2 has content (lines > 0)" test_error_type_2_has_lines
run_test "error-type-3 has content (lines > 0)" test_error_type_3_has_lines
run_test "error-type-4 has content (lines > 0)" test_error_type_4_has_lines
run_test "error-type-5 has content (lines > 0)" test_error_type_5_has_lines
run_test "error-type-6 has content (lines > 0)" test_error_type_6_has_lines

run_test "error-handling-index has content (lines > 0)" test_index_has_lines

run_test "Total content preserved (>= 1,062 lines)" test_total_content_preserved

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
