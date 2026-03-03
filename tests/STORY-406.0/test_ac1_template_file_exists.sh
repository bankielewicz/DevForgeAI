#!/bin/bash
# Test AC#1: Template file created at canonical location
# STORY-406: Create Batch Sibling Story Session Template
#
# Validates:
# - File exists at src/claude/memory/batch-sibling-story-session-template.md
# - File is non-empty and valid Markdown (readable)
#
# Expected: FAIL initially (TDD Red phase - file does not exist yet)

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET_FILE="$PROJECT_ROOT/src/claude/memory/batch-sibling-story-session-template.md"

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
# Test 1: Target file exists
# -----------------------------------------------------------------------------
test_file_exists() {
    local test_name="File exists at canonical location"
    if [ -f "$TARGET_FILE" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "File not found: $TARGET_FILE"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: File is non-empty
# -----------------------------------------------------------------------------
test_file_non_empty() {
    local test_name="File is non-empty"
    if [ ! -f "$TARGET_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    local size
    size=$(wc -c < "$TARGET_FILE")
    if [ "$size" -gt 0 ]; then
        pass_test "$test_name ($size bytes)"
    else
        fail_test "$test_name" "File is empty (0 bytes)"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: File starts with Markdown heading (or YAML frontmatter then heading)
# -----------------------------------------------------------------------------
test_valid_markdown_heading() {
    local test_name="File starts with a Markdown heading"
    if [ ! -f "$TARGET_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    # Check if file has YAML frontmatter (starts with ---)
    local first_line
    first_line=$(head -n1 "$TARGET_FILE")

    if [ "$first_line" = "---" ]; then
        # Has YAML frontmatter - find the first # heading after the closing ---
        local heading_found
        heading_found=$(awk '/^---$/{if(++c==2){found=1;next}} found && /^#/{print;exit}' "$TARGET_FILE")
        if [ -n "$heading_found" ]; then
            pass_test "$test_name (with YAML frontmatter)"
        else
            fail_test "$test_name" "No Markdown heading found after YAML frontmatter"
        fi
    else
        # No frontmatter - first non-blank should be heading
        local first_nonblank
        first_nonblank=$(grep -m1 -E '^\S' "$TARGET_FILE")
        if echo "$first_nonblank" | grep -q '^#'; then
            pass_test "$test_name"
        else
            fail_test "$test_name" "First non-blank line does not start with '#': $first_nonblank"
        fi
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-406 AC#1: Template File at Canonical Location"
echo "=============================================="
echo "Target file: $TARGET_FILE"
echo "----------------------------------------------"
echo ""

run_test "1" test_file_exists
run_test "2" test_file_non_empty
run_test "3" test_valid_markdown_heading

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
