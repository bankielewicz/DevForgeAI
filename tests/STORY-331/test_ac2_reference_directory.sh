#!/bin/bash
# Test AC#2: Reference Directory Structure
# STORY-331: Refactor agent-generator.md with Progressive Disclosure
#
# Validates:
# - Directory src/claude/agents/agent-generator/references/ exists
# - Contains 6-10 reference files
# - All files use lowercase-hyphen naming (no underscores, no CamelCase)
#
# Expected: FAIL initially (TDD Red phase - directory does not exist yet)

# Note: Not using set -e due to arithmetic operations with (( ))

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
REF_DIR="$PROJECT_ROOT/src/claude/agents/agent-generator/references"
MIN_FILES=6
MAX_FILES=10

# Test tracking
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test helper functions
pass_test() {
    local test_name="$1"
    TESTS_PASSED=$((TESTS_PASSED + 1))
    echo "[PASS] $test_name"
}

fail_test() {
    local test_name="$1"
    local message="$2"
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo "[FAIL] $test_name: $message"
}

run_test() {
    local test_name="$1"
    TESTS_RUN=$((TESTS_RUN + 1))
    shift
    "$@"
}

# -----------------------------------------------------------------------------
# Test 1: Reference directory exists
# -----------------------------------------------------------------------------
test_reference_directory_exists() {
    local test_name="Reference directory exists"

    if [ -d "$REF_DIR" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Directory not found: $REF_DIR"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: Reference directory contains files
# -----------------------------------------------------------------------------
test_reference_directory_not_empty() {
    local test_name="Reference directory contains files"

    if [ ! -d "$REF_DIR" ]; then
        fail_test "$test_name" "Cannot check - directory does not exist"
        return
    fi

    local file_count
    file_count=$(find "$REF_DIR" -maxdepth 1 -type f -name "*.md" | wc -l)

    if [ "$file_count" -gt 0 ]; then
        pass_test "$test_name (found $file_count files)"
    else
        fail_test "$test_name" "No .md files found in reference directory"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: File count within range (6-10)
# -----------------------------------------------------------------------------
test_file_count_in_range() {
    local test_name="Reference file count in range ($MIN_FILES-$MAX_FILES)"

    if [ ! -d "$REF_DIR" ]; then
        fail_test "$test_name" "Cannot check - directory does not exist"
        return
    fi

    local file_count
    file_count=$(find "$REF_DIR" -maxdepth 1 -type f -name "*.md" | wc -l)

    if [ "$file_count" -ge "$MIN_FILES" ] && [ "$file_count" -le "$MAX_FILES" ]; then
        pass_test "$test_name (actual: $file_count files)"
    else
        fail_test "$test_name" "Found $file_count files (expected $MIN_FILES-$MAX_FILES)"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: All files use lowercase-hyphen naming
# -----------------------------------------------------------------------------
test_lowercase_hyphen_naming() {
    local test_name="All files use lowercase-hyphen naming"

    if [ ! -d "$REF_DIR" ]; then
        fail_test "$test_name" "Cannot check - directory does not exist"
        return
    fi

    local invalid_files=""

    # Find files that DON'T match the lowercase-hyphen pattern
    # Pattern: starts with lowercase letter, contains only lowercase letters, numbers, and hyphens, ends with .md
    while IFS= read -r file; do
        local basename
        basename=$(basename "$file")

        # Check if filename matches lowercase-hyphen pattern
        if ! echo "$basename" | grep -qE '^[a-z][a-z0-9-]*\.md$'; then
            invalid_files="$invalid_files $basename"
        fi
    done < <(find "$REF_DIR" -maxdepth 1 -type f -name "*.md")

    if [ -z "$invalid_files" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Invalid file names:$invalid_files"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: No underscore in filenames
# -----------------------------------------------------------------------------
test_no_underscores() {
    local test_name="No underscores in filenames"

    if [ ! -d "$REF_DIR" ]; then
        fail_test "$test_name" "Cannot check - directory does not exist"
        return
    fi

    local files_with_underscores
    files_with_underscores=$(find "$REF_DIR" -maxdepth 1 -type f -name "*_*.md" | wc -l)

    if [ "$files_with_underscores" -eq 0 ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Found $files_with_underscores files with underscores"
    fi
}

# -----------------------------------------------------------------------------
# Test 6: No uppercase in filenames
# -----------------------------------------------------------------------------
test_no_uppercase() {
    local test_name="No uppercase letters in filenames"

    if [ ! -d "$REF_DIR" ]; then
        fail_test "$test_name" "Cannot check - directory does not exist"
        return
    fi

    local uppercase_files=""

    while IFS= read -r file; do
        local basename
        basename=$(basename "$file")

        if echo "$basename" | grep -q '[A-Z]'; then
            uppercase_files="$uppercase_files $basename"
        fi
    done < <(find "$REF_DIR" -maxdepth 1 -type f -name "*.md")

    if [ -z "$uppercase_files" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Files with uppercase:$uppercase_files"
    fi
}

# -----------------------------------------------------------------------------
# Test 7: Expected reference files present
# -----------------------------------------------------------------------------
test_expected_files_present() {
    local test_name="Expected reference files present"

    if [ ! -d "$REF_DIR" ]; then
        fail_test "$test_name" "Cannot check - directory does not exist"
        return
    fi

    # Core expected files per story specification
    local expected_files=(
        "template-patterns.md"
        "frontmatter-specification.md"
        "tool-restrictions.md"
        "output-formats.md"
        "validation-workflow.md"
        "error-handling.md"
    )

    local missing_files=""

    for expected in "${expected_files[@]}"; do
        if [ ! -f "$REF_DIR/$expected" ]; then
            missing_files="$missing_files $expected"
        fi
    done

    if [ -z "$missing_files" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Missing files:$missing_files"
    fi
}

# -----------------------------------------------------------------------------
# Test 8: All reference files are valid markdown
# -----------------------------------------------------------------------------
test_valid_markdown_files() {
    local test_name="All reference files are valid markdown (start with heading)"

    if [ ! -d "$REF_DIR" ]; then
        fail_test "$test_name" "Cannot check - directory does not exist"
        return
    fi

    local invalid_files=""

    while IFS= read -r file; do
        local basename
        basename=$(basename "$file")

        # Check if file starts with a heading (# Title) within first 10 lines
        if ! head -n 10 "$file" | grep -qE '^#'; then
            invalid_files="$invalid_files $basename"
        fi
    done < <(find "$REF_DIR" -maxdepth 1 -type f -name "*.md")

    if [ -z "$invalid_files" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Files without heading:$invalid_files"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-331 AC#2: Reference Directory Structure"
echo "=============================================="
echo "Target directory: $REF_DIR"
echo "Expected file count: $MIN_FILES-$MAX_FILES"
echo "----------------------------------------------"
echo ""

run_test "1" test_reference_directory_exists
run_test "2" test_reference_directory_not_empty
run_test "3" test_file_count_in_range
run_test "4" test_lowercase_hyphen_naming
run_test "5" test_no_underscores
run_test "6" test_no_uppercase
run_test "7" test_expected_files_present
run_test "8" test_valid_markdown_files

echo ""
echo "=============================================="
echo "Test Summary: $TESTS_PASSED/$TESTS_RUN passed"
echo "=============================================="

if [ "$TESTS_FAILED" -gt 0 ]; then
    echo "Status: FAILED ($TESTS_FAILED failures)"
    exit 1
else
    echo "Status: PASSED"
    exit 0
fi
