#!/bin/bash
# Test AC#2: Reference Directory Structure Created
# STORY-401: Extract Anti-Pattern-Scanner to Reference Files
#
# Validates:
# - Directory src/claude/agents/anti-pattern-scanner/references/ exists
# - Contains exactly 2 files: integration-testing-guide.md and metrics-reference.md
# - Files use lowercase-hyphen naming
#
# Expected: FAIL initially (TDD Red phase - directory does not exist yet)

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
REF_DIR="$PROJECT_ROOT/src/claude/agents/anti-pattern-scanner/references"
EXPECTED_FILE_COUNT=2

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
# Test 2: Exactly 2 reference files present
# -----------------------------------------------------------------------------
test_exact_file_count() {
    local test_name="Reference directory contains exactly $EXPECTED_FILE_COUNT files"

    if [ ! -d "$REF_DIR" ]; then
        fail_test "$test_name" "Cannot check - directory does not exist"
        return
    fi

    local file_count
    file_count=$(find "$REF_DIR" -maxdepth 1 -type f -name "*.md" | wc -l)

    if [ "$file_count" -eq "$EXPECTED_FILE_COUNT" ]; then
        pass_test "$test_name (found $file_count files)"
    else
        fail_test "$test_name" "Found $file_count files (expected exactly $EXPECTED_FILE_COUNT)"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: integration-testing-guide.md exists
# -----------------------------------------------------------------------------
test_integration_testing_guide_exists() {
    local test_name="integration-testing-guide.md exists"

    if [ ! -d "$REF_DIR" ]; then
        fail_test "$test_name" "Cannot check - directory does not exist"
        return
    fi

    if [ -f "$REF_DIR/integration-testing-guide.md" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "File not found: $REF_DIR/integration-testing-guide.md"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: metrics-reference.md exists
# -----------------------------------------------------------------------------
test_metrics_reference_exists() {
    local test_name="metrics-reference.md exists"

    if [ ! -d "$REF_DIR" ]; then
        fail_test "$test_name" "Cannot check - directory does not exist"
        return
    fi

    if [ -f "$REF_DIR/metrics-reference.md" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "File not found: $REF_DIR/metrics-reference.md"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: All files use lowercase-hyphen naming
# -----------------------------------------------------------------------------
test_lowercase_hyphen_naming() {
    local test_name="All files use lowercase-hyphen naming"

    if [ ! -d "$REF_DIR" ]; then
        fail_test "$test_name" "Cannot check - directory does not exist"
        return
    fi

    local invalid_files=""

    while IFS= read -r file; do
        local basename
        basename=$(basename "$file")

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
# Test 6: Reference files start with markdown heading
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
echo "STORY-401 AC#2: Reference Directory Structure"
echo "=============================================="
echo "Target directory: $REF_DIR"
echo "Expected file count: $EXPECTED_FILE_COUNT"
echo "----------------------------------------------"
echo ""

run_test "1" test_reference_directory_exists
run_test "2" test_exact_file_count
run_test "3" test_integration_testing_guide_exists
run_test "4" test_metrics_reference_exists
run_test "5" test_lowercase_hyphen_naming
run_test "6" test_valid_markdown_files

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
