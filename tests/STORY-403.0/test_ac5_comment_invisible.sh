#!/bin/bash
# Test AC#5: Comment Is Invisible in Rendered Markdown
# STORY-403: Document Implementation Notes Format in Story Template
#
# Validates:
# - HTML comment uses proper syntax (<!-- ... -->)
# - Comment opens with <!-- and closes with -->
# - No malformed comment tags that would render visibly
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
# Test 1: Comment starts with proper <!-- syntax
# -----------------------------------------------------------------------------
test_comment_opens_correctly() {
    local test_name="Comment starts with <!-- syntax"

    if [ ! -f "$TEMPLATE_FILE" ]; then
        fail_test "$test_name" "Template file not found"
        return
    fi

    if grep -q '<!-- IMPLEMENTATION NOTES FORMAT' "$TEMPLATE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No properly opened <!-- IMPLEMENTATION NOTES FORMAT comment found"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: Comment ends with proper --> syntax
# -----------------------------------------------------------------------------
test_comment_closes_correctly() {
    local test_name="Comment ends with --> syntax"

    if [ ! -f "$TEMPLATE_FILE" ]; then
        fail_test "$test_name" "Template file not found"
        return
    fi

    local comment_start
    comment_start=$(grep -n '<!-- IMPLEMENTATION NOTES FORMAT' "$TEMPLATE_FILE" | head -1 | cut -d: -f1)

    if [ -z "$comment_start" ]; then
        fail_test "$test_name" "Comment block not found"
        return
    fi

    # Find the next --> after the comment start
    local close_line
    close_line=$(sed -n "${comment_start},\$p" "$TEMPLATE_FILE" | grep -n '\-\->' | head -1 | cut -d: -f1)

    if [ -n "$close_line" ] && [ "$close_line" -gt 0 ]; then
        pass_test "$test_name (closes at relative line $close_line)"
    else
        fail_test "$test_name" "No closing --> found after comment start at line $comment_start"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: No --> appears inside the comment body (would prematurely close it)
# -----------------------------------------------------------------------------
test_no_premature_closing() {
    local test_name="No premature --> inside comment body"

    if [ ! -f "$TEMPLATE_FILE" ]; then
        fail_test "$test_name" "Template file not found"
        return
    fi

    local comment_start
    comment_start=$(grep -n '<!-- IMPLEMENTATION NOTES FORMAT' "$TEMPLATE_FILE" | head -1 | cut -d: -f1)

    if [ -z "$comment_start" ]; then
        fail_test "$test_name" "Comment block not found"
        return
    fi

    # Count occurrences of --> after comment start
    local close_count
    close_count=$(sed -n "${comment_start},\$p" "$TEMPLATE_FILE" | grep -c '\-\->')

    # There should be exactly 1 closing --> (the actual end of the comment)
    # But we need to check only until the next ## section to be safe
    local next_section
    next_section=$(sed -n "$((comment_start + 1)),\$p" "$TEMPLATE_FILE" | grep -n '^## ' | head -1 | cut -d: -f1)

    if [ -n "$next_section" ]; then
        next_section=$((comment_start + next_section))
        close_count=$(sed -n "${comment_start},${next_section}p" "$TEMPLATE_FILE" | grep -c '\-\->')
    fi

    if [ "$close_count" -eq 1 ]; then
        pass_test "$test_name (exactly 1 closing tag found)"
    else
        fail_test "$test_name" "Found $close_count occurrences of --> (expected exactly 1)"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Comment does not contain nested <!-- (would break rendering)
# -----------------------------------------------------------------------------
test_no_nested_opening() {
    local test_name="No nested <!-- inside comment body"

    if [ ! -f "$TEMPLATE_FILE" ]; then
        fail_test "$test_name" "Template file not found"
        return
    fi

    local comment_start
    comment_start=$(grep -n '<!-- IMPLEMENTATION NOTES FORMAT' "$TEMPLATE_FILE" | head -1 | cut -d: -f1)

    if [ -z "$comment_start" ]; then
        fail_test "$test_name" "Comment block not found"
        return
    fi

    # Count <!-- in the comment block (starting from line after the opening)
    local next_section
    next_section=$(sed -n "$((comment_start + 1)),\$p" "$TEMPLATE_FILE" | grep -n '^## ' | head -1 | cut -d: -f1)

    local nested_count
    if [ -n "$next_section" ]; then
        next_section=$((comment_start + next_section))
        nested_count=$(sed -n "$((comment_start + 1)),${next_section}p" "$TEMPLATE_FILE" | grep -c '<!--')
    else
        nested_count=$(sed -n "$((comment_start + 1)),\$p" "$TEMPLATE_FILE" | grep -c '<!--')
    fi

    if [ "$nested_count" -eq 0 ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Found $nested_count nested <!-- tags inside comment body"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-403 AC#5: Comment Invisible in Rendered"
echo "=============================================="
echo "Target file: $TEMPLATE_FILE"
echo "----------------------------------------------"
echo ""

run_test "1" test_comment_opens_correctly
run_test "2" test_comment_closes_correctly
run_test "3" test_no_premature_closing
run_test "4" test_no_nested_opening

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
