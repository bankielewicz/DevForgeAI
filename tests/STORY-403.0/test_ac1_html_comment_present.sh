#!/bin/bash
# Test AC#1: HTML Comment Block Present in Story Template
# STORY-403: Document Implementation Notes Format in Story Template
#
# Validates:
# - An HTML comment block exists within or adjacent to the Definition of Done section
# - Comment is between DoD section and Change Log section
#
# Expected: FAIL initially (TDD Red phase - comment does not exist yet)

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEMPLATE_FILE="$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/assets/templates/story-template.md"

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
# Test 1: Template file exists
# -----------------------------------------------------------------------------
test_template_file_exists() {
    local test_name="Template file exists"
    if [ -f "$TEMPLATE_FILE" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "File not found: $TEMPLATE_FILE"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: HTML comment block exists in template
# -----------------------------------------------------------------------------
test_html_comment_exists() {
    local test_name="HTML comment block exists in template"

    if [ ! -f "$TEMPLATE_FILE" ]; then
        fail_test "$test_name" "Cannot check - template file does not exist"
        return
    fi

    # Look for an HTML comment that contains "IMPLEMENTATION NOTES FORMAT"
    if grep -q '<!--.*IMPLEMENTATION NOTES FORMAT' "$TEMPLATE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No HTML comment with 'IMPLEMENTATION NOTES FORMAT' found in template"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: Comment is located in DoD section area
# -----------------------------------------------------------------------------
test_comment_in_dod_area() {
    local test_name="Comment located in Definition of Done section area"

    if [ ! -f "$TEMPLATE_FILE" ]; then
        fail_test "$test_name" "Cannot check - template file does not exist"
        return
    fi

    # Get line numbers for DoD section and Change Log section
    local dod_line
    dod_line=$(grep -n "^## Definition of Done" "$TEMPLATE_FILE" | head -1 | cut -d: -f1)

    local changelog_line
    changelog_line=$(grep -n "^## Change Log" "$TEMPLATE_FILE" | head -1 | cut -d: -f1)

    local comment_line
    comment_line=$(grep -n '<!--.*IMPLEMENTATION NOTES FORMAT' "$TEMPLATE_FILE" | head -1 | cut -d: -f1)

    if [ -z "$dod_line" ]; then
        fail_test "$test_name" "## Definition of Done section not found in template"
        return
    fi

    if [ -z "$comment_line" ]; then
        fail_test "$test_name" "Implementation Notes Format comment not found"
        return
    fi

    if [ -z "$changelog_line" ]; then
        fail_test "$test_name" "## Change Log section not found in template"
        return
    fi

    # Comment should be within or immediately adjacent to DoD section (within 15 lines before or after)
    # Per AC#1: "within or immediately adjacent to the ## Definition of Done section"
    local adjacent_threshold=15
    local before_dod=$((dod_line - comment_line))
    local after_dod=$((comment_line - dod_line))

    if [ "$comment_line" -lt "$changelog_line" ] && { [ "$before_dod" -ge 0 ] && [ "$before_dod" -le "$adjacent_threshold" ]; } || { [ "$after_dod" -ge 0 ] && [ "$comment_line" -lt "$changelog_line" ]; }; then
        pass_test "$test_name (line $comment_line, DoD at $dod_line)"
    else
        fail_test "$test_name" "Comment at line $comment_line is outside DoD area (DoD: $dod_line, ChangeLog: $changelog_line)"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Comment block is properly closed
# -----------------------------------------------------------------------------
test_comment_properly_closed() {
    local test_name="HTML comment block is properly closed"

    if [ ! -f "$TEMPLATE_FILE" ]; then
        fail_test "$test_name" "Cannot check - template file does not exist"
        return
    fi

    # Check for opening <!-- and closing --> around the Implementation Notes Format comment
    local comment_start
    comment_start=$(grep -n '<!--.*IMPLEMENTATION NOTES FORMAT' "$TEMPLATE_FILE" | head -1 | cut -d: -f1)

    if [ -z "$comment_start" ]; then
        fail_test "$test_name" "Comment block not found"
        return
    fi

    # Look for closing --> after the comment start
    local has_closing
    has_closing=$(sed -n "${comment_start},\$p" "$TEMPLATE_FILE" | grep -c '\-\->')

    if [ "$has_closing" -gt 0 ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Comment starting at line $comment_start has no closing -->"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-403 AC#1: HTML Comment Block Present"
echo "=============================================="
echo "Target file: $TEMPLATE_FILE"
echo "----------------------------------------------"
echo ""

run_test "1" test_template_file_exists
run_test "2" test_html_comment_exists
run_test "3" test_comment_in_dod_area
run_test "4" test_comment_properly_closed

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
